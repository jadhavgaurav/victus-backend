"""
Long-term memory tools for storing and recalling user facts
"""
import uuid

# Refactor: Use MemoryStore

# Refactor: Use MemoryStore
from ..memory.factory import get_memory_store
from ..utils.context import get_session_id, get_user_id
from .base import SafeTool, RiskLevel
from .schemas.memory_schemas import RememberFactSchema, RecallFactSchema


def _remember_fact(key: str, value: str, user_id: str = None) -> str:
    if not user_id:
        user_id = get_user_id()
    
    store = get_memory_store()
    try:
        # We assume 'episodic' or 'semantic' type or introduce a 'fact' type?
        # The prompt for repository_pgvector.py limited types to semantic/episodic/procedural.
        # So we map "fact" to "semantic" or "episodic" with metadata key='fact'.
        # Let's say facts are "semantic" memories about the user.
        
        # Note: If backend is FAISS, the FaissMemoryStore adapter needs to handle this call
        # and route it back to the SQL UserFact logic.
        
        # We pass type="semantic" and metadata={"key": key, "subtype": "fact"}.
        # The FaissMemoryStore adapter I wrote explicitly checks type="semantic" and metadata.get("key").
        
        store.write_memory(
            user_id=uuid.UUID(str(user_id)), # Ensure UUID
            type="semantic",
            text=value,
            metadata={"key": key, "subtype": "fact"}
        )
        return f"Remembered fact: '{key}' set to '{value}'."
    except Exception as e:
        return f"Error remembering fact: {e}"

def _recall_fact(key: str, user_id: str = None) -> str:
    if not user_id:
        user_id = get_user_id()
    
    store = get_memory_store()
    try:
        # Search for the fact.
        # For Pgvector, we verify if we can utilize search_memory with metadata filter.
        # But search_memory is similarity search based on query_text.
        # We want EXACT match on key.
        # search_memory implementation supports metadata_filter.
        # BUT it requires a query_text for embedding.
        # If we just want to look up by key, PgvectorMemoryRepository.search_memory calculates embedding.
        # Implementation Detail:
        # If we pass query_text="", embedding might be weird but valid.
        # However, we simply want look up.
        # Current PgvectorRepository doesn't have "get_by_metadata".
        # But `recall_fact` is specific to Key-Value.
        # For Pgvector backend, we might need a "get_memory" or "search_exact" method?
        # Prompt said: "Implement PgvectorMemoryRepository... write_memory... search_memory... get_recent_episodic".
        # It did NOT ask for exact metadata lookup.
        # This implies `recall_fact` might need to be deprecated or implemented via search?
        # OR: We rely on the fact that FaissMemoryStore (Legacy) *does* logic to recall from SQL.
        # For Pgvector, if we treat facts as vector memories, we retrieve by query="key"?
        # That's fuzzy. "My name" vs "name".
        # 
        # For now, to satisfy "Preserve existing memory tool interfaces", "No regressions", 
        # and "Step 4B: Implement PgvectorMemoryRepository ... (only) write, search, get_recent".
        # Use query_text=key and metadata_filter={"key": key}?
        # If I search with metadata_filter, I get the exact memory.
        
        results = store.search_memory(
            user_id=uuid.UUID(str(user_id)),
            query_text=key, # Embedding this
            top_k=1,
            types=["semantic"],
            metadata_filter={"key": key, "subtype": "fact"}
        )
        
        if results:
            fact_text = results[0]["text"]
            return f"The stored fact for '{key}' is: '{fact_text}'"
        else:
             return f"Fact not found. I don't have a stored fact for '{key}'."
             
    except Exception as e:
        return f"Error recalling fact: {e}"

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
