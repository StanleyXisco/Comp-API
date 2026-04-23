"""add content column to post

Revision ID: 412650e14bbf
Revises: 4d40a7c9cf73
Create Date: 2026-04-22 18:25:37.506690

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '412650e14bbf'
down_revision: Union[str, Sequence[str], None] = '4d40a7c9cf73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
