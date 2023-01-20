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

_cdm_version_ = "0.1.0"

Base = declarative_base()
metadata = Base.metadata


class Observation_type(Base):
    __tablename__ = "observation_type"
    __table_args__ = {'schema': 'cdm'}
    id = Column(Integer, comment="ID / primary key", primary_key=True, index=False)  # noqa
    name = Column(String, comment="Short name for observation type", index=False)  # noqa
    description = Column(String, comment="Description of observation type", index=False)  # noqa
    link = Column(String, comment="Link to definition of observation type", index=False)  # noqa


class Feature_type(Base):
    __tablename__ = "feature_type"
    __table_args__ = {'schema': 'cdm'}
    id = Column(Integer, comment="ID / primary key", primary_key=True, index=False)  # noqa
    name = Column(String, comment="Short name for feature type", index=False)  # noqa
    description = Column(String, comment="Description of feature type", index=False)  # noqa
    link = Column(String, comment="Link to definition of feature type", index=False)  # noqa


class Observed_property(Base):
    __tablename__ = "observed_property"
    __table_args__ = {'schema': 'cdm'}
    id = Column(Integer, comment="ID / primary key", primary_key=True, index=False)  # noqa
    short_name = Column(String, comment="Short name representation of observed property, e.g. 'at'", index=False)  # noqa
    standard_name = Column(String, comment="CF standard name (if applicable), e.g. 'air_temperature'", index=False)  # noqa
    units = Column(String, comment="Canonical units, e.g. 'Kelvin'", index=False)  # noqa
    description = Column(String, comment="Description of observed property", index=False)  # noqa
    link = Column(String, comment="Link to definition / source of observed property", index=False)  # noqa


class Observing_procedure(Base):
    __tablename__ = "observing_procedure"
    __table_args__ = {'schema': 'cdm'}
    id = Column(Integer, comment="ID / primary key", primary_key=True, index=False)  # noqa
    name = Column(String, comment="Name of observing procedure", index=False)  # noqa
    description = Column(String, comment="Description of observing procedure", index=False)  # noqa
    link = Column(String, comment="Link to further information", index=False)  # noqa


class Record_status(Base):
    __tablename__ = "record_status"
    __table_args__ = {'schema': 'cdm'}
    id = Column(Integer, comment="ID / primary key", primary_key=True, index=False)  # noqa
    name = Column(String, comment="Short name for status", index=False)
    description = Column(String, comment="Description of the status", index=False)  # noqa


class Hosts(Base):
    __tablename__ = "hosts"
    __table_args__ = {'schema': 'cdm'}
    id = Column(String, comment="ID / primary key", primary_key=True, index=False)  # noqa
    name = Column(String, comment="Preferred name of host", index=False)
    description = Column(String, comment="Description of host", index=False)
    link = Column(String, comment="URI to host, e.g. to OSCAR/Surface", index=False)  # noqa
    location = Column(Geography, comment="Location of station", index=False)
    elevation = Column(Numeric, comment="Elevation of station above mean sea level", index=False)  # noqa
    wigos_station_identifier = Column(String, comment="WIGOS station identifier", index=False)  # noqa
    facility_type = Column(String, comment="Type of observing facility, fixed land, mobile sea, etc", index=False)  # noqa
    date_established = Column(String, comment="Date host was first established", index=False)  # noqa
    wmo_region = Column(String, comment="WMO region in which the host is located", index=False)  # noqa
    territory = Column(String, comment="Territory the host is located in", index=False)  # noqa
    valid_from = Column(DateTime(timezone=True), comment="Date from which the details for this record are valid", index=False)  # noqa
    valid_to = Column(DateTime(timezone=True), comment="Date after which the details for this record are no longer valid", index=False)  # noqa
    version = Column(Integer, comment="Version number of this record", index=False)  # noqa
    change_date = Column(DateTime(timezone=True), comment="Date this record was changed", index=False)  # noqa
    user = Column(ForeignKey("cdm.users.id"), comment="Which user last modified this record", index=False)  # noqa
    status = Column(ForeignKey("cdm.record_status.id"), comment="Whether this is the latest version or an archived version of the record", index=False)  # noqa
    comments = Column(String, comment="Free text comments on this record, for example description of changes made etc", index=False)  # noqa


class Observers(Base):
    __tablename__ = "observers"
    __table_args__ = {'schema': 'cdm'}
    id = Column(String, comment="ID / primary key", primary_key=True, index=False)  # noqa
    name = Column(String, comment="Name of sensor", index=False)
    description = Column(String, comment="Description of sensor", index=False)  # noqa
    link = Column(String, comment="Link to further information", index=False)  # noqa
    location = Column(Geography, comment="Location of observer", index=False)  # noqa
    elevation = Column(Numeric, comment="Elevation of observer above mean sea level", index=False)  # noqa


class Observations(Base):
    __tablename__ = "observations"
    __table_args__ = {'schema': 'cdm'}
    id = Column(String, comment="ID / primary key", primary_key=True, index=False)  # noqa
    location = Column(Geography, comment="Location of observation", index=True)  # noqa
    elevation = Column(Numeric, comment="Elevation of observation above mean sea level", index=False)  # noqa
    observation_type = Column(ForeignKey("cdm.observation_type.id"), comment="Type of observation", index=True)  # noqa
    phenomenon_start = Column(DateTime(timezone=True), comment="Start time of the phenomenon being observed or observing period, if missing assumed instantaneous with time given by phenomenon_end", index=False)  # noqa
    phenomenon_end = Column(DateTime(timezone=True), comment="End time of the phenomenon being observed or observing period", index=True)  # noqa
    result_value = Column(Numeric, comment="The value of the result in numeric representation", index=False)  # noqa
    result_uom = Column(String, comment="Units used to represent the value being observed", index=False)  # noqa
    result_description = Column(String, comment="String representation of the result if applicable", index=False)  # noqa
    result_quality = Column(JSONB, comment="JSON representation of the result quality, key / value pairs", index=False)  # noqa
    result_time = Column(DateTime(timezone=True), comment="Time that the result became available", index=False)  # noqa
    valid_from = Column(DateTime(timezone=True), comment="Time that the result starts to be valid", index=False)  # noqa
    valid_to = Column(DateTime(timezone=True), comment="Time after which the result is no longer valid", index=False)  # noqa
    host = Column(ForeignKey("cdm.hosts.id"), comment="Host associated with making the observation, equivalent to OGC OMS 'host'", index=False)  # noqa
    observer = Column(ForeignKey("cdm.observers.id"), comment="Observer associated with making the observation, equivalent to OGC OMS 'observer'", index=False)  # noqa
    observed_property = Column(ForeignKey("cdm.observed_property.id"), comment="The phenomenon, or thing, being observed", index=True)  # noqa
    observing_procedure = Column(ForeignKey("cdm.observing_procedure.id"), comment="Procedure used to make the observation", index=False)  # noqa
    report_id = Column(String, comment="Parent report ID, used to link coincident observations together", index=False)  # noqa
    collection = Column(ForeignKey("cdm.collections.id"), comment="Primary collection or dataset that this observation belongs to", index=True)  # noqa
    parameter = Column(JSONB, comment="List of key/ value pairs in JSONB", index=False)  # noqa
    feature_of_interest = Column(ForeignKey("cdm.features.id"), comment="Feature that this observation is associated with", index=False)  # noqa
    version = Column(Integer, comment="Version number of this record", index=False)  # noqa
    change_date = Column(DateTime(timezone=True), comment="Date this record was changed", index=False)  # noqa
    user = Column(ForeignKey("cdm.users.id"), comment="Which user last modified this record", index=False)  # noqa
    status = Column(ForeignKey("cdm.record_status.id"), comment="Whether this is the latest version or an archived version of the record", index=False)  # noqa
    comments = Column(String, comment="Free text comments on this record, for example description of changes made etc", index=False)  # noqa
    source = Column(ForeignKey("cdm.source.id"), comment="The source of this record", index=True)  # noqa


class Collections(Base):
    __tablename__ = "collections"
    __table_args__ = {'schema': 'cdm'}
    id = Column(String, comment="ID / primary key", primary_key=True, index=False)  # noqa
    name = Column(String, comment="Name of collection", index=False)
    link = Column(String, comment="Link to further information on collection", index=False)  # noqa


class Features(Base):
    __tablename__ = "features"
    __table_args__ = {'schema': 'cdm'}
    id = Column(String, comment="ID / primary key", primary_key=True, index=False)  # noqa
    type = Column(ForeignKey("cdm.feature_type.id"), comment="enumerated feature type", index=False)  # noqa
    geometry = Column(Geography, comment="", index=False)
    elevation = Column(Numeric, comment="Elevation of feature above mean sea level", index=False)  # noqa
    parent = Column(ForeignKey("cdm.features.id"), comment="Parent feature for this feature if nested", index=False)  # noqa
    name = Column(String, comment="Name of feature", index=False)
    description = Column(String, comment="Description of feature", index=False)  # noqa
    link = Column(String, comment="Link to further information on feature", index=False)  # noqa


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'cdm'}
    id = Column(String, comment="ID / primary key", primary_key=True, index=False)  # noqa
    name = Column(String, comment="Name of user", index=False)


class Source(Base):
    __tablename__ = "source"
    __table_args__ = {'schema': 'cdm'}
    id = Column(String, comment="ID / primary key", primary_key=True, index=False)  # noqa
    name = Column(String, comment="Name of source", index=False)
    link = Column(String, comment="Link to further information on source", index=False)  # noqa

