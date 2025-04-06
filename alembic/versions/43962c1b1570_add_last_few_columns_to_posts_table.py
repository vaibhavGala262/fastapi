"""add last few columns to posts table 

Revision ID: 43962c1b1570
Revises: 6be1945a0158
Create Date: 2025-04-06 23:33:19.177158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43962c1b1570'
down_revision: Union[str, None] = '6be1945a0158'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts' , sa.Column(
        'published' , sa.Boolean() , nullable=False , server_default='TRUE' 
    ),)
    op.add_column('posts' , sa.Column(
        'created_at' , sa.TIMESTAMP(timezone=True) , nullable=False ,server_default=sa.text('NOW()')
    ),)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts' , 'published')
    op.drop_column('posts' , 'created_at')
    pass
