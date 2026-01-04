from typing import Any, Dict, List, Literal, Optional, Type
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class ToolSpec(BaseModel):
    """
    Defines the contract for a tool.
    This matches the Policy Registry needs and provides runtime validation.
    """
    model_config = ConfigDict(frozen=True)

    name: str
    description: str
    category: Literal["calendar", "email", "files", "tasks", "system", "web", "memory", "other"]
    
    # Validation models
    args_model: Type[BaseModel]
    result_model: Optional[Type[BaseModel]] = None
    
    # Policy defaults (must match registry authoritative data strictly speaking, 
    # but having them here helps with self-documentation and default registration)
    side_effects: bool
    external_communication: bool
    destructive: bool
    
    default_action_type: Literal["READ", "WRITE", "EXECUTE", "DELETE"]
    default_sensitivity: Literal["low", "medium", "high"]
    default_scope: Literal["single", "batch", "all"]
    
    required_capabilities: List[str] = Field(default_factory=list)


class ToolResult(BaseModel):
    """
    Standardized result returned by the ToolRuntime.
    """
    model_config = ConfigDict(frozen=True)

    status: Literal["success", "error", "needs_confirmation", "denied"]
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    latency_ms: int
    redactions_applied: List[str] = Field(default_factory=list)
    
    # IDs for tracking and context
    policy_decision_id: Optional[UUID] = None
    pending_confirmation_id: Optional[UUID] = None
    
    # When confirmation is needed, this prompt is what the agent should say
    confirmation_prompt: Optional[str] = None
