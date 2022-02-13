# =================================================================
#
# Authors: Ian Edwards
#
# Copyright (c) 2020, OpenCDMS Project
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

# NOTE: Currently this module only contains a provider for "MIDAS Open"


import os
import logging
from types import ModuleType
from opencdms.models.midas import core as midas_models
from opencdms.dtos import midas as midas_schemas

from .base import CDMSProvider
from ..fileformats.text import read_badc

LOGGER = logging.getLogger(__name__)


# MIDAS Open paths and filenames are of the form:
#     badc/ukmo-midas-open/data/
#     uk-daily-weather-obs/dataset-version-201908/
#     berkshire/00838_bracknell-beaufort-park/
#     qc-version-1/
#
#     midas-open_uk-daily-weather-obs_dv-201908_
#     berkshire_00838_bracknell-beaufort-park_qcv-1_1991.csv

DEFAULT_PATH = os.path.join("badc", "ukmo-midas-open", "data")
DEFAULT_DATASET_VERSION = "201908"
DEFAULT_QC_VERSION = 1


element_lookup = {
    "wind_speed": {"hourly": "uk-hourly-weather-obs"},
    "wind_direction": {"hourly": "uk-hourly-weather-obs"},
    'mean_wind_speed': {'hourly': 'uk-mean-wind-obs'},
    'mean_wind_dir': {'hourly': 'uk-mean-wind-obs'},
    'prcp_amt': {'hourly': 'uk-hourly-rain-obs', 'daily': 'uk-daily-rain-obs'},
    'max_air_temp': {'daily': 'uk-daily-temperature-obs'},
    'min_air_temp': {'daily': 'uk-daily-temperature-obs'},
    'glbl_irad_amt': {'daily': 'uk-radiation-obs'},
    'difu_irad_amt': {'daily': 'uk-radiation-obs'},
    'q5cm_soil_temp': {'daily': 'uk-soil-temperature-obs'},
    'q10cm_soil_temp': {'daily': 'uk-soil-temperature-obs'},
}
station_county_lookup = {
    838: "berkshire",
}
station_filename_lookup = {
    838: "00838_bracknell-beaufort-park",
}

date_time_column_lookup = {
    'uk-daily-rain-obs': 'ob_date',
    'uk-daily-temperature-obs': 'ob_end_time',
    'uk-daily-weather-obs': 'ob_end_time',
    'uk-hourly-rain-obs': 'ob_end_time',
    'uk-hourly-weather-obs': 'ob_time',
    'uk-mean-wind-obs': 'ob_end_time',
    'uk-radiation-obs': 'ob_end_time',
    'uk-soil-temperature-obs': 'ob_time'
}

valid_dataset_versions = ["201901", "201908"]
valid_qc_versions = [0, 1]


class MidasOpen(CDMSProvider):
    """Provider for MIDAS Open data"""

    def __init__(self, connection_string, *args, **kwargs):
        self.connection_string = connection_string

    def obs(self, src_id, elements, period, qc_version=None, **kwargs):
        """Return observatons as Pandas DataFrame

        Args:
            src_id (int): The ID of the required station
            elements (list): List of elements to return
            period (str): Either 'hourly' or 'daily'
            qc_version (int): 0 or 1

        Returns:
            DataFrame: Pandas DataFrame containing onservations data

        """
        if "year" not in kwargs.keys():
            raise ValueError(
               "NOTE: Currently you must supply a year, e.g. year=1991")

        year = kwargs["year"]

        for element in elements:
            if element not in element_lookup:
                raise ValueError('"{}" element not recognised'.format(element))

        qc_version = DEFAULT_QC_VERSION if qc_version is None else qc_version
        dataset_version = kwargs.get(
            "dataset_version", DEFAULT_DATASET_VERSION)

        if src_id not in station_county_lookup:
            raise ValueError("Station ID not recognised")

        if period not in element_lookup[element]:
            raise ValueError('"{} period not available for {} element'.format(
                period, element))

        if qc_version not in valid_qc_versions:
            raise ValueError(
                "qc_version must be one of: {}".format(
                    ", ".join(map(str, valid_qc_versions))
                )
            )

        if dataset_version not in valid_dataset_versions:
            raise ValueError(
                "dataset_version must be one of: {}".format(
                    ", ".join(valid_dataset_versions)
                )
            )

        station_county = station_county_lookup[src_id]
        station_filename = station_filename_lookup[src_id]

        # The following code should be moved to a get_path() method
        directory = os.path.join(
            DEFAULT_PATH,
            element_lookup[element][period],
            "dataset-version-{}".format(dataset_version),
            station_county,
            station_filename,
            "qc-version-{}".format(qc_version),
        )

        filename = "_".join(
            [
                "midas-open",
                element_lookup[element][period],
                "dv-{}".format(dataset_version),
                station_county,
                station_filename,
                "qcv-{}".format(qc_version),
                "{}.csv".format(year),
            ]
        )

        filepath = os.path.join(self.connection_string, directory, filename)

        return read_badc(filepath, usecols=[
            "src_id",
            date_time_column_lookup[element_lookup[element][period]],
            *elements
        ])


class MidasProvider(CDMSProvider):
    def __init__(
        self,
        models: ModuleType = midas_models,
        schemas: ModuleType = midas_schemas
    ):
        super().__init__(models, schemas)
