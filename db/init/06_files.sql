CREATE TABLE files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
    user_id UUID NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    session_id UUID,
    original_name VARCHAR NOT NULL,
    stored_name VARCHAR NOT NULL UNIQUE,
    mime_type VARCHAR NOT NULL,
    size_bytes INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ
);

CREATE INDEX ix_files_user_id ON files (user_id);