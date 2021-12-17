from opencdms.dtos.clide import station_schema as clide_station
from opencdms.dtos.opencdms import station_schema as opencdms_station
from tests.unit.dtos import data


def test_can_convert_common_station_to_clide_station():
    opencdms_stn = opencdms_station.Station(**data.station_data)
    clide_stn = clide_station.Station(**data.station_data)

    assert opencdms_stn.dict() != clide_stn.dict()

#
# def test_can_convert_clide_station_to_common_station():
#     assert False
