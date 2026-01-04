from uuid import UUID
from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..models.message import Message

# Optional: Import memory store if available and reliable
# from ..memory.store import MemoryStore 

def get_context(
    db: Session,
    user_id: UUID, 
    session_id: UUID, 
    utterance: str, 
    limit_messages: int = 10
) -> Dict[str, Any]:
    """
    Retrieves the context for the agent:
    1. Recent conversation history (last N messages).
    2. (TODO) Semantic memory / RAG context based on utterance.
    """
    
    # 1. Fetch recent messages
    # We want them in chronological order, so we fetch desc then reverse
    recent_msgs = db.query(Message).filter(
        Message.session_id == session_id,
        Message.user_id == user_id
    ).order_by(desc(Message.created_at)).limit(limit_messages).all()
    
    history = []
    for m in reversed(recent_msgs):
        history.append({
            "role": m.role,
            "content": m.content,
            "modality": m.modality
        })
        
    # 2. (Future) Memory Retrieval
    # relevant_facts = memory_store.search(utterance)
    
    return {
        "history": history,
        "memory_facts": [] # Placeholder
    }
