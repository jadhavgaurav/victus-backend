
import pytest
from httpx import AsyncClient
from uuid import uuid4
from unittest.mock import MagicMock

@pytest.mark.asyncio
async def test_post_message_to_existing_session(async_client: AsyncClient, token_headers, mock_db_session, mock_user):
    session_id = str(uuid4())
    
    # Mock finding the session
    mock_session = MagicMock()
    mock_session.id = session_id
    mock_session.user_id = mock_user.id
    
    # Setup query chain: db.query(Session).filter(...).first() -> mock_session
    # Note: validation does db.query(Session).filter(id==..., user_id==...).first()
    # We simplistically assume any query returns our mock for this test
    query_mock = mock_db_session.query.return_value
    filter_mock = query_mock.filter.return_value
    # Support multiple filter calls if chained
    filter_mock.filter.return_value = filter_mock 
    filter_mock.first.return_value = mock_session

    # 2. Post Message
    # We also need to mock the orchestrator since it's called after validation
    
    # We can patch 'src.api.sessions.message.AgentOrchestrator'
    from unittest.mock import patch
    with patch("src.api.sessions.message.AgentOrchestrator") as mock_orch_cls:
        mock_orch = mock_orch_cls.return_value
        mock_orch.handle_user_utterance.return_value.assistant_text = "I am ready"
        mock_orch.handle_user_utterance.return_value.pending_confirmation = None
        mock_orch.handle_user_utterance.return_value.metadata = {}

        msg_res = await async_client.post(
            f"/sessions/{session_id}/message", 
            json={"content": "Hello"}, 
            headers=token_headers
        )
        assert msg_res.status_code == 200, msg_res.text
        data = msg_res.json()
        assert data["session_id"] == session_id
        assert data["assistant_text"] == "I am ready"

@pytest.mark.asyncio
async def test_post_message_to_random_session(async_client: AsyncClient, token_headers, mock_db_session):
    random_id = str(uuid4())
    
    # Mock NOT finding the session
    query_mock = mock_db_session.query.return_value
    filter_mock = query_mock.filter.return_value
    filter_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = None # Not found

    response = await async_client.post(
        f"/sessions/{random_id}/message", 
        json={"content": "Hello"}, 
        headers=token_headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"
