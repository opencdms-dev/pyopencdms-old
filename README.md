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


### How to use `pyopencdms`

After installing `pyopencdms`, `opencdms` will be available.
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


