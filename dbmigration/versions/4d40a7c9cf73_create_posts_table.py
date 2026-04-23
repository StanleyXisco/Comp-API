"""create posts table

Revision ID: 4d40a7c9cf73
Revises: 75854aac7bfb
Create Date: 2026-04-22 18:07:50.495500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d40a7c9cf73'
down_revision: Union[str, Sequence[str], None] = '75854aac7bfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False))
    


def downgrade() -> None:
    """Downgrade schema. (rollback)"""
    op.drop_table('posts')
