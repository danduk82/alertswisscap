from geoalchemy2 import Geometry
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from alertswisscap.model.orm.cap import Base, CAPAlert, CAPArea, CAPCircle, CAPInfo, CAPLinestring, CAPPolygon


class CapPgController:
    def __init__(self, pg_url, dbschema="alertswisscap"):
        self.url = pg_url
        self.dbschema = dbschema
        self.engine = create_engine(self.url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def put_alerts(self, alerts):
        for alert in alerts:
            cap_alert = CAPAlert(
                reference=alert["reference"],
                cap_id=alert["cap_id"],
                cap_sender=alert["cap_sender"],
                cap_sent=alert["cap_sent"],
                cap_status=alert["cap_status"],
                cap_message_type=alert["cap_message_type"],
                cap_scope=alert["cap_scope"],
            )
            for info in alert["cap_info"]:
                cap_info = CAPInfo(
                    cap_language=info["cap_language"],
                    cap_category=info["cap_category"],
                    cap_event=info["cap_event"],
                    cap_urgency=info["cap_urgency"],
                    cap_severity=info["cap_severity"],
                    cap_certainty=info["cap_certainty"],
                    cap_onset=info["cap_onset"],
                    cap_sender_name=info["cap_sender_name"],
                    cap_headline=info["cap_headline"],
                    cap_description=info["cap_description"],
                    cap_instruction=info["cap_instruction"],
                    cap_contact=info["cap_contact"],
                )
                cap_alert.cap_info.append(cap_info)
            self.session.add(cap_alert)
        self.session.commit()
