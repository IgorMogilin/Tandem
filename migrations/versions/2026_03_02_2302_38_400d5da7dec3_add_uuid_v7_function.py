"""Add uuid_v7 function

Revision ID: 400d5da7dec3
Revises:
Create Date: 2026-03-02 23:02:38.289495

"""

from pathlib import Path
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "400d5da7dec3"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    sql_file = Path(__file__).parent.parent / "sql" / "generate_uuid__v7.sql"
    if not sql_file.exists():
        raise FileNotFoundError("Не найден код добавления UUID v7")
    with open(sql_file) as file:
        sql= file.read()
    op.execute(sql)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP FUNCTION IF EXISTS generate_uuid__v7();")
