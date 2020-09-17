"""h

Revision ID: 789cd0551468
Revises: 0a494b700de5
Create Date: 2020-09-09 14:38:04.902386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '789cd0551468'
down_revision = '0a494b700de5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_discord_id_key', 'user', type_='unique')
    op.drop_column('user', 'discord_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('discord_id', sa.BIGINT(), autoincrement=False, nullable=True))
    op.create_unique_constraint('user_discord_id_key', 'user', ['discord_id'])
    # ### end Alembic commands ###