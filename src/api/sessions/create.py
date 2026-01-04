from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
# imports removed
from sqlalchemy.orm import Session as DbSession

from ...database import get_db
from ...auth.dependencies import get_current_user
from ...models import Session
from ...utils.logging import get_logger
from ...utils.security import limiter

logger = get_logger(__name__)
router = APIRouter()

class CreateSessionResponse(BaseModel):
    session_id: str

@router.post("/", response_model=CreateSessionResponse)
@limiter.limit("30/minute")
async def create_session(
    request: Request,
    db: DbSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new server-owned session.
    """
    try:
        new_session = Session(
            user_id=current_user.id,
            metadata_={
                "created_by": "ui",
                "client": "web"
            }
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        
        return CreateSessionResponse(session_id=str(new_session.id))
    except Exception as e:
        logger.error(f"Error creating session: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create session"
        )
