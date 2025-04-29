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


class CAPAlertUnified(Base):
    """
    CAPAlertUnified is a unified model for CAP alerts, combining fields from
    cap_alerts, cap_info, and cap_area sections. This model is designed to
    simplify the database schema and improve query performance by reducing
    the need for complex joins.
    """

    __tablename__ = "cap_alerts"

    cap_id = Column(String, primary_key=True)

    # Original cap_alerts fields
    reference = Column(String, nullable=False)
    cap_sender = Column(String, nullable=True)
    cap_sent = Column(DateTime, nullable=False)
    cap_status = Column(String, nullable=False)
    cap_message_type = Column(String, nullable=False)
    cap_scope = Column(String, nullable=False)
    cap_code = Column(String, nullable=True)
    cap_restriction = Column(String, nullable=True)
    cap_references = Column(String, nullable=True)

    # cap_info fields (merged)
    cap_category = Column(String, nullable=False)
    cap_event = Column(String, nullable=False)
    cap_urgency = Column(String, nullable=False)
    cap_severity = Column(String, nullable=False)
    cap_certainty = Column(String, nullable=False)
    cap_onset = Column(DateTime, nullable=True)
    cap_expires = Column(DateTime, nullable=True)
    cap_sender_name = Column(String, nullable=True)
    cap_web = Column(String, nullable=True)
    cap_contact = Column(String, nullable=True)

    # Language-specific fields
    cap_headline_de = Column(String, nullable=True)
    cap_headline_fr = Column(String, nullable=True)
    cap_headline_it = Column(String, nullable=True)
    cap_headline_en = Column(String, nullable=True)

    cap_description_de = Column(String, nullable=True)
    cap_description_fr = Column(String, nullable=True)
    cap_description_it = Column(String, nullable=True)
    cap_description_en = Column(String, nullable=True)

    cap_instruction_de = Column(String, nullable=True)
    cap_instruction_fr = Column(String, nullable=True)
    cap_instruction_it = Column(String, nullable=True)
    cap_instruction_en = Column(String, nullable=True)

    # cap_area fields (merged)
    cap_area_desc = Column(String, nullable=True)
    cap_area_altitude = Column(Float, nullable=True)
    cap_area_ceiling = Column(Float, nullable=True)

    # Relationships (if you still have other spatial tables)
    cap_geocodes = relationship("CAPGeocodes", back_populates="cap_alert", cascade="all, delete-orphan")
    cap_circles = relationship("CAPCircle", back_populates="cap_alert", cascade="all, delete-orphan")
    cap_polygons = relationship("CAPPolygon", back_populates="cap_alert", cascade="all, delete-orphan")


class CAPGeocodes(Base):
    __tablename__ = "cap_geocodes"

    geocode_id = Column(Integer, primary_key=True, autoincrement=True)
    valueName = Column(String, nullable=False)
    value = Column(String, nullable=False)

    cap_alert_cap_id = Column(String, ForeignKey("cap_alerts.cap_id", ondelete="CASCADE"), nullable=False)
    cap_alert = relationship("CAPAlertUnified", back_populates="cap_geocodes")


class CAPPolygon(Base):
    __tablename__ = "cap_polygons"

    polygon_id = Column(Integer, primary_key=True, autoincrement=True)
    geom = Column(Geometry(geometry_type="MULTIPOLYGON", srid=4326))

    cap_alert_cap_id = Column(String, ForeignKey("cap_alerts.cap_id", ondelete="CASCADE"), nullable=False)
    cap_alert = relationship("CAPAlertUnified", back_populates="cap_polygons")


class CAPCircle(Base):
    __tablename__ = "cap_circles"

    circle_id = Column(Integer, primary_key=True, autoincrement=True)
    geom = Column(Geometry(geometry_type="POINT", srid=4326))
    radius = Column(Float, nullable=True)  # radius in kilometers

    cap_alert_cap_id = Column(String, ForeignKey("cap_alerts.cap_id", ondelete="CASCADE"), nullable=False)
    cap_alert = relationship("CAPAlertUnified", back_populates="cap_circles")


class CantonLookup(Base):
    __tablename__ = "canton_lookup"

    shortener = Column(String, primary_key=True)
    canton_number = Column(Integer, unique=True)
