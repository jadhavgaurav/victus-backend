
from sqlalchemy import Column, String, ForeignKey, Integer, Index
from sqlalchemy.sql import func
from src.database import Base
from src.db.types import UUIDType, TZDateTime, JsonBType
from src.db.base import uuid_pk

class ToolCall(Base):
    """Model for logging tool executions."""
    __tablename__ = "tool_calls"

    id = Column(UUIDType, primary_key=True, default=uuid_pk)
    session_id = Column(UUIDType, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUIDType, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    tool_name = Column(String, nullable=False)
    args = Column(JsonBType, nullable=False, server_default='{}')
    result = Column(JsonBType, nullable=False, server_default='{}')
    status = Column(String, nullable=False) # success, error
    latency_ms = Column(Integer, nullable=False, default=0)
    
    created_at = Column(TZDateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        Index('ix_tool_calls_session_id_created_at', 'session_id', 'created_at'),
        Index('ix_tool_calls_user_id_created_at', 'user_id', 'created_at'),
        Index('ix_tool_calls_tool_name_created_at', 'tool_name', 'created_at'),
    )
