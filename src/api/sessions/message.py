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

    # 2. Invoke Orchestrator
    orchestrator = AgentOrchestrator()
    try:
        # Note: handle_user_utterance is synchronous in current design
        result = orchestrator.handle_user_utterance(
            db=db,
            user_id=current_user.id,
            session_id=session_id,
            utterance=body.content,
            modality="text"  # Explicitly text
        )

        # 3. Construct Response
        # Result is expected to be an AgentResponse object or similar
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
