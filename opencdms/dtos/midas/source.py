import datetime
import enum

from pydantic import BaseModel, conint, constr, condecimal
from typing import Optional, Union
from decimal import Decimal

field_mapping = {
    "src_id": "station_id",
    "src_name": "name",
    "high_prcn_lat": "latitude",
    "high_prcn_lon": "longitude",
    "src_bgn_date": "start_datetime",
    "src_end_date": "end_datetime"
}


class GridRefType(str, enum.Enum):
    CI: str = "CI"
    IRL: str = "IRL"
    OS: str = "OS"
    XX: str = "XX"
    ROI: str = "ROI"


class Source(BaseModel):
    src_id: Optional[conint(gt=0)]
    src_name: Optional[str]
    high_prcn_lat: Optional[
        condecimal(ge=Decimal("-90.0000"), le=Decimal("90"))
    ]
    high_prcn_lon: Optional[
        condecimal(gt=Decimal("-179.9999"), le=Decimal("180"))
    ]
    loc_geog_area_id: Optional[str]
    src_bgn_date: Optional[Union[datetime.date, str]]
    rec_st_ind: Optional[conint(ge=1001)]
    src_type: Optional[constr(max_length=15)]
    grid_ref_type: Optional[GridRefType]
    src_end_date: Optional[Union[datetime.date, str]]
    elevation: Optional[float]
    wmo_region_code: Optional[int]
    zone_time: Optional[int]
    drainage_stream_id: Optional[str]
    src_upd_date: Optional[Union[datetime.date, str]]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = field_mapping


class CreateSource(BaseModel):
    src_id: conint(gt=0)
    src_name: str
    high_prcn_lat: condecimal(ge=Decimal("-90.0000"), le=Decimal("90"))
    high_prcn_lon: condecimal(gt=Decimal("-179.9999"), le=Decimal("180"))
    src_bgn_date: Optional[Union[datetime.date, str]]
    src_end_date: Optional[Union[datetime.date, str]]
    elevation: float
    loc_geog_area_id: str
    rec_st_ind: Optional[conint(ge=1001)]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = field_mapping


class UpdateSource(BaseModel):
    src_name: Optional[str]
    high_prcn_lat: Optional[
        condecimal(ge=Decimal("-90.0000"), le=Decimal("90"))
    ]
    high_prcn_lon: Optional[
        condecimal(gt=Decimal("-179.9999"), le=Decimal("180"))
    ]
    src_bgn_date: Optional[Union[datetime.date, str]]
    src_end_date: Optional[Union[datetime.date, str]]
    elevation: Optional[float]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = field_mapping


class UniqueId(BaseModel):
    src_id: conint(gt=0)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = field_mapping
