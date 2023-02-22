from pydantic import BaseModel, constr
import datetime
from typing import Optional


class WxStation(BaseModel):
    id: int
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    name: constr(max_length=256)
    alias_name: Optional[constr(max_length=256)]
    begin_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    longitude: float
    latitude: float
    elevation: Optional[float]
    code: constr(max_length=64)
    wmo: Optional[int]
    wigos: Optional[constr(max_length=64)]
    is_active: bool
    is_automatic: bool
    organization: Optional[constr(max_length=256)]
    observer: Optional[constr(max_length=256)]
    watershed: Optional[constr(max_length=256)]
    z: Optional[float]
    datum: Optional[constr(max_length=256)]
    zone: Optional[constr(max_length=256)]
    ground_water_province: Optional[constr(max_length=256)]
    river_code: Optional[int]
    river_course: Optional[constr(max_length=64)]
    catchment_area_station: Optional[constr(max_length=256)]
    river_origin: Optional[constr(max_length=256)]
    easting: Optional[float]
    northing: Optional[float]
    river_outlet: Optional[constr(max_length=256)]
    river_length: Optional[int]
    local_land_use: Optional[constr(max_length=256)]
    soil_type: Optional[constr(max_length=64)]
    site_description: Optional[constr(max_length=256)]
    land_surface_elevation: Optional[float]
    screen_length: Optional[float]
    top_casing_land_surface: Optional[float]
    depth_midpoint: Optional[float]
    screen_size: Optional[float]
    casing_type: Optional[constr(max_length=256)]
    casing_diameter: Optional[float]
    existing_gauges: Optional[constr(max_length=256)]
    flow_direction_at_station: Optional[constr(max_length=256)]
    flow_direction_above_station: Optional[constr(max_length=256)]
    flow_direction_below_station: Optional[constr(max_length=256)]
    bank_full_stage: Optional[constr(max_length=256)]
    bridge_level: Optional[constr(max_length=256)]
    access_point: Optional[constr(max_length=256)]
    temporary_benchmark: Optional[constr(max_length=256)]
    mean_sea_level: Optional[constr(max_length=256)]
    data_type: Optional[constr(max_length=256)]
    frequency_observation: Optional[constr(max_length=256)]
    historic_events: Optional[constr(max_length=256)]
    other_information: Optional[constr(max_length=256)]
    hydrology_station_type: Optional[constr(max_length=64)]
    is_surface: bool
    station_details: Optional[constr(max_length=256)]
    remarks: Optional[constr(max_length=256)]
    region: Optional[constr(max_length=256)]
    utc_offset_minutes: int
    alternative_names: Optional[constr(max_length=256)]
    wmo_station_plataform: Optional[constr(max_length=256)]
    operation_status: bool
    communication_type_id: Optional[int]
    data_source_id: Optional[int]
    profile_id: Optional[int]
    wmo_program_id: Optional[int]
    wmo_region_id: Optional[int]
    wmo_station_type_id: Optional[int]
    relocation_date: Optional[datetime.datetime]
    network: Optional[constr(max_length=256)]
    reference_station_id: Optional[int]
    country_id: Optional[int]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

