"""Add discord_id t to user

Revision ID: 0a494b700de5
Revises: c04e365e04a9
Create Date: 2020-09-09 12:08:37.995809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a494b700de5'
down_revision = 'c04e365e04a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('discord_id', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'user', ['discord_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'discord_id')
    # ### end Alembic commands ###
