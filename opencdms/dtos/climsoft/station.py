from pydantic import BaseModel
from typing import Optional


field_mapping = {
    "stationId": "station_id",
    "stationName": "name",
    "adminRegion": "region",
    "openingDatetime": "start_datetime",
    "closingDatetime": "end_datetime"
}


class Station(BaseModel):
    stationId: Optional[str]
    stationName: Optional[str]
    country: Optional[str]
    adminRegion: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    elevation: Optional[float]
    openingDatetime: Optional[str]
    closingDatetime: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = field_mapping


class CreateStation(BaseModel):
    stationId: str
    stationName: str
    country: str

    class Config:
        allow_population_by_field_name = True
        fields = field_mapping


class UpdateStation(BaseModel):
    stationName: Optional[str]
    country: Optional[str]

    class Config:
        allow_population_by_field_name = True
        fields = field_mapping


class UniqueId(BaseModel):
    stationId: str

    class Config:
        allow_population_by_field_name = True
        fields = field_mapping
