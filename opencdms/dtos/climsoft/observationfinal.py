import datetime

from pydantic import BaseModel
from typing import Optional, List, Dict
from opencdms.dtos.climsoft.station import Station


field_mapping = {
    "recordedFrom": "recorded_from",
    "describedBy": "described_by",
    "obsDatetime": "obs_datetime",
    "obsLevel": "obs_level",
    "obsValue": "obs_value",
    "qcStatus": "qc_status",
    "qcTypeLog": "qc_type_log",
    "acquisitionType": "acquisition_type",
    "dataForm": "data_form",
    "capturedBy": "captured_by",
    "temperatureUnits": "temperature_units",
    "precipitationUnits": "precipitation_units",
    "cloudHeightUnits": "cloud_height_units",
    "visUnits": "vis_units",
    "dataSourceTimeZone": "data_source_timezone",
}


class Observationfinal(BaseModel):
    recordedFrom: str
    describedBy: Optional[int]
    obsDatetime: Optional[datetime.datetime]
    obsLevel: Optional[str]
    obsValue: Optional[float]
    flag: Optional[str]
    period: Optional[int]
    qcStatus: Optional[int]
    qcTypeLog: Optional[str]
    acquisitionType: Optional[int]
    dataForm: Optional[str]
    capturedBy: Optional[str]
    mark: Optional[int]
    temperatureUnits: Optional[str]
    precipitationUnits: Optional[str]
    cloudHeightUnits: Optional[str]
    visUnits: Optional[str]
    dataSourceTimeZone: Optional[int]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = field_mapping


class ObservationfinalWithStation(Observationfinal):

    station: Optional[Station]


class CreateObservationfinal(BaseModel):
    recordedFrom: str
    describedBy: int
    obsDatetime: datetime.datetime
    obsLevel: Optional[str]
    obsValue: Optional[float]
    flag: Optional[str]
    period: Optional[int]
    qcStatus: Optional[int]
    qcTypeLog: Optional[str]
    acquisitionType: Optional[int]
    dataForm: Optional[str]
    capturedBy: Optional[str]
    mark: Optional[int]
    temperatureUnits: Optional[str]
    precipitationUnits: Optional[str]
    cloudHeightUnits: Optional[str]
    visUnits: Optional[str]
    dataSourceTimeZone: Optional[int]

    class Config:
        allow_population_by_field_name = True
        fields = field_mapping


class UpdateObservationfinal(BaseModel):
    obsLevel: Optional[str]
    obsValue: Optional[float]
    flag: Optional[str]
    period: Optional[int]
    qcStatus: Optional[int]
    qcTypeLog: Optional[str]
    acquisitionType: Optional[int]
    dataForm: Optional[str]
    capturedBy: Optional[str]
    mark: Optional[int]
    temperatureUnits: Optional[str]
    precipitationUnits: Optional[str]
    cloudHeightUnits: Optional[str]
    visUnits: Optional[str]
    dataSourceTimeZone: Optional[int]

    class Config:
        allow_population_by_field_name = True
        fields = field_mapping


class UniqueId(BaseModel):
    recordedFrom: str
    describedBy: int
    obsDatetime: str

    class Config:
        allow_population_by_field_name = True
        fields = field_mapping


class GeometrySchema(BaseModel):
    type: str = "Point"
    coordinates: List[float]


class ObservationfinalPygeoapiSchema(BaseModel):
    type: str = "Feature"
    geometry: GeometrySchema
    properties: ObservationfinalWithStation
    id: str
    links: List[Dict[str, str]]
