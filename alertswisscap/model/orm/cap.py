from geoalchemy2 import Geometry
from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base(metadata=MetaData(schema="alertswisscap"))


class CAPAlert(Base):
    __tablename__ = "cap_alerts"

    cap_id = Column(String, primary_key=True)
    reference = Column(String, nullable=False)
    cap_sender = Column(String, nullable=True)
    cap_sent = Column(DateTime, nullable=False)
    cap_status = Column(String, nullable=False)
    cap_message_type = Column(String, nullable=False)
    cap_scope = Column(String, nullable=False)
    cap_code = Column(String, nullable=True)
    cap_restriction = Column(String, nullable=True)
    cap_references = Column(String, nullable=True)

    # Assuming one-to-many relationship between CAPAlert and CAPInfo
    cap_info = relationship("CAPInfo", back_populates="cap_alert")
    cap_area = relationship("CAPArea", back_populates="cap_alert")


class CAPInfo(Base):
    __tablename__ = "cap_info"
    __table_args__ = (
        UniqueConstraint("cap_alert_cap_id", "cap_language", name="uc_cap_info_cap_id_cap_languange"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    cap_language = Column(String, nullable=False)
    cap_category = Column(String, nullable=False)
    cap_event = Column(String, nullable=False)
    cap_urgency = Column(String, nullable=False)
    cap_severity = Column(String, nullable=False)
    cap_certainty = Column(String, nullable=False)
    cap_onset = Column(DateTime, nullable=True)
    cap_sender_name = Column(String, nullable=True)
    cap_expires = Column(DateTime, nullable=True)
    cap_sender_name = Column(String, nullable=True)
    cap_headline = Column(String, nullable=False)
    cap_description = Column(String, nullable=False)
    cap_instruction = Column(String, nullable=True)
    cap_web = Column(String, nullable=True)
    cap_contact = Column(String, nullable=True)

    # Foreign key relationship with CAPAlert
    cap_alert_cap_id = Column(String, ForeignKey("cap_alerts.cap_id"), nullable=False)
    cap_alert = relationship("CAPAlert", back_populates="cap_info")


class CAPArea(Base):
    __tablename__ = "cap_areas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cap_circle_id = Column(Integer, ForeignKey("cap_circles.id"))
    cap_polygon_id = Column(Integer, ForeignKey("cap_polygons.id"))

    cap_alert_cap_id = Column(String, ForeignKey("cap_alerts.cap_id"), nullable=False)
    cap_alert = relationship("CAPAlert", back_populates="cap_area")


class CAPPolygon(Base):
    __tablename__ = "cap_polygons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    geom = Column(Geometry(geometry_type="MULTIPOLYGON", srid=4326))


class CAPCircle(Base):
    __tablename__ = "cap_circles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    geom = Column(Geometry(geometry_type="POINT", srid=4326))
    radius = Column(Float)


# Create the engine and tables
# engine = create_engine('postgresql://your_username:your_password@localhost/your_database')
# Base.metadata.create_all(engine)
