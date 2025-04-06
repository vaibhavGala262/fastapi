"""create post table

Revision ID: 6b25d11de5f4
Revises: 
Create Date: 2025-04-06 22:00:02.839726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b25d11de5f4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts' , sa.Column('id', sa.Integer(), nullable=False, primary_key=True) 
                    , sa.Column('title', sa.String(), nullable=False) , sa.Column('content', sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
