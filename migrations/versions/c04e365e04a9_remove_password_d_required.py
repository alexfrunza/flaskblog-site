"""Remove password d required

Revision ID: c04e365e04a9
Revises: a6ce672fa94b
Create Date: 2020-09-09 10:57:26.421397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c04e365e04a9'
down_revision = 'a6ce672fa94b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###