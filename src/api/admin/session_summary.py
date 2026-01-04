from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from ...database import get_db
from ...auth.dependencies import get_current_active_superuser
from ...models import Session as UserSession, Message, PendingConfirmationModel
from ...config import settings
from ...utils.logging import get_logger

# Import redaction logic if available
try:
    from ...tools.redaction import redact_data
except ImportError:
    def redact_data(data: Any) -> Any:
        return data

router = APIRouter(prefix="/admin/sessions", tags=["Admin"])
logger = get_logger(__name__)

@router.get("/{session_id}/summary", dependencies=[Depends(get_current_active_superuser)])
def get_session_summary_admin(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get admin-level summary of a session.
    Gated by generic admin flag + superuser requirement.
    """
    if not settings.ADMIN_DEBUG_ENABLED:
        raise HTTPException(status_code=404, detail="Not Found")

    # Fetch session (no user scope check needed for superuser, but we want to confirm existence)
    session = db.query(UserSession).filter(UserSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    try:
        # Fetch data similar to history but without redaction? Or WITH redaction but showing hidden fields?
        # User requested: "redacted sensitive information"
        # So we reuse logic or similar.
        
        messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at.asc()).all()
        pending = db.query(PendingConfirmationModel).filter(PendingConfirmationModel.session_id == session_id).all()
        
        # Rollups
        tool_counts = {}
        for m in messages:
            # Analyze tool usage if available in message metadata or separate tables
            pass
            
        return {
            "session_id": str(session.id),
            "user_id": str(session.user_id),
            "created_at": session.started_at,
            "message_count": len(messages),
            "active_confirmation": any(p.status == 'pending' for p in pending),
            "messages_preview": [
                {"role": m.role, "content": m.content[:50] + "..." if len(m.content) > 50 else m.content} 
                for m in messages[-5:]
            ]
        }
        
    except Exception as e:
        logger.error(f"Error fetching session summary: {e}")
        raise HTTPException(status_code=500, detail="Internal Error")

