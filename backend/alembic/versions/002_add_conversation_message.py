"""Add conversation and message tables for AI chatbot

Revision ID: 002_add_conversation_message
Revises: 001_initial_setup
Create Date: 2026-03-27

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '002_add_conversation_message'
down_revision = '001_initial_setup'
branch_labels = None
depends_on = None


def upgrade():
    # Create conversation table
    op.create_table('conversation',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.current_timestamp()),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for conversation table
    op.create_index(op.f('ix_conversation_user_id'), 'conversation', ['user_id'])

    # Create message table
    op.create_table('message',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('conversation_id', UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.current_timestamp()),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("role IN ('user', 'assistant')", name='check_message_role')
    )

    # Create indexes for message table
    op.create_index(op.f('ix_message_conversation_id'), 'message', ['conversation_id'])
    op.create_index(op.f('ix_message_user_id'), 'message', ['user_id'])

    # Attach the update trigger to conversation table
    op.execute("""
        CREATE TRIGGER update_conversation_updated_at
        BEFORE UPDATE ON conversation
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade():
    # Drop trigger
    op.execute('DROP TRIGGER IF EXISTS update_conversation_updated_at ON conversation')

    # Drop indexes
    op.drop_index(op.f('ix_message_user_id'), table_name='message')
    op.drop_index(op.f('ix_message_conversation_id'), table_name='message')
    op.drop_index(op.f('ix_conversation_user_id'), table_name='conversation')

    # Drop tables
    op.drop_table('message')
    op.drop_table('conversation')
