"""init products and categories

Revision ID: bc1159e469b3
Revises: 
Create Date: 2025-12-24 00:14:22.947138

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc1159e469b3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
    )

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=False),
        sa.Column("image_url", sa.String(length=200), nullable=False),
        sa.Column("price_shmeckles", sa.Float(), nullable=False),
        sa.Column("price_flurbos", sa.Float(), nullable=False),
        sa.Column("price_credits", sa.Float(), nullable=False),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("categories.id"), nullable=False),
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("products")
    op.drop_table("categories")

