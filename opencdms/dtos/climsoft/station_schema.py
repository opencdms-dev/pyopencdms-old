from pydantic import BaseModel
from typing import Optional


class Station(BaseModel):
    stationId: str
    stationName: str
    country: str
    adminRegion: str
    latitude: float
    longitude: float
    elevation: float
    openingDatetime: str
    closingDatetime: str

    class Config:
        orm_mode = True
        fields = {
            "stationId": "station_id",
            "station_name": "name",
            "adminRegion": "region",
            "openingDatetime": "start_datetime",
            "closingDatetime": "end_datetime"
        }


class CreateStation(BaseModel):
    stationId: str
    stationName: str
    country: str


class UpdateStation(BaseModel):
    stationName: Optional[str]
    country: Optional[str]




