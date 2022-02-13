from opencdms.dtos.mch import station as mch_station
from opencdms.dtos.opencdms import station_schema as opencdms_station
from tests.unit.dtos import data
import json
from decimal import Decimal


def test_can_convert_common_station_to_mch_station():
    opencdms_stn = opencdms_station.Station(**data.station_data)
    mch_stn = mch_station.Station(**data.station_data)

    assert opencdms_stn.dict() != mch_stn.dict()


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

    output_schema = mch_station.Station(
        Station='3450',
        StationName='Test station',
        StationName2='Alt test station',
        TimeZone='0',
        Longitud=Decimal('128.454'),
        Latitud=Decimal('67.111')
    )

    output_json = json.dumps(output_schema.dict(), default=str)
    output_dict = json.loads(output_json)
    assert mch_station.Station(**input_dict) == output_schema

    for k, v in mch_station.field_mapping.items():
        assert k in output_dict and v in input_dict
