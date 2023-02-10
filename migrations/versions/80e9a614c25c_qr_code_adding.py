"""qr code adding

Revision ID: 80e9a614c25c
Revises: ab5355746aa0
Create Date: 2023-01-27 16:37:11.691250

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '80e9a614c25c'
down_revision = 'ab5355746aa0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('job')
    op.drop_table('client')
    op.drop_table('ticket')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ticket',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('code', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('time', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('status', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('client',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('first_name', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('last_name', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('email', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('phone_number', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('device_hash', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('role_name', mysql.VARCHAR(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('job',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('client_name', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('phone_number', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('final_price', mysql.FLOAT(), nullable=True),
    sa.Column('payment', mysql.FLOAT(), nullable=True),
    sa.Column('description', mysql.VARCHAR(length=150), nullable=True),
    sa.Column('status', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('deliver_date', mysql.VARCHAR(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
