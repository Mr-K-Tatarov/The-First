"""add users

Revision ID: 845c8232416e
Revises: 
Create Date: 2021-02-03 00:29:10.753111

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '845c8232416e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('login', sa.VARCHAR(length=20), nullable=False),
    sa.Column('password', sa.VARBINARY(), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('is_delete', sa.BOOLEAN(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('login')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###