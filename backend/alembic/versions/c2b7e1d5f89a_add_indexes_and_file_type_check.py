"""add indexes and file_type constraint

Revision ID: c2b7e1d5f89a
Revises: 8d300e45b937
Create Date: 2024-06-07 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'c2b7e1d5f89a'
down_revision = '8d300e45b937'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    op.create_index('ix_materials_category', 'materials', ['category'], unique=False)
    op.create_index('ix_materials_map_name', 'materials', ['map_name'], unique=False)
    op.create_index('ix_materials_created_at', 'materials', ['created_at'], unique=False)
    op.create_index('ix_materials_title', 'materials', ['title'], unique=False)
    op.create_check_constraint('ck_materials_file_type', 'materials', "file_type IN ('image','video','gif')")

def downgrade() -> None:
    op.drop_constraint('ck_materials_file_type', 'materials', type_='check')
    op.drop_index('ix_materials_title', table_name='materials')
    op.drop_index('ix_materials_created_at', table_name='materials')
    op.drop_index('ix_materials_map_name', table_name='materials')
    op.drop_index('ix_materials_category', table_name='materials')
    op.drop_index('ix_users_email', table_name='users')
