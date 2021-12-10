# coding: utf-8
from sqlalchemy import (
    BigInteger,
    CHAR,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Table,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


CLIDE_VIEWS = {
    "cdms_get_ext_views",
    "ext_class",
    "ext_equipment",
    "ext_obs_aero",
    "ext_obs_aws",
    "ext_obs_climat",
    "ext_obs_daily",
    "ext_obs_daily_basics",
    "ext_obs_monthly",
    "ext_obs_monthly_calculated",
    "ext_obs_monthly_combined",
    "ext_obs_subdaily",
    "ext_obs_subdaily_cloud_layers",
    "ext_obs_subdaily_soil_temps",
    "ext_obs_upper_air",
    "ext_station_audit",
    "ext_station_class",
    "ext_station_equipment",
    "ext_stations",
}


# region SQL Views
t_cdms_get_ext_views = Table(
    "cdms_get_ext_views", metadata, Column("table_name", String)
)

t_ext_class = Table(
    "ext_class",
    metadata,
    Column("id", Integer),
    Column("class", String(10)),
    Column("description", String(50)),
)


t_ext_equipment = Table(
    "ext_equipment",
    metadata,
    Column("id", Integer),
    Column("type", String(50)),
    Column("comments", String(1000)),
    Column("version", String(50)),
)


t_ext_obs_aero = Table(
    "ext_obs_aero",
    metadata,
    Column("id", Integer),
    Column("station_no", String(15)),
    Column("lsd", DateTime),
    Column("gmt", DateTime),
    Column("lct", DateTime),
    Column("data_source", CHAR(2)),
    Column("insert_datetime", DateTime),
    Column("change_datetime", DateTime),
    Column("change_user", String(20)),
    Column("qa_flag", CHAR(1)),
    Column("comments", String(1000)),
    Column("message_type", CHAR(1)),
    Column("wind_dir", Numeric(4, 0)),
    Column("wind_dir_qa", CHAR(2)),
    Column("wind_speed", Numeric(4, 1)),
    Column("wind_speed_qa", CHAR(2)),
    Column("max_gust_10m", Numeric(4, 1)),
    Column("max_gust_10m_qa", CHAR(2)),
    Column("cavok_or_skc", CHAR(1)),
    Column("visibility", Numeric(7, 3)),
    Column("visibility_qa", CHAR(2)),
    Column("pres_wea_intensity_1", Numeric(1, 0)),
    Column("pres_wea_desc_1", CHAR(2)),
    Column("pres_wea_phen_1", String(6)),
    Column("pres_wea_1_qa", CHAR(2)),
    Column("pres_wea_intensity_2", Numeric(1, 0)),
    Column("pres_wea_desc_2", CHAR(2)),
    Column("pres_wea_phen_2", String(6)),
    Column("pres_wea_2_qa", CHAR(2)),
    Column("pres_wea_intensity_3", Numeric(1, 0)),
    Column("pres_wea_desc_3", CHAR(2)),
    Column("pres_wea_phen_3", String(6)),
    Column("pres_wea_3_qa", CHAR(2)),
    Column("cloud_amt_oktas_1", Numeric(2, 0)),
    Column("cloud_amt_code_1", CHAR(3)),
    Column("cloud_amt_1_qa", CHAR(2)),
    Column("cloud_type_1", String(2)),
    Column("cloud_type_1_qa", CHAR(2)),
    Column("cloud_height_code_1", CHAR(3)),
    Column("cloud_height_1_qa", CHAR(2)),
    Column("cloud_amt_oktas_2", Numeric(2, 0)),
    Column("cloud_amt_code_2", CHAR(3)),
    Column("cloud_amt_2_qa", CHAR(2)),
    Column("cloud_type_2", String(2)),
    Column("cloud_type_2_qa", CHAR(2)),
    Column("cloud_height_code_2", CHAR(3)),
    Column("cloud_height_2_qa", CHAR(2)),
    Column("cloud_amt_oktas_3", Numeric(2, 0)),
    Column("cloud_amt_code_3", CHAR(3)),
    Column("cloud_amt_3_qa", CHAR(2)),
    Column("cloud_type_3", String(2)),
    Column("cloud_type_3_qa", CHAR(2)),
    Column("cloud_height_code_3", CHAR(3)),
    Column("cloud_height_3_qa", CHAR(2)),
    Column("cloud_amt_oktas_4", Numeric(2, 0)),
    Column("cloud_amt_code_4", CHAR(3)),
    Column("cloud_amt_4_qa", CHAR(2)),
    Column("cloud_type_4", String(2)),
    Column("cloud_type_4_qa", CHAR(2)),
    Column("cloud_height_code_4", CHAR(3)),
    Column("cloud_height_4_qa", CHAR(2)),
    Column("cloud_amt_oktas_5", Numeric(2, 0)),
    Column("cloud_amt_code_5", CHAR(3)),
    Column("cloud_amt_5_qa", CHAR(2)),
    Column("cloud_type_5", String(2)),
    Column("cloud_type_5_qa", CHAR(2)),
    Column("cloud_height_code_5", CHAR(3)),
    Column("cloud_height_5_qa", CHAR(2)),
    Column("cloud_amt_oktas_6", Numeric(2, 0)),
    Column("cloud_amt_code_6", CHAR(3)),
    Column("cloud_amt_6_qa", CHAR(2)),
    Column("cloud_type_6", String(2)),
    Column("cloud_type_6_qa", CHAR(2)),
    Column("cloud_height_code_6", CHAR(3)),
    Column("cloud_height_6_qa", CHAR(2)),
    Column("ceiling_clear_flag", Numeric(1, 0)),
    Column("ceiling_clear_flag_qa", CHAR(2)),
    Column("air_temp", Numeric(4, 1)),
    Column("air_temp_f", Numeric(4, 1)),
    Column("air_temp_qa", CHAR(2)),
    Column("dew_point", Numeric(4, 1)),
    Column("dew_point_f", Numeric(4, 1)),
    Column("dew_point_qa", CHAR(2)),
    Column("qnh", Numeric(7, 1)),
    Column("qnh_inches", Numeric(8, 3)),
    Column("qnh_qa", CHAR(2)),
    Column("rec_wea_desc_1", CHAR(2)),
    Column("rec_wea_phen_1", String(6)),
    Column("rec_wea_1_qa", CHAR(2)),
    Column("rec_wea_desc_2", CHAR(2)),
    Column("rec_wea_phen_2", String(6)),
    Column("rec_wea_2_qa", CHAR(2)),
    Column("rec_wea_desc_3", CHAR(2)),
    Column("rec_wea_phen_3", String(6)),
    Column("rec_wea_3_qa", CHAR(2)),
    Column("text_msg", String(1024)),
    Column("error_flag", Numeric(1, 0)),
    Column("remarks", String(400)),
    Column("remarks_qa", CHAR(2)),
    Column("wind_speed_knots", Numeric(5, 1)),
    Column("max_gust_10m_knots", Numeric(5, 1)),
    Column("visibility_miles", Numeric(7, 3)),
)


t_ext_obs_aws = Table(
    "ext_obs_aws",
    metadata,
    Column("id", Integer),
    Column("station_no", String(15)),
    Column("lsd", DateTime),
    Column("gmt", DateTime),
    Column("lct", DateTime),
    Column("insert_datetime", DateTime),
    Column("change_datetime", DateTime),
    Column("change_user", String(20)),
    Column("data_source", CHAR(2)),
    Column("qa_flag", CHAR(1)),
    Column("measure_period", SmallInteger),
    Column("mn_wind_dir_pt", CHAR(3)),
    Column("mn_wind_dir_deg", SmallInteger),
    Column("mn_wind_dir_qa", CHAR(2)),
    Column("mn_wind_dir_stddev", Numeric(3, 1)),
    Column("mn_wind_dir_stddev_qa", CHAR(2)),
    Column("mn_wind_speed", Numeric(7, 1)),
    Column("mn_wind_speed_qa", CHAR(2)),
    Column("mn_wind_speed_stddev", Numeric(7, 1)),
    Column("mn_wind_speed_stddev_qa", CHAR(2)),
    Column("mn_gust_speed", Numeric(7, 1)),
    Column("mn_gust_speed_qa", CHAR(2)),
    Column("mn_gust_time", String(8)),
    Column("mn_gust_time_qa", CHAR(2)),
    Column("mn_gust_dir_pt", CHAR(3)),
    Column("mn_gust_dir_deg", SmallInteger),
    Column("mn_gust_dir_qa", CHAR(2)),
    Column("inst_gust_speed", Numeric(7, 1)),
    Column("inst_gust_qa", CHAR(2)),
    Column("inst_gust_time", String(8)),
    Column("inst_gust_time_qa", CHAR(2)),
    Column("inst_gust_dir_pt", CHAR(3)),
    Column("inst_gust_dir_deg", SmallInteger),
    Column("inst_gust_dir_qa", CHAR(2)),
    Column("mn_temp", Numeric(7, 1)),
    Column("mn_temp_qa", CHAR(2)),
    Column("mn_temp_subaveraging", Numeric(7, 1)),
    Column("mn_temp_subaveraging_period", SmallInteger),
    Column("mn_temp_subaveraging_qa", CHAR(2)),
    Column("max_temp", Numeric(7, 1)),
    Column("max_temp_time", String(8)),
    Column("max_temp_time_qa", CHAR(2)),
    Column("max_temp_qa", CHAR(2)),
    Column("min_temp", Numeric(7, 1)),
    Column("min_temp_qa", CHAR(2)),
    Column("min_temp_time", String(8)),
    Column("min_temp_time_qa", CHAR(2)),
    Column("min_grass_temp", Numeric(7, 1)),
    Column("min_grass_temp_qa", CHAR(2)),
    Column("min_grass_temp_time", String(8)),
    Column("min_grass_temp_time_qa", CHAR(2)),
    Column("mn_humidity", Numeric(4, 1)),
    Column("mn_humidity_qa", CHAR(2)),
    Column("max_humidity", Numeric(4, 1)),
    Column("max_humidity_qa", CHAR(2)),
    Column("max_humidity_time", String(8)),
    Column("max_humidity_time_qa", CHAR(2)),
    Column("min_humidity", Numeric(4, 1)),
    Column("min_humidity_qa", CHAR(2)),
    Column("min_humidity_time", String(8)),
    Column("min_humidity_time_qa", CHAR(2)),
    Column("mn_station_pres", Numeric(5, 1)),
    Column("mn_station_pres_qa", CHAR(2)),
    Column("mn_sea_level_pres", Numeric(5, 1)),
    Column("mn_sea_level_pres_qa", CHAR(2)),
    Column("max_pres", Numeric(5, 1)),
    Column("max_pres_qa", CHAR(2)),
    Column("max_pres_time", String(8)),
    Column("max_pres_time_qa", CHAR(2)),
    Column("min_pres", Numeric(5, 1)),
    Column("min_pres_qa", CHAR(2)),
    Column("min_pres_time", String(8)),
    Column("min_pres_time_qa", CHAR(2)),
    Column("tot_rain", Numeric(6, 1)),
    Column("tot_rain_qa", CHAR(2)),
    Column("tot_rain_two", Numeric(6, 1)),
    Column("tot_rain_two_qa", CHAR(2)),
    Column("tot_sun", Integer),
    Column("tot_sun_qa", CHAR(2)),
    Column("tot_insolation", Numeric(7, 2)),
    Column("tot_insolation_qa", CHAR(2)),
    Column("leaf_wetness", SmallInteger),
    Column("leaf_wetness_qa", CHAR(2)),
    Column("mn_uv", Numeric(4, 0)),
    Column("mn_uv_qa", CHAR(2)),
    Column("mn_soil_moisture_10", Numeric(3, 1)),
    Column("mn_soil_moisture_10_qa", CHAR(2)),
    Column("mn_soil_temp_10", Numeric(5, 1)),
    Column("mn_soil_temp_10_qa", CHAR(2)),
    Column("mn_soil_moisture_20", Numeric(3, 1)),
    Column("mn_soil_moisture_20_qa", CHAR(2)),
    Column("mn_soil_temp_20", Numeric(5, 1)),
    Column("mn_soil_temp_20_qa", CHAR(2)),
    Column("mn_soil_moisture_30", Numeric(3, 1)),
    Column("mn_soil_moisture_30_qa", CHAR(2)),
    Column("mn_soil_temp_30", Numeric(5, 1)),
    Column("mn_soil_temp_30_qa", CHAR(2)),
    Column("mn_soil_moisture_50", Numeric(3, 1)),
    Column("mn_soil_moisture_50_qa", CHAR(2)),
    Column("mn_soil_temp_50", Numeric(5, 1)),
    Column("mn_soil_temp_50_qa", CHAR(2)),
    Column("mn_soil_moisture_100", Numeric(3, 1)),
    Column("mn_soil_moisture_100_qa", CHAR(2)),
    Column("mn_soil_temp_100", Numeric(5, 1)),
    Column("mn_soil_temp_100_qa", CHAR(2)),
)


t_ext_obs_climat = Table(
    "ext_obs_climat",
    metadata,
    Column("station_no", String(15)),
    Column("lsd", Date),
    Column("station_pres", Numeric),
    Column("msl_pres", Numeric),
    Column("air_temp", Numeric),
    Column("dew_point", Numeric),
    Column("vapour_pres", Numeric),
    Column("max_temp", Numeric),
    Column("min_temp", Numeric),
    Column("rain", Numeric),
    Column("rain_days", Numeric),
    Column("sunshine", Numeric),
    Column("max_rowcount", BigInteger),
    Column("min_rowcount", BigInteger),
    Column("rain_rowcount", BigInteger),
    Column("sunshine_rowcount", BigInteger),
    Column("pres_daycount", BigInteger),
    Column("temp_daycount", BigInteger),
    Column("vapour_daycount", BigInteger),
    Column("days_in_month", Float(53)),
)


t_ext_obs_daily = Table(
    "ext_obs_daily",
    metadata,
    Column("id", Integer),
    Column("station_no", String(15)),
    Column("lsd", DateTime),
    Column("data_source", CHAR(2)),
    Column("insert_datetime", DateTime),
    Column("change_datetime", DateTime),
    Column("change_user", String(20)),
    Column("qa_flag", CHAR(1)),
    Column("aws_flag", CHAR(1)),
    Column("comments", String(1000)),
    Column("rain_24h", Numeric(6, 1)),
    Column("rain_24h_inches", Numeric(7, 3)),
    Column("rain_24h_period", Numeric(2, 0)),
    Column("rain_24h_type", String(10)),
    Column("rain_24h_count", Numeric(2, 0)),
    Column("rain_24h_qa", CHAR(2)),
    Column("max_air_temp", Numeric(7, 1)),
    Column("max_air_temp_f", Numeric(7, 1)),
    Column("max_air_temp_period", Numeric(2, 0)),
    Column("max_air_temp_time", String(5)),
    Column("max_air_temp_qa", CHAR(2)),
    Column("min_air_temp", Numeric(5, 1)),
    Column("min_air_temp_f", Numeric(5, 1)),
    Column("min_air_temp_period", Numeric(2, 0)),
    Column("min_air_temp_time", String(5)),
    Column("min_air_temp_qa", CHAR(2)),
    Column("reg_max_air_temp", Numeric(7, 1)),
    Column("reg_max_air_temp_qa", CHAR(2)),
    Column("reg_min_air_temp", Numeric(7, 1)),
    Column("reg_min_air_temp_qa", CHAR(2)),
    Column("ground_temp", Numeric(5, 1)),
    Column("ground_temp_f", Numeric(5, 1)),
    Column("ground_temp_qa", CHAR(2)),
    Column("max_gust_dir", Numeric(3, 0)),
    Column("max_gust_dir_qa", CHAR(2)),
    Column("max_gust_speed", Numeric(4, 1)),
    Column("max_gust_speed_kts", Numeric(3, 0)),
    Column("max_gust_speed_bft", String(2)),
    Column("max_gust_speed_qa", CHAR(2)),
    Column("max_gust_time", String(5)),
    Column("max_gust_time_qa", CHAR(2)),
    Column("wind_run_lt10", Numeric(6, 2)),
    Column("wind_run_lt10_miles", Numeric(6, 2)),
    Column("wind_run_lt10_period", Numeric(3, 0)),
    Column("wind_run_lt10_qa", CHAR(2)),
    Column("wind_run_gt10", Numeric(6, 2)),
    Column("wind_run_gt10_miles", Numeric(6, 2)),
    Column("wind_run_gt10_period", Numeric(3, 0)),
    Column("wind_run_gt10_qa", CHAR(2)),
    Column("evaporation", Numeric(4, 1)),
    Column("evaporation_inches", Numeric(5, 3)),
    Column("evaporation_period", Numeric(3, 0)),
    Column("evaporation_qa", CHAR(2)),
    Column("evap_water_max_temp", Numeric(5, 1)),
    Column("evap_water_max_temp_f", Numeric(5, 1)),
    Column("evap_water_max_temp_qa", CHAR(2)),
    Column("evap_water_min_temp", Numeric(5, 1)),
    Column("evap_water_min_temp_f", Numeric(5, 1)),
    Column("evap_water_min_temp_qa", CHAR(2)),
    Column("sunshine_duration", Numeric(3, 1)),
    Column("sunshine_duration_qa", CHAR(2)),
    Column("river_height", Numeric(5, 1)),
    Column("river_height_in", Numeric(8, 1)),
    Column("river_height_qa", CHAR(2)),
    Column("radiation", Numeric(6, 1)),
    Column("radiation_qa", CHAR(2)),
    Column("thunder_flag", CHAR(1)),
    Column("thunder_flag_qa", CHAR(2)),
    Column("frost_flag", CHAR(1)),
    Column("frost_flag_qa", CHAR(2)),
    Column("dust_flag", CHAR(1)),
    Column("dust_flag_qa", CHAR(2)),
    Column("haze_flag", CHAR(1)),
    Column("haze_flag_qa", CHAR(2)),
    Column("fog_flag", CHAR(1)),
    Column("fog_flag_qa", CHAR(2)),
    Column("strong_wind_flag", CHAR(1)),
    Column("strong_wind_flag_qa", CHAR(2)),
    Column("gale_flag", CHAR(1)),
    Column("gale_flag_qa", CHAR(2)),
    Column("hail_flag", CHAR(1)),
    Column("hail_flag_qa", CHAR(2)),
    Column("snow_flag", CHAR(1)),
    Column("snow_flag_qa", CHAR(2)),
    Column("lightning_flag", CHAR(1)),
    Column("lightning_flag_qa", CHAR(2)),
    Column("shower_flag", CHAR(1)),
    Column("shower_flag_qa", CHAR(2)),
    Column("rain_flag", CHAR(1)),
    Column("rain_flag_qa", CHAR(2)),
    Column("dew_flag", CHAR(1)),
    Column("dew_flag_qa", CHAR(2)),
)


t_ext_obs_daily_basics = Table(
    "ext_obs_daily_basics",
    metadata,
    Column("station_no", String(15)),
    Column("lsd", DateTime),
    Column("max_air_temp", Numeric(7, 1)),
    Column("min_air_temp", Numeric(5, 1)),
    Column("rain_24h", Numeric(6, 1)),
)


t_ext_obs_monthly = Table(
    "ext_obs_monthly",
    metadata,
    Column("id", Integer),
    Column("station_no", String(15)),
    Column("lsd", Date),
    Column("data_source", CHAR(2)),
    Column("insert_datetime", DateTime),
    Column("change_datetime", DateTime),
    Column("change_user", String(20)),
    Column("qa_flag", CHAR(1)),
    Column("comments", String(1000)),
    Column("dly_max_rain", Numeric(8, 1)),
    Column("dly_max_rain_inches", Numeric(8, 1)),
    Column("dly_max_rain_date", String(120)),
    Column("dly_max_rain_qa", CHAR(2)),
    Column("max_max_air_temp", Numeric(7, 1)),
    Column("max_max_air_temp_f", Numeric(7, 1)),
    Column("max_max_air_temp_qa", CHAR(2)),
    Column("max_max_air_temp_date", String(120)),
    Column("min_min_air_temp", Numeric(7, 1)),
    Column("min_min_air_temp_f", Numeric(7, 1)),
    Column("min_min_air_temp_qa", CHAR(2)),
    Column("min_min_air_temp_date", String(120)),
    Column("min_min_ground_temp", Numeric(7, 1)),
    Column("min_min_ground_temp_f", Numeric(7, 1)),
    Column("min_min_ground_temp_qa", CHAR(2)),
    Column("min_min_ground_temp_date", String(120)),
    Column("mn_air_temp", Numeric(7, 1)),
    Column("mn_air_temp_f", Numeric(7, 1)),
    Column("mn_air_temp_qa", CHAR(2)),
    Column("mn_max_air_temp", Numeric(7, 1)),
    Column("mn_max_air_temp_f", Numeric(7, 1)),
    Column("mn_max_air_temp_qa", CHAR(2)),
    Column("mn_min_air_temp", Numeric(7, 1)),
    Column("mn_min_air_temp_f", Numeric(7, 1)),
    Column("mn_min_air_temp_qa", CHAR(2)),
    Column("mn_wet_bulb_temp", Numeric(7, 1)),
    Column("mn_wet_bulb_temp_f", Numeric(7, 1)),
    Column("mn_wet_bulb_temp_qa", CHAR(2)),
    Column("mn_min_ground_temp", Numeric(7, 1)),
    Column("mn_min_ground_temp_f", Numeric(7, 1)),
    Column("mn_min_ground_temp_qa", CHAR(2)),
    Column("mn_asread_pres", Numeric(7, 1)),
    Column("mn_asread_pres_inches", Numeric(8, 3)),
    Column("mn_asread_pres_mmhg", Numeric(7, 2)),
    Column("mn_asread_pres_qa", CHAR(2)),
    Column("mn_msl_pres", Numeric(7, 1)),
    Column("mn_msl_pres_inches", Numeric(8, 3)),
    Column("mn_msl_pres_mmhg", Numeric(7, 2)),
    Column("mn_msl_pres_qa", CHAR(2)),
    Column("mn_station_pres", Numeric(7, 1)),
    Column("mn_station_pres_inches", Numeric(8, 3)),
    Column("mn_station_pres_mmhg", Numeric(7, 2)),
    Column("mn_station_pres_qa", CHAR(2)),
    Column("mn_vapour_pres", Numeric(7, 1)),
    Column("mn_vapour_pres_inches", Numeric(8, 3)),
    Column("mn_vapour_pres_mmhg", Numeric(7, 2)),
    Column("mn_vapour_pres_qa", CHAR(2)),
    Column("mn_evaporation", Numeric(4, 1)),
    Column("mn_evaporation_inches", Numeric(6, 3)),
    Column("mn_evaporation_qa", CHAR(2)),
    Column("mn_rel_humidity", Numeric(4, 1)),
    Column("mn_rel_humidity_qa", CHAR(2)),
    Column("mn_sun_hours", Numeric(4, 2)),
    Column("mn_sun_hours_qa", CHAR(2)),
    Column("mn_tot_cloud_oktas", Numeric(1, 0)),
    Column("mn_tot_cloud_tenths", Numeric(2, 0)),
    Column("mn_tot_cloud_qa", CHAR(2)),
    Column("tot_evaporation", Numeric(8, 1)),
    Column("tot_evaporation_inches", Numeric(9, 3)),
    Column("tot_evaporation_qa", CHAR(2)),
    Column("tot_rain", Numeric(8, 1)),
    Column("tot_rain_inches", Numeric(9, 3)),
    Column("tot_rain_qa", CHAR(2)),
    Column("tot_rain_days", Numeric(4, 0)),
    Column("tot_rain_days_qa", CHAR(2)),
    Column("tot_rain_percent", Numeric(4, 0)),
    Column("tot_rain_percent_qa", CHAR(2)),
)


t_ext_obs_monthly_calculated = Table(
    "ext_obs_monthly_calculated",
    metadata,
    Column("station_no", String(15)),
    Column("lsd", Date),
    Column("yyyy_mm", Text),
    Column("max_max_air_temp", Numeric),
    Column("min_min_air_temp", Numeric),
    Column("min_min_ground_temp", Numeric),
    Column("mn_min_ground_temp", Numeric),
    Column("mn_max_air_temp", Numeric),
    Column("mn_min_air_temp", Numeric),
    Column("mn_air_temp", Numeric),
    Column("dly_max_rain", Numeric),
    Column("tot_rain", Numeric),
    Column("tot_rain_days", Numeric),
    Column("tot_rain_percent", Float(53)),
    Column("mn_evaporation", Numeric),
    Column("tot_evaporation", Numeric),
    Column("mn_sun_hours", Numeric),
    Column("mn_asread_pres", Numeric),
    Column("mn_msl_pres", Numeric),
    Column("mn_station_pres", Numeric),
    Column("mn_vapour_pres", Numeric),
    Column("mn_rel_humidity", Numeric),
    Column("mn_tot_cloud_oktas", Numeric),
)


t_ext_obs_monthly_combined = Table(
    "ext_obs_monthly_combined",
    metadata,
    Column("source", Text),
    Column("station_no", String(15)),
    Column("yyyy_mm", Text),
    Column("lsd", Date),
    Column("max_max_air_temp", Numeric),
    Column("min_min_air_temp", Numeric),
    Column("min_min_ground_temp", Numeric),
    Column("mn_min_ground_temp", Numeric),
    Column("mn_max_air_temp", Numeric),
    Column("mn_min_air_temp", Numeric),
    Column("mn_air_temp", Numeric),
    Column("dly_max_rain", Numeric),
    Column("tot_rain", Numeric),
    Column("tot_rain_days", Numeric),
    Column("tot_rain_percent", Float(53)),
    Column("mn_evaporation", Numeric),
    Column("tot_evaporation", Numeric),
    Column("mn_sun_hours", Numeric),
    Column("mn_asread_pres", Numeric),
    Column("mn_msl_pres", Numeric),
    Column("mn_station_pres", Numeric),
    Column("mn_vapour_pres", Numeric),
    Column("mn_rel_humidity", Numeric),
    Column("mn_tot_cloud_oktas", Numeric),
)


t_ext_obs_subdaily = Table(
    "ext_obs_subdaily",
    metadata,
    Column("id", Integer),
    Column("station_no", String(15)),
    Column("lsd", DateTime),
    Column("gmt", DateTime),
    Column("lct", DateTime),
    Column("data_source", CHAR(2)),
    Column("insert_datetime", DateTime),
    Column("change_datetime", DateTime),
    Column("change_user", String(20)),
    Column("qa_flag", CHAR(1)),
    Column("aws_flag", CHAR(1)),
    Column("comments", String(1000)),
    Column("air_temp", Numeric(7, 1)),
    Column("air_temp_f", Numeric(7, 1)),
    Column("air_temp_qa", CHAR(2)),
    Column("sea_water_temp", Numeric(7, 1)),
    Column("sea_water_temp_f", Numeric(7, 1)),
    Column("sea_water_temp_qa", CHAR(2)),
    Column("wet_bulb", Numeric(7, 1)),
    Column("wet_bulb_f", Numeric(7, 1)),
    Column("wet_bulb_qa", CHAR(2)),
    Column("dew_point", Numeric(7, 1)),
    Column("dew_point_f", Numeric(7, 1)),
    Column("dew_point_qa", CHAR(2)),
    Column("rel_humidity", Numeric(4, 1)),
    Column("rel_humidity_qa", CHAR(2)),
    Column("baro_temp", Numeric(7, 1)),
    Column("baro_temp_f", Numeric(7, 1)),
    Column("baro_temp_qa", CHAR(2)),
    Column("pres_as_read", Numeric(7, 1)),
    Column("pres_as_read_inches", Numeric(8, 3)),
    Column("pres_as_read_qa", CHAR(2)),
    Column("station_pres", Numeric(7, 1)),
    Column("station_pres_inches", Numeric(8, 3)),
    Column("station_pres_qa", CHAR(2)),
    Column("msl_pres", Numeric(7, 1)),
    Column("msl_pres_inches", Numeric(8, 3)),
    Column("msl_pres_qa", CHAR(2)),
    Column("vapour_pres", Numeric(7, 1)),
    Column("vapour_pres_inches", Numeric(8, 3)),
    Column("vapour_pres_qa", CHAR(2)),
    Column("qnh", Numeric(7, 1)),
    Column("qnh_qa", CHAR(2)),
    Column("visibility", Numeric(7, 3)),
    Column("visibility_miles", Numeric(7, 3)),
    Column("visibility_code", CHAR(1)),
    Column("visibility_qa", CHAR(2)),
    Column("rain_3h", Numeric(7, 1)),
    Column("rain_3h_inches", Numeric(7, 3)),
    Column("rain_3h_qa", CHAR(2)),
    Column("rain_3h_hours", Numeric(3, 0)),
    Column("rain_cum", Numeric(7, 1)),
    Column("rain_cum_inches", Numeric(7, 3)),
    Column("rain_cum_qa", CHAR(2)),
    Column("wind_dir", Numeric(3, 0)),
    Column("wind_dir_qa", CHAR(2)),
    Column("wind_dir_std_dev", Numeric(3, 0)),
    Column("wind_dir_std_dev_qa", CHAR(2)),
    Column("wind_speed", Numeric(5, 1)),
    Column("wind_speed_knots", Numeric(5, 1)),
    Column("wind_speed_mph", Numeric(5, 1)),
    Column("wind_speed_bft", CHAR(2)),
    Column("wind_speed_qa", CHAR(2)),
    Column("pres_weather_code", String(2)),
    Column("pres_weather_bft", String(20)),
    Column("pres_weather_qa", CHAR(2)),
    Column("past_weather_code", String(2)),
    Column("past_weather_bft", String(20)),
    Column("past_weather_qa", CHAR(2)),
    Column("tot_cloud_oktas", SmallInteger),
    Column("tot_cloud_tenths", SmallInteger),
    Column("tot_cloud_qa", CHAR(2)),
    Column("tot_low_cloud_oktas", SmallInteger),
    Column("tot_low_cloud_tenths", SmallInteger),
    Column("tot_low_cloud_height", Integer),
    Column("tot_low_cloud_qa", CHAR(2)),
    Column("state_of_sea", String(2)),
    Column("state_of_sea_qa", CHAR(2)),
    Column("state_of_swell", String(2)),
    Column("state_of_swell_qa", CHAR(2)),
    Column("swell_direction", String(3)),
    Column("swell_direction_qa", CHAR(2)),
    Column("sea_level", Numeric(5, 3)),
    Column("sea_level_qa", CHAR(2)),
    Column("sea_level_residual", Numeric(5, 3)),
    Column("sea_level_residual_qa", CHAR(2)),
    Column("sea_level_resid_adj", Numeric(5, 3)),
    Column("sea_level_resid_adj_qa", CHAR(2)),
    Column("radiation", Numeric(6, 1)),
    Column("radiation_qa", CHAR(2)),
    Column("sunshine", Numeric(3, 1)),
    Column("sunshine_qa", CHAR(2)),
    Column("tot_low_cloud_height_feet", Integer),
    Column("wind_gust_kts", Numeric(3, 0)),
    Column("wind_gust", Numeric(6, 1)),
    Column("wind_gust_qa", CHAR(2)),
    Column("wind_gust_dir", Numeric(3, 0)),
    Column("wind_gust_dir_qa", CHAR(2)),
)


t_ext_obs_subdaily_cloud_layers = Table(
    "ext_obs_subdaily_cloud_layers",
    metadata,
    Column("station_no", String(15)),
    Column("lsd", DateTime),
    Column("layer_no", Integer),
    Column("layer_type", String(6)),
    Column("cloud_oktas", SmallInteger),
    Column("cloud_tenths", SmallInteger),
    Column("cloud_amt_qa", CHAR(2)),
    Column("cloud_type", String(2)),
    Column("cloud_type_qa", CHAR(2)),
    Column("cloud_height", Numeric(6, 0)),
    Column("cloud_height_feet", Numeric(7, 0)),
    Column("cloud_height_qa", CHAR(2)),
    Column("cloud_dir", Numeric(3, 0)),
    Column("cloud_dir_qa", CHAR(2)),
    Column("data_source", CHAR(2)),
    Column("insert_datetime", DateTime),
    Column("change_datetime", DateTime),
    Column("change_user", String(20)),
    Column("qa_flag", CHAR(1)),
    Column("aws_flag", CHAR(1)),
)


t_ext_obs_subdaily_soil_temps = Table(
    "ext_obs_subdaily_soil_temps",
    metadata,
    Column("station_no", String(15)),
    Column("lsd", DateTime),
    Column("soil_depth", Numeric(5, 0)),
    Column("soil_temp", Numeric(7, 1)),
    Column("soil_temp_f", Numeric(7, 1)),
    Column("soil_temp_qa", CHAR(2)),
    Column("change_user", String(20)),
    Column("insert_datetime", DateTime),
    Column("change_datetime", DateTime),
    Column("qa_flag", CHAR(1)),
    Column("aws_flag", CHAR(1)),
)


t_ext_obs_upper_air = Table(
    "ext_obs_upper_air",
    metadata,
    Column("id", Integer),
    Column("station_no", String(15)),
    Column("lsd", DateTime),
    Column("gmt", DateTime),
    Column("lct", DateTime),
    Column("data_source", CHAR(2)),
    Column("insert_datetime", DateTime),
    Column("change_datetime", DateTime),
    Column("change_user", String(20)),
    Column("qa_flag", CHAR(1)),
    Column("pressure", Numeric(7, 1)),
    Column("pressure_qa", CHAR(2)),
    Column("level_type", Numeric(2, 0)),
    Column("geo_height", Numeric(8, 1)),
    Column("geo_height_qa", CHAR(2)),
    Column("air_temp", Numeric(7, 1)),
    Column("air_temp_qa", CHAR(2)),
    Column("dew_point", Numeric(4, 1)),
    Column("dew_point_qa", CHAR(2)),
    Column("wind_direction", Numeric(4, 0)),
    Column("wind_direction_qa", CHAR(2)),
    Column("wind_speed", Numeric(5, 1)),
    Column("wind_speed_qa", CHAR(2)),
)


t_ext_station_audit = Table(
    "ext_station_audit",
    metadata,
    Column("station_no", String(15)),
    Column("station_name", String(40)),
    Column("datetime", DateTime(True)),
    Column("audit_type_id", Integer),
    Column("audit_type_description", String(50)),
    Column("event_description", Text),
    Column("user", String(40)),
)


t_ext_station_class = Table(
    "ext_station_class",
    metadata,
    Column("station_no", String(15)),
    Column("station_name", String(40)),
    Column("class", String(10)),
    Column("class_description", String(50)),
    Column("class_start", DateTime),
    Column("class_end", DateTime),
    Column("description", String(80)),
)


t_ext_station_equipment = Table(
    "ext_station_equipment",
    metadata,
    Column("station_no", String(15)),
    Column("station_name", String(40)),
    Column("equipment_type", String(50)),
    Column("equipment_version", String(50)),
    Column("equipment_comments", String(1000)),
    Column("serial_no", String(50)),
    Column("asset_id", String(50)),
    Column("height", Numeric(7, 3)),
    Column("date_start", Date),
    Column("date_end", Date),
    Column("comments", String(1000)),
)


t_ext_stations = Table(
    "ext_stations",
    metadata,
    Column("id", Integer),
    Column("station_no", String(15)),
    Column("name_primary", String(40)),
    Column("name_secondary", String(40)),
    Column("region", String(40)),
    Column("catchment", String(40)),
    Column("authority", String(50)),
    Column("status", String(50)),
    Column("start_date", Date),
    Column("end_date", Date),
    Column("aero_height", Numeric(6, 1)),
    Column("station_elevation", Numeric(7, 3)),
    Column("latitude", Numeric(8, 4)),
    Column("longitude", Numeric(8, 4)),
    Column("time_zone", String(3)),
    Column("utc_offset", Numeric(4, 1)),
    Column("timezone_description", String(50)),
    Column("id_aero", String(10)),
    Column("id_imo", String(10)),
    Column("id_marine", String(10)),
    Column("id_wmo", String(10)),
    Column("id_hydro", String(10)),
    Column("id_aust", String(10)),
    Column("id_niwa", String(10)),
    Column("id_niwa_agent", String(10)),
    Column("country_code", String(4)),
    Column("country_description", String(50)),
    Column("lu_0_100m", Integer),
    Column("land_use_0_100m", String(100)),
    Column("lu_100m_1km", Integer),
    Column("land_use_100m_1km", String(100)),
    Column("lu_1km_10km", Integer),
    Column("land_use_1km_10km", String(100)),
    Column("comments", String(1000)),
)
# endregion


class CodesSimple(Base):
    __tablename__ = "codes_simple"
    __table_args__ = (
        UniqueConstraint("code_type", "code"),
        {"comment": "List of codes used in CliDE"},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    code_type = Column(String(40), nullable=False, comment="Character code type")
    code = Column(String(40), nullable=False)
    description = Column(String(400), comment="Description of code")
    change_user = Column(String(10), comment="User of last change")
    change_datetime = Column(DateTime, comment="Timestamp of last change")
    insert_datetime = Column(DateTime, nullable=False, comment="Timestamp of insert")


class Datum(Base):
    __tablename__ = "datums"
    __table_args__ = {"comment": "Geodetic datums"}

    datum_name = Column(String(20), primary_key=True)
    description = Column(String(100))


class Equipment(Base):
    __tablename__ = "equipment"
    __table_args__ = {"comment": "Stores equipment master information."}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    type = Column(String(50), comment="Type of equipment")
    comments = Column(String(1000), comment="Comments for equipment")
    version = Column(String(50), comment="Version of equipment")


class GuiUser(Base):
    __tablename__ = "gui_users"
    __table_args__ = {"comment": "User data for web GUI"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    username = Column(String(20), nullable=False, unique=True, comment="Login user id")
    css_filename = Column(String(120), comment="Name of style sheet selected")
    layout = Column(
        CHAR(4),
        autoincrement=True,
        comment="Layout of page: LEFT menu, top menu, popup menu, HTML",
    )
    key = Column(String(64))
    disabled = Column(CHAR(1))
    disable_date = Column(DateTime(True))
    station_maint = Column(CHAR(1), nullable=False, server_default=text("'N'::bpchar"))
    codes_maint = Column(CHAR(1), nullable=False, server_default=text("'N'::bpchar"))
    user_admin = Column(CHAR(1), nullable=False, server_default=text("'N'::bpchar"))
    file_ingest = Column(CHAR(1), nullable=False, server_default=text("'N'::bpchar"))
    key_entry = Column(CHAR(1), nullable=False, server_default=text("'N'::bpchar"))
    qa = Column(CHAR(1), nullable=False, server_default=text("'N'::bpchar"))
    products = Column(CHAR(1), nullable=False, server_default=text("'N'::bpchar"))


class IngestMonitor(Base):
    __tablename__ = "ingest_monitor"
    __table_args__ = {"comment": "Stores file ingestion stats for data ingests"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    username = Column(String(20), nullable=False, comment="User that started ingest")
    ip_addr = Column(
        String(20), comment="Client IP address where ingest was invoked from"
    )
    filename = Column(String(200), comment="File name of file being ingested")
    ingest_start = Column(
        DateTime,
        nullable=False,
        server_default=text("now()"),
        comment="Ingest start time",
    )
    ingest_end = Column(DateTime, comment="Ingest end time")
    file_recs = Column(Integer, comment="Count of all input file records")
    ingested_recs = Column(Integer, comment="Count of all ingested input file records")
    ok_count = Column(Integer)
    err_count = Column(Integer)
    cancel_flag = Column(CHAR(1))
    cancel_user = Column(String(20))
    change_datetime = Column(DateTime)


class KeySetting(Base):
    __tablename__ = "key_settings"
    __table_args__ = (
        UniqueConstraint("profile", "element", "obs_type"),
        {"comment": "Stores key entry settings: Default units, disable flag"},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    profile = Column(String(20), nullable=False, comment="profile name")
    obs_type = Column(String(20), comment="obsservation type: daily, subdaily")
    element = Column(String(120), comment="observation element")
    default_unit = Column(String(20), comment="Default unit in key entry forms")
    disable_flag = Column(CHAR(1), comment="Y=disable in entry forms")
    change_user = Column(String(20))
    change_datetime = Column(DateTime)


class LandUse(Base):
    __tablename__ = "land_use"
    __table_args__ = {"comment": "Stores allowed values for stations.soil_type_id"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    land_use_code = Column(
        String(10), nullable=False, unique=True, comment="Land usage code"
    )
    priority = Column(Integer, nullable=False, comment="Land usage priority")
    description = Column(String(100), comment="Land use description")


class ObsAudit(Base):
    __tablename__ = "obs_audit"
    __table_args__ = (
        Index("obs_audit_row_id_idx", "row_id"),
        {"comment": "Audit trail of all changes to station Station."},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    table_name = Column(String(100), comment="Observation table where data is changed")
    row_id = Column(Integer, comment="Row id of changed data")
    column_name = Column(String(100), comment="Column that has been changed")
    column_value = Column(String(4000))
    change_user = Column(String(20), comment="User performing the change")
    datetime = Column(DateTime(True), comment="Datetime of change")


class ObsAverage(Base):
    __tablename__ = "obs_averages"
    __table_args__ = (
        UniqueConstraint("name", "station_no", "month"),
        {"comment": "Normals and other monthly long term averages of observations."},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    insert_datetime = Column(DateTime, nullable=False, server_default=text("now()"))
    change_datetime = Column(DateTime)
    change_user = Column(String(20))
    station_no = Column(String(20), nullable=False)
    month = Column(SmallInteger, nullable=False, comment="Month of averages")
    name = Column(String(60), nullable=False, comment="Name of this set of averages")
    active_normal = Column(CHAR(1))
    from_date = Column(
        Date, nullable=False, comment="Start date of observations in this average set"
    )
    to_date = Column(
        Date, nullable=False, comment="End date of observations in this average set"
    )
    station_pres = Column(
        Numeric(7, 1),
        comment="Average Station Pressure: from obs_subdaily.station_pres",
    )
    msl_pres = Column(
        Numeric(7, 1), comment="Average MSL Pressure: from obs_subdaily.msl_pres"
    )
    air_temp = Column(
        Numeric(7, 1), comment="Average air temp: from obs_subdaily.air_temp"
    )
    max_air_temp = Column(
        Numeric(7, 1), comment="Average max air temp: from obs_daily.max_air_temp"
    )
    min_air_temp = Column(
        Numeric(7, 1), comment="Average min air temp: from obs_daily.min_air_temp"
    )
    vapour_pres = Column(
        Numeric(7, 1), comment="Average vapour pressure: from obs_subdaily.dew_point"
    )
    rainfall = Column(
        Numeric(7, 1), comment="Avg Total monthly rainfall. from obs_daily.rain_24h"
    )
    rain_days = Column(
        SmallInteger,
        comment="Avg Total monthly rain days. from obs_daily.rain_24h_count",
    )
    sun_hours = Column(
        SmallInteger,
        comment="Avg monthly sunshine hours. from obs_daily.sunshine_duration",
    )
    missing_station_pres = Column(
        SmallInteger,
        comment="Number of years missing from the record of normal station pressure",
    )
    missing_air_temp = Column(
        SmallInteger,
        comment="Number of years missing from the record of normal air temp",
    )
    missing_max_min = Column(
        SmallInteger,
        comment="Number of years missing from the record of normal daily max or min air temp",
    )
    missing_vapour_pres = Column(
        SmallInteger,
        comment="Number of years missing from the record of normal daily vapour pres",
    )
    missing_rainfall = Column(
        SmallInteger,
        comment="Number of years missing from the record of normal daily rainfall",
    )
    missing_sun_hours = Column(
        SmallInteger,
        comment="Number of years missing from the record of normal daily sunshine hours",
    )
    air_temp_stddev = Column(Numeric(7, 1), comment="Std Deviation of air temp")


class ObsClicomElementMap(Base):
    __tablename__ = "obs_clicom_element_map"
    __table_args__ = {"comment": "Mapping Clicom Codes to CLDB table, column"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    clicom_element = Column(String(5), nullable=False)
    cldb_table = Column(String(80), nullable=False)
    cldb_column = Column(String(80), nullable=False)
    associated_col = Column(String(80))
    associated_value = Column(String(100))
    column_type = Column(String(4), server_default=text("'num'::character varying"))
    nominal_value = Column(String(20))


class ObsMonthly(Base):
    __tablename__ = "obs_monthly"
    __table_args__ = (
        UniqueConstraint("station_no", "lsd"),
        Index("obs_monthly_lsd_idx", "lsd"),
        {"comment": "Stores monthly data not available as daily or subdaily"},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    station_no = Column(String(15), nullable=False, comment="Local Station identifier")
    lsd = Column(Date, nullable=False, comment="Local System Year and Month")
    data_source = Column(
        CHAR(2), comment="Code for data source, see codes_simple for code_type=DATA_SRC"
    )
    insert_datetime = Column(DateTime, comment="Date/Time row is inserted")
    change_datetime = Column(DateTime, comment="Date/Time row is updated")
    change_user = Column(String(20), comment="User who added/changed row")
    qa_flag = Column(CHAR(1), comment="QA flag for row Y/N")
    comments = Column(String(1000), comment="User comments")
    dly_max_rain = Column(Numeric(8, 1), comment="Highest Daily precipitation mm")
    dly_max_rain_inches = Column(
        Numeric(8, 1), comment="Highest Daily precipitation (inches to .001)"
    )
    dly_max_rain_date = Column(
        String(120), comment="Date(s) of highest rain as dd,dd,dd,..."
    )
    dly_max_rain_qa = Column(CHAR(2))
    max_max_air_temp = Column(
        Numeric(7, 1), comment="Highest daily maximum air temp (C to 0.1)"
    )
    max_max_air_temp_f = Column(
        Numeric(7, 1), comment="Highest daily maximum air temp (F to 0.1)"
    )
    max_max_air_temp_qa = Column(CHAR(2))
    max_max_air_temp_date = Column(
        String(120), comment="Date(s) of highest max air temp as dd,dd,dd,..."
    )
    min_min_air_temp = Column(
        Numeric(7, 1), comment="Lowest daily minimum air temp (C to 0.1)"
    )
    min_min_air_temp_f = Column(
        Numeric(7, 1), comment="Lowest daily minimum air temp (F to 0.1)"
    )
    min_min_air_temp_qa = Column(CHAR(2))
    min_min_air_temp_date = Column(
        String(120), comment="Date(s) of lowest daily min as dd,dd,dd,..."
    )
    min_min_ground_temp = Column(
        Numeric(7, 1), comment="Lowest minimum daily ground temp (C to 0.1)"
    )
    min_min_ground_temp_f = Column(
        Numeric(7, 1), comment="Lowest minimum daily ground temp (F to 0.1)"
    )
    min_min_ground_temp_qa = Column(CHAR(2))
    min_min_ground_temp_date = Column(
        String(120), comment="Date(s) of lowest daily ground min as dd,dd,dd,..."
    )
    mn_air_temp = Column(Numeric(7, 1), comment="Mean air temperature (C to 0.1)")
    mn_air_temp_f = Column(Numeric(7, 1), comment="Mean air temperature (F to 0.1)")
    mn_air_temp_qa = Column(CHAR(2))
    mn_max_air_temp = Column(
        Numeric(7, 1), comment="Mean of maximum daily air temp (C to 0.1)"
    )
    mn_max_air_temp_f = Column(
        Numeric(7, 1), comment="Mean of maximum daily air temp (F to 0.1)"
    )
    mn_max_air_temp_qa = Column(CHAR(2))
    mn_min_air_temp = Column(
        Numeric(7, 1), comment="Mean of minimum daily air temp (C to 0.1)"
    )
    mn_min_air_temp_f = Column(
        Numeric(7, 1), comment="Mean of minimum daily air temp (F to 0.1)"
    )
    mn_min_air_temp_qa = Column(CHAR(2))
    mn_wet_bulb_temp = Column(
        Numeric(7, 1), comment="Mean wet bulb temperature (C to 0.1)"
    )
    mn_wet_bulb_temp_f = Column(
        Numeric(7, 1), comment="Mean wet bulb temperature (F to 0.1)"
    )
    mn_wet_bulb_temp_qa = Column(CHAR(2))
    mn_min_ground_temp = Column(
        Numeric(7, 1), comment="Mean of minimum daily ground temp (C to 0.1)"
    )
    mn_min_ground_temp_f = Column(
        Numeric(7, 1), comment="Mean of minimum daily ground temp (F to 0.1)"
    )
    mn_min_ground_temp_qa = Column(CHAR(2))
    mn_asread_pres = Column(Numeric(7, 1), comment="Mean as read pressure (hPa to 0.1)")
    mn_asread_pres_inches = Column(
        Numeric(8, 3), comment="Mean as read pressure (inches to 0.001)"
    )
    mn_asread_pres_mmhg = Column(
        Numeric(7, 2), comment="Mean as read pressure (mmHg to 0.01)"
    )
    mn_asread_pres_qa = Column(CHAR(2))
    mn_msl_pres = Column(Numeric(7, 1), comment="Mean MSL pressure (hPa to 0.1)")
    mn_msl_pres_inches = Column(
        Numeric(8, 3), comment="Mean MSL pressure (inches to 0.001)"
    )
    mn_msl_pres_mmhg = Column(Numeric(7, 2), comment="Mean MSL pressure (mmHg to 0.01)")
    mn_msl_pres_qa = Column(CHAR(2))
    mn_station_pres = Column(
        Numeric(7, 1), comment="Mean station level pressure (hPa to 0.1)"
    )
    mn_station_pres_inches = Column(
        Numeric(8, 3), comment="Mean station level pressure (inches to 0.001)"
    )
    mn_station_pres_mmhg = Column(
        Numeric(7, 2), comment="Mean station level pressure (mmHg to 0.01)"
    )
    mn_station_pres_qa = Column(CHAR(2))
    mn_vapour_pres = Column(Numeric(7, 1), comment="Mean Vapour Pressure (hPa to 0.1)")
    mn_vapour_pres_inches = Column(
        Numeric(8, 3), comment="Mean Vapour Pressure (Inches to 0.001)"
    )
    mn_vapour_pres_mmhg = Column(
        Numeric(7, 2), comment="Mean Vapour Pressure (mmHg to 0.01)"
    )
    mn_vapour_pres_qa = Column(CHAR(2))
    mn_evaporation = Column(
        Numeric(4, 1), comment="Mean of daily evaporation (mm to 0.1)"
    )
    mn_evaporation_inches = Column(
        Numeric(6, 3), comment="Mean of daily evaporation (Inches to 0.001)"
    )
    mn_evaporation_qa = Column(CHAR(2))
    mn_rel_humidity = Column(Numeric(4, 1), comment="Mean Relative Humidity (% to 0.1)")
    mn_rel_humidity_qa = Column(CHAR(2))
    mn_sun_hours = Column(
        Numeric(4, 2), comment="Mean of daily bright sunshine (hours to 0.01)"
    )
    mn_sun_hours_qa = Column(CHAR(2))
    mn_tot_cloud_oktas = Column(
        Numeric(1, 0), comment="Mean of Daily Total Cloud Amt (Octas 0-9)"
    )
    mn_tot_cloud_tenths = Column(
        Numeric(2, 0), comment="Mean of Daily Total Cloud Amt (Tenths 0-10)"
    )
    mn_tot_cloud_qa = Column(CHAR(2))
    tot_evaporation = Column(
        Numeric(8, 1), comment="Total Monthly evaporation (mm to 0.1)"
    )
    tot_evaporation_inches = Column(
        Numeric(9, 3), comment="Total Monthly evaporation (Inches to 0.001)"
    )
    tot_evaporation_qa = Column(CHAR(2))
    tot_rain = Column(Numeric(8, 1), comment="Total monthly precipitation  (mm to 0.1)")
    tot_rain_inches = Column(
        Numeric(9, 3), comment="Total monthly precipitation  (Inches to 0.001)"
    )
    tot_rain_qa = Column(CHAR(2))
    tot_rain_days = Column(Numeric(4, 0), comment="Number of rain days")
    tot_rain_days_qa = Column(CHAR(2))
    tot_rain_percent = Column(
        Numeric(4, 0),
        comment="Percentage complete (not missing) of daily records for month",
    )
    tot_rain_percent_qa = Column(CHAR(2))


class ObsSubdailySoilTemp(Base):
    __tablename__ = "obs_subdaily_soil_temps"
    __table_args__ = (
        Index("fki_obs_subdaily_soil_temps_subdaily_id_fkey", "sub_daily_id"),
        {"comment": "Sub Daily surface observations"},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    sub_daily_id = Column(
        Integer,
        nullable=False,
        comment="Surrogate key of parent sub daily row",
    )
    data_source = Column(CHAR(2), nullable=False, server_default=text("'1'::bpchar"))
    insert_datetime = Column(DateTime, nullable=False, server_default=text("now()"))
    change_datetime = Column(DateTime)
    change_user = Column(String(20))
    qa_flag = Column(CHAR(1), nullable=False, server_default=text("'N'::bpchar"))
    aws_flag = Column(CHAR(1), nullable=False, server_default=text("'N'::bpchar"))
    soil_depth = Column(Numeric(5, 0), nullable=False, comment="Soil depth in cm")
    soil_temp = Column(Numeric(7, 1), comment="Soil Temperature (C to 0.1)")
    soil_temp_f = Column(Numeric(7, 1), comment="Soil Temperature (F to 0.1)")
    soil_temp_qa = Column(CHAR(2), comment="Quality Code for soil_temp")


class ObscodesCloudAmtConv(Base):
    __tablename__ = "obscodes_cloud_amt_conv"
    __table_args__ = {"comment": "Cloud Amount conversions"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    code_0501 = Column(CHAR(1), comment="WMO Code 0501 code form")
    code_2700 = Column(CHAR(1), comment="WMO Code 2700 code form")
    code_bft = Column(String(10), comment="Beaufort code")
    tenths = Column(
        String(5), comment="Tenths (Can be multiple values comma separated)"
    )
    oktas = Column(CHAR(1), comment="Oktas (1-9)")
    change_user = Column(String(10), comment="User of last change")
    change_datetime = Column(DateTime, comment="Timestamp of last change")
    insert_datetime = Column(DateTime, nullable=False, comment="Timestamp of insert")


class ObscodesCloudConv1677(Base):
    __tablename__ = "obscodes_cloud_conv_1677"
    __table_args__ = {"comment": "Cloud Height conversions for WMO 1677"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    code = Column(String(2), comment="WMO 1677 code")
    low_feet = Column(Numeric(7, 0), comment="Lower bound in feet")
    low_meters = Column(Numeric(7, 0), comment="Lower bound in M")
    change_user = Column(String(10), comment="User of last change")
    change_datetime = Column(DateTime, comment="Timestamp of last change")
    insert_datetime = Column(DateTime, comment="Timestamp of insert")


class ObscodesCloudHtConv(Base):
    __tablename__ = "obscodes_cloud_ht_conv"
    __table_args__ = {"comment": "Cloud Height conversions"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    code = Column(CHAR(1), comment="WMO 1600 Code")
    low_feet = Column(Numeric(9, 0), comment="Lower bound in feet")
    high_feet = Column(Numeric(9, 0), comment="Upper bound in Feet")
    low_meters = Column(Numeric(7, 0), comment="Lower Bound in M")
    high_meters = Column(Numeric(7, 0), comment="Upper Bound in M")
    change_user = Column(String(10), comment="User of last change")
    change_datetime = Column(DateTime, comment="Timestamp of last change")
    insert_datetime = Column(DateTime, comment="Timestamp of insert")


class ObscodesCloudTypeConv(Base):
    __tablename__ = "obscodes_cloud_type_conv"
    __table_args__ = {"comment": "Cloud Type conversions"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    code_0500 = Column(CHAR(1))
    code_figure = Column(CHAR(1), comment="WMO Code figure")
    wmo_table = Column(CHAR(4), comment="WMO Table no (0513 Low, 0515 Mid, 0509 High)")
    layer = Column(String(4), comment="Cloud Layer: Low, Mid, High")
    types = Column(String(10), comment="Acceptable Cloud types")
    change_user = Column(String(10), comment="User of last change")
    change_datetime = Column(DateTime, comment="Timestamp of last change")
    insert_datetime = Column(DateTime, comment="Timestamp of insert")


class ObscodesVisibility(Base):
    __tablename__ = "obscodes_visibility"
    __table_args__ = {
        "comment": "Visibility conversions: Aero, non-Aero, Km, yards. WMO 4300"
    }

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    non_aero_scale = Column(
        String(2), nullable=False, comment="Visibility non-Aero scale"
    )
    distance_km = Column(Numeric(5, 2), comment="Distance in Km")
    distance_yards = Column(Numeric(7, 0), comment="Distance in Yards")
    valid_aero_codes = Column(String(100), comment="Valid Aero codes, comma sep")
    code = Column(CHAR(1))
    change_user = Column(String(10), comment="User of last change")
    change_datetime = Column(DateTime, comment="Timestamp of last change")
    insert_datetime = Column(DateTime, comment="Timestamp of insert")


class ObscodesWindDir(Base):
    __tablename__ = "obscodes_wind_dir"
    __table_args__ = {
        "comment": "Wind Direction conversions: Compass points to degrees"
    }

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    compass = Column(String(6), nullable=False, comment="Compass points: NNE, SE, CLM,")
    degrees = Column(Numeric(3, 0), comment="Degrees (0-360)")
    low_degrees = Column(Numeric(5, 2), comment="Lower bound in degrees (>)")
    high_degrees = Column(Numeric(5, 2), comment="Upper bound in degrees (<=)")
    change_user = Column(String(10), comment="User of last change")
    change_datetime = Column(DateTime, comment="Timestamp of last change")
    insert_datetime = Column(DateTime, comment="Timestamp of insert")


class ObscodesWindSpeed(Base):
    __tablename__ = "obscodes_wind_speed"
    __table_args__ = {"comment": "Wind speed conversions: Beaufort, m/s, knots"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    code_bft = Column(String(2), nullable=False, comment="Beaufort code")
    ms = Column(Numeric(5, 2), comment="M/S")
    low_ms = Column(Numeric(5, 2), comment="Lower bound in M/S")
    high_ms = Column(Numeric(5, 2), comment="Upper bound in M/S")
    low_knots = Column(Numeric(5, 2), comment="Lower bound in Knots")
    high_knots = Column(Numeric(5, 2), comment="Upper bound in Knots")
    change_user = Column(String(10), comment="User of last change")
    change_datetime = Column(DateTime, comment="Timestamp of last change")
    insert_datetime = Column(DateTime, comment="Timestamp of insert")


class ObscodesWx(Base):
    __tablename__ = "obscodes_wx"
    __table_args__ = {"comment": "WMO Code 4677 (WX codes)"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    code = Column(String(2), nullable=False, comment="WMO 4677 code")
    name = Column(String(40), comment="Name of phenomenon")
    description = Column(String(200), comment="Description of phenomenon")
    change_user = Column(String(10), comment="User of last change")
    change_datetime = Column(DateTime, comment="Timestamp of last change")
    insert_datetime = Column(DateTime, comment="Timestamp of insert")


class ObsconvFactor(Base):
    __tablename__ = "obsconv_factors"
    __table_args__ = {"comment": "WMO Code 4677 (WX codes)"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    from_type = Column(
        String(20), nullable=False, comment="From unit (eg. Fahrenheit, Inches)"
    )
    to_type = Column(String(20), nullable=False, comment="To unit (eg. Celsius, mm)")
    pre_sum = Column(
        Numeric(5, 2), comment="Value to add prior to multiplying conversion factor"
    )
    mult_factor = Column(
        Numeric(7, 4), nullable=False, comment="Conversion factor. Multiplied by From."
    )
    post_sum = Column(
        Numeric(7, 4), comment="Value to add after multiplying conversion factor."
    )
    change_user = Column(String(10), comment="User of last change")
    change_datetime = Column(DateTime, comment="Timestamp of last change")
    insert_datetime = Column(DateTime, nullable=False, comment="Timestamp of insert")


class Pivot(Base):
    __tablename__ = "pivot"
    __table_args__ = {"comment": "Utility table of sequential integers"}

    i = Column(Integer, primary_key=True)


class SoilType(Base):
    __tablename__ = "soil_types"
    __table_args__ = {"comment": "Stores allowed values for stations.soil_type_id"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    soil_type = Column(String(10), nullable=False, comment="Soil type code")
    description = Column(String(50), comment="Soil type description")


class SpatialRefSy(Base):
    __tablename__ = "spatial_ref_sys"
    __table_args__ = {"comment": "Spatial reference system definitions from PostGIS"}

    srid = Column(Integer, primary_key=True)
    auth_name = Column(String(256))
    auth_srid = Column(Integer)
    srtext = Column(String(2048))
    proj4text = Column(String(2048))


class StationAuditType(Base):
    __tablename__ = "station_audit_types"
    __table_args__ = {"comment": "Stores allowed values for station_audit.type_id"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    audit_type = Column(
        String(10), nullable=False, unique=True, comment="Audit type code"
    )
    description = Column(String(50), comment="Description of audit type")
    system_type = Column(CHAR(1), nullable=False, server_default=text("'N'::bpchar"))


class StationCountry(Base):
    __tablename__ = "station_countries"
    __table_args__ = {"comment": "Stores countries that stations can belong to."}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    iso_code = Column(
        String(4),
        nullable=False,
        unique=True,
        comment="International ISO country code 3166",
    )
    description = Column(String(50), comment="Country Name")


class StationStatu(Base):
    __tablename__ = "station_status"
    __table_args__ = {"comment": "Stores allowed values for stations.status_id"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    status = Column(String(10), nullable=False, comment="Status Code")
    description = Column(String(50), comment="Description of status")


class StationTimezone(Base):
    __tablename__ = "station_timezones"
    __table_args__ = {"comment": "Stores time zone that stations can be in."}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    tm_zone = Column(String(3), nullable=False, unique=True, comment="Time zone code")
    utc_diff = Column(
        Numeric(4, 1),
        nullable=False,
        comment="Adjustment ADDED to get local standard time",
    )
    description = Column(String(50), comment="Description of time zone")


class StationType(Base):
    __tablename__ = "station_types"
    __table_args__ = {"comment": "Stores allowed values for stations.type_id"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    station_type = Column(String(10), nullable=False, comment="Station type code")
    description = Column(String(50), comment="Station type description")


class SurfaceType(Base):
    __tablename__ = "surface_types"
    __table_args__ = {"comment": "Stores allowed values for stations.surface_type_id"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    surface_type = Column(String(10), nullable=False, comment="Surface type code")
    description = Column(String(50), comment="Surface type description")


class UserSession(Base):
    __tablename__ = "user_sessions"
    __table_args__ = {"comment": "Stores User session information"}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    username = Column(String(20), nullable=False, comment="Login username")
    environment = Column(String(20), nullable=False)
    ip_addr = Column(String(20), comment="IP of client")
    start_timestamp = Column(
        DateTime,
        nullable=False,
        server_default=text("now()"),
        comment="Start of session",
    )
    end_timestamp = Column(DateTime, comment="End of session")
    logout_flag = Column(CHAR(1))
    timeout_flag = Column(CHAR(1), comment="Session ended by timeout")
    killed_flag = Column(CHAR(1), comment="Session ended by admin kill")


class Station(Base):
    __tablename__ = "stations"
    __table_args__ = (
        Index("fki_stations_country_code_fkey", "country_code"),
        Index("fki_stations_time_zone_fkey", "time_zone"),
        Index("fki_stations_soil_type_id_fkey", "soil_type"),
        Index("fki_stations_status_id_fkey", "status_id"),
        Index("fki_stations_surface_type_id_fkey", "surface_type"),
        Index("fki_stations_land_use_0_id_fkey", "lu_0_100m"),
        Index("fki_stations_land_use_100_id_fkey", "lu_100m_1km"),
        Index("fki_stations_land_use_1km_id_fkey", "lu_1km_10km"),
        UniqueConstraint("id_wmo", "start_date"),
        {"comment": "Stores station data."},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    station_no = Column(String(15), nullable=False, unique=True)
    status_id = Column(
        ForeignKey("station_status.id"),
        nullable=False,
        comment="Station status ID joins to station_status",
    )
    time_zone = Column(ForeignKey("station_timezones.tm_zone"), nullable=False)
    id_aero = Column(String(10))
    id_imo = Column(String(10))
    id_marine = Column(String(10))
    id_wmo = Column(String(10))
    id_hydro = Column(String(10))
    id_aust = Column(String(10))
    id_niwa = Column(String(10))
    id_niwa_agent = Column(String(10))
    comments = Column(String(1000))
    country_code = Column(ForeignKey("station_countries.iso_code"))
    start_date = Column(Date)
    end_date = Column(Date)
    ht_aero = Column(Numeric(6, 1))
    ht_elev = Column(Numeric(7, 3))
    ht_ssb = Column(Numeric(7, 4))
    latitude = Column(Numeric(8, 4))
    longitude = Column(Numeric(8, 4))
    name_primary = Column(String(40))
    name_secondary = Column(String(40))
    region = Column(String(40))
    catchment = Column(String(40))
    authority = Column(String(50))
    lu_0_100m = Column(ForeignKey("land_use.id"))
    lu_100m_1km = Column(ForeignKey("land_use.id"))
    lu_1km_10km = Column(ForeignKey("land_use.id"))
    soil_type = Column(ForeignKey("soil_types.id"))
    surface_type = Column(ForeignKey("surface_types.id"))
    critical_river_height = Column(
        Numeric(7, 3), comment="Critical River height (eg. Flood level) in M"
    )
    location_datum = Column(ForeignKey("datums.datum_name", onupdate="CASCADE"))
    location_epsg = Column(ForeignKey("spatial_ref_sys.srid", onupdate="CASCADE"))

    station_country = relationship("StationCountry")
    datum = relationship("Datum")
    spatial_ref_sy = relationship("SpatialRefSy")
    land_use = relationship("LandUse", primaryjoin="Station.lu_0_100m == LandUse.id")
    land_use1 = relationship("LandUse", primaryjoin="Station.lu_100m_1km == LandUse.id")
    land_use2 = relationship("LandUse", primaryjoin="Station.lu_1km_10km == LandUse.id")
    soil_type1 = relationship("SoilType")
    status = relationship("StationStatu")
    surface_type1 = relationship("SurfaceType")
    station_timezone = relationship("StationTimezone")


class TimezoneDiff(Base):
    __tablename__ = "timezone_diffs"
    __table_args__ = (
        Index("fki_timezone_diffs", "tm_zone"),
        {"comment": "Stores timezone differences due to daylight savings"},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    start_timestamp = Column(
        DateTime, nullable=False, comment="Date time difference starts"
    )
    end_timestamp = Column(
        DateTime, nullable=False, comment="Date time difference ends"
    )
    tm_zone = Column(
        ForeignKey("station_timezones.tm_zone"),
        nullable=False,
        comment="Time zone where difference applies",
    )
    tm_diff = Column(Numeric(4, 1), comment="UTC offset during this period")

    station_timezone = relationship("StationTimezone")


class ObsAero(Base):
    __tablename__ = "obs_aero"
    __table_args__ = (
        Index("obs_aero_unique_1", "station_no", "lsd", unique=True),
        {"comment": "METAR / SPECI Aero message observations"},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    station_no = Column(
        ForeignKey("stations.station_no"),
        nullable=False,
        comment="Local Station identifier",
    )
    lsd = Column(
        DateTime, nullable=False, comment="Local System Time (No Daylight Savings)"
    )
    gmt = Column(DateTime, comment="GMT (UTC+0)")
    lct = Column(DateTime, comment="Local Clock Time (With Daylight Savings)")
    data_source = Column(
        CHAR(2), nullable=False, comment="Code for data source (Ref Table??)"
    )
    insert_datetime = Column(
        DateTime, nullable=False, comment="Date/time row is inserted"
    )
    change_datetime = Column(DateTime, comment="Date/time row is changed")
    change_user = Column(String(20), comment="User who added/changed row")
    qa_flag = Column(
        CHAR(1),
        nullable=False,
        server_default=text("'N'::bpchar"),
        comment="QA flag for row (Y/N)",
    )
    comments = Column(String(1000), comment="User comments")
    message_type = Column(CHAR(1), comment="M=METAR, S=SPECI")
    wind_dir = Column(Numeric(4, 0), comment="Degrees (0-360)")
    wind_dir_qa = Column(CHAR(2))
    wind_speed = Column(Numeric(4, 1), comment="Wind Speed (M/s to 0.1)")
    wind_speed_qa = Column(CHAR(2))
    max_gust_10m = Column(Numeric(4, 1), comment="Max Wind Speed (M/s to 0.1)")
    max_gust_10m_qa = Column(CHAR(2))
    cavok_or_skc = Column(CHAR(1), comment="C=CAVOK, S=SKC")
    visibility = Column(Numeric(7, 3), comment="Km to (0.001)")
    visibility_qa = Column(CHAR(2))
    pres_wea_intensity_1 = Column(
        Numeric(1, 0), comment="0=Light, 1=Moderate, 2=Heavy,3=In Vicinity"
    )
    pres_wea_desc_1 = Column(CHAR(2), comment="MI,BC,PR,DR,BL,SH,TS,FZ")
    pres_wea_phen_1 = Column(
        String(6),
        comment="DZ,RA,SN,SG,IC,PL,GR,GS, BR, FG, FU, VA, DU, SA, HZ, PO, SQ, FC, SS, DS (WMO 4678)",
    )
    pres_wea_1_qa = Column(CHAR(2))
    pres_wea_intensity_2 = Column(
        Numeric(1, 0), comment="0=Light, 1=Moderate, 2=Heavy,3=In Vicinity"
    )
    pres_wea_desc_2 = Column(CHAR(2), comment="MI,BC,PR,DR,BL,SH,TS,FZ")
    pres_wea_phen_2 = Column(
        String(6),
        comment="DZ,RA,SN,SG,IC,PL,GR,GS, BR, FG, FU, VA, DU, SA, HZ, PO, SQ, FC, SS, DS (WMO 4678)",
    )
    pres_wea_2_qa = Column(CHAR(2))
    pres_wea_intensity_3 = Column(
        Numeric(1, 0), comment="0=Light, 1=Moderate, 2=Heavy,3=In Vicinity"
    )
    pres_wea_desc_3 = Column(CHAR(2), comment="MI,BC,PR,DR,BL,SH,TS,FZ")
    pres_wea_phen_3 = Column(
        String(6),
        comment="DZ,RA,SN,SG,IC,PL,GR,GS, BR, FG, FU, VA, DU, SA, HZ, PO, SQ, FC, SS, DS (WMO 4678)",
    )
    pres_wea_3_qa = Column(CHAR(2))
    cloud_amt_oktas_1 = Column(Numeric(2, 0), comment="Oktas (0-9)")
    cloud_amt_code_1 = Column(CHAR(3), comment="FEW, SCD, BKN,OVC")
    cloud_amt_1_qa = Column(CHAR(2))
    cloud_type_1 = Column(String(2), comment="ST, SC, CU, etc")
    cloud_type_1_qa = Column(CHAR(2))
    cloud_height_code_1 = Column(CHAR(3), comment="Code (WMO Code 1690)")
    cloud_height_1_qa = Column(CHAR(2))
    cloud_amt_oktas_2 = Column(Numeric(2, 0), comment="Oktas (0-9)")
    cloud_amt_code_2 = Column(CHAR(3), comment="FEW, SCD, BKN,OVC")
    cloud_amt_2_qa = Column(CHAR(2))
    cloud_type_2 = Column(String(2), comment="ST, SC, CU, etc")
    cloud_type_2_qa = Column(CHAR(2))
    cloud_height_code_2 = Column(CHAR(3), comment="Code (WMO Code 1690)")
    cloud_height_2_qa = Column(CHAR(2))
    cloud_amt_oktas_3 = Column(Numeric(2, 0), comment="Oktas (0-9)")
    cloud_amt_code_3 = Column(CHAR(3), comment="FEW, SCD, BKN,OVC")
    cloud_amt_3_qa = Column(CHAR(2))
    cloud_type_3 = Column(String(2), comment="ST, SC, CU, etc")
    cloud_type_3_qa = Column(CHAR(2))
    cloud_height_code_3 = Column(CHAR(3), comment="Code (WMO Code 1690)")
    cloud_height_3_qa = Column(CHAR(2))
    cloud_amt_oktas_4 = Column(Numeric(2, 0), comment="Oktas (0-9)")
    cloud_amt_code_4 = Column(CHAR(3), comment="FEW, SCD, BKN,OVC")
    cloud_amt_4_qa = Column(CHAR(2))
    cloud_type_4 = Column(String(2), comment="ST, SC, CU, etc")
    cloud_type_4_qa = Column(CHAR(2))
    cloud_height_code_4 = Column(CHAR(3), comment="Code (WMO Code 1690)")
    cloud_height_4_qa = Column(CHAR(2))
    cloud_amt_oktas_5 = Column(Numeric(2, 0), comment="Oktas (0-9)")
    cloud_amt_code_5 = Column(CHAR(3), comment="FEW, SCD, BKN,OVC")
    cloud_amt_5_qa = Column(CHAR(2))
    cloud_type_5 = Column(String(2), comment="ST, SC, CU, etc")
    cloud_type_5_qa = Column(CHAR(2))
    cloud_height_code_5 = Column(CHAR(3), comment="Code (WMO Code 1690)")
    cloud_height_5_qa = Column(CHAR(2))
    cloud_amt_oktas_6 = Column(Numeric(2, 0), comment="Oktas (0-9)")
    cloud_amt_code_6 = Column(CHAR(3), comment="FEW, SCD, BKN,OVC")
    cloud_amt_6_qa = Column(CHAR(2))
    cloud_type_6 = Column(String(2), comment="0-9")
    cloud_type_6_qa = Column(CHAR(2))
    cloud_height_code_6 = Column(CHAR(3), comment="Code (WMO Code 1690)")
    cloud_height_6_qa = Column(CHAR(2))
    ceiling_clear_flag = Column(Numeric(1, 0), comment="Code (0,1=\x94CLR BLW 125\x94)")
    ceiling_clear_flag_qa = Column(CHAR(2))
    air_temp = Column(Numeric(4, 1), comment="C to 0.1")
    air_temp_f = Column(Numeric(4, 1), comment="F to 0.1")
    air_temp_qa = Column(CHAR(2))
    dew_point = Column(Numeric(4, 1), comment="C to 0.1")
    dew_point_f = Column(Numeric(4, 1), comment="F to 0.1")
    dew_point_qa = Column(CHAR(2))
    qnh = Column(Numeric(7, 1), comment="hPa to 0.1")
    qnh_inches = Column(Numeric(8, 3), comment="Inches to 0.001")
    qnh_qa = Column(CHAR(2))
    rec_wea_desc_1 = Column(CHAR(2), comment="MI,BC,PR,BL,SH,TS,FZ")
    rec_wea_phen_1 = Column(
        String(6),
        comment="REFZRA, REFZDZ, RERA, RESN, REGR, REBLSN,REDS, RESS, RETS, REUP",
    )
    rec_wea_1_qa = Column(CHAR(2))
    rec_wea_desc_2 = Column(CHAR(2), comment="MI,BC,PR,BL,SH,TS,FZ")
    rec_wea_phen_2 = Column(
        String(6),
        comment="REFZRA, REFZDZ, RERA, RESN, REGR, REBLSN,REDS, RESS, RETS, REUP",
    )
    rec_wea_2_qa = Column(CHAR(2))
    rec_wea_desc_3 = Column(CHAR(2), comment="MI,BC,PR,BL,SH,TS,FZ")
    rec_wea_phen_3 = Column(
        String(6),
        comment="REFZRA, REFZDZ, RERA, RESN, REGR, REBLSN,REDS, RESS, RETS, REUP",
    )
    rec_wea_3_qa = Column(CHAR(2))
    text_msg = Column(String(1024), comment="METAR/SPECI msg")
    error_flag = Column(Numeric(1, 0), comment="Code (1=Yes, 0=No)")
    remarks = Column(
        String(400),
        comment="Additional Remarks supplied by observer. (Mainly paper docs)",
    )
    remarks_qa = Column(CHAR(2))
    wind_speed_knots = Column(Numeric(5, 1), comment="Wind Speed in Knots")
    max_gust_10m_knots = Column(Numeric(5, 1), comment="Max Gust >10M Knots")
    visibility_miles = Column(Numeric(7, 3))

    station = relationship("Station")


class ObsAw(Base):
    __tablename__ = "obs_aws"
    __table_args__ = (
        Index("obs_aws_unique_1", "station_no", "lsd", unique=True),
        Index("obs_aws_lct_idx", "lct"),
        Index("obs_aws_lsd_idx", "lsd"),
        {"comment": "AWS observations"},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    station_no = Column(
        ForeignKey("stations.station_no"),
        nullable=False,
        comment="Local Station identifier",
    )
    lsd = Column(
        DateTime,
        nullable=False,
        comment="Local System Time (No Daylight Savings)",
    )
    gmt = Column(DateTime, comment="GMT (UTC+0)")
    lct = Column(DateTime, comment="Local Clock Time (With Daylight Savings)")
    insert_datetime = Column(
        DateTime, nullable=False, comment="Date/time row is inserted"
    )
    change_datetime = Column(DateTime, comment="Date/time row is changed")
    change_user = Column(String(20), comment="User who added/changed row")
    data_source = Column(CHAR(2))
    qa_flag = Column(
        CHAR(1),
        nullable=False,
        server_default=text("'N'::bpchar"),
        comment="QA flag for row (Y/N)",
    )
    measure_period = Column(
        SmallInteger, comment='Average Period in minutes. "Standard" is (10 min)'
    )
    mn_wind_dir_pt = Column(
        CHAR(3), comment='(10 min) mean direction in points. ("ENE")'
    )
    mn_wind_dir_deg = Column(
        SmallInteger, comment="(10 min) mean direction in degrees. (0-360)"
    )
    mn_wind_dir_qa = Column(CHAR(2))
    mn_wind_dir_stddev = Column(Numeric(3, 1), comment="(10 min) mean dir Std Dev")
    mn_wind_dir_stddev_qa = Column(CHAR(2))
    mn_wind_speed = Column(
        Numeric(7, 1), comment="(10 min) mean wind speed (m/s to 0.1)"
    )
    mn_wind_speed_qa = Column(CHAR(2))
    mn_wind_speed_stddev = Column(
        Numeric(7, 1), comment="(10 min) mean speed Std Dev (m/s to 0.1)"
    )
    mn_wind_speed_stddev_qa = Column(CHAR(2))
    mn_gust_speed = Column(
        Numeric(7, 1), comment="(10 min) mean gust speed (m/s to 0.1)"
    )
    mn_gust_speed_qa = Column(CHAR(2))
    mn_gust_time = Column(String(8), comment="Time at end of sample period")
    mn_gust_time_qa = Column(CHAR(2))
    mn_gust_dir_pt = Column(
        CHAR(3), comment='Mean Direction of maximum wind speed. ("ENE")'
    )
    mn_gust_dir_deg = Column(
        SmallInteger, comment="Mean Direction of maximum wind speed. (0-360)"
    )
    mn_gust_dir_qa = Column(CHAR(2))
    inst_gust_speed = Column(
        Numeric(7, 1), comment="Instantaneous gust speed (m/s to 0.1)"
    )
    inst_gust_qa = Column(CHAR(2))
    inst_gust_time = Column(
        String(8), comment="Time of instantaneous gust speed (09:30)"
    )
    inst_gust_time_qa = Column(CHAR(2))
    inst_gust_dir_pt = Column(
        CHAR(3), comment='Direction of instantaneous gust speed. ("ENE")'
    )
    inst_gust_dir_deg = Column(
        SmallInteger, comment="Direction of instantaneous gust speed. (0-360)"
    )
    inst_gust_dir_qa = Column(CHAR(2))
    mn_temp = Column(Numeric(7, 1), comment="(10 min) mean. (C to 0.1)")
    mn_temp_qa = Column(CHAR(2))
    mn_temp_subaveraging = Column(Numeric(7, 1), comment="Sub-averaged temp (C to 0.1)")
    mn_temp_subaveraging_period = Column(
        SmallInteger, comment="Sub-averaging period (minutes)"
    )
    mn_temp_subaveraging_qa = Column(CHAR(2))
    max_temp = Column(Numeric(7, 1), comment="(10 min) maximum. (C to 0.1)")
    max_temp_time = Column(String(8), comment="Time of max temperature. (hh:mm:ss)")
    max_temp_time_qa = Column(CHAR(2))
    max_temp_qa = Column(CHAR(2))
    min_temp = Column(Numeric(7, 1), comment="(10 min) minimum. (C to 0.1)")
    min_temp_qa = Column(CHAR(2))
    min_temp_time = Column(String(8), comment="Time of min temperature.  (hh:mm:ss)")
    min_temp_time_qa = Column(CHAR(2))
    min_grass_temp = Column(
        Numeric(7, 1), comment="(10 min) minimum grass temp. (C to 0.1)"
    )
    min_grass_temp_qa = Column(CHAR(2))
    min_grass_temp_time = Column(
        String(8), comment="Time of min grass temp.  (hh:mm:ss)"
    )
    min_grass_temp_time_qa = Column(CHAR(2))
    mn_humidity = Column(Numeric(4, 1), comment="(10 min)average humidity (% to 0.1)")
    mn_humidity_qa = Column(CHAR(2))
    max_humidity = Column(Numeric(4, 1), comment="(10 min) maximum humidity (% to 0.1)")
    max_humidity_qa = Column(CHAR(2))
    max_humidity_time = Column(
        String(8), comment="Time of maximum humidity.  (hh:mm:ss)"
    )
    max_humidity_time_qa = Column(CHAR(2))
    min_humidity = Column(Numeric(4, 1), comment="(10 min) minimum humidity (% to 0.1)")
    min_humidity_qa = Column(CHAR(2))
    min_humidity_time = Column(
        String(8), comment="Time of minimum humidity.  (hh:mm:ss)"
    )
    min_humidity_time_qa = Column(CHAR(2))
    mn_station_pres = Column(
        Numeric(5, 1), comment="Average station pressure (hPa to 0.1)"
    )
    mn_station_pres_qa = Column(CHAR(2))
    mn_sea_level_pres = Column(
        Numeric(5, 1), comment="Average sea level pressure (hPa to 0.1)"
    )
    mn_sea_level_pres_qa = Column(CHAR(2))
    max_pres = Column(Numeric(5, 1), comment="Maximum pressure (hPa to 0.1)")
    max_pres_qa = Column(CHAR(2))
    max_pres_time = Column(String(8), comment="Time of maximum pressure.  (hh:mm:ss)")
    max_pres_time_qa = Column(CHAR(2))
    min_pres = Column(Numeric(5, 1), comment="Minimum pressure (hPa to 0.1)")
    min_pres_qa = Column(CHAR(2))
    min_pres_time = Column(String(8), comment="Time of minimum pressure.  (hh:mm:ss)")
    min_pres_time_qa = Column(CHAR(2))
    tot_rain = Column(Numeric(6, 1), comment="(10 min) total rainfall (mm to 0.1)")
    tot_rain_qa = Column(CHAR(2))
    tot_rain_two = Column(
        Numeric(6, 1), comment="(10 min) total rainfall instrument #2 (mm to 0.1)"
    )
    tot_rain_two_qa = Column(CHAR(2))
    tot_sun = Column(Integer, comment="(10 min) total sunshine (secs, max 600)")
    tot_sun_qa = Column(CHAR(2))
    tot_insolation = Column(
        Numeric(7, 2), comment="(10 min) insolation (Mj/m2 to 0.01)"
    )
    tot_insolation_qa = Column(CHAR(2))
    leaf_wetness = Column(SmallInteger, comment="1/0 indicating leaf wetness.")
    leaf_wetness_qa = Column(CHAR(2))
    mn_uv = Column(Numeric(4, 0), comment="(10 min) mean UV (mV)")
    mn_uv_qa = Column(CHAR(2))
    mn_soil_moisture_10 = Column(
        Numeric(3, 1), comment="(10 min) mean soil moisture at 10cm (% to 0.1)"
    )
    mn_soil_moisture_10_qa = Column(CHAR(2))
    mn_soil_temp_10 = Column(
        Numeric(5, 1), comment="(10 min) mean soil temperature at 10cm (C to 0.1)"
    )
    mn_soil_temp_10_qa = Column(CHAR(2))
    mn_soil_moisture_20 = Column(
        Numeric(3, 1), comment="(10 min) mean soil moisture at 20cm (% to 0.1)"
    )
    mn_soil_moisture_20_qa = Column(CHAR(2))
    mn_soil_temp_20 = Column(
        Numeric(5, 1), comment="(10 min) mean soil temperature at 20cm (C to 0.1)"
    )
    mn_soil_temp_20_qa = Column(CHAR(2))
    mn_soil_moisture_30 = Column(
        Numeric(3, 1), comment="(10 min) mean soil moisture at 30cm (% to 0.1)"
    )
    mn_soil_moisture_30_qa = Column(CHAR(2))
    mn_soil_temp_30 = Column(
        Numeric(5, 1), comment="(10 min) mean soil temperature at 30cm (C to 0.1)"
    )
    mn_soil_temp_30_qa = Column(CHAR(2))
    mn_soil_moisture_50 = Column(
        Numeric(3, 1), comment="(10 min) mean soil moisture at 50cm (% to 0.1)"
    )
    mn_soil_moisture_50_qa = Column(CHAR(2))
    mn_soil_temp_50 = Column(
        Numeric(5, 1), comment="(10 min) mean soil temperature at 50cm (C to 0.1)"
    )
    mn_soil_temp_50_qa = Column(CHAR(2))
    mn_soil_moisture_100 = Column(
        Numeric(3, 1), comment="(10 min) mean soil moisture at 100cm (% to 0.1)"
    )
    mn_soil_moisture_100_qa = Column(CHAR(2))
    mn_soil_temp_100 = Column(
        Numeric(5, 1), comment="(10 min) mean soil temperature at 100cm (C to 0.1)"
    )
    mn_soil_temp_100_qa = Column(CHAR(2))

    station = relationship("Station")


class ObsDaily(Base):
    __tablename__ = "obs_daily"
    __table_args__ = (
        Index("obs_daily_unique_1", "station_no", "lsd", unique=True),
        Index("obs_daily_lsd_idx", "lsd"),
        {"comment": "Daily surface observations"},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    station_no = Column(
        ForeignKey("stations.station_no"),
        nullable=False,
        comment="Local Station identifier",
    )
    lsd = Column(
        DateTime,
        nullable=False,
        comment="Local System Time (No Daylight Savings)",
    )
    data_source = Column(
        CHAR(2), nullable=False, comment="Code for data source (DATA_SRC)"
    )
    insert_datetime = Column(
        DateTime,
        nullable=False,
        server_default=text("now()"),
        comment="Date/time row is inserted",
    )
    change_datetime = Column(DateTime, comment="Date/time row is changed")
    change_user = Column(String(20), comment="User who added/changed row")
    qa_flag = Column(
        CHAR(1),
        nullable=False,
        server_default=text("'N'::bpchar"),
        comment="QA flag for row (Y/N)",
    )
    aws_flag = Column(
        CHAR(1),
        nullable=False,
        server_default=text("'N'::bpchar"),
        comment="AWS sourced data or not (Y/N)",
    )
    comments = Column(String(1000), comment="User comments")
    rain_24h = Column(Numeric(6, 1), comment="LCT 0900 to 0900 (mm to 0.1)")
    rain_24h_inches = Column(
        Numeric(7, 3), comment="LCT 0900 to 0900 (inches to 0.001)"
    )
    rain_24h_period = Column(Numeric(2, 0), comment="Period of data: Normally 1 day")
    rain_24h_type = Column(
        String(10), comment="rain,frost,fog,dew,trace,snow,other, n/a"
    )
    rain_24h_count = Column(
        Numeric(2, 0), comment="No of days rain has fallen. Default 1."
    )
    rain_24h_qa = Column(CHAR(2), comment="Quality code for rain_24h")
    max_air_temp = Column(
        Numeric(7, 1), comment="Maximum air temperature (0.1C). Standard 0900"
    )
    max_air_temp_f = Column(
        Numeric(7, 1), comment="Maximum air temperature (0.1F). Standard 0900"
    )
    max_air_temp_period = Column(
        Numeric(2, 0), comment="Period for max air temp (hours). Standard 0900"
    )
    max_air_temp_time = Column(
        String(5), comment="Time that max air temp was reached. Standard 0900"
    )
    max_air_temp_qa = Column(CHAR(2), comment="Quality code for max_air_temp")
    min_air_temp = Column(
        Numeric(5, 1), comment="Minimum air temperature (0.1C). Standard 0900"
    )
    min_air_temp_f = Column(
        Numeric(5, 1), comment="Minimum air temperature (0.1F). Standard 0900"
    )
    min_air_temp_period = Column(
        Numeric(2, 0), comment="Period for min air temp (hours). Standard 0900"
    )
    min_air_temp_time = Column(
        String(5), comment="Time that min air temp was reached. Standard 0900"
    )
    min_air_temp_qa = Column(CHAR(2), comment="Quality code for min_air_temp")
    reg_max_air_temp = Column(
        Numeric(7, 1), comment="Maximum air temperature (0.1C). Regional."
    )
    reg_max_air_temp_qa = Column(CHAR(2), comment="Quality code for max_air_temp_reg")
    reg_min_air_temp = Column(
        Numeric(7, 1), comment="Minimum air temperature (0.1C). Regional."
    )
    reg_min_air_temp_qa = Column(CHAR(2), comment="Quality code for min_air_temp")
    ground_temp = Column(Numeric(5, 1), comment="Ground surface temp (0.1C)")
    ground_temp_f = Column(Numeric(5, 1), comment="Ground surface temp (0.1F)")
    ground_temp_qa = Column(CHAR(2), comment="Quality code for ground_temp")
    max_gust_dir = Column(Numeric(3, 0), comment="Degrees (0-360)")
    max_gust_dir_qa = Column(CHAR(2), comment="Quality code for max_gust_dir")
    max_gust_speed = Column(Numeric(4, 1), comment="Speed of max wind gust M/s (0.1)")
    max_gust_speed_kts = Column(Numeric(3, 0))
    max_gust_speed_bft = Column(String(2), comment="Speed of max wind gust Beaufort")
    max_gust_speed_qa = Column(CHAR(2), comment="Quality code for max_gust_speed")
    max_gust_time = Column(String(5), comment="Time of max wind gust")
    max_gust_time_qa = Column(CHAR(2), comment="Quality code for max_gust_time")
    wind_run_lt10 = Column(
        Numeric(6, 2), comment="Wind run taken from <10M (evaporation) Km"
    )
    wind_run_lt10_miles = Column(
        Numeric(6, 2), comment="Wind run taken from <10M (evaporation) Miles"
    )
    wind_run_lt10_period = Column(
        Numeric(3, 0), comment="Period in hours for Wind run <10"
    )
    wind_run_lt10_qa = Column(CHAR(2), comment="Quality code for wind_run_lt10")
    wind_run_gt10 = Column(
        Numeric(6, 2), comment="Wind run taken from >10M anemometer Km"
    )
    wind_run_gt10_miles = Column(
        Numeric(6, 2), comment="Wind run taken from >10M anemometer Miles"
    )
    wind_run_gt10_period = Column(
        Numeric(3, 0), comment="Period in hours for Wind run >10"
    )
    wind_run_gt10_qa = Column(CHAR(2), comment="Quality code for wind_run_gt10")
    evaporation = Column(Numeric(4, 1), comment="Evaporation in mm (0.1)")
    evaporation_inches = Column(Numeric(5, 3), comment="Evaporation in inches (0.001)")
    evaporation_period = Column(
        Numeric(3, 0), comment="Period in hours for evaporation"
    )
    evaporation_qa = Column(CHAR(2), comment="Quality code for evaporation")
    evap_water_max_temp = Column(Numeric(5, 1), comment="Max water temp (0.1C)")
    evap_water_max_temp_f = Column(Numeric(5, 1), comment="Max water temp (0.1F)")
    evap_water_max_temp_qa = Column(CHAR(2), comment="Quality code for evap_max_temp")
    evap_water_min_temp = Column(Numeric(5, 1), comment="Min water temp (0.1C)")
    evap_water_min_temp_f = Column(Numeric(5, 1), comment="Min water temp (0.1F)")
    evap_water_min_temp_qa = Column(CHAR(2), comment="Quality code for evap_min_temp")
    sunshine_duration = Column(Numeric(3, 1), comment="Decimal Hours to (0.1)")
    sunshine_duration_qa = Column(CHAR(2), comment="Quality code for sunshine_duration")
    river_height = Column(Numeric(5, 1), comment="Daily river height reading (0.1M)")
    river_height_in = Column(Numeric(8, 1))
    river_height_qa = Column(CHAR(2), comment="Quality code for river_height")
    radiation = Column(Numeric(6, 1), comment="Daily radiation Mj/M to 0.1")
    radiation_qa = Column(CHAR(2), comment="Quality code for radiation")
    thunder_flag = Column(CHAR(1), comment="Y/N for thunder")
    thunder_flag_qa = Column(CHAR(2), comment="Quality code for thunder_flag")
    frost_flag = Column(CHAR(1), comment="Y/N for frost")
    frost_flag_qa = Column(CHAR(2), comment="Quality code for frost_flag")
    dust_flag = Column(CHAR(1), comment="Y/N for dust")
    dust_flag_qa = Column(CHAR(2), comment="Quality code for dust_flag")
    haze_flag = Column(CHAR(1), comment="Y/N for haze")
    haze_flag_qa = Column(CHAR(2), comment="Quality code for haze_flag")
    fog_flag = Column(CHAR(1), comment="Y/N for fog")
    fog_flag_qa = Column(CHAR(2), comment="Quality code for fog_flag")
    strong_wind_flag = Column(CHAR(1), comment="Y/N for strong wind")
    strong_wind_flag_qa = Column(CHAR(2), comment="Quality code for strong_wind_flag")
    gale_flag = Column(CHAR(1), comment="Y/N for gale")
    gale_flag_qa = Column(CHAR(2), comment="Quality code for gale_flag")
    hail_flag = Column(CHAR(1), comment="Y/N for hail")
    hail_flag_qa = Column(CHAR(2), comment="Quality code for hail_flag")
    snow_flag = Column(CHAR(1), comment="Y/N for snow")
    snow_flag_qa = Column(CHAR(2), comment="Quality code for snow_flag")
    lightning_flag = Column(CHAR(1), comment="Y/N for lightning")
    lightning_flag_qa = Column(CHAR(2), comment="Quality code for lightning_flag")
    shower_flag = Column(CHAR(1), comment="Y/N for shower")
    shower_flag_qa = Column(CHAR(2), comment="Quality code for shower_flag")
    rain_flag = Column(CHAR(1), comment="Y/N for rain")
    rain_flag_qa = Column(CHAR(2), comment="Quality code for rain_flag")
    dew_flag = Column(CHAR(1))
    dew_flag_qa = Column(CHAR(2))

    station = relationship("Station")


class ObsSubdaily(Base):
    __tablename__ = "obs_subdaily"
    __table_args__ = (
        Index("obs_subdaily_unique_1", "station_no", "lsd", unique=True),
        Index("obs_subdaily_lct_idx", "lct"),
        Index("obs_subdaily_lsd_idx", "lsd"),
        {"comment": "Sub Daily surface observations"},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    station_no = Column(
        ForeignKey("stations.station_no"),
        nullable=False,
        comment="Local Station identifier",
    )
    lsd = Column(
        DateTime,
        nullable=False,
        comment="Local System Time (No Daylight Savings)",
    )
    gmt = Column(DateTime, comment="GMT (UTC+0)")
    lct = Column(DateTime, comment="Local Clock Time (With Daylight Savings)")
    data_source = Column(
        CHAR(2), nullable=False, comment="Code for data source (DATA_SRC)"
    )
    insert_datetime = Column(
        DateTime, nullable=False, comment="Date/time row is inserted"
    )
    change_datetime = Column(DateTime, comment="Date/time row is changed")
    change_user = Column(String(20), comment="User who added/changed row")
    qa_flag = Column(
        CHAR(1),
        nullable=False,
        server_default=text("'N'::bpchar"),
        comment="QA flag for row (Y/N)",
    )
    aws_flag = Column(
        CHAR(1),
        nullable=False,
        server_default=text("'N'::bpchar"),
        comment="AWS sourced data or not (Y/N)",
    )
    comments = Column(String(1000), comment="User comments")
    air_temp = Column(Numeric(7, 1), comment="Current Air temperature (0.1C)")
    air_temp_f = Column(Numeric(7, 1), comment="Current Air Temp in Fahrenheit (0.1F)")
    air_temp_qa = Column(CHAR(2), comment="Quality Code for air_temp")
    sea_water_temp = Column(
        Numeric(7, 1), comment="Current Sea water Temperature (0.1C)"
    )
    sea_water_temp_f = Column(
        Numeric(7, 1), comment="Current Sea water Temp in Fahrenheit (0.1F)"
    )
    sea_water_temp_qa = Column(CHAR(2), comment="Quality Code for sea_water_temp")
    wet_bulb = Column(Numeric(7, 1), comment="Current Wet bulb reading (0.1C)")
    wet_bulb_f = Column(
        Numeric(7, 1), comment="Current Wet bulb reading in Fahrenheit (0.1F)"
    )
    wet_bulb_qa = Column(CHAR(2), comment="Quality Code for wet_bulb")
    dew_point = Column(Numeric(7, 1), comment="Current Dew Point Temperature (0.1C)")
    dew_point_f = Column(Numeric(7, 1), comment="Current Dew Point Fahrenheit (0.1F)")
    dew_point_qa = Column(CHAR(2), comment="Quality Code for dew_point")
    rel_humidity = Column(Numeric(4, 1), comment="Relative humidity  (% to 0.1)")
    rel_humidity_qa = Column(CHAR(2), comment="Quality Code for rel_humidity")
    baro_temp = Column(Numeric(7, 1), comment="Current Barometer Temperature (0.1C)")
    baro_temp_f = Column(Numeric(7, 1), comment="Current Barometer Fahrenheit (0.1F)")
    baro_temp_qa = Column(CHAR(2), comment="Quality Code for baro_temp")
    pres_as_read = Column(
        Numeric(7, 1), comment="Pressure as read from barometer (hPa to 0.1)"
    )
    pres_as_read_inches = Column(
        Numeric(8, 3), comment="Pressure as read from barometer (Inches to 0.001)"
    )
    pres_as_read_qa = Column(CHAR(2), comment="Quality Code for pres_as_read")
    station_pres = Column(Numeric(7, 1), comment="Station Pressure (hPa to 0.1)")
    station_pres_inches = Column(
        Numeric(8, 3), comment="Station Pressure (Inches to 0.001)"
    )
    station_pres_qa = Column(CHAR(2), comment="Quality Code for station_pres")
    msl_pres = Column(Numeric(7, 1), comment="Mean Sea Level Pressure (hPa to 0.1)")
    msl_pres_inches = Column(
        Numeric(8, 3), comment="Mean Sea Level Pressure (Inches to 0.001)"
    )
    msl_pres_qa = Column(CHAR(2), comment="Quality Code for msl_pres")
    vapour_pres = Column(Numeric(7, 1), comment="Vapour Pressure (hPa to 0.1)")
    vapour_pres_inches = Column(
        Numeric(8, 3), comment="Vapour Pressure (Inches to 0.001)"
    )
    vapour_pres_qa = Column(CHAR(2), comment="Quality Code for vapour_pres")
    qnh = Column(Numeric(7, 1), comment="Local QNH (hPa to 0.1)")
    qnh_qa = Column(CHAR(2), comment="Quality Code for qnh")
    visibility = Column(Numeric(7, 3), comment="Visibility in Km (Km to 0.001)")
    visibility_miles = Column(
        Numeric(7, 3), comment="Visibility in Miles (Miles to 0.001)"
    )
    visibility_code = Column(CHAR(1))
    visibility_qa = Column(CHAR(2), comment="Quality Code for visibility")
    rain_3h = Column(Numeric(7, 1), comment="3 hours cumulative (mm to 0.1)")
    rain_3h_inches = Column(
        Numeric(7, 3), comment="3 hours cumulative (Inches to 0.001)"
    )
    rain_3h_qa = Column(CHAR(2), comment="Quality Code for rain_3h")
    rain_3h_hours = Column(Numeric(3, 0), server_default=text("3"))
    rain_cum = Column(Numeric(7, 1), comment="Cumulative since 0900 (mm to 0.1)")
    rain_cum_inches = Column(
        Numeric(7, 3), comment="Cumulative since 0900 (Inches to 0.001)"
    )
    rain_cum_qa = Column(CHAR(2), comment="Quality Code for rain_cum")
    wind_dir = Column(
        Numeric(3, 0), comment="10 min Avg Wind direction (degrees 0-360)"
    )
    wind_dir_qa = Column(CHAR(2), comment="Quality Code for wind_dir")
    wind_dir_std_dev = Column(
        Numeric(3, 0), comment="10 min Avg Wind direction standard deviation"
    )
    wind_dir_std_dev_qa = Column(CHAR(2), comment="Quality Code for wind_dir_std_dev")
    wind_speed = Column(Numeric(5, 1), comment="10 min Avg Wind Speed (M/S to 0.1)")
    wind_speed_knots = Column(
        Numeric(5, 1), comment="10 min Avg Wind Speed (Knots to 0.1)"
    )
    wind_speed_mph = Column(Numeric(5, 1), comment="10 min Avg Wind Speed (MPH to 0.1)")
    wind_speed_bft = Column(CHAR(2), comment="10 min Avg Beaufort code for wind speed")
    wind_speed_qa = Column(CHAR(2), comment="Quality Code for wind_speed")
    pres_weather_code = Column(String(2), comment="WMO Code 4677 for present weather.")
    pres_weather_bft = Column(String(20), comment="Beaufort Code for present weather")
    pres_weather_qa = Column(CHAR(2), comment="Quality Code for pres_weather")
    past_weather_code = Column(String(2), comment="WMO Code 4561")
    past_weather_bft = Column(String(20), comment="Beaufort Code for past weather")
    past_weather_qa = Column(CHAR(2), comment="Quality Code for past_weather")
    tot_cloud_oktas = Column(
        SmallInteger, comment="Total amount of sky covered by cloud (0-9)"
    )
    tot_cloud_tenths = Column(
        SmallInteger, comment="Total amount of sky covered by cloud (0-10)"
    )
    tot_cloud_qa = Column(CHAR(2), comment="Quality Code for tot_cloud")
    tot_low_cloud_oktas = Column(
        SmallInteger, comment="Total amount of sky covered by Low cloud (0-9)"
    )
    tot_low_cloud_tenths = Column(
        SmallInteger, comment="Total amount of sky covered by Low cloud (0-10)"
    )
    tot_low_cloud_height = Column(Integer)
    tot_low_cloud_qa = Column(CHAR(2), comment="Quality Code for tot_low_cloud")
    state_of_sea = Column(String(2), comment="State of Sea (Douglas Scale WMO 3700)")
    state_of_sea_qa = Column(CHAR(2), comment="Quality Code for state_of_sea")
    state_of_swell = Column(
        String(2), comment="State open sea swell (Douglas Scale WMO 3700)"
    )
    state_of_swell_qa = Column(CHAR(2), comment="Quality Code for state_of_swell")
    swell_direction = Column(
        String(3), comment="Direction of Swell (16 Compass Points)"
    )
    swell_direction_qa = Column(CHAR(2), comment="Quality Code for swell_direction")
    sea_level = Column(
        Numeric(5, 3), comment="Sea level (M to 0.001) above tide gauge zero"
    )
    sea_level_qa = Column(CHAR(2), comment="Quality Code for sea_level")
    sea_level_residual = Column(
        Numeric(5, 3), comment="+/- Diff from predicted sea level"
    )
    sea_level_residual_qa = Column(
        CHAR(2), comment="Quality Code for sea_level_residual"
    )
    sea_level_resid_adj = Column(
        Numeric(5, 3), comment="Adjusted residual (adjusted for pressure)"
    )
    sea_level_resid_adj_qa = Column(
        CHAR(2), comment="Quality Code for sea_level_residual_adj"
    )
    radiation = Column(Numeric(6, 1), comment="Radiation Mj/M to 0.1")
    radiation_qa = Column(CHAR(2))
    sunshine = Column(Numeric(3, 1), comment="Decimal Hours to 0.1")
    sunshine_qa = Column(CHAR(2))
    tot_low_cloud_height_feet = Column(Integer)
    wind_gust_kts = Column(Numeric(3, 0), comment="Wind Gust speed Knots")
    wind_gust = Column(Numeric(6, 1), comment="Wind Gust speed M/S")
    wind_gust_qa = Column(CHAR(2))
    wind_gust_dir = Column(Numeric(3, 0), comment="Wind Gust direction 0-360")
    wind_gust_dir_qa = Column(CHAR(2))
    river_height = Column(Numeric(7, 3), comment="River height in M")
    river_height_in = Column(Numeric(8, 1))
    river_height_qa = Column(CHAR(2))
    qnh_inches = Column(Numeric(8, 3))

    station = relationship("Station")


class ObsUpperAir(Base):
    __tablename__ = "obs_upper_air"
    __table_args__ = (
        Index("obs_upper_unique_1", "station_no", "lsd", "geo_height", unique=True),
        {"comment": "Upper Air observations"},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    station_no = Column(
        ForeignKey("stations.station_no"),
        nullable=False,
        comment="Local Station identifier",
    )
    lsd = Column(
        DateTime, nullable=False, comment="Local System Time (No Daylight Savings)"
    )
    gmt = Column(DateTime, comment="GMT (UTC+0)")
    lct = Column(DateTime, comment="Local Clock Time (With Daylight Savings)")
    data_source = Column(
        CHAR(2), nullable=False, comment="Code for data source (Ref Table??)"
    )
    insert_datetime = Column(
        DateTime, nullable=False, comment="Date/time row is inserted"
    )
    change_datetime = Column(DateTime, comment="Date/time row is changed")
    change_user = Column(String(20), comment="User who added/changed row")
    qa_flag = Column(
        CHAR(1),
        nullable=False,
        server_default=text("'N'::bpchar"),
        comment="QA flag for row (Y/N)",
    )
    pressure = Column(Numeric(7, 1), nullable=False, comment="Pressure (hPa to 0.1)")
    pressure_qa = Column(CHAR(2))
    level_type = Column(Numeric(2, 0), comment="Level type (0,1,n)")
    geo_height = Column(Numeric(8, 1), comment="Meters")
    geo_height_qa = Column(CHAR(2))
    air_temp = Column(Numeric(7, 1), comment="Temperature (C to 0.1)")
    air_temp_qa = Column(CHAR(2))
    dew_point = Column(Numeric(4, 1), comment="Dew Point Temperature (C to 0.1)")
    dew_point_qa = Column(CHAR(2))
    wind_direction = Column(Numeric(4, 0), comment="Direction (0-360 degrees)")
    wind_direction_qa = Column(CHAR(2))
    wind_speed = Column(Numeric(5, 1), comment="Wind Speed (M/s to 0.1)")
    wind_speed_qa = Column(CHAR(2))

    station = relationship("Station")


class StationAudit(Base):
    __tablename__ = "station_audit"
    __table_args__ = (
        Index("fki_station_audit_audit_type_id_fkey", "audit_type_id"),
        Index("fki_station_audit_station_id_fkey", "station_id"),
        {"comment": "Audit trail of all changes to station Station."},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    station_id = Column(ForeignKey("stations.id"), comment="Station ID of audit record")
    datetime = Column(DateTime(True), comment="Date/Time of event being recorded")
    event_datetime = Column(DateTime(True), server_default=text("now()"))
    audit_type_id = Column(
        ForeignKey("station_audit_types.id"),
        nullable=False,
        comment="Audit Type ID. Joins to station_audit_type",
    )
    description = Column(String(1000), comment="Description of audit event")
    event_user = Column(String(40), comment="User performing the auditable event")

    audit_type = relationship("StationAuditType")
    station = relationship("Station")


class StationClas(Base):
    __tablename__ = "station_class"
    __table_args__ = (
        Index("fki_station_class_station_id_fkey", "station_id"),
        Index("fki_station_class_type_id_fkey", "type_id"),
        {"comment": "Stores contacts (people) for station"},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    station_id = Column(
        ForeignKey("stations.id"),
        nullable=False,
        comment="Station ID of station class",
    )
    type_id = Column(
        ForeignKey("station_types.id"), comment="ID of Type for this class"
    )
    description = Column(String(80))
    class_start = Column(DateTime, comment="Date this class started for the station.")
    class_end = Column(DateTime, comment="Date this class ended for the station.")

    station = relationship("Station")
    type = relationship("StationType")


class StationContact(Base):
    __tablename__ = "station_contacts"
    __table_args__ = (
        Index("fki_station_contacts_station_id_fkey", "station_id"),
        {"comment": "Stores contacts (people) for station"},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    station_id = Column(
        ForeignKey("stations.id"),
        nullable=False,
        comment="Station ID of station contact",
    )
    title = Column(String(50))
    name = Column(String(50))
    addr1 = Column(String(50))
    addr2 = Column(String(50))
    addr3 = Column(String(50))
    addr4 = Column(String(50))
    town = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    postcode = Column(String(10))
    home_phone = Column(String(20))
    work_phone = Column(String(20))
    mob_phone = Column(String(20))
    email = Column(String(100))
    fax = Column(String(20))
    comments = Column(String(4000))
    start_date = Column(Date)
    end_date = Column(Date)

    station = relationship("Station")


class StationEquipment(Base):
    __tablename__ = "station_equipment"
    __table_args__ = (
        Index("fki_station_equipment_equipment_id_fkey", "equipment_id"),
        Index("fki_station_equipment_station_id_fkey", "station_id"),
        {"comment": "Stores equipment installed at station."},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    station_id = Column(
        ForeignKey("stations.id"), nullable=False, comment="ID of station"
    )
    equipment_id = Column(ForeignKey("equipment.id"))
    serial_no = Column(String(50), comment="Serial no of equipment")
    asset_id = Column(String(50), comment="Asset code of equipment")
    height = Column(Numeric(7, 3))
    comments = Column(String(1000), comment="Comments for equipment")
    date_start = Column(Date, comment="Date of installation")
    date_end = Column(Date, comment="Date of decomissioning or removal")

    equipment = relationship("Equipment")
    station = relationship("Station")


class StationFile(Base):
    __tablename__ = "station_files"
    __table_args__ = (
        Index("fki_station_files_station_id_fkey", "station_id"),
        {
            "comment": "Stores address of files such as images, pdfs, Word docs, etc. for station."
        },
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Surrogate Key",
    )
    station_id = Column(
        ForeignKey("stations.id"),
        nullable=False,
        comment="ID of station this row belongs to",
    )
    title = Column(String(50), comment="Title of file")
    description = Column(String(1000), comment="Description of file")
    file_path = Column(String(200), comment="Full path to file.")

    station = relationship("Station")


class ObsSubdailyCloudLayer(Base):
    __tablename__ = "obs_subdaily_cloud_layers"
    __table_args__ = (
        Index("fki_obs_subdaily_cloud_layers_subdaily_id_fkey", "sub_daily_id"),
        {"comment": "Sub Daily surface observations"},
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    sub_daily_id = Column(
        ForeignKey("obs_subdaily.id"),
        nullable=False,
        comment="Surrogate key of parent sub daily row",
    )
    data_source = Column(CHAR(2), nullable=False, server_default=text("'1'::bpchar"))
    insert_datetime = Column(DateTime, nullable=False, server_default=text("now()"))
    change_datetime = Column(DateTime)
    change_user = Column(String(20))
    qa_flag = Column(CHAR(1), nullable=False, server_default=text("'N'::bpchar"))
    aws_flag = Column(CHAR(1), nullable=False, server_default=text("'N'::bpchar"))
    layer_no = Column(Integer, nullable=False, comment="layer number. (1,2,3,n)")
    layer_type = Column(String(6), comment="Low, Mid, High")
    cloud_oktas = Column(SmallInteger, comment="Cloud  amount in octas (0-9)")
    cloud_tenths = Column(SmallInteger, comment="Cloud  amount in tenths (0-10)")
    cloud_amt_qa = Column(CHAR(2), comment="Quality Code for clout_amt")
    cloud_type = Column(String(2), comment="Cloud type, WMO code")
    cloud_type_qa = Column(CHAR(2), comment="Quality Code for cloud_type")
    cloud_height = Column(Numeric(6, 0), comment="Cloud height in Meters (M to 1.0)")
    cloud_height_feet = Column(
        Numeric(7, 0), comment="Cloud height in feet (feet to 1.0)"
    )
    cloud_height_qa = Column(CHAR(2), comment="Quality Code for cloud_height")
    cloud_dir = Column(Numeric(3, 0), comment="Cloud movement Direction (0-360)")
    cloud_dir_qa = Column(CHAR(2), comment="Quality Code for cloud_dir")

    sub_daily = relationship("ObsSubdaily")
