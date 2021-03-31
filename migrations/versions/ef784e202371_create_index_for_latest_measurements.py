"""Create index for latest measurements

Revision ID: ef784e202371
Revises: 256a79be1bd8
Create Date: 2021-03-31 20:19:23.439480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef784e202371'
down_revision = '256a79be1bd8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('latest_by_node_id', 'measurement', ['nodeId', sa.text('timestamp DESC')])


def downgrade():
    op.drop_index('latest_by_node_id')
