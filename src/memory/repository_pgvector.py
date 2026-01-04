
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import text as sql_text

from ..database import SessionLocal
from ..models.memory import Memory
from .embeddings import EmbeddingService

class PgvectorMemoryRepository:
    """
    Repository for handling Memory operations with pgvector in Postgres.
    """
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service

    def write_memory(
        self,
        user_id: uuid.UUID,
        type: str,
        text: str,
        metadata: Dict[str, Any],
        session_id: Optional[uuid.UUID] = None
    ) -> uuid.UUID:
        """
        Writes a new memory to the database.
        """
        # Validate type
        if type not in ["semantic", "episodic", "procedural"]:
            raise ValueError(f"Invalid memory type: {type}")

        # Compute embedding
        embedding = self.embedding_service.embed_text(text)
        
        # Ensure metadata is serializable (though JsonB handles dicts)
        # We assume metadata is already a dict.
        
        db: Session = SessionLocal()
        try:
            # We must check if the embedding column exists (defensive for local dev without extension)
            # But the model has it defined. If the underlying logic fails, it will raise an error.
            # We proceed with the standard insert.
            
            memory = Memory(
                user_id=user_id,
                type=type,
                text=text,
                embedding=embedding,
                metadata_=metadata, # Mapped to 'metadata' column
                # session_id is not yet in the Memory model (Step 3 definitions didn't include it in Memory table explicitly?)
                # Checking Step 3 prompt: "4) memories Table: id, user_id, type, text, embedding, metadata, created_at, last_accessed_at, decay_score"
                # It does NOT have session_id. So we store session_id in metadata if needed.
            )
            
            if session_id:
                memory.metadata_["session_id"] = str(session_id)

            db.add(memory)
            db.commit()
            db.refresh(memory)
            return memory.id
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def search_memory(
        self,
        user_id: uuid.UUID,
        query_text: str,
        top_k: int = 5,
        types: Optional[List[str]] = None,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Searches memories by semantic similarity.
        """
        embedding = self.embedding_service.embed_text(query_text)
        
        db: Session = SessionLocal()
        try:
            # Base query
            stmt = select(Memory).where(Memory.user_id == user_id)
            
            # Apply type filter
            if types:
                stmt = stmt.where(Memory.type.in_(types))
                
            # Apply metadata filter (simple Exact Match for top-level keys)
            if metadata_filter:
                for key, value in metadata_filter.items():
                    # JSONB contained operator: @>
                    # Using sql text for jsonb containment or sqlalchemy operator
                    stmt = stmt.where(Memory.metadata_.contains({key: value}))

            # Vector similarity ordering
            # FAISS used L2 (Euclidean).
            # We use pgvector L2 distance operator (<->) via l2_distance method.
            
            distance_col = Memory.embedding.l2_distance(embedding).label("distance")
            stmt = stmt.order_by(distance_col).limit(top_k)
            
            # Select relevant columns + distance
            stmt = select(Memory, distance_col).where(Memory.user_id == user_id)
            if types:
                stmt = stmt.where(Memory.type.in_(types))
            if metadata_filter:
                for key, value in metadata_filter.items():
                    stmt = stmt.where(Memory.metadata_.contains({key: value}))
            stmt = stmt.order_by(distance_col).limit(top_k)

            results = db.execute(stmt).all()
            
            output = []
            for memory, distance in results:
                # Convert L2 distance to similarity score.
                # L2 distance is [0, infinity). 0 is identical.
                # A standard bounded similarity from distance d is 1 / (1 + d).
                score = 1 / (1 + distance)
                
                output.append({
                    "id": memory.id,
                    "text": memory.text,
                    "type": memory.type,
                    "metadata": memory.metadata_,
                    "score": score,
                    "created_at": memory.created_at
                })
                
                # Update last accessed
                memory.last_accessed_at = sql_text("now()")
                db.add(memory)
            
            db.commit() # Commit the last_accessed_updates
            return output
            
        except Exception as e:
            db.rollback()
            # If "function cosine_distance(vector, vector) does not exist" or column missing
            # we might want to log it. User prompt says "Do not silently swallow DB errors".
            raise e
        finally:
            db.close()

    def get_recent_episodic(
        self,
        user_id: uuid.UUID,
        limit: int = 10,
        session_id: Optional[uuid.UUID] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves recent episodic memories.
        """
        db: Session = SessionLocal()
        try:
            stmt = select(Memory).where(
                Memory.user_id == user_id,
                Memory.type == "episodic"
            )
            
            if session_id:
                stmt = stmt.where(Memory.metadata_.contains({"session_id": str(session_id)}))
                
            stmt = stmt.order_by(desc(Memory.created_at)).limit(limit)
            
            memories = db.scalars(stmt).all()
            
            return [{
                "id": m.id,
                "text": m.text,
                "type": m.type,
                "metadata": m.metadata_,
                "created_at": m.created_at
            } for m in memories]
            
        finally:
            db.close()
