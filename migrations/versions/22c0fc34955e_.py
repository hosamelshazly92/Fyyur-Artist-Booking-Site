"""empty message

Revision ID: 22c0fc34955e
Revises: 1f7cfdeef2ab
Create Date: 2020-07-23 19:06:57.014486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22c0fc34955e'
down_revision = '1f7cfdeef2ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('artist', sa.Column('seeking_talent', sa.String(length=120), nullable=True))
    op.drop_column('venue', 'seeking_talent')
    op.drop_column('venue', 'seeking_description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('seeking_description', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.add_column('venue', sa.Column('seeking_talent', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_column('artist', 'seeking_talent')
    op.drop_column('artist', 'seeking_description')
    # ### end Alembic commands ###