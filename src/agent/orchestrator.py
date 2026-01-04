from uuid import UUID
from sqlalchemy.orm import Session

from ..utils.logging import get_logger
from ..policy.confirmations import resolve_confirmation
from ..models.policy import PendingConfirmationModel
from ..tools.runtime import ToolRuntime
from .message_store import save_user_message, save_assistant_message
from .contracts import OrchestratorResponse
from .intent_parser import parse_intent
from .context import get_context
from .planner import build_plan

logger = get_logger(__name__)

class AgentOrchestrator:
    def __init__(self):
        self.tool_runtime = ToolRuntime()
        
    def handle_user_utterance(
        self,
        db: Session,
        user_id: UUID,
        session_id: UUID,
        utterance: str,
        modality: str = "voice",
        idempotency_key: str = None
    ) -> OrchestratorResponse:
        """
        Main entry point for handling a user command.
        """
        
        
        # Start Trace
        from ..observability.langfuse_client import langfuse_client
        
        trace = langfuse_client.trace(
            name="victus.command",
            user_id=str(user_id),
            session_id=str(session_id),
            input={"utterance": utterance, "modality": modality}
        )
        
        # 1. Persist User Message
        save_user_message(db, user_id, session_id, utterance, modality, trace_id=trace.id, idempotency_key=idempotency_key)
        
        # 2. Check for Pending Confirmation Logic
        pending_conf = db.query(PendingConfirmationModel).filter(
            PendingConfirmationModel.session_id == session_id,
            PendingConfirmationModel.user_id == user_id,
            PendingConfirmationModel.status == "pending"
        ).first()
        
        if pending_conf:
            logger.info(f"Attempting to resolve confirmation {pending_conf.id} with: {utterance}")
            langfuse_client.observe(trace, "confirmation.resolve_attempt", input=utterance)
            
            resolution = resolve_confirmation(user_id, session_id, pending_conf.id, utterance, db)
            
            langfuse_client.observe(trace, "confirmation.resolution", output=resolution)
            
            if resolution["status"] == "confirmed":
                tool_name = resolution["tool_name"]
                tool_args = resolution["tool_args"]
                
                # Execute via Runtime
                result = self.tool_runtime.execute(
                    user_id=user_id,
                    session_id=session_id,
                    tool_name=tool_name,
                    args_dict=tool_args,
                    db=db,
                    trace=trace
                )
                
                response_text = self._summarize_result(result)
                save_assistant_message(db, user_id, session_id, response_text, modality, trace_id=trace.id)
                
                trace.update(output=response_text)
                return OrchestratorResponse(
                     assistant_text=response_text,
                     should_speak=True,
                     metadata={"tool_result": result.model_dump()}
                )
                
            elif resolution["status"] == "still_pending":
                 msg = resolution["message"]
                 save_assistant_message(db, user_id, session_id, msg, modality, trace_id=trace.id)
                 trace.update(output=msg)
                 return OrchestratorResponse(assistant_text=msg, should_speak=True)
                 
            else:
                msg = f"Confirmation failed: {resolution.get('message')}"
                save_assistant_message(db, user_id, session_id, msg, modality, trace_id=trace.id)
                trace.update(output=msg)
                return OrchestratorResponse(assistant_text=msg, should_speak=True)

        # 3. Context Retrieval (A2.6)
        context = get_context(db, user_id, session_id, utterance)
        langfuse_client.observe(trace, "context.retrieved", output={"context_len": len(context)})

        # Serialize Context
        history_txt = "\n".join([f"{m['role']}: {m['content']}" for m in context.get("history", [])[-3:]])
        memories_txt = "\n".join(context.get("memory_facts", []))
        context_str = f"Conversation History:\n{history_txt}\n\nRelevant Memories:\n{memories_txt}"

        # 4. Intent Parsing
        intent = parse_intent(utterance, context_str=context_str)
        langfuse_client.observe(trace, "intent.parsed", output=intent.model_dump())
        
        # 5. Planning
        plan = build_plan(intent, context)
        langfuse_client.observe(trace, "plan.built", output=plan.model_dump())
        
        if plan.requires_user_input:
            msg = plan.clarifying_question or "Could you clarify that?"
            save_assistant_message(db, user_id, session_id, msg, modality, trace_id=trace.id)
            trace.update(output=msg)
            return OrchestratorResponse(assistant_text=msg, should_speak=True)
            
        # 6. Execute Plan Steps
        results = []
        for step in plan.steps:
            langfuse_client.observe(trace, "tool.execution_start", input={"tool": step.tool_name, "args": step.args})
            
            result = self.tool_runtime.execute(
                user_id=user_id,
                session_id=session_id,
                tool_name=step.tool_name,
                args_dict=step.args,
                db=db,
                trace=trace
            )
            results.append(result)
            
            langfuse_client.observe(trace, "tool.execution_result", output=result.model_dump())
            
            if result.status != "success":
                break
                
        # 7. Response Generation
        final_result = results[-1] if results else None
        
        if not final_result:
             msg = "I didn't do anything."
             save_assistant_message(db, user_id, session_id, msg, modality, trace_id=trace.id)
             trace.update(output=msg)
             return OrchestratorResponse(assistant_text=msg)
             
        response_text = self._summarize_result(final_result)
        save_assistant_message(db, user_id, session_id, response_text, modality, trace_id=trace.id)
        
        trace.update(output=response_text)
        # Helper to extract confirmation info
        pending_conf_data = None
        if final_result.status == "needs_confirmation":
             pending_conf_data = {
                 "id": str(final_result.pending_confirmation_id) if final_result.pending_confirmation_id else None,
                 "prompt": final_result.confirmation_prompt
             }

        return OrchestratorResponse(
            assistant_text=response_text,
            should_speak=True,
            metadata={"tool_result": final_result.model_dump()},
            pending_confirmation=pending_conf_data
        )

    def _summarize_result(self, result) -> str:
        """
        Converts ToolResult into a voice-friendly string.
        """
        if result.status == "success":
            # Heuristic summary or data inspection
            # If data has a 'message' field, use it.
            if result.data and "message" in result.data:
                return f"Done. {result.data['message']}"
            return "Done."
            
        elif result.status == "needs_confirmation":
            # The runtime (via policy) might provide a prompt, or we generate one.
            # Contracts might need update to pass policy prompt up, but we can default:
            return result.confirmation_prompt or "This action requires approval. Please say the confirmation phrase."
            
        elif result.status == "denied":
            return f"I cannot do that. {result.error or 'Policy denied action.'}"
            
        elif result.status == "error":
            return f"Something went wrong. {result.error}"
            
        return "Command completed."
