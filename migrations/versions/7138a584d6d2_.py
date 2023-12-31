"""empty message

Revision ID: 7138a584d6d2
Revises: 230a9177cdd1
Create Date: 2023-08-15 08:01:44.339803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7138a584d6d2'
down_revision = '230a9177cdd1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todo', 'admin')
    op.add_column('user', sa.Column('admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'admin')
    op.add_column('todo', sa.Column('admin', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
