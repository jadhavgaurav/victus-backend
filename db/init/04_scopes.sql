-- Add scopes column to users and sessions_override to sessions
ALTER TABLE users ADD COLUMN scopes JSONB DEFAULT '["core", "tool.web.search", "tool.system.rag", "tool.files.read"]'::jsonb;

ALTER TABLE sessions ADD COLUMN scopes_override JSONB DEFAULT NULL;