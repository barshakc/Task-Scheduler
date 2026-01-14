"""Add next_run column to tasks table

Revision ID: add_next_run_to_tasks
Revises: <previous_revision_id>
Create Date: 2026-01-14 13:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_next_run_to_tasks'
down_revision = '43a68ecdb4c8'
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Add the column as nullable
    op.add_column('tasks', sa.Column('next_run', sa.DateTime(timezone=True), nullable=True))

    # Step 2: Backfill existing tasks with current UTC time
    op.execute("UPDATE tasks SET next_run = NOW() WHERE next_run IS NULL")

    # Step 3: Alter column to NOT NULL
    op.alter_column('tasks', 'next_run', nullable=False)


def downgrade():
    # Remove the column if rolling back
    op.drop_column('tasks', 'next_run')
