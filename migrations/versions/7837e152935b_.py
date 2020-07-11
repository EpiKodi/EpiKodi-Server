"""empty message

Revision ID: 7837e152935b
Revises: 
Create Date: 2020-07-11 22:16:03.208883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7837e152935b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('files',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Text(), nullable=True),
    sa.Column('filename', sa.Text(), nullable=False),
    sa.Column('user', sa.Text(), nullable=False),
    sa.Column('extension', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('friends',
    sa.Column('user_id_1', sa.Text(), nullable=True),
    sa.Column('user_id_2', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id_1'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id_2'], ['users.id'], )
    )
    op.create_table('pending_friends',
    sa.Column('user_id_1', sa.Text(), nullable=True),
    sa.Column('user_id_2', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id_1'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id_2'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pending_friends')
    op.drop_table('friends')
    op.drop_table('files')
    op.drop_table('users')
    # ### end Alembic commands ###
