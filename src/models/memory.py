from sqlalchemy import Column, String, ForeignKey, Boolean, UniqueConstraint, Index
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from src.database import Base
from src.db.types import UUIDType, TZDateTime, JsonBType
from src.db.base import uuid_pk

# Embedding dimension
EMBED_DIM = 1536

from src.config import settings

if settings.ENVIRONMENT == "test":
    # SQLite fallback
    VectorType = String
    # No HNSW index for SQLite
    vector_index_args = ()
else:
    VectorType = Vector(EMBED_DIM)
    vector_index_args = (
        Index(
            'ix_memories_embedding_hnsw',
            'embedding',
            postgresql_using='hnsw',
            postgresql_with={'m': 16, 'ef_construction': 64},
            postgresql_ops={'embedding': 'vector_cosine_ops'}
        ),
    )

class Memory(Base):
    """
    Model for persistent, vector-searchable user memories.
    A2.1 Specification.
    """
    __tablename__ = "memories"

    id = Column(UUIDType, primary_key=True, default=uuid_pk)
    user_id = Column(UUIDType, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(UUIDType, ForeignKey("sessions.id", ondelete="SET NULL"), nullable=True)
    
    # Core Content
    type = Column(String, nullable=False)  # FACT, PREFERENCE, TASK, SUMMARY, CONTACT, PROJECT, NOTE
    source = Column(String, nullable=False) # chat, tool, user, import
    content = Column(String, nullable=False) # Sanitized content
    content_hash = Column(String, nullable=False) # Deduplication hash
    
    embedding = Column(VectorType, nullable=False)
    
    metadata_ = Column("metadata", JsonBType, nullable=False, server_default='{}')
    
    # Lifecycle
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(TZDateTime, server_default=func.now(), nullable=False)
    updated_at = Column(TZDateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    expires_at = Column(TZDateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint('user_id', 'content_hash', name='uq_memories_user_content_hash'),
        Index('ix_memories_user_id_created_at', 'user_id', 'created_at'),
        Index('ix_memories_user_id_type', 'user_id', 'type'),
    ) + vector_index_args

class MemoryEvent(Base):
    """
    Audit trail for memory modifications (A2.1).
    """
    __tablename__ = "memory_events"

    id = Column(UUIDType, primary_key=True, default=uuid_pk)
    user_id = Column(UUIDType, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    memory_id = Column(UUIDType, ForeignKey("memories.id", ondelete="CASCADE"), nullable=False)
    
    event_type = Column(String, nullable=False) # CREATED, UPDATED, DELETED, RETRIEVED, EXPIRED
    actor = Column(String, nullable=False) # user, system, tool
    reason = Column(String, nullable=True)
    trace_id = Column(String, nullable=True)
    
    created_at = Column(TZDateTime, server_default=func.now(), nullable=False)
    
    __table_args__ = (
        Index('ix_memory_events_user_created', 'user_id', 'created_at'),
        Index('ix_memory_events_memory_id', 'memory_id'),
    )
