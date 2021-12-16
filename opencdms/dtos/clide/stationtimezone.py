from pydantic import BaseModel


class StationTimezone(BaseModel):
    id: int
    tm_zone: str
    utc_diff: int
    description: str

    class Config:
        orm_mode = True


class CreateStationTimezone(BaseModel):
    id: int
    tm_zone: str
    utc_diff: int
    description: str
