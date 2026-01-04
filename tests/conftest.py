
import os
# Set env vars BEFORE importing app
os.environ["ENVIRONMENT"] = "test"
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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base, get_db

# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()

    # Override the dependency
    app.dependency_overrides[get_db] = lambda: session
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
    app.dependency_overrides.clear() # Clear overrides after test

@pytest.fixture
def csrf_headers():
    return {"X-CSRF-Token": "test-token"}
