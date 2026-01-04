from datetime import datetime, timezone
from uuid import UUID
from typing import Dict, Any

from sqlalchemy.orm import Session
from ..models.policy import PendingConfirmationModel

def resolve_confirmation(
    user_id: UUID, 
    session_id: UUID, 
    confirmation_id: UUID, 
    user_utterance: str,
    db: Session
) -> Dict[str, Any]:
    """
    Attempts to resolve a pending confirmation based on user input.
    """
    confirmation = db.query(PendingConfirmationModel).filter(
        PendingConfirmationModel.id == confirmation_id,
        PendingConfirmationModel.user_id == user_id,
        PendingConfirmationModel.session_id == session_id
    ).first()
    
    if not confirmation:
        return {"status": "error", "message": "Confirmation not found"}
    
    if confirmation.status != "pending":
        return {"status": "error", "message": f"Confirmation is already {confirmation.status}"}
        
    if confirmation.expires_at and confirmation.expires_at < datetime.now(timezone.utc):
        confirmation.status = "expired"
        db.commit()
        return {"status": "error", "message": "Confirmation expired"}

    # Check required phrase if present
    if confirmation.required_phrase:
         # Normalize for comparison (basic case-insensitivity)
         if confirmation.required_phrase.lower() not in user_utterance.lower():
             return {
                 "status": "still_pending",
                 "message": f"Please say exactly: '{confirmation.required_phrase}' to confirm."
             }
             
    # If we got here, it's confirmed
    confirmation.status = "confirmed"
    db.commit()
    
    return {
        "status": "confirmed",
        "tool_name": confirmation.tool_name,
        "tool_args": confirmation.tool_args
    }

def cancel_confirmation(
    user_id: UUID, 
    session_id: UUID, 
    confirmation_id: UUID, 
    db: Session
) -> Dict[str, Any]:
    """
    Explicitly cancels a pending confirmation.
    """
    confirmation = db.query(PendingConfirmationModel).filter(
        PendingConfirmationModel.id == confirmation_id,
        PendingConfirmationModel.user_id == user_id
    ).first()
    
    if not confirmation:
        return {"status": "error", "message": "Confirmation not found"}
        
    confirmation.status = "cancelled"
    db.commit()
    
    return {"status": "cancelled"}

def create_confirmation(
    user_id: UUID,
    session_id: UUID,
    tool_name: str,
    tool_args: Dict[str, Any],
    decision_type: str,
    required_phrase: str = None,
    db: Session = None,
    expiry_seconds: int = 300
) -> PendingConfirmationModel:
    """
    Creates a new confirmation and cancels any existing active ones for this session.
    """
    # 1. Cancel existing active confirmations
    active = db.query(PendingConfirmationModel).filter(
        PendingConfirmationModel.session_id == session_id,
        PendingConfirmationModel.status == "pending"
    ).all()
    
    for conf in active:
        conf.status = "cancelled"
    
    # 2. Create new
    from datetime import timedelta
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expiry_seconds)
    
    new_conf = PendingConfirmationModel(
        user_id=user_id,
        session_id=session_id,
        tool_name=tool_name,
        tool_args=tool_args,
        decision_type=decision_type,
        required_phrase=required_phrase,
        status="pending",
        expires_at=expires_at
    )
    db.add(new_conf)
    db.commit()
    db.refresh(new_conf)
    return new_conf

