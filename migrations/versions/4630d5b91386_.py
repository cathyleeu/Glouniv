"""empty message

Revision ID: 4630d5b91386
Revises: 196d53a821a4
Create Date: 2014-09-25 15:48:37.638000

"""

# revision identifiers, used by Alembic.
revision = '4630d5b91386'
down_revision = '196d53a821a4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('i_univ', sa.Column('univ_name', sa.String(length=255), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('i_univ', 'univ_name')
    ### end Alembic commands ###
