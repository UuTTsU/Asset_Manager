"""add default to created_at

Revision ID: ab16eb126292
Revises: 0da6e1fa7637
Create Date: 2026-11-17 07:27:41.444614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab16eb126292'
down_revision: Union[str, Sequence[str], None] = '0da6e1fa7637'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'created_at', server_default=sa.func.now())


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "users",
        "created_at",
        server_default=None,
    )
