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
revision: str = "df85f32342e4"
down_revision: Union[str, None] = "255f65c142b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """CREATE OR REPLACE VIEW alertswisscap.v_cap_polygons AS
        SELECT alert.*, info.*, areas.*, polygons.*
        FROM alertswisscap.cap_alerts as alert
        JOIN alertswisscap.cap_info as info ON alert.cap_id = info.cap_alert_cap_id
        JOIN alertswisscap.cap_areas as areas ON info.info_id = areas.cap_info_info_id
        JOIN alertswisscap.cap_polygons as polygons on areas.area_id = polygons.cap_area_area_id;
    """
    )
    op.execute(
        """CREATE OR REPLACE VIEW alertswisscap.v_cap_circles AS
        SELECT alert.*, info.*, areas.*, circles.*
        FROM alertswisscap.cap_alerts as alert
        JOIN alertswisscap.cap_info as info ON alert.cap_id = info.cap_alert_cap_id
        JOIN alertswisscap.cap_areas as areas ON info.info_id = areas.cap_info_info_id
        JOIN alertswisscap.cap_circles as circles on areas.area_id = circles.cap_area_area_id;
    """
    )


def downgrade() -> None:
    op.execute("DROP VIEW alertswisscap.v_cap_circles CASCADE;")
    op.execute("DROP VIEW alertswisscap.v_cap_polygons CASCADE;")
