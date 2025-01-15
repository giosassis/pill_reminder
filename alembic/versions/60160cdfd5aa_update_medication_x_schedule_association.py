"""Update Medication x Schedule association

Revision ID: 60160cdfd5aa
Revises: 243c27ed8eb8
Create Date: 2025-01-12 10:41:06.588296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '60160cdfd5aa'
down_revision: Union[str, None] = '243c27ed8eb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index('ix_medication_schedule_association_id',
                  table_name='medication_schedule_association')
    op.drop_table('medication_schedule_association')
    op.add_column('medication_schedules', sa.Column(
        'medication_id', sa.String(), nullable=True))
    op.create_foreign_key(None, 'medication_schedules',
                          'medications', ['medication_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'medication_schedules', type_='foreignkey')
    op.drop_column('medication_schedules', 'medication_id')
    op.create_table('medication_schedule_association',
                    sa.Column('id', sa.VARCHAR(),
                              autoincrement=False, nullable=False),
                    sa.Column('medication_id', sa.VARCHAR(),
                              autoincrement=False, nullable=True),
                    sa.Column('schedule_id', sa.VARCHAR(),
                              autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['medication_id'], [
                        'medications.id'], name='medication_schedule_association_medication_id_fkey'),
                    sa.ForeignKeyConstraint(['schedule_id'], [
                        'medication_schedules.id'], name='medication_schedule_association_schedule_id_fkey'),
                    sa.PrimaryKeyConstraint(
                        'id', name='medication_schedule_association_pkey')
                    )
    op.create_index('ix_medication_schedule_association_id',
                    'medication_schedule_association', ['id'], unique=False)
