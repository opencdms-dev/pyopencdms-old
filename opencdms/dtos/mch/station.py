from pydantic import BaseModel, constr
from typing import Optional
from decimal import Decimal

field_mapping = {
    "Station": "station_id",
    "StationName": "name",
    "StationName2": "secondary_name",
    "TimeZone": "timezone",
    "Longitud": "longitude",
    "Latitud": "latitude"
}


class Station(BaseModel):
    Station: Optional[str]
    StationName: Optional[str]
    StationName2: Optional[str]
    TimeZone: Optional[constr(max_length=4)]
    Longitud: Optional[Decimal]
    Latitud: Optional[Decimal]

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        fields = field_mapping


class CreateStation(BaseModel):
    Station: Optional[str]
    StationName: Optional[str]
    StationName2: Optional[str]
    TimeZone: Optional[constr(max_length=4)]
    Longitud: Optional[Decimal]
    Latitud: Optional[Decimal]

    class Config:
        fields = field_mapping


class UpdateStation(BaseModel):
    StationName: Optional[str]
    StationName2: Optional[str]
    TimeZone: Optional[constr(max_length=4)]
    Longitud: Optional[Decimal]
    Latitud: Optional[Decimal]

    class Config:
        fields = field_mapping


class UniqueId(BaseModel):
    Station: str

    class Config:
        fields = field_mapping
