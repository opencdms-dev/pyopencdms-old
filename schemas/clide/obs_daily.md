## obs_daily
**Daily surface observations**

| Column name | Description |
|-------------|-------------|
|id|\<auto increment\>|
|station_no|Local Station identifier|
|lsd|Local System Time (No Daylight Savings)|
|data_source|Code for data source (DATA_SRC)|
|insert_datetime|Date/time row is inserted|
|change_datetime|Date/time row is changed|
|change_user|User who added/changed row|
|qa_flag|QA flag for row (Y/N)|
|aws_flag|AWS sourced data or not (Y/N)|
|comments|User comments|
|rain_24h|LCT 0900 to 0900 (mm to 0.1)|
|rain_24h_inches|LCT 0900 to 0900 (inches to 0.001)|
|rain_24h_period|Period of data: Normally 1 day|
|rain_24h_type|rain,frost,fog,dew,trace,snow,other, n/a|
|rain_24h_count|No of days rain has fallen. Default 1.|
|rain_24h_qa|Quality code for rain_24h|
|max_air_temp|Maximum air temperature (0.1C). Standard 0900|
|max_air_temp_f|Maximum air temperature (0.1F). Standard 0900|
|max_air_temp_period|Period for max air temp (hours). Standard 0900|
|max_air_temp_time|Time that max air temp was reached. Standard 0900|
|max_air_temp_qa|Quality code for max_air_temp|
|min_air_temp|Minimum air temperature (0.1C). Standard 0900|
|min_air_temp_f|Minimum air temperature (0.1F). Standard 0900|
|min_air_temp_period|Period for min air temp (hours). Standard 0900|
|min_air_temp_time|Time that min air temp was reached. Standard 0900|
|min_air_temp_qa|Quality code for min_air_temp|
|reg_max_air_temp|Maximum air temperature (0.1C). Regional.|
|reg_max_air_temp_qa|Quality code for max_air_temp_reg|
|reg_min_air_temp|Minimum air temperature (0.1C). Regional.|
|reg_min_air_temp_qa|Quality code for min_air_temp|
|ground_temp|Ground surface temp (0.1C)|
|ground_temp_f|Ground surface temp (0.1F)|
|ground_temp_qa|Quality code for ground_temp|
|max_gust_dir|Degrees (0-360)|
|max_gust_dir_qa|Quality code for max_gust_dir|
|max_gust_speed|Speed of max wind gust M/s (0.1)|
|max_gust_speed_bft|Speed of max wind gust Beaufort|
|max_gust_speed_qa|Quality code for max_gust_speed|
|max_gust_time|Time of max wind gust|
|max_gust_time_qa|Quality code for max_gust_time|
|wind_run_lt10|Wind run taken from <10M (evaporation) Km|
|wind_run_lt10_miles|Wind run taken from <10M (evaporation) Miles|
|wind_run_lt10_period|Period in hours for Wind run <10|
|wind_run_lt10_qa|Quality code for wind_run_lt10|
|wind_run_gt10|Wind run taken from >10M anemometer Km|
|wind_run_gt10_miles|Wind run taken from >10M anemometer Miles|
|wind_run_gt10_period|Period in hours for Wind run >10|
|wind_run_gt10_qa|Quality code for wind_run_gt10|
|evaporation|Evaporation in mm (0.1)|
|evaporation_inches|Evaporation in inches (0.001)|
|evaporation_period|Period in hours for evaporation|
|evaporation_qa|Quality code for evaporation|
|evap_water_max_temp|Max water temp (0.1C)|
|evap_water_max_temp_f|Max water temp (0.1F)|
|evap_water_max_temp_qa|Quality code for evap_max_temp|
|evap_water_min_temp|Min water temp (0.1C)|
|evap_water_min_temp_f|Min water temp (0.1F)|
|evap_water_min_temp_qa|Quality code for evap_min_temp|
|sunshine_duration|Decimal Hours to (0.1)|
|sunshine_duration_qa|Quality code for sunshine_duration|
|river_height|Daily river height reading (0.1M)|
|river_height_qa|Quality code for river_height|
|radiation|Daily radiation Mj/M to 0.1|
|radiation_qa|Quality code for radiation|
|thunder_flag|Y/N for thunder|
|thunder_flag_qa|Quality code for thunder_flag|
|frost_flag|Y/N for frost|
|frost_flag_qa|Quality code for frost_flag|
|dust_flag|Y/N for dust|
|dust_flag_qa|Quality code for dust_flag|
|haze_flag|Y/N for haze|
|haze_flag_qa|Quality code for haze_flag|
|fog_flag|Y/N for fog|
|fog_flag_qa|Quality code for fog_flag|
|strong_wind_flag|Y/N for strong wind|
|strong_wind_flag_qa|Quality code for strong_wind_flag|
|gale_flag|Y/N for gale|
|gale_flag_qa|Quality code for gale_flag|
|hail_flag|Y/N for hail|
|hail_flag_qa|Quality code for hail_flag|
|snow_flag|Y/N for snow|
|snow_flag_qa|Quality code for snow_flag|
|lightning_flag|Y/N for lightning|
|lightning_flag_qa|Quality code for lightning_flag|
|shower_flag|Y/N for shower|
|shower_flag_qa|Quality code for shower_flag|
|rain_flag|Y/N for rain|
|rain_flag_qa|Quality code for rain_flag|
