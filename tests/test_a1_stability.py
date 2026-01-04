import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models import User, Session
from src.auth.security import get_password_hash
import uuid

client = TestClient(app)

@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(
        email=f"test_a1_{uuid.uuid4()}@example.com",
        username=f"test_a1_{uuid.uuid4()}",
        hashed_password=get_password_hash("password123"),
        is_active=True,
        is_verified=True,
        provider="local"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def auth_headers(test_user):
    """Login and get auth headers (cookies/token)."""
    # For A1 we use cookies. The test client handles cookies automatically if we use a session context
    # but here we might need to simulate the login flow or manually set cookies if using client.post directly.
    # simpler: bypass auth dependency or use the login endpoint.
    
    response = client.post("/api/auth/login", json={
        "email": test_user.email,
        "password": "password123"
    })
    assert response.status_code == 200
    # Cookies are stored in client.cookies
    return response.headers # or just rely on client state

def test_a1_create_session(test_user):
    """A1.2: Server-owned session creation."""
    # Login first
    response = client.post("/api/auth/login", json={
        "email": test_user.email,
        "password": "password123"
    })
    assert response.status_code == 200
    # Debug: Check if cookie is set
    assert "victus_session" in response.cookies, f"Login cookies: {response.cookies}"
    
    response = client.post("/api/sessions/")
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    
    # Verify it is a valid UUID
    session_id = data["session_id"]
    try:
        uuid.UUID(session_id)
    except ValueError:
        pytest.fail("Returned session_id is not a valid UUID")

from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_orchestratorv():
    with patch("src.api.sessions.message.AgentOrchestrator") as MockClass:
        instance = MockClass.return_value
        # Mock successful response
        response = MagicMock()
        response.assistant_text = "I am a mock agent"
        response.pending_confirmation = None
        response.metadata = {"request_id": "test-req-id"}
        instance.handle_user_utterance.return_value = response
        yield instance

def test_a1_message_valid_session(db_session, test_user, mock_orchestratorv):
    """A1.3: Message to valid session works."""
    # Login
    resp = client.post("/api/auth/login", json={
        "email": test_user.email,
        "password": "password123"
    })
    assert resp.status_code == 200
    assert "victus_session" in resp.cookies
    
    # Create session
    create_resp = client.post("/api/sessions/")
    session_id = create_resp.json()["session_id"]
    
    # Send message
    msg_resp = client.post(f"/api/sessions/{session_id}/message", json={
        "content": "Hello A1"
    })
    
    assert msg_resp.status_code == 200
    data = msg_resp.json()
    assert data["session_id"] == session_id
    assert "assistant_text" in data
    assert data["assistant_text"] == "I am a mock agent"

def test_a1_message_invalid_session(test_user):
    """A1.3: Message to random interactions returns 404."""
    # Login
    client.post("/api/auth/login", json={
        "email": test_user.email,
        "password": "password123"
    })
    
    random_id = str(uuid.uuid4())
    response = client.post(f"/api/sessions/{random_id}/message", json={
        "content": "Should fail"
    })
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"

def test_a1_trace_id_presence():
    """A1.5: Error responses have trace_id."""
    # Trigger a 404 (handled exception) or 500 (unhandled)
    # 404 usually handled by FastAPI default handler, might not have our custom trace_id wrapper if it's middleware
    # But our middleware wraps everything.
    
    response = client.get("/api/non-existent-endpoint-for-trace-check")
    # This returns 404. Check headers.
    assert "X-Trace-ID" in response.headers
    
    # Only our custom error handler returns JSON body with trace_id for 500s.
    # For standard responses, we check header.
