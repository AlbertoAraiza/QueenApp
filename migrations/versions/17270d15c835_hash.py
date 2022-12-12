"""hash

Revision ID: 17270d15c835
Revises: 2b34b88b0e5a
Create Date: 2022-11-11 10:58:53.053430

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '17270d15c835'
down_revision = '2b34b88b0e5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(table_name='client',
                    column_name='device_id',
                    new_column_name='device_hash',
                    existing_type = sa.Text)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(table_name='client',
                    column_name='device_hash',
                    new_column_name='device_id',
                    existing_type = sa.Text)
    # ### end Alembic commands ###