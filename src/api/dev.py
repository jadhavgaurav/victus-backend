from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from ..database import get_db
from ..models import User, Session as UserSession
from ..config import settings
from ..auth.routes import set_auth_cookies, generate_csrf_token
from ..utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/dev", tags=["Development"])

@router.post("/bootstrap")
async def bootstrap_dev_session(response: Response, request: Request, db: Session = Depends(get_db)):
    """
    Bootstrap a development session for the user 'dev@victus.local'.
    Only works if ENVIRONMENT is 'development' or 'local'.
    """
    if settings.ENVIRONMENT not in ["development", "local", "dev"]:
        raise HTTPException(status_code=403, detail="Dev tools disabled in non-dev environment")

    email = "dev@victus.local"
    
    # Find or Create Dev User
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.info(f"Dev user not found, creating {email}...")
        import secrets
        from ..auth.security import get_password_hash
        
        user = User(
            email=email,
            username="dev_user",
            full_name="Developer",
            is_active=True,
            is_verified=True,
            provider="local",
            hashed_password=get_password_hash("dev_password_insecure"), # Set a dummy password just in case
            avatar_url="https://api.dicebear.com/7.x/avataaars/svg?seed=dev_user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create Session
    session_token = str(uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    
    ip = request.client.host if request.client else "127.0.0.1"
    ua = request.headers.get("user-agent", "DevBootstrap")
    
    new_session = UserSession(
        id=session_token,
        user_id=user.id,
        expires_at=expires_at,
        metadata_={
            "user_agent": ua,
            "ip_address": ip,
            "type": "dev_bootstrap"
        }
    )
    db.add(new_session)
    db.commit()
    
    # Set Cookies
    csrf_token = generate_csrf_token()
    set_auth_cookies(response, session_token, csrf_token)
    
    logger.info(f"Bootstrapped dev session for {email}")
    
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "avatar_url": user.avatar_url,
            "is_superuser": user.is_superuser
        },
        "session": {
            "id": session_token,
            "expires_at": expires_at.isoformat()
        }
    }
