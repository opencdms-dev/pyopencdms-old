import os
from sqlalchemy import create_engine
from geoalchemy2 import Geography

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database, drop_database
from typing import Optional

_cdm_version_ = "0.0.1"

Base = declarative_base()
metadata = Base.metadata

class Observation_type(Base):
    __tablename__ = "observation_type"
    __table_args__ = {'schema': 'cdm'}
    id = Column(  Integer, comment="ID / primary key", primary_key=True)
    name = Column(  String, comment="Short name for observation type")
    description = Column(  String, comment="Description of observation type")
    link = Column(  String, comment="Link to definition of observation type")


class Feature_type(Base):
    __tablename__ = "feature_type"
    __table_args__ = {'schema': 'cdm'}
    id = Column(  Integer, comment="ID / primary key", primary_key=True)
    name = Column(  String, comment="Short name for feature type")
    description = Column(  String, comment="Description of feature type")
    link = Column(  String, comment="Link to definition of feature type")


class Observed_property(Base):
    __tablename__ = "observed_property"
    __table_args__ = {'schema': 'cdm'}
    id = Column(  Integer, comment="ID / primary key", primary_key=True)
    short_name = Column(  String, comment="Short name representation of observed property, e.g. 'at'")
    standard_name = Column(  String, comment="CF standard name (if applicable), e.g. 'air_temperature'")
    units = Column(  String, comment="Canonical units, e.g. 'Kelvin'")
    description = Column(  String, comment="Description of observed property")
    link = Column(  String, comment="Link to definition / source of observed property")


class Observing_procedure(Base):
    __tablename__ = "observing_procedure"
    __table_args__ = {'schema': 'cdm'}
    id = Column(  Integer, comment="ID / primary key", primary_key=True)
    name = Column(  String, comment="Name of observing procedure")
    description = Column(  String, comment="Description of observing procedure")
    link = Column(  String, comment="Link to further information")


class Record_status(Base):
    __tablename__ = "record_status"
    __table_args__ = {'schema': 'cdm'}
    id = Column(  Integer, comment="ID / primary key", primary_key=True)
    name = Column(  String, comment="Short name for status")
    description = Column(  String, comment="Description of the status")


class Stations(Base):
    __tablename__ = "stations"
    __table_args__ = {'schema': 'cdm'}
    id = Column(  String, comment="ID / primary key", primary_key=True)
    name = Column(  String, comment="Preferred name of station")
    description = Column(  String, comment="Station description")
    link = Column(  String, comment="URI to station, e.g. to OSCAR/Surface")
    location = Column(  Geography, comment="Location of station")
    elevation = Column(  Numeric, comment="Elevation of station above mean sea level")
    wigos_station_identifier = Column(  String, comment="WIGOS station identifier")
    facility_type = Column(  String, comment="Type of observing facility, fixed land, mobile sea, etc")
    date_established = Column(  String, comment="Date station was first established")
    wmo_region = Column(  String, comment="WMO region in which the station is located")
    territory = Column(  String, comment="Territory the station is located in")
    valid_from = Column(  DateTime, comment="Date from which the details for this record are valid")
    valid_to = Column(  DateTime, comment="Date after which the details for this record are no longer valid")
    version = Column(  Integer, comment="Version number of this record")
    change_date = Column(  DateTime, comment="Date this record was changed")
    user = Column(ForeignKey("cdm.users.id"), comment="Which user last modified this record")
    status = Column( ForeignKey("cdm.record_status.id"), comment="Whether this is the latest version or an archived version of the record")
    comments = Column(  String, comment="Free text comments on this record, for example description of changes made etc")


class Sensors(Base):
    __tablename__ = "sensors"
    __table_args__ = {'schema': 'cdm'}
    id = Column(  String, comment="ID / primary key", primary_key=True)
    name = Column(  String, comment="Name of sensor")
    description = Column(  String, comment="Description of sensor")
    link = Column(  String, comment="Link to further information")


class Observations(Base):
    __tablename__ = "observations"
    __table_args__ = {'schema': 'cdm'}
    id = Column(  String, comment="ID / primary key", primary_key=True)
    location = Column(  Geography, comment="location of observation")
    observation_type = Column( ForeignKey("cdm.observation_type.id"), comment="Type of observation")
    phenomenon_start = Column(  DateTime, comment="Start time of the phenomenon being observed or observing period, if missing assumed instantaneous with time given by phenomenon_end")
    phenomenon_end = Column(  DateTime, comment="End time of the phenomenon being observed or observing period")
    result_value = Column(  Numeric, comment="The value of the result in numeric representation")
    result_uom = Column(  String, comment="Units used to represent the value being observed")
    result_description = Column(  String, comment="String representation of the result if applicable")
    result_quality = Column(  JSONB, comment="JSON representation of the result quality, key / value pairs")
    result_time = Column(  DateTime, comment="Time that the result became available")
    valid_from = Column(  DateTime, comment="Time that the result starts to be valid")
    valid_to = Column(  DateTime, comment="Time after which the result is no longer valid")
    station = Column( ForeignKey("cdm.stations.id"), comment="Station associated with making the observation, equivalent to OGC OMS 'host'")
    sensor = Column( ForeignKey("cdm.sensors.id"), comment="Sensor associated with making the observation, equivalent to OGC OMS 'observer'")
    observed_property = Column( ForeignKey("cdm.observed_property.id"), comment="The phenomenon, or thing, being observed")
    observing_procedure = Column( ForeignKey("cdm.observing_procedure.id"), comment="Procedure used to make the observation")
    report_id = Column(  String, comment="Parent report ID, used to link coincident observations together")
    collection = Column( ForeignKey("cdm.collections.id"), comment="Primary collection or dataset that this observation belongs to")
    parameter = Column(  JSONB, comment="List of key/ value pairs in JSONB")
    feature_of_interest = Column( ForeignKey("cdm.features.id"), comment="Feature that this observation is associated with")
    version = Column(  Integer, comment="Version number of this record")
    change_date = Column(  DateTime, comment="Date this record was changed")
    user = Column( ForeignKey("cdm.users.id"), comment="Which user last modified this record")
    status = Column( ForeignKey("cdm.record_status.id"), comment="Whether this is the latest version or an archived version of the record")
    comments = Column(  String, comment="Free text comments on this record, for example description of changes made etc")


class Collections(Base):
    __tablename__ = "collections"
    __table_args__ = {'schema': 'cdm'}
    id = Column(  String, comment="ID / primary key", primary_key=True)
    name = Column(  String, comment="Name of collection")
    link = Column(  String, comment="Link to further information on collection")


class Features(Base):
    __tablename__ = "features"
    __table_args__ = {'schema': 'cdm'}
    id = Column(  String, comment="ID / primary key", primary_key=True)
    type = Column( ForeignKey("cdm.feature_type.id"), comment="enumerated feature type")
    geometry = Column(  Geography, comment="")
    parent = Column( ForeignKey("cdm.features.id"), comment="Parent feature for this feature if nested")


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'cdm'}
    id = Column(  String, comment="ID / primary key", primary_key=True)
    name = Column(  String, comment="Name of user")

