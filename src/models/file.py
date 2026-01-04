from sqlalchemy import Column, String, Integer, ForeignKey, Index
from sqlalchemy.sql import func
from src.database import Base
from src.db.types import UUIDType, TZDateTime
from src.db.base import uuid_pk

class FileMetadata(Base):
    __tablename__ = "files"

    id = Column(UUIDType, primary_key=True, default=uuid_pk)
    user_id = Column(UUIDType, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(UUIDType, nullable=True) # Optional link to session
    
    original_name = Column(String, nullable=False)
    stored_name = Column(String, nullable=False, unique=True)
    mime_type = Column(String, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    
    created_at = Column(TZDateTime, server_default=func.now(), nullable=False)
    # expires_at for retention policy (Step 10F)
    expires_at = Column(TZDateTime, nullable=True)

    __table_args__ = (
        Index('ix_files_user_id', 'user_id'),
    )
