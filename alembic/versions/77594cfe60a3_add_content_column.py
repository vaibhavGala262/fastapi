"""add content column

Revision ID: 77594cfe60a3
Revises: 6b25d11de5f4
Create Date: 2025-04-06 22:12:02.564768

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '77594cfe60a3'
down_revision: Union[str, None] = '6b25d11de5f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


#def upgrade() -> None:
#    """Upgrade schema."""
#    op.add_column('posts', sa.Column('content', sa.Text(), nullable=True))
#    pass


#def downgrade() -> None:
#    op.drop_column('posts' , 'content')
#    """Downgrade schema."""
#    pass


def upgrade():
    conn = op.get_bind()
    inspector = inspect(conn)

    # Check if 'content' column already exists
    columns = [col["name"] for col in inspector.get_columns("posts")]
    if "content" not in columns:
        op.add_column('posts', sa.Column('content', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('posts', 'content')