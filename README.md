OpenCDMS
========

[![](https://img.shields.io/pypi/v/opencdms.svg)](https://pypi.python.org/pypi/opencdms) [![Travis-CI Build](https://img.shields.io/travis/opencdms/pyopencdms.svg)](https://travis-ci.com/opencdms/pyopencdms) [![Documentation Status](https://readthedocs.org/projects/opencdms/badge/?version=latest)](https://opencdms.readthedocs.io/en/latest/?badge=latest) [![Updates](https://pyup.io/repos/github/opencdms/opencdms/shield.svg)](https://pyup.io/repos/github/opencdms/opencdms/)

## Example

### Create a virtual environment for OpenCDMS development

These instructions are for Debian/Ubuntu Linux. If you run into problems then
please raise a [new issue](https://github.com/opencdms/pyopencdms/issues/new).

```
# Navigate to a suitable home directory
cd ~

# Create a directory for the project
mkdir opencdms-dev
cd opencdms-dev

# Create a directory for git repositories
mkdir git
cd git

# Clone pyopencdms and opencdms-test-data
git clone https://github.com/opencdms/pyopencdms.git
git clone https://github.com/opencdms/opencdms-test-data.git
cd ..

# Create a virtual environment for installing Python dependencies
python3 -m venv opencdms-env

# Activate the virtual environment
. opencdms-env/bin/activate

# Manually add pandas dependency
pip3 install pandas

# Add `opencdms` to the virtual environment's python path
echo $HOME"/opencdms-dev/git/pyopencdms/" > lib/python3.7/site-packages/opencdms.pth

```

### Example python commands

```
import os
from pathlib import Path

from opencdms import MidasOpen

# Instead of using a database connection string, the MIDAS Open
# provider requires the root directory for the MIDAS Open data.
connection = os.path.join(
    Path.home(), 'opencdms-demo', 'git', 'opencdms-test-data')

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
