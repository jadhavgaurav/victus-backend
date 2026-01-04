from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class MemoryBase(BaseModel):
    type: str = Field(..., description="FACT, PREFERENCE, TASK, SUMMARY, etc")
    content: str
    metadata: Dict[str, Any] = {}

class MemoryCreate(MemoryBase):
    pass

class MemoryUpdate(BaseModel):
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class MemoryRead(MemoryBase):
    id: UUID
    user_id: UUID
    session_id: Optional[UUID]
    source: str
    created_at: datetime
    updated_at: datetime
    score: Optional[float] = None # For search results

    class Config:
        from_attributes = True

class MemorySearch(BaseModel):
    query: str
    types: Optional[List[str]] = None
    top_k: int = 8
    min_score: float = 0.70
