"""Create Users and Credentials(View) tables

Revision ID: 0a5919b81056
Revises: 
Create Date: 2023-06-23 04:08:02.183297

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0a5919b81056"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "planner__users",
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("pronoun", sa.Enum("he", "she", name="pronouns"), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_planner__auth_credentials_username"), "planner__users", ["email"]
    )
    op.execute(
        """
        CREATE VIEW planner__auth_credentials AS
            SELECT planner__users.email as username, planner__users.password, planner__users.id as user_id
            FROM planner__users; 
        """
    )


def downgrade() -> None:
    op.execute("DROP VIEW planner__auth_credentials;")
    op.drop_index(
        op.f("ix_planner__auth_credentials_username"), table_name="planner__users"
    )
    op.drop_table("planner__users")
