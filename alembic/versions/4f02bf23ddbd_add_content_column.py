"""add content column

Revision ID: 4f02bf23ddbd
Revises: 5fc973b79941
Create Date: 2022-09-09 22:50:50.529654

"""
from tokenize import String
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f02bf23ddbd'
down_revision = '5fc973b79941'
branch_labels = None
depends_on = None

# alembic upgrade head
def upgrade():
    op.add_column('posts', sa.Column("content", sa.String(), nullable=False))
    pass

# alembic downgrade -1 (one step backwards)
#  OR alembic downgrade <down_revision>
def downgrade():
    op.drop_column('posts', 'content')
    pass
