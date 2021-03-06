"""init

Revision ID: 2aa17e8da0e4
Revises: 
Create Date: 2021-02-03 23:45:01.549826

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '2aa17e8da0e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
                    sa.Column('update_at', sa.TIMESTAMP(), nullable=False),
                    sa.Column('message', sa.VARCHAR(length=255), nullable=False),
                    sa.Column('sender_id', sa.Integer(), nullable=False),
                    sa.Column('recipient_id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
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
    op.drop_table('message')
    # ### end Alembic commands ###
