from opencdms.dtos.midas import source as midas_station
from opencdms.dtos.opencdms import station_schema as opencdms_station
from tests.unit.dtos import data
import json
from decimal import Decimal
import datetime


def test_can_convert_common_station_to_midas_station():
    opencdms_stn = opencdms_station.Station(**data.station_data)
    midas_stn = midas_station.Source(**data.station_data)

    assert opencdms_stn.dict() != midas_stn.dict()


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

    output_schema = midas_station.Source(
        src_id=3450,
        src_name='Test station',
        high_prcn_lat=Decimal('67.111'),
        high_prcn_lon=Decimal('128.454'),
        loc_geog_area_id='SHEL',
        src_bgn_date=datetime.date(2019, 1, 1),
        rec_st_ind=1234,
        src_type=None,
        grid_ref_type=None,
        src_end_date=datetime.date(2056, 12, 31),
        elevation=30.0,
        wmo_region_code=None,
        zone_time=None,
        drainage_stream_id=None,
        src_upd_date=None
    )

    output_json = json.dumps(output_schema.dict(), default=str)
    output_dict = json.loads(output_json)
    assert midas_station.Source(**input_dict) == output_schema

    for k, v in midas_station.field_mapping.items():
        assert k in output_dict and v in input_dict
