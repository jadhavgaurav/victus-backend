from typing import Dict, Any

# Intent schema definition
# name -> { required_slots: [], tool_name: str }

INTENTS: Dict[str, Any] = {
    "unknown": {
        "required_slots": [],
        "tool_name": None
    },
    
    # Calendar
    "create_calendar_event": {
        "required_slots": ["subject", "start_time_str", "end_time_str"],
        "tool_name": "create_calendar_event",
        "description": "Schedule a meeting or event."
    },
    "get_calendar_events": {
        "required_slots": ["days"], 
        "tool_name": "get_calendar_events",
        "description": "Check calendar schedule."
    },
    
    # Weather
    "get_weather_info": {
        "required_slots": ["location"], # num_days optional (defaults to 1 in tool)
        "tool_name": "get_weather_info",
        "description": "Get weather forecast."
    },
    
    # Files
    "list_files": {
        "required_slots": ["directory_path"],
        "tool_name": "list_files",
        "description": "List files in a directory."
    },
    
    # Email
    "read_emails": {
        "required_slots": [], # optional folder/max
        "tool_name": "read_emails",
        "description": "Read recent emails."
    },
    "send_email": {
        "required_slots": ["to", "subject", "content"],
        "tool_name": "send_email",
        "description": "Send an email."
    },
    
     # System
    "get_system_info": {
        "required_slots": [],
        "tool_name": "get_system_info",
        "description": "Get system information."
    }
}
