
from sqlalchemy import Column, String, Boolean, Index
from sqlalchemy.sql import func
from src.database import Base
from src.db.types import UUIDType, TZDateTime, JsonBType
from src.db.base import uuid_pk

class User(Base):
    """Model for storing user accounts."""
    __tablename__ = "users"

    id = Column(UUIDType, primary_key=True, default=uuid_pk)
    email = Column(String, nullable=True) # Nullable as per Step 3 instructions ("Don’t enforce email required yet")
    display_name = Column(String, nullable=True)
    
    # Keeping existing fields for backward compatibility if logic relies on them
    username = Column(String, unique=True, index=True, nullable=True) 
    hashed_password = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    provider = Column(String, default="local")
    provider_id = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    is_superuser = Column(Boolean, default=False)
    scopes = Column(JsonBType, nullable=True, server_default='["core", "tool.web.search", "tool.system.rag", "tool.files.read"]')
    settings = Column(JsonBType, nullable=True, server_default='{}')
    
    # OAuth tokens
    microsoft_access_token = Column(String, nullable=True)
    microsoft_refresh_token = Column(String, nullable=True)
    microsoft_token_expires_at = Column(TZDateTime, nullable=True)
    
    created_at = Column(TZDateTime, server_default=func.now(), nullable=False)
    updated_at = Column(TZDateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login = Column(TZDateTime, nullable=True)

    __table_args__ = (
        Index('ix_users_email', 'email', unique=True, postgresql_where=(email.isnot(None))),
    )
