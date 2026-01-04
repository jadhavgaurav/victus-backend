from uuid import UUID
from sqlalchemy.orm import Session
from ..models.tool_execution import AgentMessage

def save_user_message(
    db: Session,
    user_id: UUID, 
    session_id: UUID, 
    content: str, 
    modality: str = "text",
    trace_id: str = None,
    idempotency_key: str = None
) -> AgentMessage:
    """
    Persists the user's raw command/message.
    """
    # Check for existing message (Idempotency)
    if idempotency_key:
        existing = db.query(AgentMessage).filter(
            AgentMessage.idempotency_key == idempotency_key,
            AgentMessage.session_id == session_id,
            AgentMessage.role == "user"
        ).first()
        if existing:
            return existing

    msg = AgentMessage(
        user_id=user_id,
        session_id=session_id,
        role="user",
        content=content,
        modality=modality,
        trace_id=trace_id,
        idempotency_key=idempotency_key,
        status="COMPLETED" # User message is received=completed
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
    modality: str = "text",
    trace_id: str = None
) -> AgentMessage:
    """
    Persists the assistant's final response.
    """
    msg = AgentMessage(
        user_id=user_id,
        session_id=session_id,
        role="assistant",
        content=content,
        modality=modality,
        trace_id=trace_id,
        status="COMPLETED"
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
