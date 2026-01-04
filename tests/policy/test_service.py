import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import settings
from src.policy.service import check_and_record_policy
from src.policy.contracts import PolicyCheck
from src.models.policy import PolicyDecisionModel, PendingConfirmationModel

# Use the real DB from settings
engine = create_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_policy_persistence_allow(db):
    # Test that ALLOW decision is persisted
    check = PolicyCheck(
        user_id=uuid.uuid4(),
        session_id=uuid.uuid4(),
        tool_name="calendar.read",
        action_type="READ",
        target_entity="calendar",
        scope="single",
        sensitivity="low",
        intent_summary="Reading calendar",
        tool_args_preview={}
    )
    
    decision = check_and_record_policy(check, db)
    assert decision.decision == "ALLOW"
    
    # DB Check
    record = db.query(PolicyDecisionModel).filter_by(session_id=check.session_id).first()
    assert record is not None
    assert record.decision == "ALLOW"
    assert record.tool_name == "calendar.read"

def test_policy_persistence_confirmation(db):
    # Test that ALLOW_WITH_CONFIRMATION creates both decision and pending confirmation
    check = PolicyCheck(
        user_id=uuid.uuid4(),
        session_id=uuid.uuid4(),
        tool_name="email.send",
        action_type="WRITE",
        target_entity="email",
        scope="single",
        sensitivity="high",
        intent_summary="Sending email",
        tool_args_preview={"to": "test@example.com"}
    )
    
    decision = check_and_record_policy(check, db)
    assert decision.decision == "ALLOW_WITH_CONFIRMATION"
    
    # Decision record
    record = db.query(PolicyDecisionModel).filter_by(session_id=check.session_id).first()
    assert record.decision == "ALLOW_WITH_CONFIRMATION"
    
    # Pending Confirmation record
    confirmation = db.query(PendingConfirmationModel).filter_by(session_id=check.session_id).first()
    assert confirmation is not None
    assert confirmation.decision_type == "ALLOW_WITH_CONFIRMATION"
    assert confirmation.tool_name == "email.send"
    assert confirmation.status == "pending"
    assert confirmation.tool_args == {"to": "test@example.com"}
