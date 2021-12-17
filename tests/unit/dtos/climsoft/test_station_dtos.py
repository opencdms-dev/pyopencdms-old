from opencdms.dtos.opencdms import station_schema as opencdms_station
from opencdms.dtos.climsoft import station_schema as climsoft_station
from tests.unit.dtos import data


def test_can_convert_common_station_to_climsoft_station():
    opencdms_stn = opencdms_station.Station(**data.station_data)
    climsoft_stn = climsoft_station.Station(**data.station_data)

    assert opencdms_stn.dict() != climsoft_stn.dict()

#
# def test_can_convert_climsoft_station_to_common_station():
#     assert False

