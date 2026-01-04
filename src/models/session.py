
from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy.sql import func
from src.database import Base
from src.db.types import UUIDType, TZDateTime, JsonBType
from src.db.base import uuid_pk

class Session(Base):
    """Model for chat sessions (conversations)."""
    __tablename__ = "sessions"

    id = Column(UUIDType, primary_key=True, default=uuid_pk)
    user_id = Column(UUIDType, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    started_at = Column(TZDateTime, server_default=func.now(), nullable=False)
    ended_at = Column(TZDateTime, nullable=True)
    expires_at = Column(TZDateTime, nullable=True)
    revoked_at = Column(TZDateTime, nullable=True)
    metadata_ = Column("metadata", JsonBType, nullable=False, server_default='{}')
    scopes_override = Column(JsonBType, nullable=True)

    __table_args__ = (
        Index('ix_sessions_user_id_started_at', 'user_id', 'started_at'),
    )
