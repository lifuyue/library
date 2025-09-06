"""add_is_admin_column_and_seed_admin

Revision ID: 8d300e45b937
Revises: 
Create Date: 2025-08-22 02:05:43.785451

"""
from typing import Sequence, Union
from datetime import datetime
import os

from alembic import op
import sqlalchemy as sa
from passlib.context import CryptContext


# revision identifiers, used by Alembic.
revision: str = '8d300e45b937'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Base migration for PostgreSQL-only deployment
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = set(inspector.get_table_names())

    # Create users table if missing
    if 'users' not in existing_tables:
        op.create_table(
            'users',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('username', sa.String(50), nullable=False, unique=True, index=True),
            sa.Column('email', sa.String(100), nullable=False, unique=True, index=True),
            sa.Column('hashed_password', sa.String(255), nullable=False),
            sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column('is_admin', sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        )

    # Create materials table if missing
    if 'materials' not in existing_tables:
        op.create_table(
            'materials',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('title', sa.String(200), nullable=False, index=True),
            sa.Column('description', sa.Text()),
            sa.Column('category', sa.String(50), nullable=False),
            sa.Column('map_name', sa.String(50)),
            sa.Column('file_path', sa.String(500), nullable=False),
            sa.Column('file_type', sa.String(20), nullable=False),
            sa.Column('file_size', sa.Integer),
            sa.Column('thumbnail_path', sa.String(500)),
            sa.Column('tags', sa.Text()),
            sa.Column('views', sa.Integer, nullable=False, server_default=sa.text('0')),
            sa.Column('likes', sa.Integer, nullable=False, server_default=sa.text('0')),
            sa.Column('uploader_id', sa.Integer, nullable=True),
            sa.Column('is_approved', sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.ForeignKeyConstraint(['uploader_id'], ['users.id'], name='fk_materials_users', ondelete='SET NULL'),
        )

    # Ensure is_admin column exists on users
    try:
        user_columns = {c['name'] for c in inspector.get_columns('users')}
    except Exception:
        user_columns = set()
    if 'is_admin' not in user_columns and 'users' in existing_tables:
        op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default=sa.false()))

    # Seed default admin user if not present
    admin_username = os.getenv('ADMIN_DEFAULT_USERNAME', 'admin')
    admin_email = os.getenv('ADMIN_DEFAULT_EMAIL', 'admin@example.com')
    admin_password = os.getenv('ADMIN_DEFAULT_PASSWORD', 'admin123')

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(admin_password)

    conn.execute(
        sa.text(
            """
            INSERT INTO users (username, email, hashed_password, is_active, is_admin, created_at)
            SELECT
                CAST(:username AS VARCHAR(50)),
                CAST(:email AS VARCHAR(100)),
                :password,
                TRUE,
                TRUE,
                :created_at
            WHERE NOT EXISTS (
                SELECT 1 FROM users
                WHERE username = CAST(:username AS VARCHAR(50))
                   OR email = CAST(:email AS VARCHAR(100))
            )
            """
        ),
        {
            "username": admin_username,
            "email": admin_email,
            "password": hashed_password,
            "created_at": datetime.utcnow(),
        },
    )


def downgrade() -> None:
    # Conservative downgrade: drop is_admin if exists; leave tables intact
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    cols = {c['name'] for c in inspector.get_columns('users')} if 'users' in inspector.get_table_names() else set()
    if 'is_admin' in cols:
        op.drop_column('users', 'is_admin')
