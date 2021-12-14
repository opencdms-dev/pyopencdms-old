from pydantic import BaseModel, constr
from typing import Optional
from decimal import Decimal


class Station(BaseModel):
    Station: str
    StationName: str
    StationName2: str
    TimeZone: constr(max_length=4)
    Longitud: Decimal
    Latitud: Decimal

    class Config:
        orm_mode = True
        fields = {
            "Station": "station_id",
            "StationName": "name",
            "StationName2": "secondary_name",
            "TimeZone": "timezone",
            "Longitud": "longitude",
            "Latitud": "latitude"
        }


class CreateStation(BaseModel):
    Station: str
    StationName: str


class UpdateStation(BaseModel):
    StationName: Optional[str]






