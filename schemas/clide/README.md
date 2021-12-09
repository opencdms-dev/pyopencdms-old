CliDE has a somewhat hybrid design. `obs_subdaily` follows the Element Model but for cloud cover and soil temperatures there are 'subtables' ([#10](https://github.com/opencdms/reference-implementation/issues/10#issuecomment-667896059)).

## Tables

| Table name | Description |
|------------|-------------|
|codes_simple|List of codes used in CliDE|
|datums|Geodetic datums|
|equipment|Stores equipment master information.|
|station_types|Stores allowed values for stations.type_id|
|obs_aero|METAR / SPECI Aero message observations|
|obs_aws|AWS observations|
|obs_daily|Daily surface observations|
|obs_subdaily|Sub Daily surface observations|
|obs_monthly|Stores monthly data not available as daily or subdaily|
|obs_subdaily_cloud_layers|Sub Daily surface observations|
|obs_subdaily_soil_temps|Sub Daily surface observations|
|obs_upper_air|Upper Air observations|
|station_audit|Audit trail of all changes to station Station.|
|station_audit_types|Stores allowed values for station_audit.type_id|
|stations|Stores station data.|
|station_class|Stores contacts (people) for station|
|station_equipment|Stores equipment installed at station.|
|land_use|Stores allowed values for stations.soil_type_id|
|soil_types|Stores allowed values for stations.soil_type_id|
|station_countries|Stores countries that stations can belong to.|
|station_status|Stores allowed values for stations.status_id|
|station_timezones|Stores time zone that stations can be in.|
|surface_types|Stores allowed values for stations.surface_type_id|
|gui_users|User data for web GUI|
|ingest_monitor|Stores file ingestion stats for data ingests|
|key_settings|Stores key entry settings: Default units, disable flag|
|obs_audit|Audit trail of all changes to station Station.|
|obs_averages|Normals and other monthly long term averages of observations.|
|obs_clicom_element_map|Mapping Clicom Codes to CLDB table, column|
|obscodes_cloud_amt_conv|Cloud Amount conversions|
|obscodes_cloud_conv_1677|Cloud Height conversions for WMO 1677|
|obscodes_cloud_ht_conv|Cloud Height conversions|
|obscodes_cloud_type_conv|Cloud Type conversions|
|obscodes_visibility|Visibility conversions: Aero, non-Aero, Km, yards. WMO 4300|
|obscodes_wind_dir|Wind Direction conversions: Compass points to degrees|
|obscodes_wind_speed|Wind speed conversions: Beaufort, m/s, knots|
|obscodes_wx|WMO Code 4677 (WX codes)|
|obsconv_factors|WMO Code 4677 (WX codes)|
|pivot|Utility table of sequential integers|
|spatial_ref_sys|Spatial reference system definitions from PostGIS|
|station_contacts|Stores contacts (people) for station|
|station_files|Stores address of files such as images, pdfs, Word docs, etc. for station.|
|timezone_diffs|Stores timezone differences due to daylight savings|
|user_sessions|Stores User session information|
