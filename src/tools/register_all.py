
from .contracts import ToolSpec
from .registry import register_tool
from .assembler import get_all_tools
from .base import SafeTool, RiskLevel

def _map_risk_to_spec(tool: SafeTool) -> dict:
    """Heuristic mapping from old RiskLevel to new ToolSpec fields."""
    risk = tool.risk_level
    
    spec = {
        "side_effects": False,
        "external_communication": False,
        "destructive": False,
        "default_action_type": "READ",
        "default_sensitivity": "low",
        "default_scope": "single"
    }

    if risk == RiskLevel.MEDIUM:
        spec.update({
            "side_effects": True,
            "default_action_type": "WRITE",
            "default_sensitivity": "medium"
        })
    elif risk == RiskLevel.HIGH:
        spec.update({
            "side_effects": True,
            "destructive": True,
            "default_action_type": "EXECUTE", 
            "default_sensitivity": "high"
        })
        
    # Heuristic category
    name = tool.name.lower()
    if "email" in name or "outlook" in name:
        spec["category"] = "email"
        spec["external_communication"] = True
    elif "calendar" in name:
        spec["category"] = "calendar"
    elif "file" in name:
        spec["category"] = "files"
    elif "web" in name or "search" in name:
        spec["category"] = "web"
        spec["external_communication"] = True
    elif "system" in name or "app" in name or "screen" in name or "clip" in name:
        spec["category"] = "system"
    elif "memo" in name:
        spec["category"] = "memory"
    else:
        spec["category"] = "other"
        
    return spec

def register_all_tools():
    """
    Registers all available tools in the system.
    This includes both new native tools and adapted SafeTools.
    """
    # Import legacy tools via assembler
    # Passing rag_enabled=False for now to avoid complexity or loop
    legacy_tools = get_all_tools(rag_enabled=True) 
    
    for tool in legacy_tools:
        if isinstance(tool, SafeTool):
            # Adapt SafeTool to ToolSpec
            defaults = _map_risk_to_spec(tool)
            
            spec = ToolSpec(
                name=tool.name,
                description=tool.description,
                category=defaults["category"],
                args_model=tool.args_schema, # SafeTool uses Pydantic schema
                side_effects=defaults["side_effects"],
                external_communication=defaults["external_communication"],
                destructive=defaults["destructive"],
                default_action_type=defaults["default_action_type"],
                default_sensitivity=defaults["default_sensitivity"],
                default_scope=defaults["default_scope"]
            )
            
            # Register with the raw function (_func)
            # SafeTool stores it in _func
            if hasattr(tool, "_func"):
                register_tool(spec, tool._func)

