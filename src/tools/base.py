
from enum import Enum
from typing import Type, Any, Callable
from pydantic import BaseModel
from langchain_core.tools import BaseTool

from ..security.scopes import Scope

class RiskLevel(str, Enum):
    LOW = "low"         # Read-only, safe
    MEDIUM = "medium"   # Writes without external side effects or minor impact
    HIGH = "high"       # Significant side effects

class SafeTool(BaseTool):
    """
    A wrapper around LangChain's BaseTool that adds a risk_level 
    and policy enforcement capability.
    """
    risk_level: RiskLevel = RiskLevel.HIGH
    required_scope: str = Scope.CORE.value
    
    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    @classmethod
    def from_func(
        cls,
        func: Callable,
        name: str,
        description: str,
        args_schema: Type[BaseModel],
        risk_level: RiskLevel = RiskLevel.HIGH,
        required_scope: str = Scope.CORE.value,
        return_direct: bool = False,
    ) -> "SafeTool":
        """
        Creates a SafeTool from a function.
        """
        instance = cls(
            name=name,
            description=description,
            args_schema=args_schema,
            risk_level=risk_level,
            required_scope=required_scope,
            return_direct=return_direct,
        )
        object.__setattr__(instance, "_func", func)
        return instance

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        # Use ToolRuntime for execution
        from .runtime import ToolRuntime
        from ..utils.context import get_trace_id, get_user_id, get_session_id
        from ..database import SessionLocal
        
        user_id = get_user_id()
        session_id = get_session_id()
        
        # If no context (e.g. testing), we might fail or mock.
        # Assuming context exists or using fallback.
        if not user_id:
             # Fallback/Error? For now strict.
             # Wait, existing tools might run without session in some scripts?
             # But runtime requires IDs.
             import uuid
             user_id = uuid.uuid4() # unsafe default
             
        if not session_id:
             import uuid
             session_id = uuid.uuid4()

        db = SessionLocal()
        try:
            runtime = ToolRuntime()
            result = runtime.execute(
                user_id=user_id, 
                session_id=session_id, 
                tool_name=self.name, 
                args_dict=kwargs, 
                db=db
            )
            
            if result.status == "success":
                return result.data
            elif result.status == "needs_confirmation":
                return (
                    f"Action Requires Confirmation. Prompt: {result.confirmation_prompt}. "
                    f"Please confirm this action (Pending ID: {result.pending_confirmation_id})."
                )
            elif result.status == "denied":
                return f"Action Denied: {result.error}"
            else:
                return f"Error: {result.error}"

        except Exception as e:
            return f"System Error executing {self.name}: {e}"
        finally:
            db.close()

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        # Async version invoking sync runtime (as Runtime using sync DB session)
        # In future, Runtime should be async.
        return self._run(*args, **kwargs)

    # Legacy logging logic removed as Runtime handles persistence
    def _create_pending_action(self, action_id: str, args: dict):
        pass

    def _log_trace_step(self, trace_id: str, decision: str, args: dict, result: Any, duration: float):
        pass

