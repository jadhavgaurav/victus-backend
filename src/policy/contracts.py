from datetime import datetime
from typing import Any, Dict, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class PolicyCheck(BaseModel):
    """
    Input schema for policy evaluation.
    This defines what the agent wants to do.
    """
    model_config = ConfigDict(frozen=True)

    # Required core context
    user_id: UUID
    session_id: UUID
    tool_name: str
    action_type: Literal["READ", "WRITE", "EXECUTE", "DELETE"]
    target_entity: str = Field(description="The primary entity being acted opon, e.g., 'calendar_event', 'email'")
    
    # Impact assessment fields
    scope: Literal["single", "batch", "all"]
    sensitivity: Literal["low", "medium", "high"]
    
    # Human-readable explanations
    intent_summary: str = Field(description="Short description of what happens")
    tool_args_preview: Dict[str, Any] = Field(description="Redacted arguments for safe logging")

    # Optional context
    device_locked: Optional[bool] = None
    user_present: Optional[bool] = None
    network: Optional[Literal["trusted", "untrusted"]] = None
    time_of_day: Optional[str] = None


class PolicyDecision(BaseModel):
    """
    Output schema for policy evaluation.
    This defines what the agent is allowed to do.
    """
    model_config = ConfigDict(frozen=True)

    decision: Literal["ALLOW", "ALLOW_WITH_CONFIRMATION", "DENY", "ESCALATE"]
    risk_score: int = Field(ge=0, le=100)
    reason_code: str = Field(description="Machine-readable reason code")
    
    # User interaction fields
    user_prompt: Optional[str] = None
    required_confirmation_phrase: Optional[str] = None
    expires_at: Optional[datetime] = None
    
    # ID from persistence layer
    id: Optional[UUID] = None

    def is_blocking(self) -> bool:
        return self.decision in ("DENY", "ESCALATE", "ALLOW_WITH_CONFIRMATION")
