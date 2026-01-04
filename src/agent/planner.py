from typing import Dict, Any
from .contracts import Intent, Plan, PlanStep
from .intents_catalog import INTENTS

def build_plan(intent: Intent, context: Dict[str, Any]) -> Plan:
    """
    Constructs an execution plan based on the intent and catalog.
    """
    
    # 1. Handle clarification
    if intent.needs_clarification:
        return Plan(
            requires_user_input=True,
            clarifying_question=intent.clarifying_question
        )
        
    # 2. Handle Unknown
    if intent.name == "unknown" or intent.name not in INTENTS:
        return Plan(
            requires_user_input=True,
            clarifying_question="I'm not sure how to help with that. Could you rephrase?"
        )
        
    # 3. Build Tool Plan
    catalog_entry = INTENTS[intent.name]
    tool_name = catalog_entry["tool_name"]
    
    if not tool_name:
         # Should catch unknown here too, but just in case
        return Plan(requires_user_input=True, clarifying_question="I don't have a tool for that yet.")

    # Construct args from slots
    # We pass the slots directly as args. 
    # The tool runtime validation will catch any issues/types.
    
    step = PlanStep(
        tool_name=tool_name,
        args=intent.slots,
        intent_summary=f"User wants to {catalog_entry.get('description', 'perform action')} with params: {intent.slots}"
    )
    
    return Plan(steps=[step])
