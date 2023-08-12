"""Add StorageLastUpdate model

Revision ID: 4fdc433308f4
Revises: 192a9111cac1
Create Date: 2023-08-12 13:30:15.224477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4fdc433308f4'
down_revision: Union[str, None] = '192a9111cac1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'storage_last_update',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('value', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('storage_last_update')
