
import os
# Set env vars BEFORE importing app
os.environ["OPENAI_API_KEY"] = "sk-test-key"
os.environ["SMTP_USER"] = "test"
os.environ["SMTP_PASS"] = "test"
os.environ["SMTP_HOST"] = "localhost"
os.environ["FROM_EMAIL"] = "test@example.com"
os.environ["SMTP_PORT"] = "587"

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import MagicMock
from uuid import uuid4

from src.main import app
from src.auth.dependencies import get_current_user
from src.database import get_db
from src.models import User, Session as UserSession

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", cookies={"csrf_token": "test-token"}) as client:
        yield client

@pytest.fixture
def mock_user():
    user = MagicMock(spec=User)
    user.id = uuid4()
    user.is_active = True
    return user

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def token_headers(mock_user, mock_db_session):
    # Override dependencies for authenticated requests
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db_session
    yield {"Authorization": "Bearer test", "X-CSRF-Token": "test-token"}
    app.dependency_overrides.clear()

@pytest.fixture
def csrf_headers():
    return {"X-CSRF-Token": "test-token"}
