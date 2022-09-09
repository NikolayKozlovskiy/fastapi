"""add user table

Revision ID: c3a49611025c
Revises: 4f02bf23ddbd
Create Date: 2022-09-09 22:58:14.979744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3a49611025c'
down_revision = '4f02bf23ddbd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False), 
                    sa.Column('email', sa.String(), nullable=False), 
                    sa.Column('password', sa.String(), nullable=False), 
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'), 
                    sa.UniqueConstraint('email'))

    pass


def downgrade():
    op.drop_table('users')
    pass
