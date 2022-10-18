from pydantic import BaseModel
from typing import Optional


class StationStatu(BaseModel):
    id: int
    status: str
    description: str

    class Config:
        orm_mode = True


class CreateStationStatu(BaseModel):
    id: Optional[int] = None
    status: str
    description: Optional[str] = ""
