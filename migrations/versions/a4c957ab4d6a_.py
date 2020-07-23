"""empty message

Revision ID: a4c957ab4d6a
Revises: 22c0fc34955e
Create Date: 2020-07-23 19:19:38.685259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4c957ab4d6a'
down_revision = '22c0fc34955e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'seeking_talent')
    op.add_column('venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'seeking_talent')
    op.add_column('artist', sa.Column('seeking_talent', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###