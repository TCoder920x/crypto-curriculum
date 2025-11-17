"""add_documents_table

Revision ID: b6682b59c3a1
Revises: e007a264ef05
Create Date: 2025-11-17 16:32:34.273662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6682b59c3a1'
down_revision = 'e007a264ef05'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create documents table
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('storage_path', sa.Text(), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=False, server_default='user-upload'),
        sa.Column('module_id', sa.Integer(), nullable=True),
        sa.Column('course_scope', sa.String(length=100), nullable=True),
        sa.Column('uploader_id', sa.Integer(), nullable=True),
        sa.Column('openai_file_id', sa.String(length=255), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['uploader_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_id'), 'documents', ['id'], unique=False)
    op.create_index(op.f('ix_documents_category'), 'documents', ['category'], unique=False)
    op.create_index(op.f('ix_documents_module_id'), 'documents', ['module_id'], unique=False)
    op.create_index(op.f('ix_documents_uploader_id'), 'documents', ['uploader_id'], unique=False)
    op.create_index(op.f('ix_documents_is_deleted'), 'documents', ['is_deleted'], unique=False)
    op.create_index(op.f('ix_documents_created_at'), 'documents', ['created_at'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_documents_created_at'), table_name='documents')
    op.drop_index(op.f('ix_documents_is_deleted'), table_name='documents')
    op.drop_index(op.f('ix_documents_uploader_id'), table_name='documents')
    op.drop_index(op.f('ix_documents_module_id'), table_name='documents')
    op.drop_index(op.f('ix_documents_category'), table_name='documents')
    op.drop_index(op.f('ix_documents_id'), table_name='documents')
    
    # Drop table
    op.drop_table('documents')


