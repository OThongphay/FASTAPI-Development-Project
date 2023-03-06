"""create posts table

Revision ID: 3ce24f73bd09
Revises: 
Create Date: 2023-03-06 10:18:20.452941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ce24f73bd09'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable = False, primary_key = True), sa.Column('title', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
