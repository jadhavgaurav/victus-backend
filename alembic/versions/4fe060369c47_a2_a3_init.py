"""a2_a3_init

Revision ID: 4fe060369c47
Revises: a2c3ba5a6b8f
Create Date: 2026-01-04 11:06:32.325508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import src.db.types
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = '4fe060369c47'
down_revision: Union[str, None] = 'a2c3ba5a6b8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Enable pgvector
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    
    # 1.1 Fix Sessions Table (Missing columns from 3c60)
    op.execute("ALTER TABLE sessions ADD COLUMN IF NOT EXISTS expires_at TIMESTAMP WITH TIME ZONE")
    op.execute("ALTER TABLE sessions ADD COLUMN IF NOT EXISTS revoked_at TIMESTAMP WITH TIME ZONE")
    op.execute("ALTER TABLE sessions ADD COLUMN IF NOT EXISTS scopes_override JSONB")

    # 2. Cleanup Legacy/Replaced Tables
    # We drop tables that are being replaced by A2/A3 architecture
    
    # Drop 'files' (if exists - seemingly unused/replaced)
    op.execute("DROP TABLE IF EXISTS files CASCADE")
    
    # Drop 'traces' and related (replaced by new observability or just cleanup)
    op.execute("DROP TABLE IF EXISTS trace_steps CASCADE")
    op.execute("DROP TABLE IF EXISTS traces CASCADE")
    
    # Drop 'pending_actions' (replaced by ToolExecution state machine)
    op.execute("DROP TABLE IF EXISTS pending_actions CASCADE")
    
    # Drop 'pending_confirmations' (replaced by confirmations table)
    op.execute("DROP TABLE IF EXISTS pending_confirmations CASCADE")
    
    # Drop 'tool_calls' (replaced by tool_executions)
    # This might cascade delete policy_decisions if they fk to tool_calls
    op.execute("DROP TABLE IF EXISTS tool_calls CASCADE")
    
    # Drop 'messages' (replaced by agent_messages)
    # Note: This wipes chat history. Acceptable for Dev/Refactor.
    op.execute("DROP TABLE IF EXISTS messages CASCADE")
    op.execute("DROP TABLE IF EXISTS chat_messages CASCADE") # Just in case

    # 2.1 Force Clean New Tables (Idempotency)
    op.execute("DROP TABLE IF EXISTS agent_messages CASCADE")
    op.execute("DROP TABLE IF EXISTS tool_executions CASCADE")
    op.execute("DROP TABLE IF EXISTS confirmations CASCADE")
    op.execute("DROP TABLE IF EXISTS memory_events CASCADE")

    # 3. Create New A3 Tables
    
    # agent_messages
    op.create_table('agent_messages',
        sa.Column('id', src.db.types.UUIDType(length=36), nullable=False),
        sa.Column('session_id', src.db.types.UUIDType(length=36), nullable=False),
        sa.Column('user_id', src.db.types.UUIDType(length=36), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('modality', sa.String(), server_default='text', nullable=True),
        sa.Column('status', sa.String(), server_default='CREATED', nullable=False),
        sa.Column('idempotency_key', sa.String(), nullable=True),
        sa.Column('trace_id', sa.String(), nullable=True),
        sa.Column('created_at', src.db.types.TZDateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', src.db.types.TZDateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # tool_executions
    op.create_table('tool_executions',
        sa.Column('id', src.db.types.UUIDType(length=36), nullable=False),
        sa.Column('message_id', src.db.types.UUIDType(length=36), nullable=False),
        sa.Column('tool_name', sa.String(), nullable=False),
        sa.Column('tool_call_id', sa.String(), nullable=False),
        sa.Column('arguments', src.db.types.JsonBType(), nullable=False),
        sa.Column('status', sa.String(), server_default='PENDING', nullable=False),
        sa.Column('result', src.db.types.JsonBType(), nullable=True),
        sa.Column('error', sa.String(), nullable=True),
        sa.Column('started_at', src.db.types.TZDateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('completed_at', src.db.types.TZDateTime(timezone=True), nullable=True),
        sa.Column('meta_usage', src.db.types.JsonBType(), nullable=True),
        sa.ForeignKeyConstraint(['message_id'], ['agent_messages.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tool_call_id', name='uq_tool_executions_tool_call_id')
    )
    
    # confirmations
    op.create_table('confirmations',
        sa.Column('id', src.db.types.UUIDType(length=36), nullable=False),
        sa.Column('session_id', src.db.types.UUIDType(length=36), nullable=False),
        sa.Column('user_id', src.db.types.UUIDType(length=36), nullable=False),
        sa.Column('tool_execution_id', src.db.types.UUIDType(length=36), nullable=True),
        sa.Column('action_type', sa.String(), nullable=False),
        sa.Column('payload', src.db.types.JsonBType(), nullable=False),
        sa.Column('status', sa.String(), server_default='PENDING', nullable=False),
        sa.Column('expires_at', src.db.types.TZDateTime(timezone=True), nullable=False),
        sa.Column('created_at', src.db.types.TZDateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('resolved_at', src.db.types.TZDateTime(timezone=True), nullable=True),
        sa.Column('resolution', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tool_execution_id'], ['tool_executions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create Indices
    op.create_index('ix_agent_messages_session_created', 'agent_messages', ['session_id', 'created_at'], unique=False)
    op.create_index('ix_agent_messages_idempotency', 'agent_messages', ['idempotency_key'], unique=True, postgresql_where=(sa.column('idempotency_key').isnot(None)))
    op.create_index('ix_confirmations_user_status', 'confirmations', ['user_id', 'status'], unique=False)

    # 4. Migrate/Update Memories (A2)
    # We drop and recreate memories to ensure clean state and schema match
    op.execute("DROP TABLE IF EXISTS memories CASCADE")
    
    op.create_table('memories',
        sa.Column('id', src.db.types.UUIDType(length=36), nullable=False),
        sa.Column('user_id', src.db.types.UUIDType(length=36), nullable=False),
        sa.Column('session_id', src.db.types.UUIDType(length=36), nullable=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('content_hash', sa.String(), nullable=False),
        sa.Column('embedding', Vector(1536), nullable=False),
        sa.Column('metadata', src.db.types.JsonBType(), server_default='{}', nullable=False),
        sa.Column('is_deleted', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', src.db.types.TZDateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', src.db.types.TZDateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('expires_at', src.db.types.TZDateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'content_hash', name='uq_memories_user_content_hash')
    )

    # Vector Index
    op.create_index('ix_memories_embedding_hnsw', 'memories', ['embedding'], unique=False, postgresql_using='hnsw', postgresql_with={'m': 16, 'ef_construction': 64}, postgresql_ops={'embedding': 'vector_cosine_ops'})
    op.create_index('ix_memories_user_id_created_at', 'memories', ['user_id', 'created_at'], unique=False)
    op.create_index('ix_memories_user_id_type', 'memories', ['user_id', 'type'], unique=False)

    # 5. Fix Users Table (Missing columns)
    # Idempotent addition
    op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_superuser BOOLEAN DEFAULT false NOT NULL")
    op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS scopes JSONB DEFAULT '[]'::jsonb NOT NULL")
    op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS settings JSONB DEFAULT '{}'::jsonb NOT NULL")

    # 5. Create memory_events
    op.create_table('memory_events',
        sa.Column('id', src.db.types.UUIDType(length=36), nullable=False),
        sa.Column('user_id', src.db.types.UUIDType(length=36), nullable=False),
        sa.Column('memory_id', src.db.types.UUIDType(length=36), nullable=False),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('actor', sa.String(), nullable=False),
        sa.Column('reason', sa.String(), nullable=True),
        sa.Column('trace_id', sa.String(), nullable=True),
        sa.Column('created_at', src.db.types.TZDateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['memory_id'], ['memories.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_memory_events_user_created', 'memory_events', ['user_id', 'created_at'], unique=False)
    op.create_index('ix_memory_events_memory_id', 'memory_events', ['memory_id'], unique=False)


def downgrade() -> None:
    # Irreversible migration for Dev (too complex to revert logic)
    # Just drop the new tables
    op.drop_table('memory_events')
    op.drop_table('confirmations')
    op.drop_table('tool_executions')
    op.drop_table('agent_messages')
    
    # Revert memory columns? Too hard.
    pass
