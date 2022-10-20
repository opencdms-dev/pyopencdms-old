import datetime
from typing import Optional
from pydantic import BaseModel, constr
from opencdms.dtos.surface.wx_station import WxStation


field_mapping = {"datetime_": "datetime"}


class CreateRawData(BaseModel):
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    datetime_: datetime.datetime
    measured: float
    consisted: Optional[float]
    qc_range_description: Optional[constr(max_length=256)]
    qc_step_description: Optional[constr(max_length=256)]
    qc_persist_description: Optional[constr(max_length=256)]
    manual_flag: Optional[int]
    qc_persist_quality_flag: Optional[int]
    qc_range_quality_flag: Optional[int]
    qc_step_quality_flag: Optional[int]
    quality_flag: int
    station_id: int
    variable_id: int
    observation_flag_id: Optional[int]
    is_daily: Optional[bool]
    remarks: Optional[constr(max_length=150)]
    observer: Optional[constr(max_length=150)]
    code: constr(max_length=60)
    ml_flag: Optional[int]


class UpdateRawData(BaseModel):
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    datetime_: Optional[datetime.datetime]
    measured: Optional[float]
    consisted: Optional[float]
    qc_range_description: Optional[constr(max_length=256)]
    qc_step_description: Optional[constr(max_length=256)]
    qc_persist_description: Optional[constr(max_length=256)]
    manual_flag: Optional[int]
    qc_persist_quality_flag: Optional[int]
    qc_range_quality_flag: Optional[int]
    qc_step_quality_flag: Optional[int]
    quality_flag: Optional[int]
    station_id: Optional[int]
    variable_id: Optional[int]
    observation_flag_id: Optional[int]
    is_daily: Optional[bool]
    remarks: Optional[constr(max_length=150)]
    observer: Optional[constr(max_length=150)]
    code: Optional[constr(max_length=60)]
    ml_flag: Optional[int]


class RawData(CreateRawData):
    station: WxStation

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = field_mapping
