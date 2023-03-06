"""add the last few columns to posts table

Revision ID: f3694b56f193
Revises: d056b638749a
Create Date: 2023-03-06 11:00:57.510974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3694b56f193'
down_revision = 'd056b638749a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable = False, server_default = 'True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone = True), nullable = False, server_default = sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
