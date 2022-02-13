OpenCDMS Python library: `pyopencdms`
====================================
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

[![](https://img.shields.io/pypi/v/opencdms.svg)](https://pypi.python.org/pypi/opencdms) [![Travis-CI Build](https://img.shields.io/travis/opencdms/pyopencdms.svg)](https://travis-ci.com/opencdms/pyopencdms) [![Documentation Status](https://readthedocs.org/projects/opencdms/badge/?version=latest)](https://opencdms.readthedocs.io/en/latest/?badge=latest) [![Updates](https://pyup.io/repos/github/opencdms/opencdms/shield.svg)](https://pyup.io/repos/github/opencdms/opencdms/)

## Overview

A Climate Data Management System (CDMS) is an integrated computer-based system that facilitates the effective archival, management, analysis, delivery and utilization of a wide range of integrated climate data ([WMO 2014](https://library.wmo.int/index.php?lvl=notice_display&id=16300)).

`pyopencdms` aims to build a common Python API supporting multiple Climate Data Management Systems (CDMS) that use different underlying database engines.

The image below shows the [CliDE](http://www.bom.gov.au/climate/pacific/about-clide.shtml), [Climsoft](https://climsoft.org/), [MCH](https://community.wmo.int/mch-meteorology-climatology-and-hydrology-database-management-system), [MIDAS](https://catalogue.ceda.ac.uk/uuid/dbd451271eb04662beade68da43546e1) and other CDMSs being accessed through a single common API.

In addition we will add support for the [WIGOS Meta Data Representation (WMDR)](https://github.com/wmo-im/wmdr) and collaborate with experts to create a new "CDMS Data Model Representation" that will support addional capabilities that are beyond the scope of WMDR.

![OpenCDMS data layer](https://raw.githubusercontent.com/opencdms/media/main/architecture/opencdms-data-layer-1.0.png)

The [opencdms-test-data](https://github.com/opencdms/opencdms-test-data) repository will be used as a source of test data for development to ensure interoperability between systems works as intended.

## Dependencies

`pyopencdms` officially supports Python 3.7.1 and above, 3.8, and 3.9 (in line with the [Pandas package](https://pandas.pydata.org/docs/getting_started/install.html#python-version-support))

<img src="https://raw.githubusercontent.com/opencdms/media/main/architecture/pyopencdms-architecture-0.2.png" width="400" />

`pyopencdms` uses SQLAlchemy (2.0-style) to connect to multiple database technologies including PostgreSQL, MySQL/MariaDB, Oracle and SQLite.

It is expected that SQLAlchemy objects, Panda's [DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and JSON will be key data types for exchanging data.

<!-- Geospatial dependencies like [PostGIS](http://postgis.net/), [GeoAlchemy2](https://github.com/geoalchemy/geoalchemy2) and [SpatiaLite](https://en.wikipedia.org/wiki/SpatiaLite) may be introduced in the future if required. -->

## Example

- Create a virtual environment for OpenCDMS development
- Install dependencies used by `pyopencdms`
- Clone a copy of the `opencdms-test-data` repository

### Example python commands

> NOTE: The example below is old and will be updated by the end of 2021.

```
import os
from pathlib import Path

from opencdms import MidasOpen

# Instead of using a database connection string, the MIDAS Open
# provider requires the root directory for the MIDAS Open data.
connection = os.path.join(
    Path.home(), 'opencdms-dev', 'git', 'opencdms-test-data')

# All instances of CDMS Providers act as an active session
session = MidasOpen(connection)

filters = {
    'src_id': 838,
    'period': 'hourly',
    'year': 1991,
    'elements': ['wind_speed', 'wind_direction'],
}

# Get observations using filters
obs = session.obs(**filters)

# Save observations to CSV file
obs.to_csv('example_observations.csv')

```

<!--
  * Free software: MIT license
  * Documentation: https://opencdms.readthedocs.io.

  Features
  --------
  * TODO
-->

### Naming Convention
#### Data Transfer Object (DTO) naming convention

DTOs reside in opencdms.dtos.{lower_case_provider_name}.{lower_case_model_name}.py files.

Unique ID schema of any model should be in the respective schema file and named `UniqueId`

Create and Update schema should be in the respective schema file and named:
- Create{model_name_in_models_opencdms.models_module}
- Update{model_name_in_models_opencdms.models_module}
- For DTO used representing original row in database should be named as same as the model name in opencdms.models module.

### How to use `pyopencdms`

After installing `pyopencdms` the `opencdms` Python package will be available to import.

Currently, `opencdms` package has 5 providers:
 - mch
 - midas
 - climsoft
 - clide
 - opencdms

##### `mch` Provider
You can manipulate `opencdms.models.mch.english` models using `mch` provider.
Here are some examples:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from opencdms.utils.db import get_mch_english_connection_string
from opencdms.provider.mch import MCHProvider

db_url = get_mch_english_connection_string()
db_engine = create_engine(db_url)
station_data = dict(
    Station="TEST",
    StationName="Test Station"
)

SessionLocal = sessionmaker(bind=db_engine)
db_session = SessionLocal()
mch_provider = MCHProvider()

# create station
station = mch_provider.create(db_session, "Station", station_data)

# get list of stations
stations = mch_provider.list(db_session, "Station")

# get a single station
station = mch_provider.get(
    db_session,
    "Station",
    {"Station": station_data["Station"]}
)

# update a station
mch_provider.update(
    db_session,
    "Station",
    {"Station": station_data["Station"]},
    {'StationName': 'Updated Station Name'}
)

# delete a station
deleted = mch_provider.delete(
    db_session,
    "Station",
    {"Station": station_data["Station"]}
)
```

Similarly, we can use all other providers except `opencdms` provider.
Here is an example of opencdms provider

```python
from opencdms.provider.opencdms import OpenCDMSProvider, ProviderConfig
from tests.unit.dtos.data import station_data

# We are instantiating OpenCDMSProvider where we have enabled clide provider
provider = OpenCDMSProvider(ProviderConfig(enable_clide=True))

# create station
station = provider.create("Station", station_data)

# get a single station
station = provider.get("Station", {"id": station_data["id"]})

# get a list of stations
stations = provider.list("Station")

# update a station
provider.update(
    "Station",
    {"id": station_data["id"]},
    {'region': 'US'}
)

# delete a station
provider.delete(
    "Station",
    {"id": station_data['id']}
)
```

The code above will only manipulate clide models. Notice that, we have not explicitly
defined db session. It will be done automatically in OpenCDMSProvider.


Let us look at an example where multiple provider is enables.

```python
from sqlalchemy import create_engine
from opencdms.dtos.clide import station as clide_station
from opencdms.dtos.clide import stationstatu as clide_station_status
from opencdms.dtos.clide import stationtimezone as clide_station_timezone
from opencdms.dtos.mch import station as mch_station
from opencdms.models import clide
from opencdms.models.mch import english as mch
from opencdms.provider.opencdms import OpenCDMSProvider, ProviderConfig
from opencdms.utils.db import get_clide_connection_string, \
    get_mch_english_connection_string


timezone_data = dict(
    id=1,
    tm_zone="UTC",
    utc_diff=0,
    description="UTC timezone"
)

station_status_data = dict(
    id=1,
    status="ACTIVE",
    description="test station status 1"
)

station_data = {
    "station_id": 3450,
    "station_no": "1SHFY45485HH",
    "name": "Test station",
    "secondary_name": "Alt test station",
    "latitude": 67.111,
    "longitude": 128.454,
    "elevation": 30,
    "region": "UK",
    "start_datetime": "2019-01-01",
    "end_datetime": "2056-12-31",
    "status_id": 1,
    "timezone": "UTC",
    "country": "England",
    "loc_geog_area_id": "SHEL",
    "rec_st_ind": 1234
}

CLIDE_DB_URL = get_clide_connection_string()
clide_db_engine = create_engine(CLIDE_DB_URL)

MCH_DB_URL = get_mch_english_connection_string()
mch_db_engine = create_engine(MCH_DB_URL)

mch.Base.metadata.create_all(bind=mch_db_engine)
clide.Base.metadata.create_all(bind=clide_db_engine)

provider = OpenCDMSProvider(
    ProviderConfig(enable_mch=True, enable_clide=True)
)

station_status = provider.create("StationStatu", station_status_data)
assert isinstance(
    station_status["clide"],
    clide_station_status.StationStatu
)

timezone = provider.create("StationTimezone", timezone_data)
assert isinstance(
    timezone["clide"],
    clide_station_timezone.StationTimezone
)

station_data["timezone"] = timezone["clide"].tm_zone
station_data["status_id"] = station_status["clide"].id

station = provider.create("Station", station_data)
assert isinstance(station["clide"], clide_station.Station)
assert isinstance(station["mch"], mch_station.Station)

station = provider.get(
    "Station",
    {
        "station_id": station_data["station_id"]
    }
)
assert isinstance(station["clide"], clide_station.Station)
assert isinstance(station["mch"], mch_station.Station)

stations = provider.list("Station")
for station in stations["clide"]:
    assert isinstance(station, clide_station.Station)
for station in stations["mch"]:
    assert isinstance(station, mch_station.Station)

station = provider.update(
    "Station",
    {
        "station_id": station_data["station_id"]
    },
    {
        'region': 'US',
        "station_no": station_data["station_no"],
        "timezone": station_data["timezone"],
        "status_id": station_data["status_id"],
        "name": "Test station",
        "secondary_name": "Alt test station",
        "latitude": 67.111,
        "longitude": 128.454,
    }
)

assert station["clide"].region == 'US'
assert station["mch"].TimeZone == '0'

deleted = provider.delete(
    "Station",
    {
        "station_id": station_data["station_id"]
    }
)
assert deleted["clide"]["station_id"] == station_data['station_id']
assert deleted["mch"]["station_id"] == station_data['station_id']
```

Here we have declared some variables for later use. Then we migrated the database
and created an `OpenCDMSProvider` with `mch` and `clide` provider enabled.
Now, we want to create a station in both of `mch` and `clide`. Clide has some
constraint checks before you can create a station. So, we need a `station_status_id`
and `timezone`. So, we create those first. When we execute this line

```python
station_status = provider.create("StationStatu", station_status_data)
```
and then print `station_status`, we get,
```python
{'clide': StationStatu(id=1, status='ACTIVE', description='test station status 1'), 'climsoft': None, 'mch': AttributeError("module 'opencdms.models.mch.english' has no attribute 'StationStatu'"), 'midas': None}
```
Notice that, for clide `station_status` was created and for mch it threw an error. It's expected
because mch doesn't have `station_status`.

Then we go ahead and create timezone for clide station and create station.

As, `station` is both in `mch` and `clide`, for both of them it will be created.

```python
station = provider.create("Station", station_data)
```
Now, if we print station, we will see that for both of `mch` and `clide`, station was created.
```python
print(station)
{'clide': Station(id=3450, station_no='1SHFY45485HH', status_id=1, time_zone='UTC', region='UK', latitude=None, longitude=None, start_date=None, end_date=None, ht_elev=None), 'climsoft': None, 'mch': Station(Station='3450', StationName='Test station', StationName2=None, TimeZone=None, Longitud=None, Latitud=None), 'midas': None}
```

When we want to get a single station, we do the following:

```python

station = provider.get(
    "Station",
    {
        "station_id": station_data["station_id"]
    }
)
```
Here, we have passed a dict for `unique_id`. This dict should contain all the
attribute name and value that are required by each provider that you have enabled.

Such as, for `clide` only `id` is required and for `mch` only `Station` is required.
But in the field mapping (opencdms/dtos/clide/station.py::field_mapping and opencdms/dtos/mch/station.py::field_mapping)
for both of clide and mch, the field name is `station_id`. So, we only passed this
key with value.

If we passed `
    {
        "station_id": station_data["station_id"],
        "another_ky": "random_value"
    }`
the opencdms provider would automatically parse the necessary field and discard
everything else.

So, when we instantiate a provider and perform an operation and pass some data to use in that operation,
`opencdms` only takes the data that are required by each enabled provider, perform the
operation and returns a response in the form:

```python
{
    "clide": "a model or list of model/error/None",
    "mch": "a model or list of model/error/None",
    "midas": "a model or list of model/error/None",
    "climsoft": "a model or list of model/error/None"
}
```
