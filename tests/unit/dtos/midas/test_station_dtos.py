from opencdms.dtos.opencdms import station_schema as opencdms_station
from opencdms.dtos.midas import source_schema as midas_station
from tests.unit.dtos import data


def test_can_convert_common_station_to_midas_station():
    opencdms_stn = opencdms_station.Station(**data.station_data)
    midas_stn = midas_station.Source(**data.station_data)

    assert opencdms_stn.dict() != midas_stn.dict()


# def test_can_convert_midas_station_to_common_station():
#     assert False


