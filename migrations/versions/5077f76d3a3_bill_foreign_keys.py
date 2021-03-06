"""bill foreign keys

Revision ID: 5077f76d3a3
Revises: 5a927336192f
Create Date: 2015-11-15 18:19:40.740280

"""

# revision identifiers, used by Alembic.
revision = '5077f76d3a3'
down_revision = '5a927336192f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'bills', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'bills', 'bill_types', ['type_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bills', type_='foreignkey')
    op.drop_constraint(None, 'bills', type_='foreignkey')
    ### end Alembic commands ###
