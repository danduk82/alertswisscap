"""Create geocodes stuff

Revision ID: 93a87e9850d8
Revises: f0ace6c7445b
Create Date: 2025-04-29 14:11:04.077542

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "93a87e9850d8"
down_revision: Union[str, None] = "f0ace6c7445b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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

    op.execute(
        """CREATE OR REPLACE VIEW alertswisscap.v_cap_alerts_geocodes AS
            SELECT
                a.cap_id || '_GC_' || g.value AS view_id,
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
                g."valueName",
                g.value,
                CAST(ST_Force2D(k.geom) AS geometry(MultiPolygon, 4326)) AS geom
            FROM
                alertswisscap.cap_alerts a
            JOIN
                alertswisscap.cap_geocodes g ON g.cap_alert_cap_id = a.cap_id
            JOIN
                alertswisscap.canton_lookup l ON g.value = l.shortener
            JOIN
                alertswisscap.tlm_kantonsgebiet k ON k.kantonsnummer = l.canton_number
            WHERE
                g."valueName" = 'CANTON';
            """
    )


def downgrade() -> None:
    op.execute("DROP VIEW alertswisscap.v_cap_alerts_geocodes;")
    op.execute("TRUNCATE alertswisscap.canton_lookup;")
