"""create posts table

Revision ID: 5fc973b79941
Revises: 
Create Date: 2022-09-09 21:57:16.092508

"""
# comand: alembic revision -m  "create posts table"
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fc973b79941'
down_revision = None
branch_labels = None
depends_on = None

# alembic upgrade 5fc973b79941
def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True),sa.Column('title', sa.String, nullable=False))
    
    pass


def downgrade():
    op.drop_table('posts')
    pass
