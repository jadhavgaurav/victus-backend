from fastapi import APIRouter, Depends, HTTPException, status, Request
from ...utils.security import limiter
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from ...database import get_db
from ...auth.dependencies import get_current_user
from ...models import Session
from ...agent.orchestrator import AgentOrchestrator
from ...utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

class MessageRequest(BaseModel):
    content: str

class MessageResponse(BaseModel):
    assistant_text: str
    session_id: str
    pending_confirmation: Optional[dict] = None
    request_id: Optional[str] = None

@router.post("/{session_id}/message", response_model=MessageResponse)
@limiter.limit("30/minute")
async def post_session_message(
    session_id: str,
    request: Request,
    body: MessageRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Send a keyed message to a specific session.
    Validates ownership and invokes appropriate agent logic.
    """
    # 1. Validate Session Ownership
    # Using 'Session' model as the session record.
    session = db.query(Session).filter(
        Session.id == session_id,
        Session.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    # 1.5 Idempotency Check (A3.2)
    idempotency_key = request.headers.get("Idempotency-Key")
    if not idempotency_key:
        # Generate stable key based on session + content
        import hashlib
        idempotency_key = hashlib.sha256(f"{session_id}:{body.content}".encode()).hexdigest()

    # Check if User Message already exists
    from ...models.tool_execution import AgentMessage
    existing_msg = db.query(AgentMessage).filter(
        AgentMessage.role == "user",
        AgentMessage.idempotency_key == idempotency_key,
        AgentMessage.session_id == session_id
    ).first()

    if existing_msg:
        # Check for correlated Assistant Message
        # We assume trace_id links them.
        if existing_msg.trace_id:
             assistant_msg = db.query(AgentMessage).filter(
                 AgentMessage.role == "assistant",
                 AgentMessage.trace_id == existing_msg.trace_id
             ).first()
             
             if assistant_msg:
                 return MessageResponse(
                     assistant_text=assistant_msg.content,
                     session_id=session_id,
                     pending_confirmation=None, # Rehydrating this might require metadata storage?
                     request_id=assistant_msg.trace_id
                 )
        # If no assistant msg, it might be processing or failed.
        # We could return 409 or retry.
        # For now, we proceed to retry (exactly-once logic in tools handles side effects).
        logger.warning(f"Idempotency hit {idempotency_key} but no response found. Retrying.")

    # 2. Invoke Orchestrator
    orchestrator = AgentOrchestrator()
    try:
        # handle_user_utterance now accepts idempotency_key
        result = orchestrator.handle_user_utterance(
            db=db,
            user_id=current_user.id,
            session_id=session_id,
            utterance=body.content,
            modality="text",  # Explicitly text
            idempotency_key=idempotency_key
        )

        # 3. Construct Response
        return MessageResponse(
            assistant_text=result.assistant_text,
            session_id=session_id,
            pending_confirmation=result.pending_confirmation,
            request_id=result.metadata.get("request_id") if result.metadata else None
        )

    except Exception as e:
        logger.error(f"Error handling message for session {session_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e) 
        )
