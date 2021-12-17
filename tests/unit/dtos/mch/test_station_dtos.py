from opencdms.dtos.opencdms import station_schema as opencdms_station
from opencdms.dtos.mch import station_schema as mch_station
from tests.unit.dtos import data


def test_can_convert_common_station_to_mch_station():
    opencdms_stn = opencdms_station.Station(**data.station_data)
    mch_stn = mch_station.Station(**data.station_data)

    assert opencdms_stn.dict() != mch_stn.dict()

#
# def test_can_convert_mch_station_to_common_station():
#     assert False

