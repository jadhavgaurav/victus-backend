from typing import Callable, Dict, List, Optional, Tuple

from .contracts import ToolSpec

# Registry storage: name -> (Spec, Callable)
_TOOL_REGISTRY: Dict[str, Tuple[ToolSpec, Callable]] = {}

def register_tool(spec: ToolSpec, func: Callable) -> None:
    """
    Registers a tool with its specification and implementation.
    """
    if spec.name in _TOOL_REGISTRY:
        # We might want to warn or overwrite. For now, overwrite is fine for reloading.
        pass
    _TOOL_REGISTRY[spec.name] = (spec, func)

def get_tool(name: str) -> Optional[Tuple[ToolSpec, Callable]]:
    """
    Retrieves a tool spec and callable by name.
    """
    return _TOOL_REGISTRY.get(name)

def list_tools() -> List[ToolSpec]:
    """
    Returns a list of all registered tool specifications.
    """
    return [spec for spec, _ in _TOOL_REGISTRY.values()]

def clear_registry() -> None:
    """
    Clears the registry (useful for tests).
    """
    _TOOL_REGISTRY.clear()
