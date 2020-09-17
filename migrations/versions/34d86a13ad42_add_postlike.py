"""Add PostLike

Revision ID: 34d86a13ad42
Revises: 0e3d89590cb8
Create Date: 2020-09-06 17:18:56.216860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34d86a13ad42'
down_revision = '0e3d89590cb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_like')
    # ### end Alembic commands ###