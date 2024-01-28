"""Create Accounts

Revision ID: 07ad4f4c1efb
Revises: 0a5919b81056
Create Date: 2024-01-28 02:25:42.261307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07ad4f4c1efb'
down_revision = '0a5919b81056'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('accounts',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('currency', sa.String(length=5), nullable=False),
        sa.Column('balance', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accounts_name_per_user'), 'accounts', ['name', 'user_id'], unique=True)


def downgrade() -> None:
    op.drop_table('accounts')
    op.drop_index(op.f('ix_accounts_name_per_user'), table_name='accounts')
