"""init

Revision ID: 83cb7cc995a3
Revises:
Create Date: 2019-04-19 10:49:31.744443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83cb7cc995a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'guid_tracker',
        sa.Column('id', sa.String, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('expire', sa.DateTime, nullable=False),
    )


def downgrade():
    op.drop_table('guid_tracker')
