from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class Intent(BaseModel):
    """
    Represents the synthesized intent from the user's command.
    """
    name: str # e.g. "create_calendar_event", "unknown"
    slots: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 0.0 # 0.0 to 1.0
    needs_clarification: bool = False
    clarifying_question: Optional[str] = None

class PlanStep(BaseModel):
    """
    A single step in the execution plan, mapping to a tool call.
    """
    tool_name: str
    args: Dict[str, Any]
    intent_summary: str # Justification/Context for the policy engine

class Plan(BaseModel):
    """
    The sequence of actions the agent intends to take.
    """
    steps: List[PlanStep] = Field(default_factory=list)
    requires_user_input: bool = False
    clarifying_question: Optional[str] = None

class OrchestratorResponse(BaseModel):
    """
    The final response returned to the user/frontend.
    """
    assistant_text: str
    should_speak: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)
    pending_confirmation: Optional[Dict[str, Any]] = None
