
import uuid
from sqlalchemy.types import TypeDecorator, CHAR, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import JSON, DateTime

class UUIDType(TypeDecorator):
    """Platform-independent UUID type.
    
    Uses PostgreSQL's UUID type for Postgres, and CHAR(36) for others (SQLite).
    """
    impl = CHAR(36)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID(as_uuid=True))
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if dialect.name == "postgresql":
            return str(value)
        if not isinstance(value, uuid.UUID):
            return str(value)
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        return value

class TZDateTime(TypeDecorator):
    """Timezone-aware DateTime.
    
    Ensures that timestamps are stored with timezone information (UTC).
    """
    impl = TIMESTAMP(timezone=True)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(TIMESTAMP(timezone=True))
        return dialect.type_descriptor(DateTime(timezone=True))

class JsonBType(TypeDecorator):
    """Platform-independent JSON type.
    
    Uses JSONB for Postgres, JSON for others.
    """
    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB)
        return dialect.type_descriptor(JSON)
