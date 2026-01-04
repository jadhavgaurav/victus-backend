from enum import Enum
from typing import List, Set, Optional
from pydantic import BaseModel

class Scope(str, Enum):
    # Core capabilities (often default)
    EMAIL_READ = "tool.email.read"
    EMAIL_SEND = "tool.email.send"
    CALENDAR_READ = "tool.calendar.read"
    CALENDAR_WRITE = "tool.calendar.write"
    
    # Filesystem
    FILES_READ = "tool.files.read"
    FILES_WRITE = "tool.files.write"
    
    # Web / Network
    WEB_SEARCH = "tool.web.search"
    WEB_BROWSE = "tool.web.browse"
    
    # System / Admin
    SYSTEM_RAG = "tool.system.rag"
    SYSTEM_AUTOMATION = "tool.system.automation"
    
    # Catch-all for basic conversation memory etc
    CORE = "core"

class AccessError(Exception):
    """Raised when a scope check fails."""
    def __init__(self, required: Scope, available: Set[str]):
        self.required = required
        self.available = available
        super().__init__(f"Missing required scope: {required}. Available: {available}")

class ScopeSet(BaseModel):
    """Encapsulates a set of granted scopes."""
    scopes: Set[str] = set()

    def has(self, scope: Scope) -> bool:
        return scope.value in self.scopes

    def require(self, scope: Scope):
        if not self.has(scope):
            raise AccessError(scope, self.scopes)
    
    @classmethod
    def from_list(cls, items: List[str]) -> "ScopeSet":
        return cls(scopes=set(items))

    @classmethod
    def default_user_scopes(cls) -> List[str]:
        """Default scopes granted to a fresh user."""
        return [
            Scope.CORE.value,
            Scope.WEB_SEARCH.value,
            Scope.SYSTEM_RAG.value,
            Scope.FILES_READ.value, # Safe read own files
            # Write, Email, Calendar explicitly NOT default usually, but for VICTUS dev we might enable them.
            # Following prompt: "Default scopes must be least-privilege".
            # So let's keep it tight.
        ]

    def to_list(self) -> List[str]:
        return list(self.scopes)
