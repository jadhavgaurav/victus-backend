from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from ..utils.logging import get_logger

logger = get_logger("audit")

class SecurityEventType(str, Enum):
    AUTH_LOGIN_SUCCESS = "auth.login.success"
    AUTH_LOGIN_FAILED = "auth.login.failed"
    AUTH_SIGNUP = "auth.signup"
    AUTH_LOGOUT = "auth.logout"
    
    FILE_UPLOAD = "file.upload"
    FILE_DELETE = "file.delete"
    
    POLICY_OVERRIDE = "policy.override"
    SENSITIVE_ACTION = "action.sensitive"
    
    RATE_LIMIT = "security.ratelimit"
    SSRF_BLOCKED = "security.ssrf_blocked"

def log_security_event(
    event_type: SecurityEventType,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None
):
    """
    Structured security logging.
    In MVP, logs to standard logger with special marker.
    In prod, ideally ship to SIEM/ELK.
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    
    log_entry = {
        "event_type": event_type.value,
        "timestamp": timestamp,
        "user_id": str(user_id) if user_id else "anonymous",
        "session_id": str(session_id) if session_id else None,
        "ip_address": ip_address,
        "details": details or {}
    }
    
    # Log with a distinct prefix or level
    logger.info(f"SECURITY_EVENT: {log_entry}")
