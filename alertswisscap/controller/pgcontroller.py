from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from alertswisscap.model.geometries import (
    AlertSwissCapGeometryMultiPolygon,
    AlertSwissCapGeometryPoints,
    CAPGeocodesDict,
)
from alertswisscap.model.orm.cap import (
    Base,
    CAPAlert,
    CAPArea,
    CAPCircle,
    CAPGeocodes,
    CAPInfo,
    CAPPolygon,
)


class CapPgController:
    def __init__(self, pg_url, dbschema="alertswisscap"):
        self.url = pg_url
        self.dbschema = dbschema
        self.engine = create_engine(self.url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def load_alerts(self):
        alerts = self.session.query(CAPAlert).all()
        infos = self.session.query(CAPInfo).all()
        return alerts, infos

    def put_alerts(self, alerts):
        self.session.query(CAPAlert).delete()

        for alert in alerts:
            cap_alert = CAPAlert(
                reference=alert["reference"],
                cap_id=alert["content"][0]["cap_id"],
                cap_sender=alert["content"][0]["cap_sender"],
                cap_sent=alert["content"][0]["cap_sent"],
                cap_status=alert["content"][0]["cap_status"],
                cap_message_type=alert["content"][0]["cap_message_type"],
                cap_scope=alert["content"][0]["cap_scope"],
            )
            # FIXME: what to do if there are no cap_info?
            for info in alert["content"][0].get("cap_info", []):
                cap_info = CAPInfo(
                    cap_language=info.get("cap_language", None),
                    cap_category=info.get("cap_category", None),
                    cap_event=info.get("cap_event", None),
                    cap_urgency=info.get("cap_urgency", None),
                    cap_severity=info.get("cap_severity", None),
                    cap_certainty=info.get("cap_certainty", None),
                    cap_onset=info.get("cap_onset", None),
                    cap_sender_name=info.get("cap_sender_name", None),
                    cap_headline=info.get("cap_headline", None),
                    cap_description=info.get("cap_description", None),
                    cap_instruction=info.get("cap_instruction", None),
                    cap_contact=info.get("cap_contact", None),
                )
                # FIXME: what to do if there are no cap_area?
                for area in info.get("cap_area", []):
                    cap_area = CAPArea(
                        cap_area_desc=area.get("cap_area_desc", None),
                        cap_area_altitude=area.get("cap_area_altitude", None),
                        cap_area_ceiling=area.get("cap_area_ceiling", None),
                    )
                    cap_geocodes = CAPGeocodesDict(area.get("geocodes", []))
                    for k, v in cap_geocodes.items():
                        print(k, v)
                        geocode = CAPGeocodes(valueName=k, value=v)
                        cap_area.cap_geocodes.append(geocode)
                    cap_multipolygon = AlertSwissCapGeometryMultiPolygon(
                        area.get("polygons", []), cap_geocodes.get("ALERTSWISS_EXCLUDE_POLYGON")
                    )
                    cap_polygon = CAPPolygon(geom=from_shape(cap_multipolygon.as_multipolygon(), srid=4326))
                    cap_area.cap_polygons.append(cap_polygon)
                    circles = AlertSwissCapGeometryPoints(area.get("circles", []))
                    for circle in circles.points():
                        cap_circle = CAPCircle(geom=from_shape(circle.point, srid=4326), radius=circle.radius)
                        cap_area.cap_circles.append(cap_circle)
                    cap_info.cap_area.append(cap_area)
                cap_alert.cap_info.append(cap_info)
            self.session.add(cap_alert)
        self.session.commit()
