from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import hmac

class CSRFMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.safe_methods = {"GET", "HEAD", "OPTIONS", "TRACE"}

    async def dispatch(self, request: Request, call_next):
        # Skip CSRF for tests
        # Import inside method to avoid circular imports if config imports middleware (unlikely but safe)
        from ..config import settings
        if settings.ENVIRONMENT == "test":
             return await call_next(request)

        if request.method in self.safe_methods:
            return await call_next(request)

        # Skip CSRF for special paths if necessary (e.g. webhooks, public APIs without auth)
        # For now, enforce globally.
        # Logic: 
        # 1. Cookie must exist.
        # 2. Header "X-CSRF-Token" must match cookie.
        
        csrf_cookie = request.cookies.get("csrf_token")
        csrf_header = request.headers.get("x-csrf-token")

        if not csrf_cookie or not csrf_header:
            return JSONResponse(
                status_code=403, 
                content={"detail": "CSRF token missing (cookie or header)"}
            )

        # Secure comparison
        if not hmac.compare_digest(csrf_cookie, csrf_header):
             return JSONResponse(
                status_code=403, 
                content={"detail": "CSRF token mismatch"}
            )

        return await call_next(request)
