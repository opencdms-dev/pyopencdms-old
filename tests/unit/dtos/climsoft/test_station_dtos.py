from opencdms.dtos.climsoft import station as climsoft_station
from opencdms.dtos.opencdms import station_schema as opencdms_station
from tests.unit.dtos import data
import json


def test_can_convert_common_station_to_climsoft_station():
    opencdms_stn = opencdms_station.Station(**data.station_data)
    climsoft_stn = climsoft_station.Station(**data.station_data)

    assert opencdms_stn.dict() != climsoft_stn.dict()


def test_json_to_pydantic_should_match():
    input_dict = {
        'station_id': 3450,
        'station_no': '1SHFY45485HH',
        'name': 'Test station',
        'secondary_name': 'Alt test station',
        'latitude': 67.111,
        'longitude': 128.454,
        'elevation': 30,
        'region': 'UK',
        'start_datetime': '2019-01-01',
        'end_datetime': '2056-12-31',
        'status_id': 123,
        'timezone': 0,
        'country': 'England',
        'loc_geog_area_id': 'SHEL',
        'rec_st_ind': 1234
    }

    output_schema = climsoft_station.Station(
        stationId='3450',
        stationName='Test station',
        country='England',
        adminRegion='UK',
        latitude=67.111,
        longitude=128.454,
        elevation=30.0,
        openingDatetime='2019-01-01',
        closingDatetime='2056-12-31'
    )

    output_json = json.dumps(output_schema.dict(), default=str)
    output_dict = json.loads(output_json)
    assert climsoft_station.Station(**input_dict) == output_schema

    for k, v in climsoft_station.field_mapping.items():
        assert k in output_dict and v in input_dict
