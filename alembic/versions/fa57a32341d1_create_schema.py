"""create tables

Revision ID: 255f65c142b3
Revises:
Create Date: 2024-02-12 15:11:23.334436

"""

from collections.abc import Sequence
from typing import Union

import geoalchemy2
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fa57a32341d1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE SCHEMA IF NOT EXISTS alertswisscap;")


def downgrade() -> None:
    op.execute("DROP SCHEMA alertswisscap CASCADE;")
