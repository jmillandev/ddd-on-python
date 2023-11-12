"""Create Users and Accounts

Revision ID: 0a5919b81056
Revises: 
Create Date: 2023-06-23 04:08:02.183297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a5919b81056'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('currencies',
    sa.Column('code', sa.String(length=5), nullable=False),
    sa.Column('description', sa.String(length=50), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_currencies_code'), 'currencies', ['code'], unique=True)
    op.create_index(op.f('ix_currencies_id'), 'currencies', ['id'], unique=False)
    op.create_index(op.f('ix_currencies_public_id'), 'currencies', ['public_id'], unique=True)

    op.create_table('users',
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.UUID(), nullable=False),
    sa.Column('pronoun', sa.Enum('he', 'she', name='pronouns'), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_public_id'), 'users', ['public_id'], unique=True)

    op.create_table('accounts',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.Column('balance', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accounts_id'), 'accounts', ['id'], unique=False)
    op.create_index(op.f('ix_accounts_public_id'), 'accounts', ['public_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_accounts_public_id'), table_name='accounts')
    op.drop_index(op.f('ix_accounts_id'), table_name='accounts')
    op.drop_table('accounts')
    op.drop_index(op.f('ix_users_public_id'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_currencies_public_id'), table_name='currencies')
    op.drop_index(op.f('ix_currencies_id'), table_name='currencies')
    op.drop_index(op.f('ix_currencies_code'), table_name='currencies')
    op.drop_table('currencies')
