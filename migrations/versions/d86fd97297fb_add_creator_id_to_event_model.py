"""Add creator_id to Event model

Revision ID: d86fd97297fb
Revises: f98deb92114f
Create Date: 2025-01-22 09:51:05.910435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd86fd97297fb'
down_revision = 'f98deb92114f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('creator_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_event_creator', 'user', ['creator_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_constraint('fk_event_creator', type_='foreignkey')
        batch_op.drop_column('creator_id')

    # ### end Alembic commands ###
