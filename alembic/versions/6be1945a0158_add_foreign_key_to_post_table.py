"""add foreign key to post table

Revision ID: 6be1945a0158
Revises: cb9a6db11517
Create Date: 2025-04-06 23:00:02.858530

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6be1945a0158'
down_revision: Union[str, None] = 'cb9a6db11517'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts" , sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',local_cols=['owner_id'],remote_cols=['id'], ondelete='CASCADE')




    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts' , 'owner_id')
    pass
