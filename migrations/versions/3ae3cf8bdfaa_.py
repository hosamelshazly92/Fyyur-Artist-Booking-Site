"""empty message

Revision ID: 3ae3cf8bdfaa
Revises: 6f2994f8eeaf
Create Date: 2020-07-24 02:53:51.594040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ae3cf8bdfaa'
down_revision = '6f2994f8eeaf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('show_start_time_key', 'show', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('show_start_time_key', 'show', ['start_time'])
    # ### end Alembic commands ###
