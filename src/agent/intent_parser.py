from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from ..config import settings
from .contracts import Intent
from .intents_catalog import INTENTS

# Initializing LLM for Intent Parsing
# Using a slightly lower temperature for deterministic output
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    openai_api_key=settings.OPENAI_API_KEY,
    max_tokens=500
)

# Pydantic Parser
parser = PydanticOutputParser(pydantic_object=Intent)

# System Prompt
SYSTEM_PROMPT = """You are a strict intent classification engine.
Your job is to analyze the user's command and map it to one of the known intents.

KNOWN INTENTS:
{intent_list}

RULES:
1. If the user's request matches a known intent, extract the parameters (slots).
2. If the user's request does not match any known intent clearly, return intent 'unknown'.
3. Confidence should be a float between 0.0 and 1.0.
4. If critical slots are missing for the chosen intent, mark 'needs_clarification' as True and provide a single 'clarifying_question'.
   - Required slots for {intent_example}: Use catalog definitions.
   
OUTPUT FORMAT:
Return strictly a JSON object matching the Intent schema.
"""

def _build_intent_list() -> str:
    lines = []
    for k, v in INTENTS.items():
        if k == "unknown": continue
        lines.append(f"- {k}: {v.get('description', '')}. Required Slots: {v.get('required_slots', [])}")
    return "\n".join(lines)

intent_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{utterance}")
])

chain = intent_prompt | llm | parser

def parse_intent(utterance: str, context_str: Optional[str] = None) -> Intent:
    """
    Parses the user utterance into a structured Intent.
    """
    try:
        # We could inject context here if needed to resolve references (e.g. "send it to him")
        # For now, simplistic execution.
        
        intent_list_str = _build_intent_list()
        
        # We pass a sample intent for the prompt to know about requirements mechanism
        # (Though the catalog list has them)
        
        result = chain.invoke({
            "intent_list": intent_list_str,
            "intent_example": "create_calendar_event",
            "utterance": utterance
        })
        
        # Post-validation (Double check logic)
        if result.name in INTENTS and result.name != "unknown":
            spec = INTENTS[result.name]
            missing = [slot for slot in spec["required_slots"] if slot not in result.slots or not result.slots[slot]]
            
            if missing and not result.needs_clarification:
                # LLM failed to flag it, we force it
                result.needs_clarification = True
                result.clarifying_question = f"I need the following information to proceed: {', '.join(missing)}."
                
        return result
        
    except Exception as e:
        # Fallback
        print(f"Intent Parsing Error: {e}")
        return Intent(name="unknown", confidence=0.0)
