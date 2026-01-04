import pytest
from uuid import uuid4
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock

from src.database import settings
from src.tools.runtime import ToolRuntime
from src.tools.register_all import register_all_tools
from src.tools.registry import clear_registry, register_tool
from src.tools.contracts import ToolSpec
from src.models.tool_call import ToolCall
from src.models.policy import PendingConfirmationModel
from src.models.user import User
from src.models.session import Session

from pydantic import BaseModel

# Setup DB
engine = create_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        # Create Dummy User and Session for FK constraints
        user_id = uuid4()
        user = User(id=user_id, email=f"test{user_id}@example.com")
        session.add(user)
        session.commit()
        
        session_id = uuid4()
        sess = Session(id=session_id, user_id=user_id)
        session.add(sess)
        session.commit()
        
        # Keep IDs for tests
        session.test_user_id = user_id
        session.test_session_id = session_id
        
        yield session
    finally:
        session.close()

@pytest.fixture(autouse=True)
def setup_registry():
    clear_registry()
    # Ensure system tools are registered for rate limit test
    register_all_tools()
    yield
    clear_registry()

def test_unknown_tool_denied(db):
    runtime = ToolRuntime()
    result = runtime.execute(
        user_id=db.test_user_id,
        session_id=db.test_session_id,
        tool_name="non_existent_tool",
        args_dict={},
        db=db
    )
    assert result.status == "denied"
    assert "not found" in result.error

def test_validation_error(db):
    runtime = ToolRuntime()
    # get_calendar_events expects 'days' (int), pass string
    result = runtime.execute(
        user_id=db.test_user_id,
        session_id=db.test_session_id,
        tool_name="get_calendar_events",
        args_dict={"days": "not_an_int"},
        db=db
    )
    assert result.status == "error"
    assert "Validation Error" in result.error
    
    # Check persistence (Validation error should persist)
    # Using specific user/session
    call = db.query(ToolCall).filter(ToolCall.session_id == db.test_session_id).first()
    assert call is not None
    assert call.status == "error"

@patch("src.tools.m365_tools.get_access_token", return_value="mock_token")
@patch("src.tools.m365_tools.requests.get")
def test_policy_allow_execution(mock_get, mock_token, db):
    # Mock MS Graph Response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "value": [
            {
                "subject": "Mock Event",
                "start": {"dateTime": "2025-01-01T10:00:00Z"},
                "end": {"dateTime": "2025-01-01T11:00:00Z"}
            }
        ]
    }
    mock_get.return_value = mock_response

    runtime = ToolRuntime()
    
    # get_calendar_events -> ALLOW
    result = runtime.execute(
        user_id=db.test_user_id,
        session_id=db.test_session_id,
        tool_name="get_calendar_events",
        args_dict={"days": 1},
        db=db
    )
    
    assert result.status == "success"
    # Data should contain our mock event string
    assert "Mock Event" in str(result.data)
    assert result.policy_decision_id is not None
    
    # Check Persistence
    call = db.query(ToolCall).filter(ToolCall.session_id == db.test_session_id).order_by(text("created_at DESC")).first()
    assert call is not None
    assert call.status == "success"
    assert call.tool_name == "get_calendar_events"

def test_policy_confirmation_required(db):
    class EmailArgs(BaseModel):
        to: str
        body: str

    def email_tool(to, body):
        return {"sent": True}

    # Register in Runtime Registry
    register_tool(
        ToolSpec(
            name="test.email", 
            description="Send email", 
            category="email",
            args_model=EmailArgs,
            side_effects=True,
            external_communication=True,
            destructive=False,
            default_action_type="WRITE",
            default_sensitivity="high",
            default_scope="single"
        ),
        email_tool
    )

    # Patch Policy Registry to include this tool, otherwise Engine returns Unknown->Deny
    with patch.dict("src.policy.tool_registry.TOOL_POLICY_REGISTRY", {
        "test.email": {
            "category": "email",
            "default_action_type": "WRITE",
            "default_sensitivity": "high",
            "default_scope": "single",
            "side_effects": True,
            "external_communication": True, # Triggers confirmation
            "destructive": False,
        }
    }):
        runtime = ToolRuntime()
        result = runtime.execute(
            user_id=db.test_user_id,
            session_id=db.test_session_id,
            tool_name="test.email",
            args_dict={"to": "foo@bar.com", "body": "hello"},
            db=db
        )
        
        assert result.status == "needs_confirmation"
        assert result.pending_confirmation_id is not None
        assert result.confirmation_prompt is not None
        
        # Check Persistence of Pending Confirmation
        pending = db.query(PendingConfirmationModel).filter(PendingConfirmationModel.id == result.pending_confirmation_id).first()
        assert pending is not None
        assert pending.status == "pending"

def test_redaction_in_args_and_result(db):
    class SecretArgs(BaseModel):
        api_key: str

    def secret_tool(api_key):
        return {"token": "super_secret_token_123"}
        
    register_tool(
        ToolSpec(
            name="test.secret",
            description="Secret tool",
            category="other", 
            args_model=SecretArgs,
            side_effects=False, 
            external_communication=False, 
            destructive=False,
            default_action_type="READ",
            default_sensitivity="low",
            default_scope="single"
        ),
        secret_tool
    )
    
     # Patch Policy Registry
    with patch.dict("src.policy.tool_registry.TOOL_POLICY_REGISTRY", {
        "test.secret": {
            "category": "other",
            "default_action_type": "READ",
            "default_sensitivity": "low",
            "default_scope": "single",
            "side_effects": False,
            "external_communication": False,
            "destructive": False,
        }
    }):
        runtime = ToolRuntime()
        
        result = runtime.execute(
            user_id=db.test_user_id,
            session_id=db.test_session_id,
            tool_name="test.secret",
            args_dict={"api_key": "raw_key_123"},
            db=db
        )
        
        assert result.status == "success"
        # Result data should be redacted
        assert result.data["token"] == "[REDACTED]"
        assert "token" in result.redactions_applied
        
        # DB Persistence Check
        call = db.query(ToolCall).filter(ToolCall.session_id == db.test_session_id).order_by(text("created_at DESC")).first()
        
        # Check Args Redaction
        assert call.args["api_key"] == "[REDACTED]" # Changed to .args
        # Check Result Redaction
        assert call.result["token"] == "[REDACTED]" # Changed to .result

def test_rate_limiting(db):
    # Trigger 11 calls in 1 minute (limit is 10)
    # Ensure tool persists
    register_all_tools()
    runtime = ToolRuntime()
    
    # 10 allowed calls
    for _ in range(10):
        runtime.execute(
            user_id=db.test_user_id,
            session_id=db.test_session_id,
            tool_name="get_system_info",
            args_dict={},
            db=db
        )
        # Small delay to ensure DB order?
        
    # 11th call should fail
    result = runtime.execute(
        user_id=db.test_user_id,
        session_id=db.test_session_id,
        tool_name="get_system_info",
        args_dict={},
        db=db
    )
    
    assert result.status == "denied"
    assert "Rate limit" in result.error
