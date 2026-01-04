
import pytest
import uuid
from uuid import uuid4
from sqlalchemy.orm import Session
from src.memory.write import write_memory
from src.memory.retrieve import retrieve_memories
from src.models import Memory, MemoryEvent

# Since we are using SQLite in tests, and we updated Memory model to use String instead of Vector,
# we can test the logic flow but NOT the actual vector search accuracy (cosine similarity).

def test_write_memory_logic(db_session: Session):
    # Setup
    user_id = str(uuid4())
    content = "The user loves coding in Python."
    
    # Execute Write
    mem_id = write_memory(
        db=db_session,
        user_id=user_id,
        session_id=None,
        type_="FACT",
        source="test",
        content=content,
        metadata={"confidence": 0.9}
    )
    
    # Verify Persistence
    mem = db_session.query(Memory).filter(Memory.id == mem_id).first()
    assert mem is not None
    assert mem.content == content
    assert mem.user_id == uuid.UUID(user_id) if isinstance(mem.user_id, uuid.UUID) else str(mem.user_id) == user_id
    
    pass

def test_retrieve_memory_logic(db_session: Session):
    # Setup
    user_id = str(uuid4())
    write_memory(db_session, user_id, None, "FACT", "test", "Apples are red (fact 1)", {"topic": "fruit"})
    write_memory(db_session, user_id, None, "FACT", "test", "Sky is blue (fact 2)", {"topic": "nature"})
    
    # Test Retrieval (Mocked logic in test env returns all matching filters)
    results = retrieve_memories(
        db=db_session,
        user_id=user_id,
        query_text="Apples", # Ignored in mock
        types=["FACT"],
        metadata_filter={"topic": "fruit"}
    )
    
    assert len(results) == 1
    assert "Apples" in results[0].content
    assert results[0].metadata_["topic"] == "fruit"

