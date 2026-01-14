"""fix task_runs fk cascade

Revision ID: abc123def456
Revises: <previous_revision_id>
Create Date: 2026-01-13 21:40:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'abc123def456'
down_revision = '07b76d7b297b'
branch_labels = None
depends_on = None


def upgrade():
    # Drop the old foreign key constraint
    op.drop_constraint('task_runs_task_id_fkey', 'task_runs', type_='foreignkey')
    
    # Create new foreign key with ON DELETE CASCADE
    op.create_foreign_key(
        'task_runs_task_id_fkey',
        'task_runs',
        'tasks',
        ['task_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade():
    # Drop the cascade FK
    op.drop_constraint('task_runs_task_id_fkey', 'task_runs', type_='foreignkey')
    
    # Recreate the original FK without cascade
    op.create_foreign_key(
        'task_runs_task_id_fkey',
        'task_runs',
        'tasks',
        ['task_id'],
        ['id']
    )
