import re

class Redacter:
    """
    Utility to redact sensitive information from text.
    """
    
    # Simple regex patterns for common secrets
    PATTERNS = [
        (r"sk-[a-zA-Z0-9]{20,}T3BlbkFJ[a-zA-Z0-9]{20,}", "[REDACTED_OPENAI_KEY]"), # OpenAI key lookalike
        (r"sk-[a-zA-Z0-9]{32,}", "[REDACTED_KEY]"),
        (r"ghp_[a-zA-Z0-9]{36}", "[REDACTED_GITHUB_KEY]"),
        (r"Bearer [a-zA-Z0-9\-\._~\+\/]{20,}", "Bearer [REDACTED_TOKEN]"),
        (r"Password=[^;&]*", "Password=[REDACTED]"),
        (r"password=[^;&]*", "password=[REDACTED]"),
        # Email address (optional, maybe not secret but PII)
        # (r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[EMAIL]"),
    ]

    @staticmethod
    def redact(text: str) -> str:
        if not text:
            return text
        for pattern, replacement in Redacter.PATTERNS:
            text = re.sub(pattern, replacement, text)
        return text

def redact_text(text: str) -> str:
    return Redacter.redact(text)

def redact_dict(data: dict) -> dict:
    """
    Recursively redact string values in a dictionary.
    """
    if not data:
        return data
    new_data = data.copy()
    for k, v in new_data.items():
        if isinstance(v, str):
            new_data[k] = redact_text(v)
        elif isinstance(v, dict):
            new_data[k] = redact_dict(v)
        elif isinstance(v, list):
            new_data[k] = [redact_dict(i) if isinstance(i, dict) else redact_text(i) if isinstance(i, str) else i for i in v]
    return new_data
