# coding: utf-8
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    UniqueConstraint,
    text,
    PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class RawData(Base):
    __tablename__ = "raw_data"
    __table_args__ = (
        PrimaryKeyConstraint(
            "datetime",
            "station_id",
            "variable_id",
        ),
        Index(
            "raw_data_datetime_station_id_variable_id_uidx",
            "datetime",
            "station_id",
            "variable_id",
            unique=True,
        ),
    )

    created_at = Column(
        DateTime(True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        DateTime(True), nullable=False, server_default=text("now()")
    )
    datetime = Column(DateTime(True), nullable=False, index=True)
    measured = Column(Float(53), nullable=False)
    consisted = Column(Float(53))
    qc_range_description = Column(String(256))
    qc_step_description = Column(String(256))
    qc_persist_description = Column(String(256))
    manual_flag = Column(Integer)
    qc_persist_quality_flag = Column(Integer)
    qc_range_quality_flag = Column(Integer)
    qc_step_quality_flag = Column(Integer)
    quality_flag = Column(Integer, nullable=False)
    station_id = Column(ForeignKey("wx_station.id"), nullable=False)
    variable_id = Column(Integer, nullable=False)
    observation_flag_id = Column(Integer)
    is_daily = Column(Boolean, nullable=False, server_default=text("false"))
    remarks = Column(String(150))
    observer = Column(String(150))
    code = Column(String(60))
    ml_flag = Column(Integer, server_default=text("1"))

    station = relationship("WxStation")


class WxCountry(Base):
    __tablename__ = "wx_country"

    id = Column(
        BigInteger,
        primary_key=True,
        server_default=text("nextval('wx_country_id_seq'::regclass)"),
    )
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    notation = Column(String(16), nullable=False)
    name = Column(String(256), nullable=False, unique=True)
    description = Column(String(256))


class WxDatasource(Base):
    __tablename__ = "wx_datasource"

    id = Column(
        BigInteger,
        primary_key=True,
        server_default=text("nextval('wx_datasource_id_seq'::regclass)"),
    )
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    symbol = Column(String(8), nullable=False, unique=True)
    name = Column(String(32), nullable=False, unique=True)
    base_url = Column(String(200))
    location = Column(String(256))


class WxStationcommunication(Base):
    __tablename__ = "wx_stationcommunication"

    id = Column(
        BigInteger,
        primary_key=True,
        server_default=text(
            "nextval('wx_stationcommunication_id_seq'::regclass)"
        ),
    )
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    name = Column(String(45), nullable=False)
    description = Column(String(256), nullable=False)
    color = Column(String(7), nullable=False)


class WxStationprofile(Base):
    __tablename__ = "wx_stationprofile"

    id = Column(
        BigInteger,
        primary_key=True,
        server_default=text("nextval('wx_stationprofile_id_seq'::regclass)"),
    )
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    name = Column(String(45), nullable=False)
    description = Column(String(256), nullable=False)
    color = Column(String(7), nullable=False)
    is_automatic = Column(Boolean, nullable=False)
    is_manual = Column(Boolean, nullable=False)


class WxWmoprogram(Base):
    __tablename__ = "wx_wmoprogram"

    id = Column(
        BigInteger,
        primary_key=True,
        server_default=text("nextval('wx_wmoprogram_id_seq'::regclass)"),
    )
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    name = Column(String(256), nullable=False, unique=True)
    description = Column(String(512))
    notation = Column(String(256))
    path = Column(String(256))


class WxWmoregion(Base):
    __tablename__ = "wx_wmoregion"

    id = Column(
        BigInteger,
        primary_key=True,
        server_default=text("nextval('wx_wmoregion_id_seq'::regclass)"),
    )
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    name = Column(String(256), nullable=False, unique=True)
    description = Column(String(256))
    notation = Column(String(256))


class WxWmostationtype(Base):
    __tablename__ = "wx_wmostationtype"

    id = Column(
        BigInteger,
        primary_key=True,
        server_default=text("nextval('wx_wmostationtype_id_seq'::regclass)"),
    )
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    name = Column(String(256), nullable=False, unique=True)
    description = Column(String(256))
    notation = Column(String(256))


class WxStation(Base):
    __tablename__ = "wx_station"
    __table_args__ = (UniqueConstraint("data_source_id", "code"),)

    id = Column(
        BigInteger,
        primary_key=True,
        server_default=text("nextval('wx_station_id_seq'::regclass)"),
    )
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    name = Column(String(256), nullable=False)
    alias_name = Column(String(256))
    begin_date = Column(DateTime(True))
    end_date = Column(DateTime(True))
    longitude = Column(Float(53), nullable=False)
    latitude = Column(Float(53), nullable=False)
    elevation = Column(Float(53))
    code = Column(String(64), nullable=False)
    wmo = Column(Integer)
    wigos = Column(String(64))
    is_active = Column(Boolean, nullable=False)
    is_automatic = Column(Boolean, nullable=False)
    organization = Column(String(256))
    observer = Column(String(256))
    watershed = Column(String(256))
    z = Column(Float(53))
    datum = Column(String(256))
    zone = Column(String(256))
    ground_water_province = Column(String(256))
    river_code = Column(Integer)
    river_course = Column(String(64))
    catchment_area_station = Column(String(256))
    river_origin = Column(String(256))
    easting = Column(Float(53))
    northing = Column(Float(53))
    river_outlet = Column(String(256))
    river_length = Column(Integer)
    local_land_use = Column(String(256))
    soil_type = Column(String(64))
    site_description = Column(String(256))
    land_surface_elevation = Column(Float(53))
    screen_length = Column(Float(53))
    top_casing_land_surface = Column(Float(53))
    depth_midpoint = Column(Float(53))
    screen_size = Column(Float(53))
    casing_type = Column(String(256))
    casing_diameter = Column(Float(53))
    existing_gauges = Column(String(256))
    flow_direction_at_station = Column(String(256))
    flow_direction_above_station = Column(String(256))
    flow_direction_below_station = Column(String(256))
    bank_full_stage = Column(String(256))
    bridge_level = Column(String(256))
    access_point = Column(String(256))
    temporary_benchmark = Column(String(256))
    mean_sea_level = Column(String(256))
    data_type = Column(String(256))
    frequency_observation = Column(String(256))
    historic_events = Column(String(256))
    other_information = Column(String(256))
    hydrology_station_type = Column(String(64))
    is_surface = Column(Boolean, nullable=False)
    station_details = Column(String(256))
    remarks = Column(String(256))
    region = Column(String(256))
    utc_offset_minutes = Column(Integer, nullable=False)
    alternative_names = Column(String(256))
    wmo_station_plataform = Column(String(256))
    operation_status = Column(Boolean, nullable=False)
    communication_type_id = Column(
        ForeignKey(
            "wx_stationcommunication.id", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    data_source_id = Column(
        ForeignKey("wx_datasource.id", deferrable=True, initially="DEFERRED"),
        index=True,
    )
    profile_id = Column(
        ForeignKey(
            "wx_stationprofile.id", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    wmo_program_id = Column(
        ForeignKey("wx_wmoprogram.id", deferrable=True, initially="DEFERRED"),
        index=True,
    )
    wmo_region_id = Column(
        ForeignKey("wx_wmoregion.id", deferrable=True, initially="DEFERRED"),
        index=True,
    )
    wmo_station_type_id = Column(
        ForeignKey(
            "wx_wmostationtype.id", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    relocation_date = Column(DateTime(True))
    network = Column(String(256))
    reference_station_id = Column(
        ForeignKey("wx_station.id", deferrable=True, initially="DEFERRED"),
        index=True,
    )
    country_id = Column(
        ForeignKey("wx_country.id", deferrable=True, initially="DEFERRED"),
        index=True,
    )

    communication_type = relationship("WxStationcommunication")
    country = relationship("WxCountry")
    data_source = relationship("WxDatasource")
    profile = relationship("WxStationprofile")
    reference_station = relationship("WxStation", remote_side=[id])
    wmo_program = relationship("WxWmoprogram")
    wmo_region = relationship("WxWmoregion")
    wmo_station_type = relationship("WxWmostationtype")
