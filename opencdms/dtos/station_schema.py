from decimal import Decimal
from pydantic import BaseModel
from typing import Optional, Union


class Station(BaseModel):
    station_id: Union[int, str]
    station_no: Union[int, str]
    name: str
    secondary_name: Optional[str]
    latitude: Decimal
    longitude: Decimal
    elevation: int
    region: str
    start_datetime: str
    end_datetime: str


class CreateStation(BaseModel):
    name: str
    secondary_name: Optional[str]
    latitude: Decimal
    longitude: Decimal
    elevation: int
    region: str
    start_date: str
    end_date: str


class UpdateStudent(BaseModel):
    name: Optional[str]
    secondary_name: Optional[str]
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]
    elevation: Optional[int]
    region: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
