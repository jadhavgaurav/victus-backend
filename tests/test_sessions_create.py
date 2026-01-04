
import pytest
from httpx import AsyncClient
from uuid import UUID

@pytest.mark.asyncio
async def test_create_session(async_client: AsyncClient, token_headers, mock_db_session):
    # Ensure the session object added to DB has an ID if refresh is called
    def side_effect_refresh(instance):
        if not instance.id:
             from uuid import uuid4
             instance.id = uuid4()
    
    mock_db_session.refresh.side_effect = side_effect_refresh

    response = await async_client.post("/sessions/", headers=token_headers)
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    try:
        UUID(data["session_id"])
    except ValueError:
        pytest.fail("Returned session_id is not a valid UUID")

@pytest.mark.asyncio
async def test_create_session_unauthenticated(async_client: AsyncClient, csrf_headers):
    response = await async_client.post("/sessions/", headers=csrf_headers)
    assert response.status_code == 401
