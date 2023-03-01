"""remove 2 columns

Revision ID: dd8659d523b9
Revises: e7369893e040
Create Date: 2023-02-25 18:14:49.729399

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'dd8659d523b9'
down_revision = 'e7369893e040'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
