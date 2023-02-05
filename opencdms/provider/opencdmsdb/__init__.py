# =============================================================================
# MIT License
#
# Copyright (c) 2023, OpenCDMS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# =============================================================================
from geoalchemy2 import Geography
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Table
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import registry, relationship

from opencdms.models import cdm


mapper_registry = registry()


observation_type = Table(
    "observation_type",
    mapper_registry.metadata,
    Column("id", Integer, comment="ID / primary key", primary_key=True, index=False),
    Column("name", String, comment="Short name for observation type", index=False),
    Column("description", String, comment="Description of observation type", index=False),
    Column("link", String, comment="Link to definition of observation type", index=False),
    schema="cdm"
)


feature_type = Table(
    "feature_type",
    mapper_registry.metadata,
    Column("id", Integer, comment="ID / primary key", primary_key=True, index=False),
    Column("name", String, comment="Short name for feature type", index=False),
    Column("description", String, comment="Description of feature type", index=False),
    Column("link", String, comment="Link to definition of feature type", index=False),
    schema="cdm"
)


users = Table(
    "users",
    mapper_registry.metadata,
    Column("id", Integer, comment="ID / primary key", primary_key=True, index=False),
    Column("name", String, comment="Name of user", index=False),
    schema="cdm"
)


observed_property = Table(
    "observed_property",
    mapper_registry.metadata,
    Column("id", Integer, comment="ID / primary key", primary_key=True, index=False),
    Column("short_name", String, comment="Short name representation of observed property, e.g. 'at'", index=False),
    Column("standard_name", String, comment="CF standard name (if applicable), e.g. 'air_temperature'", index=False),
    Column("units", String, comment="Canonical units, e.g. 'Kelvin'", index=False),
    Column("description", String, comment="Description of observed property", index=False),
    Column("link", String, comment="Link to definition / source of observed property", index=False),
    schema="cdm"
)


observing_procedure = Table(
    "observing_procedure",
    mapper_registry.metadata,
    Column("id", Integer, comment="ID / primary key", primary_key=True, index=False),
    Column("name", String, comment="Name of observing procedure", index=False),
    Column("description", String, comment="Description of observing procedure", index=False),
    Column("link", String, comment="Link to further information", index=False),
    schema="cdm"
)


record_status = Table(
    "record_status",
    mapper_registry.metadata,
    Column("id", Integer, comment="ID / primary key", primary_key=True, index=False),
    Column("name", String, comment="Short name for status", index=False),
    Column("description", String, comment="Description of the status", index=False),
    schema="cdm"
)


hosts = Table(
    "hosts",
    mapper_registry.metadata,
    Column("id", String, comment="ID / primary key", primary_key=True, index=False),
    Column("name", String, comment="Preferred name of host", index=False),
    Column("description", String, comment="Description of host", index=False),
    Column("link", String, comment="URI to host, e.g. to OSCAR/Surface", index=False),
    Column("location", Geography, comment="Location of station", index=False),
    Column("elevation", Numeric, comment="Elevation of station above mean sea level", index=False),
    Column("wigos_station_identifier", String, comment="WIGOS station identifier", index=False),
    Column("facility_type", String, comment="Type of observing facility, fixed land, mobile sea, etc", index=False),
    Column("date_established", String, comment="Date host was first established", index=False),
    Column("wmo_region", String, comment="WMO region in which the host is located", index=False),
    Column("territory", String, comment="Territory the host is located in", index=False),
    Column("valid_from", DateTime(timezone=True), comment="Date from which the details for this record are valid", index=False),
    Column("valid_to", DateTime(timezone=True), comment="Date after which the details for this record are no longer valid", index=False),
    Column("version", Integer, comment="Version number of this record", index=False),
    Column("change_date", DateTime(timezone=True), comment="Date this record was changed", index=False),
    Column("user_id",ForeignKey("cdm.users.id"), comment="Which user last modified this record", index=False),
    Column("status_id",ForeignKey("cdm.record_status.id"), comment="Whether this is the latest version or an archived version of the record", index=False),
    Column("comments", String, comment="Free text comments on this record, for example description of changes made etc", index=False),
    schema="cdm"
)


observers = Table(
    "observers",
    mapper_registry.metadata,
    Column("id", String, comment="ID / primary key", primary_key=True, index=False),
    Column("name", String, comment="Name of sensor", index=False),
    Column("description", String, comment="Description of sensor", index=False),
    Column("link", String, comment="Link to further information", index=False),
    Column("location", Geography, comment="Location of observer", index=False),
    Column("elevation", Numeric, comment="Elevation of observer above mean sea level", index=False),
    schema="cdm"
)


collections = Table(
    "collections",
    mapper_registry.metadata,
    Column("id", String, comment="ID / primary key", primary_key=True, index=False),
    Column("name", String, comment="Name of collection", index=False),
    Column("link", String, comment="Link to further information on collection", index=False),
    schema="cdm"
)


features = Table(
    "features",
    mapper_registry.metadata,
    Column("id", String, comment="ID / primary key", primary_key=True, index=False),
    Column("type_id",ForeignKey("cdm.feature_type.id"), comment="enumerated feature type", index=False),
    Column("geometry", Geography, comment="", index=False),
    Column("elevation", Numeric, comment="Elevation of feature above mean sea level", index=False),
    Column("parent_id",ForeignKey("cdm.features.id"), comment="Parent feature for this feature if nested", index=False),
    Column("name", String, comment="Name of feature", index=False),
    Column("description", String, comment="Description of feature", index=False),
    Column("link", String, comment="Link to further information on feature", index=False),
    schema="cdm"
)


source = Table(
    "source",
    mapper_registry.metadata,
    Column("id", Integer, comment="ID / primary key", primary_key=True, autoincrement=True),
    Column("name", String, comment="Name of source", index=False),
    Column("link", String, comment="Link to further information on source", index=False),
    schema="cdm"
)


observations = Table(
    "observations",
    mapper_registry.metadata,
    Column("id", String, comment="ID / primary key", primary_key=True, index=False),
    Column("location", Geography, comment="Location of observation", index=True),
    Column("elevation", Numeric, comment="Elevation of observation above mean sea level", index=False),
    Column("observation_type_id",ForeignKey("cdm.observation_type.id"), comment="Type of observation", index=True),
    Column("phenomenon_start", DateTime(timezone=True), comment="Start time of the phenomenon being observed or observing period, if missing assumed instantaneous with time given by phenomenon_end", index=False),
    Column("phenomenon_end", DateTime(timezone=True), comment="End time of the phenomenon being observed or observing period", index=True),
    Column("result_value", Numeric, comment="The value of the result in float representation", index=False),
    Column("result_uom", String, comment="Units used to represent the value being observed", index=False),
    Column("result_description", String, comment="str representation of the result if applicable", index=False),
    Column("result_quality", JSONB, comment="JSON representation of the result quality, key / value pairs", index=False),
    Column("result_time", DateTime(timezone=True), comment="Time that the result became available", index=False),
    Column("valid_from", DateTime(timezone=True), comment="Time that the result starts to be valid", index=False),
    Column("valid_to", DateTime(timezone=True), comment="Time after which the result is no longer valid", index=False),
    Column("host_id",ForeignKey("cdm.hosts.id"), comment="Host associated with making the observation, equivalent to OGC OMS 'host'", index=False),
    Column("observer_id",ForeignKey("cdm.observers.id"), comment="Observer associated with making the observation, equivalent to OGC OMS 'observer'", index=False),
    Column("observed_property_id",ForeignKey("cdm.observed_property.id"), comment="The phenomenon, or thing, being observed", index=True),
    Column("observing_procedure_id",ForeignKey("cdm.observing_procedure.id"), comment="Procedure used to make the observation", index=False),
    Column("report_id", String, comment="Parent report ID, used to link coincident observations together", index=False),
    Column("collection_id",ForeignKey("cdm.collections.id"), comment="Primary collection or dataset that this observation belongs to", index=True),
    Column("parameter", JSONB, comment="List of key/ value pairs in dict", index=False),
    Column("feature_of_interest_id",ForeignKey("cdm.features.id"), comment="Feature that this observation is associated with", index=False),
    Column("version", Integer, comment="Version number of this record", index=False),
    Column("change_date", DateTime(timezone=True), comment="Date this record was changed", index=False),
    Column("user_id",ForeignKey("cdm.users.id"), comment="Which user last modified this record", index=False),
    Column("status_id",ForeignKey("cdm.record_status.id"), comment="Whether this is the latest version or an archived version of the record", index=False),
    Column("comments", String, comment="Free text comments on this record, for example description of changes made etc", index=False),
    Column("source_id",ForeignKey("cdm.source.id"), comment="The source of this record", index=True),
    schema="cdm"
)


def start_mappers():
    mapper_registry.map_imperatively(cdm.ObservationType, observation_type,properties = {
        "observations_": relationship("Observation",back_populates="observation_type_")
    })
    mapper_registry.map_imperatively(cdm.FeatureType, feature_type, properties = {
        "features_": relationship("Feature",back_populates="feature_type_")
    })
    mapper_registry.map_imperatively(cdm.User, users, properties = {
        "hosts_": relationship("Host",back_populates="users_"),
        "observations_": relationship("Observation", back_populates="user_")
    })
    mapper_registry.map_imperatively(cdm.ObservedProperty, observed_property, properties = {
        "observations_": relationship("Observation", back_populates="observed_property_")
    })
    mapper_registry.map_imperatively(cdm.ObservingProcedure, observing_procedure, properties={
        "observations_": relationship("Observation",back_populates="observing_procedure_")
    })
    mapper_registry.map_imperatively(cdm.RecordStatus, record_status, properties= {
        "hosts_": relationship("Host", back_populates="record_statuses_"),
        "observations_": relationship("Observation", back_populates="record_status_")
    })
    mapper_registry.map_imperatively(cdm.Host, hosts, properties = {
        "users_": relationship("User",back_populates="hosts_"),
        "record_statuses_": relationship("RecordStatus",back_populates="hosts_"),
        "observations_": relationship("Observation", back_populates="host_")
    })
    mapper_registry.map_imperatively(cdm.Observer, observers, properties = {
        "observations_": relationship("Observation", back_populates="observer_")
    })
    mapper_registry.map_imperatively(cdm.Collection, collections,properties={
        "observations_": relationship("Observation",back_populates="collection_")
    })
    mapper_registry.map_imperatively(cdm.Feature, features, properties = {
        "feature_type_": relationship("FeatureType",back_populates="features_", uselist=False),
        "parent_feature_": relationship("Feature",foreign_keys="Feature.parent_id" ),
        "observations_": relationship("Observation", back_populates="feature_")
    })
    mapper_registry.map_imperatively(cdm.Source, source, properties = {
        "observations_": relationship("Observation", back_populates="source_")
    })
    mapper_registry.map_imperatively(cdm.Observation, observations, properties = {
        "observation_type_": relationship("ObservationType",back_populates="observations_", uselist=False),
        "host_": relationship("Host",back_populates="observations_", uselist=False),
        "observer_": relationship("Observer",back_populates="observations_", uselist=False),
        "observed_property_": relationship("ObservedProperty",back_populates="observations_", uselist=False),
        "observing_procedure_": relationship("ObservingProcedure",back_populates="observations_", uselist=False),
        "collection_": relationship("Collection",back_populates="observations_", uselist=False),
        "feature_": relationship("Feature",back_populates="observations_", uselist=False),
        "user_": relationship("User",back_populates="observations_", uselist=False),
        "record_status_": relationship("RecordStatus",back_populates="observations_", uselist=False),
        "source_": relationship("Source",back_populates="observations_", uselist=False),
    })
