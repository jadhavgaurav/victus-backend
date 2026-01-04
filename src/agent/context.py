from uuid import UUID
from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..models.tool_execution import AgentMessage
from ..memory.retrieve import retrieve_memories

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
    2. Semantic memory / RAG context based on utterance.
    """
    
    # 1. Fetch recent messages
    recent_msgs = db.query(AgentMessage).filter(
        AgentMessage.session_id == session_id,
        AgentMessage.user_id == user_id
    ).order_by(desc(AgentMessage.created_at)).limit(limit_messages).all()
    
    history = []
    for m in reversed(recent_msgs):
        history.append({
            "role": m.role,
            "content": m.content,
            "modality": m.modality
        })
        
    # 2. Memory Retrieval (A2.6)
    memories = retrieve_memories(
        db=db, 
        user_id=str(user_id), 
        query_text=utterance,
        types=["FACT", "PREFERENCE", "TASK", "SUMMARY", "NOTE"],
        top_k=5, 
        min_score=0.65
    )
    
    memory_facts = []
    for m in memories:
        memory_facts.append(f"[{m.type}] {m.content}")
    
    return {
        "history": history,
        "memory_facts": memory_facts
    }
