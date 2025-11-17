"""add ai chat tables

Revision ID: e007a264ef05
Revises: 9b22f910f2c6
Create Date: 2025-01-27 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e007a264ef05'
down_revision = '9b22f910f2c6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create query_logs table
    op.create_table(
        'query_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('query', sa.Text(), nullable=False),
        sa.Column('response', sa.Text(), nullable=False),
        sa.Column('operation_type', sa.String(length=50), nullable=True),
        sa.Column('conversation_id', sa.Integer(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_query_logs_user_id'), 'query_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_query_logs_conversation_id'), 'query_logs', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_query_logs_created_at'), 'query_logs', ['created_at'], unique=False)
    
    # Create thread_maps table
    op.create_table(
        'thread_maps',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('thread_id', sa.String(length=255), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_used_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('conversation_id'),
        sa.UniqueConstraint('thread_id')
    )
    op.create_index(op.f('ix_thread_maps_conversation_id'), 'thread_maps', ['conversation_id'], unique=True)
    op.create_index(op.f('ix_thread_maps_thread_id'), 'thread_maps', ['thread_id'], unique=True)
    op.create_index(op.f('ix_thread_maps_user_id'), 'thread_maps', ['user_id'], unique=False)
    
    # Add OpenAI fields to users table
    op.add_column('users', sa.Column('openai_assistant_id', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('openai_vector_store_id', sa.String(length=255), nullable=True))
    
    # Add conversation_id to chat_messages table
    op.add_column('chat_messages', sa.Column('conversation_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_chat_messages_conversation_id'), 'chat_messages', ['conversation_id'], unique=False)
    op.create_index('ix_chat_messages_user_conversation', 'chat_messages', ['user_id', 'conversation_id'], unique=False)


def downgrade() -> None:
    # Remove indexes
    op.drop_index('ix_chat_messages_user_conversation', table_name='chat_messages')
    op.drop_index(op.f('ix_chat_messages_conversation_id'), table_name='chat_messages')
    
    # Remove conversation_id from chat_messages
    op.drop_column('chat_messages', 'conversation_id')
    
    # Remove OpenAI fields from users
    op.drop_column('users', 'openai_vector_store_id')
    op.drop_column('users', 'openai_assistant_id')
    
    # Drop thread_maps table
    op.drop_index(op.f('ix_thread_maps_user_id'), table_name='thread_maps')
    op.drop_index(op.f('ix_thread_maps_thread_id'), table_name='thread_maps')
    op.drop_index(op.f('ix_thread_maps_conversation_id'), table_name='thread_maps')
    op.drop_table('thread_maps')
    
    # Drop query_logs table
    op.drop_index(op.f('ix_query_logs_created_at'), table_name='query_logs')
    op.drop_index(op.f('ix_query_logs_conversation_id'), table_name='query_logs')
    op.drop_index(op.f('ix_query_logs_user_id'), table_name='query_logs')
    op.drop_table('query_logs')

