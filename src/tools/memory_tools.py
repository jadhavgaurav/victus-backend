"""
Long-term memory tools for storing and recalling user facts
"""
import uuid

# Refactor: Use MemoryStore

from ..utils.context import get_session_id, get_user_id
from .base import SafeTool, RiskLevel
from .schemas.memory_schemas import RememberFactSchema, RecallFactSchema
from ..database import SessionLocal
from ..memory.write import write_memory
from ..memory.retrieve import retrieve_memories

def _remember_fact(key: str, value: str, user_id: str = None) -> str:
    if not user_id:
        user_id = get_user_id()
    
    db = SessionLocal()
    try:
        session_id = get_session_id()
        
        # A2 system: type="FACT", source="tool"
        write_memory(
            db=db,
            user_id=str(user_id),
            session_id=session_id, # Might be None, handled in write_memory
            type_="FACT",
            source="tool:remember_fact",
            content=f"{key}: {value}",
            metadata={"key": key, "subtype": "fact"}
        )
        return f"Remembered fact: '{key}' set to '{value}'."
    except Exception as e:
        return f"Error remembering fact: {e}"
    finally:
        db.close()

def _recall_fact(key: str, user_id: str = None) -> str:
    if not user_id:
        user_id = get_user_id()
    
    db = SessionLocal()
    try:
        # Exact lookup via metadata
        results = retrieve_memories(
            db=db,
            user_id=str(user_id),
            query_text=key, # Semantic + filter
            types=["FACT"],
            metadata_filter={"key": key},
            top_k=1,
            min_score=0.0 # Force return if filter matches, regardless of score (embedding of key vs key should be high anyway)
        )
        
        if results:
            fact_content = results[0].content
            return f"The stored fact for '{key}' is: '{fact_content}'"
        else:
            return f"Fact not found. I don't have a stored fact for '{key}'."
             
    except Exception as e:
        return f"Error recalling fact: {e}"
    finally:
        db.close()

# --- Tool Construction ---

remember_fact = SafeTool.from_func(
    func=_remember_fact,
    name="remember_fact",
    description="Stores a key-value pair as a personal fact for long-term memory.",
    args_schema=RememberFactSchema,
    risk_level=RiskLevel.MEDIUM
)

recall_fact = SafeTool.from_func(
    func=_recall_fact,
    name="recall_fact",
    description="Recalls a specific personal fact previously stored in long-term memory.",
    args_schema=RecallFactSchema,
    risk_level=RiskLevel.LOW
)
