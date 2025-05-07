"""Create views

Revision ID: f0ace6c7445b
Revises: 56715f4c6ac8
Create Date: 2025-04-29 13:53:53.008399

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f0ace6c7445b"
down_revision: Union[str, None] = "56715f4c6ac8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """CREATE OR REPLACE VIEW alertswisscap.v_cap_alerts_polygons AS
                    SELECT
                        a.cap_id || '_P_' || p.polygon_id AS view_id,
                        a.cap_id,
                        a.reference,
                        a.cap_sender,
                        a.cap_sent,
                        a.cap_status,
                        a.cap_message_type,
                        a.cap_scope,
                        a.cap_category,
                        a.cap_urgency,
                        a.cap_severity,
                        a.cap_certainty,
                        a.cap_onset,
                        a.cap_expires,
                        a.cap_sender_name,
                        a.cap_area_desc,
                        a.cap_area_altitude,
                        a.cap_area_ceiling,
                        a.cap_headline_de,
                        a.cap_headline_fr,
                        a.cap_headline_it,
                        a.cap_headline_en,
                        a.cap_description_de,
                        a.cap_description_fr,
                        a.cap_description_it,
                        a.cap_description_en,
                        a.cap_event_de,
                        a.cap_event_fr,
                        a.cap_event_it,
                        a.cap_event_en,
                        a.cap_instruction_de,
                        a.cap_instruction_fr,
                        a.cap_instruction_it,
                        a.cap_instruction_en,
                        a.cap_web,
                        a.cap_contact,
                        CAST(p.geom AS geometry(MULTIPOLYGON, 4326)) AS geom
                    FROM
                        alertswisscap.cap_alerts a
                    JOIN
                        alertswisscap.cap_polygons p ON p.cap_alert_cap_id = a.cap_id;

                    """
    )
    op.execute(
        """CREATE OR REPLACE VIEW alertswisscap.v_cap_alerts_circles AS
                    SELECT
                        a.cap_id || '_C_' || c.circle_id AS view_id,
                        a.cap_id,
                        a.reference,
                        a.cap_sender,
                        a.cap_sent,
                        a.cap_status,
                        a.cap_message_type,
                        a.cap_scope,
                        a.cap_category,
                        a.cap_urgency,
                        a.cap_severity,
                        a.cap_certainty,
                        a.cap_onset,
                        a.cap_expires,
                        a.cap_sender_name,
                        a.cap_area_desc,
                        a.cap_area_altitude,
                        a.cap_area_ceiling,
                        a.cap_headline_de,
                        a.cap_headline_fr,
                        a.cap_headline_it,
                        a.cap_headline_en,
                        a.cap_description_de,
                        a.cap_description_fr,
                        a.cap_description_it,
                        a.cap_event_de,
                        a.cap_event_fr,
                        a.cap_event_it,
                        a.cap_event_en,
                        a.cap_description_en,
                        a.cap_instruction_de,
                        a.cap_instruction_fr,
                        a.cap_instruction_it,
                        a.cap_instruction_en,
                        a.cap_web,
                        a.cap_contact,
                        CAST(c.geom AS geometry(POINT, 4326)) AS geom,
                        c.radius
                    FROM
                        alertswisscap.cap_alerts a
                    JOIN
                        alertswisscap.cap_circles c ON c.cap_alert_cap_id = a.cap_id;
                    """
    )


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS alertswisscap.v_cap_alerts_polygons;")
    op.execute("DROP VIEW IF EXISTS alertswisscap.v_cap_alerts_circles;")
