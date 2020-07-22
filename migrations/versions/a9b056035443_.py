"""empty message

Revision ID: a9b056035443
Revises: 128bd32b97a4
Create Date: 2020-07-22 14:22:56.473806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9b056035443'
down_revision = '128bd32b97a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('city', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('state', sa.String(length=120), nullable=True))
    op.drop_column('venue', 'area_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('area_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('venue', 'state')
    op.drop_column('venue', 'city')
    # ### end Alembic commands ###
