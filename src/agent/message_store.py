from uuid import UUID
from sqlalchemy.orm import Session
from ..models.message import Message

def save_user_message(
    db: Session,
    user_id: UUID, 
    session_id: UUID, 
    content: str, 
    modality: str = "text"
) -> Message:
    """
    Persists the user's raw command/message.
    """
    msg = Message(
        user_id=user_id,
        session_id=session_id,
        role="user",
        content=content,
        modality=modality
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def save_assistant_message(
    db: Session,
    user_id: UUID, 
    session_id: UUID, 
    content: str, 
    modality: str = "text"
) -> Message:
    """
    Persists the assistant's final response.
    """
    msg = Message(
        user_id=user_id,
        session_id=session_id,
        role="assistant",
        content=content,
        modality=modality
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
