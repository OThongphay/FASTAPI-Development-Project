"""add user table

Revision ID: 90ca876ca534
Revises: 511e1f5bb140
Create Date: 2023-03-06 10:33:48.561028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90ca876ca534'
down_revision = '511e1f5bb140'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('email', sa.String(), nullable = False),
                    sa.Column('password', sa.String(), nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone = True), server_default = sa.text('now()'), nullable = False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
