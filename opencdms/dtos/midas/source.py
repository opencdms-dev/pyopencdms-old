import enum

from pydantic import BaseModel, conint, constr, condecimal
from typing import Optional
from decimal import Decimal


class GridRefType(str, enum.Enum):
    CI: str = "CI"
    IRL: str = "IRL"
    OS: str = "OS"
    XX: str = "XX"
    ROI: str = "ROI"


class Source(BaseModel):
    src_id: conint(gt=0)
    src_name: str
    high_prcn_lat: condecimal(ge=Decimal("-90.0000"), le=Decimal("90"))
    high_prcn_lon: condecimal(gt=Decimal("-179.9999"), le=Decimal("180"))
    loc_geog_area_id: Optional[str]
    src_bgn_date: str
    rec_st_ind: Optional[conint(ge=1001)]
    src_type: Optional[constr(max_length=15)]
    grid_ref_type: Optional[GridRefType]
    src_end_date: str
    elevation: float
    wmo_region_code: Optional[int]
    zone_time: Optional[int]
    drainage_stream_id: Optional[str]
    src_upd_date: Optional[str]

    class Config:
        orm_mode = True
        fields = {
            "src_id": "station_id",
            "src_name": "name",
            "high_prcn_lat": "latitude",
            "high_prcn_lon": "longitude",
            "src_bgn_date": "start_datetime",
            "src_end_date": "end_datetime"
        }


class UniqueId(BaseModel):
    src_id: conint(gt=0)

