"""create superadmin

Revision ID: 434ed2ef3419
Revises: f4c7223e0c61
Create Date: 2026-03-02 23:25:18.667407

"""
import os
from typing import Sequence, Union

from alembic import op


from dotenv import load_dotenv
from src.common.enums import UserRole

load_dotenv()


# revision identifiers, used by Alembic.
revision: str = "434ed2ef3419"
down_revision: Union[str, Sequence[str], None] = "f4c7223e0c61"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    superadmin_name = os.getenv('SUPERADMIN_NAME', 'Admin')
    superadmin_telegram = os.getenv('SUPERADMIN_TELEGRAM_ID')
    if not superadmin_telegram:
        raise Exception("Необходимо указать ID суперадмина в env!")
    op.execute(
        f"""
        INSERT INTO "user" (name, telegram_id, role, is_active)
        VALUES ('{superadmin_name}', {superadmin_telegram}, '{UserRole.SUPERADMIN.value}', true)
        """
    )



def downgrade() -> None:
    """Downgrade schema."""
    superadmin_telegram = os.getenv('SUPERADMIN_TELEGRAM_ID')
    if superadmin_telegram:
        op.execute(f"""DELETE FROM "user" WHERE telegram_id = {superadmin_telegram}""")
