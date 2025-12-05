"""Add is_admin field to users

Revision ID: f1e2d673d554
Revises: f908531100da
Create Date: 2025-12-04 13:12:08.601818

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1e2d673d554'
down_revision: Union[str, Sequence[str], None] = 'f908531100da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add column as nullable first
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))
    
    # Set default value for existing users
    op.execute("UPDATE users SET is_admin = false WHERE is_admin IS NULL")
    
    # Now make it NOT NULL
    op.alter_column('users', 'is_admin', nullable=False)


def downgrade() -> None:
    op.drop_column('users', 'is_admin')
