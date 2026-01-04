"""add_user_settings_and_scopes

Revision ID: a2c3ba5a6b8f
Revises: 0b34eb58d39a
Create Date: 2026-01-03 10:11:04.637267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a2c3ba5a6b8f'
down_revision: Union[str, None] = '0b34eb58d39a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Manually added columns
    op.add_column('users', sa.Column('settings', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'settings')
    op.drop_column('users', 'scopes')
