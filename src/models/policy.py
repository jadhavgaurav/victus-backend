from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from ..database import Base

class PolicyDecisionModel(Base):
    __tablename__ = "policy_decisions"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(PG_UUID(as_uuid=True), index=True, nullable=False)
    user_id = Column(PG_UUID(as_uuid=True), index=True, nullable=False)
    tool_name = Column(String, nullable=False)
    decision = Column(String, nullable=False) # ALLOW, ALLOW_WITH_CONFIRMATION, DENY, ESCALATE
    risk_score = Column(Integer, nullable=False)
    reason_code = Column(String, nullable=False)
    intent_summary = Column(Text, nullable=True)
    
    # Optional FK to tool_calls if we want to link them later
    tool_call_id = Column(PG_UUID(as_uuid=True), ForeignKey("tool_calls.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)


class PendingConfirmationModel(Base):
    __tablename__ = "pending_confirmations"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(PG_UUID(as_uuid=True), index=True, nullable=False)
    user_id = Column(PG_UUID(as_uuid=True), index=True, nullable=False)
    
    tool_name = Column(String, nullable=False)
    tool_args = Column(JSON, nullable=False)
    
    required_phrase = Column(String, nullable=True)
    decision_type = Column(String, nullable=False) # ESCALATE, ALLOW_WITH_CONFIRMATION
    
    expires_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="pending", nullable=False) # pending, confirmed, expired, cancelled
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
