
from sqlalchemy import Column, String, ForeignKey, Index
from sqlalchemy.sql import func
from src.database import Base
from src.db.types import UUIDType, TZDateTime
from src.db.base import uuid_pk

class Message(Base):
    """Model for a single message in a chat session."""
    __tablename__ = "messages"

    id = Column(UUIDType, primary_key=True, default=uuid_pk)
    session_id = Column(UUIDType, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUIDType, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    role = Column(String, nullable=False) # user, assistant, system, tool
    content = Column(String, nullable=False)
    modality = Column(String, nullable=False, default="text") # voice, text
    
    created_at = Column(TZDateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        Index('ix_messages_session_id_created_at', 'session_id', 'created_at'),
        Index('ix_messages_user_id_created_at', 'user_id', 'created_at'),
    )
