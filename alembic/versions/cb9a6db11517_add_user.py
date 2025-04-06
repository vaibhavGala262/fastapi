"""add user

Revision ID: cb9a6db11517
Revises: 77594cfe60a3
Create Date: 2025-04-06 22:28:43.717025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb9a6db11517'
down_revision: Union[str, None] = '77594cfe60a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users" , sa.Column('id' , sa.Integer() , nullable=False ) , sa.Column('email' , sa.String() , nullable=False) , 
                    sa.Column('password' , sa.String() , nullable=False) , sa.Column('created_at' , sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
                   sa.PrimaryKeyConstraint('id') , sa.UniqueConstraint('email') )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    
    pass
