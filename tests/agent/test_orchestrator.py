import pytest
from uuid import uuid4
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import settings
from src.agent.orchestrator import AgentOrchestrator
from src.agent.contracts import Intent
from src.models.user import User
from src.models.session import Session
from src.models.message import Message
from src.models.policy import PendingConfirmationModel

# Setup DB
engine = create_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        user_id = uuid4()
        user = User(id=user_id, email=f"test{user_id}@example.com")
        session.add(user)
        session.commit()
        
        session_id = uuid4()
        sess = Session(id=session_id, user_id=user_id)
        session.add(sess)
        session.commit()
        
        session.test_user_id = user_id
        session.test_session_id = session_id
        
        yield session
    finally:
        session.close()

@pytest.fixture(autouse=True)
def setup_tools():
    from src.tools.registry import register_tool, clear_registry
    from src.tools.contracts import ToolSpec
    from pydantic import BaseModel
    
    clear_registry()
    
    class SystemArgs(BaseModel):
        pass
        
    def system_tool():
        return {"message": "All systems go"}
        
    register_tool(ToolSpec(
        name="get_system_info",
        description="sys info",
        category="system",
        args_model=SystemArgs,
        side_effects=False,
        external_communication=False,
        destructive=False,
        default_action_type="READ",
        default_sensitivity="low",
        default_scope="all"
    ), system_tool)
    
    yield
    clear_registry()

def test_orchestrator_happy_path(db):
    """
    Test a clear command that maps to a tool and executes successfully.
    """
    orchestrator = AgentOrchestrator()
    
    # Mock Intent Parser to avoid LLM call
    mock_intent = Intent(
        name="get_system_info",
        slots={},
        confidence=1.0
    )
    
    with patch("src.agent.orchestrator.parse_intent", return_value=mock_intent):
        # We manually patched registry in fixture, so get_system_info exists.
        
        response = orchestrator.handle_user_utterance(
            db=db,
            user_id=db.test_user_id,
            session_id=db.test_session_id,
            utterance="System status",
            modality="text"
        )
        
        # Verify persistence
        msgs = db.query(Message).filter(Message.session_id == db.test_session_id).all()
        assert len(msgs) == 2 # User + Assistant
        assert msgs[0].role == "user"
        assert msgs[1].role == "assistant"
        
        # Verify response
        assert "Done" in response.assistant_text or "All systems go" in response.assistant_text
        assert response.should_speak is True

def test_orchestrator_ambiguity(db):
    """
    Test a command that returns needs_clarification.
    """
    orchestrator = AgentOrchestrator()
    
    mock_intent = Intent(
        name="create_calendar_event",
        slots={"subject": "Meeting"}, # Missing time
        confidence=0.8,
        needs_clarification=True,
        clarifying_question="When is the meeting?"
    )
    
    with patch("src.agent.orchestrator.parse_intent", return_value=mock_intent):
        response = orchestrator.handle_user_utterance(
            db=db,
            user_id=db.test_user_id,
            session_id=db.test_session_id,
            utterance="Schedule a meeting",
            modality="text"
        )
        
        assert response.assistant_text == "When is the meeting?"
        # Should not have executed any tool

def test_orchestrator_confirmation_loop(db):
    """
    Test the full loop: Risk -> Needs Confirm -> User Confirms -> Success
    """
    orchestrator = AgentOrchestrator()
    
    # Needs to mock Intent Parser AND The Catalog so Planner finds 'nuke_intent'
    mock_intent = Intent(
        name="nuke_intent",
        slots={"target": "all"},
        confidence=1.0
    )
    
    # Register the tool so Runtime invalidation doesn't fail
    from src.tools.registry import register_tool
    from src.tools.contracts import ToolSpec
    from pydantic import BaseModel
    
    class NukeArgs(BaseModel):
        target: str
        
    def nuke_tool(target: str):
        return {"message": "Nuked"}
        
    register_tool(ToolSpec(
        name="nuke_tool",
        description="Nuke it",
        category="system",
        args_model=NukeArgs,
        side_effects=True,
        external_communication=False,
        destructive=True,
        default_action_type="DELETE",
        default_sensitivity="high",
        default_scope="all"
    ), nuke_tool)

    # Patch catalog so Planner maps nuke_intent -> nuke_tool
    new_catalog = {
        "nuke_intent": {
            "required_slots": ["target"],
            "tool_name": "nuke_tool",
            "description": "Nuke tool"
        }
    }

    with patch("src.agent.orchestrator.parse_intent", return_value=mock_intent), \
         patch.dict("src.agent.planner.INTENTS", new_catalog):
         
        # Mock Runtime Execute to force needs_confirmation on first call
        with patch.object(orchestrator.tool_runtime, "execute") as mock_exec:
            from src.tools.contracts import ToolResult
            
            # Call 1: Needs Confirmation
            mock_exec.return_value = ToolResult(
                status="needs_confirmation",
                latency_ms=100,
                confirmation_prompt="Are you sure?",
            )
            
            response1 = orchestrator.handle_user_utterance(
                db=db,
                user_id=db.test_user_id,
                session_id=db.test_session_id,
                utterance="Nuke the database"
            )
            
            assert response1.assistant_text == "Are you sure?"
            
            # Insert Fake Confirmation Record (simulating what Runtime/Policy would have done)
            conf_id = uuid4()
            db.add(PendingConfirmationModel(
                id=conf_id,
                session_id=db.test_session_id,
                user_id=db.test_user_id,
                tool_name="nuke_tool",
                tool_args={"target": "all"},
                decision_type="ALLOW_WITH_CONFIRMATION",
                status="pending",
                required_phrase="YES I AM SURE"
            ))
            db.commit()
            
            # Call 2: User Confirms
            # Mock Runtime to return SUCCESS now
            mock_exec.return_value = ToolResult(
                status="success",
                latency_ms=100,
                data={"message": "Nuked"}
            )
            
            response2 = orchestrator.handle_user_utterance(
                db=db,
                user_id=db.test_user_id,
                session_id=db.test_session_id,
                utterance="YES I AM SURE"
            )
            
            assert "Done. Nuked" in response2.assistant_text

