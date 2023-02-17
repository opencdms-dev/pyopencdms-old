from decimal import Decimal
from pydantic import BaseModel,UUID4
from typing import NewType, Optional, List, Dict
from datetime import datetime

from opencdms.types import Geography, Coordinates

class CreateObservationSchema(BaseModel):
    location: Geography
    version: int
    change_date: datetime
    phenomenon_end: datetime
    result_value: float
    comments: str
    host_id: str
    observer_id: str
    collection_id: str
    feature_of_interest_id: str
    report_id: Optional[str] = ""
    user_id: Optional[int] = None
    status_id: Optional[int] = None
    source_id: Optional[int] = None
    observed_property_id: Optional[int] = None
    parameter: Optional[dict] = None
    elevation: float = None
    observation_type_id: Optional[int] = None
    phenomenon_start: Optional[datetime] = None
    result_uom: Optional[str] = ""
    result_description: Optional[str] = ""
    result_quality: Optional[dict] = None
    result_time: Optional[datetime] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    observing_procedure_id: Optional[int] = None

class UpdateObservationSchema(BaseModel):
    location: Geography
    version: int
    change_date: datetime
    phenomenon_end: datetime
    result_value: float
    comments: str
    host_id: str
    observer_id: str
    collection_id: str
    feature_of_interest_id: str
    report_id: Optional[str] = ""
    user_id: Optional[int] = None
    status_id: Optional[int] = None
    source_id: Optional[int] = None
    observed_property_id: Optional[int] = None
    parameter: Optional[dict] = None
    elevation: float = None
    observation_type_id: Optional[int] = None
    phenomenon_start: Optional[datetime] = None
    result_uom: Optional[str] = ""
    result_description: Optional[str] = ""
    result_quality: Optional[dict] = None
    result_time: Optional[datetime] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    observing_procedure_id: Optional[int] = None


class ObservationSchema(CreateObservationSchema):
    id : UUID4
    coordinates: Coordinates
    class Config:
        orm_mode = True


class GeometrySchema(BaseModel):
    type: str = "Point"
    coordinates: List[float]


class ObservationPygeoapiSchema(BaseModel):
    type: str = "Feature"
    geometry: GeometrySchema
    properties: ObservationSchema
    id: str
    links: List[Dict[str, str]]