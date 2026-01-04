from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..models.memory import Memory, MemoryEvent
from ..utils.redaction import redact_text
from .embeddings import embeddings

def retrieve_memories(
    db: Session,
    user_id: str,
    query_text: str,
    types: Optional[List[str]] = None,
    metadata_filter: Optional[dict] = None,
    top_k: int = 5,
    min_score: float = 0.70
) -> List[Memory]:
    """
    Semantic search for memories.
    """
    safe_query = redact_text(query_text)
    query_vec = embeddings.embed_texts([safe_query])[0]
    
    now = datetime.now(timezone.utc)
    
    from src.config import settings
    if settings.ENVIRONMENT == "test":
         # Fallback for SQLite testing (Exact match or just recent)
         # We'll ignore vector similarity since we lack pgvector
         stmt = db.query(Memory).filter(
            Memory.user_id == user_id,
            Memory.is_deleted == False
         )
         if types:
             stmt = stmt.filter(Memory.type.in_(types))
         if metadata_filter:
            for key, value in metadata_filter.items():
                stmt = stmt.filter(Memory.metadata_.contains({key: value}))
                
         memories = stmt.limit(top_k).all()
         # Add fake score attribute? OR rely on API returning list
         return memories

    # Cosine distance: 0=identical, 1=opposite (for normalized).
    # Similarity = 1 - distance.
    # min_score 0.70 => max_distance 0.30
    max_distance = 1.0 - min_score
    
    # Build wrapper for distance
    distance_col = Memory.embedding.cosine_distance(query_vec).label("distance")
    
    stmt = db.query(Memory, distance_col).filter(
        Memory.user_id == user_id,
        Memory.is_deleted == False,
        or_(Memory.expires_at == None, Memory.expires_at > now),
        distance_col < max_distance
    )
    
    if types:
        stmt = stmt.filter(Memory.type.in_(types))
        
    if metadata_filter:
        for key, value in metadata_filter.items():
            # JSONB contains check
            stmt = stmt.filter(Memory.metadata_.contains({key: value}))
        
    results = stmt.order_by(distance_col).limit(top_k).all()
    
    memories = []
    for mem, dist in results:
        # Attach score for convenience (not persisted)
        mem.score = 1.0 - dist
        memories.append(mem)
        
    # Log retrieval event (bulk?)
    # A2.1 says "RETRIEVED" event.
    # To avoid DB spam, maybe log only if results found, or per message logic.
    # For now, simplistic logging.
    if memories:
        for mem in memories:
            event = MemoryEvent(
                user_id=user_id,
                memory_id=mem.id,
                event_type="RETRIEVED",
                actor="system",
                reason="query_search"
            )
            db.add(event)
        db.commit()
        
    return memories
