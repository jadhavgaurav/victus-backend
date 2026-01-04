"""
Main FastAPI application for Project VICTUS
"""

import os
# Fix OpenMP runtime conflict on macOS
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

from contextlib import asynccontextmanager  # noqa: E402

from fastapi import FastAPI, Request  # noqa: E402
from fastapi.responses import JSONResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402

# Local Imports
from .database import init_db  # noqa: E402
from .tools.config import async_client  # noqa: E402
from .config import settings  # noqa: E402
from .utils.logging import get_logger  # noqa: E402
from .utils.security import setup_cors, setup_rate_limiting  # noqa: E402

from .auth import router as auth_router  # noqa: E402
from .api import (  # noqa: E402
    health_router,
    chat_router,
    documents_router,
    voice_router,
    conversations_router,
    facts_router,
    email_router,
    calendar_router,
    stats_router,
    pages,
    settings as settings_api,
)
from .api.routes import approvals, traces  # noqa: E402
from .middleware import TraceMiddleware  # noqa: E402
from .security.csrf import CSRFMiddleware

logger = get_logger(__name__)

# Lifecycle Manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Project VICTUS AI Assistant...")
    init_db()
    
    # Initialize global HTTP client
    # async_client is strictly for internal tool use if needed, usually init lazily
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    await async_client.aclose()

# FastAPI App Definition
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Advanced AI Personal Assistant with Voice Capabilities",
    lifespan=lifespan
)

# Setup Security
setup_cors(app)
setup_rate_limiting(app)

# Mount Static Files (Frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Middleware
app.add_middleware(CSRFMiddleware)
app.add_middleware(TraceMiddleware)

# Register Routers
app.include_router(auth_router)
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(voice_router)
# Voice WebSocket
from .voice.ws import router as voice_ws_router
app.include_router(voice_ws_router)
app.include_router(conversations_router)
app.include_router(facts_router)
app.include_router(email_router)
app.include_router(calendar_router)
app.include_router(approvals.router)
app.include_router(traces.router)

from .api.sessions import history as session_history
from .api.sessions import message as session_message
from .api.sessions import create as session_create
from .api.admin import session_summary as admin_session_summary
app.include_router(session_history.router)
app.include_router(session_message.router, prefix="/sessions")
app.include_router(session_create.router, prefix="/sessions")
app.include_router(admin_session_summary.router)
app.include_router(settings_api.router)
app.include_router(stats_router)

# Dev Routes
if settings.ENVIRONMENT in ["development", "local", "dev"]:
    from .api import dev
    app.include_router(dev.router)
app.include_router(pages.router)  # HTML Pages

# Global Exception Handler (Optional but good practice)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )
