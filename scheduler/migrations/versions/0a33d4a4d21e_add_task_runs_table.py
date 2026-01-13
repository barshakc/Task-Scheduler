"""add task_runs table

Revision ID: 0a33d4a4d21e
Revises: 85b14f2d1a45
Create Date: 2026-01-13 14:58:27.963069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a33d4a4d21e'
down_revision: Union[str, Sequence[str], None] = '85b14f2d1a45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade():
    from alembic import op
    import sqlalchemy as sa
    from sqlalchemy.dialects import postgresql

    taskstatus_enum = postgresql.ENUM('active', 'paused', name='taskstatus', create_type=False)

    op.create_table(
        'task_runs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('task_id', sa.Integer, sa.ForeignKey('tasks.id'), nullable=False),
        sa.Column('status', taskstatus_enum, nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('result', sa.JSON(), nullable=True),
    )

def downgrade():
    from alembic import op

    op.drop_table('task_runs')