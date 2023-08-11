"""Rename column path to alias

Revision ID: 192a9111cac1
Revises: 2e3b4399e615
Create Date: 2023-08-12 02:08:26.114757

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '192a9111cac1'
down_revision: Union[str, None] = '2e3b4399e615'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('files', 'path', new_column_name='alias')


def downgrade() -> None:
    op.alter_column('files', 'alias', new_column_name='path')
