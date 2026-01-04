import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.main import app
from src.security.scopes import Scope, ScopeSet
from src.security.network import is_safe_url
from src.security.crypto import encrypt_json, decrypt_json
from src.security.files import validate_and_save_upload
from src.models import User
from src.database import get_db

client = TestClient(app)

# --- 1. Scopes Tests ---
def test_scope_set_logic():
    scopes = ScopeSet({Scope.USER_READ, Scope.CHAT})
    assert scopes.has(Scope.USER_READ)
    assert scopes.has(Scope.CHAT)
    assert not scopes.has(Scope.ADMIN_ALL)
    
    # Test all
    assert scopes.has_all({Scope.USER_READ, Scope.CHAT})
    assert not scopes.has_all({Scope.USER_READ, Scope.ADMIN_ALL})

# --- 2. Encryption Tests ---
def test_encryption_roundtrip():
    data = {"secret": "key", "value": 123}
    encrypted = encrypt_json(data)
    assert encrypted != data
    decrypted = decrypt_json(encrypted)
    assert decrypted == data

# --- 3. Network / SSRF Tests ---
def test_ssrf_protection():
    # Safe public URL
    # assert is_safe_url("https://google.com") # Depends on network, might be flaky if offline. Skip if strictly offline.
    # We can mock socket.gethostbyname but logic is complex.
    # Let's test blocked IPs if we mock resolution.
    
    with patch("socket.gethostbyname", return_value="127.0.0.1"):
        assert is_safe_url("http://localhost") is False
        assert is_safe_url("http://127.0.0.1") is False
        assert is_safe_url("http://google.com") is False # because we mocked it to 127.0.0.1
        
    with patch("socket.gethostbyname", return_value="192.168.1.5"):
        assert is_safe_url("http://internal-service") is False
        
    with patch("socket.gethostbyname", return_value="8.8.8.8"):
        assert is_safe_url("http://google.com") is True

# --- 4. CSRF Tests ---
def test_csrf_enforcement():
    # POST without token should fail (if not authenticated? or globally?)
    # Our middleware skips SAFE methods.
    # For Unsafe methods, it checks cookie vs header.
    
    # Needs a route. Let's hit /api/health (POST allowed? No usually GET).
    # Hit /api/auth/login
    
    response = client.post("/api/auth/login", json={"email": "a", "password": "b"})
    # Should get 403 CSRF missing
    assert response.status_code == 403
    assert "CSRF token missing" in response.json()["detail"]
    
    # With mismatch
    client.cookies.set("csrf_token", "abc")
    response = client.post("/api/auth/login", json={"email": "a", "password": "b"}, headers={"x-csrf-token": "xyz"})
    assert response.status_code == 403
    assert "CSRF token mismatch" in response.json()["detail"]

# --- 5. File Safety Tests ---
# Mock file uploads is tricky with TestClient/FastAPI structure sometimes.
# We can test validation logic directly.

@patch("src.security.files.scan_file")
def test_file_validation_rejects_bad_mime(mock_scan):
    # Mock UploadFile
    mock_file = MagicMock()
    mock_file.filename = "malicious.exe"
    mock_file.file.read.side_effect = [b"MZ\x90\x00", b""] # EXE signature
    mock_file.file.tell.return_value = 100
    
    from src.security.files import validate_and_save_upload, HTTPException
    
    try:
        validate_and_save_upload(mock_file, "/tmp")
        assert False, "Should have raised exception"
    except HTTPException as e:
        assert IsBadMime(e)

def IsBadMime(e):
    return e.status_code == 400 and "Invalid file type" in e.detail

# --- 6. Rate Limit Tests ---
# Requires firing multiple requests.
# Might be slow.
# We skip for unit test speed, rely on manual verification or integration test.
