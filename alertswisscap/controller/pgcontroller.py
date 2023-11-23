from ..model.orm.cap import Base, CAPAlert, CAPInfo, CAPArea, CAPPolygon, CAPLinestring, CAPCircle
from ..apiclient.client import CAPClient

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from sqlalchemy.exc import IntegrityError

from geoalchemy2 import Geometry

class PgController():
    def __init__(self, pg_url):
        self.pg_url = pg_url
        self.engine = create_engine(self.url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
    def put_alert(self, alert):
        cap_alert = CAPAlert(
            reference=alert['reference'],
            cap_id=alert['cap_id'],
            cap_sender=alert['cap_sender'],
            cap_sent=alert['cap_sent'],
            cap_status=alert['cap_status'],
            cap_message_type=alert['cap_message_type'],
            cap_scope=alert['cap_scope']
        )
        cap_info = CAPInfo(
            cap_language=alert['cap_language'],
            cap_category=alert['cap_category'],
            cap_event=alert['cap_event'],
            cap_urgency=alert['cap_urgency'],
            cap_severity=alert['cap_severity'],
            cap_certainty=alert['cap_certainty'],
            cap_onset=alert['cap_onset'],
            cap_sender_name=alert['cap_sender_name'],
            cap_headline=alert['cap_headline'],
            cap_description=alert['cap_description'],
            cap_instruction=alert['cap_instruction'],
            cap_contact=alert['cap_contact']
        )
        cap_alert.cap_info = cap_info
        self.session.add(cap_alert)
        self.session.commit()
    