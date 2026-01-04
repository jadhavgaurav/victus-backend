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
from .middleware.error_handler import ErrorHandlerMiddleware
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
    
    # Initialize Agent Executor
    from .agent import create_agent_executor
    try:
        # RAG is enabled by default for now, or check settings
        app.state.agent_executor = create_agent_executor(rag_enabled=True)
        logger.info("Agent executor initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize agent executor: {e}")
        app.state.agent_executor = None
    
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
# Register Routers
from fastapi import APIRouter
from .voice.ws import router as voice_ws_router
from .api.sessions import history as session_history
from .api.sessions import message as session_message
from .api.sessions import create as session_create
from .api.admin import session_summary as admin_session_summary
from .api.memories import router as memories_router


api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(health_router)
api_router.include_router(chat_router)
api_router.include_router(documents_router)
api_router.include_router(voice_router)
api_router.include_router(voice_ws_router)
api_router.include_router(conversations_router)
api_router.include_router(facts_router)
api_router.include_router(email_router)
api_router.include_router(calendar_router)
api_router.include_router(approvals.router)
api_router.include_router(traces.router)
api_router.include_router(session_history.router)
api_router.include_router(session_message.router, prefix="/sessions")
api_router.include_router(session_create.router, prefix="/sessions")
api_router.include_router(memories_router)
api_router.include_router(admin_session_summary.router)
api_router.include_router(settings_api.router)
api_router.include_router(stats_router)

# Dev Routes
if settings.ENVIRONMENT in ["development", "local", "dev", "test"]:
    from .api import dev
    api_router.include_router(dev.router)

app.include_router(api_router)
app.include_router(pages.router)  # HTML Pages

# Global Exception Handler (Optional but good practice)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )
