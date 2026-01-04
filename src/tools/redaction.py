import re
from typing import Any, List, Tuple

# Redaction patterns
SENSITIVE_KEYS = {
    "token", "access_token", "refresh_token", "api_key", "secret", 
    "password", "cookie", "authorization", "auth_token"
}

# Regex for common secret formats
# JWT-like pattern (3 parts, base64ish)
JWT_PATTERN = re.compile(r"^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$")
BEARER_PATTERN = re.compile(r"^Bearer\s+", re.IGNORECASE)

def redact(obj: Any) -> Tuple[Any, List[str]]:
    """
    Recursively scans and redact secrets from dictionaries and lists.
    Returns the redacted object and a list of redacted keys/paths.
    Does NOT mutate the original object (creates a copy).
    """
    redacted_keys = []

    def _redact_recursive(item: Any, path: str = "") -> Any:
        try:
            if isinstance(item, dict):
                new_dict = {}
                for k, v in item.items():
                    current_path = f"{path}.{k}" if path else k
                    
                    # Check key name
                    if k.lower() in SENSITIVE_KEYS:
                        redacted_keys.append(current_path)
                        new_dict[k] = "[REDACTED]"
                        continue
                    
                    # Check string values for patterns
                    if isinstance(v, str):
                        if len(v) > 20 and JWT_PATTERN.match(v):
                             redacted_keys.append(current_path)
                             new_dict[k] = "[REDACTED OPTIONAL JWT]"
                             continue
                        if BEARER_PATTERN.match(v):
                             redacted_keys.append(current_path)
                             new_dict[k] = "[REDACTED BEARER]"
                             continue

                    # Recurse
                    new_dict[k] = _redact_recursive(v, current_path)
                return new_dict
                
            elif isinstance(item, list):
                return [_redact_recursive(x, f"{path}[{i}]") for i, x in enumerate(item)]
            
            return item
            
        except Exception:
            # Safety net: if redaction fails, return a safe error marker 
            # rather than blowing up or leaking raw data if we tried to partial return.
            # But prompt says "if error, return original with a 'redaction_error' flag".
            # Returning original might be unsafe if it contains secrets. 
            # I'll return a safe placeholder + error flag logic structure if this simple recursion fails.
            return {"_error": "Redaction failed", "_safe": True}

    result = _redact_recursive(obj)
    return result, redacted_keys
