"""Alembic migration script for Todo application initial setup."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision = '001_initial_setup'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create user table
    op.create_table('user',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=255), nullable=True),
        sa.Column('last_name', sa.String(length=255), nullable=True),
        sa.Column('password_hash', sa.Text(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.current_timestamp()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Create indexes for user table
    op.create_index(op.f('ix_user_email'), 'user', ['email'])

    # Create task table
    op.create_table('task',
        sa.Column('id', UUID(as_uuid=True), nullable=False, default=sa.text("gen_random_uuid()")),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_completed', sa.Boolean(), nullable=True, default=False),
        sa.Column('due_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('priority', sa.String(length=20), nullable=True, default='medium'),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.current_timestamp()),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for task table
    op.create_index(op.f('ix_task_user_id'), 'task', ['user_id'])
    op.create_index(op.f('ix_task_is_completed'), 'task', ['is_completed'])
    op.create_index(op.f('ix_task_due_date'), 'task', ['due_date'])
    op.create_index(op.f('ix_task_priority'), 'task', ['priority'])

    # Create trigger function to update 'updated_at' column
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)

    # Attach the trigger to user table
    op.execute("""
        CREATE TRIGGER update_user_updated_at 
        BEFORE UPDATE ON "user" 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)

    # Attach the trigger to task table
    op.execute("""
        CREATE TRIGGER update_task_updated_at 
        BEFORE UPDATE ON task 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade():
    # Drop triggers
    op.execute("DROP TRIGGER IF EXISTS update_task_updated_at ON task;")
    op.execute("DROP TRIGGER IF EXISTS update_user_updated_at ON \"user\";")
    
    # Drop function
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column();")
    
    # Drop indexes for task table
    op.drop_index(op.f('ix_task_priority'), table_name='task')
    op.drop_index(op.f('ix_task_due_date'), table_name='task')
    op.drop_index(op.f('ix_task_is_completed'), table_name='task')
    op.drop_index(op.f('ix_task_user_id'), table_name='task')

    # Drop task table
    op.drop_table('task')

    # Drop indexes for user table
    op.drop_index(op.f('ix_user_email'), table_name='user')

    # Drop user table
    op.drop_table('user')