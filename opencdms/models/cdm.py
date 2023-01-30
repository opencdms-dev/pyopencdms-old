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
import abc
from dataclasses import dataclass, field
from datetime import datetime
from typing import NewType, Optional


Geography = NewType("Geography", str)


class OpenCDMSBase(abc.ABC):
    """
    Base class for OpenCDMS domain models.

    """
    def table_info(self) -> str:
        """ Return table comment """
        return self._comment

    def column_info(self, column: str) -> str:
        """ Return column information """
        return self._comments.get(column)


@dataclass(kw_only=True)
class ObservationType(OpenCDMSBase):
    name: str
    description: str
    link: str = field(default=None)
    id: int = field(default=None)
    _comments = {
        "id": "ID / primary key",
        "name": "Short name for observation type",
        "description": "Description of observation type",
        "link": "Link to definition of observation type",
    }
    _comment = ""

@dataclass(kw_only=True)
class FeatureType(OpenCDMSBase):
    name: str
    description: str
    link: str = field(default=None)
    id: int = field(default=None)
    _comments = {
        "id": "ID / primary key",
        "name": "Short name for feature type",
        "description": "Description of feature type",
        "link": "Link to definition of feature type",
    }
    _comment = ""



@dataclass(kw_only=True)
class User(OpenCDMSBase):
    name: str
    id: str = field(default=None)
    _comments = {
        "id": "ID / primary key",
        "name": "Name of user",
    }
    _comment = "Placeholder table"


@dataclass(kw_only=True)
class ObservedProperty(OpenCDMSBase):
    short_name: str
    units: str
    description: str
    standard_name: str = field(default=None)
    link: str = field(default=None)
    id: int = field(default=None)
    _comments = {
        "id": "ID / primary key",
        "short_name": "Short name representation of observed property, e.g. 'at'",
        "standard_name": "CF standard name (if applicable), e.g. 'air_temperature'",
        "units": "Canonical units, e.g. 'Kelvin'",
        "description": "Description of observed property",
        "link": "Link to definition / source of observed property",
    }
    _comment = ""


@dataclass(kw_only=True)
class ObservingProcedure(OpenCDMSBase):
    name: str
    description: str
    id: int = field(default=None)
    link: str = field(default=None)
    _comments = {
        "id": "ID / primary key",
        "name": "Name of observing procedure",
        "description": "Description of observing procedure",
        "link": "Link to further information",
    }
    _comment = ""


@dataclass(kw_only=True)
class RecordStatus(OpenCDMSBase):
    name: str
    description: str
    id: int = field(default=None)
    _comments = {
        "id": "ID / primary key",
        "name": "Short name for status",
        "description": "Description of the status",
    }
    _comment = ""


@dataclass(kw_only=True)
class Host(OpenCDMSBase):
    id: str
    name: str
    version: int
    change_date: datetime
    user_id: int
    status_id: int
    comments: str
    id: int = field(default=None)
    description: str = field(default=None)
    link: str = field(default=None)
    location: Geography  = field(default=None)
    elevation: float = field(default=None)
    wigos_station_identifier: str = field(default=None)
    facility_type: str = field(default=None)
    date_established: str = field(default=None)
    wmo_region: str = field(default=None)
    territory: str = field(default=None)
    valid_from: datetime = field(default=None)
    valid_to: datetime = field(default=None)
    _comments = {
        "id": "ID / primary key",
        "name": "Preferred name of host",
        "description": "Description of host",
        "link": "URI to host, e.g. to OSCAR/Surface",
        "location": "Location of station",
        "elevation": "Elevation of station above mean sea level",
        "wigos_station_identifier": "WIGOS station identifier",
        "facility_type": "Type of observing facility, fixed land, mobile sea, etc",
        "date_established": "Date host was first established",
        "wmo_region": "WMO region in which the host is located",
        "territory": "Territory the host is located in",
        "valid_from": "Date from which the details for this record are valid",
        "valid_to": "Date after which the details for this record are no longer valid",
        "version": "Version number of this record",
        "change_date": "Date this record was changed",
        "user_id": "Which user last modified this record",
        "status_id": "Whether this is the latest version or an archived version of the record",
        "comments": "Free text comments on this record, for example description of changes made etc"
    }
    _comment = ""


@dataclass(kw_only=True)
class Observer(OpenCDMSBase):
    name: str
    description: str
    link: str = field(default=None)
    location: Geography = field(default=None)
    elevation: float = field(default=None)
    id: int = field(default=None)
    _comments = {
        "id": "ID / primary key",
        "name": "Name of sensor",
        "description": "Description of sensor",
        "link": "Link to further information",
        "location": "Location of observer",
        "elevation": "Elevation of observer above mean sea level"
    }
    _comment = ""


@dataclass(kw_only=True)
class Collection(OpenCDMSBase):
    name: str
    link: str = field(default=True)
    id: int = field(default=None)
    _comments = {
        "id": "ID / primary key",
        "name": "Name of collection",
        "link": "Link to further information on collection"
    }
    _comment = ""


@dataclass(kw_only=True)
class Feature(OpenCDMSBase):
    type_id: int
    geometry: Geography
    elevation: float = field(default=None)
    parent_id: int = field(default=None)
    name: str = field(default=None)
    description: str = field(default=None)
    link: str = field(default=None)
    id: int = field(default=None)
    _comments = {
        "id": "ID / primary key",
        "type_id": "enumerated feature type",
        "geometry": "",
        "elevation": "Elevation of feature above mean sea level",
        "parent_id": "Parent feature for this feature if nested",
        "name": "Name of feature",
        "description": "Description of feature",
        "link": "Link to further information on feature"
    }
    _comment = "table to contain definition of different geographic features"


@dataclass(kw_only=True)
class Source(OpenCDMSBase):
    name: str
    link: str = field(default=None)
    id: int = field(default=None)
    _comments = {
        "id": "ID / primary key",
        "name": "Name of source",
        "link": "Link to further information on source"
    }
    _comment = ""


@dataclass(kw_only=True)
class Observation(OpenCDMSBase):
    location: Geography
    version: int
    change_date: datetime
    user_id: int
    status_id: int
    comments: str
    source_id: int
    phenomenon_end: datetime
    result_value: float
    observed_property_id: int
    parameter: dict = field(default=None)
    id: int = field(default=None)
    elevation: float = field(default=None)
    observation_type_id: int = field(default=None)
    phenomenon_start: datetime = field(default=None)
    result_uom: str = field(default=None)
    result_description: str = field(default=None)
    result_quality: Optional[dict]
    result_time: datetime = field(default=None)
    valid_from: datetime = field(default=None)
    valid_to: datetime = field(default=None)
    host_id: str = field(default=None)
    observer_id: str = field(default=None)
    observing_procedure_id: int = field(default=None)
    report_id: str = field(default=None)
    collection_id: str = field(default=None)
    feature_of_interest_id: str = field(default=None)
    
    _comments = {
        "id": "ID / primary key",
        "location": "Location of observation",
        "elevation": "Elevation of observation above mean sea level",
        "observation_type_id": "Type of observation",
        "phenomenon_start": "Start time of the phenomenon being observed or observing period, if missing assumed instantaneous with time given by phenomenon_end",
        "phenomenon_end": "End time of the phenomenon being observed or observing period",
        "result_value": "The value of the result in float representation",
        "result_uom": "Units used to represent the value being observed",
        "result_description": "str representation of the result if applicable",
        "result_quality": "JSON representation of the result quality, key / value pairs",
        "result_time": "Time that the result became available",
        "valid_from": "Time that the result starts to be valid",
        "valid_to": "Time after which the result is no longer valid",
        "host_id": "Host associated with making the observation, equivalent to OGC OMS 'host'",
        "observer_id": "Observer associated with making the observation, equivalent to OGC OMS 'observer'",
        "observed_property_id": "The phenomenon, or thing, being observed",
        "observing_procedure_id": "Procedure used to make the observation",
        "report_id": "Parent report ID, used to link coincident observations together",
        "collection_id": "Primary collection or dataset that this observation belongs to",
        "parameter": "List of key/ value pairs in dict",
        "feature_of_interest_id": "Feature that this observation is associated with",
        "version": "Version number of this record",
        "change_date": "Date this record was changed",
        "user_id": "Which user last modified this record",
        "status_id": "Whether this is the latest version or an archived version of the record",
        "comments": "Free text comments on this record, for example description of changes made etc",
        "source_id": "The source of this record"
    }
    _comment = "table to store observations"
