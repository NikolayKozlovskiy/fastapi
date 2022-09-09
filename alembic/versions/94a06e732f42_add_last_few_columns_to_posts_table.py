"""add last few columns to posts table

Revision ID: 94a06e732f42
Revises: f3928154d025
Create Date: 2022-09-09 23:34:54.463594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94a06e732f42'
down_revision = 'f3928154d025'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean, server_default="TRUE", nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
