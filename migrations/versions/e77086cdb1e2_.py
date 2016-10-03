"""empty message

Revision ID: e77086cdb1e2
Revises: 45ab1fea9b37
Create Date: 2016-10-03 23:19:01.676948

"""

# revision identifiers, used by Alembic.
revision = 'e77086cdb1e2'
down_revision = '45ab1fea9b37'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('event', 'school',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_constraint(None, 'event', type_='foreignkey')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'event', 'profile', ['school'], ['school'])
    op.alter_column('event', 'school',
               existing_type=sa.VARCHAR(),
               nullable=True)
    ### end Alembic commands ###
