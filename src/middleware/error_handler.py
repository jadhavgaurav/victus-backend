import uuid
import time
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from ..utils.logging import get_logger

logger = get_logger(__name__)

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Generate Trace ID
        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
            # Add trace_id to response headers
            response.headers["X-Trace-ID"] = trace_id
            return response
            
        except Exception as exc:
            duration = time.time() - start_time
            
            # Log full details
            logger.error(
                f"Unhandled exception",
                extra={
                    "trace_id": trace_id,
                    "path": request.url.path,
                    "method": request.method,
                    "duration": duration,
                    "error": str(exc)
                },
                exc_info=True
            )
            
            # Return standardized error response
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": "An unexpected error occurred. Please report this trace ID.",
                        "trace_id": trace_id
                    }
                }
            )
