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
    CAPAlertUnified,
    CAPCircle,
    CAPGeocodes,
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
        alerts = self.session.query(CAPAlertUnified).all()
        infos = self.session.query(CAPAlertUnified).all()
        return alerts, infos

    def put_alerts(self, alerts):
        self.session.query(CAPAlertUnified).delete()

        for alert in alerts:
            first_content = alert["content"][0]

            cap_alert = CAPAlertUnified(
                cap_id=first_content["cap_id"],
                reference=alert["reference"],
                cap_sender=first_content.get("cap_sender"),
                cap_sent=first_content.get("cap_sent"),
                cap_status=first_content.get("cap_status"),
                cap_message_type=first_content.get("cap_message_type"),
                cap_scope=first_content.get("cap_scope"),
                cap_code=first_content.get("cap_code"),
                cap_restriction=first_content.get("cap_restriction"),
                cap_references=first_content.get("cap_references"),
                cap_category=None,  # will be filled from 'de-CH' info
                cap_event=None,
                cap_urgency=None,
                cap_severity=None,
                cap_certainty=None,
                cap_onset=None,
                cap_expires=None,
                cap_sender_name=None,
                cap_web=None,
                cap_contact=None,
            )

            # Now process infos
            for info in first_content.get("cap_info", []):
                lang = info.get("cap_language")

                if lang == "de-CH":
                    # Fill common fields from de-CH info block
                    cap_alert.cap_category = info.get("cap_category")
                    cap_alert.cap_event = info.get("cap_event")
                    cap_alert.cap_urgency = info.get("cap_urgency")
                    cap_alert.cap_severity = info.get("cap_severity")
                    cap_alert.cap_certainty = info.get("cap_certainty")
                    cap_alert.cap_onset = info.get("cap_onset")
                    cap_alert.cap_expires = info.get("cap_expires")
                    cap_alert.cap_sender_name = info.get("cap_sender_name")
                    cap_alert.cap_web = info.get("cap_web")
                    cap_alert.cap_contact = info.get("cap_contact")

                    # Process areas (ONLY for de-CH)
                    for area in info.get("cap_area", []):
                        cap_alert.cap_area_desc = area.get("cap_area_desc")
                        cap_alert.cap_area_altitude = area.get("cap_area_altitude")
                        cap_alert.cap_area_ceiling = area.get("cap_area_ceiling")

                        # Geocodes
                        cap_geocodes = CAPGeocodesDict(area.get("geocodes", []))
                        for k, v in cap_geocodes.items():
                            geocode = CAPGeocodes(valueName=k, value=v, cap_alert=cap_alert)
                            self.session.add(geocode)

                        # Polygons
                        cap_multipolygon = AlertSwissCapGeometryMultiPolygon(
                            area.get("polygons", []), cap_geocodes.get("ALERTSWISS_EXCLUDE_POLYGON")
                        )
                        cap_polygon = CAPPolygon(
                            geom=from_shape(cap_multipolygon.as_multipolygon(), srid=4326),
                            cap_alert=cap_alert,
                        )
                        self.session.add(cap_polygon)

                        # Circles
                        circles = AlertSwissCapGeometryPoints(area.get("circles", []))
                        for circle in circles.points():
                            cap_circle = CAPCircle(
                                geom=from_shape(circle.point, srid=4326),
                                radius=circle.radius,
                                cap_alert=cap_alert,
                            )
                            self.session.add(cap_circle)

                # Process translations into language-specific fields
                if lang == "de-CH":
                    cap_alert.cap_headline_de = info.get("cap_headline")
                    cap_alert.cap_description_de = info.get("cap_description")
                    cap_alert.cap_instruction_de = info.get("cap_instruction")
                elif lang == "fr-CH":
                    cap_alert.cap_headline_fr = info.get("cap_headline")
                    cap_alert.cap_description_fr = info.get("cap_description")
                    cap_alert.cap_instruction_fr = info.get("cap_instruction")
                elif lang == "it-CH":
                    cap_alert.cap_headline_it = info.get("cap_headline")
                    cap_alert.cap_description_it = info.get("cap_description")
                    cap_alert.cap_instruction_it = info.get("cap_instruction")
                elif lang == "en-US":
                    cap_alert.cap_headline_en = info.get("cap_headline")
                    cap_alert.cap_description_en = info.get("cap_description")
                    cap_alert.cap_instruction_en = info.get("cap_instruction")

            self.session.add(cap_alert)

        self.session.commit()
