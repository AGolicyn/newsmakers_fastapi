"""constraint

Revision ID: 71da5f17a107
Revises: 5421acf78d8b
Create Date: 2023-03-14 16:35:43.952524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71da5f17a107'
down_revision = '5421acf78d8b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index('data_title_date_unique_1',
                    'news_title',
                    [sa.text("((data->>'title')::text)"),
                     sa.text("(substring((data->>'time')::text, 1, 10))")],
                    unique=True)

    op.create_index('data_href_date_unique_1',
                    'news_title',
                    [sa.text("((data->>'href')::text)"),
                     sa.text("(substring((data->>'time')::text, 1, 10))")],
                    unique=True)


def downgrade() -> None:
    op.drop_index(op.f('data_href_date_unique_1'), table_name='news_title')
    op.drop_index(op.f('data_title_date_unique_1'), table_name='news_title')
