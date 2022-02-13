from pydantic import BaseModel


class StationStatu(BaseModel):
    id: int
    status: str
    description: str

    class Config:
        orm_mode = True


class CreateStationStatu(BaseModel):
    id: int
    status: str
    description: str
