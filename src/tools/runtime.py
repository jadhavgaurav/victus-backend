import logging
import traceback
import time
from uuid import UUID, uuid4
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session
from pydantic import ValidationError

from .contracts import ToolResult
from .registry import get_tool
from .redaction import redact
from .guards import ToolGuards
from ..policy.contracts import PolicyCheck
from ..policy.service import check_and_record_policy
from ..models.tool_call import ToolCall
from ..models.user import User
from ..models.session import Session as SessionModel
from ..security.scopes import Scope, ScopeSet

logger = logging.getLogger(__name__)

class ToolRuntime:
    def execute(
        self, 
        user_id: UUID, 
        session_id: UUID, 
        tool_name: str, 
        args_dict: Dict[str, Any], 
        db: Session,
        intent_summary: Optional[str] = None,
        trace: Optional[Any] = None
    ) -> ToolResult:
        """
        The ONLY supported way to execute tools.
        Enforces: Registry -> Validation -> Policy -> Guards -> Execution -> Redaction -> Persistence.
        """
        start_time = time.time()
        
        # 1. Registry Lookup
        tool_entry = get_tool(tool_name)
        if not tool_entry:
            return self._record_and_return_error(
                db, user_id, session_id, tool_name, args_dict, 
                "Tool not found in registry", 
                "denied", 
                start_time
            )
        
        tool_spec, tool_func = tool_entry

        # 1.5 Scope Check
        # Fetch user/session to check scopes
        # Using db session passed in.
        
        # We need to efficiently fetch only scopes potentially?
        # For now, fetching objects is fine.
        db_user = db.query(User).filter(User.id == user_id).first()
        db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()

        if not db_user:
             # Should not happen if authenticated, but safety
             return self._record_and_return_error(
                db, user_id, session_id, tool_name, args_dict,
                "User not found for scope check",
                "denied",
                start_time
            )
            
        # Determine effective scopes
        # Default to User scopes, override if Session has specific override (optional)
        # Assuming user.scopes is list of strings
        user_scopes = db_user.scopes or []
        # If session override exists, it MIGHT replace or append. 
        # Requirement: "per-session restrictions (optional override)". 
        # Usually override means "use this instead". Or it restricts?
        # Safe default: if override, use it. If not, use user.
        effective_scopes_list = db_session.scopes_override if (db_session and db_session.scopes_override is not None) else user_scopes
        
        scope_set = ScopeSet.from_list(effective_scopes_list)
        
        # Check tool requirement
        # tool_spec is expected to be SafeTool instance
        required = getattr(tool_spec, "required_scope", Scope.CORE.value)
        
        if not scope_set.has(Scope(required)):
             return self._record_and_return_error(
                db, user_id, session_id, tool_name, args_dict,
                f"SCOPE_MISSING: Required '{required}' but have {scope_set.to_list()}",
                "denied",
                start_time
            )

        # 2. Validation
        try:
            validated_args = tool_spec.args_model(**args_dict)
            # Use data dict for policy checks to avoid pydantic objects in logic if needed,
            # or keep clean.
            clean_args = validated_args.model_dump()
        except ValidationError as e:
            # Safe error message
            safe_error = f"Validation Error: {str(e)}"
            return self._record_and_return_error(
                db, user_id, session_id, tool_name, args_dict,
                safe_error,
                "error",
                start_time
            )

        # 3. Policy Check
        # Redact args for policy preview
        redacted_args, _ = redact(clean_args)
        
        policy_check = PolicyCheck(
            user_id=user_id,
            session_id=session_id,
            tool_name=tool_name,
            action_type=tool_spec.default_action_type,
            target_entity=tool_spec.category, # Simplified mapping
            scope=tool_spec.default_scope, 
            sensitivity=tool_spec.default_sensitivity,
            intent_summary=intent_summary or f"Execute {tool_name}",
            tool_args_preview=redacted_args
        )
        
        policy_decision = check_and_record_policy(policy_check, db)
        
        # 4. Handle Policy Decision
        if policy_decision.decision == "DENY":
            return self._record_and_return_error(
                db, user_id, session_id, tool_name, redacted_args,
                f"Policy denied: {policy_decision.reason_code}",
                "denied",
                start_time,
                policy_decision_id=policy_decision.id
            )
            
        if policy_decision.decision in ("ALLOW_WITH_CONFIRMATION", "ESCALATE"):
            # Ensure pending confirmation exists (handled by check_and_record_policy)
            # We need to find the pending ID. Querying it back might be needed if service didn't return it.
            # Service persists it. We can find it by session/tool/status=pending.
            
            # For simplicity/efficiency we could have had service return it, but adhering to signature.
            # Let's query it.
            from ..models.policy import PendingConfirmationModel
            pending = db.query(PendingConfirmationModel).filter(
                             PendingConfirmationModel.session_id == session_id,
                             PendingConfirmationModel.status == "pending",
                             # created recently?
                      ).order_by(PendingConfirmationModel.created_at.desc()).first()
            
            pending_id = pending.id if pending else None
            
            # Record attempt (status needs_confirmation isn't standard tool_call status usually, use 'pending' or 'error'?)
            # Prompt says: "persist tool_calls row with status=error or pending-like status"
            self._persist_tool_call(
                db, user_id, session_id, tool_name, redacted_args, 
                "Policy requires confirmation", 
                "needs_confirmation", 
                int((time.time() - start_time) * 1000)
            )

            return ToolResult(
                status="needs_confirmation",
                latency_ms=int((time.time() - start_time) * 1000),
                policy_decision_id=policy_decision.id,
                pending_confirmation_id=pending_id,
                confirmation_prompt=policy_decision.user_prompt
            )

        # 5. Guards (Rate Limits & Loops)
        guards = ToolGuards(db)
        if not guards.check_rate_limit(session_id, tool_name):
             return self._record_and_return_error(
                db, user_id, session_id, tool_name, redacted_args,
                "Rate limit exceeded",
                "denied",
                start_time,
                policy_decision_id=policy_decision.id
            )
            
        if not guards.check_loop_breaker(session_id, tool_name):
             return self._record_and_return_error(
                db, user_id, session_id, tool_name, redacted_args,
                "Loop detected: repeated failures",
                "error",
                start_time,
                policy_decision_id=policy_decision.id
            )

        # 6. Execution
        try:
            # We assume tool_func takes simple args or dependency injection is handled outside runtime OR 
            # we need to inject DB if the tool expects it?
            # Prompt: "If tools use DB, inject via dependency, not global engine creation."
            # "Tool callable must not receive raw DB sessions unless your existing tools require it."
            
            # We'll pass validated args. If tool needs 'db', we might need introspection or convention.
            # For now, simplistic **clean_args call.
            
            # NOTE: If we are wrapping existing tools, they might expect specific signatures.
            # We assume existing tool adapter (Step 6G) handles signature matching.
            
            result_data = tool_func(**clean_args)
            
            # 7. Redaction of Result
            redacted_result, result_redactions = redact(result_data)
            
            # 8. Success Persistence
            self._persist_tool_call(
                db, user_id, session_id, tool_name, redacted_args, 
                redacted_result, 
                "success", 
                int((time.time() - start_time) * 1000)
            )
            
            return ToolResult(
                status="success",
                data=redacted_result if isinstance(redacted_result, dict) else {"result": redacted_result},
                latency_ms=int((time.time() - start_time) * 1000),
                redactions_applied=result_redactions,
                policy_decision_id=policy_decision.id
            )

        except Exception as e:
            # Runtime error
            trace = traceback.format_exc()
            logger.error(f"Tool execution failed: {tool_name} {trace}")
            
            return self._record_and_return_error(
                db, user_id, session_id, tool_name, redacted_args,
                f"Execution Error: {str(e)}", # Safe string
                "error",
                start_time,
                policy_decision_id=policy_decision.id
            )

    def _record_and_return_error(
        self, db, user_id, session_id, tool_name, args, error_msg, status, start_time, policy_decision_id=None
    ) -> ToolResult:
        latency = int((time.time() - start_time) * 1000)
        
        # Redact args if not already redacted (in registry fail case it might be raw)
        safe_args, _ = redact(args)
        
        self._persist_tool_call(
            db, user_id, session_id, tool_name, safe_args, 
            {"error": error_msg}, 
            status if status != "denied" else "error", # Persist denied as error? Or keep denied? ToolCall status usually success/error.
            latency
        )
        
        return ToolResult(
            status=status,
            error=error_msg,
            latency_ms=latency,
            policy_decision_id=policy_decision_id
        )

    def _persist_tool_call(self, db, user_id, session_id, tool_name, args, result, status, latency):
        try:
            # Ensure args and result are JSON serializable (dicts).
            # If result is not dict, wrap it?
            # ToolCall model expects JSON/String? 
            # Looking at existing ToolCall model from context or assuming standard.
            # Step 3 prompt mentioned "tool_calls tables" were created.
            
            # Using str conversion for session_id/user_id just in case DB model expects str UUIDs.
            
            call = ToolCall(
                id=str(uuid4()),
                session_id=str(session_id), # Assuming model takes string or UUID
                user_id=str(user_id) if hasattr(user_id, 'hex') else user_id, # Handle UUID obj
                tool_name=tool_name,
                args=args, # Correct column name
                result=result, # Correct column name is 'result'
                status=status,
                latency_ms=latency # Assuming model has latency_ms or we check model definition again
            )
            db.add(call)
            db.commit()
        except Exception as e:
            logger.error(f"Failed to persist tool call: {e}")
            db.rollback()
