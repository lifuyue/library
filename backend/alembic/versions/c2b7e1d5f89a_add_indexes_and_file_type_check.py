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
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    existing_tables = set(inspector.get_table_names())

    # users.email index — skip if any index or unique constraint already covers email
    if 'users' in existing_tables:
        user_indexes = inspector.get_indexes('users')
        user_uniques = inspector.get_unique_constraints('users')
        has_email_idx = any('email' in (idx.get('column_names') or []) for idx in user_indexes)
        has_email_unique = any('email' in (uc.get('column_names') or []) for uc in user_uniques)
        if not (has_email_idx or has_email_unique):
            op.create_index('ix_users_email', 'users', ['email'], unique=False)

    # materials indexes
    if 'materials' in existing_tables:
        existing_material_indexes_detail = inspector.get_indexes('materials')
        for name, cols in [
            ('ix_materials_category', ['category']),
            ('ix_materials_map_name', ['map_name']),
            ('ix_materials_created_at', ['created_at']),
            ('ix_materials_title', ['title']),
        ]:
            has_same_cols = any(set(cols) == set((idx.get('column_names') or [])) for idx in existing_material_indexes_detail)
            if not has_same_cols:
                op.create_index(name, 'materials', cols, unique=False)

        # materials file_type check constraint
        existing_checks = {ck['name'] for ck in inspector.get_check_constraints('materials')}
        if 'ck_materials_file_type' not in existing_checks:
            op.create_check_constraint('ck_materials_file_type', 'materials', "file_type IN ('image','video','gif')")

def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    existing_tables = set(inspector.get_table_names())

    if 'materials' in existing_tables:
        existing_checks = {ck['name'] for ck in inspector.get_check_constraints('materials')}
        if 'ck_materials_file_type' in existing_checks:
            op.drop_constraint('ck_materials_file_type', 'materials', type_='check')

        existing_material_indexes = {idx['name'] for idx in inspector.get_indexes('materials')}
        for name in ['ix_materials_title', 'ix_materials_created_at', 'ix_materials_map_name', 'ix_materials_category']:
            if name in existing_material_indexes:
                op.drop_index(name, table_name='materials')

    if 'users' in existing_tables:
        existing_user_indexes = {idx['name'] for idx in inspector.get_indexes('users')}
        if 'ix_users_email' in existing_user_indexes:
            op.drop_index('ix_users_email', table_name='users')
