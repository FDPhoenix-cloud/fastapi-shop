"""Add image_url to products

Revision ID: 92314abced7f
Revises: bc1159e469b3
Create Date: 2025-12-27 19:50:44.780380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '92314abced7f'
down_revision: Union[str, Sequence[str], None] = 'bc1159e469b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column("image_url", sa.String(length=500), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("products", "image_url")

