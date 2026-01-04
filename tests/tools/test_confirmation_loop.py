import pytest
from uuid import uuid4
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import settings
from src.tools.runtime import ToolRuntime
from src.tools.registry import register_tool, clear_registry
from src.tools.contracts import ToolSpec
from src.policy.confirmations import resolve_confirmation
from src.models.user import User
from src.models.session import Session
from src.models.policy import PendingConfirmationModel
from pydantic import BaseModel

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
def setup_registry():
    clear_registry()
    yield
    clear_registry()

def test_confirmation_loop(db):
    """
    Verifies that a tool requiring confirmation can be:
    1. BLOCKED (needs_confirmation)
    2. CONFIRMED (via resolve_confirmation)
    3. ALLOWED (on retry)
    """
    
    # 1. Register High Risk Tool
    class TransferArgs(BaseModel):
        amount: int
        to_account: str

    def transfer_tool(amount: int, to_account: str):
        return {"status": "transferred", "amount": amount}

    register_tool(
        ToolSpec(
            name="bank.transfer", 
            description="Transfer money", 
            category="other",
            args_model=TransferArgs,
            side_effects=True,
            external_communication=True,
            destructive=True,
            default_action_type="EXECUTE", # Default High Risk
            default_sensitivity="high",
            default_scope="single"
        ),
        transfer_tool
    )
    
    # Patch Policy Registry to force logic
    with patch.dict("src.policy.tool_registry.TOOL_POLICY_REGISTRY", {
        "bank.transfer": {
            "category": "other",
            "default_action_type": "EXECUTE",
            "default_sensitivity": "high",
            "default_scope": "single",
            "side_effects": True,
            "external_communication": True,
            "destructive": True, 
        }
    }):
        runtime = ToolRuntime()
        
        # 2. First Attempt -> Needs Confirmation
        result1 = runtime.execute(
            user_id=db.test_user_id,
            session_id=db.test_session_id,
            tool_name="bank.transfer",
            args_dict={"amount": 1000, "to_account": "ACC123"},
            db=db
        )
        
        assert result1.status == "needs_confirmation"
        assert result1.pending_confirmation_id is not None
        conf_id = result1.pending_confirmation_id
        
        # Fetch required phrase to ensure test passes matching logic
        pending_record = db.query(PendingConfirmationModel).filter(PendingConfirmationModel.id == conf_id).first()
        required_phrase = pending_record.required_phrase
        
        # 3. User Confirms
        # User says the required phrase
        confirm_result = resolve_confirmation(
            user_id=db.test_user_id,
            session_id=db.test_session_id,
            confirmation_id=conf_id,
            user_utterance=f"Yes, {required_phrase}", # Prepend common words to test substring match
            db=db
        )
        
        assert confirm_result["status"] == "confirmed"
        
        # Verify DB state
        pending = db.query(PendingConfirmationModel).filter(PendingConfirmationModel.id == conf_id).first()
        assert pending.status == "confirmed"
        
        # 4. Retry -> Should Succeed
        result2 = runtime.execute(
            user_id=db.test_user_id,
            session_id=db.test_session_id,
            tool_name="bank.transfer",
            args_dict={"amount": 1000, "to_account": "ACC123"}, # Same args
            db=db
        )
        
        assert result2.status == "success"
        assert result2.data["status"] == "transferred"
        
        # 5. Verify Consumption (Re-retry should fail or need confirm again?)
        # Service logic marks it "completed".
        # So next call should trigger NEW confirmation flow.
        
        result3 = runtime.execute(
            user_id=db.test_user_id,
            session_id=db.test_session_id,
            tool_name="bank.transfer",
            args_dict={"amount": 1000, "to_account": "ACC123"}, # Same args
            db=db
        )
        
        assert result3.status == "needs_confirmation"
        assert result3.pending_confirmation_id != conf_id # New ID
