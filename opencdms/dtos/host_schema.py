from decimal import Decimal
from pydantic import BaseModel,UUID4
from typing import Optional, Union
from typing import NewType, Optional
from datetime import datetime
Geography = NewType("Geography", str)

class Host(BaseModel):
    id: UUID4
    name: str
    version: int
    change_date: datetime
    user_id: int
    status_id: int
    comments: str
    description: Optional[str] = ""
    link: Optional[str] = ""
    location: Geography  = None
    elevation: float = None
    wigos_station_identifier: Optional[str] = ""
    facility_type: Optional[str] = ""
    date_established: Optional[str] = ""
    wmo_region: Optional[str] = ""
    territory: Optional[str] = ""
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None

    class Config:
        orm_mode =True
