import os
import base64
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Get key from env
# Format: Base64 string of 32 bytes for AES-GCM or Fernet key
KEY_B64 = os.getenv("VICTUS_DATA_KEY")

def _get_key_bytes() -> bytes:
    if not KEY_B64:
        raise ValueError("VICTUS_DATA_KEY not set")
    try:
        return base64.b64decode(KEY_B64)
    except Exception as e:
        raise ValueError(f"Invalid VICTUS_DATA_KEY: {e}")

def encrypt_json(data: dict) -> dict:
    """
    Encrypts a dictionary to a stored format.
    Using Fernet for simplicity and authenticated encryption (AES-128-CBC + HMAC).
    Or AES-GCM (modern standard). 
    Let's use Fernet as it produces URL-safe strings and handles IV/Auth internally.
    But for 'field-level' JSONB storage, we might want to store { "ct": "...", "alg": "fernet" }.
    """
    key = _get_key_bytes()
    f = Fernet(key)
    
    payload_str = json.dumps(data)
    token = f.encrypt(payload_str.encode('utf-8'))
    
    return {
        "v": 1,
        "alg": "fernet",
        "ct": token.decode('utf-8')
    }

def decrypt_json(stored: dict) -> dict:
    """
    Decrypts the stored format back to a dictionary.
    """
    if not stored or "ct" not in stored:
        raise ValueError("Invalid encrypted payload format")
        
    key = _get_key_bytes()
    f = Fernet(key)
    
    ct = stored["ct"]
    try:
        decrypted_bytes = f.decrypt(ct.encode('utf-8'))
        return json.loads(decrypted_bytes.decode('utf-8'))
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")

def encrypt_str(value: str) -> str:
    """Simple string encryption returning b64 string."""
    key = _get_key_bytes()
    f = Fernet(key)
    return f.encrypt(value.encode('utf-8')).decode('utf-8')

def decrypt_str(token: str) -> str:
    key = _get_key_bytes()
    f = Fernet(key)
    return f.decrypt(token.encode('utf-8')).decode('utf-8')
