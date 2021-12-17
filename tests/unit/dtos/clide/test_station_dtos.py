import json

from opencdms.dtos.clide import station as clide_station
from opencdms.dtos.opencdms import station_schema as opencdms_station
from tests.unit.dtos import data

field_mapping = {v: k for k, v in clide_station.field_mapping.items()}


def test_can_convert_common_station_to_clide_station():
    opencdms_stn = opencdms_station.Station(**data.station_data)
    clide_stn = clide_station.Station(**data.station_data)

    assert opencdms_stn.dict() != clide_stn.dict()


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

    output_schema = clide_station.Station(
        id=3450,
        station_no='1SHFY45485HH',
        status_id=123,
        time_zone='0',
        region='UK',
        latitude=67.111,
        longitude=128.454,
        start_date='2019-01-01',
        end_date='2056-12-31',
        ht_elev=30.0
    )

    output_json = json.dumps(output_schema.dict(), default=str)
    output_dict = json.loads(output_json)
    assert clide_station.Station(**input_dict) == output_schema

    for k, v in clide_station.field_mapping.items():
        assert k in output_dict and v in input_dict
