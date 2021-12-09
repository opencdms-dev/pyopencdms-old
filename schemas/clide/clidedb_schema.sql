--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- Name: clideDB; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE "clideDB" IS 'Main CliDE database';


--
-- Name: plpgsql; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: postgres
--

CREATE OR REPLACE PROCEDURAL LANGUAGE plpgsql;


ALTER PROCEDURAL LANGUAGE plpgsql OWNER TO postgres;

SET search_path = public, pg_catalog;

--
-- Name: cube; Type: SHELL TYPE; Schema: public; Owner: clideadmin
--

CREATE TYPE cube;


--
-- Name: cube_in(cstring); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_in(cstring) RETURNS cube
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_in';


ALTER FUNCTION public.cube_in(cstring) OWNER TO clideadmin;

--
-- Name: cube_out(cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_out(cube) RETURNS cstring
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_out';


ALTER FUNCTION public.cube_out(cube) OWNER TO clideadmin;

--
-- Name: cube; Type: TYPE; Schema: public; Owner: clideadmin
--

CREATE TYPE cube (
    INTERNALLENGTH = variable,
    INPUT = cube_in,
    OUTPUT = cube_out,
    ALIGNMENT = double,
    STORAGE = plain
);


ALTER TYPE public.cube OWNER TO clideadmin;

--
-- Name: TYPE cube; Type: COMMENT; Schema: public; Owner: clideadmin
--

COMMENT ON TYPE cube IS 'multi-dimensional cube ''(FLOAT-1, FLOAT-2, ..., FLOAT-N), (FLOAT-1, FLOAT-2, ..., FLOAT-N)''';


--
-- Name: cube_dim(cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_dim(cube) RETURNS integer
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_dim';


ALTER FUNCTION public.cube_dim(cube) OWNER TO clideadmin;

--
-- Name: cube_distance(cube, cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_distance(cube, cube) RETURNS double precision
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_distance';


ALTER FUNCTION public.cube_distance(cube, cube) OWNER TO clideadmin;

--
-- Name: cube_is_point(cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_is_point(cube) RETURNS boolean
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_is_point';


ALTER FUNCTION public.cube_is_point(cube) OWNER TO clideadmin;

--
-- Name: earth(); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION earth() RETURNS double precision
    LANGUAGE sql IMMUTABLE
    AS $$SELECT '6378168'::float8$$;


ALTER FUNCTION public.earth() OWNER TO clideadmin;

--
-- Name: earth; Type: DOMAIN; Schema: public; Owner: clideadmin
--

CREATE DOMAIN earth AS cube
	CONSTRAINT not_3d CHECK ((cube_dim(VALUE) <= 3))
	CONSTRAINT not_point CHECK (cube_is_point(VALUE))
	CONSTRAINT on_surface CHECK ((abs(((cube_distance(VALUE, '(0)'::cube) / earth()) - (1)::double precision)) < 9.99999999999999955e-07::double precision));


ALTER DOMAIN public.earth OWNER TO clideadmin;

--
-- Name: tablefunc_crosstab_2; Type: TYPE; Schema: public; Owner: clideadmin
--

CREATE TYPE tablefunc_crosstab_2 AS (
	row_name text,
	category_1 text,
	category_2 text
);


ALTER TYPE public.tablefunc_crosstab_2 OWNER TO clideadmin;

--
-- Name: tablefunc_crosstab_3; Type: TYPE; Schema: public; Owner: clideadmin
--

CREATE TYPE tablefunc_crosstab_3 AS (
	row_name text,
	category_1 text,
	category_2 text,
	category_3 text
);


ALTER TYPE public.tablefunc_crosstab_3 OWNER TO clideadmin;

--
-- Name: tablefunc_crosstab_4; Type: TYPE; Schema: public; Owner: clideadmin
--

CREATE TYPE tablefunc_crosstab_4 AS (
	row_name text,
	category_1 text,
	category_2 text,
	category_3 text,
	category_4 text
);


ALTER TYPE public.tablefunc_crosstab_4 OWNER TO clideadmin;

--
-- Name: climat_data(character varying, date); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION climat_data(station_no character varying, yyyy_mm date) RETURNS TABLE(station_no character varying, lsd timestamp without time zone, station_pres numeric, msl_pres numeric, dew_point numeric, vapour_pres numeric, max_temp numeric, min_temp numeric, avg_temp numeric, temp_stddev numeric, rain numeric, rain_days bigint, sunshine numeric, max_rowcount bigint, min_rowcount bigint, rain_rowcount bigint, sunshine_rowcount bigint, pres_daycount bigint, vapour_daycount bigint, days_in_month double precision, max_gt_25_count bigint, max_gt_30_count bigint, max_gt_35_count bigint, max_gt_40_count bigint, min_lt_0_count bigint, max_lt_0_count bigint, rain_gt_1_count bigint, rain_gt_5_count bigint, rain_gt_10_count bigint, rain_gt_50_count bigint, rain_gt_100_count bigint, rain_gt_150_count bigint, wind_gt_10_count bigint, wind_gt_20_count bigint, wind_gt_30_count bigint, wind_daycount bigint, vis_lt_50m_count bigint, vis_lt_100m_count bigint, vis_lt_1km_count bigint, vis_daycount bigint, max_avg_temp text, max_avg_temp_dt text, min_avg_temp text, min_avg_temp_dt text, max_max_temp numeric, max_max_temp_dt text, min_min_temp numeric, min_min_temp_dt text, max_rain numeric, max_rain_dt text, max_gust numeric, max_gust_dt text, hail_count bigint, thunder_count bigint, utc_temp_time text, aws_flag character, day_count bigint)
    LANGUAGE sql ROWS 1
    AS $_$SELECT subday.station_no, subday.yyyy_mm AS lsd,
  subday.station_pres, subday.msl_pres, subday.dew_point, subday.vapour_pres,
  day.max_temp, day.min_temp, day.avg_temp, day.temp_stddev,
  day.rain, day.rain_days, day.sunshine,
  day.max_rowcount, day.min_rowcount,
  day.rain_rowcount, day.sunshine_rowcount, subday.pres_daycount, subday.vapour_daycount, 
  date_part('day'::text, date_trunc('month', subday.yyyy_mm) + '1 month'::interval - '1 day'::interval) AS days_in_month, 
  day.max_gt_25_count, day.max_gt_30_count, day.max_gt_35_count, day.max_gt_40_count,
  day.min_lt_0_count, day.max_lt_0_count,
  day.rain_gt_1_count, day.rain_gt_5_count, day.rain_gt_10_count, day.rain_gt_50_count, day.rain_gt_100_count,
  day.rain_gt_150_count,
  subday.wind_gt_10_count, subday.wind_gt_20_count, subday.wind_gt_30_count, subday.wind_daycount,
  subday.vis_lt_50m_count, subday.vis_lt_100m_count, subday.vis_lt_1km_count,
  subday.vis_daycount,
  to_char(day.max_avg_temp, '999.9'::text) AS max_avg_temp,
  to_char(max_avg_temp_dt.lsd, 'dd'::text) AS max_avg_temp_dt,
  to_char(day.min_avg_temp, '999.9'::text) AS min_avg_temp,
  to_char(min_avg_temp_dt.lsd, 'dd'::text) AS min_avg_temp_dt,
  day.max_max_temp, to_char(max_max_temp_dt.lsd, 'dd'::text) AS max_max_temp_dt,
  day.min_min_temp, to_char(min_min_temp_dt.lsd, 'dd'::text) AS min_min_temp_dt,
  day.max_rain, to_char(max_rain_dt.lsd, 'dd'::text) AS max_rain_dt, day.max_gust,
  to_char(max_gust_dt.lsd, 'dd'::text) AS max_gust_dt,
  day.hail_count,
  day.thunder_count, 
  substr(lct_to_utc(subday.station_no, (subday.yyyy_mm::date + '9 hours'::interval)::character varying)::text, 12, 2) AS utc_temp_time, 
  day.aws_flag, day.day_count 
   FROM ( SELECT sdd.station_no, 
            date_trunc('month', sdd.yyyy_mm_dd) AS yyyy_mm, 
            round(avg(iif_sql(sdd.pres_count >= 2, sdd.station_pres, NULL::numeric)), 1) AS station_pres, round(avg(iif_sql(sdd.pres_count >= 2, sdd.msl_pres, NULL::numeric)), 1) AS msl_pres, round(avg(sdd.dew_point), 1) AS dew_point, round(avg(sdd.vapour_pres), 1) AS vapour_pres, sum(iif_sql(sdd.pres_count >= 2, 1, 0)) AS pres_daycount, sum(iif_sql(sdd.vapour_count >= 2, 1, 0)) AS vapour_daycount, sum( 
                CASE 
                    WHEN sdd.avg_daily_wind > 10::numeric THEN 1 
                    ELSE 0 
                END) AS wind_gt_10_count, sum( 
                CASE 
                    WHEN sdd.avg_daily_wind > 20::numeric THEN 1 
                    ELSE 0 
                END) AS wind_gt_20_count, sum( 
                CASE 
                    WHEN sdd.avg_daily_wind > 30::numeric THEN 1 
                    ELSE 0 
                END) AS wind_gt_30_count, sum( 
                CASE 
                    WHEN sdd.daily_wind_count >= 8 THEN 1 
                    ELSE 0 
                END) AS wind_daycount, sum( 
                CASE 
                    WHEN sdd.min_daily_visibility < 0.05 THEN 1 
                    ELSE 0 
                END) AS vis_lt_50m_count, sum( 
                CASE 
                    WHEN sdd.min_daily_visibility < 0.1 THEN 1 
                    ELSE 0 
                END) AS vis_lt_100m_count, sum( 
                CASE 
                    WHEN sdd.min_daily_visibility < 1::numeric THEN 1 
                    ELSE 0 
                END) AS vis_lt_1km_count, sum( 
                CASE 
                    WHEN sdd.daily_vis_count > 0 THEN 1 
                    ELSE 0 
                END) AS vis_daycount 
           FROM ( SELECT sd.station_no, 
                    date_trunc('day', sd.lsd) AS yyyy_mm_dd, 
                    avg(sd.station_pres) AS station_pres, avg(sd.msl_pres) AS msl_pres, avg(sd.dew_point) AS dew_point, avg(exp(1.8096 + 17.269425 * sd.dew_point / (237.3 + sd.dew_point))) AS vapour_pres, count(sd.station_pres) AS pres_count, count(sd.dew_point) AS vapour_count, avg(sd.wind_speed) AS avg_daily_wind, count(sd.wind_speed) AS daily_wind_count, min(sd.visibility) AS min_daily_visibility, count(sd.visibility) AS daily_vis_count 
                   FROM obs_subdaily sd 
                   WHERE station_no = $1
                     AND date_trunc('month', sd.lsd) = $2
                  GROUP BY sd.station_no, date_trunc('day', sd.lsd)) sdd 
          GROUP BY sdd.station_no, date_trunc('month', sdd.yyyy_mm_dd)) subday 
   JOIN ( SELECT d.station_no AS stationno, 
            date_trunc('month', d.lsd) AS yyyymm, 
            round(avg(d.max_air_temp), 1) AS max_temp, round(avg(d.min_air_temp), 1) AS min_temp, round(avg((d.max_air_temp + d.min_air_temp) / 2::numeric), 1) AS avg_temp, round(stddev((d.max_air_temp + d.min_air_temp) / 2::numeric), 1) AS temp_stddev, round(sum(d.rain_24h), 0) AS rain, sum( 
                CASE 
                    WHEN d.rain_24h >= 1::numeric THEN 1 
                    ELSE 0 
                END) AS rain_days, round(sum(d.sunshine_duration), 0) AS sunshine, count(d.max_air_temp) AS max_rowcount, count(d.min_air_temp) AS min_rowcount, count(d.rain_24h) AS rain_rowcount, count(d.sunshine_duration) AS sunshine_rowcount, sum( 
                CASE 
                    WHEN d.max_air_temp >= 25::numeric THEN 1 
                    ELSE 0 
                END) AS max_gt_25_count, sum( 
                CASE 
                    WHEN d.max_air_temp >= 30::numeric THEN 1 
                    ELSE 0 
                END) AS max_gt_30_count, sum( 
                CASE 
                    WHEN d.max_air_temp >= 35::numeric THEN 1 
                    ELSE 0 
                END) AS max_gt_35_count, sum( 
                CASE 
                    WHEN d.max_air_temp >= 40::numeric THEN 1 
                    ELSE 0 
                END) AS max_gt_40_count, sum( 
                CASE 
                    WHEN d.min_air_temp < 0::numeric THEN 1 
                    ELSE 0 
                END) AS min_lt_0_count, sum( 
                CASE 
                    WHEN d.max_air_temp < 0::numeric THEN 1 
                    ELSE 0 
                END) AS max_lt_0_count, sum( 
                CASE 
                    WHEN d.rain_24h >= 1::numeric THEN 1 
                    ELSE 0 
                END) AS rain_gt_1_count, sum( 
                CASE 
                    WHEN d.rain_24h >= 5::numeric THEN 1 
                    ELSE 0 
                END) AS rain_gt_5_count, sum( 
                CASE 
                    WHEN d.rain_24h >= 10::numeric THEN 1 
                    ELSE 0 
                END) AS rain_gt_10_count, sum( 
                CASE 
                    WHEN d.rain_24h >= 50::numeric THEN 1 
                    ELSE 0 
                END) AS rain_gt_50_count, sum( 
                CASE 
                    WHEN d.rain_24h >= 100::numeric THEN 1 
                    ELSE 0 
                END) AS rain_gt_100_count, sum( 
                CASE 
                    WHEN d.rain_24h >= 150::numeric THEN 1 
                    ELSE 0 
                END) AS rain_gt_150_count, max((d.max_air_temp + d.min_air_temp) / 2::numeric) AS max_avg_temp, min((d.max_air_temp + d.min_air_temp) / 2::numeric) AS min_avg_temp, max(d.max_air_temp) AS max_max_temp, min(d.min_air_temp) AS min_min_temp, max(d.rain_24h) AS max_rain, max(d.max_gust_speed) AS max_gust, sum( 
                CASE 
                    WHEN d.hail_flag = 'Y'::bpchar THEN 1 
                    ELSE 0 
                END) AS hail_count, sum( 
                CASE 
                    WHEN d.thunder_flag = 'Y'::bpchar THEN 1 
                    ELSE 0 
                END) AS thunder_count, 'N'::character(1) AS aws_flag, count(*) AS day_count 
           FROM obs_daily d 
           WHERE station_no = $1
             AND date_trunc('month', d.lsd) = $2
          GROUP BY d.station_no, date_trunc('month', d.lsd)) day 
     ON subday.station_no::text = day.stationno::text AND subday.yyyy_mm = day.yyyymm 
   LEFT JOIN obs_daily max_avg_temp_dt ON day.stationno::text = max_avg_temp_dt.station_no::text AND date_trunc('month', max_avg_temp_dt.lsd) = day.yyyymm AND ((max_avg_temp_dt.max_air_temp + max_avg_temp_dt.min_air_temp) / 2::numeric) = day.max_avg_temp 
   LEFT JOIN obs_daily min_avg_temp_dt ON day.stationno::text = min_avg_temp_dt.station_no::text AND date_trunc('month', min_avg_temp_dt.lsd) = day.yyyymm AND ((min_avg_temp_dt.max_air_temp + min_avg_temp_dt.min_air_temp) / 2::numeric) = day.min_avg_temp 
   LEFT JOIN obs_daily max_max_temp_dt ON day.stationno::text = max_max_temp_dt.station_no::text AND date_trunc('month', max_max_temp_dt.lsd) = day.yyyymm AND max_max_temp_dt.max_air_temp = day.max_max_temp 
   LEFT JOIN obs_daily min_min_temp_dt ON day.stationno::text = min_min_temp_dt.station_no::text AND date_trunc('month', min_min_temp_dt.lsd) = day.yyyymm AND min_min_temp_dt.min_air_temp = day.min_min_temp 
   LEFT JOIN obs_daily max_rain_dt ON day.stationno::text = max_rain_dt.station_no::text AND date_trunc('month', max_rain_dt.lsd) = day.yyyymm AND max_rain_dt.rain_24h = day.max_rain 
   LEFT JOIN obs_daily max_gust_dt ON day.stationno::text = max_gust_dt.station_no::text AND date_trunc('month', max_gust_dt.lsd) = day.yyyymm AND max_gust_dt.max_gust_speed = day.max_gust 
WHERE subday.station_no = $1
  AND subday.yyyy_mm = $2;$_$;


ALTER FUNCTION public.climat_data(station_no character varying, yyyy_mm date) OWNER TO postgres;

--
-- Name: connectby(text, text, text, text, integer); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION connectby(text, text, text, text, integer) RETURNS SETOF record
    LANGUAGE c STABLE STRICT
    AS '$libdir/tablefunc', 'connectby_text';


ALTER FUNCTION public.connectby(text, text, text, text, integer) OWNER TO clideadmin;

--
-- Name: connectby(text, text, text, text, integer, text); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION connectby(text, text, text, text, integer, text) RETURNS SETOF record
    LANGUAGE c STABLE STRICT
    AS '$libdir/tablefunc', 'connectby_text';


ALTER FUNCTION public.connectby(text, text, text, text, integer, text) OWNER TO clideadmin;

--
-- Name: connectby(text, text, text, text, text, integer); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION connectby(text, text, text, text, text, integer) RETURNS SETOF record
    LANGUAGE c STABLE STRICT
    AS '$libdir/tablefunc', 'connectby_text_serial';


ALTER FUNCTION public.connectby(text, text, text, text, text, integer) OWNER TO clideadmin;

--
-- Name: connectby(text, text, text, text, text, integer, text); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION connectby(text, text, text, text, text, integer, text) RETURNS SETOF record
    LANGUAGE c STABLE STRICT
    AS '$libdir/tablefunc', 'connectby_text_serial';


ALTER FUNCTION public.connectby(text, text, text, text, text, integer, text) OWNER TO clideadmin;

--
-- Name: crosstab(text); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION crosstab(text) RETURNS SETOF record
    LANGUAGE c STABLE STRICT
    AS '$libdir/tablefunc', 'crosstab';


ALTER FUNCTION public.crosstab(text) OWNER TO clideadmin;

--
-- Name: crosstab(text, integer); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION crosstab(text, integer) RETURNS SETOF record
    LANGUAGE c STABLE STRICT
    AS '$libdir/tablefunc', 'crosstab';


ALTER FUNCTION public.crosstab(text, integer) OWNER TO clideadmin;

--
-- Name: crosstab(text, text); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION crosstab(text, text) RETURNS SETOF record
    LANGUAGE c STABLE STRICT
    AS '$libdir/tablefunc', 'crosstab_hash';


ALTER FUNCTION public.crosstab(text, text) OWNER TO clideadmin;

--
-- Name: crosstab2(text); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION crosstab2(text) RETURNS SETOF tablefunc_crosstab_2
    LANGUAGE c STABLE STRICT
    AS '$libdir/tablefunc', 'crosstab';


ALTER FUNCTION public.crosstab2(text) OWNER TO clideadmin;

--
-- Name: crosstab3(text); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION crosstab3(text) RETURNS SETOF tablefunc_crosstab_3
    LANGUAGE c STABLE STRICT
    AS '$libdir/tablefunc', 'crosstab';


ALTER FUNCTION public.crosstab3(text) OWNER TO clideadmin;

--
-- Name: crosstab4(text); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION crosstab4(text) RETURNS SETOF tablefunc_crosstab_4
    LANGUAGE c STABLE STRICT
    AS '$libdir/tablefunc', 'crosstab';


ALTER FUNCTION public.crosstab4(text) OWNER TO clideadmin;

--
-- Name: cube(double precision[]); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube(double precision[]) RETURNS cube
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_a_f8';


ALTER FUNCTION public.cube(double precision[]) OWNER TO clideadmin;

--
-- Name: cube(double precision); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube(double precision) RETURNS cube
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_f8';


ALTER FUNCTION public.cube(double precision) OWNER TO clideadmin;

--
-- Name: cube(double precision[], double precision[]); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube(double precision[], double precision[]) RETURNS cube
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_a_f8_f8';


ALTER FUNCTION public.cube(double precision[], double precision[]) OWNER TO clideadmin;

--
-- Name: cube(double precision, double precision); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube(double precision, double precision) RETURNS cube
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_f8_f8';


ALTER FUNCTION public.cube(double precision, double precision) OWNER TO clideadmin;

--
-- Name: cube(cube, double precision); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube(cube, double precision) RETURNS cube
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_c_f8';


ALTER FUNCTION public.cube(cube, double precision) OWNER TO clideadmin;

--
-- Name: cube(cube, double precision, double precision); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube(cube, double precision, double precision) RETURNS cube
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_c_f8_f8';


ALTER FUNCTION public.cube(cube, double precision, double precision) OWNER TO clideadmin;

--
-- Name: cube_cmp(cube, cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_cmp(cube, cube) RETURNS integer
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_cmp';


ALTER FUNCTION public.cube_cmp(cube, cube) OWNER TO clideadmin;

--
-- Name: FUNCTION cube_cmp(cube, cube); Type: COMMENT; Schema: public; Owner: clideadmin
--

COMMENT ON FUNCTION cube_cmp(cube, cube) IS 'btree comparison function';


--
-- Name: cube_contained(cube, cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_contained(cube, cube) RETURNS boolean
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_contained';


ALTER FUNCTION public.cube_contained(cube, cube) OWNER TO clideadmin;

--
-- Name: FUNCTION cube_contained(cube, cube); Type: COMMENT; Schema: public; Owner: clideadmin
--

COMMENT ON FUNCTION cube_contained(cube, cube) IS 'contained in';


--
-- Name: cube_contains(cube, cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_contains(cube, cube) RETURNS boolean
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_contains';


ALTER FUNCTION public.cube_contains(cube, cube) OWNER TO clideadmin;

--
-- Name: FUNCTION cube_contains(cube, cube); Type: COMMENT; Schema: public; Owner: clideadmin
--

COMMENT ON FUNCTION cube_contains(cube, cube) IS 'contains';


--
-- Name: cube_enlarge(cube, double precision, integer); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_enlarge(cube, double precision, integer) RETURNS cube
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_enlarge';


ALTER FUNCTION public.cube_enlarge(cube, double precision, integer) OWNER TO clideadmin;

--
-- Name: cube_eq(cube, cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_eq(cube, cube) RETURNS boolean
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_eq';


ALTER FUNCTION public.cube_eq(cube, cube) OWNER TO clideadmin;

--
-- Name: FUNCTION cube_eq(cube, cube); Type: COMMENT; Schema: public; Owner: clideadmin
--

COMMENT ON FUNCTION cube_eq(cube, cube) IS 'same as';


--
-- Name: cube_ge(cube, cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_ge(cube, cube) RETURNS boolean
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_ge';


ALTER FUNCTION public.cube_ge(cube, cube) OWNER TO clideadmin;

--
-- Name: FUNCTION cube_ge(cube, cube); Type: COMMENT; Schema: public; Owner: clideadmin
--

COMMENT ON FUNCTION cube_ge(cube, cube) IS 'greater than or equal to';


--
-- Name: cube_gt(cube, cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_gt(cube, cube) RETURNS boolean
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_gt';


ALTER FUNCTION public.cube_gt(cube, cube) OWNER TO clideadmin;

--
-- Name: FUNCTION cube_gt(cube, cube); Type: COMMENT; Schema: public; Owner: clideadmin
--

COMMENT ON FUNCTION cube_gt(cube, cube) IS 'greater than';


--
-- Name: cube_inter(cube, cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_inter(cube, cube) RETURNS cube
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_inter';


ALTER FUNCTION public.cube_inter(cube, cube) OWNER TO clideadmin;

--
-- Name: cube_le(cube, cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_le(cube, cube) RETURNS boolean
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_le';


ALTER FUNCTION public.cube_le(cube, cube) OWNER TO clideadmin;

--
-- Name: FUNCTION cube_le(cube, cube); Type: COMMENT; Schema: public; Owner: clideadmin
--

COMMENT ON FUNCTION cube_le(cube, cube) IS 'lower than or equal to';


--
-- Name: cube_ll_coord(cube, integer); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_ll_coord(cube, integer) RETURNS double precision
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_ll_coord';


ALTER FUNCTION public.cube_ll_coord(cube, integer) OWNER TO clideadmin;

--
-- Name: cube_lt(cube, cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_lt(cube, cube) RETURNS boolean
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_lt';


ALTER FUNCTION public.cube_lt(cube, cube) OWNER TO clideadmin;

--
-- Name: FUNCTION cube_lt(cube, cube); Type: COMMENT; Schema: public; Owner: clideadmin
--

COMMENT ON FUNCTION cube_lt(cube, cube) IS 'lower than';


--
-- Name: cube_ne(cube, cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_ne(cube, cube) RETURNS boolean
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_ne';


ALTER FUNCTION public.cube_ne(cube, cube) OWNER TO clideadmin;

--
-- Name: FUNCTION cube_ne(cube, cube); Type: COMMENT; Schema: public; Owner: clideadmin
--

COMMENT ON FUNCTION cube_ne(cube, cube) IS 'different';


--
-- Name: cube_overlap(cube, cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_overlap(cube, cube) RETURNS boolean
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_overlap';


ALTER FUNCTION public.cube_overlap(cube, cube) OWNER TO clideadmin;

--
-- Name: FUNCTION cube_overlap(cube, cube); Type: COMMENT; Schema: public; Owner: clideadmin
--

COMMENT ON FUNCTION cube_overlap(cube, cube) IS 'overlaps';


--
-- Name: cube_size(cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_size(cube) RETURNS double precision
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_size';


ALTER FUNCTION public.cube_size(cube) OWNER TO clideadmin;

--
-- Name: cube_subset(cube, integer[]); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_subset(cube, integer[]) RETURNS cube
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_subset';


ALTER FUNCTION public.cube_subset(cube, integer[]) OWNER TO clideadmin;

--
-- Name: cube_union(cube, cube); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_union(cube, cube) RETURNS cube
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_union';


ALTER FUNCTION public.cube_union(cube, cube) OWNER TO clideadmin;

--
-- Name: cube_ur_coord(cube, integer); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION cube_ur_coord(cube, integer) RETURNS double precision
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'cube_ur_coord';


ALTER FUNCTION public.cube_ur_coord(cube, integer) OWNER TO clideadmin;

--
-- Name: earth_box(earth, double precision); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION earth_box(earth, double precision) RETURNS cube
    LANGUAGE sql IMMUTABLE STRICT
    AS $_$SELECT cube_enlarge($1, gc_to_sec($2), 3)$_$;


ALTER FUNCTION public.earth_box(earth, double precision) OWNER TO clideadmin;

--
-- Name: earth_distance(earth, earth); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION earth_distance(earth, earth) RETURNS double precision
    LANGUAGE sql IMMUTABLE STRICT
    AS $_$SELECT sec_to_gc(cube_distance($1, $2))$_$;


ALTER FUNCTION public.earth_distance(earth, earth) OWNER TO clideadmin;

--
-- Name: g_cube_compress(internal); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION g_cube_compress(internal) RETURNS internal
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'g_cube_compress';


ALTER FUNCTION public.g_cube_compress(internal) OWNER TO clideadmin;

--
-- Name: g_cube_consistent(internal, cube, integer, oid, internal); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION g_cube_consistent(internal, cube, integer, oid, internal) RETURNS boolean
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'g_cube_consistent';


ALTER FUNCTION public.g_cube_consistent(internal, cube, integer, oid, internal) OWNER TO clideadmin;

--
-- Name: g_cube_decompress(internal); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION g_cube_decompress(internal) RETURNS internal
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'g_cube_decompress';


ALTER FUNCTION public.g_cube_decompress(internal) OWNER TO clideadmin;

--
-- Name: g_cube_penalty(internal, internal, internal); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION g_cube_penalty(internal, internal, internal) RETURNS internal
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'g_cube_penalty';


ALTER FUNCTION public.g_cube_penalty(internal, internal, internal) OWNER TO clideadmin;

--
-- Name: g_cube_picksplit(internal, internal); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION g_cube_picksplit(internal, internal) RETURNS internal
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'g_cube_picksplit';


ALTER FUNCTION public.g_cube_picksplit(internal, internal) OWNER TO clideadmin;

--
-- Name: g_cube_same(cube, cube, internal); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION g_cube_same(cube, cube, internal) RETURNS internal
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'g_cube_same';


ALTER FUNCTION public.g_cube_same(cube, cube, internal) OWNER TO clideadmin;

--
-- Name: g_cube_union(internal, internal); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION g_cube_union(internal, internal) RETURNS cube
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/cube', 'g_cube_union';


ALTER FUNCTION public.g_cube_union(internal, internal) OWNER TO clideadmin;

--
-- Name: gc_to_sec(double precision); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION gc_to_sec(double precision) RETURNS double precision
    LANGUAGE sql IMMUTABLE STRICT
    AS $_$SELECT CASE WHEN $1 < 0 THEN 0::float8 WHEN $1/earth() > pi() THEN 2*earth() ELSE 2*earth()*sin($1/(2*earth())) END$_$;


ALTER FUNCTION public.gc_to_sec(double precision) OWNER TO clideadmin;

--
-- Name: geo_distance(point, point); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION geo_distance(point, point) RETURNS double precision
    LANGUAGE c IMMUTABLE STRICT
    AS '$libdir/earthdistance', 'geo_distance';


ALTER FUNCTION public.geo_distance(point, point) OWNER TO clideadmin;

--
-- Name: iif_sql(boolean, anyelement, anyelement); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION iif_sql(boolean, anyelement, anyelement) RETURNS anyelement
    LANGUAGE sql IMMUTABLE
    AS $_$ SELECT case $1 when true then $2 else $3 end $_$;


ALTER FUNCTION public.iif_sql(boolean, anyelement, anyelement) OWNER TO postgres;

--
-- Name: key_summary(date, date); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION key_summary(from_date date, to_date date) RETURNS TABLE(change_user character varying, tab character varying, first_date date, last_date date, rows_keyed bigint, days double precision, number_of_stations bigint, pct character varying)
    LANGUAGE sql ROWS 1
    AS $_$
select
  o.change_user,
  'daily' as tab,
  min(o.lsd)::date as first_date,
  max(o.lsd)::date as last_date,
  count(o.*) as rows_keyed,
  (max(o.lsd)::date - min(o.lsd)::date) + 1 as days,
  (SELECT COUNT (agg.*)
    FROM (SELECT distinct o2.station_no
          FROM obs_daily o2
          WHERE date_trunc('day', o2.insert_datetime) >= $1
            AND date_trunc('day', o2.insert_datetime) <= $2
            AND o2.change_user = o.change_user) agg) as number_of_stations,
  TO_CHAR(( count(*)::double precision / (((max(o.lsd)::date - min(o.lsd)::date) + 1) * (SELECT COUNT (agg.*)
      FROM (SELECT distinct o2.station_no
            FROM obs_daily o2
            WHERE date_trunc('day', o2.insert_datetime) >= $1
              AND date_trunc('day', o2.insert_datetime) <= $2
              AND o2.change_user = o.change_user) agg)) ) * 100, '990.0%') as pct
from obs_daily o
where date_trunc('day', o.insert_datetime) >= $1
  and date_trunc('day', o.insert_datetime) <= $2
group by change_user, tab

UNION

select
  o.change_user,
  'subdaily' as tab,
  min(o.lsd::date) as first_date,
  max(o.lsd::date) as last_date,
  count(o.*) as rows_keyed,
  (date_trunc('day', max(o.lsd))::date - date_trunc('day', min(o.lsd))::date) + 1 as days,
  (SELECT COUNT (agg.*)
    FROM (SELECT distinct o2.station_no
          FROM obs_subdaily o2
          WHERE date_trunc('day', o2.insert_datetime) >= $1
            AND date_trunc('day', o2.insert_datetime) <= $2
            AND o2.change_user = o.change_user) agg) as number_of_stations,
  '-' as pct
from obs_subdaily o
where date_trunc('day', o.insert_datetime) >= $1
  and date_trunc('day', o.insert_datetime) <= $2
group by change_user, tab

UNION

select
  o.change_user,
  'monthly' as tab,
  min(o.lsd::date) as first_date,
  max(o.lsd::date) as last_date,
  count(o.*) as rows_keyed,
  (EXTRACT(year FROM age(date_trunc('month', max(o.lsd)::date), date_trunc('month', min(o.lsd)::date)))*12 +
    EXTRACT(month FROM age(date_trunc('month', max(o.lsd)::date), date_trunc('month', min(o.lsd)::date))) + 1) as days,
  (SELECT COUNT (agg.*)
    FROM (SELECT distinct o2.station_no
          FROM obs_monthly o2
          WHERE date_trunc('day', o2.insert_datetime) >= $1
            AND date_trunc('day', o2.insert_datetime) <= $2
            AND o2.change_user = o.change_user) agg) as number_of_stations,
  TO_CHAR(count(*)::double precision /
    ((EXTRACT(year FROM age(date_trunc('month', max(o.lsd)::date), date_trunc('month', min(o.lsd)::date)))*12 +
    EXTRACT(month FROM age(date_trunc('month', max(o.lsd)::date), date_trunc('month', min(o.lsd)::date))) + 1) * (SELECT COUNT (agg.*)
      FROM (SELECT distinct o2.station_no
            FROM obs_monthly o2
            WHERE date_trunc('day', o2.insert_datetime) >= $1
              AND date_trunc('day', o2.insert_datetime) <= $2
              AND o2.change_user = o.change_user) agg))
    * 100, '990.0%') as pct
from obs_monthly o
where date_trunc('day', o.insert_datetime) >= $1
  and date_trunc('day', o.insert_datetime) <= $2
group by change_user, tab

UNION

select
  o.change_user,
  'aero' as tab,
  min(o.lsd::date) as first_date,
  max(o.lsd::date) as last_date,
  count(o.*) as rows_keyed,
  (date_trunc('day', max(o.lsd))::date - date_trunc('day', min(o.lsd))::date) + 1 as days,
  (SELECT COUNT (agg.*)
    FROM (SELECT distinct o2.station_no
          FROM obs_aero o2
          WHERE date_trunc('day', o2.insert_datetime) >= $1
            AND date_trunc('day', o2.insert_datetime) <= $2
            AND o2.change_user = o.change_user) agg) as number_of_stations,
  '-' as pct
from obs_aero o
where date_trunc('day', o.insert_datetime) >= $1
  and date_trunc('day', o.insert_datetime) <= $2
group by change_user, tab

order by change_user, tab;
$_$;


ALTER FUNCTION public.key_summary(from_date date, to_date date) OWNER TO postgres;

--
-- Name: key_summary_with_stations(date, date); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION key_summary_with_stations(from_date date, to_date date) RETURNS TABLE(change_user character varying, tab character varying, station_no character varying, first_date date, last_date date, rows_keyed bigint, days double precision, pct character varying)
    LANGUAGE sql ROWS 1
    AS $_$

select
  change_user,
  'daily' as tab,
  station_no,
  min(lsd)::date as first_date,
  max(lsd)::date as last_date,
  count(*) as rows_keyed,
  (max(lsd)::date - min(lsd)::date) + 1 as days,
  TO_CHAR(( count(*)::double precision / ((max(lsd)::date - min(lsd)::date) + 1) ) * 100.0, '990.0%') as pct
from obs_daily
where insert_datetime::date >= $1
  and insert_datetime::date <= $2
group by change_user, tab, station_no

UNION

select
  change_user,
  'subdaily' as tab,
  station_no,
  min(lsd::date) as first_date,
  max(lsd::date) as last_date,
  count(*) as rows_keyed,
  (date_trunc('day', max(lsd))::date - date_trunc('day', min(lsd))::date) + 1 as days,
  '-' as pct
from obs_subdaily
where date_trunc('day', insert_datetime) >= $1
  and date_trunc('day', insert_datetime) <= $2
group by change_user, tab, station_no

UNION

select
  change_user,
  'monthly' as tab,
  station_no,
  min(lsd::date) as first_date,
  max(lsd::date) as last_date,
  count(*) as rows_keyed,
  (EXTRACT(year FROM age(date_trunc('month', max(lsd)::date), date_trunc('month', min(lsd)::date)))*12 +
    EXTRACT(month FROM age(date_trunc('month', max(lsd)::date), date_trunc('month', min(lsd)::date))) + 1) as days,
  TO_CHAR(count(*)::double precision /
    (EXTRACT(year FROM age(date_trunc('month', max(lsd)::date), date_trunc('month', min(lsd)::date)))*12 +
    EXTRACT(month FROM age(date_trunc('month', max(lsd)::date), date_trunc('month', min(lsd)::date))) + 1)
    * 100.0, '990.0%') as pct
from obs_monthly
where date_trunc('day', insert_datetime) >= $1
  and date_trunc('day', insert_datetime) <= $2
group by change_user, tab, station_no

UNION

select
  change_user,
  'aero' as tab,
  station_no,
  min(lsd::date) as first_date,
  max(lsd::date) as last_date,
  count(*) as rows_keyed,
  (date_trunc('day', max(lsd))::date - date_trunc('day', min(lsd))::date) + 1 as days,
  '-' as pct
from obs_aero
where date_trunc('day', insert_datetime) >= $1
  and date_trunc('day', insert_datetime) <= $2
group by change_user, tab, station_no

order by change_user, tab, station_no;
$_$;


ALTER FUNCTION public.key_summary_with_stations(from_date date, to_date date) OWNER TO postgres;

--
-- Name: latitude(earth); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION latitude(earth) RETURNS double precision
    LANGUAGE sql IMMUTABLE STRICT
    AS $_$SELECT CASE WHEN cube_ll_coord($1, 3)/earth() < -1 THEN -90::float8 WHEN cube_ll_coord($1, 3)/earth() > 1 THEN 90::float8 ELSE degrees(asin(cube_ll_coord($1, 3)/earth())) END$_$;


ALTER FUNCTION public.latitude(earth) OWNER TO clideadmin;

--
-- Name: lct_to_lsd(character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION lct_to_lsd(station character varying, lct character varying) RETURNS character varying
    LANGUAGE sql STABLE
    AS $_$
SELECT
  CASE WHEN tm_diff IS NULL THEN $2
       ELSE TO_CHAR($2::timestamp without time zone - CAST((tm_diff - utc_diff)||' hours' AS INTERVAL), 'yyyy-mm-dd HH24:mi')
  END as return_lsd
FROM stations AS s
     INNER JOIN station_timezones AS st ON st.tm_zone = s.time_zone
     LEFT JOIN timezone_diffs AS td ON td.tm_zone = s.time_zone
                                   AND start_timestamp <= $2::date
                                   AND end_timestamp >= $2::date
WHERE station_no = $1;
$_$;


ALTER FUNCTION public.lct_to_lsd(station character varying, lct character varying) OWNER TO postgres;

--
-- Name: lct_to_utc(character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION lct_to_utc(station character varying, lct character varying) RETURNS character varying
    LANGUAGE sql STABLE
    AS $_$
SELECT
  TO_CHAR($2::timestamp without time zone - CAST(CASE WHEN tm_diff IS NULL THEN utc_diff ELSE tm_diff END||' hours' AS INTERVAL), 'yyyy-mm-dd HH24:mi') as return_utc
FROM stations AS s
     INNER JOIN station_timezones AS st ON st.tm_zone = s.time_zone
     LEFT JOIN timezone_diffs AS td ON td.tm_zone = s.time_zone
                                   AND start_timestamp <= $2::date
                                   AND end_timestamp >= $2::date
WHERE station_no = $1;
$_$;


ALTER FUNCTION public.lct_to_utc(station character varying, lct character varying) OWNER TO postgres;

--
-- Name: ll_to_earth(double precision, double precision); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION ll_to_earth(double precision, double precision) RETURNS earth
    LANGUAGE sql IMMUTABLE STRICT
    AS $_$SELECT cube(cube(cube(earth()*cos(radians($1))*cos(radians($2))),earth()*cos(radians($1))*sin(radians($2))),earth()*sin(radians($1)))::earth$_$;


ALTER FUNCTION public.ll_to_earth(double precision, double precision) OWNER TO clideadmin;

--
-- Name: longitude(earth); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION longitude(earth) RETURNS double precision
    LANGUAGE sql IMMUTABLE STRICT
    AS $_$SELECT degrees(atan2(cube_ll_coord($1, 2), cube_ll_coord($1, 1)))$_$;


ALTER FUNCTION public.longitude(earth) OWNER TO clideadmin;

--
-- Name: lsd_to_lct(character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION lsd_to_lct(station character varying, lsd character varying) RETURNS character varying
    LANGUAGE sql STABLE
    AS $_$
SELECT
  CASE WHEN tm_diff IS NULL THEN $2
       ELSE TO_CHAR($2::timestamp without time zone - CAST((utc_diff - tm_diff)||' hours' AS INTERVAL), 'yyyy-mm-dd HH24:mi')
  END as return_lct
FROM stations AS s
     INNER JOIN station_timezones AS st ON st.tm_zone = s.time_zone
     LEFT JOIN timezone_diffs AS td ON td.tm_zone = s.time_zone
                                   AND start_timestamp <= $2::date
                                   AND end_timestamp >= $2::date
WHERE station_no = $1;
$_$;


ALTER FUNCTION public.lsd_to_lct(station character varying, lsd character varying) OWNER TO postgres;

--
-- Name: lsd_to_utc(character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION lsd_to_utc(station character varying, lsd character varying) RETURNS character varying
    LANGUAGE sql STABLE
    AS $_$
SELECT
  TO_CHAR($2::timestamp without time zone - CAST(utc_diff||' hours' AS INTERVAL), 'yyyy-mm-dd HH24:mi') as return_utc
FROM stations AS s
     INNER JOIN station_timezones AS st ON st.tm_zone = s.time_zone
WHERE station_no = $1;
$_$;


ALTER FUNCTION public.lsd_to_utc(station character varying, lsd character varying) OWNER TO postgres;

--
-- Name: monthly_obs(character varying[], character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION monthly_obs(station_array character varying[], nfrom character varying, nto character varying) RETURNS TABLE(station_no character varying, yyyy_mm character varying, max_max_air_temp numeric, min_min_air_temp numeric, min_min_ground_temp numeric, mn_min_ground_temp numeric, mn_max_air_temp numeric, mn_min_air_temp numeric, mn_air_temp numeric, dly_max_rain numeric, tot_rain numeric, tot_rain_days numeric, tot_rain_percent double precision, mn_evaporation numeric, tot_evaporation numeric, mn_sun_hours numeric, mn_asread_pres numeric, mn_msl_pres numeric, mn_station_pres numeric, mn_vapour_pres numeric, mn_rel_humidity numeric, mn_tot_cloud_oktas numeric, mn_wet_bulb_temp numeric)
    LANGUAGE sql
    AS $_$
SELECT daily.station_no,
	daily.yyyy_mm,
	max_max_air_temp,
	min_min_air_temp,
	min_min_ground_temp,
	mn_min_ground_temp,
	mn_max_air_temp,
	mn_min_air_temp,
	mn_air_temp,
	dly_max_rain,
	tot_rain,
	tot_rain_days,
	(missing_count/days_in_month)*100 as tot_rain_percent,
	mn_evaporation,
	tot_evaporation,
	mn_sun_hours,
	mn_asread_pres,
	mn_msl_pres,
	mn_station_pres,
	mn_vapour_pres,
	mn_rel_humidity,
	mn_tot_cloud_oktas,
	mn_wet_bulb_temp
FROM (
--Daily columns
SELECT  station_no,
	to_char(lsd, 'yyyy-mm') as yyyy_mm,
	max(max_air_temp) as max_max_air_temp,
	min(min_air_temp) as min_min_air_temp,
	min(ground_temp) as min_min_ground_temp,
	avg(ground_temp) as mn_min_ground_temp,
	avg(max_air_temp) as mn_max_air_temp,
	avg(min_air_temp) as mn_min_air_temp,
	avg((max_air_temp + min_air_temp)/2) as mn_air_temp,
	max(rain_24h) as dly_max_rain,
	sum(rain_24h) as tot_rain,
	sum(rain_24h_count) as tot_rain_days,
	date_part('day'::text, (((("substring"(to_char(lsd, 'yyyy-mm'), 1, 4) || '-'::text) || "substring"(to_char(lsd, 'yyyy-mm'), 6, 2)) || '-01'::text)::date) + '1 mon'::interval - '1 day'::interval) as days_in_month,
	sum(CASE WHEN rain_24h_qa = '00' THEN 1 ELSE 0 END) as missing_count,
	avg(evaporation) as mn_evaporation,
	sum(evaporation) as tot_evaporation,
	avg(sunshine_duration) as mn_sun_hours
FROM obs_daily
WHERE station_no = ANY($1)
AND lsd >= to_timestamp($2, 'yyyy-mm')
AND lsd < to_timestamp($3, 'yyyy-mm') + '1 month'::interval
GROUP BY station_no, to_char(lsd, 'yyyy-mm')
) daily

FULL JOIN (
--Sub Daily columns
SELECT  station_no,
	to_char(lsd, 'yyyy-mm') as yyyy_mm,
	avg(pres_as_read) as mn_asread_pres,
	avg(msl_pres) as mn_msl_pres,
	avg(station_pres) as mn_station_pres,
	avg(vapour_pres) as mn_vapour_pres,
	avg(rel_humidity) as mn_rel_humidity,
	avg(tot_cloud_oktas) as mn_tot_cloud_oktas,
	avg(wet_bulb) as mn_wet_bulb_temp
FROM obs_subdaily
WHERE station_no = ANY($1)
AND lsd >= to_timestamp($2, 'yyyy-mm')
AND lsd < to_timestamp($3, 'yyyy-mm') + '1 month'::interval
GROUP BY station_no, to_char(lsd, 'yyyy-mm')
) subdaily
ON daily.station_no = subdaily.station_no
AND daily.yyyy_mm = subdaily.yyyy_mm;
$_$;


ALTER FUNCTION public.monthly_obs(station_array character varying[], nfrom character varying, nto character varying) OWNER TO postgres;

--
-- Name: monthly_rain_quintile(character varying, character varying, numeric, character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION monthly_rain_quintile(station character varying, month character varying, inrain numeric, nfrom character varying, nto character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $_$
DECLARE res RECORD;
DECLARE prev_max NUMERIC(7,1);
DECLARE prev_quintile integer;

BEGIN
	FOR res IN
	
		select mm, quintile, min(rain) as min, max(rain) as max
		from (
		select mm, rain, ntile(5) over (partition by mm order by rain) as quintile
			from (
				select rain, substr(year_mm, 6,2) as mm
				from (
					select sum(rain_24h) as rain, to_char(lsd, 'yyyy-mm') as year_mm
					from obs_daily
					where lsd > to_timestamp($4, 'yyyy-mm') AND lsd <= to_timestamp($5, 'yyyy-mm')
					and station_no = $1		
					group by to_char(lsd, 'yyyy-mm')
				) z
			) x WHERE mm = $2
		) y
		group by mm, quintile
		order by mm, quintile

	LOOP	--Logic to extract appropriate quintile 

	--Lower than the minimum value in lowest quintile...return 0
	IF res.quintile = 1 AND $3 < res.min THEN
		RETURN 0;
	END IF;

	--res.min is rank minimum amt, res.max is rank maximum amt, res.quintile is rank
	IF $3 >= res.min AND $3 <= res.max THEN
		--Amount is definitely in this quintile
		RETURN res.quintile;
	ELSIF $3 < res.min THEN	
		--need to determine if part of this or previous quintile.
		--calculate half-way between maximum of prev and minimum of current
		IF $3 > (prev_max + (res.min-prev_max)/2) THEN
			RETURN res.quintile;
		ELSE
			RETURN prev_quintile;
		END IF;
	ELSE
		prev_max = res.max;
		prev_quintile = res.quintile;
	END IF;
	END LOOP;

	--No quintile has been selected! Value must be bigger than max in last group...return 6.
	RETURN 6;

END
$_$;


ALTER FUNCTION public.monthly_rain_quintile(station character varying, month character varying, inrain numeric, nfrom character varying, nto character varying) OWNER TO postgres;

--
-- Name: normal_rand(integer, double precision, double precision); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION normal_rand(integer, double precision, double precision) RETURNS SETOF double precision
    LANGUAGE c STRICT
    AS '$libdir/tablefunc', 'normal_rand';


ALTER FUNCTION public.normal_rand(integer, double precision, double precision) OWNER TO clideadmin;

--
-- Name: obs_monthly_summary(character varying, date, time without time zone); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION obs_monthly_summary(stat_no character varying, yyyy_mm date, subdaily_time time without time zone) RETURNS TABLE(station_no character varying, month text, tot_rain numeric, max_rain numeric, max_rain_date text, mn_max_air_temp numeric, mn_min_air_temp numeric, max_max_air_temp numeric, max_max_temp_date text, min_max_air_temp numeric, min_max_temp_date text, min_min_air_temp numeric, min_min_temp_date text, max_min_air_temp numeric, max_min_temp_date text, mean_temp text, max_ground_temp numeric, max_ground_date text, min_ground_temp numeric, min_ground_date text, mn_ground_temp numeric, x01_days_count bigint, x02_days_count bigint, x1_days_count bigint, x10_days_count bigint, x50_days_count bigint, temp_gt30_count bigint, temp_lt20_count bigint, non_rain_days_count bigint, min_msl_pressure numeric, min_mslp_date text, max_msl_pressure numeric, max_mslp_date text, avg_msl_pressure text, tot_evaporation numeric, avg_evaporation text, tot_sunshine numeric, avg_sunshine text, max_gust numeric, max_gust_date text, max_wind_run numeric, max_run_date text, mn_9am_wind_speed numeric)
    LANGUAGE sql ROWS 1
    AS $_$
SELECT a.station_no, a.mon AS month, max(a.tot_rain) AS tot_rain, max(a.max_rain) AS max_rain, min(a.max_rain_date) AS max_rain_date, max(a.mn_max_air_temp) as mn_max_air_temp, max(a.mn_min_air_temp) as mn_min_air_temp, max(a.max_max_air_temp) AS max_max_air_temp, min(a.max_max_temp_date) AS max_max_temp_date, min(a.min_max_air_temp) AS min_max_air_temp, min(a.min_max_temp_date) AS min_max_temp_date, min(a.min_min_air_temp) AS min_min_air_temp, min(a.min_min_temp_date) AS min_min_temp_date, max(a.max_min_air_temp) AS max_min_air_temp, min(a.max_min_temp_date) AS max_min_temp_date, min(a.mean_temp) AS mean_temp, max(a.max_ground_temp) AS max_ground_temp, min(a.max_ground_date) AS max_ground_date, min(a.min_ground_temp) AS min_ground_temp, min(a.min_ground_date) AS min_ground_date, max(a.mn_ground_temp) as mn_ground_temp, max(a.x01_rain_count) AS x01_days_count, max(a.x02_rain_count) AS x02_days_count, max(a.x1_rain_count) AS x1_days_count, max(a.x10_rain_count) AS x10_days_count, max(a.x50_rain_count) AS x50_days_count, max(a.temp_gt30_count) AS temp_gt30_count, max(a.temp_lt20_count) AS temp_lt20_count, max(a.non_rain_count) AS non_rain_days_count, max(a.min_msl_pres) AS min_msl_pressure, min(a.min_mslp_date) AS min_mslp_date, max(a.max_msl_pres) AS max_msl_pressure, min(a.max_mslp_date) AS max_mslp_date, max(a.avg_msl_pres) AS avg_msl_pressure, max(a.tot_evaporation) AS tot_evaporation, max(a.avg_evaporation) AS avg_evaporation, max(a.tot_sunshine) AS tot_sunshine, max(a.avg_sunshine) AS avg_sunshine, max(a.max_gust) AS max_gust, min(a.max_gust_date) AS max_gust_date, max(a.max_wind_run) AS max_wind_run, min(a.max_run_date) AS max_run_date, max(mn_9am_wind_speed) as mn_9am_wind_speed
   FROM ( SELECT dat.station_no, dat.mon, dat.tot_rain, dat.max_rain, maxraindate.max_rain_date, round(dat.mn_max_air_temp,1) as mn_max_air_temp, round(dat.mn_min_air_temp,1) as mn_min_air_temp, dat.max_max_air_temp, maxmaxtempdate.max_max_temp_date, dat.min_max_air_temp, minmaxtempdate.min_max_temp_date, dat.min_min_air_temp, minmintempdate.min_min_temp_date, dat.max_min_air_temp, maxmintempdate.max_min_temp_date, to_char(dat.mean_temp, '9999990.0'::text) AS mean_temp, dat.max_ground_temp, round(dat.mn_ground_temp,1) as mn_ground_temp, maxgrounddate.max_ground_date, dat.min_ground_temp, mingrounddate.min_ground_date, dat.x01_rain_count, dat.x02_rain_count, dat.x1_rain_count, dat.x10_rain_count, dat.x50_rain_count, dat.non_rain_count, dat.temp_gt30_count, dat.temp_lt20_count, subdaily.min_msl_pres, minmslpdate.min_mslp_date, subdaily.max_msl_pres, maxmslpdate.max_mslp_date, to_char(subdaily.avg_msl_pres, '9999990.0'::text) AS avg_msl_pres, dat.tot_evaporation, to_char(dat.avg_evaporation, '9999990.0'::text) AS avg_evaporation, dat.tot_sunshine, to_char(dat.avg_sunshine, '9999990.0'::text) AS avg_sunshine, dat.max_gust, maxgustdate.max_gust_date, dat.max_wind_run, maxrundate.max_run_date, round(subdaily_9am.mn_9am_wind_speed,1) as mn_9am_wind_speed
           FROM ( SELECT day.station_no, to_char(day.lsd, 'Mon yyyy'::text) AS mon, sum(day.rain_24h) AS tot_rain, max(day.rain_24h) AS max_rain, avg(day.max_air_temp) AS mn_max_air_temp, avg(day.min_air_temp) AS mn_min_air_temp, max(day.max_air_temp) AS max_max_air_temp, min(day.max_air_temp) AS min_max_air_temp, min(day.min_air_temp) AS min_min_air_temp, max(day.min_air_temp) AS max_min_air_temp, avg((day.max_air_temp + day.min_air_temp) / 2::numeric) AS mean_temp, min(day.ground_temp) AS min_ground_temp, max(day.ground_temp) AS max_ground_temp, avg(day.ground_temp) AS mn_ground_temp, sum(
                        CASE
                            WHEN day.rain_24h >= 0.1 THEN 1
                            ELSE 0
                        END) AS x01_rain_count, sum(
                        CASE
                            WHEN day.rain_24h >= 0.2 THEN 1
                            ELSE 0
                        END) AS x02_rain_count, sum(
                        CASE
                            WHEN day.rain_24h >= 1::numeric THEN 1
                            ELSE 0
                        END) AS x1_rain_count, sum(
                        CASE
                            WHEN day.rain_24h >= 10::numeric THEN 1
                            ELSE 0
                        END) AS x10_rain_count, sum(
                        CASE
                            WHEN day.rain_24h >= 50::numeric THEN 1
                            ELSE 0
                        END) AS x50_rain_count, sum(
                        CASE
                            WHEN day.rain_24h < 0.1 THEN 1
                            ELSE 0
                        END) AS non_rain_count, sum(
                        CASE
                            WHEN day.max_air_temp >= 30.0 THEN 1
                            ELSE 0
                        END) AS temp_gt30_count, sum(
                        CASE
                            WHEN day.min_air_temp <= 20.0 THEN 1
                            ELSE 0
                        END) AS temp_lt20_count, sum(day.evaporation) AS tot_evaporation, avg(day.evaporation) AS avg_evaporation, sum(day.sunshine_duration) AS tot_sunshine, avg(day.sunshine_duration) AS avg_sunshine, max(day.max_gust_speed) AS max_gust, max(day.wind_run_gt10) AS max_wind_run
                   FROM obs_daily day
                   WHERE upper(day.station_no) = $1
                     AND date_trunc('month', day.lsd) = $2
                  GROUP BY day.station_no, to_char(day.lsd, 'Mon yyyy'::text)) dat
      LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS max_max_temp_date, obs_daily.max_air_temp, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
                   FROM obs_daily
                   WHERE upper(station_no) = $1) maxmaxtempdate ON dat.station_no::text = maxmaxtempdate.station_no::text AND dat.mon = maxmaxtempdate.mon AND dat.max_max_air_temp = maxmaxtempdate.max_air_temp
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS min_max_temp_date, obs_daily.max_air_temp, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
              FROM obs_daily
              WHERE upper(station_no) = $1) minmaxtempdate ON dat.station_no::text = minmaxtempdate.station_no::text AND dat.mon = minmaxtempdate.mon AND dat.min_max_air_temp = minmaxtempdate.max_air_temp
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS min_min_temp_date, obs_daily.min_air_temp, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
         FROM obs_daily
         WHERE upper(station_no) = $1) minmintempdate ON dat.min_min_air_temp = minmintempdate.min_air_temp AND dat.mon = minmintempdate.mon AND dat.station_no::text = minmintempdate.station_no::text
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS max_min_temp_date, obs_daily.min_air_temp, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
    FROM obs_daily
    WHERE upper(station_no) = $1) maxmintempdate ON dat.max_min_air_temp = maxmintempdate.min_air_temp AND dat.mon = maxmintempdate.mon AND dat.station_no::text = maxmintempdate.station_no::text
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS max_rain_date, obs_daily.rain_24h, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
   FROM obs_daily
   WHERE upper(station_no) = $1) maxraindate ON dat.max_rain = maxraindate.rain_24h AND dat.mon = maxraindate.mon AND dat.station_no::text = maxraindate.station_no::text
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS min_ground_date, obs_daily.ground_temp, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
   FROM obs_daily) mingrounddate ON dat.min_ground_temp = mingrounddate.ground_temp AND dat.mon = mingrounddate.mon AND dat.station_no::text = mingrounddate.station_no::text
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS max_ground_date, obs_daily.ground_temp, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
   FROM obs_daily
   WHERE upper(station_no) = $1) maxgrounddate ON dat.max_ground_temp = maxgrounddate.ground_temp AND dat.mon = maxgrounddate.mon AND dat.station_no::text = maxgrounddate.station_no::text
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS max_gust_date, obs_daily.max_gust_speed, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
   FROM obs_daily
   WHERE upper(station_no) = $1) maxgustdate ON dat.max_gust = maxgustdate.max_gust_speed AND dat.mon = maxgustdate.mon AND dat.station_no::text = maxgustdate.station_no::text
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS max_run_date, obs_daily.wind_run_gt10, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
   FROM obs_daily
   WHERE upper(station_no) = $1) maxrundate ON dat.max_wind_run = maxrundate.wind_run_gt10 AND dat.mon = maxrundate.mon AND dat.station_no::text = maxrundate.station_no::text
   LEFT JOIN ( SELECT obs_subdaily.station_no, to_char(obs_subdaily.lsd, 'Mon yyyy'::text) AS mon, avg(obs_subdaily.wind_speed) AS mn_9am_wind_speed
   FROM obs_subdaily
   WHERE upper(station_no) = $1
     AND lct::time = $3
  GROUP BY obs_subdaily.station_no, to_char(obs_subdaily.lsd, 'Mon yyyy'::text)) subdaily_9am ON dat.mon = subdaily_9am.mon AND dat.station_no::text = subdaily_9am.station_no::text
   LEFT JOIN ( SELECT obs_subdaily.station_no, to_char(obs_subdaily.lsd, 'Mon yyyy'::text) AS mon, min(obs_subdaily.msl_pres) AS min_msl_pres, max(obs_subdaily.msl_pres) AS max_msl_pres, avg(obs_subdaily.msl_pres) AS avg_msl_pres
   FROM obs_subdaily
   WHERE upper(station_no) = $1
  GROUP BY obs_subdaily.station_no, to_char(obs_subdaily.lsd, 'Mon yyyy'::text)) subdaily ON dat.mon = subdaily.mon AND dat.station_no::text = subdaily.station_no::text
   LEFT JOIN ( SELECT obs_subdaily.station_no, obs_subdaily.lsd, to_char(obs_subdaily.lsd, 'Dy ddth'::text) AS max_mslp_date, obs_subdaily.msl_pres, to_char(obs_subdaily.lsd, 'Mon yyyy'::text) AS mon
   FROM obs_subdaily
   WHERE upper(station_no) = $1) maxmslpdate ON subdaily.max_msl_pres = maxmslpdate.msl_pres AND subdaily.mon = maxmslpdate.mon AND subdaily.station_no::text = maxmslpdate.station_no::text
   LEFT JOIN ( SELECT obs_subdaily.station_no, obs_subdaily.lsd, to_char(obs_subdaily.lsd, 'Dy ddth'::text) AS min_mslp_date, obs_subdaily.msl_pres, to_char(obs_subdaily.lsd, 'Mon yyyy'::text) AS mon
   FROM obs_subdaily
   WHERE upper(station_no) = $1) minmslpdate ON subdaily.min_msl_pres = minmslpdate.msl_pres AND subdaily.mon = minmslpdate.mon AND subdaily.station_no::text = minmslpdate.station_no::text) a
  GROUP BY a.station_no, a.mon;$_$;


ALTER FUNCTION public.obs_monthly_summary(stat_no character varying, yyyy_mm date, subdaily_time time without time zone) OWNER TO postgres;

--
-- Name: obs_monthly_summary_high(character varying, date, time without time zone); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION obs_monthly_summary_high(stat_no character varying, yyyy_mm date, subdaily_time time without time zone) RETURNS TABLE(station_no character varying, month text, tot_rain numeric, max_rain numeric, max_rain_date text, mn_max_air_temp numeric, mn_min_air_temp numeric, max_max_air_temp numeric, max_max_temp_date text, min_max_air_temp numeric, min_max_temp_date text, min_min_air_temp numeric, min_min_temp_date text, max_min_air_temp numeric, max_min_temp_date text, mean_temp text, max_ground_temp numeric, max_ground_date text, min_ground_temp numeric, min_ground_date text, mn_ground_temp numeric, x01_days_count bigint, x02_days_count bigint, x1_days_count bigint, x10_days_count bigint, x50_days_count bigint, temp_gt30_count bigint, temp_lt20_count bigint, non_rain_days_count bigint, min_msl_pressure numeric, min_mslp_date text, max_msl_pressure numeric, max_mslp_date text, avg_msl_pressure text, tot_evaporation numeric, avg_evaporation text, tot_sunshine numeric, avg_sunshine text, max_gust numeric, max_gust_date text, max_wind_run numeric, max_run_date text, mn_9am_wind_speed numeric)
    LANGUAGE sql ROWS 1
    AS $_$
SELECT a.station_no, a.mon AS month, max(a.tot_rain) AS tot_rain, max(a.max_rain) AS max_rain, min(a.max_rain_date) AS max_rain_date, max(a.mn_max_air_temp) as mn_max_air_temp, min(a.mn_min_air_temp) as mn_min_air_temp, max(a.max_max_air_temp) AS max_max_air_temp, min(a.max_max_temp_date) AS max_max_temp_date, min(a.min_max_air_temp) AS min_max_air_temp, min(a.min_max_temp_date) AS min_max_temp_date, min(a.min_min_air_temp) AS min_min_air_temp, min(a.min_min_temp_date) AS min_min_temp_date, max(a.max_min_air_temp) AS max_min_air_temp, min(a.max_min_temp_date) AS max_min_temp_date, min(a.mean_temp) AS mean_temp, max(a.max_ground_temp) AS max_ground_temp, min(a.max_ground_date) AS max_ground_date, min(a.min_ground_temp) AS min_ground_temp, min(a.min_ground_date) AS min_ground_date, max(a.mn_ground_temp) as mn_ground_temp, max(a.x01_rain_count) AS x01_days_count, max(a.x02_rain_count) AS x02_days_count, max(a.x1_rain_count) AS x1_days_count, max(a.x10_rain_count) AS x10_days_count, max(a.x50_rain_count) AS x50_days_count, max(a.temp_gt30_count) AS temp_gt30_count, max(a.temp_lt20_count) AS temp_lt20_count, max(a.non_rain_count) AS non_rain_days_count, max(a.min_msl_pres) AS min_msl_pressure, min(a.min_mslp_date) AS min_mslp_date, max(a.max_msl_pres) AS max_msl_pressure, min(a.max_mslp_date) AS max_mslp_date, max(a.avg_msl_pres) AS avg_msl_pressure, max(a.tot_evaporation) AS tot_evaporation, max(a.avg_evaporation) AS avg_evaporation, max(a.tot_sunshine) AS tot_sunshine, max(a.avg_sunshine) AS avg_sunshine, max(a.max_gust) AS max_gust, min(a.max_gust_date) AS max_gust_date, max(a.max_wind_run) AS max_wind_run, min(a.max_run_date) AS max_run_date, max(mn_9am_wind_speed) as mn_9am_wind_speed
   FROM ( SELECT dat.station_no, dat.mon, dat.tot_rain, dat.max_rain, maxraindate.max_rain_date, dat.max_max_air_temp, maxmaxtempdate.max_max_temp_date, round(dat.mn_max_air_temp,1) as mn_max_air_temp, round(dat.mn_min_air_temp,1) as mn_min_air_temp, dat.min_max_air_temp, minmaxtempdate.min_max_temp_date, dat.min_min_air_temp, minmintempdate.min_min_temp_date, dat.max_min_air_temp, maxmintempdate.max_min_temp_date, to_char(dat.mean_temp, '9999990.0'::text) AS mean_temp, dat.max_ground_temp, maxgrounddate.max_ground_date, dat.min_ground_temp, mingrounddate.min_ground_date, round(dat.mn_ground_temp,1) as mn_ground_temp, dat.x01_rain_count, dat.x02_rain_count, dat.x1_rain_count, dat.x10_rain_count, dat.x50_rain_count, dat.non_rain_count, dat.temp_gt30_count, dat.temp_lt20_count, subdaily.min_msl_pres, minmslpdate.min_mslp_date, subdaily.max_msl_pres, maxmslpdate.max_mslp_date, to_char(subdaily.avg_msl_pres, '9999990.0'::text) AS avg_msl_pres, dat.tot_evaporation, to_char(dat.avg_evaporation, '9999990.0'::text) AS avg_evaporation, dat.tot_sunshine, to_char(dat.avg_sunshine, '9999990.0'::text) AS avg_sunshine, dat.max_gust, maxgustdate.max_gust_date, dat.max_wind_run, maxrundate.max_run_date, round(subdaily_9am.mn_9am_wind_speed,1) as mn_9am_wind_speed
           FROM ( SELECT day.station_no, to_char(day.lsd, 'Mon yyyy'::text) AS mon, sum(day.rain_24h) AS tot_rain, max(day.rain_24h) AS max_rain, avg(day.max_air_temp) AS mn_max_air_temp, avg(day.min_air_temp) AS mn_min_air_temp, max(day.max_air_temp) AS max_max_air_temp, min(day.max_air_temp) AS min_max_air_temp, min(day.min_air_temp) AS min_min_air_temp, max(day.min_air_temp) AS max_min_air_temp, avg((day.max_air_temp + day.min_air_temp) / 2::numeric) AS mean_temp, min(day.ground_temp) AS min_ground_temp, max(day.ground_temp) AS max_ground_temp, avg(day.ground_temp) AS mn_ground_temp, sum(
                        CASE
                            WHEN day.rain_24h >= 0.1 THEN 1
                            ELSE 0
                        END) AS x01_rain_count, sum(
                        CASE
                            WHEN day.rain_24h >= 0.2 THEN 1
                            ELSE 0
                        END) AS x02_rain_count, sum(
                        CASE
                            WHEN day.rain_24h >= 1::numeric THEN 1
                            ELSE 0
                        END) AS x1_rain_count, sum(
                        CASE
                            WHEN day.rain_24h >= 10::numeric THEN 1
                            ELSE 0
                        END) AS x10_rain_count, sum(
                        CASE
                            WHEN day.rain_24h >= 50::numeric THEN 1
                            ELSE 0
                        END) AS x50_rain_count, sum(
                        CASE
                            WHEN day.rain_24h < 0.1 THEN 1
                            ELSE 0
                        END) AS non_rain_count, sum(
                        CASE
                            WHEN day.max_air_temp >= 30.0 THEN 1
                            ELSE 0
                        END) AS temp_gt30_count, sum(
                        CASE
                            WHEN day.min_air_temp <= 20.0 THEN 1
                            ELSE 0
                        END) AS temp_lt20_count, sum(day.evaporation) AS tot_evaporation, avg(day.evaporation) AS avg_evaporation, sum(day.sunshine_duration) AS tot_sunshine, avg(day.sunshine_duration) AS avg_sunshine, max(day.max_gust_speed) AS max_gust, max(day.wind_run_gt10) AS max_wind_run
                   FROM obs_daily day
                  WHERE upper(day.station_no) = $1
                    AND date_trunc('month', day.lsd) = $2
                    AND (day.rain_24h IS NULL OR (day.rain_24h_qa IN ( SELECT codes_simple.code
                           FROM codes_simple
                          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) AND (day.max_air_temp IS NULL OR (day.max_air_temp_qa IN ( SELECT codes_simple.code
                           FROM codes_simple
                          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) AND (day.min_air_temp IS NULL OR (day.min_air_temp_qa IN ( SELECT codes_simple.code
                           FROM codes_simple
                          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) AND (day.ground_temp IS NULL OR (day.ground_temp_qa IN ( SELECT codes_simple.code
                           FROM codes_simple
                          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) AND (day.evaporation IS NULL OR (day.evaporation_qa IN ( SELECT codes_simple.code
                           FROM codes_simple
                          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) AND (day.sunshine_duration IS NULL OR (day.sunshine_duration_qa IN ( SELECT codes_simple.code
                           FROM codes_simple
                          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) AND (day.max_gust_speed IS NULL OR (day.max_gust_speed_qa IN ( SELECT codes_simple.code
                           FROM codes_simple
                          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) AND (day.wind_run_gt10 IS NULL OR (day.wind_run_gt10_qa IN ( SELECT codes_simple.code
                           FROM codes_simple
                          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text)))
                  GROUP BY day.station_no, to_char(day.lsd, 'Mon yyyy'::text)) dat
      LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS max_max_temp_date, obs_daily.max_air_temp, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
                   FROM obs_daily
                  WHERE upper(station_no) = $1
                    AND (obs_daily.max_air_temp_qa IN ( SELECT codes_simple.code
                           FROM codes_simple
                          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) maxmaxtempdate ON dat.station_no::text = maxmaxtempdate.station_no::text AND dat.mon = maxmaxtempdate.mon AND dat.max_max_air_temp = maxmaxtempdate.max_air_temp
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS min_max_temp_date, obs_daily.max_air_temp, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
              FROM obs_daily
             WHERE upper(station_no) = $1
               AND (obs_daily.max_air_temp_qa IN ( SELECT codes_simple.code
                      FROM codes_simple
                     WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) minmaxtempdate ON dat.station_no::text = minmaxtempdate.station_no::text AND dat.mon = minmaxtempdate.mon AND dat.min_max_air_temp = minmaxtempdate.max_air_temp
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS min_min_temp_date, obs_daily.min_air_temp, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
         FROM obs_daily
        WHERE upper(station_no) = $1
          AND (obs_daily.min_air_temp_qa IN ( SELECT codes_simple.code
                 FROM codes_simple
                WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) minmintempdate ON dat.min_min_air_temp = minmintempdate.min_air_temp AND dat.mon = minmintempdate.mon AND dat.station_no::text = minmintempdate.station_no::text
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS max_min_temp_date, obs_daily.min_air_temp, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
    FROM obs_daily
   WHERE upper(station_no) = $1
     AND (obs_daily.min_air_temp_qa IN ( SELECT codes_simple.code
            FROM codes_simple
           WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) maxmintempdate ON dat.max_min_air_temp = maxmintempdate.min_air_temp AND dat.mon = maxmintempdate.mon AND dat.station_no::text = maxmintempdate.station_no::text
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS max_rain_date, obs_daily.rain_24h, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
   FROM obs_daily
  WHERE upper(station_no) = $1
    AND (obs_daily.rain_24h_qa IN ( SELECT codes_simple.code
           FROM codes_simple
          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) maxraindate ON dat.max_rain = maxraindate.rain_24h AND dat.mon = maxraindate.mon AND dat.station_no::text = maxraindate.station_no::text
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS min_ground_date, obs_daily.ground_temp, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
   FROM obs_daily
  WHERE upper(station_no) = $1
    AND (obs_daily.ground_temp_qa IN ( SELECT codes_simple.code
           FROM codes_simple
          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) mingrounddate ON dat.min_ground_temp = mingrounddate.ground_temp AND dat.mon = mingrounddate.mon AND dat.station_no::text = mingrounddate.station_no::text
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS max_ground_date, obs_daily.ground_temp, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
   FROM obs_daily
  WHERE upper(station_no) = $1
    AND (obs_daily.ground_temp_qa IN ( SELECT codes_simple.code
           FROM codes_simple
          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) maxgrounddate ON dat.max_ground_temp = maxgrounddate.ground_temp AND dat.mon = maxgrounddate.mon AND dat.station_no::text = maxgrounddate.station_no::text
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS max_gust_date, obs_daily.max_gust_speed, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
   FROM obs_daily
  WHERE upper(station_no) = $1
    AND (obs_daily.max_gust_speed_qa IN ( SELECT codes_simple.code
           FROM codes_simple
          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) maxgustdate ON dat.max_gust = maxgustdate.max_gust_speed AND dat.mon = maxgustdate.mon AND dat.station_no::text = maxgustdate.station_no::text
   LEFT JOIN ( SELECT obs_daily.station_no, obs_daily.lsd, to_char(obs_daily.lsd, 'Dy ddth'::text) AS max_run_date, obs_daily.wind_run_gt10, to_char(obs_daily.lsd, 'Mon yyyy'::text) AS mon
   FROM obs_daily
  WHERE upper(station_no) = $1
    AND (obs_daily.wind_run_gt10_qa IN ( SELECT codes_simple.code
           FROM codes_simple
          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) maxrundate ON dat.max_wind_run = maxrundate.wind_run_gt10 AND dat.mon = maxrundate.mon AND dat.station_no::text = maxrundate.station_no::text
   LEFT JOIN ( SELECT obs_subdaily.station_no, to_char(obs_subdaily.lsd, 'Mon yyyy'::text) AS mon, avg(obs_subdaily.wind_speed) AS mn_9am_wind_speed
   FROM obs_subdaily
   WHERE upper(station_no) = $1
     AND lct::time = $3
     AND (obs_subdaily.wind_speed_qa IN ( SELECT codes_simple.code
           FROM codes_simple
          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))
  GROUP BY obs_subdaily.station_no, to_char(obs_subdaily.lsd, 'Mon yyyy'::text)) subdaily_9am ON dat.mon = subdaily_9am.mon AND dat.station_no::text = subdaily_9am.station_no::text
   LEFT JOIN ( SELECT obs_subdaily.station_no, to_char(obs_subdaily.lsd, 'Mon yyyy'::text) AS mon, min(obs_subdaily.msl_pres) AS min_msl_pres, max(obs_subdaily.msl_pres) AS max_msl_pres, avg(obs_subdaily.msl_pres) AS avg_msl_pres
   FROM obs_subdaily
  WHERE upper(station_no) = $1
    AND (obs_subdaily.msl_pres_qa IN ( SELECT codes_simple.code
           FROM codes_simple
          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))
  GROUP BY obs_subdaily.station_no, to_char(obs_subdaily.lsd, 'Mon yyyy'::text)) subdaily ON dat.mon = subdaily.mon AND dat.station_no::text = subdaily.station_no::text
   LEFT JOIN ( SELECT obs_subdaily.station_no, obs_subdaily.lsd, to_char(obs_subdaily.lsd, 'Dy ddth'::text) AS max_mslp_date, obs_subdaily.msl_pres, to_char(obs_subdaily.lsd, 'Mon yyyy'::text) AS mon
   FROM obs_subdaily
  WHERE upper(station_no) = $1
    AND (obs_subdaily.msl_pres_qa IN ( SELECT codes_simple.code
           FROM codes_simple
          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) maxmslpdate ON subdaily.max_msl_pres = maxmslpdate.msl_pres AND subdaily.mon = maxmslpdate.mon AND subdaily.station_no::text = maxmslpdate.station_no::text
   LEFT JOIN ( SELECT obs_subdaily.station_no, obs_subdaily.lsd, to_char(obs_subdaily.lsd, 'Dy ddth'::text) AS min_mslp_date, obs_subdaily.msl_pres, to_char(obs_subdaily.lsd, 'Mon yyyy'::text) AS mon
   FROM obs_subdaily
  WHERE upper(station_no) = $1
    AND (obs_subdaily.msl_pres_qa IN ( SELECT codes_simple.code
           FROM codes_simple
          WHERE codes_simple.code_type::text = 'QUAL_HIGH'::text))) minmslpdate ON subdaily.min_msl_pres = minmslpdate.msl_pres AND subdaily.mon = minmslpdate.mon AND subdaily.station_no::text = minmslpdate.station_no::text) a
  GROUP BY a.station_no, a.mon;$_$;


ALTER FUNCTION public.obs_monthly_summary_high(stat_no character varying, yyyy_mm date, subdaily_time time without time zone) OWNER TO postgres;

--
-- Name: sec_to_gc(double precision); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION sec_to_gc(double precision) RETURNS double precision
    LANGUAGE sql IMMUTABLE STRICT
    AS $_$SELECT CASE WHEN $1 < 0 THEN 0::float8 WHEN $1/(2*earth()) > 1 THEN pi()*earth() ELSE 2*earth()*asin($1/(2*earth())) END$_$;


ALTER FUNCTION public.sec_to_gc(double precision) OWNER TO clideadmin;

--
-- Name: stations_id_wmo_dates_trg(); Type: FUNCTION; Schema: public; Owner: clideadmin
--

CREATE FUNCTION stations_id_wmo_dates_trg() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  DECLARE
    myrec RECORD;
  BEGIN
    IF TG_OP = 'INSERT' THEN
      SELECT * INTO myrec
        FROM stations
        WHERE id_wmo = NEW.id_wmo
          AND (start_date < NEW.end_date or NEW.end_date is null)
          AND (end_date > NEW.start_date or end_date is null);
      IF FOUND THEN
        RAISE EXCEPTION 'INSERT failed: overlapping dates with same id_wmo % for station_no % with dates (%,%)',
            myrec.id_wmo, myrec.station_no, myrec.start_date, myrec.end_date;
      END IF;
    END IF;
    IF TG_OP = 'UPDATE' THEN
      SELECT * INTO myrec
        FROM stations
        WHERE id_wmo = NEW.id_wmo
          AND (start_date < NEW.end_date or NEW.end_date is null)
          AND (end_date > NEW.start_date or end_date is null)
          AND id <> OLD.id;
      IF FOUND THEN
        RAISE EXCEPTION 'INSERT failed: overlapping dates with same id_wmo % for station_no % with dates (%,%)',
            myrec.id_wmo, myrec.station_no, myrec.start_date, myrec.end_date;
      END IF;
    END IF;

    RETURN NEW;
  END;
$$;


ALTER FUNCTION public.stations_id_wmo_dates_trg() OWNER TO clideadmin;

--
-- Name: utc_to_lct(character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION utc_to_lct(station character varying, utc character varying) RETURNS character varying
    LANGUAGE sql STABLE
    AS $_$
SELECT
  TO_CHAR($2::timestamp without time zone + CAST(CASE WHEN tm_diff IS NULL THEN utc_diff ELSE tm_diff END||' hours' AS INTERVAL), 'yyyy-mm-dd HH24:mi') as return_lct
FROM stations AS s
     INNER JOIN station_timezones AS st ON st.tm_zone = s.time_zone
     LEFT JOIN timezone_diffs AS td ON td.tm_zone = s.time_zone
                                   AND start_timestamp <= $2::date
                                   AND end_timestamp >= $2::date
 WHERE station_no = $1;
$_$;


ALTER FUNCTION public.utc_to_lct(station character varying, utc character varying) OWNER TO postgres;

--
-- Name: utc_to_lsd(character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION utc_to_lsd(station character varying, utc character varying) RETURNS character varying
    LANGUAGE sql STABLE
    AS $_$
SELECT
  TO_CHAR($2::timestamp without time zone + CAST(utc_diff||' hours' AS INTERVAL), 'yyyy-mm-dd HH24:mi') as return_lsd
FROM stations AS s
     INNER JOIN station_timezones AS st ON st.tm_zone = s.time_zone
WHERE station_no = $1;
$_$;


ALTER FUNCTION public.utc_to_lsd(station character varying, utc character varying) OWNER TO postgres;

--
-- Name: &&; Type: OPERATOR; Schema: public; Owner: clideadmin
--

CREATE OPERATOR && (
    PROCEDURE = cube_overlap,
    LEFTARG = cube,
    RIGHTARG = cube,
    COMMUTATOR = &&,
    RESTRICT = areasel,
    JOIN = areajoinsel
);


ALTER OPERATOR public.&& (cube, cube) OWNER TO clideadmin;

--
-- Name: <; Type: OPERATOR; Schema: public; Owner: clideadmin
--

CREATE OPERATOR < (
    PROCEDURE = cube_lt,
    LEFTARG = cube,
    RIGHTARG = cube,
    COMMUTATOR = >,
    NEGATOR = >=,
    RESTRICT = scalarltsel,
    JOIN = scalarltjoinsel
);


ALTER OPERATOR public.< (cube, cube) OWNER TO clideadmin;

--
-- Name: <=; Type: OPERATOR; Schema: public; Owner: clideadmin
--

CREATE OPERATOR <= (
    PROCEDURE = cube_le,
    LEFTARG = cube,
    RIGHTARG = cube,
    COMMUTATOR = >=,
    NEGATOR = >,
    RESTRICT = scalarltsel,
    JOIN = scalarltjoinsel
);


ALTER OPERATOR public.<= (cube, cube) OWNER TO clideadmin;

--
-- Name: <>; Type: OPERATOR; Schema: public; Owner: clideadmin
--

CREATE OPERATOR <> (
    PROCEDURE = cube_ne,
    LEFTARG = cube,
    RIGHTARG = cube,
    COMMUTATOR = <>,
    NEGATOR = =,
    RESTRICT = neqsel,
    JOIN = neqjoinsel
);


ALTER OPERATOR public.<> (cube, cube) OWNER TO clideadmin;

--
-- Name: <@; Type: OPERATOR; Schema: public; Owner: clideadmin
--

CREATE OPERATOR <@ (
    PROCEDURE = cube_contained,
    LEFTARG = cube,
    RIGHTARG = cube,
    COMMUTATOR = @>,
    RESTRICT = contsel,
    JOIN = contjoinsel
);


ALTER OPERATOR public.<@ (cube, cube) OWNER TO clideadmin;

--
-- Name: <@>; Type: OPERATOR; Schema: public; Owner: clideadmin
--

CREATE OPERATOR <@> (
    PROCEDURE = geo_distance,
    LEFTARG = point,
    RIGHTARG = point,
    COMMUTATOR = <@>
);


ALTER OPERATOR public.<@> (point, point) OWNER TO clideadmin;

--
-- Name: =; Type: OPERATOR; Schema: public; Owner: clideadmin
--

CREATE OPERATOR = (
    PROCEDURE = cube_eq,
    LEFTARG = cube,
    RIGHTARG = cube,
    COMMUTATOR = =,
    NEGATOR = <>,
    MERGES,
    RESTRICT = eqsel,
    JOIN = eqjoinsel
);


ALTER OPERATOR public.= (cube, cube) OWNER TO clideadmin;

--
-- Name: >; Type: OPERATOR; Schema: public; Owner: clideadmin
--

CREATE OPERATOR > (
    PROCEDURE = cube_gt,
    LEFTARG = cube,
    RIGHTARG = cube,
    COMMUTATOR = <,
    NEGATOR = <=,
    RESTRICT = scalargtsel,
    JOIN = scalargtjoinsel
);


ALTER OPERATOR public.> (cube, cube) OWNER TO clideadmin;

--
-- Name: >=; Type: OPERATOR; Schema: public; Owner: clideadmin
--

CREATE OPERATOR >= (
    PROCEDURE = cube_ge,
    LEFTARG = cube,
    RIGHTARG = cube,
    COMMUTATOR = <=,
    NEGATOR = <,
    RESTRICT = scalargtsel,
    JOIN = scalargtjoinsel
);


ALTER OPERATOR public.>= (cube, cube) OWNER TO clideadmin;

--
-- Name: @; Type: OPERATOR; Schema: public; Owner: clideadmin
--

CREATE OPERATOR @ (
    PROCEDURE = cube_contains,
    LEFTARG = cube,
    RIGHTARG = cube,
    COMMUTATOR = ~,
    RESTRICT = contsel,
    JOIN = contjoinsel
);


ALTER OPERATOR public.@ (cube, cube) OWNER TO clideadmin;

--
-- Name: @>; Type: OPERATOR; Schema: public; Owner: clideadmin
--

CREATE OPERATOR @> (
    PROCEDURE = cube_contains,
    LEFTARG = cube,
    RIGHTARG = cube,
    COMMUTATOR = <@,
    RESTRICT = contsel,
    JOIN = contjoinsel
);


ALTER OPERATOR public.@> (cube, cube) OWNER TO clideadmin;

--
-- Name: ~; Type: OPERATOR; Schema: public; Owner: clideadmin
--

CREATE OPERATOR ~ (
    PROCEDURE = cube_contained,
    LEFTARG = cube,
    RIGHTARG = cube,
    COMMUTATOR = @,
    RESTRICT = contsel,
    JOIN = contjoinsel
);


ALTER OPERATOR public.~ (cube, cube) OWNER TO clideadmin;

--
-- Name: cube_ops; Type: OPERATOR CLASS; Schema: public; Owner: clideadmin
--

CREATE OPERATOR CLASS cube_ops
    DEFAULT FOR TYPE cube USING btree AS
    OPERATOR 1 <(cube,cube) ,
    OPERATOR 2 <=(cube,cube) ,
    OPERATOR 3 =(cube,cube) ,
    OPERATOR 4 >=(cube,cube) ,
    OPERATOR 5 >(cube,cube) ,
    FUNCTION 1 cube_cmp(cube,cube);


ALTER OPERATOR CLASS public.cube_ops USING btree OWNER TO clideadmin;

--
-- Name: gist_cube_ops; Type: OPERATOR CLASS; Schema: public; Owner: clideadmin
--

CREATE OPERATOR CLASS gist_cube_ops
    DEFAULT FOR TYPE cube USING gist AS
    OPERATOR 3 &&(cube,cube) ,
    OPERATOR 6 =(cube,cube) ,
    OPERATOR 7 @>(cube,cube) ,
    OPERATOR 8 <@(cube,cube) ,
    OPERATOR 13 @(cube,cube) ,
    OPERATOR 14 ~(cube,cube) ,
    FUNCTION 1 g_cube_consistent(internal,cube,integer,oid,internal) ,
    FUNCTION 2 g_cube_union(internal,internal) ,
    FUNCTION 3 g_cube_compress(internal) ,
    FUNCTION 4 g_cube_decompress(internal) ,
    FUNCTION 5 g_cube_penalty(internal,internal,internal) ,
    FUNCTION 6 g_cube_picksplit(internal,internal) ,
    FUNCTION 7 g_cube_same(cube,cube,internal);


ALTER OPERATOR CLASS public.gist_cube_ops USING gist OWNER TO clideadmin;

--
-- Name: cdms_get_ext_views; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW cdms_get_ext_views AS
    SELECT tables.table_name FROM information_schema.tables WHERE ((((tables.table_type)::text = 'VIEW'::text) AND ((tables.table_schema)::text <> ALL (ARRAY['pg_catalog'::text, 'information_schema'::text]))) AND ((tables.table_name)::text ~~ 'ext_%'::text));


ALTER TABLE public.cdms_get_ext_views OWNER TO clidegui;

--
-- Name: codes_simple_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE codes_simple_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.codes_simple_id OWNER TO clidegui;

--
-- Name: SEQUENCE codes_simple_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE codes_simple_id IS 'PK sequence for codes_simple';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: codes_simple; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE codes_simple (
    id integer DEFAULT nextval('codes_simple_id'::regclass) NOT NULL,
    code_type character varying(40) NOT NULL,
    code character varying(40) NOT NULL,
    description character varying(400),
    change_user character varying(10),
    change_datetime timestamp without time zone,
    insert_datetime timestamp without time zone NOT NULL
);


ALTER TABLE public.codes_simple OWNER TO clidegui;

--
-- Name: TABLE codes_simple; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE codes_simple IS 'List of codes used in CliDE';


--
-- Name: COLUMN codes_simple.code_type; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN codes_simple.code_type IS 'Character code type';


--
-- Name: COLUMN codes_simple.description; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN codes_simple.description IS 'Description of code';


--
-- Name: COLUMN codes_simple.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN codes_simple.change_user IS 'User of last change';


--
-- Name: COLUMN codes_simple.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN codes_simple.change_datetime IS 'Timestamp of last change';


--
-- Name: COLUMN codes_simple.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN codes_simple.insert_datetime IS 'Timestamp of insert';


--
-- Name: datums; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE datums (
    datum_name character varying(20) NOT NULL,
    description character varying(100)
);


ALTER TABLE public.datums OWNER TO clidegui;

--
-- Name: TABLE datums; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE datums IS 'Geodetic datums';


--
-- Name: equipment_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE equipment_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.equipment_id OWNER TO clidegui;

--
-- Name: SEQUENCE equipment_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE equipment_id IS 'PK sequence for equipment';


--
-- Name: equipment; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE equipment (
    id integer DEFAULT nextval('equipment_id'::regclass) NOT NULL,
    type character varying(50),
    comments character varying(1000),
    version character varying(50)
);


ALTER TABLE public.equipment OWNER TO clidegui;

--
-- Name: TABLE equipment; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE equipment IS 'Stores equipment master information.';


--
-- Name: COLUMN equipment.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN equipment.id IS 'Surrogate Key';


--
-- Name: COLUMN equipment.type; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN equipment.type IS 'Type of equipment';


--
-- Name: COLUMN equipment.comments; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN equipment.comments IS 'Comments for equipment';


--
-- Name: COLUMN equipment.version; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN equipment.version IS 'Version of equipment';


--
-- Name: station_types_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE station_types_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.station_types_id OWNER TO clidegui;

--
-- Name: SEQUENCE station_types_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE station_types_id IS 'PK sequence for station status';


--
-- Name: station_types; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE station_types (
    id integer DEFAULT nextval('station_types_id'::regclass) NOT NULL,
    station_type character varying(10) NOT NULL,
    description character varying(50)
);


ALTER TABLE public.station_types OWNER TO clidegui;

--
-- Name: TABLE station_types; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE station_types IS 'Stores allowed values for stations.type_id';


--
-- Name: COLUMN station_types.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_types.id IS 'Surrogate Key';


--
-- Name: COLUMN station_types.station_type; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_types.station_type IS 'Station type code';


--
-- Name: COLUMN station_types.description; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_types.description IS 'Station type description';


--
-- Name: ext_class; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_class AS
    SELECT station_types.id, station_types.station_type AS class, station_types.description FROM station_types;


ALTER TABLE public.ext_class OWNER TO clidegui;

--
-- Name: ext_equipment; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_equipment AS
    SELECT equipment.id, equipment.type, equipment.comments, equipment.version FROM equipment;


ALTER TABLE public.ext_equipment OWNER TO clidegui;

--
-- Name: obs_aero_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obs_aero_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obs_aero_id OWNER TO clidegui;

--
-- Name: SEQUENCE obs_aero_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obs_aero_id IS 'PK sequence for obs_aero';


--
-- Name: obs_aero; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obs_aero (
    id integer DEFAULT nextval('obs_aero_id'::regclass) NOT NULL,
    station_no character varying(15) NOT NULL,
    lsd timestamp without time zone NOT NULL,
    gmt timestamp without time zone,
    lct timestamp without time zone,
    data_source character(2) NOT NULL,
    insert_datetime timestamp without time zone NOT NULL,
    change_datetime timestamp without time zone,
    change_user character varying(20),
    qa_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    comments character varying(1000),
    message_type character(1),
    wind_dir numeric(4,0),
    wind_dir_qa character(2),
    wind_speed numeric(4,1),
    wind_speed_qa character(2),
    max_gust_10m numeric(4,1),
    max_gust_10m_qa character(2),
    cavok_or_skc character(1),
    visibility numeric(7,3),
    visibility_qa character(2),
    pres_wea_intensity_1 numeric(1,0),
    pres_wea_desc_1 character(2),
    pres_wea_phen_1 character varying(6),
    pres_wea_1_qa character(2),
    pres_wea_intensity_2 numeric(1,0),
    pres_wea_desc_2 character(2),
    pres_wea_phen_2 character varying(6),
    pres_wea_2_qa character(2),
    pres_wea_intensity_3 numeric(1,0),
    pres_wea_desc_3 character(2),
    pres_wea_phen_3 character varying(6),
    pres_wea_3_qa character(2),
    cloud_amt_oktas_1 numeric(2,0),
    cloud_amt_code_1 character(3),
    cloud_amt_1_qa character(2),
    cloud_type_1 character varying(2),
    cloud_type_1_qa character(2),
    cloud_height_code_1 character(3),
    cloud_height_1_qa character(2),
    cloud_amt_oktas_2 numeric(2,0),
    cloud_amt_code_2 character(3),
    cloud_amt_2_qa character(2),
    cloud_type_2 character varying(2),
    cloud_type_2_qa character(2),
    cloud_height_code_2 character(3),
    cloud_height_2_qa character(2),
    cloud_amt_oktas_3 numeric(2,0),
    cloud_amt_code_3 character(3),
    cloud_amt_3_qa character(2),
    cloud_type_3 character varying(2),
    cloud_type_3_qa character(2),
    cloud_height_code_3 character(3),
    cloud_height_3_qa character(2),
    cloud_amt_oktas_4 numeric(2,0),
    cloud_amt_code_4 character(3),
    cloud_amt_4_qa character(2),
    cloud_type_4 character varying(2),
    cloud_type_4_qa character(2),
    cloud_height_code_4 character(3),
    cloud_height_4_qa character(2),
    cloud_amt_oktas_5 numeric(2,0),
    cloud_amt_code_5 character(3),
    cloud_amt_5_qa character(2),
    cloud_type_5 character varying(2),
    cloud_type_5_qa character(2),
    cloud_height_code_5 character(3),
    cloud_height_5_qa character(2),
    cloud_amt_oktas_6 numeric(2,0),
    cloud_amt_code_6 character(3),
    cloud_amt_6_qa character(2),
    cloud_type_6 character varying(2),
    cloud_type_6_qa character(2),
    cloud_height_code_6 character(3),
    cloud_height_6_qa character(2),
    ceiling_clear_flag numeric(1,0),
    ceiling_clear_flag_qa character(2),
    air_temp numeric(4,1),
    air_temp_f numeric(4,1),
    air_temp_qa character(2),
    dew_point numeric(4,1),
    dew_point_f numeric(4,1),
    dew_point_qa character(2),
    qnh numeric(7,1),
    qnh_inches numeric(8,3),
    qnh_qa character(2),
    rec_wea_desc_1 character(2),
    rec_wea_phen_1 character varying(6),
    rec_wea_1_qa character(2),
    rec_wea_desc_2 character(2),
    rec_wea_phen_2 character varying(6),
    rec_wea_2_qa character(2),
    rec_wea_desc_3 character(2),
    rec_wea_phen_3 character varying(6),
    rec_wea_3_qa character(2),
    text_msg character varying(1024),
    error_flag numeric(1,0),
    remarks character varying(400),
    remarks_qa character(2),
    wind_speed_knots numeric(5,1),
    max_gust_10m_knots numeric(5,1),
    visibility_miles numeric(7,3)
);


ALTER TABLE public.obs_aero OWNER TO clidegui;

--
-- Name: TABLE obs_aero; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obs_aero IS 'METAR / SPECI Aero message observations';


--
-- Name: COLUMN obs_aero.station_no; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.station_no IS 'Local Station identifier';


--
-- Name: COLUMN obs_aero.lsd; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.lsd IS 'Local System Time (No Daylight Savings)';


--
-- Name: COLUMN obs_aero.gmt; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.gmt IS 'GMT (UTC+0)';


--
-- Name: COLUMN obs_aero.lct; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.lct IS 'Local Clock Time (With Daylight Savings)';


--
-- Name: COLUMN obs_aero.data_source; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.data_source IS 'Code for data source (Ref Table??)';


--
-- Name: COLUMN obs_aero.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.insert_datetime IS 'Date/time row is inserted';


--
-- Name: COLUMN obs_aero.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.change_datetime IS 'Date/time row is changed';


--
-- Name: COLUMN obs_aero.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.change_user IS 'User who added/changed row';


--
-- Name: COLUMN obs_aero.qa_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.qa_flag IS 'QA flag for row (Y/N)';


--
-- Name: COLUMN obs_aero.comments; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.comments IS 'User comments';


--
-- Name: COLUMN obs_aero.message_type; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.message_type IS 'M=METAR, S=SPECI';


--
-- Name: COLUMN obs_aero.wind_dir; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.wind_dir IS 'Degrees (0-360)';


--
-- Name: COLUMN obs_aero.wind_speed; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.wind_speed IS 'Wind Speed (M/s to 0.1)';


--
-- Name: COLUMN obs_aero.max_gust_10m; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.max_gust_10m IS 'Max Wind Speed (M/s to 0.1)';


--
-- Name: COLUMN obs_aero.cavok_or_skc; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cavok_or_skc IS 'C=CAVOK, S=SKC';


--
-- Name: COLUMN obs_aero.visibility; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.visibility IS 'Km to (0.001)';


--
-- Name: COLUMN obs_aero.pres_wea_intensity_1; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.pres_wea_intensity_1 IS '0=Light, 1=Moderate, 2=Heavy,3=In Vicinity';


--
-- Name: COLUMN obs_aero.pres_wea_desc_1; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.pres_wea_desc_1 IS 'MI,BC,PR,DR,BL,SH,TS,FZ';


--
-- Name: COLUMN obs_aero.pres_wea_phen_1; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.pres_wea_phen_1 IS 'DZ,RA,SN,SG,IC,PL,GR,GS, BR, FG, FU, VA, DU, SA, HZ, PO, SQ, FC, SS, DS (WMO 4678)';


--
-- Name: COLUMN obs_aero.pres_wea_intensity_2; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.pres_wea_intensity_2 IS '0=Light, 1=Moderate, 2=Heavy,3=In Vicinity';


--
-- Name: COLUMN obs_aero.pres_wea_desc_2; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.pres_wea_desc_2 IS 'MI,BC,PR,DR,BL,SH,TS,FZ';


--
-- Name: COLUMN obs_aero.pres_wea_phen_2; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.pres_wea_phen_2 IS 'DZ,RA,SN,SG,IC,PL,GR,GS, BR, FG, FU, VA, DU, SA, HZ, PO, SQ, FC, SS, DS (WMO 4678)';


--
-- Name: COLUMN obs_aero.pres_wea_intensity_3; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.pres_wea_intensity_3 IS '0=Light, 1=Moderate, 2=Heavy,3=In Vicinity';


--
-- Name: COLUMN obs_aero.pres_wea_desc_3; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.pres_wea_desc_3 IS 'MI,BC,PR,DR,BL,SH,TS,FZ';


--
-- Name: COLUMN obs_aero.pres_wea_phen_3; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.pres_wea_phen_3 IS 'DZ,RA,SN,SG,IC,PL,GR,GS, BR, FG, FU, VA, DU, SA, HZ, PO, SQ, FC, SS, DS (WMO 4678)';


--
-- Name: COLUMN obs_aero.cloud_amt_oktas_1; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_amt_oktas_1 IS 'Oktas (0-9)';


--
-- Name: COLUMN obs_aero.cloud_amt_code_1; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_amt_code_1 IS 'FEW, SCD, BKN,OVC';


--
-- Name: COLUMN obs_aero.cloud_type_1; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_type_1 IS 'ST, SC, CU, etc';


--
-- Name: COLUMN obs_aero.cloud_height_code_1; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_height_code_1 IS 'Code (WMO Code 1690)';


--
-- Name: COLUMN obs_aero.cloud_amt_oktas_2; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_amt_oktas_2 IS 'Oktas (0-9)';


--
-- Name: COLUMN obs_aero.cloud_amt_code_2; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_amt_code_2 IS 'FEW, SCD, BKN,OVC';


--
-- Name: COLUMN obs_aero.cloud_type_2; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_type_2 IS 'ST, SC, CU, etc';


--
-- Name: COLUMN obs_aero.cloud_height_code_2; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_height_code_2 IS 'Code (WMO Code 1690)';


--
-- Name: COLUMN obs_aero.cloud_amt_oktas_3; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_amt_oktas_3 IS 'Oktas (0-9)';


--
-- Name: COLUMN obs_aero.cloud_amt_code_3; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_amt_code_3 IS 'FEW, SCD, BKN,OVC';


--
-- Name: COLUMN obs_aero.cloud_type_3; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_type_3 IS 'ST, SC, CU, etc';


--
-- Name: COLUMN obs_aero.cloud_height_code_3; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_height_code_3 IS 'Code (WMO Code 1690)';


--
-- Name: COLUMN obs_aero.cloud_amt_oktas_4; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_amt_oktas_4 IS 'Oktas (0-9)';


--
-- Name: COLUMN obs_aero.cloud_amt_code_4; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_amt_code_4 IS 'FEW, SCD, BKN,OVC';


--
-- Name: COLUMN obs_aero.cloud_type_4; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_type_4 IS 'ST, SC, CU, etc';


--
-- Name: COLUMN obs_aero.cloud_height_code_4; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_height_code_4 IS 'Code (WMO Code 1690)';


--
-- Name: COLUMN obs_aero.cloud_amt_oktas_5; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_amt_oktas_5 IS 'Oktas (0-9)';


--
-- Name: COLUMN obs_aero.cloud_amt_code_5; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_amt_code_5 IS 'FEW, SCD, BKN,OVC';


--
-- Name: COLUMN obs_aero.cloud_type_5; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_type_5 IS 'ST, SC, CU, etc';


--
-- Name: COLUMN obs_aero.cloud_height_code_5; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_height_code_5 IS 'Code (WMO Code 1690)';


--
-- Name: COLUMN obs_aero.cloud_amt_oktas_6; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_amt_oktas_6 IS 'Oktas (0-9)';


--
-- Name: COLUMN obs_aero.cloud_amt_code_6; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_amt_code_6 IS 'FEW, SCD, BKN,OVC';


--
-- Name: COLUMN obs_aero.cloud_type_6; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_type_6 IS '0-9';


--
-- Name: COLUMN obs_aero.cloud_height_code_6; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.cloud_height_code_6 IS 'Code (WMO Code 1690)';


--
-- Name: COLUMN obs_aero.ceiling_clear_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.ceiling_clear_flag IS 'Code (0,1=CLR BLW 125)';


--
-- Name: COLUMN obs_aero.air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.air_temp IS 'C to 0.1';


--
-- Name: COLUMN obs_aero.air_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.air_temp_f IS 'F to 0.1';


--
-- Name: COLUMN obs_aero.dew_point; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.dew_point IS 'C to 0.1';


--
-- Name: COLUMN obs_aero.dew_point_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.dew_point_f IS 'F to 0.1';


--
-- Name: COLUMN obs_aero.qnh; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.qnh IS 'hPa to 0.1';


--
-- Name: COLUMN obs_aero.qnh_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.qnh_inches IS 'Inches to 0.001';


--
-- Name: COLUMN obs_aero.rec_wea_desc_1; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.rec_wea_desc_1 IS 'MI,BC,PR,BL,SH,TS,FZ';


--
-- Name: COLUMN obs_aero.rec_wea_phen_1; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.rec_wea_phen_1 IS 'REFZRA, REFZDZ, RERA, RESN, REGR, REBLSN,REDS, RESS, RETS, REUP';


--
-- Name: COLUMN obs_aero.rec_wea_desc_2; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.rec_wea_desc_2 IS 'MI,BC,PR,BL,SH,TS,FZ';


--
-- Name: COLUMN obs_aero.rec_wea_phen_2; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.rec_wea_phen_2 IS 'REFZRA, REFZDZ, RERA, RESN, REGR, REBLSN,REDS, RESS, RETS, REUP';


--
-- Name: COLUMN obs_aero.rec_wea_desc_3; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.rec_wea_desc_3 IS 'MI,BC,PR,BL,SH,TS,FZ';


--
-- Name: COLUMN obs_aero.rec_wea_phen_3; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.rec_wea_phen_3 IS 'REFZRA, REFZDZ, RERA, RESN, REGR, REBLSN,REDS, RESS, RETS, REUP';


--
-- Name: COLUMN obs_aero.text_msg; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.text_msg IS 'METAR/SPECI msg';


--
-- Name: COLUMN obs_aero.error_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.error_flag IS 'Code (1=Yes, 0=No)';


--
-- Name: COLUMN obs_aero.remarks; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.remarks IS 'Additional Remarks supplied by observer. (Mainly paper docs)';


--
-- Name: COLUMN obs_aero.wind_speed_knots; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.wind_speed_knots IS 'Wind Speed in Knots';


--
-- Name: COLUMN obs_aero.max_gust_10m_knots; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aero.max_gust_10m_knots IS 'Max Gust >10M Knots';


--
-- Name: ext_obs_aero; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_obs_aero AS
    SELECT obs_aero.id, obs_aero.station_no, obs_aero.lsd, obs_aero.gmt, obs_aero.lct, obs_aero.data_source, obs_aero.insert_datetime, obs_aero.change_datetime, obs_aero.change_user, obs_aero.qa_flag, obs_aero.comments, obs_aero.message_type, obs_aero.wind_dir, obs_aero.wind_dir_qa, obs_aero.wind_speed, obs_aero.wind_speed_qa, obs_aero.max_gust_10m, obs_aero.max_gust_10m_qa, obs_aero.cavok_or_skc, obs_aero.visibility, obs_aero.visibility_qa, obs_aero.pres_wea_intensity_1, obs_aero.pres_wea_desc_1, obs_aero.pres_wea_phen_1, obs_aero.pres_wea_1_qa, obs_aero.pres_wea_intensity_2, obs_aero.pres_wea_desc_2, obs_aero.pres_wea_phen_2, obs_aero.pres_wea_2_qa, obs_aero.pres_wea_intensity_3, obs_aero.pres_wea_desc_3, obs_aero.pres_wea_phen_3, obs_aero.pres_wea_3_qa, obs_aero.cloud_amt_oktas_1, obs_aero.cloud_amt_code_1, obs_aero.cloud_amt_1_qa, obs_aero.cloud_type_1, obs_aero.cloud_type_1_qa, obs_aero.cloud_height_code_1, obs_aero.cloud_height_1_qa, obs_aero.cloud_amt_oktas_2, obs_aero.cloud_amt_code_2, obs_aero.cloud_amt_2_qa, obs_aero.cloud_type_2, obs_aero.cloud_type_2_qa, obs_aero.cloud_height_code_2, obs_aero.cloud_height_2_qa, obs_aero.cloud_amt_oktas_3, obs_aero.cloud_amt_code_3, obs_aero.cloud_amt_3_qa, obs_aero.cloud_type_3, obs_aero.cloud_type_3_qa, obs_aero.cloud_height_code_3, obs_aero.cloud_height_3_qa, obs_aero.cloud_amt_oktas_4, obs_aero.cloud_amt_code_4, obs_aero.cloud_amt_4_qa, obs_aero.cloud_type_4, obs_aero.cloud_type_4_qa, obs_aero.cloud_height_code_4, obs_aero.cloud_height_4_qa, obs_aero.cloud_amt_oktas_5, obs_aero.cloud_amt_code_5, obs_aero.cloud_amt_5_qa, obs_aero.cloud_type_5, obs_aero.cloud_type_5_qa, obs_aero.cloud_height_code_5, obs_aero.cloud_height_5_qa, obs_aero.cloud_amt_oktas_6, obs_aero.cloud_amt_code_6, obs_aero.cloud_amt_6_qa, obs_aero.cloud_type_6, obs_aero.cloud_type_6_qa, obs_aero.cloud_height_code_6, obs_aero.cloud_height_6_qa, obs_aero.ceiling_clear_flag, obs_aero.ceiling_clear_flag_qa, obs_aero.air_temp, obs_aero.air_temp_f, obs_aero.air_temp_qa, obs_aero.dew_point, obs_aero.dew_point_f, obs_aero.dew_point_qa, obs_aero.qnh, obs_aero.qnh_inches, obs_aero.qnh_qa, obs_aero.rec_wea_desc_1, obs_aero.rec_wea_phen_1, obs_aero.rec_wea_1_qa, obs_aero.rec_wea_desc_2, obs_aero.rec_wea_phen_2, obs_aero.rec_wea_2_qa, obs_aero.rec_wea_desc_3, obs_aero.rec_wea_phen_3, obs_aero.rec_wea_3_qa, obs_aero.text_msg, obs_aero.error_flag, obs_aero.remarks, obs_aero.remarks_qa, obs_aero.wind_speed_knots, obs_aero.max_gust_10m_knots, obs_aero.visibility_miles FROM obs_aero ORDER BY obs_aero.station_no, obs_aero.lsd;


ALTER TABLE public.ext_obs_aero OWNER TO clidegui;

--
-- Name: obs_aws_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obs_aws_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obs_aws_id OWNER TO clidegui;

--
-- Name: SEQUENCE obs_aws_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obs_aws_id IS 'PK sequence for obs_aws';


--
-- Name: obs_aws; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obs_aws (
    id integer DEFAULT nextval('obs_aws_id'::regclass) NOT NULL,
    station_no character varying(15) NOT NULL,
    lsd timestamp without time zone NOT NULL,
    gmt timestamp without time zone,
    lct timestamp without time zone,
    insert_datetime timestamp without time zone NOT NULL,
    change_datetime timestamp without time zone,
    change_user character varying(20),
    data_source character(2),
    qa_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    measure_period smallint,
    mn_wind_dir_pt character(3),
    mn_wind_dir_deg smallint,
    mn_wind_dir_qa character(2),
    mn_wind_dir_stddev numeric(3,1),
    mn_wind_dir_stddev_qa character(2),
    mn_wind_speed numeric(7,1),
    mn_wind_speed_qa character(2),
    mn_wind_speed_stddev numeric(7,1),
    mn_wind_speed_stddev_qa character(2),
    mn_gust_speed numeric(7,1),
    mn_gust_speed_qa character(2),
    mn_gust_time character varying(8),
    mn_gust_time_qa character(2),
    mn_gust_dir_pt character(3),
    mn_gust_dir_deg smallint,
    mn_gust_dir_qa character(2),
    inst_gust_speed numeric(7,1),
    inst_gust_qa character(2),
    inst_gust_time character varying(8),
    inst_gust_time_qa character(2),
    inst_gust_dir_pt character(3),
    inst_gust_dir_deg smallint,
    inst_gust_dir_qa character(2),
    mn_temp numeric(7,1),
    mn_temp_qa character(2),
    mn_temp_subaveraging numeric(7,1),
    mn_temp_subaveraging_period smallint,
    mn_temp_subaveraging_qa character(2),
    max_temp numeric(7,1),
    max_temp_time character varying(8),
    max_temp_time_qa character(2),
    max_temp_qa character(2),
    min_temp numeric(7,1),
    min_temp_qa character(2),
    min_temp_time character varying(8),
    min_temp_time_qa character(2),
    min_grass_temp numeric(7,1),
    min_grass_temp_qa character(2),
    min_grass_temp_time character varying(8),
    min_grass_temp_time_qa character(2),
    mn_humidity numeric(4,1),
    mn_humidity_qa character(2),
    max_humidity numeric(4,1),
    max_humidity_qa character(2),
    max_humidity_time character varying(8),
    max_humidity_time_qa character(2),
    min_humidity numeric(4,1),
    min_humidity_qa character(2),
    min_humidity_time character varying(8),
    min_humidity_time_qa character(2),
    mn_station_pres numeric(5,1),
    mn_station_pres_qa character(2),
    mn_sea_level_pres numeric(5,1),
    mn_sea_level_pres_qa character(2),
    max_pres numeric(5,1),
    max_pres_qa character(2),
    max_pres_time character varying(8),
    max_pres_time_qa character(2),
    min_pres numeric(5,1),
    min_pres_qa character(2),
    min_pres_time character varying(8),
    min_pres_time_qa character(2),
    tot_rain numeric(6,1),
    tot_rain_qa character(2),
    tot_rain_two numeric(6,1),
    tot_rain_two_qa character(2),
    tot_sun integer,
    tot_sun_qa character(2),
    tot_insolation numeric(7,2),
    tot_insolation_qa character(2),
    leaf_wetness smallint,
    leaf_wetness_qa character(2),
    mn_uv numeric(4,0),
    mn_uv_qa character(2),
    mn_soil_moisture_10 numeric(3,1),
    mn_soil_moisture_10_qa character(2),
    mn_soil_temp_10 numeric(5,1),
    mn_soil_temp_10_qa character(2),
    mn_soil_moisture_20 numeric(3,1),
    mn_soil_moisture_20_qa character(2),
    mn_soil_temp_20 numeric(5,1),
    mn_soil_temp_20_qa character(2),
    mn_soil_moisture_30 numeric(3,1),
    mn_soil_moisture_30_qa character(2),
    mn_soil_temp_30 numeric(5,1),
    mn_soil_temp_30_qa character(2),
    mn_soil_moisture_50 numeric(3,1),
    mn_soil_moisture_50_qa character(2),
    mn_soil_temp_50 numeric(5,1),
    mn_soil_temp_50_qa character(2),
    mn_soil_moisture_100 numeric(3,1),
    mn_soil_moisture_100_qa character(2),
    mn_soil_temp_100 numeric(5,1),
    mn_soil_temp_100_qa character(2)
);


ALTER TABLE public.obs_aws OWNER TO clidegui;

--
-- Name: TABLE obs_aws; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obs_aws IS 'AWS observations';


--
-- Name: COLUMN obs_aws.station_no; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.station_no IS 'Local Station identifier';


--
-- Name: COLUMN obs_aws.lsd; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.lsd IS 'Local System Time (No Daylight Savings)';


--
-- Name: COLUMN obs_aws.gmt; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.gmt IS 'GMT (UTC+0)';


--
-- Name: COLUMN obs_aws.lct; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.lct IS 'Local Clock Time (With Daylight Savings)';


--
-- Name: COLUMN obs_aws.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.insert_datetime IS 'Date/time row is inserted';


--
-- Name: COLUMN obs_aws.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.change_datetime IS 'Date/time row is changed';


--
-- Name: COLUMN obs_aws.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.change_user IS 'User who added/changed row';


--
-- Name: COLUMN obs_aws.qa_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.qa_flag IS 'QA flag for row (Y/N)';


--
-- Name: COLUMN obs_aws.measure_period; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.measure_period IS 'Average Period in minutes. "Standard" is (10 min)';


--
-- Name: COLUMN obs_aws.mn_wind_dir_pt; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_wind_dir_pt IS '(10 min) mean direction in points. ("ENE")';


--
-- Name: COLUMN obs_aws.mn_wind_dir_deg; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_wind_dir_deg IS '(10 min) mean direction in degrees. (0-360)';


--
-- Name: COLUMN obs_aws.mn_wind_dir_stddev; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_wind_dir_stddev IS '(10 min) mean dir Std Dev';


--
-- Name: COLUMN obs_aws.mn_wind_speed; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_wind_speed IS '(10 min) mean wind speed (m/s to 0.1)';


--
-- Name: COLUMN obs_aws.mn_wind_speed_stddev; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_wind_speed_stddev IS '(10 min) mean speed Std Dev (m/s to 0.1)';


--
-- Name: COLUMN obs_aws.mn_gust_speed; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_gust_speed IS '(10 min) mean gust speed (m/s to 0.1)';


--
-- Name: COLUMN obs_aws.mn_gust_time; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_gust_time IS 'Time at end of sample period';


--
-- Name: COLUMN obs_aws.mn_gust_dir_pt; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_gust_dir_pt IS 'Mean Direction of maximum wind speed. ("ENE")';


--
-- Name: COLUMN obs_aws.mn_gust_dir_deg; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_gust_dir_deg IS 'Mean Direction of maximum wind speed. (0-360)';


--
-- Name: COLUMN obs_aws.inst_gust_speed; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.inst_gust_speed IS 'Instantaneous gust speed (m/s to 0.1)';


--
-- Name: COLUMN obs_aws.inst_gust_time; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.inst_gust_time IS 'Time of instantaneous gust speed (09:30)';


--
-- Name: COLUMN obs_aws.inst_gust_dir_pt; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.inst_gust_dir_pt IS 'Direction of instantaneous gust speed. ("ENE")';


--
-- Name: COLUMN obs_aws.inst_gust_dir_deg; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.inst_gust_dir_deg IS 'Direction of instantaneous gust speed. (0-360)';


--
-- Name: COLUMN obs_aws.mn_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_temp IS '(10 min) mean. (C to 0.1)';


--
-- Name: COLUMN obs_aws.mn_temp_subaveraging; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_temp_subaveraging IS 'Sub-averaged temp (C to 0.1)';


--
-- Name: COLUMN obs_aws.mn_temp_subaveraging_period; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_temp_subaveraging_period IS 'Sub-averaging period (minutes)';


--
-- Name: COLUMN obs_aws.max_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.max_temp IS '(10 min) maximum. (C to 0.1)';


--
-- Name: COLUMN obs_aws.max_temp_time; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.max_temp_time IS 'Time of max temperature. (hh:mm:ss)';


--
-- Name: COLUMN obs_aws.min_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.min_temp IS '(10 min) minimum. (C to 0.1)';


--
-- Name: COLUMN obs_aws.min_temp_time; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.min_temp_time IS 'Time of min temperature.  (hh:mm:ss)';


--
-- Name: COLUMN obs_aws.min_grass_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.min_grass_temp IS '(10 min) minimum grass temp. (C to 0.1)';


--
-- Name: COLUMN obs_aws.min_grass_temp_time; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.min_grass_temp_time IS 'Time of min grass temp.  (hh:mm:ss)';


--
-- Name: COLUMN obs_aws.mn_humidity; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_humidity IS '(10 min)average humidity (% to 0.1)';


--
-- Name: COLUMN obs_aws.max_humidity; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.max_humidity IS '(10 min) maximum humidity (% to 0.1)';


--
-- Name: COLUMN obs_aws.max_humidity_time; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.max_humidity_time IS 'Time of maximum humidity.  (hh:mm:ss)';


--
-- Name: COLUMN obs_aws.min_humidity; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.min_humidity IS '(10 min) minimum humidity (% to 0.1)';


--
-- Name: COLUMN obs_aws.min_humidity_time; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.min_humidity_time IS 'Time of minimum humidity.  (hh:mm:ss)';


--
-- Name: COLUMN obs_aws.mn_station_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_station_pres IS 'Average station pressure (hPa to 0.1)';


--
-- Name: COLUMN obs_aws.mn_sea_level_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_sea_level_pres IS 'Average sea level pressure (hPa to 0.1)';


--
-- Name: COLUMN obs_aws.max_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.max_pres IS 'Maximum pressure (hPa to 0.1)';


--
-- Name: COLUMN obs_aws.max_pres_time; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.max_pres_time IS 'Time of maximum pressure.  (hh:mm:ss)';


--
-- Name: COLUMN obs_aws.min_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.min_pres IS 'Minimum pressure (hPa to 0.1)';


--
-- Name: COLUMN obs_aws.min_pres_time; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.min_pres_time IS 'Time of minimum pressure.  (hh:mm:ss)';


--
-- Name: COLUMN obs_aws.tot_rain; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.tot_rain IS '(10 min) total rainfall (mm to 0.1)';


--
-- Name: COLUMN obs_aws.tot_rain_two; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.tot_rain_two IS '(10 min) total rainfall instrument #2 (mm to 0.1)';


--
-- Name: COLUMN obs_aws.tot_sun; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.tot_sun IS '(10 min) total sunshine (secs, max 600)';


--
-- Name: COLUMN obs_aws.tot_insolation; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.tot_insolation IS '(10 min) insolation (Mj/m2 to 0.01)';


--
-- Name: COLUMN obs_aws.leaf_wetness; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.leaf_wetness IS '1/0 indicating leaf wetness.';


--
-- Name: COLUMN obs_aws.mn_uv; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_uv IS '(10 min) mean UV (mV)';


--
-- Name: COLUMN obs_aws.mn_soil_moisture_10; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_soil_moisture_10 IS '(10 min) mean soil moisture at 10cm (% to 0.1)';


--
-- Name: COLUMN obs_aws.mn_soil_temp_10; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_soil_temp_10 IS '(10 min) mean soil temperature at 10cm (C to 0.1)';


--
-- Name: COLUMN obs_aws.mn_soil_moisture_20; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_soil_moisture_20 IS '(10 min) mean soil moisture at 20cm (% to 0.1)';


--
-- Name: COLUMN obs_aws.mn_soil_temp_20; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_soil_temp_20 IS '(10 min) mean soil temperature at 20cm (C to 0.1)';


--
-- Name: COLUMN obs_aws.mn_soil_moisture_30; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_soil_moisture_30 IS '(10 min) mean soil moisture at 30cm (% to 0.1)';


--
-- Name: COLUMN obs_aws.mn_soil_temp_30; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_soil_temp_30 IS '(10 min) mean soil temperature at 30cm (C to 0.1)';


--
-- Name: COLUMN obs_aws.mn_soil_moisture_50; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_soil_moisture_50 IS '(10 min) mean soil moisture at 50cm (% to 0.1)';


--
-- Name: COLUMN obs_aws.mn_soil_temp_50; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_soil_temp_50 IS '(10 min) mean soil temperature at 50cm (C to 0.1)';


--
-- Name: COLUMN obs_aws.mn_soil_moisture_100; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_soil_moisture_100 IS '(10 min) mean soil moisture at 100cm (% to 0.1)';


--
-- Name: COLUMN obs_aws.mn_soil_temp_100; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_aws.mn_soil_temp_100 IS '(10 min) mean soil temperature at 100cm (C to 0.1)';


--
-- Name: ext_obs_aws; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_obs_aws AS
    SELECT obs_aws.id, obs_aws.station_no, obs_aws.lsd, obs_aws.gmt, obs_aws.lct, obs_aws.insert_datetime, obs_aws.change_datetime, obs_aws.change_user, obs_aws.data_source, obs_aws.qa_flag, obs_aws.measure_period, obs_aws.mn_wind_dir_pt, obs_aws.mn_wind_dir_deg, obs_aws.mn_wind_dir_qa, obs_aws.mn_wind_dir_stddev, obs_aws.mn_wind_dir_stddev_qa, obs_aws.mn_wind_speed, obs_aws.mn_wind_speed_qa, obs_aws.mn_wind_speed_stddev, obs_aws.mn_wind_speed_stddev_qa, obs_aws.mn_gust_speed, obs_aws.mn_gust_speed_qa, obs_aws.mn_gust_time, obs_aws.mn_gust_time_qa, obs_aws.mn_gust_dir_pt, obs_aws.mn_gust_dir_deg, obs_aws.mn_gust_dir_qa, obs_aws.inst_gust_speed, obs_aws.inst_gust_qa, obs_aws.inst_gust_time, obs_aws.inst_gust_time_qa, obs_aws.inst_gust_dir_pt, obs_aws.inst_gust_dir_deg, obs_aws.inst_gust_dir_qa, obs_aws.mn_temp, obs_aws.mn_temp_qa, obs_aws.mn_temp_subaveraging, obs_aws.mn_temp_subaveraging_period, obs_aws.mn_temp_subaveraging_qa, obs_aws.max_temp, obs_aws.max_temp_time, obs_aws.max_temp_time_qa, obs_aws.max_temp_qa, obs_aws.min_temp, obs_aws.min_temp_qa, obs_aws.min_temp_time, obs_aws.min_temp_time_qa, obs_aws.min_grass_temp, obs_aws.min_grass_temp_qa, obs_aws.min_grass_temp_time, obs_aws.min_grass_temp_time_qa, obs_aws.mn_humidity, obs_aws.mn_humidity_qa, obs_aws.max_humidity, obs_aws.max_humidity_qa, obs_aws.max_humidity_time, obs_aws.max_humidity_time_qa, obs_aws.min_humidity, obs_aws.min_humidity_qa, obs_aws.min_humidity_time, obs_aws.min_humidity_time_qa, obs_aws.mn_station_pres, obs_aws.mn_station_pres_qa, obs_aws.mn_sea_level_pres, obs_aws.mn_sea_level_pres_qa, obs_aws.max_pres, obs_aws.max_pres_qa, obs_aws.max_pres_time, obs_aws.max_pres_time_qa, obs_aws.min_pres, obs_aws.min_pres_qa, obs_aws.min_pres_time, obs_aws.min_pres_time_qa, obs_aws.tot_rain, obs_aws.tot_rain_qa, obs_aws.tot_rain_two, obs_aws.tot_rain_two_qa, obs_aws.tot_sun, obs_aws.tot_sun_qa, obs_aws.tot_insolation, obs_aws.tot_insolation_qa, obs_aws.leaf_wetness, obs_aws.leaf_wetness_qa, obs_aws.mn_uv, obs_aws.mn_uv_qa, obs_aws.mn_soil_moisture_10, obs_aws.mn_soil_moisture_10_qa, obs_aws.mn_soil_temp_10, obs_aws.mn_soil_temp_10_qa, obs_aws.mn_soil_moisture_20, obs_aws.mn_soil_moisture_20_qa, obs_aws.mn_soil_temp_20, obs_aws.mn_soil_temp_20_qa, obs_aws.mn_soil_moisture_30, obs_aws.mn_soil_moisture_30_qa, obs_aws.mn_soil_temp_30, obs_aws.mn_soil_temp_30_qa, obs_aws.mn_soil_moisture_50, obs_aws.mn_soil_moisture_50_qa, obs_aws.mn_soil_temp_50, obs_aws.mn_soil_temp_50_qa, obs_aws.mn_soil_moisture_100, obs_aws.mn_soil_moisture_100_qa, obs_aws.mn_soil_temp_100, obs_aws.mn_soil_temp_100_qa FROM obs_aws ORDER BY obs_aws.station_no, obs_aws.lsd;


ALTER TABLE public.ext_obs_aws OWNER TO clidegui;

--
-- Name: obs_daily_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obs_daily_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obs_daily_id OWNER TO clidegui;

--
-- Name: SEQUENCE obs_daily_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obs_daily_id IS 'PK sequence for obs_daily';


--
-- Name: obs_daily; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obs_daily (
    id integer DEFAULT nextval('obs_daily_id'::regclass) NOT NULL,
    station_no character varying(15) NOT NULL,
    lsd timestamp without time zone NOT NULL,
    data_source character(2) NOT NULL,
    insert_datetime timestamp without time zone DEFAULT now() NOT NULL,
    change_datetime timestamp without time zone,
    change_user character varying(20),
    qa_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    aws_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    comments character varying(1000),
    rain_24h numeric(6,1),
    rain_24h_inches numeric(7,3),
    rain_24h_period numeric(2,0),
    rain_24h_type character varying(10),
    rain_24h_count numeric(2,0),
    rain_24h_qa character(2),
    max_air_temp numeric(7,1),
    max_air_temp_f numeric(7,1),
    max_air_temp_period numeric(2,0),
    max_air_temp_time character varying(5),
    max_air_temp_qa character(2),
    min_air_temp numeric(5,1),
    min_air_temp_f numeric(5,1),
    min_air_temp_period numeric(2,0),
    min_air_temp_time character varying(5),
    min_air_temp_qa character(2),
    reg_max_air_temp numeric(7,1),
    reg_max_air_temp_qa character(2),
    reg_min_air_temp numeric(7,1),
    reg_min_air_temp_qa character(2),
    ground_temp numeric(5,1),
    ground_temp_f numeric(5,1),
    ground_temp_qa character(2),
    max_gust_dir numeric(3,0),
    max_gust_dir_qa character(2),
    max_gust_speed numeric(4,1),
    max_gust_speed_kts numeric(3,0),
    max_gust_speed_bft character varying(2),
    max_gust_speed_qa character(2),
    max_gust_time character varying(5),
    max_gust_time_qa character(2),
    wind_run_lt10 numeric(6,2),
    wind_run_lt10_miles numeric(6,2),
    wind_run_lt10_period numeric(3,0),
    wind_run_lt10_qa character(2),
    wind_run_gt10 numeric(6,2),
    wind_run_gt10_miles numeric(6,2),
    wind_run_gt10_period numeric(3,0),
    wind_run_gt10_qa character(2),
    evaporation numeric(4,1),
    evaporation_inches numeric(5,3),
    evaporation_period numeric(3,0),
    evaporation_qa character(2),
    evap_water_max_temp numeric(5,1),
    evap_water_max_temp_f numeric(5,1),
    evap_water_max_temp_qa character(2),
    evap_water_min_temp numeric(5,1),
    evap_water_min_temp_f numeric(5,1),
    evap_water_min_temp_qa character(2),
    sunshine_duration numeric(3,1),
    sunshine_duration_qa character(2),
    river_height numeric(5,1),
    river_height_in numeric(8,1),
    river_height_qa character(2),
    radiation numeric(6,1),
    radiation_qa character(2),
    thunder_flag character(1),
    thunder_flag_qa character(2),
    frost_flag character(1),
    frost_flag_qa character(2),
    dust_flag character(1),
    dust_flag_qa character(2),
    haze_flag character(1),
    haze_flag_qa character(2),
    fog_flag character(1),
    fog_flag_qa character(2),
    strong_wind_flag character(1),
    strong_wind_flag_qa character(2),
    gale_flag character(1),
    gale_flag_qa character(2),
    hail_flag character(1),
    hail_flag_qa character(2),
    snow_flag character(1),
    snow_flag_qa character(2),
    lightning_flag character(1),
    lightning_flag_qa character(2),
    shower_flag character(1),
    shower_flag_qa character(2),
    rain_flag character(1),
    rain_flag_qa character(2),
    dew_flag character(1),
    dew_flag_qa character(2)
);


ALTER TABLE public.obs_daily OWNER TO clidegui;

--
-- Name: TABLE obs_daily; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obs_daily IS 'Daily surface observations';


--
-- Name: COLUMN obs_daily.station_no; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.station_no IS 'Local Station identifier';


--
-- Name: COLUMN obs_daily.lsd; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.lsd IS 'Local System Time (No Daylight Savings)';


--
-- Name: COLUMN obs_daily.data_source; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.data_source IS 'Code for data source (DATA_SRC)';


--
-- Name: COLUMN obs_daily.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.insert_datetime IS 'Date/time row is inserted';


--
-- Name: COLUMN obs_daily.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.change_datetime IS 'Date/time row is changed';


--
-- Name: COLUMN obs_daily.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.change_user IS 'User who added/changed row';


--
-- Name: COLUMN obs_daily.qa_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.qa_flag IS 'QA flag for row (Y/N)';


--
-- Name: COLUMN obs_daily.aws_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.aws_flag IS 'AWS sourced data or not (Y/N)';


--
-- Name: COLUMN obs_daily.comments; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.comments IS 'User comments';


--
-- Name: COLUMN obs_daily.rain_24h; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.rain_24h IS 'LCT 0900 to 0900 (mm to 0.1)';


--
-- Name: COLUMN obs_daily.rain_24h_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.rain_24h_inches IS 'LCT 0900 to 0900 (inches to 0.001)';


--
-- Name: COLUMN obs_daily.rain_24h_period; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.rain_24h_period IS 'Period of data: Normally 1 day';


--
-- Name: COLUMN obs_daily.rain_24h_type; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.rain_24h_type IS 'rain,frost,fog,dew,trace,snow,other, n/a';


--
-- Name: COLUMN obs_daily.rain_24h_count; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.rain_24h_count IS 'No of days rain has fallen. Default 1.';


--
-- Name: COLUMN obs_daily.rain_24h_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.rain_24h_qa IS 'Quality code for rain_24h';


--
-- Name: COLUMN obs_daily.max_air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.max_air_temp IS 'Maximum air temperature (0.1C). Standard 0900';


--
-- Name: COLUMN obs_daily.max_air_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.max_air_temp_f IS 'Maximum air temperature (0.1F). Standard 0900';


--
-- Name: COLUMN obs_daily.max_air_temp_period; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.max_air_temp_period IS 'Period for max air temp (hours). Standard 0900';


--
-- Name: COLUMN obs_daily.max_air_temp_time; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.max_air_temp_time IS 'Time that max air temp was reached. Standard 0900';


--
-- Name: COLUMN obs_daily.max_air_temp_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.max_air_temp_qa IS 'Quality code for max_air_temp';


--
-- Name: COLUMN obs_daily.min_air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.min_air_temp IS 'Minimum air temperature (0.1C). Standard 0900';


--
-- Name: COLUMN obs_daily.min_air_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.min_air_temp_f IS 'Minimum air temperature (0.1F). Standard 0900';


--
-- Name: COLUMN obs_daily.min_air_temp_period; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.min_air_temp_period IS 'Period for min air temp (hours). Standard 0900';


--
-- Name: COLUMN obs_daily.min_air_temp_time; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.min_air_temp_time IS 'Time that min air temp was reached. Standard 0900';


--
-- Name: COLUMN obs_daily.min_air_temp_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.min_air_temp_qa IS 'Quality code for min_air_temp';


--
-- Name: COLUMN obs_daily.reg_max_air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.reg_max_air_temp IS 'Maximum air temperature (0.1C). Regional.';


--
-- Name: COLUMN obs_daily.reg_max_air_temp_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.reg_max_air_temp_qa IS 'Quality code for max_air_temp_reg';


--
-- Name: COLUMN obs_daily.reg_min_air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.reg_min_air_temp IS 'Minimum air temperature (0.1C). Regional.';


--
-- Name: COLUMN obs_daily.reg_min_air_temp_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.reg_min_air_temp_qa IS 'Quality code for min_air_temp';


--
-- Name: COLUMN obs_daily.ground_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.ground_temp IS 'Ground surface temp (0.1C)';


--
-- Name: COLUMN obs_daily.ground_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.ground_temp_f IS 'Ground surface temp (0.1F)';


--
-- Name: COLUMN obs_daily.ground_temp_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.ground_temp_qa IS 'Quality code for ground_temp';


--
-- Name: COLUMN obs_daily.max_gust_dir; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.max_gust_dir IS 'Degrees (0-360)';


--
-- Name: COLUMN obs_daily.max_gust_dir_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.max_gust_dir_qa IS 'Quality code for max_gust_dir';


--
-- Name: COLUMN obs_daily.max_gust_speed; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.max_gust_speed IS 'Speed of max wind gust M/s (0.1)';


--
-- Name: COLUMN obs_daily.max_gust_speed_bft; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.max_gust_speed_bft IS 'Speed of max wind gust Beaufort';


--
-- Name: COLUMN obs_daily.max_gust_speed_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.max_gust_speed_qa IS 'Quality code for max_gust_speed';


--
-- Name: COLUMN obs_daily.max_gust_time; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.max_gust_time IS 'Time of max wind gust';


--
-- Name: COLUMN obs_daily.max_gust_time_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.max_gust_time_qa IS 'Quality code for max_gust_time';


--
-- Name: COLUMN obs_daily.wind_run_lt10; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.wind_run_lt10 IS 'Wind run taken from <10M (evaporation) Km';


--
-- Name: COLUMN obs_daily.wind_run_lt10_miles; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.wind_run_lt10_miles IS 'Wind run taken from <10M (evaporation) Miles';


--
-- Name: COLUMN obs_daily.wind_run_lt10_period; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.wind_run_lt10_period IS 'Period in hours for Wind run <10';


--
-- Name: COLUMN obs_daily.wind_run_lt10_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.wind_run_lt10_qa IS 'Quality code for wind_run_lt10';


--
-- Name: COLUMN obs_daily.wind_run_gt10; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.wind_run_gt10 IS 'Wind run taken from >10M anemometer Km';


--
-- Name: COLUMN obs_daily.wind_run_gt10_miles; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.wind_run_gt10_miles IS 'Wind run taken from >10M anemometer Miles';


--
-- Name: COLUMN obs_daily.wind_run_gt10_period; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.wind_run_gt10_period IS 'Period in hours for Wind run >10';


--
-- Name: COLUMN obs_daily.wind_run_gt10_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.wind_run_gt10_qa IS 'Quality code for wind_run_gt10';


--
-- Name: COLUMN obs_daily.evaporation; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.evaporation IS 'Evaporation in mm (0.1)';


--
-- Name: COLUMN obs_daily.evaporation_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.evaporation_inches IS 'Evaporation in inches (0.001)';


--
-- Name: COLUMN obs_daily.evaporation_period; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.evaporation_period IS 'Period in hours for evaporation';


--
-- Name: COLUMN obs_daily.evaporation_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.evaporation_qa IS 'Quality code for evaporation';


--
-- Name: COLUMN obs_daily.evap_water_max_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.evap_water_max_temp IS 'Max water temp (0.1C)';


--
-- Name: COLUMN obs_daily.evap_water_max_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.evap_water_max_temp_f IS 'Max water temp (0.1F)';


--
-- Name: COLUMN obs_daily.evap_water_max_temp_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.evap_water_max_temp_qa IS 'Quality code for evap_max_temp';


--
-- Name: COLUMN obs_daily.evap_water_min_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.evap_water_min_temp IS 'Min water temp (0.1C)';


--
-- Name: COLUMN obs_daily.evap_water_min_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.evap_water_min_temp_f IS 'Min water temp (0.1F)';


--
-- Name: COLUMN obs_daily.evap_water_min_temp_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.evap_water_min_temp_qa IS 'Quality code for evap_min_temp';


--
-- Name: COLUMN obs_daily.sunshine_duration; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.sunshine_duration IS 'Decimal Hours to (0.1)';


--
-- Name: COLUMN obs_daily.sunshine_duration_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.sunshine_duration_qa IS 'Quality code for sunshine_duration';


--
-- Name: COLUMN obs_daily.river_height; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.river_height IS 'Daily river height reading (0.1M)';


--
-- Name: COLUMN obs_daily.river_height_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.river_height_qa IS 'Quality code for river_height';


--
-- Name: COLUMN obs_daily.radiation; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.radiation IS 'Daily radiation Mj/M to 0.1';


--
-- Name: COLUMN obs_daily.radiation_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.radiation_qa IS 'Quality code for radiation';


--
-- Name: COLUMN obs_daily.thunder_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.thunder_flag IS 'Y/N for thunder';


--
-- Name: COLUMN obs_daily.thunder_flag_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.thunder_flag_qa IS 'Quality code for thunder_flag';


--
-- Name: COLUMN obs_daily.frost_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.frost_flag IS 'Y/N for frost';


--
-- Name: COLUMN obs_daily.frost_flag_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.frost_flag_qa IS 'Quality code for frost_flag';


--
-- Name: COLUMN obs_daily.dust_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.dust_flag IS 'Y/N for dust';


--
-- Name: COLUMN obs_daily.dust_flag_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.dust_flag_qa IS 'Quality code for dust_flag';


--
-- Name: COLUMN obs_daily.haze_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.haze_flag IS 'Y/N for haze';


--
-- Name: COLUMN obs_daily.haze_flag_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.haze_flag_qa IS 'Quality code for haze_flag';


--
-- Name: COLUMN obs_daily.fog_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.fog_flag IS 'Y/N for fog';


--
-- Name: COLUMN obs_daily.fog_flag_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.fog_flag_qa IS 'Quality code for fog_flag';


--
-- Name: COLUMN obs_daily.strong_wind_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.strong_wind_flag IS 'Y/N for strong wind';


--
-- Name: COLUMN obs_daily.strong_wind_flag_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.strong_wind_flag_qa IS 'Quality code for strong_wind_flag';


--
-- Name: COLUMN obs_daily.gale_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.gale_flag IS 'Y/N for gale';


--
-- Name: COLUMN obs_daily.gale_flag_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.gale_flag_qa IS 'Quality code for gale_flag';


--
-- Name: COLUMN obs_daily.hail_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.hail_flag IS 'Y/N for hail';


--
-- Name: COLUMN obs_daily.hail_flag_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.hail_flag_qa IS 'Quality code for hail_flag';


--
-- Name: COLUMN obs_daily.snow_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.snow_flag IS 'Y/N for snow';


--
-- Name: COLUMN obs_daily.snow_flag_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.snow_flag_qa IS 'Quality code for snow_flag';


--
-- Name: COLUMN obs_daily.lightning_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.lightning_flag IS 'Y/N for lightning';


--
-- Name: COLUMN obs_daily.lightning_flag_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.lightning_flag_qa IS 'Quality code for lightning_flag';


--
-- Name: COLUMN obs_daily.shower_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.shower_flag IS 'Y/N for shower';


--
-- Name: COLUMN obs_daily.shower_flag_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.shower_flag_qa IS 'Quality code for shower_flag';


--
-- Name: COLUMN obs_daily.rain_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.rain_flag IS 'Y/N for rain';


--
-- Name: COLUMN obs_daily.rain_flag_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_daily.rain_flag_qa IS 'Quality code for rain_flag';


--
-- Name: obs_subdaily_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obs_subdaily_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obs_subdaily_id OWNER TO clidegui;

--
-- Name: SEQUENCE obs_subdaily_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obs_subdaily_id IS 'PK sequence for obs_subdaily';


--
-- Name: obs_subdaily; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obs_subdaily (
    id integer DEFAULT nextval('obs_subdaily_id'::regclass) NOT NULL,
    station_no character varying(15) NOT NULL,
    lsd timestamp without time zone NOT NULL,
    gmt timestamp without time zone,
    lct timestamp without time zone,
    data_source character(2) NOT NULL,
    insert_datetime timestamp without time zone NOT NULL,
    change_datetime timestamp without time zone,
    change_user character varying(20),
    qa_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    aws_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    comments character varying(1000),
    air_temp numeric(7,1),
    air_temp_f numeric(7,1),
    air_temp_qa character(2),
    sea_water_temp numeric(7,1),
    sea_water_temp_f numeric(7,1),
    sea_water_temp_qa character(2),
    wet_bulb numeric(7,1),
    wet_bulb_f numeric(7,1),
    wet_bulb_qa character(2),
    dew_point numeric(7,1),
    dew_point_f numeric(7,1),
    dew_point_qa character(2),
    rel_humidity numeric(4,1),
    rel_humidity_qa character(2),
    baro_temp numeric(7,1),
    baro_temp_f numeric(7,1),
    baro_temp_qa character(2),
    pres_as_read numeric(7,1),
    pres_as_read_inches numeric(8,3),
    pres_as_read_qa character(2),
    station_pres numeric(7,1),
    station_pres_inches numeric(8,3),
    station_pres_qa character(2),
    msl_pres numeric(7,1),
    msl_pres_inches numeric(8,3),
    msl_pres_qa character(2),
    vapour_pres numeric(7,1),
    vapour_pres_inches numeric(8,3),
    vapour_pres_qa character(2),
    qnh numeric(7,1),
    qnh_qa character(2),
    visibility numeric(7,3),
    visibility_miles numeric(7,3),
    visibility_code character(1),
    visibility_qa character(2),
    rain_3h numeric(7,1),
    rain_3h_inches numeric(7,3),
    rain_3h_qa character(2),
    rain_3h_hours numeric(3,0) DEFAULT 3,
    rain_cum numeric(7,1),
    rain_cum_inches numeric(7,3),
    rain_cum_qa character(2),
    wind_dir numeric(3,0),
    wind_dir_qa character(2),
    wind_dir_std_dev numeric(3,0),
    wind_dir_std_dev_qa character(2),
    wind_speed numeric(5,1),
    wind_speed_knots numeric(5,1),
    wind_speed_mph numeric(5,1),
    wind_speed_bft character(2),
    wind_speed_qa character(2),
    pres_weather_code character varying(2),
    pres_weather_bft character varying(20),
    pres_weather_qa character(2),
    past_weather_code character varying(2),
    past_weather_bft character varying(20),
    past_weather_qa character(2),
    tot_cloud_oktas smallint,
    tot_cloud_tenths smallint,
    tot_cloud_qa character(2),
    tot_low_cloud_oktas smallint,
    tot_low_cloud_tenths smallint,
    tot_low_cloud_height integer,
    tot_low_cloud_qa character(2),
    state_of_sea character varying(2),
    state_of_sea_qa character(2),
    state_of_swell character varying(2),
    state_of_swell_qa character(2),
    swell_direction character varying(3),
    swell_direction_qa character(2),
    sea_level numeric(5,3),
    sea_level_qa character(2),
    sea_level_residual numeric(5,3),
    sea_level_residual_qa character(2),
    sea_level_resid_adj numeric(5,3),
    sea_level_resid_adj_qa character(2),
    radiation numeric(6,1),
    radiation_qa character(2),
    sunshine numeric(3,1),
    sunshine_qa character(2),
    tot_low_cloud_height_feet integer,
    wind_gust_kts numeric(3,0),
    wind_gust numeric(6,1),
    wind_gust_qa character(2),
    wind_gust_dir numeric(3,0),
    wind_gust_dir_qa character(2),
    river_height numeric(7,3),
    river_height_in numeric(8,1),
    river_height_qa character(2),
    qnh_inches numeric(8,3)
);


ALTER TABLE public.obs_subdaily OWNER TO clidegui;

--
-- Name: TABLE obs_subdaily; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obs_subdaily IS 'Sub Daily surface observations';


--
-- Name: COLUMN obs_subdaily.station_no; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.station_no IS 'Local Station identifier';


--
-- Name: COLUMN obs_subdaily.lsd; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.lsd IS 'Local System Time (No Daylight Savings)';


--
-- Name: COLUMN obs_subdaily.gmt; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.gmt IS 'GMT (UTC+0)';


--
-- Name: COLUMN obs_subdaily.lct; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.lct IS 'Local Clock Time (With Daylight Savings)';


--
-- Name: COLUMN obs_subdaily.data_source; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.data_source IS 'Code for data source (DATA_SRC)';


--
-- Name: COLUMN obs_subdaily.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.insert_datetime IS 'Date/time row is inserted';


--
-- Name: COLUMN obs_subdaily.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.change_datetime IS 'Date/time row is changed';


--
-- Name: COLUMN obs_subdaily.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.change_user IS 'User who added/changed row';


--
-- Name: COLUMN obs_subdaily.qa_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.qa_flag IS 'QA flag for row (Y/N)';


--
-- Name: COLUMN obs_subdaily.aws_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.aws_flag IS 'AWS sourced data or not (Y/N)';


--
-- Name: COLUMN obs_subdaily.comments; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.comments IS 'User comments';


--
-- Name: COLUMN obs_subdaily.air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.air_temp IS 'Current Air temperature (0.1C)';


--
-- Name: COLUMN obs_subdaily.air_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.air_temp_f IS 'Current Air Temp in Fahrenheit (0.1F)';


--
-- Name: COLUMN obs_subdaily.air_temp_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.air_temp_qa IS 'Quality Code for air_temp';


--
-- Name: COLUMN obs_subdaily.sea_water_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.sea_water_temp IS 'Current Sea water Temperature (0.1C)';


--
-- Name: COLUMN obs_subdaily.sea_water_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.sea_water_temp_f IS 'Current Sea water Temp in Fahrenheit (0.1F)';


--
-- Name: COLUMN obs_subdaily.sea_water_temp_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.sea_water_temp_qa IS 'Quality Code for sea_water_temp';


--
-- Name: COLUMN obs_subdaily.wet_bulb; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.wet_bulb IS 'Current Wet bulb reading (0.1C)';


--
-- Name: COLUMN obs_subdaily.wet_bulb_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.wet_bulb_f IS 'Current Wet bulb reading in Fahrenheit (0.1F)';


--
-- Name: COLUMN obs_subdaily.wet_bulb_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.wet_bulb_qa IS 'Quality Code for wet_bulb';


--
-- Name: COLUMN obs_subdaily.dew_point; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.dew_point IS 'Current Dew Point Temperature (0.1C)';


--
-- Name: COLUMN obs_subdaily.dew_point_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.dew_point_f IS 'Current Dew Point Fahrenheit (0.1F)';


--
-- Name: COLUMN obs_subdaily.dew_point_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.dew_point_qa IS 'Quality Code for dew_point';


--
-- Name: COLUMN obs_subdaily.rel_humidity; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.rel_humidity IS 'Relative humidity  (% to 0.1)';


--
-- Name: COLUMN obs_subdaily.rel_humidity_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.rel_humidity_qa IS 'Quality Code for rel_humidity';


--
-- Name: COLUMN obs_subdaily.baro_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.baro_temp IS 'Current Barometer Temperature (0.1C)';


--
-- Name: COLUMN obs_subdaily.baro_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.baro_temp_f IS 'Current Barometer Fahrenheit (0.1F)';


--
-- Name: COLUMN obs_subdaily.baro_temp_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.baro_temp_qa IS 'Quality Code for baro_temp';


--
-- Name: COLUMN obs_subdaily.pres_as_read; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.pres_as_read IS 'Pressure as read from barometer (hPa to 0.1)';


--
-- Name: COLUMN obs_subdaily.pres_as_read_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.pres_as_read_inches IS 'Pressure as read from barometer (Inches to 0.001)';


--
-- Name: COLUMN obs_subdaily.pres_as_read_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.pres_as_read_qa IS 'Quality Code for pres_as_read';


--
-- Name: COLUMN obs_subdaily.station_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.station_pres IS 'Station Pressure (hPa to 0.1)';


--
-- Name: COLUMN obs_subdaily.station_pres_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.station_pres_inches IS 'Station Pressure (Inches to 0.001)';


--
-- Name: COLUMN obs_subdaily.station_pres_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.station_pres_qa IS 'Quality Code for station_pres';


--
-- Name: COLUMN obs_subdaily.msl_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.msl_pres IS 'Mean Sea Level Pressure (hPa to 0.1)';


--
-- Name: COLUMN obs_subdaily.msl_pres_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.msl_pres_inches IS 'Mean Sea Level Pressure (Inches to 0.001)';


--
-- Name: COLUMN obs_subdaily.msl_pres_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.msl_pres_qa IS 'Quality Code for msl_pres';


--
-- Name: COLUMN obs_subdaily.vapour_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.vapour_pres IS 'Vapour Pressure (hPa to 0.1)';


--
-- Name: COLUMN obs_subdaily.vapour_pres_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.vapour_pres_inches IS 'Vapour Pressure (Inches to 0.001)';


--
-- Name: COLUMN obs_subdaily.vapour_pres_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.vapour_pres_qa IS 'Quality Code for vapour_pres';


--
-- Name: COLUMN obs_subdaily.qnh; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.qnh IS 'Local QNH (hPa to 0.1)';


--
-- Name: COLUMN obs_subdaily.qnh_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.qnh_qa IS 'Quality Code for qnh';


--
-- Name: COLUMN obs_subdaily.visibility; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.visibility IS 'Visibility in Km (Km to 0.001)';


--
-- Name: COLUMN obs_subdaily.visibility_miles; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.visibility_miles IS 'Visibility in Miles (Miles to 0.001)';


--
-- Name: COLUMN obs_subdaily.visibility_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.visibility_qa IS 'Quality Code for visibility';


--
-- Name: COLUMN obs_subdaily.rain_3h; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.rain_3h IS '3 hours cumulative (mm to 0.1)';


--
-- Name: COLUMN obs_subdaily.rain_3h_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.rain_3h_inches IS '3 hours cumulative (Inches to 0.001)';


--
-- Name: COLUMN obs_subdaily.rain_3h_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.rain_3h_qa IS 'Quality Code for rain_3h';


--
-- Name: COLUMN obs_subdaily.rain_cum; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.rain_cum IS 'Cumulative since 0900 (mm to 0.1)';


--
-- Name: COLUMN obs_subdaily.rain_cum_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.rain_cum_inches IS 'Cumulative since 0900 (Inches to 0.001)';


--
-- Name: COLUMN obs_subdaily.rain_cum_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.rain_cum_qa IS 'Quality Code for rain_cum';


--
-- Name: COLUMN obs_subdaily.wind_dir; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.wind_dir IS '10 min Avg Wind direction (degrees 0-360)';


--
-- Name: COLUMN obs_subdaily.wind_dir_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.wind_dir_qa IS 'Quality Code for wind_dir';


--
-- Name: COLUMN obs_subdaily.wind_dir_std_dev; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.wind_dir_std_dev IS '10 min Avg Wind direction standard deviation';


--
-- Name: COLUMN obs_subdaily.wind_dir_std_dev_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.wind_dir_std_dev_qa IS 'Quality Code for wind_dir_std_dev';


--
-- Name: COLUMN obs_subdaily.wind_speed; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.wind_speed IS '10 min Avg Wind Speed (M/S to 0.1)';


--
-- Name: COLUMN obs_subdaily.wind_speed_knots; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.wind_speed_knots IS '10 min Avg Wind Speed (Knots to 0.1)';


--
-- Name: COLUMN obs_subdaily.wind_speed_mph; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.wind_speed_mph IS '10 min Avg Wind Speed (MPH to 0.1)';


--
-- Name: COLUMN obs_subdaily.wind_speed_bft; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.wind_speed_bft IS '10 min Avg Beaufort code for wind speed';


--
-- Name: COLUMN obs_subdaily.wind_speed_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.wind_speed_qa IS 'Quality Code for wind_speed';


--
-- Name: COLUMN obs_subdaily.pres_weather_code; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.pres_weather_code IS 'WMO Code 4677 for present weather.';


--
-- Name: COLUMN obs_subdaily.pres_weather_bft; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.pres_weather_bft IS 'Beaufort Code for present weather';


--
-- Name: COLUMN obs_subdaily.pres_weather_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.pres_weather_qa IS 'Quality Code for pres_weather';


--
-- Name: COLUMN obs_subdaily.past_weather_code; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.past_weather_code IS 'WMO Code 4561';


--
-- Name: COLUMN obs_subdaily.past_weather_bft; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.past_weather_bft IS 'Beaufort Code for past weather';


--
-- Name: COLUMN obs_subdaily.past_weather_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.past_weather_qa IS 'Quality Code for past_weather';


--
-- Name: COLUMN obs_subdaily.tot_cloud_oktas; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.tot_cloud_oktas IS 'Total amount of sky covered by cloud (0-9)';


--
-- Name: COLUMN obs_subdaily.tot_cloud_tenths; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.tot_cloud_tenths IS 'Total amount of sky covered by cloud (0-10)';


--
-- Name: COLUMN obs_subdaily.tot_cloud_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.tot_cloud_qa IS 'Quality Code for tot_cloud';


--
-- Name: COLUMN obs_subdaily.tot_low_cloud_oktas; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.tot_low_cloud_oktas IS 'Total amount of sky covered by Low cloud (0-9)';


--
-- Name: COLUMN obs_subdaily.tot_low_cloud_tenths; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.tot_low_cloud_tenths IS 'Total amount of sky covered by Low cloud (0-10)';


--
-- Name: COLUMN obs_subdaily.tot_low_cloud_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.tot_low_cloud_qa IS 'Quality Code for tot_low_cloud';


--
-- Name: COLUMN obs_subdaily.state_of_sea; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.state_of_sea IS 'State of Sea (Douglas Scale WMO 3700)';


--
-- Name: COLUMN obs_subdaily.state_of_sea_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.state_of_sea_qa IS 'Quality Code for state_of_sea';


--
-- Name: COLUMN obs_subdaily.state_of_swell; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.state_of_swell IS 'State open sea swell (Douglas Scale WMO 3700)';


--
-- Name: COLUMN obs_subdaily.state_of_swell_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.state_of_swell_qa IS 'Quality Code for state_of_swell';


--
-- Name: COLUMN obs_subdaily.swell_direction; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.swell_direction IS 'Direction of Swell (16 Compass Points)';


--
-- Name: COLUMN obs_subdaily.swell_direction_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.swell_direction_qa IS 'Quality Code for swell_direction';


--
-- Name: COLUMN obs_subdaily.sea_level; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.sea_level IS 'Sea level (M to 0.001) above tide gauge zero';


--
-- Name: COLUMN obs_subdaily.sea_level_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.sea_level_qa IS 'Quality Code for sea_level';


--
-- Name: COLUMN obs_subdaily.sea_level_residual; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.sea_level_residual IS '+/- Diff from predicted sea level';


--
-- Name: COLUMN obs_subdaily.sea_level_residual_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.sea_level_residual_qa IS 'Quality Code for sea_level_residual';


--
-- Name: COLUMN obs_subdaily.sea_level_resid_adj; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.sea_level_resid_adj IS 'Adjusted residual (adjusted for pressure)';


--
-- Name: COLUMN obs_subdaily.sea_level_resid_adj_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.sea_level_resid_adj_qa IS 'Quality Code for sea_level_residual_adj';


--
-- Name: COLUMN obs_subdaily.radiation; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.radiation IS 'Radiation Mj/M to 0.1';


--
-- Name: COLUMN obs_subdaily.sunshine; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.sunshine IS 'Decimal Hours to 0.1';


--
-- Name: COLUMN obs_subdaily.wind_gust_kts; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.wind_gust_kts IS 'Wind Gust speed Knots';


--
-- Name: COLUMN obs_subdaily.wind_gust; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.wind_gust IS 'Wind Gust speed M/S';


--
-- Name: COLUMN obs_subdaily.wind_gust_dir; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.wind_gust_dir IS 'Wind Gust direction 0-360';


--
-- Name: COLUMN obs_subdaily.river_height; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily.river_height IS 'River height in M';


--
-- Name: ext_obs_climat; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_obs_climat AS
    SELECT subday.station_no, to_date(subday.yyyy_mm, 'yyyy-mm'::text) AS lsd, subday.station_pres, subday.msl_pres, subday.air_temp, subday.dew_point, subday.vapour_pres, day.max_temp, day.min_temp, day.rain, day.rain_days, day.sunshine, day.max_rowcount, day.min_rowcount, day.rain_rowcount, day.sunshine_rowcount, subday.pres_daycount, subday.temp_daycount, subday.vapour_daycount, date_part('day'::text, (((((("substring"(subday.yyyy_mm, 1, 4) || '-'::text) || "substring"(subday.yyyy_mm, 6, 2)) || '-01'::text))::date + '1 mon'::interval) - '1 day'::interval)) AS days_in_month FROM ((SELECT sdd.station_no, "substring"(sdd.yyyy_mm_dd, 1, 7) AS yyyy_mm, round(avg(sdd.station_pres), 1) AS station_pres, round(avg(sdd.msl_pres), 1) AS msl_pres, round(avg(sdd.air_temp), 1) AS air_temp, round(avg(sdd.dew_point), 1) AS dew_point, round(avg(sdd.vapour_pres), 1) AS vapour_pres, sum(iif_sql((sdd.pres_count >= 4), 1, 0)) AS pres_daycount, sum(iif_sql((sdd.temp_count >= 4), 1, 0)) AS temp_daycount, sum(iif_sql((sdd.vapour_count >= 4), 1, 0)) AS vapour_daycount FROM (SELECT sd.station_no, to_char(sd.lsd, 'yyyy-mm_dd'::text) AS yyyy_mm_dd, avg(sd.station_pres) AS station_pres, avg(sd.msl_pres) AS msl_pres, avg(sd.air_temp) AS air_temp, avg(sd.dew_point) AS dew_point, avg(exp((1.8096 + ((17.269425 * sd.dew_point) / (237.3 + sd.dew_point))))) AS vapour_pres, count(sd.station_pres) AS pres_count, count(sd.air_temp) AS temp_count, count(sd.dew_point) AS vapour_count FROM obs_subdaily sd GROUP BY sd.station_no, to_char(sd.lsd, 'yyyy-mm_dd'::text)) sdd GROUP BY sdd.station_no, "substring"(sdd.yyyy_mm_dd, 1, 7)) subday JOIN (SELECT d.station_no AS stationno, to_char(d.lsd, 'yyyy-mm'::text) AS yyyymm, round(avg(d.max_air_temp), 1) AS max_temp, round(avg(d.min_air_temp), 1) AS min_temp, round(sum(d.rain_24h), 1) AS rain, sum(d.rain_24h_count) AS rain_days, round(sum(d.sunshine_duration), 1) AS sunshine, count(d.max_air_temp) AS max_rowcount, count(d.min_air_temp) AS min_rowcount, count(d.rain_24h) AS rain_rowcount, count(d.sunshine_duration) AS sunshine_rowcount FROM obs_daily d GROUP BY d.station_no, to_char(d.lsd, 'yyyy-mm'::text)) day ON ((((subday.station_no)::text = (day.stationno)::text) AND (subday.yyyy_mm = day.yyyymm))));


ALTER TABLE public.ext_obs_climat OWNER TO clidegui;

--
-- Name: ext_obs_daily; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_obs_daily AS
    SELECT obs_daily.id, obs_daily.station_no, obs_daily.lsd, obs_daily.data_source, obs_daily.insert_datetime, obs_daily.change_datetime, obs_daily.change_user, obs_daily.qa_flag, obs_daily.aws_flag, obs_daily.comments, obs_daily.rain_24h, obs_daily.rain_24h_inches, obs_daily.rain_24h_period, obs_daily.rain_24h_type, obs_daily.rain_24h_count, obs_daily.rain_24h_qa, obs_daily.max_air_temp, obs_daily.max_air_temp_f, obs_daily.max_air_temp_period, obs_daily.max_air_temp_time, obs_daily.max_air_temp_qa, obs_daily.min_air_temp, obs_daily.min_air_temp_f, obs_daily.min_air_temp_period, obs_daily.min_air_temp_time, obs_daily.min_air_temp_qa, obs_daily.reg_max_air_temp, obs_daily.reg_max_air_temp_qa, obs_daily.reg_min_air_temp, obs_daily.reg_min_air_temp_qa, obs_daily.ground_temp, obs_daily.ground_temp_f, obs_daily.ground_temp_qa, obs_daily.max_gust_dir, obs_daily.max_gust_dir_qa, obs_daily.max_gust_speed, obs_daily.max_gust_speed_kts, obs_daily.max_gust_speed_bft, obs_daily.max_gust_speed_qa, obs_daily.max_gust_time, obs_daily.max_gust_time_qa, obs_daily.wind_run_lt10, obs_daily.wind_run_lt10_miles, obs_daily.wind_run_lt10_period, obs_daily.wind_run_lt10_qa, obs_daily.wind_run_gt10, obs_daily.wind_run_gt10_miles, obs_daily.wind_run_gt10_period, obs_daily.wind_run_gt10_qa, obs_daily.evaporation, obs_daily.evaporation_inches, obs_daily.evaporation_period, obs_daily.evaporation_qa, obs_daily.evap_water_max_temp, obs_daily.evap_water_max_temp_f, obs_daily.evap_water_max_temp_qa, obs_daily.evap_water_min_temp, obs_daily.evap_water_min_temp_f, obs_daily.evap_water_min_temp_qa, obs_daily.sunshine_duration, obs_daily.sunshine_duration_qa, obs_daily.river_height, obs_daily.river_height_in, obs_daily.river_height_qa, obs_daily.radiation, obs_daily.radiation_qa, obs_daily.thunder_flag, obs_daily.thunder_flag_qa, obs_daily.frost_flag, obs_daily.frost_flag_qa, obs_daily.dust_flag, obs_daily.dust_flag_qa, obs_daily.haze_flag, obs_daily.haze_flag_qa, obs_daily.fog_flag, obs_daily.fog_flag_qa, obs_daily.strong_wind_flag, obs_daily.strong_wind_flag_qa, obs_daily.gale_flag, obs_daily.gale_flag_qa, obs_daily.hail_flag, obs_daily.hail_flag_qa, obs_daily.snow_flag, obs_daily.snow_flag_qa, obs_daily.lightning_flag, obs_daily.lightning_flag_qa, obs_daily.shower_flag, obs_daily.shower_flag_qa, obs_daily.rain_flag, obs_daily.rain_flag_qa, obs_daily.dew_flag, obs_daily.dew_flag_qa FROM obs_daily ORDER BY obs_daily.station_no, obs_daily.lsd;


ALTER TABLE public.ext_obs_daily OWNER TO clidegui;

--
-- Name: ext_obs_daily_basics; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_obs_daily_basics AS
    SELECT obs_daily.station_no, obs_daily.lsd, obs_daily.max_air_temp, obs_daily.min_air_temp, obs_daily.rain_24h FROM obs_daily ORDER BY obs_daily.station_no, obs_daily.lsd;


ALTER TABLE public.ext_obs_daily_basics OWNER TO clidegui;

--
-- Name: key_settings_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE key_settings_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.key_settings_id OWNER TO clidegui;

--
-- Name: SEQUENCE key_settings_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE key_settings_id IS 'PK sequence for key_settings';


--
-- Name: obs_monthly; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obs_monthly (
    id integer DEFAULT nextval('key_settings_id'::regclass) NOT NULL,
    station_no character varying(15) NOT NULL,
    lsd date NOT NULL,
    data_source character(2),
    insert_datetime timestamp without time zone,
    change_datetime timestamp without time zone,
    change_user character varying(20),
    qa_flag character(1),
    comments character varying(1000),
    dly_max_rain numeric(8,1),
    dly_max_rain_inches numeric(8,1),
    dly_max_rain_date character varying(120),
    dly_max_rain_qa character(2),
    max_max_air_temp numeric(7,1),
    max_max_air_temp_f numeric(7,1),
    max_max_air_temp_qa character(2),
    max_max_air_temp_date character varying(120),
    min_min_air_temp numeric(7,1),
    min_min_air_temp_f numeric(7,1),
    min_min_air_temp_qa character(2),
    min_min_air_temp_date character varying(120),
    min_min_ground_temp numeric(7,1),
    min_min_ground_temp_f numeric(7,1),
    min_min_ground_temp_qa character(2),
    min_min_ground_temp_date character varying(120),
    mn_air_temp numeric(7,1),
    mn_air_temp_f numeric(7,1),
    mn_air_temp_qa character(2),
    mn_max_air_temp numeric(7,1),
    mn_max_air_temp_f numeric(7,1),
    mn_max_air_temp_qa character(2),
    mn_min_air_temp numeric(7,1),
    mn_min_air_temp_f numeric(7,1),
    mn_min_air_temp_qa character(2),
    mn_wet_bulb_temp numeric(7,1),
    mn_wet_bulb_temp_f numeric(7,1),
    mn_wet_bulb_temp_qa character(2),
    mn_min_ground_temp numeric(7,1),
    mn_min_ground_temp_f numeric(7,1),
    mn_min_ground_temp_qa character(2),
    mn_asread_pres numeric(7,1),
    mn_asread_pres_inches numeric(8,3),
    mn_asread_pres_mmhg numeric(7,2),
    mn_asread_pres_qa character(2),
    mn_msl_pres numeric(7,1),
    mn_msl_pres_inches numeric(8,3),
    mn_msl_pres_mmhg numeric(7,2),
    mn_msl_pres_qa character(2),
    mn_station_pres numeric(7,1),
    mn_station_pres_inches numeric(8,3),
    mn_station_pres_mmhg numeric(7,2),
    mn_station_pres_qa character(2),
    mn_vapour_pres numeric(7,1),
    mn_vapour_pres_inches numeric(8,3),
    mn_vapour_pres_mmhg numeric(7,2),
    mn_vapour_pres_qa character(2),
    mn_evaporation numeric(4,1),
    mn_evaporation_inches numeric(6,3),
    mn_evaporation_qa character(2),
    mn_rel_humidity numeric(4,1),
    mn_rel_humidity_qa character(2),
    mn_sun_hours numeric(4,2),
    mn_sun_hours_qa character(2),
    mn_tot_cloud_oktas numeric(1,0),
    mn_tot_cloud_tenths numeric(2,0),
    mn_tot_cloud_qa character(2),
    tot_evaporation numeric(8,1),
    tot_evaporation_inches numeric(9,3),
    tot_evaporation_qa character(2),
    tot_rain numeric(8,1),
    tot_rain_inches numeric(9,3),
    tot_rain_qa character(2),
    tot_rain_days numeric(4,0),
    tot_rain_days_qa character(2),
    tot_rain_percent numeric(4,0),
    tot_rain_percent_qa character(2)
);


ALTER TABLE public.obs_monthly OWNER TO clidegui;

--
-- Name: TABLE obs_monthly; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obs_monthly IS 'Stores monthly data not available as daily or subdaily';


--
-- Name: COLUMN obs_monthly.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.id IS 'Surrogate Key';


--
-- Name: COLUMN obs_monthly.station_no; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.station_no IS 'Local Station identifier';


--
-- Name: COLUMN obs_monthly.lsd; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.lsd IS 'Local System Year and Month';


--
-- Name: COLUMN obs_monthly.data_source; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.data_source IS 'Code for data source, see codes_simple for code_type=DATA_SRC';


--
-- Name: COLUMN obs_monthly.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.insert_datetime IS 'Date/Time row is inserted';


--
-- Name: COLUMN obs_monthly.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.change_datetime IS 'Date/Time row is updated';


--
-- Name: COLUMN obs_monthly.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.change_user IS 'User who added/changed row';


--
-- Name: COLUMN obs_monthly.qa_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.qa_flag IS 'QA flag for row Y/N';


--
-- Name: COLUMN obs_monthly.comments; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.comments IS 'User comments';


--
-- Name: COLUMN obs_monthly.dly_max_rain; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.dly_max_rain IS 'Highest Daily precipitation mm';


--
-- Name: COLUMN obs_monthly.dly_max_rain_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.dly_max_rain_inches IS 'Highest Daily precipitation (inches to .001)';


--
-- Name: COLUMN obs_monthly.dly_max_rain_date; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.dly_max_rain_date IS 'Date(s) of highest rain as dd,dd,dd,...';


--
-- Name: COLUMN obs_monthly.max_max_air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.max_max_air_temp IS 'Highest daily maximum air temp (C to 0.1)';


--
-- Name: COLUMN obs_monthly.max_max_air_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.max_max_air_temp_f IS 'Highest daily maximum air temp (F to 0.1)';


--
-- Name: COLUMN obs_monthly.max_max_air_temp_date; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.max_max_air_temp_date IS 'Date(s) of highest max air temp as dd,dd,dd,...';


--
-- Name: COLUMN obs_monthly.min_min_air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.min_min_air_temp IS 'Lowest daily minimum air temp (C to 0.1)';


--
-- Name: COLUMN obs_monthly.min_min_air_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.min_min_air_temp_f IS 'Lowest daily minimum air temp (F to 0.1)';


--
-- Name: COLUMN obs_monthly.min_min_air_temp_date; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.min_min_air_temp_date IS 'Date(s) of lowest daily min as dd,dd,dd,...';


--
-- Name: COLUMN obs_monthly.min_min_ground_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.min_min_ground_temp IS 'Lowest minimum daily ground temp (C to 0.1)';


--
-- Name: COLUMN obs_monthly.min_min_ground_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.min_min_ground_temp_f IS 'Lowest minimum daily ground temp (F to 0.1)';


--
-- Name: COLUMN obs_monthly.min_min_ground_temp_date; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.min_min_ground_temp_date IS 'Date(s) of lowest daily ground min as dd,dd,dd,...';


--
-- Name: COLUMN obs_monthly.mn_air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_air_temp IS 'Mean air temperature (C to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_air_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_air_temp_f IS 'Mean air temperature (F to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_max_air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_max_air_temp IS 'Mean of maximum daily air temp (C to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_max_air_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_max_air_temp_f IS 'Mean of maximum daily air temp (F to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_min_air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_min_air_temp IS 'Mean of minimum daily air temp (C to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_min_air_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_min_air_temp_f IS 'Mean of minimum daily air temp (F to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_wet_bulb_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_wet_bulb_temp IS 'Mean wet bulb temperature (C to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_wet_bulb_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_wet_bulb_temp_f IS 'Mean wet bulb temperature (F to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_min_ground_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_min_ground_temp IS 'Mean of minimum daily ground temp (C to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_min_ground_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_min_ground_temp_f IS 'Mean of minimum daily ground temp (F to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_asread_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_asread_pres IS 'Mean as read pressure (hPa to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_asread_pres_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_asread_pres_inches IS 'Mean as read pressure (inches to 0.001)';


--
-- Name: COLUMN obs_monthly.mn_asread_pres_mmhg; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_asread_pres_mmhg IS 'Mean as read pressure (mmHg to 0.01)';


--
-- Name: COLUMN obs_monthly.mn_msl_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_msl_pres IS 'Mean MSL pressure (hPa to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_msl_pres_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_msl_pres_inches IS 'Mean MSL pressure (inches to 0.001)';


--
-- Name: COLUMN obs_monthly.mn_msl_pres_mmhg; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_msl_pres_mmhg IS 'Mean MSL pressure (mmHg to 0.01)';


--
-- Name: COLUMN obs_monthly.mn_station_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_station_pres IS 'Mean station level pressure (hPa to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_station_pres_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_station_pres_inches IS 'Mean station level pressure (inches to 0.001)';


--
-- Name: COLUMN obs_monthly.mn_station_pres_mmhg; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_station_pres_mmhg IS 'Mean station level pressure (mmHg to 0.01)';


--
-- Name: COLUMN obs_monthly.mn_vapour_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_vapour_pres IS 'Mean Vapour Pressure (hPa to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_vapour_pres_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_vapour_pres_inches IS 'Mean Vapour Pressure (Inches to 0.001)';


--
-- Name: COLUMN obs_monthly.mn_vapour_pres_mmhg; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_vapour_pres_mmhg IS 'Mean Vapour Pressure (mmHg to 0.01)';


--
-- Name: COLUMN obs_monthly.mn_evaporation; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_evaporation IS 'Mean of daily evaporation (mm to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_evaporation_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_evaporation_inches IS 'Mean of daily evaporation (Inches to 0.001)';


--
-- Name: COLUMN obs_monthly.mn_rel_humidity; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_rel_humidity IS 'Mean Relative Humidity (% to 0.1)';


--
-- Name: COLUMN obs_monthly.mn_sun_hours; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_sun_hours IS 'Mean of daily bright sunshine (hours to 0.01)';


--
-- Name: COLUMN obs_monthly.mn_tot_cloud_oktas; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_tot_cloud_oktas IS 'Mean of Daily Total Cloud Amt (Octas 0-9)';


--
-- Name: COLUMN obs_monthly.mn_tot_cloud_tenths; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.mn_tot_cloud_tenths IS 'Mean of Daily Total Cloud Amt (Tenths 0-10)';


--
-- Name: COLUMN obs_monthly.tot_evaporation; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.tot_evaporation IS 'Total Monthly evaporation (mm to 0.1)';


--
-- Name: COLUMN obs_monthly.tot_evaporation_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.tot_evaporation_inches IS 'Total Monthly evaporation (Inches to 0.001)';


--
-- Name: COLUMN obs_monthly.tot_rain; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.tot_rain IS 'Total monthly precipitation  (mm to 0.1)';


--
-- Name: COLUMN obs_monthly.tot_rain_inches; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.tot_rain_inches IS 'Total monthly precipitation  (Inches to 0.001)';


--
-- Name: COLUMN obs_monthly.tot_rain_days; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.tot_rain_days IS 'Number of rain days';


--
-- Name: COLUMN obs_monthly.tot_rain_percent; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_monthly.tot_rain_percent IS 'Percentage complete (not missing) of daily records for month';


--
-- Name: ext_obs_monthly; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_obs_monthly AS
    SELECT obs_monthly.id, obs_monthly.station_no, obs_monthly.lsd, obs_monthly.data_source, obs_monthly.insert_datetime, obs_monthly.change_datetime, obs_monthly.change_user, obs_monthly.qa_flag, obs_monthly.comments, obs_monthly.dly_max_rain, obs_monthly.dly_max_rain_inches, obs_monthly.dly_max_rain_date, obs_monthly.dly_max_rain_qa, obs_monthly.max_max_air_temp, obs_monthly.max_max_air_temp_f, obs_monthly.max_max_air_temp_qa, obs_monthly.max_max_air_temp_date, obs_monthly.min_min_air_temp, obs_monthly.min_min_air_temp_f, obs_monthly.min_min_air_temp_qa, obs_monthly.min_min_air_temp_date, obs_monthly.min_min_ground_temp, obs_monthly.min_min_ground_temp_f, obs_monthly.min_min_ground_temp_qa, obs_monthly.min_min_ground_temp_date, obs_monthly.mn_air_temp, obs_monthly.mn_air_temp_f, obs_monthly.mn_air_temp_qa, obs_monthly.mn_max_air_temp, obs_monthly.mn_max_air_temp_f, obs_monthly.mn_max_air_temp_qa, obs_monthly.mn_min_air_temp, obs_monthly.mn_min_air_temp_f, obs_monthly.mn_min_air_temp_qa, obs_monthly.mn_wet_bulb_temp, obs_monthly.mn_wet_bulb_temp_f, obs_monthly.mn_wet_bulb_temp_qa, obs_monthly.mn_min_ground_temp, obs_monthly.mn_min_ground_temp_f, obs_monthly.mn_min_ground_temp_qa, obs_monthly.mn_asread_pres, obs_monthly.mn_asread_pres_inches, obs_monthly.mn_asread_pres_mmhg, obs_monthly.mn_asread_pres_qa, obs_monthly.mn_msl_pres, obs_monthly.mn_msl_pres_inches, obs_monthly.mn_msl_pres_mmhg, obs_monthly.mn_msl_pres_qa, obs_monthly.mn_station_pres, obs_monthly.mn_station_pres_inches, obs_monthly.mn_station_pres_mmhg, obs_monthly.mn_station_pres_qa, obs_monthly.mn_vapour_pres, obs_monthly.mn_vapour_pres_inches, obs_monthly.mn_vapour_pres_mmhg, obs_monthly.mn_vapour_pres_qa, obs_monthly.mn_evaporation, obs_monthly.mn_evaporation_inches, obs_monthly.mn_evaporation_qa, obs_monthly.mn_rel_humidity, obs_monthly.mn_rel_humidity_qa, obs_monthly.mn_sun_hours, obs_monthly.mn_sun_hours_qa, obs_monthly.mn_tot_cloud_oktas, obs_monthly.mn_tot_cloud_tenths, obs_monthly.mn_tot_cloud_qa, obs_monthly.tot_evaporation, obs_monthly.tot_evaporation_inches, obs_monthly.tot_evaporation_qa, obs_monthly.tot_rain, obs_monthly.tot_rain_inches, obs_monthly.tot_rain_qa, obs_monthly.tot_rain_days, obs_monthly.tot_rain_days_qa, obs_monthly.tot_rain_percent, obs_monthly.tot_rain_percent_qa FROM obs_monthly;


ALTER TABLE public.ext_obs_monthly OWNER TO clidegui;

--
-- Name: ext_obs_monthly_calculated; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_obs_monthly_calculated AS
    SELECT daily.station_no, daily.lsd_month AS lsd, daily.yyyy_mm, daily.max_max_air_temp, daily.min_min_air_temp, daily.min_min_ground_temp, daily.mn_min_ground_temp, daily.mn_max_air_temp, daily.mn_min_air_temp, daily.mn_air_temp, daily.dly_max_rain, daily.tot_rain, daily.tot_rain_days, (((daily.missing_count)::double precision / daily.days_in_month) * (100)::double precision) AS tot_rain_percent, daily.mn_evaporation, daily.tot_evaporation, daily.mn_sun_hours, subdaily.mn_asread_pres, subdaily.mn_msl_pres, subdaily.mn_station_pres, subdaily.mn_vapour_pres, subdaily.mn_rel_humidity, subdaily.mn_tot_cloud_oktas FROM ((SELECT obs_daily.station_no, to_char(obs_daily.lsd, 'yyyy-mm'::text) AS yyyy_mm, (date_trunc('month'::text, obs_daily.lsd))::date AS lsd_month, max(obs_daily.max_air_temp) AS max_max_air_temp, min(obs_daily.min_air_temp) AS min_min_air_temp, min(obs_daily.ground_temp) AS min_min_ground_temp, avg(obs_daily.ground_temp) AS mn_min_ground_temp, avg(obs_daily.max_air_temp) AS mn_max_air_temp, avg(obs_daily.min_air_temp) AS mn_min_air_temp, avg(((obs_daily.max_air_temp + obs_daily.min_air_temp) / (2)::numeric)) AS mn_air_temp, max(obs_daily.rain_24h) AS dly_max_rain, sum(obs_daily.rain_24h) AS tot_rain, sum(obs_daily.rain_24h_count) AS tot_rain_days, date_part('day'::text, (((((("substring"(to_char(obs_daily.lsd, 'yyyy-mm'::text), 1, 4) || '-'::text) || "substring"(to_char(obs_daily.lsd, 'yyyy-mm'::text), 6, 2)) || '-01'::text))::date + '1 mon'::interval) - '1 day'::interval)) AS days_in_month, sum(CASE WHEN (obs_daily.rain_24h_qa = '00'::bpchar) THEN 1 ELSE 0 END) AS missing_count, avg(obs_daily.evaporation) AS mn_evaporation, sum(obs_daily.evaporation) AS tot_evaporation, avg(obs_daily.sunshine_duration) AS mn_sun_hours FROM obs_daily GROUP BY obs_daily.station_no, to_char(obs_daily.lsd, 'yyyy-mm'::text), (date_trunc('month'::text, obs_daily.lsd))::date) daily JOIN (SELECT obs_subdaily.station_no, to_char(obs_subdaily.lsd, 'yyyy-mm'::text) AS yyyy_mm, (date_trunc('month'::text, obs_subdaily.lsd))::date AS lsd_month, avg(obs_subdaily.pres_as_read) AS mn_asread_pres, avg(obs_subdaily.msl_pres) AS mn_msl_pres, avg(obs_subdaily.station_pres) AS mn_station_pres, avg(obs_subdaily.vapour_pres) AS mn_vapour_pres, avg(obs_subdaily.rel_humidity) AS mn_rel_humidity, avg(obs_subdaily.tot_cloud_oktas) AS mn_tot_cloud_oktas FROM obs_subdaily GROUP BY obs_subdaily.station_no, to_char(obs_subdaily.lsd, 'yyyy-mm'::text), (date_trunc('month'::text, obs_subdaily.lsd))::date) subdaily ON ((((daily.station_no)::text = (subdaily.station_no)::text) AND (daily.yyyy_mm = subdaily.yyyy_mm))));


ALTER TABLE public.ext_obs_monthly_calculated OWNER TO clidegui;

--
-- Name: ext_obs_monthly_combined; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_obs_monthly_combined AS
    SELECT 'RAW' AS source, ext_obs_monthly_calculated.station_no, ext_obs_monthly_calculated.yyyy_mm, ext_obs_monthly_calculated.lsd, ext_obs_monthly_calculated.max_max_air_temp, ext_obs_monthly_calculated.min_min_air_temp, ext_obs_monthly_calculated.min_min_ground_temp, ext_obs_monthly_calculated.mn_min_ground_temp, ext_obs_monthly_calculated.mn_max_air_temp, ext_obs_monthly_calculated.mn_min_air_temp, ext_obs_monthly_calculated.mn_air_temp, ext_obs_monthly_calculated.dly_max_rain, ext_obs_monthly_calculated.tot_rain, ext_obs_monthly_calculated.tot_rain_days, ext_obs_monthly_calculated.tot_rain_percent, ext_obs_monthly_calculated.mn_evaporation, ext_obs_monthly_calculated.tot_evaporation, ext_obs_monthly_calculated.mn_sun_hours, ext_obs_monthly_calculated.mn_asread_pres, ext_obs_monthly_calculated.mn_msl_pres, ext_obs_monthly_calculated.mn_station_pres, ext_obs_monthly_calculated.mn_vapour_pres, ext_obs_monthly_calculated.mn_rel_humidity, ext_obs_monthly_calculated.mn_tot_cloud_oktas FROM ext_obs_monthly_calculated UNION ALL SELECT 'KEY' AS source, obs_monthly.station_no, to_char((obs_monthly.lsd)::timestamp with time zone, 'yyyy-mm'::text) AS yyyy_mm, (date_trunc('month'::text, (obs_monthly.lsd)::timestamp with time zone))::date AS lsd, obs_monthly.max_max_air_temp, obs_monthly.min_min_air_temp, obs_monthly.min_min_ground_temp, obs_monthly.mn_min_ground_temp, obs_monthly.mn_max_air_temp, obs_monthly.mn_min_air_temp, obs_monthly.mn_air_temp, obs_monthly.dly_max_rain, obs_monthly.tot_rain, obs_monthly.tot_rain_days, obs_monthly.tot_rain_percent, obs_monthly.mn_evaporation, obs_monthly.tot_evaporation, obs_monthly.mn_sun_hours, obs_monthly.mn_asread_pres, obs_monthly.mn_msl_pres, obs_monthly.mn_station_pres, obs_monthly.mn_vapour_pres, obs_monthly.mn_rel_humidity, obs_monthly.mn_tot_cloud_oktas FROM obs_monthly ORDER BY 4, 2;


ALTER TABLE public.ext_obs_monthly_combined OWNER TO clidegui;

--
-- Name: ext_obs_subdaily; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_obs_subdaily AS
    SELECT obs_subdaily.id, obs_subdaily.station_no, obs_subdaily.lsd, obs_subdaily.gmt, obs_subdaily.lct, obs_subdaily.data_source, obs_subdaily.insert_datetime, obs_subdaily.change_datetime, obs_subdaily.change_user, obs_subdaily.qa_flag, obs_subdaily.aws_flag, obs_subdaily.comments, obs_subdaily.air_temp, obs_subdaily.air_temp_f, obs_subdaily.air_temp_qa, obs_subdaily.sea_water_temp, obs_subdaily.sea_water_temp_f, obs_subdaily.sea_water_temp_qa, obs_subdaily.wet_bulb, obs_subdaily.wet_bulb_f, obs_subdaily.wet_bulb_qa, obs_subdaily.dew_point, obs_subdaily.dew_point_f, obs_subdaily.dew_point_qa, obs_subdaily.rel_humidity, obs_subdaily.rel_humidity_qa, obs_subdaily.baro_temp, obs_subdaily.baro_temp_f, obs_subdaily.baro_temp_qa, obs_subdaily.pres_as_read, obs_subdaily.pres_as_read_inches, obs_subdaily.pres_as_read_qa, obs_subdaily.station_pres, obs_subdaily.station_pres_inches, obs_subdaily.station_pres_qa, obs_subdaily.msl_pres, obs_subdaily.msl_pres_inches, obs_subdaily.msl_pres_qa, obs_subdaily.vapour_pres, obs_subdaily.vapour_pres_inches, obs_subdaily.vapour_pres_qa, obs_subdaily.qnh, obs_subdaily.qnh_qa, obs_subdaily.visibility, obs_subdaily.visibility_miles, obs_subdaily.visibility_code, obs_subdaily.visibility_qa, obs_subdaily.rain_3h, obs_subdaily.rain_3h_inches, obs_subdaily.rain_3h_qa, obs_subdaily.rain_3h_hours, obs_subdaily.rain_cum, obs_subdaily.rain_cum_inches, obs_subdaily.rain_cum_qa, obs_subdaily.wind_dir, obs_subdaily.wind_dir_qa, obs_subdaily.wind_dir_std_dev, obs_subdaily.wind_dir_std_dev_qa, obs_subdaily.wind_speed, obs_subdaily.wind_speed_knots, obs_subdaily.wind_speed_mph, obs_subdaily.wind_speed_bft, obs_subdaily.wind_speed_qa, obs_subdaily.pres_weather_code, obs_subdaily.pres_weather_bft, obs_subdaily.pres_weather_qa, obs_subdaily.past_weather_code, obs_subdaily.past_weather_bft, obs_subdaily.past_weather_qa, obs_subdaily.tot_cloud_oktas, obs_subdaily.tot_cloud_tenths, obs_subdaily.tot_cloud_qa, obs_subdaily.tot_low_cloud_oktas, obs_subdaily.tot_low_cloud_tenths, obs_subdaily.tot_low_cloud_height, obs_subdaily.tot_low_cloud_qa, obs_subdaily.state_of_sea, obs_subdaily.state_of_sea_qa, obs_subdaily.state_of_swell, obs_subdaily.state_of_swell_qa, obs_subdaily.swell_direction, obs_subdaily.swell_direction_qa, obs_subdaily.sea_level, obs_subdaily.sea_level_qa, obs_subdaily.sea_level_residual, obs_subdaily.sea_level_residual_qa, obs_subdaily.sea_level_resid_adj, obs_subdaily.sea_level_resid_adj_qa, obs_subdaily.radiation, obs_subdaily.radiation_qa, obs_subdaily.sunshine, obs_subdaily.sunshine_qa, obs_subdaily.tot_low_cloud_height_feet, obs_subdaily.wind_gust_kts, obs_subdaily.wind_gust, obs_subdaily.wind_gust_qa, obs_subdaily.wind_gust_dir, obs_subdaily.wind_gust_dir_qa FROM obs_subdaily ORDER BY obs_subdaily.station_no, obs_subdaily.lsd;


ALTER TABLE public.ext_obs_subdaily OWNER TO clidegui;

--
-- Name: obs_subdaily_cloud_layers_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obs_subdaily_cloud_layers_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obs_subdaily_cloud_layers_id OWNER TO clidegui;

--
-- Name: SEQUENCE obs_subdaily_cloud_layers_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obs_subdaily_cloud_layers_id IS 'PK sequence for obs_subdaily_cloud_layers';


--
-- Name: obs_subdaily_cloud_layers; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obs_subdaily_cloud_layers (
    id integer DEFAULT nextval('obs_subdaily_cloud_layers_id'::regclass) NOT NULL,
    sub_daily_id integer NOT NULL,
    data_source character(2) DEFAULT '1'::bpchar NOT NULL,
    insert_datetime timestamp without time zone DEFAULT now() NOT NULL,
    change_datetime timestamp without time zone,
    change_user character varying(20),
    qa_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    aws_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    layer_no integer NOT NULL,
    layer_type character varying(6),
    cloud_oktas smallint,
    cloud_tenths smallint,
    cloud_amt_qa character(2),
    cloud_type character varying(2),
    cloud_type_qa character(2),
    cloud_height numeric(6,0),
    cloud_height_feet numeric(7,0),
    cloud_height_qa character(2),
    cloud_dir numeric(3,0),
    cloud_dir_qa character(2)
);


ALTER TABLE public.obs_subdaily_cloud_layers OWNER TO clidegui;

--
-- Name: TABLE obs_subdaily_cloud_layers; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obs_subdaily_cloud_layers IS 'Sub Daily surface observations';


--
-- Name: COLUMN obs_subdaily_cloud_layers.sub_daily_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_cloud_layers.sub_daily_id IS 'Surrogate key of parent sub daily row';


--
-- Name: COLUMN obs_subdaily_cloud_layers.layer_no; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_cloud_layers.layer_no IS 'layer number. (1,2,3,n)';


--
-- Name: COLUMN obs_subdaily_cloud_layers.layer_type; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_cloud_layers.layer_type IS 'Low, Mid, High';


--
-- Name: COLUMN obs_subdaily_cloud_layers.cloud_oktas; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_cloud_layers.cloud_oktas IS 'Cloud  amount in octas (0-9)';


--
-- Name: COLUMN obs_subdaily_cloud_layers.cloud_tenths; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_cloud_layers.cloud_tenths IS 'Cloud  amount in tenths (0-10)';


--
-- Name: COLUMN obs_subdaily_cloud_layers.cloud_amt_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_cloud_layers.cloud_amt_qa IS 'Quality Code for clout_amt';


--
-- Name: COLUMN obs_subdaily_cloud_layers.cloud_type; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_cloud_layers.cloud_type IS 'Cloud type, WMO code';


--
-- Name: COLUMN obs_subdaily_cloud_layers.cloud_type_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_cloud_layers.cloud_type_qa IS 'Quality Code for cloud_type';


--
-- Name: COLUMN obs_subdaily_cloud_layers.cloud_height; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_cloud_layers.cloud_height IS 'Cloud height in Meters (M to 1.0)';


--
-- Name: COLUMN obs_subdaily_cloud_layers.cloud_height_feet; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_cloud_layers.cloud_height_feet IS 'Cloud height in feet (feet to 1.0)';


--
-- Name: COLUMN obs_subdaily_cloud_layers.cloud_height_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_cloud_layers.cloud_height_qa IS 'Quality Code for cloud_height';


--
-- Name: COLUMN obs_subdaily_cloud_layers.cloud_dir; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_cloud_layers.cloud_dir IS 'Cloud movement Direction (0-360)';


--
-- Name: COLUMN obs_subdaily_cloud_layers.cloud_dir_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_cloud_layers.cloud_dir_qa IS 'Quality Code for cloud_dir';


--
-- Name: ext_obs_subdaily_cloud_layers; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_obs_subdaily_cloud_layers AS
    SELECT s.station_no, s.lsd, scl.layer_no, scl.layer_type, scl.cloud_oktas, scl.cloud_tenths, scl.cloud_amt_qa, scl.cloud_type, scl.cloud_type_qa, scl.cloud_height, scl.cloud_height_feet, scl.cloud_height_qa, scl.cloud_dir, scl.cloud_dir_qa, scl.data_source, scl.insert_datetime, scl.change_datetime, scl.change_user, scl.qa_flag, scl.aws_flag FROM (obs_subdaily s JOIN obs_subdaily_cloud_layers scl ON ((scl.sub_daily_id = s.id))) ORDER BY s.station_no, s.lsd, scl.layer_no;


ALTER TABLE public.ext_obs_subdaily_cloud_layers OWNER TO clidegui;

--
-- Name: obs_subdaily_soil_temps_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obs_subdaily_soil_temps_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obs_subdaily_soil_temps_id OWNER TO clidegui;

--
-- Name: SEQUENCE obs_subdaily_soil_temps_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obs_subdaily_soil_temps_id IS 'PK sequence for obs_subdaily_soil_temps';


--
-- Name: obs_subdaily_soil_temps; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obs_subdaily_soil_temps (
    id integer DEFAULT nextval('obs_subdaily_soil_temps_id'::regclass) NOT NULL,
    sub_daily_id integer NOT NULL,
    data_source character(2) DEFAULT '1'::bpchar NOT NULL,
    insert_datetime timestamp without time zone DEFAULT now() NOT NULL,
    change_datetime timestamp without time zone,
    change_user character varying(20),
    qa_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    aws_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    soil_depth numeric(5,0) NOT NULL,
    soil_temp numeric(7,1),
    soil_temp_f numeric(7,1),
    soil_temp_qa character(2)
);


ALTER TABLE public.obs_subdaily_soil_temps OWNER TO clidegui;

--
-- Name: TABLE obs_subdaily_soil_temps; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obs_subdaily_soil_temps IS 'Sub Daily surface observations';


--
-- Name: COLUMN obs_subdaily_soil_temps.sub_daily_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_soil_temps.sub_daily_id IS 'Surrogate key of parent sub daily row';


--
-- Name: COLUMN obs_subdaily_soil_temps.soil_depth; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_soil_temps.soil_depth IS 'Soil depth in cm';


--
-- Name: COLUMN obs_subdaily_soil_temps.soil_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_soil_temps.soil_temp IS 'Soil Temperature (C to 0.1)';


--
-- Name: COLUMN obs_subdaily_soil_temps.soil_temp_f; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_soil_temps.soil_temp_f IS 'Soil Temperature (F to 0.1)';


--
-- Name: COLUMN obs_subdaily_soil_temps.soil_temp_qa; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_subdaily_soil_temps.soil_temp_qa IS 'Quality Code for soil_temp';


--
-- Name: ext_obs_subdaily_soil_temps; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_obs_subdaily_soil_temps AS
    SELECT s.station_no, s.lsd, sst.soil_depth, sst.soil_temp, sst.soil_temp_f, sst.soil_temp_qa, sst.change_user, sst.insert_datetime, sst.change_datetime, sst.qa_flag, sst.aws_flag FROM (obs_subdaily s JOIN obs_subdaily_soil_temps sst ON ((sst.sub_daily_id = s.id))) ORDER BY s.station_no, s.lsd, sst.soil_depth;


ALTER TABLE public.ext_obs_subdaily_soil_temps OWNER TO clidegui;

--
-- Name: obs_upper_air_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obs_upper_air_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obs_upper_air_id OWNER TO clidegui;

--
-- Name: SEQUENCE obs_upper_air_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obs_upper_air_id IS 'PK sequence for obs_upper_air';


--
-- Name: obs_upper_air; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obs_upper_air (
    id integer DEFAULT nextval('obs_upper_air_id'::regclass) NOT NULL,
    station_no character varying(15) NOT NULL,
    lsd timestamp without time zone NOT NULL,
    gmt timestamp without time zone,
    lct timestamp without time zone,
    data_source character(2) NOT NULL,
    insert_datetime timestamp without time zone NOT NULL,
    change_datetime timestamp without time zone,
    change_user character varying(20),
    qa_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    pressure numeric(7,1) NOT NULL,
    pressure_qa character(2),
    level_type numeric(2,0),
    geo_height numeric(8,1),
    geo_height_qa character(2),
    air_temp numeric(7,1),
    air_temp_qa character(2),
    dew_point numeric(4,1),
    dew_point_qa character(2),
    wind_direction numeric(4,0),
    wind_direction_qa character(2),
    wind_speed numeric(5,1),
    wind_speed_qa character(2)
);


ALTER TABLE public.obs_upper_air OWNER TO clidegui;

--
-- Name: TABLE obs_upper_air; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obs_upper_air IS 'Upper Air observations';


--
-- Name: COLUMN obs_upper_air.station_no; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.station_no IS 'Local Station identifier';


--
-- Name: COLUMN obs_upper_air.lsd; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.lsd IS 'Local System Time (No Daylight Savings)';


--
-- Name: COLUMN obs_upper_air.gmt; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.gmt IS 'GMT (UTC+0)';


--
-- Name: COLUMN obs_upper_air.lct; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.lct IS 'Local Clock Time (With Daylight Savings)';


--
-- Name: COLUMN obs_upper_air.data_source; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.data_source IS 'Code for data source (Ref Table??)';


--
-- Name: COLUMN obs_upper_air.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.insert_datetime IS 'Date/time row is inserted';


--
-- Name: COLUMN obs_upper_air.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.change_datetime IS 'Date/time row is changed';


--
-- Name: COLUMN obs_upper_air.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.change_user IS 'User who added/changed row';


--
-- Name: COLUMN obs_upper_air.qa_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.qa_flag IS 'QA flag for row (Y/N)';


--
-- Name: COLUMN obs_upper_air.pressure; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.pressure IS 'Pressure (hPa to 0.1)';


--
-- Name: COLUMN obs_upper_air.level_type; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.level_type IS 'Level type (0,1,n)';


--
-- Name: COLUMN obs_upper_air.geo_height; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.geo_height IS 'Meters';


--
-- Name: COLUMN obs_upper_air.air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.air_temp IS 'Temperature (C to 0.1)';


--
-- Name: COLUMN obs_upper_air.dew_point; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.dew_point IS 'Dew Point Temperature (C to 0.1)';


--
-- Name: COLUMN obs_upper_air.wind_direction; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.wind_direction IS 'Direction (0-360 degrees)';


--
-- Name: COLUMN obs_upper_air.wind_speed; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_upper_air.wind_speed IS 'Wind Speed (M/s to 0.1)';


--
-- Name: ext_obs_upper_air; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_obs_upper_air AS
    SELECT obs_upper_air.id, obs_upper_air.station_no, obs_upper_air.lsd, obs_upper_air.gmt, obs_upper_air.lct, obs_upper_air.data_source, obs_upper_air.insert_datetime, obs_upper_air.change_datetime, obs_upper_air.change_user, obs_upper_air.qa_flag, obs_upper_air.pressure, obs_upper_air.pressure_qa, obs_upper_air.level_type, obs_upper_air.geo_height, obs_upper_air.geo_height_qa, obs_upper_air.air_temp, obs_upper_air.air_temp_qa, obs_upper_air.dew_point, obs_upper_air.dew_point_qa, obs_upper_air.wind_direction, obs_upper_air.wind_direction_qa, obs_upper_air.wind_speed, obs_upper_air.wind_speed_qa FROM obs_upper_air ORDER BY obs_upper_air.station_no, obs_upper_air.lsd;


ALTER TABLE public.ext_obs_upper_air OWNER TO clidegui;

--
-- Name: station_audit_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE station_audit_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.station_audit_id OWNER TO clidegui;

--
-- Name: SEQUENCE station_audit_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE station_audit_id IS 'PK sequence for station audit';


--
-- Name: station_audit; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE station_audit (
    id integer DEFAULT nextval('station_audit_id'::regclass) NOT NULL,
    station_id integer,
    datetime timestamp with time zone,
    event_datetime timestamp with time zone DEFAULT now(),
    audit_type_id integer NOT NULL,
    description character varying(1000),
    event_user character varying(40)
);


ALTER TABLE public.station_audit OWNER TO clidegui;

--
-- Name: TABLE station_audit; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE station_audit IS 'Audit trail of all changes to station Station.';


--
-- Name: COLUMN station_audit.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_audit.id IS 'Surrogate Key';


--
-- Name: COLUMN station_audit.station_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_audit.station_id IS 'Station ID of audit record';


--
-- Name: COLUMN station_audit.datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_audit.datetime IS 'Date/Time of event being recorded';


--
-- Name: COLUMN station_audit.audit_type_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_audit.audit_type_id IS 'Audit Type ID. Joins to station_audit_type';


--
-- Name: COLUMN station_audit.description; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_audit.description IS 'Description of audit event';


--
-- Name: COLUMN station_audit.event_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_audit.event_user IS 'User performing the auditable event';


--
-- Name: station_audit_type_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE station_audit_type_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.station_audit_type_id OWNER TO clidegui;

--
-- Name: SEQUENCE station_audit_type_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE station_audit_type_id IS 'PK sequence for station audit type';


--
-- Name: station_audit_types; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE station_audit_types (
    id integer DEFAULT nextval('station_audit_type_id'::regclass) NOT NULL,
    audit_type character varying(10) NOT NULL,
    description character varying(50),
    system_type character(1) DEFAULT 'N'::bpchar NOT NULL
);


ALTER TABLE public.station_audit_types OWNER TO clidegui;

--
-- Name: TABLE station_audit_types; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE station_audit_types IS 'Stores allowed values for station_audit.type_id';


--
-- Name: COLUMN station_audit_types.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_audit_types.id IS 'Surrogate Key';


--
-- Name: COLUMN station_audit_types.audit_type; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_audit_types.audit_type IS 'Audit type code';


--
-- Name: COLUMN station_audit_types.description; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_audit_types.description IS 'Description of audit type';


--
-- Name: stations_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE stations_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stations_id OWNER TO clidegui;

--
-- Name: SEQUENCE stations_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE stations_id IS 'PK sequence for stations';


--
-- Name: stations; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE stations (
    id integer DEFAULT nextval('stations_id'::regclass) NOT NULL,
    station_no character varying(15) NOT NULL,
    status_id integer NOT NULL,
    time_zone character varying(3) NOT NULL,
    id_aero character varying(10),
    id_imo character varying(10),
    id_marine character varying(10),
    id_wmo character varying(10),
    id_hydro character varying(10),
    id_aust character varying(10),
    id_niwa character varying(10),
    id_niwa_agent character varying(10),
    comments character varying(1000),
    country_code character varying(4),
    start_date date,
    end_date date,
    ht_aero numeric(6,1),
    ht_elev numeric(7,3),
    ht_ssb numeric(7,4),
    latitude numeric(8,4),
    longitude numeric(8,4),
    name_primary character varying(40),
    name_secondary character varying(40),
    region character varying(40),
    catchment character varying(40),
    authority character varying(50),
    lu_0_100m integer,
    lu_100m_1km integer,
    lu_1km_10km integer,
    soil_type integer,
    surface_type integer,
    critical_river_height numeric(7,3),
    location_datum character varying(20),
    location_epsg integer
);


ALTER TABLE public.stations OWNER TO clidegui;

--
-- Name: TABLE stations; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE stations IS 'Stores station data.';


--
-- Name: COLUMN stations.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN stations.id IS 'Surrogate Key';


--
-- Name: COLUMN stations.status_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN stations.status_id IS 'Station status ID joins to station_status';


--
-- Name: COLUMN stations.critical_river_height; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN stations.critical_river_height IS 'Critical River height (eg. Flood level) in M';


--
-- Name: ext_station_audit; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_station_audit AS
    SELECT s.station_no, s.name_primary AS station_name, sa.datetime, sa.audit_type_id, sat.description AS audit_type_description, (('"'::text || (sa.description)::text) || '"'::text) AS event_description, sa.event_user AS "user" FROM ((station_audit sa JOIN stations s ON ((s.id = sa.station_id))) JOIN station_audit_types sat ON ((sat.id = sa.audit_type_id))) ORDER BY s.station_no, sa.datetime;


ALTER TABLE public.ext_station_audit OWNER TO clidegui;

--
-- Name: station_class_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE station_class_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.station_class_id OWNER TO clidegui;

--
-- Name: SEQUENCE station_class_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE station_class_id IS 'PK sequence for station class';


--
-- Name: station_class; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE station_class (
    id integer DEFAULT nextval('station_class_id'::regclass) NOT NULL,
    station_id integer NOT NULL,
    type_id integer,
    description character varying(80),
    class_start timestamp without time zone,
    class_end timestamp without time zone
);


ALTER TABLE public.station_class OWNER TO clidegui;

--
-- Name: TABLE station_class; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE station_class IS 'Stores contacts (people) for station';


--
-- Name: COLUMN station_class.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_class.id IS 'Surrogate Key';


--
-- Name: COLUMN station_class.station_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_class.station_id IS 'Station ID of station class';


--
-- Name: COLUMN station_class.type_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_class.type_id IS 'ID of Type for this class';


--
-- Name: COLUMN station_class.class_start; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_class.class_start IS 'Date this class started for the station.';


--
-- Name: COLUMN station_class.class_end; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_class.class_end IS 'Date this class ended for the station.';


--
-- Name: ext_station_class; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_station_class AS
    SELECT s.station_no, s.name_primary AS station_name, t.station_type AS class, t.description AS class_description, sc.class_start, sc.class_end, sc.description FROM ((stations s JOIN station_class sc ON ((sc.station_id = s.id))) JOIN station_types t ON ((sc.type_id = t.id))) ORDER BY s.station_no, t.station_type;


ALTER TABLE public.ext_station_class OWNER TO clidegui;

--
-- Name: station_equipment_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE station_equipment_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.station_equipment_id OWNER TO clidegui;

--
-- Name: SEQUENCE station_equipment_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE station_equipment_id IS 'PK sequence for station equipment';


--
-- Name: station_equipment; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE station_equipment (
    id integer DEFAULT nextval('station_equipment_id'::regclass) NOT NULL,
    station_id integer NOT NULL,
    equipment_id integer,
    serial_no character varying(50),
    asset_id character varying(50),
    height numeric(7,3),
    comments character varying(1000),
    date_start date,
    date_end date
);


ALTER TABLE public.station_equipment OWNER TO clidegui;

--
-- Name: TABLE station_equipment; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE station_equipment IS 'Stores equipment installed at station.';


--
-- Name: COLUMN station_equipment.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_equipment.id IS 'Surrogate Key';


--
-- Name: COLUMN station_equipment.station_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_equipment.station_id IS 'ID of station';


--
-- Name: COLUMN station_equipment.serial_no; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_equipment.serial_no IS 'Serial no of equipment';


--
-- Name: COLUMN station_equipment.asset_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_equipment.asset_id IS 'Asset code of equipment';


--
-- Name: COLUMN station_equipment.comments; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_equipment.comments IS 'Comments for equipment';


--
-- Name: COLUMN station_equipment.date_start; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_equipment.date_start IS 'Date of installation';


--
-- Name: COLUMN station_equipment.date_end; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_equipment.date_end IS 'Date of decomissioning or removal';


--
-- Name: ext_station_equipment; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_station_equipment AS
    SELECT s.station_no, s.name_primary AS station_name, e.type AS equipment_type, e.version AS equipment_version, e.comments AS equipment_comments, se.serial_no, se.asset_id, se.height, se.date_start, se.date_end, se.comments FROM ((stations s JOIN station_equipment se ON ((se.station_id = s.id))) JOIN equipment e ON ((se.equipment_id = e.id))) ORDER BY s.station_no, e.type;


ALTER TABLE public.ext_station_equipment OWNER TO clidegui;

--
-- Name: land_use_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE land_use_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.land_use_id OWNER TO clidegui;

--
-- Name: SEQUENCE land_use_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE land_use_id IS 'PK sequence for land use';


--
-- Name: land_use; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE land_use (
    id integer DEFAULT nextval('land_use_id'::regclass) NOT NULL,
    land_use_code character varying(10) NOT NULL,
    priority integer NOT NULL,
    description character varying(100)
);


ALTER TABLE public.land_use OWNER TO clidegui;

--
-- Name: TABLE land_use; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE land_use IS 'Stores allowed values for stations.soil_type_id';


--
-- Name: COLUMN land_use.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN land_use.id IS 'Surrogate Key';


--
-- Name: COLUMN land_use.land_use_code; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN land_use.land_use_code IS 'Land usage code';


--
-- Name: COLUMN land_use.priority; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN land_use.priority IS 'Land usage priority';


--
-- Name: COLUMN land_use.description; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN land_use.description IS 'Land use description';


--
-- Name: soil_types_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE soil_types_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.soil_types_id OWNER TO clidegui;

--
-- Name: SEQUENCE soil_types_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE soil_types_id IS 'PK sequence for soil types';


--
-- Name: soil_types; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE soil_types (
    id integer DEFAULT nextval('soil_types_id'::regclass) NOT NULL,
    soil_type character varying(10) NOT NULL,
    description character varying(50)
);


ALTER TABLE public.soil_types OWNER TO clidegui;

--
-- Name: TABLE soil_types; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE soil_types IS 'Stores allowed values for stations.soil_type_id';


--
-- Name: COLUMN soil_types.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN soil_types.id IS 'Surrogate Key';


--
-- Name: COLUMN soil_types.soil_type; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN soil_types.soil_type IS 'Soil type code';


--
-- Name: COLUMN soil_types.description; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN soil_types.description IS 'Soil type description';


--
-- Name: station_countries_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE station_countries_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.station_countries_id OWNER TO clidegui;

--
-- Name: SEQUENCE station_countries_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE station_countries_id IS 'PK sequence for station countries';


--
-- Name: station_countries; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE station_countries (
    id integer DEFAULT nextval('station_countries_id'::regclass) NOT NULL,
    iso_code character varying(4) NOT NULL,
    description character varying(50)
);


ALTER TABLE public.station_countries OWNER TO clidegui;

--
-- Name: TABLE station_countries; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE station_countries IS 'Stores countries that stations can belong to.';


--
-- Name: COLUMN station_countries.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_countries.id IS 'Surrogate Key';


--
-- Name: COLUMN station_countries.iso_code; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_countries.iso_code IS 'International ISO country code 3166';


--
-- Name: COLUMN station_countries.description; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_countries.description IS 'Country Name';


--
-- Name: station_status_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE station_status_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.station_status_id OWNER TO clidegui;

--
-- Name: SEQUENCE station_status_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE station_status_id IS 'PK sequence for station status';


--
-- Name: station_status; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE station_status (
    id integer DEFAULT nextval('station_status_id'::regclass) NOT NULL,
    status character varying(10) NOT NULL,
    description character varying(50)
);


ALTER TABLE public.station_status OWNER TO clidegui;

--
-- Name: TABLE station_status; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE station_status IS 'Stores allowed values for stations.status_id';


--
-- Name: COLUMN station_status.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_status.id IS 'Surrogate Key';


--
-- Name: COLUMN station_status.status; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_status.status IS 'Status Code';


--
-- Name: COLUMN station_status.description; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_status.description IS 'Description of status';


--
-- Name: station_timezones_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE station_timezones_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.station_timezones_id OWNER TO clidegui;

--
-- Name: SEQUENCE station_timezones_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE station_timezones_id IS 'PK sequence for station time zones';


--
-- Name: station_timezones; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE station_timezones (
    id integer DEFAULT nextval('station_timezones_id'::regclass) NOT NULL,
    tm_zone character varying(3) NOT NULL,
    utc_diff numeric(4,1) NOT NULL,
    description character varying(50)
);


ALTER TABLE public.station_timezones OWNER TO clidegui;

--
-- Name: TABLE station_timezones; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE station_timezones IS 'Stores time zone that stations can be in.';


--
-- Name: COLUMN station_timezones.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_timezones.id IS 'Surrogate Key';


--
-- Name: COLUMN station_timezones.tm_zone; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_timezones.tm_zone IS 'Time zone code';


--
-- Name: COLUMN station_timezones.utc_diff; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_timezones.utc_diff IS 'Adjustment ADDED to get local standard time';


--
-- Name: COLUMN station_timezones.description; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_timezones.description IS 'Description of time zone';


--
-- Name: surface_types_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE surface_types_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.surface_types_id OWNER TO clidegui;

--
-- Name: SEQUENCE surface_types_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE surface_types_id IS 'PK sequence for surface types';


--
-- Name: surface_types; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE surface_types (
    id integer DEFAULT nextval('surface_types_id'::regclass) NOT NULL,
    surface_type character varying(10) NOT NULL,
    description character varying(50)
);


ALTER TABLE public.surface_types OWNER TO clidegui;

--
-- Name: TABLE surface_types; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE surface_types IS 'Stores allowed values for stations.surface_type_id';


--
-- Name: COLUMN surface_types.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN surface_types.id IS 'Surrogate Key';


--
-- Name: COLUMN surface_types.surface_type; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN surface_types.surface_type IS 'Surface type code';


--
-- Name: COLUMN surface_types.description; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN surface_types.description IS 'Surface type description';


--
-- Name: ext_stations; Type: VIEW; Schema: public; Owner: clidegui
--

CREATE VIEW ext_stations AS
    SELECT s.id, s.station_no, s.name_primary, s.name_secondary, s.region, s.catchment, s.authority, ss.description AS status, s.start_date, s.end_date, s.ht_aero AS aero_height, s.ht_elev AS station_elevation, s.latitude, s.longitude, s.time_zone, tim.utc_diff AS utc_offset, tim.description AS timezone_description, s.id_aero, s.id_imo, s.id_marine, s.id_wmo, s.id_hydro, s.id_aust, s.id_niwa, s.id_niwa_agent, s.country_code, cou.description AS country_description, s.lu_0_100m, lu1.description AS land_use_0_100m, s.lu_100m_1km, lu2.description AS land_use_100m_1km, s.lu_1km_10km, lu3.description AS land_use_1km_10km, s.comments FROM ((((((((stations s LEFT JOIN surface_types sur ON ((s.surface_type = sur.id))) LEFT JOIN soil_types soi ON ((s.soil_type = soi.id))) LEFT JOIN station_status ss ON ((s.status_id = ss.id))) LEFT JOIN station_timezones tim ON (((s.time_zone)::text = (tim.tm_zone)::text))) LEFT JOIN station_countries cou ON (((s.country_code)::text = (cou.iso_code)::text))) LEFT JOIN land_use lu1 ON ((s.lu_0_100m = lu1.id))) LEFT JOIN land_use lu2 ON ((s.lu_100m_1km = lu2.id))) LEFT JOIN land_use lu3 ON ((s.lu_1km_10km = lu3.id))) ORDER BY s.station_no;


ALTER TABLE public.ext_stations OWNER TO clidegui;

--
-- Name: gui_users_id_seq; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE gui_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gui_users_id_seq OWNER TO clidegui;

--
-- Name: SEQUENCE gui_users_id_seq; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE gui_users_id_seq IS 'PK sequence for gui_users';


--
-- Name: gui_users; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE gui_users (
    id integer DEFAULT nextval('gui_users_id_seq'::regclass) NOT NULL,
    username character varying(20) NOT NULL,
    css_filename character varying(120),
    layout character(4) DEFAULT 'POP'::bpchar,
    key character varying(64),
    disabled character(1),
    disable_date timestamp with time zone,
    station_maint character(1) DEFAULT 'N'::bpchar NOT NULL,
    codes_maint character(1) DEFAULT 'N'::bpchar NOT NULL,
    user_admin character(1) DEFAULT 'N'::bpchar NOT NULL,
    file_ingest character(1) DEFAULT 'N'::bpchar NOT NULL,
    key_entry character(1) DEFAULT 'N'::bpchar NOT NULL,
    qa character(1) DEFAULT 'N'::bpchar NOT NULL,
    products character(1) DEFAULT 'N'::bpchar NOT NULL
);


ALTER TABLE public.gui_users OWNER TO clidegui;

--
-- Name: TABLE gui_users; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE gui_users IS 'User data for web GUI';


--
-- Name: COLUMN gui_users.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN gui_users.id IS 'Surrogate Key';


--
-- Name: COLUMN gui_users.username; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN gui_users.username IS 'Login user id';


--
-- Name: COLUMN gui_users.css_filename; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN gui_users.css_filename IS 'Name of style sheet selected';


--
-- Name: COLUMN gui_users.layout; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN gui_users.layout IS 'Layout of page: LEFT menu, top menu, popup menu, HTML';


--
-- Name: ingest_monitor_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE ingest_monitor_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ingest_monitor_id OWNER TO clidegui;

--
-- Name: SEQUENCE ingest_monitor_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE ingest_monitor_id IS 'PK sequence for ingest_monitor';


--
-- Name: ingest_monitor; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE ingest_monitor (
    id integer DEFAULT nextval('ingest_monitor_id'::regclass) NOT NULL,
    username character varying(20) NOT NULL,
    ip_addr character varying(20),
    filename character varying(200),
    ingest_start timestamp without time zone DEFAULT now() NOT NULL,
    ingest_end timestamp without time zone,
    file_recs integer,
    ingested_recs integer,
    ok_count integer,
    err_count integer,
    cancel_flag character(1),
    cancel_user character varying(20),
    change_datetime timestamp without time zone
);


ALTER TABLE public.ingest_monitor OWNER TO clidegui;

--
-- Name: TABLE ingest_monitor; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE ingest_monitor IS 'Stores file ingestion stats for data ingests';


--
-- Name: COLUMN ingest_monitor.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN ingest_monitor.id IS 'Surrogate Key';


--
-- Name: COLUMN ingest_monitor.username; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN ingest_monitor.username IS 'User that started ingest';


--
-- Name: COLUMN ingest_monitor.ip_addr; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN ingest_monitor.ip_addr IS 'Client IP address where ingest was invoked from';


--
-- Name: COLUMN ingest_monitor.filename; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN ingest_monitor.filename IS 'File name of file being ingested';


--
-- Name: COLUMN ingest_monitor.ingest_start; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN ingest_monitor.ingest_start IS 'Ingest start time';


--
-- Name: COLUMN ingest_monitor.ingest_end; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN ingest_monitor.ingest_end IS 'Ingest end time';


--
-- Name: COLUMN ingest_monitor.file_recs; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN ingest_monitor.file_recs IS 'Count of all input file records';


--
-- Name: COLUMN ingest_monitor.ingested_recs; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN ingest_monitor.ingested_recs IS 'Count of all ingested input file records';


--
-- Name: key_settings; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE key_settings (
    id integer DEFAULT nextval('key_settings_id'::regclass) NOT NULL,
    profile character varying(20) NOT NULL,
    obs_type character varying(20),
    element character varying(120),
    default_unit character varying(20),
    disable_flag character(1),
    change_user character varying(20),
    change_datetime timestamp without time zone
);


ALTER TABLE public.key_settings OWNER TO clidegui;

--
-- Name: TABLE key_settings; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE key_settings IS 'Stores key entry settings: Default units, disable flag';


--
-- Name: COLUMN key_settings.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN key_settings.id IS 'Surrogate Key';


--
-- Name: COLUMN key_settings.profile; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN key_settings.profile IS 'profile name';


--
-- Name: COLUMN key_settings.obs_type; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN key_settings.obs_type IS 'obsservation type: daily, subdaily';


--
-- Name: COLUMN key_settings.element; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN key_settings.element IS 'observation element';


--
-- Name: COLUMN key_settings.default_unit; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN key_settings.default_unit IS 'Default unit in key entry forms';


--
-- Name: COLUMN key_settings.disable_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN key_settings.disable_flag IS 'Y=disable in entry forms';


--
-- Name: obs_audit_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obs_audit_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obs_audit_id OWNER TO clidegui;

--
-- Name: SEQUENCE obs_audit_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obs_audit_id IS 'PK sequence for obs audit';


--
-- Name: obs_audit; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obs_audit (
    id integer DEFAULT nextval('obs_audit_id'::regclass) NOT NULL,
    table_name character varying(100),
    row_id integer,
    column_name character varying(100),
    column_value character varying(4000),
    change_user character varying(20),
    datetime timestamp with time zone
);


ALTER TABLE public.obs_audit OWNER TO clidegui;

--
-- Name: TABLE obs_audit; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obs_audit IS 'Audit trail of all changes to station Station.';


--
-- Name: COLUMN obs_audit.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_audit.id IS 'Surrogate Key';


--
-- Name: COLUMN obs_audit.table_name; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_audit.table_name IS 'Observation table where data is changed';


--
-- Name: COLUMN obs_audit.row_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_audit.row_id IS 'Row id of changed data';


--
-- Name: COLUMN obs_audit.column_name; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_audit.column_name IS 'Column that has been changed';


--
-- Name: COLUMN obs_audit.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_audit.change_user IS 'User performing the change';


--
-- Name: COLUMN obs_audit.datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_audit.datetime IS 'Datetime of change';


--
-- Name: obs_averages_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obs_averages_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obs_averages_id OWNER TO clidegui;

--
-- Name: SEQUENCE obs_averages_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obs_averages_id IS 'PK sequence for obs_averages';


--
-- Name: obs_averages; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obs_averages (
    id integer DEFAULT nextval('obs_averages_id'::regclass) NOT NULL,
    insert_datetime timestamp without time zone DEFAULT now() NOT NULL,
    change_datetime timestamp without time zone,
    change_user character varying(20),
    station_no character varying(20) NOT NULL,
    month smallint NOT NULL,
    name character varying(60) NOT NULL,
    active_normal character(1),
    from_date date NOT NULL,
    to_date date NOT NULL,
    station_pres numeric(7,1),
    msl_pres numeric(7,1),
    air_temp numeric(7,1),
    max_air_temp numeric(7,1),
    min_air_temp numeric(7,1),
    vapour_pres numeric(7,1),
    rainfall numeric(7,1),
    rain_days smallint,
    sun_hours smallint,
    missing_station_pres smallint,
    missing_air_temp smallint,
    missing_max_min smallint,
    missing_vapour_pres smallint,
    missing_rainfall smallint,
    missing_sun_hours smallint,
    air_temp_stddev numeric(7,1)
);


ALTER TABLE public.obs_averages OWNER TO clidegui;

--
-- Name: TABLE obs_averages; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obs_averages IS 'Normals and other monthly long term averages of observations.';


--
-- Name: COLUMN obs_averages.month; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.month IS 'Month of averages';


--
-- Name: COLUMN obs_averages.name; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.name IS 'Name of this set of averages';


--
-- Name: COLUMN obs_averages.from_date; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.from_date IS 'Start date of observations in this average set';


--
-- Name: COLUMN obs_averages.to_date; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.to_date IS 'End date of observations in this average set';


--
-- Name: COLUMN obs_averages.station_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.station_pres IS 'Average Station Pressure: from obs_subdaily.station_pres';


--
-- Name: COLUMN obs_averages.msl_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.msl_pres IS 'Average MSL Pressure: from obs_subdaily.msl_pres';


--
-- Name: COLUMN obs_averages.air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.air_temp IS 'Average air temp: from obs_subdaily.air_temp';


--
-- Name: COLUMN obs_averages.max_air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.max_air_temp IS 'Average max air temp: from obs_daily.max_air_temp';


--
-- Name: COLUMN obs_averages.min_air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.min_air_temp IS 'Average min air temp: from obs_daily.min_air_temp';


--
-- Name: COLUMN obs_averages.vapour_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.vapour_pres IS 'Average vapour pressure: from obs_subdaily.dew_point';


--
-- Name: COLUMN obs_averages.rainfall; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.rainfall IS 'Avg Total monthly rainfall. from obs_daily.rain_24h';


--
-- Name: COLUMN obs_averages.rain_days; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.rain_days IS 'Avg Total monthly rain days. from obs_daily.rain_24h_count';


--
-- Name: COLUMN obs_averages.sun_hours; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.sun_hours IS 'Avg monthly sunshine hours. from obs_daily.sunshine_duration';


--
-- Name: COLUMN obs_averages.missing_station_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.missing_station_pres IS 'Number of years missing from the record of normal station pressure';


--
-- Name: COLUMN obs_averages.missing_air_temp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.missing_air_temp IS 'Number of years missing from the record of normal air temp';


--
-- Name: COLUMN obs_averages.missing_max_min; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.missing_max_min IS 'Number of years missing from the record of normal daily max or min air temp';


--
-- Name: COLUMN obs_averages.missing_vapour_pres; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.missing_vapour_pres IS 'Number of years missing from the record of normal daily vapour pres';


--
-- Name: COLUMN obs_averages.missing_rainfall; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.missing_rainfall IS 'Number of years missing from the record of normal daily rainfall';


--
-- Name: COLUMN obs_averages.missing_sun_hours; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.missing_sun_hours IS 'Number of years missing from the record of normal daily sunshine hours';


--
-- Name: COLUMN obs_averages.air_temp_stddev; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obs_averages.air_temp_stddev IS 'Std Deviation of air temp';


--
-- Name: obs_clicom_element_map_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obs_clicom_element_map_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obs_clicom_element_map_id OWNER TO clidegui;

--
-- Name: SEQUENCE obs_clicom_element_map_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obs_clicom_element_map_id IS 'PK sequence for obs_clicom_element_map';


--
-- Name: obs_clicom_element_map; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obs_clicom_element_map (
    id integer DEFAULT nextval('obs_clicom_element_map_id'::regclass) NOT NULL,
    clicom_element character varying(5) NOT NULL,
    cldb_table character varying(80) NOT NULL,
    cldb_column character varying(80) NOT NULL,
    associated_col character varying(80),
    associated_value character varying(100),
    column_type character varying(4) DEFAULT 'num'::character varying,
    nominal_value character varying(20)
);


ALTER TABLE public.obs_clicom_element_map OWNER TO clidegui;

--
-- Name: TABLE obs_clicom_element_map; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obs_clicom_element_map IS 'Mapping Clicom Codes to CLDB table, column';


--
-- Name: obs_monthly_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obs_monthly_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obs_monthly_id OWNER TO clidegui;

--
-- Name: SEQUENCE obs_monthly_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obs_monthly_id IS 'PK sequence for obs_monthly';


--
-- Name: obscodes_cloud_amt_conv_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obscodes_cloud_amt_conv_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obscodes_cloud_amt_conv_id OWNER TO clidegui;

--
-- Name: SEQUENCE obscodes_cloud_amt_conv_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obscodes_cloud_amt_conv_id IS 'PK sequence for obscodes_cloud_amt_conv';


--
-- Name: obscodes_cloud_amt_conv; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obscodes_cloud_amt_conv (
    id integer DEFAULT nextval('obscodes_cloud_amt_conv_id'::regclass) NOT NULL,
    code_0501 character(1),
    code_2700 character(1),
    code_bft character varying(10),
    tenths character varying(5),
    oktas character(1),
    change_user character varying(10),
    change_datetime timestamp without time zone,
    insert_datetime timestamp without time zone NOT NULL
);


ALTER TABLE public.obscodes_cloud_amt_conv OWNER TO clidegui;

--
-- Name: TABLE obscodes_cloud_amt_conv; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obscodes_cloud_amt_conv IS 'Cloud Amount conversions';


--
-- Name: COLUMN obscodes_cloud_amt_conv.code_0501; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_amt_conv.code_0501 IS 'WMO Code 0501 code form';


--
-- Name: COLUMN obscodes_cloud_amt_conv.code_2700; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_amt_conv.code_2700 IS 'WMO Code 2700 code form';


--
-- Name: COLUMN obscodes_cloud_amt_conv.code_bft; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_amt_conv.code_bft IS 'Beaufort code';


--
-- Name: COLUMN obscodes_cloud_amt_conv.tenths; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_amt_conv.tenths IS 'Tenths (Can be multiple values comma separated)';


--
-- Name: COLUMN obscodes_cloud_amt_conv.oktas; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_amt_conv.oktas IS 'Oktas (1-9)';


--
-- Name: COLUMN obscodes_cloud_amt_conv.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_amt_conv.change_user IS 'User of last change';


--
-- Name: COLUMN obscodes_cloud_amt_conv.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_amt_conv.change_datetime IS 'Timestamp of last change';


--
-- Name: COLUMN obscodes_cloud_amt_conv.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_amt_conv.insert_datetime IS 'Timestamp of insert';


--
-- Name: obscodes_cloud_conv_1677_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obscodes_cloud_conv_1677_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obscodes_cloud_conv_1677_id OWNER TO clidegui;

--
-- Name: SEQUENCE obscodes_cloud_conv_1677_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obscodes_cloud_conv_1677_id IS 'PK sequence for obscodes_cloud_conv_1677';


--
-- Name: obscodes_cloud_conv_1677; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obscodes_cloud_conv_1677 (
    id integer DEFAULT nextval('obscodes_cloud_conv_1677_id'::regclass) NOT NULL,
    code character varying(2),
    low_feet numeric(7,0),
    low_meters numeric(7,0),
    change_user character varying(10),
    change_datetime timestamp without time zone,
    insert_datetime timestamp without time zone
);


ALTER TABLE public.obscodes_cloud_conv_1677 OWNER TO clidegui;

--
-- Name: TABLE obscodes_cloud_conv_1677; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obscodes_cloud_conv_1677 IS 'Cloud Height conversions for WMO 1677';


--
-- Name: COLUMN obscodes_cloud_conv_1677.code; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_conv_1677.code IS 'WMO 1677 code';


--
-- Name: COLUMN obscodes_cloud_conv_1677.low_feet; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_conv_1677.low_feet IS 'Lower bound in feet';


--
-- Name: COLUMN obscodes_cloud_conv_1677.low_meters; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_conv_1677.low_meters IS 'Lower bound in M';


--
-- Name: COLUMN obscodes_cloud_conv_1677.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_conv_1677.change_user IS 'User of last change';


--
-- Name: COLUMN obscodes_cloud_conv_1677.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_conv_1677.change_datetime IS 'Timestamp of last change';


--
-- Name: COLUMN obscodes_cloud_conv_1677.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_conv_1677.insert_datetime IS 'Timestamp of insert';


--
-- Name: obscodes_cloud_ht_conv_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obscodes_cloud_ht_conv_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obscodes_cloud_ht_conv_id OWNER TO clidegui;

--
-- Name: SEQUENCE obscodes_cloud_ht_conv_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obscodes_cloud_ht_conv_id IS 'PK sequence for obscodes_cloud_ht_conv';


--
-- Name: obscodes_cloud_ht_conv; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obscodes_cloud_ht_conv (
    id integer DEFAULT nextval('obscodes_cloud_ht_conv_id'::regclass) NOT NULL,
    code character(1),
    low_feet numeric(9,0),
    high_feet numeric(9,0),
    low_meters numeric(7,0),
    high_meters numeric(7,0),
    change_user character varying(10),
    change_datetime timestamp without time zone,
    insert_datetime timestamp without time zone
);


ALTER TABLE public.obscodes_cloud_ht_conv OWNER TO clidegui;

--
-- Name: TABLE obscodes_cloud_ht_conv; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obscodes_cloud_ht_conv IS 'Cloud Height conversions';


--
-- Name: COLUMN obscodes_cloud_ht_conv.code; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_ht_conv.code IS 'WMO 1600 Code';


--
-- Name: COLUMN obscodes_cloud_ht_conv.low_feet; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_ht_conv.low_feet IS 'Lower bound in feet';


--
-- Name: COLUMN obscodes_cloud_ht_conv.high_feet; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_ht_conv.high_feet IS 'Upper bound in Feet';


--
-- Name: COLUMN obscodes_cloud_ht_conv.low_meters; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_ht_conv.low_meters IS 'Lower Bound in M';


--
-- Name: COLUMN obscodes_cloud_ht_conv.high_meters; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_ht_conv.high_meters IS 'Upper Bound in M';


--
-- Name: COLUMN obscodes_cloud_ht_conv.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_ht_conv.change_user IS 'User of last change';


--
-- Name: COLUMN obscodes_cloud_ht_conv.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_ht_conv.change_datetime IS 'Timestamp of last change';


--
-- Name: COLUMN obscodes_cloud_ht_conv.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_ht_conv.insert_datetime IS 'Timestamp of insert';


--
-- Name: obscodes_cloud_type_conv_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obscodes_cloud_type_conv_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obscodes_cloud_type_conv_id OWNER TO clidegui;

--
-- Name: SEQUENCE obscodes_cloud_type_conv_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obscodes_cloud_type_conv_id IS 'PK sequence for obscodes_cloud_type_conv';


--
-- Name: obscodes_cloud_type_conv; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obscodes_cloud_type_conv (
    id integer DEFAULT nextval('obscodes_cloud_type_conv_id'::regclass) NOT NULL,
    code_0500 character(1),
    code_figure character(1),
    wmo_table character(4),
    layer character varying(4),
    types character varying(10),
    change_user character varying(10),
    change_datetime timestamp without time zone,
    insert_datetime timestamp without time zone
);


ALTER TABLE public.obscodes_cloud_type_conv OWNER TO clidegui;

--
-- Name: TABLE obscodes_cloud_type_conv; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obscodes_cloud_type_conv IS 'Cloud Type conversions';


--
-- Name: COLUMN obscodes_cloud_type_conv.code_figure; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_type_conv.code_figure IS 'WMO Code figure';


--
-- Name: COLUMN obscodes_cloud_type_conv.wmo_table; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_type_conv.wmo_table IS 'WMO Table no (0513 Low, 0515 Mid, 0509 High)';


--
-- Name: COLUMN obscodes_cloud_type_conv.layer; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_type_conv.layer IS 'Cloud Layer: Low, Mid, High';


--
-- Name: COLUMN obscodes_cloud_type_conv.types; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_type_conv.types IS 'Acceptable Cloud types';


--
-- Name: COLUMN obscodes_cloud_type_conv.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_type_conv.change_user IS 'User of last change';


--
-- Name: COLUMN obscodes_cloud_type_conv.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_type_conv.change_datetime IS 'Timestamp of last change';


--
-- Name: COLUMN obscodes_cloud_type_conv.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_cloud_type_conv.insert_datetime IS 'Timestamp of insert';


--
-- Name: obscodes_visibility_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obscodes_visibility_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obscodes_visibility_id OWNER TO clidegui;

--
-- Name: SEQUENCE obscodes_visibility_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obscodes_visibility_id IS 'PK sequence for obscodes_visibility';


--
-- Name: obscodes_visibility; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obscodes_visibility (
    id integer DEFAULT nextval('obscodes_visibility_id'::regclass) NOT NULL,
    non_aero_scale character varying(2) NOT NULL,
    distance_km numeric(5,2),
    distance_yards numeric(7,0),
    valid_aero_codes character varying(100),
    code character(1),
    change_user character varying(10),
    change_datetime timestamp without time zone,
    insert_datetime timestamp without time zone
);


ALTER TABLE public.obscodes_visibility OWNER TO clidegui;

--
-- Name: TABLE obscodes_visibility; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obscodes_visibility IS 'Visibility conversions: Aero, non-Aero, Km, yards. WMO 4300';


--
-- Name: COLUMN obscodes_visibility.non_aero_scale; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_visibility.non_aero_scale IS 'Visibility non-Aero scale';


--
-- Name: COLUMN obscodes_visibility.distance_km; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_visibility.distance_km IS 'Distance in Km';


--
-- Name: COLUMN obscodes_visibility.distance_yards; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_visibility.distance_yards IS 'Distance in Yards';


--
-- Name: COLUMN obscodes_visibility.valid_aero_codes; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_visibility.valid_aero_codes IS 'Valid Aero codes, comma sep';


--
-- Name: COLUMN obscodes_visibility.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_visibility.change_user IS 'User of last change';


--
-- Name: COLUMN obscodes_visibility.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_visibility.change_datetime IS 'Timestamp of last change';


--
-- Name: COLUMN obscodes_visibility.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_visibility.insert_datetime IS 'Timestamp of insert';


--
-- Name: obscodes_wind_dir_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obscodes_wind_dir_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obscodes_wind_dir_id OWNER TO clidegui;

--
-- Name: SEQUENCE obscodes_wind_dir_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obscodes_wind_dir_id IS 'PK sequence for obscodes_wind_dir';


--
-- Name: obscodes_wind_dir; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obscodes_wind_dir (
    id integer DEFAULT nextval('obscodes_wind_dir_id'::regclass) NOT NULL,
    compass character varying(6) NOT NULL,
    degrees numeric(3,0),
    low_degrees numeric(5,2),
    high_degrees numeric(5,2),
    change_user character varying(10),
    change_datetime timestamp without time zone,
    insert_datetime timestamp without time zone
);


ALTER TABLE public.obscodes_wind_dir OWNER TO clidegui;

--
-- Name: TABLE obscodes_wind_dir; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obscodes_wind_dir IS 'Wind Direction conversions: Compass points to degrees';


--
-- Name: COLUMN obscodes_wind_dir.compass; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_dir.compass IS 'Compass points: NNE, SE, CLM,';


--
-- Name: COLUMN obscodes_wind_dir.degrees; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_dir.degrees IS 'Degrees (0-360)';


--
-- Name: COLUMN obscodes_wind_dir.low_degrees; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_dir.low_degrees IS 'Lower bound in degrees (>)';


--
-- Name: COLUMN obscodes_wind_dir.high_degrees; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_dir.high_degrees IS 'Upper bound in degrees (<=)';


--
-- Name: COLUMN obscodes_wind_dir.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_dir.change_user IS 'User of last change';


--
-- Name: COLUMN obscodes_wind_dir.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_dir.change_datetime IS 'Timestamp of last change';


--
-- Name: COLUMN obscodes_wind_dir.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_dir.insert_datetime IS 'Timestamp of insert';


--
-- Name: obscodes_wind_speed_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obscodes_wind_speed_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obscodes_wind_speed_id OWNER TO clidegui;

--
-- Name: SEQUENCE obscodes_wind_speed_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obscodes_wind_speed_id IS 'PK sequence for obscodes_wind_speed';


--
-- Name: obscodes_wind_speed; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obscodes_wind_speed (
    id integer DEFAULT nextval('obscodes_wind_speed_id'::regclass) NOT NULL,
    code_bft character varying(2) NOT NULL,
    ms numeric(5,2),
    low_ms numeric(5,2),
    high_ms numeric(5,2),
    low_knots numeric(5,2),
    high_knots numeric(5,2),
    change_user character varying(10),
    change_datetime timestamp without time zone,
    insert_datetime timestamp without time zone
);


ALTER TABLE public.obscodes_wind_speed OWNER TO clidegui;

--
-- Name: TABLE obscodes_wind_speed; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obscodes_wind_speed IS 'Wind speed conversions: Beaufort, m/s, knots';


--
-- Name: COLUMN obscodes_wind_speed.code_bft; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_speed.code_bft IS 'Beaufort code';


--
-- Name: COLUMN obscodes_wind_speed.ms; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_speed.ms IS 'M/S';


--
-- Name: COLUMN obscodes_wind_speed.low_ms; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_speed.low_ms IS 'Lower bound in M/S';


--
-- Name: COLUMN obscodes_wind_speed.high_ms; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_speed.high_ms IS 'Upper bound in M/S';


--
-- Name: COLUMN obscodes_wind_speed.low_knots; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_speed.low_knots IS 'Lower bound in Knots';


--
-- Name: COLUMN obscodes_wind_speed.high_knots; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_speed.high_knots IS 'Upper bound in Knots';


--
-- Name: COLUMN obscodes_wind_speed.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_speed.change_user IS 'User of last change';


--
-- Name: COLUMN obscodes_wind_speed.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_speed.change_datetime IS 'Timestamp of last change';


--
-- Name: COLUMN obscodes_wind_speed.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wind_speed.insert_datetime IS 'Timestamp of insert';


--
-- Name: obscodes_wx_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obscodes_wx_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obscodes_wx_id OWNER TO clidegui;

--
-- Name: SEQUENCE obscodes_wx_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obscodes_wx_id IS 'PK sequence for obscodes_wx';


--
-- Name: obscodes_wx; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obscodes_wx (
    id integer DEFAULT nextval('obscodes_wx_id'::regclass) NOT NULL,
    code character varying(2) NOT NULL,
    name character varying(40),
    description character varying(200),
    change_user character varying(10),
    change_datetime timestamp without time zone,
    insert_datetime timestamp without time zone
);


ALTER TABLE public.obscodes_wx OWNER TO clidegui;

--
-- Name: TABLE obscodes_wx; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obscodes_wx IS 'WMO Code 4677 (WX codes)';


--
-- Name: COLUMN obscodes_wx.code; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wx.code IS 'WMO 4677 code';


--
-- Name: COLUMN obscodes_wx.name; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wx.name IS 'Name of phenomenon';


--
-- Name: COLUMN obscodes_wx.description; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wx.description IS 'Description of phenomenon';


--
-- Name: COLUMN obscodes_wx.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wx.change_user IS 'User of last change';


--
-- Name: COLUMN obscodes_wx.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wx.change_datetime IS 'Timestamp of last change';


--
-- Name: COLUMN obscodes_wx.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obscodes_wx.insert_datetime IS 'Timestamp of insert';


--
-- Name: obsconv_factors_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE obsconv_factors_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obsconv_factors_id OWNER TO clidegui;

--
-- Name: SEQUENCE obsconv_factors_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE obsconv_factors_id IS 'PK sequence for obsconv_factors';


--
-- Name: obsconv_factors; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE obsconv_factors (
    id integer DEFAULT nextval('obsconv_factors_id'::regclass) NOT NULL,
    from_type character varying(20) NOT NULL,
    to_type character varying(20) NOT NULL,
    pre_sum numeric(5,2),
    mult_factor numeric(7,4) NOT NULL,
    post_sum numeric(7,4),
    change_user character varying(10),
    change_datetime timestamp without time zone,
    insert_datetime timestamp without time zone NOT NULL
);


ALTER TABLE public.obsconv_factors OWNER TO clidegui;

--
-- Name: TABLE obsconv_factors; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE obsconv_factors IS 'WMO Code 4677 (WX codes)';


--
-- Name: COLUMN obsconv_factors.from_type; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obsconv_factors.from_type IS 'From unit (eg. Fahrenheit, Inches)';


--
-- Name: COLUMN obsconv_factors.to_type; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obsconv_factors.to_type IS 'To unit (eg. Celsius, mm)';


--
-- Name: COLUMN obsconv_factors.pre_sum; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obsconv_factors.pre_sum IS 'Value to add prior to multiplying conversion factor';


--
-- Name: COLUMN obsconv_factors.mult_factor; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obsconv_factors.mult_factor IS 'Conversion factor. Multiplied by From.';


--
-- Name: COLUMN obsconv_factors.post_sum; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obsconv_factors.post_sum IS 'Value to add after multiplying conversion factor.';


--
-- Name: COLUMN obsconv_factors.change_user; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obsconv_factors.change_user IS 'User of last change';


--
-- Name: COLUMN obsconv_factors.change_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obsconv_factors.change_datetime IS 'Timestamp of last change';


--
-- Name: COLUMN obsconv_factors.insert_datetime; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN obsconv_factors.insert_datetime IS 'Timestamp of insert';


--
-- Name: pivot; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE pivot (
    i integer NOT NULL
);


ALTER TABLE public.pivot OWNER TO clidegui;

--
-- Name: TABLE pivot; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE pivot IS 'Utility table of sequential integers';


--
-- Name: spatial_ref_sys; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE spatial_ref_sys (
    srid integer NOT NULL,
    auth_name character varying(256),
    auth_srid integer,
    srtext character varying(2048),
    proj4text character varying(2048)
);


ALTER TABLE public.spatial_ref_sys OWNER TO clidegui;

--
-- Name: TABLE spatial_ref_sys; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE spatial_ref_sys IS 'Spatial reference system definitions from PostGIS';


--
-- Name: station_contacts_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE station_contacts_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.station_contacts_id OWNER TO clidegui;

--
-- Name: SEQUENCE station_contacts_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE station_contacts_id IS 'PK sequence for station contacts';


--
-- Name: station_contacts; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE station_contacts (
    id integer DEFAULT nextval('station_contacts_id'::regclass) NOT NULL,
    station_id integer NOT NULL,
    title character varying(50),
    name character varying(50),
    addr1 character varying(50),
    addr2 character varying(50),
    addr3 character varying(50),
    addr4 character varying(50),
    town character varying(50),
    state character varying(50),
    country character varying(50),
    postcode character varying(10),
    home_phone character varying(20),
    work_phone character varying(20),
    mob_phone character varying(20),
    email character varying(100),
    fax character varying(20),
    comments character varying(4000),
    start_date date,
    end_date date
);


ALTER TABLE public.station_contacts OWNER TO clidegui;

--
-- Name: TABLE station_contacts; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE station_contacts IS 'Stores contacts (people) for station';


--
-- Name: COLUMN station_contacts.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_contacts.id IS 'Surrogate Key';


--
-- Name: COLUMN station_contacts.station_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_contacts.station_id IS 'Station ID of station contact';


--
-- Name: station_files_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE station_files_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.station_files_id OWNER TO clidegui;

--
-- Name: SEQUENCE station_files_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE station_files_id IS 'PK sequence for station files';


--
-- Name: station_files; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE station_files (
    id integer DEFAULT nextval('station_files_id'::regclass) NOT NULL,
    station_id integer NOT NULL,
    title character varying(50),
    description character varying(1000),
    file_path character varying(200)
);


ALTER TABLE public.station_files OWNER TO clidegui;

--
-- Name: TABLE station_files; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE station_files IS 'Stores address of files such as images, pdfs, Word docs, etc. for station.';


--
-- Name: COLUMN station_files.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_files.id IS 'Surrogate Key';


--
-- Name: COLUMN station_files.station_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_files.station_id IS 'ID of station this row belongs to';


--
-- Name: COLUMN station_files.title; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_files.title IS 'Title of file';


--
-- Name: COLUMN station_files.description; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_files.description IS 'Description of file';


--
-- Name: COLUMN station_files.file_path; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN station_files.file_path IS 'Full path to file.';


--
-- Name: timezone_diffs_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE timezone_diffs_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.timezone_diffs_id OWNER TO clidegui;

--
-- Name: SEQUENCE timezone_diffs_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE timezone_diffs_id IS 'PK sequence for timezone diffs';


--
-- Name: timezone_diffs; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE timezone_diffs (
    id integer DEFAULT nextval('timezone_diffs_id'::regclass) NOT NULL,
    start_timestamp timestamp without time zone NOT NULL,
    end_timestamp timestamp without time zone NOT NULL,
    tm_zone character varying(3) NOT NULL,
    tm_diff numeric(4,1)
);


ALTER TABLE public.timezone_diffs OWNER TO clidegui;

--
-- Name: TABLE timezone_diffs; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE timezone_diffs IS 'Stores timezone differences due to daylight savings';


--
-- Name: COLUMN timezone_diffs.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN timezone_diffs.id IS 'Surrogate Key';


--
-- Name: COLUMN timezone_diffs.start_timestamp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN timezone_diffs.start_timestamp IS 'Date time difference starts';


--
-- Name: COLUMN timezone_diffs.end_timestamp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN timezone_diffs.end_timestamp IS 'Date time difference ends';


--
-- Name: COLUMN timezone_diffs.tm_zone; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN timezone_diffs.tm_zone IS 'Time zone where difference applies';


--
-- Name: COLUMN timezone_diffs.tm_diff; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN timezone_diffs.tm_diff IS 'UTC offset during this period';


--
-- Name: user_sessions_id; Type: SEQUENCE; Schema: public; Owner: clidegui
--

CREATE SEQUENCE user_sessions_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_sessions_id OWNER TO clidegui;

--
-- Name: SEQUENCE user_sessions_id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON SEQUENCE user_sessions_id IS 'PK sequence for user_sessions';


--
-- Name: user_sessions; Type: TABLE; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE TABLE user_sessions (
    id integer DEFAULT nextval('user_sessions_id'::regclass) NOT NULL,
    username character varying(20) NOT NULL,
    environment character varying(20) NOT NULL,
    ip_addr character varying(20),
    start_timestamp timestamp without time zone DEFAULT now() NOT NULL,
    end_timestamp timestamp without time zone,
    logout_flag character(1),
    timeout_flag character(1),
    killed_flag character(1)
);


ALTER TABLE public.user_sessions OWNER TO clidegui;

--
-- Name: TABLE user_sessions; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON TABLE user_sessions IS 'Stores User session information';


--
-- Name: COLUMN user_sessions.id; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN user_sessions.id IS 'Surrogate Key';


--
-- Name: COLUMN user_sessions.username; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN user_sessions.username IS 'Login username';


--
-- Name: COLUMN user_sessions.ip_addr; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN user_sessions.ip_addr IS 'IP of client';


--
-- Name: COLUMN user_sessions.start_timestamp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN user_sessions.start_timestamp IS 'Start of session';


--
-- Name: COLUMN user_sessions.end_timestamp; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN user_sessions.end_timestamp IS 'End of session';


--
-- Name: COLUMN user_sessions.timeout_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN user_sessions.timeout_flag IS 'Session ended by timeout';


--
-- Name: COLUMN user_sessions.killed_flag; Type: COMMENT; Schema: public; Owner: clidegui
--

COMMENT ON COLUMN user_sessions.killed_flag IS 'Session ended by admin kill';


--
-- Name: CODES_SIMPLE_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY codes_simple
    ADD CONSTRAINT "CODES_SIMPLE_PK" PRIMARY KEY (id);


--
-- Name: EQUIPMENT_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY equipment
    ADD CONSTRAINT "EQUIPMENT_PK" PRIMARY KEY (id);


--
-- Name: INGEST_MONITOR_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY ingest_monitor
    ADD CONSTRAINT "INGEST_MONITOR_PK" PRIMARY KEY (id);


--
-- Name: KEY_SETTINGS_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY key_settings
    ADD CONSTRAINT "KEY_SETTINGS_PK" PRIMARY KEY (id);


--
-- Name: LAND_USE_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY land_use
    ADD CONSTRAINT "LAND_USE_PK" PRIMARY KEY (id);


--
-- Name: OBSCODES_CLOUD_AMT_CONV_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obscodes_cloud_amt_conv
    ADD CONSTRAINT "OBSCODES_CLOUD_AMT_CONV_PK" PRIMARY KEY (id);


--
-- Name: OBSCODES_CLOUD_CONV_1677_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obscodes_cloud_conv_1677
    ADD CONSTRAINT "OBSCODES_CLOUD_CONV_1677_PK" PRIMARY KEY (id);


--
-- Name: OBSCODES_CLOUD_HT_CONV_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obscodes_cloud_ht_conv
    ADD CONSTRAINT "OBSCODES_CLOUD_HT_CONV_PK" PRIMARY KEY (id);


--
-- Name: OBSCODES_CLOUD_TYPE_CONV_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obscodes_cloud_type_conv
    ADD CONSTRAINT "OBSCODES_CLOUD_TYPE_CONV_PK" PRIMARY KEY (id);


--
-- Name: OBSCODES_VISIBILITY_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obscodes_visibility
    ADD CONSTRAINT "OBSCODES_VISIBILITY_PK" PRIMARY KEY (id);


--
-- Name: OBSCODES_WIND_DIR_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obscodes_wind_dir
    ADD CONSTRAINT "OBSCODES_WIND_DIR_PK" PRIMARY KEY (id);


--
-- Name: OBSCODES_WIND_SPEED_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obscodes_wind_speed
    ADD CONSTRAINT "OBSCODES_WIND_SPEED_PK" PRIMARY KEY (id);


--
-- Name: OBSCODES_WX_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obscodes_wx
    ADD CONSTRAINT "OBSCODES_WX_PK" PRIMARY KEY (id);


--
-- Name: OBSCONV_FACTORS_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obsconv_factors
    ADD CONSTRAINT "OBSCONV_FACTORS_PK" PRIMARY KEY (id);


--
-- Name: OBS_AERO_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obs_aero
    ADD CONSTRAINT "OBS_AERO_PK" PRIMARY KEY (id);


--
-- Name: OBS_AUDIT_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obs_audit
    ADD CONSTRAINT "OBS_AUDIT_PK" PRIMARY KEY (id);


--
-- Name: OBS_AVERAGES_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obs_averages
    ADD CONSTRAINT "OBS_AVERAGES_PK" PRIMARY KEY (id);


--
-- Name: OBS_AWS_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obs_aws
    ADD CONSTRAINT "OBS_AWS_PK" PRIMARY KEY (id);


--
-- Name: OBS_DAILY_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obs_daily
    ADD CONSTRAINT "OBS_DAILY_PK" PRIMARY KEY (id);


--
-- Name: OBS_MONTHLY_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obs_monthly
    ADD CONSTRAINT "OBS_MONTHLY_PK" PRIMARY KEY (id);


--
-- Name: OBS_MONTHLY_UNIQUE; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obs_monthly
    ADD CONSTRAINT "OBS_MONTHLY_UNIQUE" UNIQUE (station_no, lsd);


--
-- Name: OBS_SUBDAILY_CLOUD_LAYERS_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obs_subdaily_cloud_layers
    ADD CONSTRAINT "OBS_SUBDAILY_CLOUD_LAYERS_PK" PRIMARY KEY (id);


--
-- Name: OBS_SUBDAILY_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obs_subdaily
    ADD CONSTRAINT "OBS_SUBDAILY_PK" PRIMARY KEY (id);


--
-- Name: OBS_SUBDAILY_SOIL_TEMPS_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obs_subdaily_soil_temps
    ADD CONSTRAINT "OBS_SUBDAILY_SOIL_TEMPS_PK" PRIMARY KEY (id);


--
-- Name: OBS_UPPER_AIR_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obs_upper_air
    ADD CONSTRAINT "OBS_UPPER_AIR_PK" PRIMARY KEY (id);


--
-- Name: SOIL_TYPES_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY soil_types
    ADD CONSTRAINT "SOIL_TYPES_PK" PRIMARY KEY (id);


--
-- Name: STATIONS_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY stations
    ADD CONSTRAINT "STATIONS_PK" PRIMARY KEY (id);


--
-- Name: STATION_AUDIT_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY station_audit
    ADD CONSTRAINT "STATION_AUDIT_PK" PRIMARY KEY (id);


--
-- Name: STATION_AUDIT_TYPES_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY station_audit_types
    ADD CONSTRAINT "STATION_AUDIT_TYPES_PK" PRIMARY KEY (id);


--
-- Name: STATION_CLASS_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY station_class
    ADD CONSTRAINT "STATION_CLASS_PK" PRIMARY KEY (id);


--
-- Name: STATION_CONTACTS_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY station_contacts
    ADD CONSTRAINT "STATION_CONTACTS_PK" PRIMARY KEY (id);


--
-- Name: STATION_COUNTRIES_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY station_countries
    ADD CONSTRAINT "STATION_COUNTRIES_PK" PRIMARY KEY (id);


--
-- Name: STATION_EQUIPMENT_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY station_equipment
    ADD CONSTRAINT "STATION_EQUIPMENT_PK" PRIMARY KEY (id);


--
-- Name: STATION_FILES_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY station_files
    ADD CONSTRAINT "STATION_FILES_PK" PRIMARY KEY (id);


--
-- Name: STATION_STATUS_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY station_status
    ADD CONSTRAINT "STATION_STATUS_PK" PRIMARY KEY (id);


--
-- Name: STATION_TIMEZONES_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY station_timezones
    ADD CONSTRAINT "STATION_TIMEZONES_PK" PRIMARY KEY (id);


--
-- Name: STATION_TYPES_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY station_types
    ADD CONSTRAINT "STATION_TYPES_PK" PRIMARY KEY (id);


--
-- Name: SURFACE_TYPES_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY surface_types
    ADD CONSTRAINT "SURFACE_TYPES_PK" PRIMARY KEY (id);


--
-- Name: TIMEZONE_DIFFS_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY timezone_diffs
    ADD CONSTRAINT "TIMEZONE_DIFFS_PK" PRIMARY KEY (id);


--
-- Name: USER_SESSIONS_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY user_sessions
    ADD CONSTRAINT "USER_SESSIONS_PK" PRIMARY KEY (id);


--
-- Name: codes_simple_code_unique; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY codes_simple
    ADD CONSTRAINT codes_simple_code_unique UNIQUE (code_type, code);


--
-- Name: datums_pkey; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY datums
    ADD CONSTRAINT datums_pkey PRIMARY KEY (datum_name);


--
-- Name: gui_users_PK; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY gui_users
    ADD CONSTRAINT "gui_users_PK" PRIMARY KEY (id);


--
-- Name: gui_users_username_unique; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY gui_users
    ADD CONSTRAINT gui_users_username_unique UNIQUE (username);


--
-- Name: key_settings_unique; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY key_settings
    ADD CONSTRAINT key_settings_unique UNIQUE (profile, element, obs_type);


--
-- Name: land_use_code_unique; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY land_use
    ADD CONSTRAINT land_use_code_unique UNIQUE (land_use_code);


--
-- Name: obs_average_unique; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obs_averages
    ADD CONSTRAINT obs_average_unique UNIQUE (name, station_no, month);


--
-- Name: obs_clicom_element_map_pk; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY obs_clicom_element_map
    ADD CONSTRAINT obs_clicom_element_map_pk PRIMARY KEY (id);


--
-- Name: pivot_pkey; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY pivot
    ADD CONSTRAINT pivot_pkey PRIMARY KEY (i);


--
-- Name: spatial_ref_sys_pkey; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY spatial_ref_sys
    ADD CONSTRAINT spatial_ref_sys_pkey PRIMARY KEY (srid);


--
-- Name: station_countries_iso_code_unique; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY station_countries
    ADD CONSTRAINT station_countries_iso_code_unique UNIQUE (iso_code);


--
-- Name: station_timezones_tm_zone_unique; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY station_timezones
    ADD CONSTRAINT station_timezones_tm_zone_unique UNIQUE (tm_zone);


--
-- Name: stations_id_wmo_start_date_unique; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY stations
    ADD CONSTRAINT stations_id_wmo_start_date_unique UNIQUE (id_wmo, start_date);


--
-- Name: stations_station_no_unique; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY stations
    ADD CONSTRAINT stations_station_no_unique UNIQUE (station_no);


--
-- Name: type_unique; Type: CONSTRAINT; Schema: public; Owner: clidegui; Tablespace: 
--

ALTER TABLE ONLY station_audit_types
    ADD CONSTRAINT type_unique UNIQUE (audit_type);


--
-- Name: fki_obs_subdaily_cloud_layers_subdaily_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_obs_subdaily_cloud_layers_subdaily_id_fkey ON obs_subdaily_cloud_layers USING btree (sub_daily_id);


--
-- Name: fki_obs_subdaily_soil_temps_subdaily_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_obs_subdaily_soil_temps_subdaily_id_fkey ON obs_subdaily_soil_temps USING btree (sub_daily_id);


--
-- Name: fki_station_audit_audit_type_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_station_audit_audit_type_id_fkey ON station_audit USING btree (audit_type_id);


--
-- Name: fki_station_audit_station_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_station_audit_station_id_fkey ON station_audit USING btree (station_id);


--
-- Name: fki_station_class_station_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_station_class_station_id_fkey ON station_class USING btree (station_id);


--
-- Name: fki_station_class_type_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_station_class_type_id_fkey ON station_class USING btree (type_id);


--
-- Name: fki_station_contacts_station_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_station_contacts_station_id_fkey ON station_contacts USING btree (station_id);


--
-- Name: fki_station_equipment_equipment_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_station_equipment_equipment_id_fkey ON station_equipment USING btree (equipment_id);


--
-- Name: fki_station_equipment_station_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_station_equipment_station_id_fkey ON station_equipment USING btree (station_id);


--
-- Name: fki_station_files_station_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_station_files_station_id_fkey ON station_files USING btree (station_id);


--
-- Name: fki_stations_country_code_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_stations_country_code_fkey ON stations USING btree (country_code);


--
-- Name: fki_stations_land_use_0_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_stations_land_use_0_id_fkey ON stations USING btree (lu_0_100m);


--
-- Name: fki_stations_land_use_100_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_stations_land_use_100_id_fkey ON stations USING btree (lu_100m_1km);


--
-- Name: fki_stations_land_use_1km_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_stations_land_use_1km_id_fkey ON stations USING btree (lu_1km_10km);


--
-- Name: fki_stations_soil_type_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_stations_soil_type_id_fkey ON stations USING btree (soil_type);


--
-- Name: fki_stations_status_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_stations_status_id_fkey ON stations USING btree (status_id);


--
-- Name: fki_stations_surface_type_id_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_stations_surface_type_id_fkey ON stations USING btree (surface_type);


--
-- Name: fki_stations_time_zone_fkey; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_stations_time_zone_fkey ON stations USING btree (time_zone);


--
-- Name: fki_timezone_diffs; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX fki_timezone_diffs ON timezone_diffs USING btree (tm_zone);


--
-- Name: obs_aero_insert_datetime_day_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_aero_insert_datetime_day_idx ON obs_aero USING btree (date_trunc('day'::text, insert_datetime));


--
-- Name: obs_aero_unique_1; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE UNIQUE INDEX obs_aero_unique_1 ON obs_aero USING btree (station_no, lsd) WITH (fillfactor=70);


--
-- Name: obs_audit_row_id_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_audit_row_id_idx ON obs_audit USING btree (row_id);


--
-- Name: obs_aws_lct_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_aws_lct_idx ON obs_aws USING btree (lct);


--
-- Name: obs_aws_lsd_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_aws_lsd_idx ON obs_aws USING btree (lsd);


--
-- Name: obs_aws_unique_1; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE UNIQUE INDEX obs_aws_unique_1 ON obs_aws USING btree (station_no, lsd) WITH (fillfactor=70);


--
-- Name: obs_aws_upper_station_lct_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_aws_upper_station_lct_idx ON obs_aws USING btree (upper((station_no)::text), lct);


--
-- Name: obs_aws_upper_station_lsd_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_aws_upper_station_lsd_idx ON obs_aws USING btree (upper((station_no)::text), lsd);


--
-- Name: obs_daily_insert_datetime_day_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_daily_insert_datetime_day_idx ON obs_daily USING btree (date_trunc('day'::text, insert_datetime));


--
-- Name: obs_daily_lsd_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_daily_lsd_idx ON obs_daily USING btree (lsd);


--
-- Name: obs_daily_unique_1; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE UNIQUE INDEX obs_daily_unique_1 ON obs_daily USING btree (station_no, lsd) WITH (fillfactor=70);


--
-- Name: obs_daily_upper_station_lsd_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_daily_upper_station_lsd_idx ON obs_daily USING btree (upper((station_no)::text), lsd);


--
-- Name: obs_monthly_insert_datetime_day_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_monthly_insert_datetime_day_idx ON obs_monthly USING btree (date_trunc('day'::text, insert_datetime));


--
-- Name: obs_monthly_lsd_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_monthly_lsd_idx ON obs_monthly USING btree (lsd);


--
-- Name: obs_monthly_upper_station_lsd_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_monthly_upper_station_lsd_idx ON obs_monthly USING btree (upper((station_no)::text), lsd);


--
-- Name: obs_subdaily_insert_datetime_day_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_subdaily_insert_datetime_day_idx ON obs_subdaily USING btree (date_trunc('day'::text, insert_datetime));


--
-- Name: obs_subdaily_lct_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_subdaily_lct_idx ON obs_subdaily USING btree (lct);


--
-- Name: obs_subdaily_lsd_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_subdaily_lsd_idx ON obs_subdaily USING btree (lsd);


--
-- Name: obs_subdaily_unique_1; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE UNIQUE INDEX obs_subdaily_unique_1 ON obs_subdaily USING btree (station_no, lsd) WITH (fillfactor=70);


--
-- Name: obs_subdaily_upper_station_lct_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_subdaily_upper_station_lct_idx ON obs_subdaily USING btree (upper((station_no)::text), lct);


--
-- Name: obs_subdaily_upper_station_lsd_idx; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE INDEX obs_subdaily_upper_station_lsd_idx ON obs_subdaily USING btree (upper((station_no)::text), lsd);


--
-- Name: obs_upper_unique_1; Type: INDEX; Schema: public; Owner: clidegui; Tablespace: 
--

CREATE UNIQUE INDEX obs_upper_unique_1 ON obs_upper_air USING btree (station_no, lsd, geo_height) WITH (fillfactor=70);


--
-- Name: stations_id_wmo_dates_trg; Type: TRIGGER; Schema: public; Owner: clidegui
--

CREATE TRIGGER stations_id_wmo_dates_trg BEFORE INSERT OR UPDATE ON stations FOR EACH ROW EXECUTE PROCEDURE stations_id_wmo_dates_trg();


--
-- Name: obs_aero_station_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY obs_aero
    ADD CONSTRAINT obs_aero_station_no_fkey FOREIGN KEY (station_no) REFERENCES stations(station_no);


--
-- Name: obs_aws_station_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY obs_aws
    ADD CONSTRAINT obs_aws_station_no_fkey FOREIGN KEY (station_no) REFERENCES stations(station_no);


--
-- Name: obs_daily_station_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY obs_daily
    ADD CONSTRAINT obs_daily_station_no_fkey FOREIGN KEY (station_no) REFERENCES stations(station_no);


--
-- Name: obs_subdaily_cloud_layers_subdaily_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY obs_subdaily_cloud_layers
    ADD CONSTRAINT obs_subdaily_cloud_layers_subdaily_id_fkey FOREIGN KEY (sub_daily_id) REFERENCES obs_subdaily(id);


--
-- Name: obs_subdaily_station_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY obs_subdaily
    ADD CONSTRAINT obs_subdaily_station_no_fkey FOREIGN KEY (station_no) REFERENCES stations(station_no);


--
-- Name: obs_upper_air_station_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY obs_upper_air
    ADD CONSTRAINT obs_upper_air_station_no_fkey FOREIGN KEY (station_no) REFERENCES stations(station_no);


--
-- Name: station_audit_audit_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY station_audit
    ADD CONSTRAINT station_audit_audit_type_id_fkey FOREIGN KEY (audit_type_id) REFERENCES station_audit_types(id);


--
-- Name: station_audit_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY station_audit
    ADD CONSTRAINT station_audit_station_id_fkey FOREIGN KEY (station_id) REFERENCES stations(id);


--
-- Name: station_class_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY station_class
    ADD CONSTRAINT station_class_station_id_fkey FOREIGN KEY (station_id) REFERENCES stations(id);


--
-- Name: station_class_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY station_class
    ADD CONSTRAINT station_class_type_id_fkey FOREIGN KEY (type_id) REFERENCES station_types(id);


--
-- Name: station_contacts_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY station_contacts
    ADD CONSTRAINT station_contacts_station_id_fkey FOREIGN KEY (station_id) REFERENCES stations(id);


--
-- Name: station_equipment_equipment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY station_equipment
    ADD CONSTRAINT station_equipment_equipment_id_fkey FOREIGN KEY (equipment_id) REFERENCES equipment(id);


--
-- Name: station_equipment_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY station_equipment
    ADD CONSTRAINT station_equipment_station_id_fkey FOREIGN KEY (station_id) REFERENCES stations(id);


--
-- Name: station_files_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY station_files
    ADD CONSTRAINT station_files_station_id_fkey FOREIGN KEY (station_id) REFERENCES stations(id);


--
-- Name: stations_country_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY stations
    ADD CONSTRAINT stations_country_code_fkey FOREIGN KEY (country_code) REFERENCES station_countries(iso_code);


--
-- Name: stations_land_use_0_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY stations
    ADD CONSTRAINT stations_land_use_0_id_fkey FOREIGN KEY (lu_0_100m) REFERENCES land_use(id);


--
-- Name: stations_land_use_100_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY stations
    ADD CONSTRAINT stations_land_use_100_id_fkey FOREIGN KEY (lu_100m_1km) REFERENCES land_use(id);


--
-- Name: stations_land_use_1km_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY stations
    ADD CONSTRAINT stations_land_use_1km_id_fkey FOREIGN KEY (lu_1km_10km) REFERENCES land_use(id);


--
-- Name: stations_location_datum_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY stations
    ADD CONSTRAINT stations_location_datum_fkey FOREIGN KEY (location_datum) REFERENCES datums(datum_name) ON UPDATE CASCADE;


--
-- Name: stations_location_epsg_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY stations
    ADD CONSTRAINT stations_location_epsg_fkey FOREIGN KEY (location_epsg) REFERENCES spatial_ref_sys(srid) ON UPDATE CASCADE;


--
-- Name: stations_soil_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY stations
    ADD CONSTRAINT stations_soil_type_id_fkey FOREIGN KEY (soil_type) REFERENCES soil_types(id);


--
-- Name: stations_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY stations
    ADD CONSTRAINT stations_status_id_fkey FOREIGN KEY (status_id) REFERENCES station_status(id);


--
-- Name: stations_surface_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY stations
    ADD CONSTRAINT stations_surface_type_id_fkey FOREIGN KEY (surface_type) REFERENCES surface_types(id);


--
-- Name: stations_time_zone_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY stations
    ADD CONSTRAINT stations_time_zone_fkey FOREIGN KEY (time_zone) REFERENCES station_timezones(tm_zone);


--
-- Name: timezone_diffs; Type: FK CONSTRAINT; Schema: public; Owner: clidegui
--

ALTER TABLE ONLY timezone_diffs
    ADD CONSTRAINT timezone_diffs FOREIGN KEY (tm_zone) REFERENCES station_timezones(tm_zone);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: climat_data(character varying, date); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON FUNCTION climat_data(station_no character varying, yyyy_mm date) FROM PUBLIC;
REVOKE ALL ON FUNCTION climat_data(station_no character varying, yyyy_mm date) FROM postgres;
GRANT ALL ON FUNCTION climat_data(station_no character varying, yyyy_mm date) TO postgres;
GRANT ALL ON FUNCTION climat_data(station_no character varying, yyyy_mm date) TO PUBLIC;


--
-- Name: iif_sql(boolean, anyelement, anyelement); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON FUNCTION iif_sql(boolean, anyelement, anyelement) FROM PUBLIC;
REVOKE ALL ON FUNCTION iif_sql(boolean, anyelement, anyelement) FROM postgres;
GRANT ALL ON FUNCTION iif_sql(boolean, anyelement, anyelement) TO postgres;
GRANT ALL ON FUNCTION iif_sql(boolean, anyelement, anyelement) TO PUBLIC;
GRANT ALL ON FUNCTION iif_sql(boolean, anyelement, anyelement) TO clide;


--
-- Name: key_summary(date, date); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON FUNCTION key_summary(from_date date, to_date date) FROM PUBLIC;
REVOKE ALL ON FUNCTION key_summary(from_date date, to_date date) FROM postgres;
GRANT ALL ON FUNCTION key_summary(from_date date, to_date date) TO postgres;
GRANT ALL ON FUNCTION key_summary(from_date date, to_date date) TO PUBLIC;
GRANT ALL ON FUNCTION key_summary(from_date date, to_date date) TO clidegui;
GRANT ALL ON FUNCTION key_summary(from_date date, to_date date) TO clide;


--
-- Name: key_summary_with_stations(date, date); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON FUNCTION key_summary_with_stations(from_date date, to_date date) FROM PUBLIC;
REVOKE ALL ON FUNCTION key_summary_with_stations(from_date date, to_date date) FROM postgres;
GRANT ALL ON FUNCTION key_summary_with_stations(from_date date, to_date date) TO postgres;
GRANT ALL ON FUNCTION key_summary_with_stations(from_date date, to_date date) TO PUBLIC;
GRANT ALL ON FUNCTION key_summary_with_stations(from_date date, to_date date) TO clidegui;
GRANT ALL ON FUNCTION key_summary_with_stations(from_date date, to_date date) TO clide;


--
-- Name: lct_to_lsd(character varying, character varying); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON FUNCTION lct_to_lsd(station character varying, lct character varying) FROM PUBLIC;
REVOKE ALL ON FUNCTION lct_to_lsd(station character varying, lct character varying) FROM postgres;
GRANT ALL ON FUNCTION lct_to_lsd(station character varying, lct character varying) TO postgres;
GRANT ALL ON FUNCTION lct_to_lsd(station character varying, lct character varying) TO PUBLIC;
GRANT ALL ON FUNCTION lct_to_lsd(station character varying, lct character varying) TO clide;


--
-- Name: lct_to_utc(character varying, character varying); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON FUNCTION lct_to_utc(station character varying, lct character varying) FROM PUBLIC;
REVOKE ALL ON FUNCTION lct_to_utc(station character varying, lct character varying) FROM postgres;
GRANT ALL ON FUNCTION lct_to_utc(station character varying, lct character varying) TO postgres;
GRANT ALL ON FUNCTION lct_to_utc(station character varying, lct character varying) TO PUBLIC;
GRANT ALL ON FUNCTION lct_to_utc(station character varying, lct character varying) TO clide;


--
-- Name: lsd_to_lct(character varying, character varying); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON FUNCTION lsd_to_lct(station character varying, lsd character varying) FROM PUBLIC;
REVOKE ALL ON FUNCTION lsd_to_lct(station character varying, lsd character varying) FROM postgres;
GRANT ALL ON FUNCTION lsd_to_lct(station character varying, lsd character varying) TO postgres;
GRANT ALL ON FUNCTION lsd_to_lct(station character varying, lsd character varying) TO PUBLIC;
GRANT ALL ON FUNCTION lsd_to_lct(station character varying, lsd character varying) TO clide;


--
-- Name: lsd_to_utc(character varying, character varying); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON FUNCTION lsd_to_utc(station character varying, lsd character varying) FROM PUBLIC;
REVOKE ALL ON FUNCTION lsd_to_utc(station character varying, lsd character varying) FROM postgres;
GRANT ALL ON FUNCTION lsd_to_utc(station character varying, lsd character varying) TO postgres;
GRANT ALL ON FUNCTION lsd_to_utc(station character varying, lsd character varying) TO PUBLIC;
GRANT ALL ON FUNCTION lsd_to_utc(station character varying, lsd character varying) TO clide;


--
-- Name: monthly_obs(character varying[], character varying, character varying); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON FUNCTION monthly_obs(station_array character varying[], nfrom character varying, nto character varying) FROM PUBLIC;
REVOKE ALL ON FUNCTION monthly_obs(station_array character varying[], nfrom character varying, nto character varying) FROM postgres;
GRANT ALL ON FUNCTION monthly_obs(station_array character varying[], nfrom character varying, nto character varying) TO postgres;
GRANT ALL ON FUNCTION monthly_obs(station_array character varying[], nfrom character varying, nto character varying) TO PUBLIC;
GRANT ALL ON FUNCTION monthly_obs(station_array character varying[], nfrom character varying, nto character varying) TO clide;


--
-- Name: monthly_rain_quintile(character varying, character varying, numeric, character varying, character varying); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON FUNCTION monthly_rain_quintile(station character varying, month character varying, inrain numeric, nfrom character varying, nto character varying) FROM PUBLIC;
REVOKE ALL ON FUNCTION monthly_rain_quintile(station character varying, month character varying, inrain numeric, nfrom character varying, nto character varying) FROM postgres;
GRANT ALL ON FUNCTION monthly_rain_quintile(station character varying, month character varying, inrain numeric, nfrom character varying, nto character varying) TO postgres;
GRANT ALL ON FUNCTION monthly_rain_quintile(station character varying, month character varying, inrain numeric, nfrom character varying, nto character varying) TO PUBLIC;
GRANT ALL ON FUNCTION monthly_rain_quintile(station character varying, month character varying, inrain numeric, nfrom character varying, nto character varying) TO clide;


--
-- Name: obs_monthly_summary(character varying, date, time without time zone); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON FUNCTION obs_monthly_summary(stat_no character varying, yyyy_mm date, subdaily_time time without time zone) FROM PUBLIC;
REVOKE ALL ON FUNCTION obs_monthly_summary(stat_no character varying, yyyy_mm date, subdaily_time time without time zone) FROM postgres;
GRANT ALL ON FUNCTION obs_monthly_summary(stat_no character varying, yyyy_mm date, subdaily_time time without time zone) TO postgres;
GRANT ALL ON FUNCTION obs_monthly_summary(stat_no character varying, yyyy_mm date, subdaily_time time without time zone) TO PUBLIC;


--
-- Name: obs_monthly_summary_high(character varying, date, time without time zone); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON FUNCTION obs_monthly_summary_high(stat_no character varying, yyyy_mm date, subdaily_time time without time zone) FROM PUBLIC;
REVOKE ALL ON FUNCTION obs_monthly_summary_high(stat_no character varying, yyyy_mm date, subdaily_time time without time zone) FROM postgres;
GRANT ALL ON FUNCTION obs_monthly_summary_high(stat_no character varying, yyyy_mm date, subdaily_time time without time zone) TO postgres;
GRANT ALL ON FUNCTION obs_monthly_summary_high(stat_no character varying, yyyy_mm date, subdaily_time time without time zone) TO PUBLIC;


--
-- Name: utc_to_lct(character varying, character varying); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON FUNCTION utc_to_lct(station character varying, utc character varying) FROM PUBLIC;
REVOKE ALL ON FUNCTION utc_to_lct(station character varying, utc character varying) FROM postgres;
GRANT ALL ON FUNCTION utc_to_lct(station character varying, utc character varying) TO postgres;
GRANT ALL ON FUNCTION utc_to_lct(station character varying, utc character varying) TO PUBLIC;
GRANT ALL ON FUNCTION utc_to_lct(station character varying, utc character varying) TO clide;


--
-- Name: utc_to_lsd(character varying, character varying); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON FUNCTION utc_to_lsd(station character varying, utc character varying) FROM PUBLIC;
REVOKE ALL ON FUNCTION utc_to_lsd(station character varying, utc character varying) FROM postgres;
GRANT ALL ON FUNCTION utc_to_lsd(station character varying, utc character varying) TO postgres;
GRANT ALL ON FUNCTION utc_to_lsd(station character varying, utc character varying) TO PUBLIC;
GRANT ALL ON FUNCTION utc_to_lsd(station character varying, utc character varying) TO clide;


--
-- Name: cdms_get_ext_views; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE cdms_get_ext_views FROM PUBLIC;
REVOKE ALL ON TABLE cdms_get_ext_views FROM clidegui;
GRANT ALL ON TABLE cdms_get_ext_views TO clidegui;
GRANT SELECT ON TABLE cdms_get_ext_views TO clide;


--
-- Name: codes_simple_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE codes_simple_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE codes_simple_id FROM clidegui;
GRANT ALL ON SEQUENCE codes_simple_id TO clidegui;
GRANT SELECT ON SEQUENCE codes_simple_id TO clide;


--
-- Name: codes_simple; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE codes_simple FROM PUBLIC;
REVOKE ALL ON TABLE codes_simple FROM clidegui;
GRANT ALL ON TABLE codes_simple TO clidegui;
GRANT SELECT ON TABLE codes_simple TO clide;


--
-- Name: equipment_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE equipment_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE equipment_id FROM clidegui;
GRANT ALL ON SEQUENCE equipment_id TO clidegui;
GRANT SELECT ON SEQUENCE equipment_id TO clide;


--
-- Name: equipment; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE equipment FROM PUBLIC;
REVOKE ALL ON TABLE equipment FROM clidegui;
GRANT ALL ON TABLE equipment TO clidegui;
GRANT SELECT ON TABLE equipment TO clide;


--
-- Name: station_types_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE station_types_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE station_types_id FROM clidegui;
GRANT ALL ON SEQUENCE station_types_id TO clidegui;
GRANT SELECT ON SEQUENCE station_types_id TO clide;


--
-- Name: station_types; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE station_types FROM PUBLIC;
REVOKE ALL ON TABLE station_types FROM clidegui;
GRANT ALL ON TABLE station_types TO clidegui;
GRANT SELECT ON TABLE station_types TO clide;


--
-- Name: ext_class; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_class FROM PUBLIC;
REVOKE ALL ON TABLE ext_class FROM clidegui;
GRANT ALL ON TABLE ext_class TO clidegui;
GRANT SELECT ON TABLE ext_class TO clide;


--
-- Name: ext_equipment; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_equipment FROM PUBLIC;
REVOKE ALL ON TABLE ext_equipment FROM clidegui;
GRANT ALL ON TABLE ext_equipment TO clidegui;
GRANT SELECT ON TABLE ext_equipment TO clide;


--
-- Name: obs_aero_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obs_aero_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obs_aero_id FROM clidegui;
GRANT ALL ON SEQUENCE obs_aero_id TO clidegui;
GRANT SELECT ON SEQUENCE obs_aero_id TO clide;


--
-- Name: obs_aero; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obs_aero FROM PUBLIC;
REVOKE ALL ON TABLE obs_aero FROM clidegui;
GRANT ALL ON TABLE obs_aero TO clidegui;
GRANT SELECT ON TABLE obs_aero TO clide;


--
-- Name: ext_obs_aero; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_obs_aero FROM PUBLIC;
REVOKE ALL ON TABLE ext_obs_aero FROM clidegui;
GRANT ALL ON TABLE ext_obs_aero TO clidegui;
GRANT SELECT ON TABLE ext_obs_aero TO clide;


--
-- Name: obs_aws_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obs_aws_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obs_aws_id FROM clidegui;
GRANT ALL ON SEQUENCE obs_aws_id TO clidegui;
GRANT SELECT ON SEQUENCE obs_aws_id TO clide;


--
-- Name: obs_aws; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obs_aws FROM PUBLIC;
REVOKE ALL ON TABLE obs_aws FROM clidegui;
GRANT ALL ON TABLE obs_aws TO clidegui;
GRANT SELECT ON TABLE obs_aws TO clide;


--
-- Name: ext_obs_aws; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_obs_aws FROM PUBLIC;
REVOKE ALL ON TABLE ext_obs_aws FROM clidegui;
GRANT ALL ON TABLE ext_obs_aws TO clidegui;
GRANT SELECT ON TABLE ext_obs_aws TO clide;


--
-- Name: obs_daily_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obs_daily_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obs_daily_id FROM clidegui;
GRANT ALL ON SEQUENCE obs_daily_id TO clidegui;
GRANT SELECT ON SEQUENCE obs_daily_id TO clide;


--
-- Name: obs_daily; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obs_daily FROM PUBLIC;
REVOKE ALL ON TABLE obs_daily FROM clidegui;
GRANT ALL ON TABLE obs_daily TO clidegui;
GRANT SELECT ON TABLE obs_daily TO clide;
GRANT SELECT ON TABLE obs_daily TO datacomp;


--
-- Name: obs_subdaily_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obs_subdaily_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obs_subdaily_id FROM clidegui;
GRANT ALL ON SEQUENCE obs_subdaily_id TO clidegui;
GRANT SELECT ON SEQUENCE obs_subdaily_id TO clide;


--
-- Name: obs_subdaily; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obs_subdaily FROM PUBLIC;
REVOKE ALL ON TABLE obs_subdaily FROM clidegui;
GRANT ALL ON TABLE obs_subdaily TO clidegui;
GRANT SELECT ON TABLE obs_subdaily TO clide;
GRANT SELECT ON TABLE obs_subdaily TO datacomp;


--
-- Name: ext_obs_climat; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_obs_climat FROM PUBLIC;
REVOKE ALL ON TABLE ext_obs_climat FROM clidegui;
GRANT ALL ON TABLE ext_obs_climat TO clidegui;
GRANT SELECT ON TABLE ext_obs_climat TO clide;


--
-- Name: ext_obs_daily_basics; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_obs_daily_basics FROM PUBLIC;
REVOKE ALL ON TABLE ext_obs_daily_basics FROM clidegui;
GRANT ALL ON TABLE ext_obs_daily_basics TO clidegui;
GRANT SELECT ON TABLE ext_obs_daily_basics TO clide;


--
-- Name: obs_monthly; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obs_monthly FROM PUBLIC;
REVOKE ALL ON TABLE obs_monthly FROM clidegui;
GRANT ALL ON TABLE obs_monthly TO clidegui;
GRANT SELECT ON TABLE obs_monthly TO clide;


--
-- Name: ext_obs_monthly; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_obs_monthly FROM PUBLIC;
REVOKE ALL ON TABLE ext_obs_monthly FROM clidegui;
GRANT ALL ON TABLE ext_obs_monthly TO clidegui;
GRANT SELECT ON TABLE ext_obs_monthly TO clide;


--
-- Name: ext_obs_monthly_calculated; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_obs_monthly_calculated FROM PUBLIC;
REVOKE ALL ON TABLE ext_obs_monthly_calculated FROM clidegui;
GRANT ALL ON TABLE ext_obs_monthly_calculated TO clidegui;
GRANT SELECT ON TABLE ext_obs_monthly_calculated TO clide;


--
-- Name: ext_obs_monthly_combined; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_obs_monthly_combined FROM PUBLIC;
REVOKE ALL ON TABLE ext_obs_monthly_combined FROM clidegui;
GRANT ALL ON TABLE ext_obs_monthly_combined TO clidegui;
GRANT SELECT ON TABLE ext_obs_monthly_combined TO clide;


--
-- Name: ext_obs_subdaily; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_obs_subdaily FROM PUBLIC;
REVOKE ALL ON TABLE ext_obs_subdaily FROM clidegui;
GRANT ALL ON TABLE ext_obs_subdaily TO clidegui;
GRANT SELECT ON TABLE ext_obs_subdaily TO clide;


--
-- Name: obs_subdaily_cloud_layers_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obs_subdaily_cloud_layers_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obs_subdaily_cloud_layers_id FROM clidegui;
GRANT ALL ON SEQUENCE obs_subdaily_cloud_layers_id TO clidegui;
GRANT SELECT ON SEQUENCE obs_subdaily_cloud_layers_id TO clide;


--
-- Name: obs_subdaily_cloud_layers; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obs_subdaily_cloud_layers FROM PUBLIC;
REVOKE ALL ON TABLE obs_subdaily_cloud_layers FROM clidegui;
GRANT ALL ON TABLE obs_subdaily_cloud_layers TO clidegui;
GRANT SELECT ON TABLE obs_subdaily_cloud_layers TO clide;


--
-- Name: ext_obs_subdaily_cloud_layers; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_obs_subdaily_cloud_layers FROM PUBLIC;
REVOKE ALL ON TABLE ext_obs_subdaily_cloud_layers FROM clidegui;
GRANT ALL ON TABLE ext_obs_subdaily_cloud_layers TO clidegui;
GRANT SELECT ON TABLE ext_obs_subdaily_cloud_layers TO clide;


--
-- Name: obs_subdaily_soil_temps_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obs_subdaily_soil_temps_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obs_subdaily_soil_temps_id FROM clidegui;
GRANT ALL ON SEQUENCE obs_subdaily_soil_temps_id TO clidegui;
GRANT SELECT ON SEQUENCE obs_subdaily_soil_temps_id TO clide;


--
-- Name: obs_subdaily_soil_temps; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obs_subdaily_soil_temps FROM PUBLIC;
REVOKE ALL ON TABLE obs_subdaily_soil_temps FROM clidegui;
GRANT ALL ON TABLE obs_subdaily_soil_temps TO clidegui;
GRANT SELECT ON TABLE obs_subdaily_soil_temps TO clide;


--
-- Name: ext_obs_subdaily_soil_temps; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_obs_subdaily_soil_temps FROM PUBLIC;
REVOKE ALL ON TABLE ext_obs_subdaily_soil_temps FROM clidegui;
GRANT ALL ON TABLE ext_obs_subdaily_soil_temps TO clidegui;
GRANT SELECT ON TABLE ext_obs_subdaily_soil_temps TO clide;


--
-- Name: obs_upper_air_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obs_upper_air_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obs_upper_air_id FROM clidegui;
GRANT ALL ON SEQUENCE obs_upper_air_id TO clidegui;
GRANT SELECT ON SEQUENCE obs_upper_air_id TO clide;


--
-- Name: obs_upper_air; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obs_upper_air FROM PUBLIC;
REVOKE ALL ON TABLE obs_upper_air FROM clidegui;
GRANT ALL ON TABLE obs_upper_air TO clidegui;
GRANT SELECT ON TABLE obs_upper_air TO clide;


--
-- Name: ext_obs_upper_air; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_obs_upper_air FROM PUBLIC;
REVOKE ALL ON TABLE ext_obs_upper_air FROM clidegui;
GRANT ALL ON TABLE ext_obs_upper_air TO clidegui;
GRANT SELECT ON TABLE ext_obs_upper_air TO clide;


--
-- Name: station_audit_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE station_audit_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE station_audit_id FROM clidegui;
GRANT ALL ON SEQUENCE station_audit_id TO clidegui;
GRANT SELECT ON SEQUENCE station_audit_id TO clide;


--
-- Name: station_audit; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE station_audit FROM PUBLIC;
REVOKE ALL ON TABLE station_audit FROM clidegui;
GRANT ALL ON TABLE station_audit TO clidegui;
GRANT SELECT ON TABLE station_audit TO clide;


--
-- Name: station_audit_type_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE station_audit_type_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE station_audit_type_id FROM clidegui;
GRANT ALL ON SEQUENCE station_audit_type_id TO clidegui;
GRANT SELECT ON SEQUENCE station_audit_type_id TO clide;


--
-- Name: station_audit_types; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE station_audit_types FROM PUBLIC;
REVOKE ALL ON TABLE station_audit_types FROM clidegui;
GRANT ALL ON TABLE station_audit_types TO clidegui;
GRANT SELECT ON TABLE station_audit_types TO clide;


--
-- Name: stations_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE stations_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE stations_id FROM clidegui;
GRANT ALL ON SEQUENCE stations_id TO clidegui;
GRANT SELECT ON SEQUENCE stations_id TO clide;


--
-- Name: stations; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE stations FROM PUBLIC;
REVOKE ALL ON TABLE stations FROM clidegui;
GRANT ALL ON TABLE stations TO clidegui;
GRANT SELECT ON TABLE stations TO clide;


--
-- Name: ext_station_audit; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_station_audit FROM PUBLIC;
REVOKE ALL ON TABLE ext_station_audit FROM clidegui;
GRANT ALL ON TABLE ext_station_audit TO clidegui;
GRANT SELECT ON TABLE ext_station_audit TO clide;


--
-- Name: station_class_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE station_class_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE station_class_id FROM clidegui;
GRANT ALL ON SEQUENCE station_class_id TO clidegui;
GRANT SELECT ON SEQUENCE station_class_id TO clide;


--
-- Name: station_class; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE station_class FROM PUBLIC;
REVOKE ALL ON TABLE station_class FROM clidegui;
GRANT ALL ON TABLE station_class TO clidegui;
GRANT SELECT ON TABLE station_class TO clide;


--
-- Name: ext_station_class; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_station_class FROM PUBLIC;
REVOKE ALL ON TABLE ext_station_class FROM clidegui;
GRANT ALL ON TABLE ext_station_class TO clidegui;
GRANT SELECT ON TABLE ext_station_class TO clide;


--
-- Name: station_equipment_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE station_equipment_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE station_equipment_id FROM clidegui;
GRANT ALL ON SEQUENCE station_equipment_id TO clidegui;
GRANT SELECT ON SEQUENCE station_equipment_id TO clide;


--
-- Name: station_equipment; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE station_equipment FROM PUBLIC;
REVOKE ALL ON TABLE station_equipment FROM clidegui;
GRANT ALL ON TABLE station_equipment TO clidegui;
GRANT SELECT ON TABLE station_equipment TO clide;


--
-- Name: ext_station_equipment; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_station_equipment FROM PUBLIC;
REVOKE ALL ON TABLE ext_station_equipment FROM clidegui;
GRANT ALL ON TABLE ext_station_equipment TO clidegui;
GRANT SELECT ON TABLE ext_station_equipment TO clide;


--
-- Name: land_use_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE land_use_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE land_use_id FROM clidegui;
GRANT ALL ON SEQUENCE land_use_id TO clidegui;
GRANT SELECT ON SEQUENCE land_use_id TO clide;


--
-- Name: land_use; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE land_use FROM PUBLIC;
REVOKE ALL ON TABLE land_use FROM clidegui;
GRANT ALL ON TABLE land_use TO clidegui;
GRANT SELECT ON TABLE land_use TO clide;


--
-- Name: soil_types_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE soil_types_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE soil_types_id FROM clidegui;
GRANT ALL ON SEQUENCE soil_types_id TO clidegui;
GRANT SELECT ON SEQUENCE soil_types_id TO clide;


--
-- Name: soil_types; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE soil_types FROM PUBLIC;
REVOKE ALL ON TABLE soil_types FROM clidegui;
GRANT ALL ON TABLE soil_types TO clidegui;
GRANT SELECT ON TABLE soil_types TO clide;


--
-- Name: station_countries_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE station_countries_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE station_countries_id FROM clidegui;
GRANT ALL ON SEQUENCE station_countries_id TO clidegui;
GRANT SELECT ON SEQUENCE station_countries_id TO clide;


--
-- Name: station_countries; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE station_countries FROM PUBLIC;
REVOKE ALL ON TABLE station_countries FROM clidegui;
GRANT ALL ON TABLE station_countries TO clidegui;
GRANT SELECT ON TABLE station_countries TO clide;


--
-- Name: station_status_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE station_status_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE station_status_id FROM clidegui;
GRANT ALL ON SEQUENCE station_status_id TO clidegui;
GRANT SELECT ON SEQUENCE station_status_id TO clide;


--
-- Name: station_status; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE station_status FROM PUBLIC;
REVOKE ALL ON TABLE station_status FROM clidegui;
GRANT ALL ON TABLE station_status TO clidegui;
GRANT SELECT ON TABLE station_status TO clide;


--
-- Name: station_timezones_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE station_timezones_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE station_timezones_id FROM clidegui;
GRANT ALL ON SEQUENCE station_timezones_id TO clidegui;
GRANT SELECT ON SEQUENCE station_timezones_id TO clide;


--
-- Name: station_timezones; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE station_timezones FROM PUBLIC;
REVOKE ALL ON TABLE station_timezones FROM clidegui;
GRANT ALL ON TABLE station_timezones TO clidegui;
GRANT SELECT ON TABLE station_timezones TO clide;


--
-- Name: surface_types_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE surface_types_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE surface_types_id FROM clidegui;
GRANT ALL ON SEQUENCE surface_types_id TO clidegui;
GRANT SELECT ON SEQUENCE surface_types_id TO clide;


--
-- Name: surface_types; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE surface_types FROM PUBLIC;
REVOKE ALL ON TABLE surface_types FROM clidegui;
GRANT ALL ON TABLE surface_types TO clidegui;
GRANT SELECT ON TABLE surface_types TO clide;


--
-- Name: ext_stations; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ext_stations FROM PUBLIC;
REVOKE ALL ON TABLE ext_stations FROM clidegui;
GRANT ALL ON TABLE ext_stations TO clidegui;
GRANT SELECT ON TABLE ext_stations TO clide;


--
-- Name: gui_users_id_seq; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE gui_users_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE gui_users_id_seq FROM clidegui;
GRANT ALL ON SEQUENCE gui_users_id_seq TO clidegui;


--
-- Name: gui_users; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE gui_users FROM PUBLIC;
REVOKE ALL ON TABLE gui_users FROM clidegui;
GRANT ALL ON TABLE gui_users TO clidegui;


--
-- Name: ingest_monitor; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE ingest_monitor FROM PUBLIC;
REVOKE ALL ON TABLE ingest_monitor FROM clidegui;
GRANT ALL ON TABLE ingest_monitor TO clidegui;
GRANT SELECT ON TABLE ingest_monitor TO clide;


--
-- Name: key_settings; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE key_settings FROM PUBLIC;
REVOKE ALL ON TABLE key_settings FROM clidegui;
GRANT ALL ON TABLE key_settings TO clidegui;
GRANT SELECT ON TABLE key_settings TO clide;


--
-- Name: obs_audit_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obs_audit_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obs_audit_id FROM clidegui;
GRANT ALL ON SEQUENCE obs_audit_id TO clidegui;
GRANT SELECT ON SEQUENCE obs_audit_id TO clide;


--
-- Name: obs_audit; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obs_audit FROM PUBLIC;
REVOKE ALL ON TABLE obs_audit FROM clidegui;
GRANT ALL ON TABLE obs_audit TO clidegui;
GRANT SELECT ON TABLE obs_audit TO clide;


--
-- Name: obs_averages; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obs_averages FROM PUBLIC;
REVOKE ALL ON TABLE obs_averages FROM clidegui;
GRANT ALL ON TABLE obs_averages TO clidegui;
GRANT SELECT ON TABLE obs_averages TO clide;


--
-- Name: obs_clicom_element_map_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obs_clicom_element_map_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obs_clicom_element_map_id FROM clidegui;
GRANT ALL ON SEQUENCE obs_clicom_element_map_id TO clidegui;
GRANT SELECT ON SEQUENCE obs_clicom_element_map_id TO clide;


--
-- Name: obs_clicom_element_map; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obs_clicom_element_map FROM PUBLIC;
REVOKE ALL ON TABLE obs_clicom_element_map FROM clidegui;
GRANT ALL ON TABLE obs_clicom_element_map TO clidegui;
GRANT SELECT ON TABLE obs_clicom_element_map TO clide;


--
-- Name: obscodes_cloud_amt_conv_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obscodes_cloud_amt_conv_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obscodes_cloud_amt_conv_id FROM clidegui;
GRANT ALL ON SEQUENCE obscodes_cloud_amt_conv_id TO clidegui;
GRANT SELECT ON SEQUENCE obscodes_cloud_amt_conv_id TO clide;


--
-- Name: obscodes_cloud_amt_conv; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obscodes_cloud_amt_conv FROM PUBLIC;
REVOKE ALL ON TABLE obscodes_cloud_amt_conv FROM clidegui;
GRANT ALL ON TABLE obscodes_cloud_amt_conv TO clidegui;
GRANT SELECT ON TABLE obscodes_cloud_amt_conv TO clide;


--
-- Name: obscodes_cloud_conv_1677_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obscodes_cloud_conv_1677_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obscodes_cloud_conv_1677_id FROM clidegui;
GRANT ALL ON SEQUENCE obscodes_cloud_conv_1677_id TO clidegui;
GRANT SELECT ON SEQUENCE obscodes_cloud_conv_1677_id TO clide;


--
-- Name: obscodes_cloud_conv_1677; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obscodes_cloud_conv_1677 FROM PUBLIC;
REVOKE ALL ON TABLE obscodes_cloud_conv_1677 FROM clidegui;
GRANT ALL ON TABLE obscodes_cloud_conv_1677 TO clidegui;
GRANT SELECT ON TABLE obscodes_cloud_conv_1677 TO clide;


--
-- Name: obscodes_cloud_ht_conv_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obscodes_cloud_ht_conv_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obscodes_cloud_ht_conv_id FROM clidegui;
GRANT ALL ON SEQUENCE obscodes_cloud_ht_conv_id TO clidegui;
GRANT SELECT ON SEQUENCE obscodes_cloud_ht_conv_id TO clide;


--
-- Name: obscodes_cloud_ht_conv; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obscodes_cloud_ht_conv FROM PUBLIC;
REVOKE ALL ON TABLE obscodes_cloud_ht_conv FROM clidegui;
GRANT ALL ON TABLE obscodes_cloud_ht_conv TO clidegui;
GRANT SELECT ON TABLE obscodes_cloud_ht_conv TO clide;


--
-- Name: obscodes_cloud_type_conv_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obscodes_cloud_type_conv_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obscodes_cloud_type_conv_id FROM clidegui;
GRANT ALL ON SEQUENCE obscodes_cloud_type_conv_id TO clidegui;
GRANT SELECT ON SEQUENCE obscodes_cloud_type_conv_id TO clide;


--
-- Name: obscodes_cloud_type_conv; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obscodes_cloud_type_conv FROM PUBLIC;
REVOKE ALL ON TABLE obscodes_cloud_type_conv FROM clidegui;
GRANT ALL ON TABLE obscodes_cloud_type_conv TO clidegui;
GRANT SELECT ON TABLE obscodes_cloud_type_conv TO clide;


--
-- Name: obscodes_visibility_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obscodes_visibility_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obscodes_visibility_id FROM clidegui;
GRANT ALL ON SEQUENCE obscodes_visibility_id TO clidegui;
GRANT SELECT ON SEQUENCE obscodes_visibility_id TO clide;


--
-- Name: obscodes_visibility; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obscodes_visibility FROM PUBLIC;
REVOKE ALL ON TABLE obscodes_visibility FROM clidegui;
GRANT ALL ON TABLE obscodes_visibility TO clidegui;
GRANT SELECT ON TABLE obscodes_visibility TO clide;


--
-- Name: obscodes_wind_dir_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obscodes_wind_dir_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obscodes_wind_dir_id FROM clidegui;
GRANT ALL ON SEQUENCE obscodes_wind_dir_id TO clidegui;
GRANT SELECT ON SEQUENCE obscodes_wind_dir_id TO clide;


--
-- Name: obscodes_wind_dir; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obscodes_wind_dir FROM PUBLIC;
REVOKE ALL ON TABLE obscodes_wind_dir FROM clidegui;
GRANT ALL ON TABLE obscodes_wind_dir TO clidegui;
GRANT SELECT ON TABLE obscodes_wind_dir TO clide;


--
-- Name: obscodes_wind_speed_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obscodes_wind_speed_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obscodes_wind_speed_id FROM clidegui;
GRANT ALL ON SEQUENCE obscodes_wind_speed_id TO clidegui;
GRANT SELECT ON SEQUENCE obscodes_wind_speed_id TO clide;


--
-- Name: obscodes_wind_speed; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obscodes_wind_speed FROM PUBLIC;
REVOKE ALL ON TABLE obscodes_wind_speed FROM clidegui;
GRANT ALL ON TABLE obscodes_wind_speed TO clidegui;
GRANT SELECT ON TABLE obscodes_wind_speed TO clide;


--
-- Name: obscodes_wx_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obscodes_wx_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obscodes_wx_id FROM clidegui;
GRANT ALL ON SEQUENCE obscodes_wx_id TO clidegui;
GRANT SELECT ON SEQUENCE obscodes_wx_id TO clide;


--
-- Name: obscodes_wx; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obscodes_wx FROM PUBLIC;
REVOKE ALL ON TABLE obscodes_wx FROM clidegui;
GRANT ALL ON TABLE obscodes_wx TO clidegui;
GRANT SELECT ON TABLE obscodes_wx TO clide;


--
-- Name: obsconv_factors_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE obsconv_factors_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE obsconv_factors_id FROM clidegui;
GRANT ALL ON SEQUENCE obsconv_factors_id TO clidegui;
GRANT SELECT ON SEQUENCE obsconv_factors_id TO clide;


--
-- Name: obsconv_factors; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE obsconv_factors FROM PUBLIC;
REVOKE ALL ON TABLE obsconv_factors FROM clidegui;
GRANT ALL ON TABLE obsconv_factors TO clidegui;
GRANT SELECT ON TABLE obsconv_factors TO clide;


--
-- Name: pivot; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE pivot FROM PUBLIC;
REVOKE ALL ON TABLE pivot FROM clidegui;
GRANT ALL ON TABLE pivot TO clidegui;
GRANT SELECT ON TABLE pivot TO PUBLIC;


--
-- Name: spatial_ref_sys; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE spatial_ref_sys FROM PUBLIC;
REVOKE ALL ON TABLE spatial_ref_sys FROM clidegui;
GRANT ALL ON TABLE spatial_ref_sys TO clidegui;
GRANT SELECT ON TABLE spatial_ref_sys TO clide;


--
-- Name: station_contacts_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE station_contacts_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE station_contacts_id FROM clidegui;
GRANT ALL ON SEQUENCE station_contacts_id TO clidegui;
GRANT SELECT ON SEQUENCE station_contacts_id TO clide;


--
-- Name: station_contacts; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE station_contacts FROM PUBLIC;
REVOKE ALL ON TABLE station_contacts FROM clidegui;
GRANT ALL ON TABLE station_contacts TO clidegui;
GRANT SELECT ON TABLE station_contacts TO clide;


--
-- Name: station_files_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE station_files_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE station_files_id FROM clidegui;
GRANT ALL ON SEQUENCE station_files_id TO clidegui;
GRANT SELECT ON SEQUENCE station_files_id TO clide;


--
-- Name: station_files; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE station_files FROM PUBLIC;
REVOKE ALL ON TABLE station_files FROM clidegui;
GRANT ALL ON TABLE station_files TO clidegui;
GRANT SELECT ON TABLE station_files TO clide;


--
-- Name: timezone_diffs_id; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON SEQUENCE timezone_diffs_id FROM PUBLIC;
REVOKE ALL ON SEQUENCE timezone_diffs_id FROM clidegui;
GRANT ALL ON SEQUENCE timezone_diffs_id TO clidegui;
GRANT SELECT ON SEQUENCE timezone_diffs_id TO clide;


--
-- Name: timezone_diffs; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE timezone_diffs FROM PUBLIC;
REVOKE ALL ON TABLE timezone_diffs FROM clidegui;
GRANT ALL ON TABLE timezone_diffs TO clidegui;
GRANT SELECT ON TABLE timezone_diffs TO clide;


--
-- Name: user_sessions; Type: ACL; Schema: public; Owner: clidegui
--

REVOKE ALL ON TABLE user_sessions FROM PUBLIC;
REVOKE ALL ON TABLE user_sessions FROM clidegui;
GRANT ALL ON TABLE user_sessions TO clidegui;
GRANT SELECT ON TABLE user_sessions TO clide;


--
-- PostgreSQL database dump complete
--

