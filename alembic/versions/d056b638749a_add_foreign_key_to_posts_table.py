"""add foreign-key to posts table

Revision ID: d056b638749a
Revises: 90ca876ca534
Create Date: 2023-03-06 10:41:53.075953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd056b638749a'
down_revision = '90ca876ca534'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('post_user_fk', source_table = "posts", referent_table = "users", local_cols = ['owner_id'], remote_cols = ['id'], ondelete = "CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name = "posts")
    op.drop_column('posts', 'owner_id')
    pass