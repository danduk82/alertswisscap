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
        SELECT (alert.cap_id::text || '_' || info.info_id::text || '_' || areas.area_id::text || '_' || polygons.polygon_id::text) AS fid,
        alert.*,
        info.*,
        areas.*,
        ST_SetSRID(ST_Multi(polygons.geom), 4326) AS geom
        FROM alertswisscap.cap_alerts as alert
        JOIN alertswisscap.cap_info as info ON alert.cap_id = info.cap_alert_cap_id
        JOIN alertswisscap.cap_areas as areas ON info.info_id = areas.cap_info_info_id
        JOIN alertswisscap.cap_polygons as polygons on areas.area_id = polygons.cap_area_area_id;
    """
    )
    op.execute(
        """CREATE OR REPLACE VIEW alertswisscap.v_cap_circles AS
        SELECT row_number() OVER () AS unique_id, alert.*, info.*, areas.*, circles.*
        FROM alertswisscap.cap_alerts as alert
        JOIN alertswisscap.cap_info as info ON alert.cap_id = info.cap_alert_cap_id
        JOIN alertswisscap.cap_areas as areas ON info.info_id = areas.cap_info_info_id
        JOIN alertswisscap.cap_circles as circles on areas.area_id = circles.cap_area_area_id;
    """
    )
    op.execute(
        """CREATE OR REPLACE VIEW alertswisscap.cap_geocodes_with_geom AS
           SELECT
               cge.*,
               kg.geom
           FROM
               alertswisscap.cap_geocodes AS cge
           JOIN
               alertswisscap.canton_lookup AS cl
               ON cge.value = cl.shortener
           JOIN
               alertswisscap.tlm_kantonsgebiet AS kg
               ON cl.canton_number = kg.kantonsnummer
           WHERE
               cge."valueName" = 'CANTON';"""
    )

    op.execute(
        """CREATE OR REPLACE VIEW alertswisscap.cap_alert_polygons AS
            SELECT
                ca.area_id AS cap_area_id,
                ci.info_id AS cap_info_id,
                al.cap_id AS cap_alert_id,
                al.*,
                ci.*,
                ca.*,
                CAST(p.geom AS geometry(MultiPolygon, 4326)) AS geom
            FROM
                alertswisscap.cap_alerts al
            JOIN
                alertswisscap.cap_info ci ON ci.cap_alert_cap_id = al.cap_id
            JOIN
                alertswisscap.cap_areas ca ON ca.cap_info_info_id = ci.info_id
            JOIN
                alertswisscap.cap_polygons p ON p.cap_area_area_id = ca.area_id;
                """
    )

    op.execute(
        """CREATE OR REPLACE VIEW alertswisscap.cap_geocodes_with_geom AS
            SELECT
                cge.*,
                kg.geom
            FROM
                alertswisscap.cap_geocodes AS cge
            JOIN
                alertswisscap.canton_lookup AS cl
                ON cge.value = cl.shortener
            JOIN
                alertswisscap.tlm_kantonsgebiet AS kg
                ON cl.canton_number = kg.kantonsnummer
            WHERE
                cge."valueName" = 'CANTON';
    """
    )

    op.execute(
        """CREATE OR REPLACE VIEW alertswisscap.cap_alert_all_geoms AS
            SELECT
                al.cap_id AS cap_alert_cap_id,
                'polygon' AS geom_type,
                CAST(p.geom AS geometry(MultiPolygon, 4326)) AS geom
            FROM
                alertswisscap.cap_alerts al
            JOIN alertswisscap.cap_info ci ON ci.cap_alert_cap_id = al.cap_id
            JOIN alertswisscap.cap_areas ca ON ca.cap_info_info_id = ci.info_id
            JOIN alertswisscap.cap_polygons p ON p.cap_area_area_id = ca.area_id

            UNION ALL

            SELECT
                al.cap_id AS cap_alert_cap_id,
                'point' AS geom_type,
                CAST(pt.geom AS geometry(Point, 4326)) AS geom
            FROM
                alertswisscap.cap_alerts al
            JOIN alertswisscap.cap_info ci ON ci.cap_alert_cap_id = al.cap_id
            JOIN alertswisscap.cap_areas ca ON ca.cap_info_info_id = ci.info_id
            JOIN alertswisscap.cap_circles pt ON pt.cap_area_area_id = ca.area_id

            UNION ALL

            SELECT
                al.cap_id AS cap_alert_cap_id,
                'geocode' AS geom_type,
                CAST(g.geom AS geometry(MultiPolygon, 4326)) AS geom
            FROM
                alertswisscap.cap_alerts al
            JOIN alertswisscap.cap_info ci ON ci.cap_alert_cap_id = al.cap_id
            JOIN alertswisscap.cap_areas ca ON ca.cap_info_info_id = ci.info_id
            JOIN alertswisscap.cap_geocodes g ON g.cap_area_area_id = ca.area_id
            WHERE g.valueName = 'CANTON';

            def downgrade() -> None:
                op.execute("DROP VIEW alertswisscap.v_cap_circles CASCADE;")
                op.execute("DROP VIEW alertswisscap.v_cap_polygons CASCADE;")
    """
    )
