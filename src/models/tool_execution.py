from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.sql import func
from src.database import Base
from src.db.types import UUIDType, TZDateTime, JsonBType
from src.db.base import uuid_pk

class AgentMessage(Base):
    """
    Persisted state of agent messages (A3.1).
    """
    __tablename__ = "agent_messages"

    id = Column(UUIDType, primary_key=True, default=uuid_pk)
    session_id = Column(UUIDType, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUIDType, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    role = Column(String, nullable=False) # user, assistant, system
    content = Column(String, nullable=True) # logic might allow null if mostly tool calls?
    modality = Column(String, nullable=True, default="text")

    
    status = Column(String, nullable=False, default="CREATED") # CREATED, PROCESSING, COMPLETED, FAILED
    idempotency_key = Column(String, nullable=True)
    trace_id = Column(String, nullable=True)
    
    created_at = Column(TZDateTime, server_default=func.now(), nullable=False)
    updated_at = Column(TZDateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index('ix_agent_messages_session_created', 'session_id', 'created_at'),
    )

class ToolExecution(Base):
    """
    Exactly-once tool execution state machine (A3.1).
    """
    __tablename__ = "tool_executions"

    id = Column(UUIDType, primary_key=True, default=uuid_pk) # tool_invocation_id
    session_id = Column(UUIDType, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUIDType, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    tool_name = Column(String, nullable=False)
    tool_action = Column(String, nullable=True)
    input = Column(JsonBType, nullable=True) # Redacted input
    
    status = Column(String, nullable=False, default="REQUESTED") 
    # REQUESTED, POLICY_DENIED, AWAITING_CONFIRMATION, CONFIRMED, RUNNING, SUCCEEDED, FAILED, CANCELLED, EXPIRED
    
    idempotency_key = Column(String, nullable=False)
    
    result = Column(JsonBType, nullable=True) # Redacted result
    error = Column(JsonBType, nullable=True)
    
    started_at = Column(TZDateTime, nullable=True)
    finished_at = Column(TZDateTime, nullable=True)
    trace_id = Column(String, nullable=True)
    metadata_ = Column("metadata", JsonBType, nullable=True)
    
    created_at = Column(TZDateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'idempotency_key', name='uq_tool_executions_user_idempotency'),
        Index('ix_tool_executions_session_created', 'session_id', 'created_at'),
    )

class Confirmation(Base):
    """
    Human-in-the-loop confirmations (A3.1).
    """
    __tablename__ = "confirmations"

    id = Column(UUIDType, primary_key=True, default=uuid_pk)
    tool_execution_id = Column(UUIDType, ForeignKey("tool_executions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUIDType, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    status = Column(String, nullable=False, default="PENDING") # PENDING, ACCEPTED, REJECTED, EXPIRED
    prompt = Column(String, nullable=False)
    expires_at = Column(TZDateTime, nullable=True)
    
    created_at = Column(TZDateTime, server_default=func.now(), nullable=False)
    updated_at = Column(TZDateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index('ix_confirmations_user_status', 'user_id', 'status'),
    )
