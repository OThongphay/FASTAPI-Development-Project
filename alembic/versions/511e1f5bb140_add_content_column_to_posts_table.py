"""add content column to posts table

Revision ID: 511e1f5bb140
Revises: 3ce24f73bd09
Create Date: 2023-03-06 10:28:03.818105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '511e1f5bb140'
down_revision = '3ce24f73bd09'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
