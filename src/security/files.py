import os
import uuid
import magic
from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException

MAX_UPLOAD_SIZE = 10 * 1024 * 1024 # 10MB
ALLOWED_MIME_TYPES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "text/plain": ".txt",
    "text/markdown": ".md"
}

def scan_file(file_path: str) -> bool:
    """
    Hook for malware scanning.
    In MVP, just logging / allowed.
    Returns True if safe.
    """
    # Placeholder for ClamAV or similar
    return True

def validate_file_size(file: UploadFile) -> None:
    # Check Content-Length header if available
    # But strictly need to check read stream or spool.
    # FastAPI UploadFile is Spooled... so we can seek end?
    # Simple check:
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    
    if size > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

def validate_and_save_upload(file: UploadFile, upload_dir: str) -> Tuple[str, str, int]:
    """
    Validates file and saves it safely.
    Returns (stored_filename, original_filename, size).
    """
    validate_file_size(file)
    
    # MIME Sniffing
    header = file.file.read(2048)
    file.file.seek(0)
    mime = magic.from_buffer(header, mime=True)
    
    if mime not in ALLOWED_MIME_TYPES:
         # Fallback check extension matches allowed??
         # Prompt says "Reject double extensions", "Allowlist MIME types".
         raise HTTPException(status_code=400, detail=f"Invalid file type: {mime}")

    # Generate Safe Filename
    ext = ALLOWED_MIME_TYPES[mime]
    original_filename = os.path.basename(file.filename) # basic cleanup
    stored_filename = f"{uuid.uuid4()}{ext}"
    
    save_path = os.path.join(upload_dir, stored_filename)
    
    # Save
    with open(save_path, "wb") as f:
        while chunk := file.file.read(8192):
            f.write(chunk)
            
    # Scan
    if not scan_file(save_path):
        os.remove(save_path)
        raise HTTPException(status_code=400, detail="File failed security scan")

    size = os.path.getsize(save_path)
    return stored_filename, original_filename, size
