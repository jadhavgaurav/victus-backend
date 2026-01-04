
from sqlalchemy import Column, String, ForeignKey, Float, Index
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from src.database import Base
from src.db.types import UUIDType, TZDateTime, JsonBType
from src.db.base import uuid_pk

# Embedding dimension from Step 1 findings
EMBED_DIM = 1536

class Memory(Base):
    """Model for semantic, episodic, and procedural memories."""
    __tablename__ = "memories"

    id = Column(UUIDType, primary_key=True, default=uuid_pk)
    user_id = Column(UUIDType, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    type = Column(String, nullable=False) # semantic, episodic, procedural
    text = Column(String, nullable=False)
    embedding = Column(Vector(EMBED_DIM), nullable=False)
    metadata_ = Column("metadata", JsonBType, nullable=False, server_default='{}')
    
    created_at = Column(TZDateTime, server_default=func.now(), nullable=False)
    last_accessed_at = Column(TZDateTime, nullable=True)
    decay_score = Column(Float, nullable=False, default=0.0)

    __table_args__ = (
        Index('ix_memories_user_id_type', 'user_id', 'type'),
        Index('ix_memories_user_id_created_at', 'user_id', 'created_at'),
        # HNSW Index for vector similarity (cosine)
        Index(
            'ix_memories_embedding_hnsw',
            embedding,
            postgresql_using='hnsw',
            postgresql_with={'m': 16, 'ef_construction': 64},
            postgresql_ops={'embedding': 'vector_cosine_ops'}
        ),
    )
