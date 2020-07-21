"""empty message

Revision ID: d4e4ce5fec84
Revises: 285e8758b264
Create Date: 2020-07-21 23:29:40.708222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4e4ce5fec84'
down_revision = '285e8758b264'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'seeking_venue')
    # ### end Alembic commands ###
