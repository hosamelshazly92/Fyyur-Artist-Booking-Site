"""empty message

Revision ID: 11df0df98ab2
Revises: 5bab534a4573
Create Date: 2020-07-22 01:35:24.238039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11df0df98ab2'
down_revision = '5bab534a4573'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('facebook_link', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('phone', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('seeking_talent', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('website', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'website')
    op.drop_column('venue', 'seeking_talent')
    op.drop_column('venue', 'phone')
    op.drop_column('venue', 'genres')
    op.drop_column('venue', 'facebook_link')
    # ### end Alembic commands ###