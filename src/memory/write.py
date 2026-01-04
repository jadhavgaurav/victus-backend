import hashlib
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..models.memory import Memory, MemoryEvent
from ..utils.redaction import redact_text, redact_dict
from .embeddings import embeddings

def compute_content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def write_memory(
    db: Session,
    user_id: str,
    session_id: str | None,
    type_: str, # FACT, PREFERENCE, etc.
    source: str,
    content: str,
    metadata: dict = None,
    retention_days: int = None
) -> str:
    """
    Writes a memory with deduplication and embedding.
    Returns memory_id.
    """
    # 1. Redact
    safe_content = redact_text(content)
    safe_metadata = redact_dict(metadata or {})
    
    # 2. Hash and Dedupe
    content_hash = compute_content_hash(safe_content)
    
    existing = db.query(Memory).filter(
        Memory.user_id == user_id,
        Memory.content_hash == content_hash,
        Memory.is_deleted == False
    ).first()
    
    now = datetime.now(timezone.utc)
    
    # Calculate expiry
    expires_at = None
    if retention_days:
        expires_at = now + timedelta(days=retention_days)
    
    if existing:
        # Update existing
        existing.updated_at = now
        existing.session_id = session_id or existing.session_id # Keep original session or update? "where this memory came from". If re-learned, maybe update.
        existing.metadata_ = safe_metadata # merge? overwrite for now.
        if expires_at:
            existing.expires_at = expires_at
            
        db.add(existing)
        db.flush()
        
        # Log Event
        event = MemoryEvent(
            user_id=user_id, 
            memory_id=existing.id,
            event_type="UPDATED",
            actor=source,
            reason="Deduplicated write"
        )
        db.add(event)
        db.commit()
        return str(existing.id)

    # 3. Embed
    # Note: embed_texts returns list of lists
    vectors = embeddings.embed_texts([safe_content])
    embedding_vector = vectors[0]

    from src.config import settings
    if settings.ENVIRONMENT == "test":
        import json
        embedding_vector = json.dumps(embedding_vector)
    
    # 4. Create
    new_memory = Memory(
        user_id=user_id,
        session_id=session_id,
        type=type_,
        source=source,
        content=safe_content,
        content_hash=content_hash,
        embedding=embedding_vector,
        metadata_=safe_metadata,
        expires_at=expires_at,
        created_at=now,
        updated_at=now
    )
    
    db.add(new_memory)
    db.flush() # get ID
    
    # Log Event
    event = MemoryEvent(
        user_id=user_id, 
        memory_id=new_memory.id,
        event_type="CREATED",
        actor=source
    )
    db.add(event)
    db.commit()
    
    return str(new_memory.id)
