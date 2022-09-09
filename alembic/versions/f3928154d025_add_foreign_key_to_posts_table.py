"""add foreign key to posts table

Revision ID: f3928154d025
Revises: c3a49611025c
Create Date: 2022-09-09 23:27:11.248911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3928154d025'
down_revision = 'c3a49611025c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey',source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fkey','posts')
    op.drop_column('posts', 'owner_id')
    pass
