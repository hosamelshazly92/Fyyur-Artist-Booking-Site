"""empty message

Revision ID: 78578a9d92ac
Revises: 191a03a80fa2
Create Date: 2020-07-21 04:43:45.446377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78578a9d92ac'
down_revision = '191a03a80fa2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('show', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    # ### end Alembic commands ###
