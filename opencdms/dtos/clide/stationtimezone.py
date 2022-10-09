from pydantic import BaseModel
from typing import Optional


class StationTimezone(BaseModel):
    id: int
    tm_zone: str
    utc_diff: int
    description: str

    class Config:
        orm_mode = True


class CreateStationTimezone(BaseModel):
    id:  Optional[int] = None
    tm_zone: str
    utc_diff: int
    description: str
