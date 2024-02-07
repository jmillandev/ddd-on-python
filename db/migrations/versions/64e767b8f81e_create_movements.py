"""Create Movements

Revision ID: 64e767b8f81e
Revises: 07ad4f4c1efb
Create Date: 2024-01-30 03:07:22.236663

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "64e767b8f81e"
down_revision = "07ad4f4c1efb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "movements__accounts",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("account_id", sa.UUID(), nullable=False),
        sa.Column("amount", sa.BigInteger(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["planner__accounts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("movements__accounts")
