from geoalchemy2 import Geometry
from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CAPAlert(Base):
    __tablename__ = "cap_alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reference = Column(String, nullable=False)
    cap_id = Column(String, nullable=False)
    cap_sender = Column(String, nullable=False)
    cap_sent = Column(DateTime, nullable=False)
    cap_status = Column(String, nullable=False)
    cap_message_type = Column(String, nullable=False)
    cap_scope = Column(String, nullable=False)

    # Assuming one-to-many relationship between CAPAlert and CAPInfo
    cap_info = relationship("CAPInfo", back_populates="cap_alert")


class CAPInfo(Base):
    __tablename__ = "cap_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cap_language = Column(String, nullable=False)
    cap_category = Column(String)
    cap_event = Column(String)
    cap_urgency = Column(String)
    cap_severity = Column(String)
    cap_certainty = Column(String)
    cap_onset = Column(DateTime)
    cap_sender_name = Column(String)
    cap_headline = Column(String)
    cap_description = Column(String)
    cap_instruction = Column(String)
    cap_contact = Column(String)

    # Foreign key relationship with CAPAlert
    cap_alert_id = Column(Integer, ForeignKey("cap_alerts.id"))
    cap_alert = relationship("CAPAlert", back_populates="cap_info")


class CAPArea(Base):
    __tablename__ = "cap_areas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cap_circle_id = Column(Integer, ForeignKey("cap_circles.id"))
    cap_polygon_id = Column(Integer, ForeignKey("cap_polygons.id"))
    cap_linestring_id = Column(Integer, ForeignKey("cap_linestrings.id"))


class CAPPolygon(Base):
    __tablename__ = "cap_polygons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    geom = Column(Geometry(geometry_type="MULTIPOLYGON", srid=4326))


class CAPLinestring(Base):
    __tablename__ = "cap_linestrings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    geom = Column(Geometry(geometry_type="MULTILINESTRING", srid=4326))


class CAPCircle(Base):
    __tablename__ = "cap_circles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    geom = Column(Geometry(geometry_type="POINT", srid=4326))
    radius = Column(Float)


# Create the engine and tables
# engine = create_engine('postgresql://your_username:your_password@localhost/your_database')
# Base.metadata.create_all(engine)
