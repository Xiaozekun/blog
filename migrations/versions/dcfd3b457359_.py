"""empty message

Revision ID: dcfd3b457359
Revises: ed70f5166518
Create Date: 2019-02-01 09:33:02.236323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcfd3b457359'
down_revision = 'ed70f5166518'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('can_comment', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'can_comment')
    # ### end Alembic commands ###
