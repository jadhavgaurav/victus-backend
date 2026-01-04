from typing import Dict, TypedDict

class ToolPolicyMeta(TypedDict):
    category: str
    default_action_type: str
    default_sensitivity: str
    default_scope: str
    side_effects: bool
    external_communication: bool
    destructive: bool

# This registry is authoritative.
# Tools without registry entries must default to DENY.
TOOL_POLICY_REGISTRY: Dict[str, ToolPolicyMeta] = {
    # System / Core
    "system.clock": {
        "category": "system",
        "default_action_type": "READ",
        "default_sensitivity": "low",
        "default_scope": "single",
        "side_effects": False,
        "external_communication": False,
        "destructive": False,
    },
    
    # Calendar
    "calendar.read": {
        "category": "calendar",
        "default_action_type": "READ",
        "default_sensitivity": "low",
        "default_scope": "batch",
        "side_effects": False,
        "external_communication": False,
        "destructive": False,
    },
    "calendar.create": {
        "category": "calendar",
        "default_action_type": "WRITE",
        "default_sensitivity": "medium",
        "default_scope": "single",
        "side_effects": True,
        "external_communication": False,
        "destructive": False,
    },

    # Email
    "email.read": {
        "category": "email",
        "default_action_type": "READ",
        "default_sensitivity": "medium",
        "default_scope": "batch",
        "side_effects": False,
        "external_communication": False,
        "destructive": False,
    },
    "email.send": {
        "category": "email",
        "default_action_type": "WRITE",
        "default_sensitivity": "high",
        "default_scope": "single",
        "side_effects": True,
        "external_communication": True,
        "destructive": False,
    },

    # Files
    "file.read": {
        "category": "files",
        "default_action_type": "READ",
        "default_sensitivity": "medium",
        "default_scope": "single",
        "side_effects": False,
        "external_communication": False,
        "destructive": False,
    },
    "file.write": {
        "category": "files",
        "default_action_type": "WRITE",
        "default_sensitivity": "medium",
        "default_scope": "single",
        "side_effects": True,
        "external_communication": False,
        "destructive": False,
    },
    "file.delete": {
        "category": "files",
        "default_action_type": "DELETE",
        "default_sensitivity": "high",
        "default_scope": "single",
        "side_effects": True,
        "external_communication": False,
        "destructive": True,
    },

    # Web (if applicable)
    "web.search": {
        "category": "web",
        "default_action_type": "READ",
        "default_sensitivity": "low",
        "default_scope": "single",
        "side_effects": False,
        "external_communication": True, # Technically yes, but usually treated as READ
        "destructive": False,
    },
    
    # --- New SafeTool Names ---
    "get_system_info": {
        "category": "system",
        "default_action_type": "READ",
        "default_sensitivity": "low",
        "default_scope": "single",
        "side_effects": False,
        "external_communication": False,
        "destructive": False,
    },
    "list_files": {
        "category": "files",
        "default_action_type": "READ",
        "default_sensitivity": "low",
        "default_scope": "single",
        "side_effects": False,
        "external_communication": False,
        "destructive": False,
    },
    "get_calendar_events": {
        "category": "calendar",
        "default_action_type": "READ",
        "default_sensitivity": "low",
        "default_scope": "batch",
        "side_effects": False,
        "external_communication": False,
        "destructive": False,
    },
    "read_emails": {
        "category": "email",
        "default_action_type": "READ",
        "default_sensitivity": "medium",
        "default_scope": "batch",
        "side_effects": False,
        "external_communication": False,
        "destructive": False,
    },
}
