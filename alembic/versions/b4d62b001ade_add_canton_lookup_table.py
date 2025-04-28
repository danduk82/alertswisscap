"""Add canton_lookup table

Revision ID: b4d62b001ade
Revises: df85f32342e4
Create Date: 2025-04-23 11:45:07.322080

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b4d62b001ade"
down_revision: Union[str, None] = "df85f32342e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "canton_lookup",
        sa.Column("shortener", sa.Text(), primary_key=True),
        sa.Column("canton_number", sa.Integer(), unique=True),
        schema="alertswisscap",
    )

    # Insert initial data
    op.execute(
        """
        INSERT INTO alertswisscap.canton_lookup (shortener, canton_number) VALUES
        ('GE', 25), ('TG', 20), ('VS', 23), ('AG', 19), ('SZ', 5),
        ('ZH', 1), ('OW', 6), ('FR', 10), ('GL', 8), ('UR', 4),
        ('NW', 7), ('SO', 11), ('AR', 15), ('JU', 26), ('GR', 18),
        ('VD', 22), ('LU', 3), ('TI', 21), ('ZG', 9), ('BL', 13),
        ('SG', 17), ('SH', 14), ('BE', 2), ('BS', 12), ('NE', 24),
        ('AI', 16);
    """
    )


def downgrade():
    op.drop_table("alertswisscap.canton_lookup")
