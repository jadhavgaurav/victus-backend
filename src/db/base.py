
import uuid

# We can reuse the existing Base from src.database if preferred,
# but if we want a clean break or to follow the prompt's `backend/app/db/base.py` structure:
# The prompt says "Reuse existing Base if already present".
# So we will import it from src.database instead of creating a new one unless needed.
# But we need a uuid_pk helper.

def uuid_pk() -> uuid.UUID:
    """Generates a random UUID4."""
    return uuid.uuid4()
