--
-- Create Schema Script
--   Database Version            : 11.2.0.2.0
--   Database Compatible Level   : 11.2.0.0.0
--   Script Compatible Level     : 11.2.0.0.0
--   Toad Version                : 14.1.120.923
--   DB Connect String           : XE
--   Schema                      : METADATA
--   Script Created by           : METADATA
--   Script Created at           : 22/11/2021 8:59:13 AM
--   Notes                       : 
--

-- Object Counts: 
--   Indexes: 47        Columns: 98         
--   Tables: 21         Columns: 206        Constraints: 200    


--
-- DEPLOYMENT  (Table) 
--
--   Row Count: 88
CREATE TABLE DEPLOYMENT
(
  DEPLOYMENT_ID         NUMBER(6)               NOT NULL,
  SRC_ID                NUMBER(6)               NOT NULL,
  ID                    VARCHAR2(8 BYTE),
  ID_TYPE               VARCHAR2(4 BYTE)        NOT NULL,
  EQUIPMENT_ID          NUMBER(6),
  EQUIPMENT_TYPE_ID     NUMBER(6)               NOT NULL,
  MET_OFFICE_EQPT_FLAG  CHAR(1 BYTE)            NOT NULL,
  OB_SYS_NAME           VARCHAR2(12 BYTE),
  MET_ROLE_ID           NUMBER(3),
  DEPL_BGN_DATE         DATE                    NOT NULL,
  DEPL_END_DATE         DATE                    NOT NULL,
  GRID_REF_TYPE         VARCHAR2(4 BYTE),
  EAST_GRID_REF         NUMBER(6),
  NORTH_GRID_REF        NUMBER(7),
  HIGH_PRCN_LAT         NUMBER(7,5),
  HIGH_PRCN_LON         NUMBER(8,5),
  ELEVATION             NUMBER(6,2),
  DEPLOYMENT_REMARK     VARCHAR2(250 BYTE),
  LAT_WGS84             NUMBER(7,5),
  LON_WGS84             NUMBER(8,5),
  IPR_OWNER             VARCHAR2(12 BYTE),
  EGM96_ELEVATION       NUMBER(6,2)
);

COMMENT ON TABLE DEPLOYMENT IS 'An instance of a piece of equipment being deployed for a purpose. Provision is made for the situation where only the type of equipment is known, by carrying Instrument Type ID as a foreign key, and making the relationship with the Equipment entity optional. Need to ensure that, if a specific piece of equipment is recorded (via Equipment ID), the attribute Equipment Type ID is automatically set to the value of the corresponding attribute in Equipment.';

COMMENT ON COLUMN DEPLOYMENT.DEPLOYMENT_ID IS ' Unique identifier of each deployment record';

COMMENT ON COLUMN DEPLOYMENT.SRC_ID IS ' Unique identifier for station in MIDAS & Metadata ';

COMMENT ON COLUMN DEPLOYMENT.ID IS ' Identifier associated with station';

COMMENT ON COLUMN DEPLOYMENT.ID_TYPE IS ' Identifier type describing identifier above';

COMMENT ON COLUMN DEPLOYMENT.EQUIPMENT_ID IS ' Unique identifier of piece of equipment';

COMMENT ON COLUMN DEPLOYMENT.EQUIPMENT_TYPE_ID IS ' Unique identifier for equipment type';

COMMENT ON COLUMN DEPLOYMENT.MET_OFFICE_EQPT_FLAG IS ' Flag describing whether Met Office owns equipment or not (T or F)';

COMMENT ON COLUMN DEPLOYMENT.OB_SYS_NAME IS ' Name of observing system if present';

COMMENT ON COLUMN DEPLOYMENT.MET_ROLE_ID IS ' Identifier describing the purpose of the equipment';

COMMENT ON COLUMN DEPLOYMENT.DEPL_BGN_DATE IS ' Begin date of deployment';

COMMENT ON COLUMN DEPLOYMENT.DEPL_END_DATE IS ' End date of deployment';

COMMENT ON COLUMN DEPLOYMENT.GRID_REF_TYPE IS ' Grid reference type (OS, IRL or CI)';

COMMENT ON COLUMN DEPLOYMENT.EAST_GRID_REF IS ' East grid reference of deployment';

COMMENT ON COLUMN DEPLOYMENT.NORTH_GRID_REF IS ' North grid reference of deployment';

COMMENT ON COLUMN DEPLOYMENT.HIGH_PRCN_LAT IS 'Latitude of deployment in degrees to 5 decimal places';

COMMENT ON COLUMN DEPLOYMENT.HIGH_PRCN_LON IS 'Longitude of deployment in degrees to 5 decimal places';

COMMENT ON COLUMN DEPLOYMENT.ELEVATION IS ' Elevation of deployment';

COMMENT ON COLUMN DEPLOYMENT.DEPLOYMENT_REMARK IS ' Remark about deployment';

COMMENT ON COLUMN DEPLOYMENT.LAT_WGS84 IS 'WGS84 Latitude of deployment in degrees to 5 decimal places';

COMMENT ON COLUMN DEPLOYMENT.LON_WGS84 IS 'WGS84 Longitude of deployment in degrees to 5 decimal places';

COMMENT ON COLUMN DEPLOYMENT.IPR_OWNER IS 'Code identifying who owns the intellectual property rights of the deployed equipment.';


--
-- PKDEPLOYMENT1  (Index) 
--
--  Dependencies: 
--   DEPLOYMENT (Table)
--
CREATE UNIQUE INDEX PKDEPLOYMENT1 ON DEPLOYMENT
(DEPLOYMENT_ID);

ALTER TABLE DEPLOYMENT ADD (
  CONSTRAINT C_D_HIGH_PRCN_LAT
  CHECK (  HIGH_PRCN_LAT BETWEEN -90.000 AND 90.000)
  ENABLE VALIDATE);

ALTER TABLE DEPLOYMENT ADD (
  CONSTRAINT C_D_HIGH_PRCN_LON
  CHECK (  HIGH_PRCN_LON BETWEEN -179.999 AND 180.000)
  ENABLE VALIDATE);

ALTER TABLE DEPLOYMENT ADD (
  CONSTRAINT C_D_SRC_ID
  CHECK (  SRC_ID >= 0)
  ENABLE VALIDATE);

ALTER TABLE DEPLOYMENT ADD (
  CONSTRAINT PKDEPLOYMENT1
  PRIMARY KEY
  (DEPLOYMENT_ID)
  USING INDEX PKDEPLOYMENT1
  ENABLE VALIDATE);



--
-- DEPLOYMENT_DETAIL  (Table) 
--
--   Row Count: 18
CREATE TABLE DEPLOYMENT_DETAIL
(
  DEPL_ATTR_ID        NUMBER(6)                 NOT NULL,
  DEPLOYMENT_ID       NUMBER(6)                 NOT NULL,
  DEPL_ATTR_BGN_DATE  DATE                      NOT NULL,
  DEPL_DTL_VAL        NUMBER(4)                 NOT NULL,
  DEPL_ATTR_END_DATE  DATE                      NOT NULL
);

COMMENT ON TABLE DEPLOYMENT_DETAIL IS 'The details of attributes associated with deployments of equipment. related to the deplyment and the deployment attribute tables.';

COMMENT ON COLUMN DEPLOYMENT_DETAIL.DEPL_ATTR_ID IS ' Deployment attribute unique identifier';

COMMENT ON COLUMN DEPLOYMENT_DETAIL.DEPLOYMENT_ID IS ' Deployment record unique identifier';

COMMENT ON COLUMN DEPLOYMENT_DETAIL.DEPL_ATTR_BGN_DATE IS ' Begin date for which attribute value is valid';

COMMENT ON COLUMN DEPLOYMENT_DETAIL.DEPL_DTL_VAL IS ' Value associated with attribute';

COMMENT ON COLUMN DEPLOYMENT_DETAIL.DEPL_ATTR_END_DATE IS ' End date for which attribute value is valid';


--
-- PKDEPLOYMENT_DETAIL  (Index) 
--
--  Dependencies: 
--   DEPLOYMENT_DETAIL (Table)
--
CREATE UNIQUE INDEX PKDEPLOYMENT_DETAIL ON DEPLOYMENT_DETAIL
(DEPL_ATTR_ID, DEPLOYMENT_ID, DEPL_ATTR_BGN_DATE);

ALTER TABLE DEPLOYMENT_DETAIL ADD (
  CONSTRAINT PKDEPLOYMENT_DETAIL
  PRIMARY KEY
  (DEPL_ATTR_ID, DEPLOYMENT_ID, DEPL_ATTR_BGN_DATE)
  USING INDEX PKDEPLOYMENT_DETAIL
  ENABLE VALIDATE);



--
-- EQPT_CALIB_COEFF  (Table) 
--
--   Row Count: 320
CREATE TABLE EQPT_CALIB_COEFF
(
  CALIB_COEFF_MSRT_ID       NUMBER(6)           NOT NULL,
  EQPT_TYPE_CALIB_COEFF_ID  NUMBER(6)           NOT NULL,
  EQPT_CALIB_ID             NUMBER(6)           NOT NULL,
  CALIB_COEFF_VAL           NUMBER(10,2)
);


--
-- PKEQPT_CALIB_COEFF  (Index) 
--
--  Dependencies: 
--   EQPT_CALIB_COEFF (Table)
--
CREATE UNIQUE INDEX PKEQPT_CALIB_COEFF ON EQPT_CALIB_COEFF
(CALIB_COEFF_MSRT_ID);

ALTER TABLE EQPT_CALIB_COEFF ADD (
  CONSTRAINT PKEQPT_CALIB_COEFF
  PRIMARY KEY
  (CALIB_COEFF_MSRT_ID)
  USING INDEX PKEQPT_CALIB_COEFF
  ENABLE VALIDATE);



--
-- EQUIPMENT  (Table) 
--
--   Row Count: 10
CREATE TABLE EQUIPMENT
(
  EQUIPMENT_ID            NUMBER(6)             NOT NULL,
  EQUIPMENT_TYPE_ID       NUMBER(6)             NOT NULL,
  MANUFACTURER_NAME       VARCHAR2(28 BYTE)     NOT NULL,
  MANUFACTURER_SN_TXT     VARCHAR2(24 BYTE)     NOT NULL,
  MET_REF_TXT             VARCHAR2(24 BYTE),
  EQPT_PRCT_DATE          DATE,
  EQUIPMENT_COST          NUMBER(6,2),
  EQPT_DSPL_DATE          DATE,
  EQPT_DSPL_RMRK          VARCHAR2(200 BYTE),
  EQPT_LAST_UPDATED_DATE  DATE
);

COMMENT ON TABLE EQUIPMENT IS 'The details of the items of equipment deployed at a station. Related by the equipment ID to the deployment table. The EQPT_PRCT_DATE and EQPT_DSPL_DATE are for equipment procurement and equipment disposal dates respectively.
However, they are more often used to record calibration validity start and end dates respectively.';

COMMENT ON COLUMN EQUIPMENT.EQUIPMENT_ID IS ' Unique identifier for piece of equipment in Metadata';

COMMENT ON COLUMN EQUIPMENT.EQUIPMENT_TYPE_ID IS ' Unique identifier for equipment type';

COMMENT ON COLUMN EQUIPMENT.MANUFACTURER_NAME IS ' Name of equipment manufacturer';

COMMENT ON COLUMN EQUIPMENT.MANUFACTURER_SN_TXT IS ' Manufacturer serial number or SI database Sensor_serial_no ';

COMMENT ON COLUMN EQUIPMENT.MET_REF_TXT IS ' Met Office reference number or SI database Asset_id';

COMMENT ON COLUMN EQUIPMENT.EQPT_PRCT_DATE IS 'Equipment procurement date, or date of calibration';

COMMENT ON COLUMN EQUIPMENT.EQUIPMENT_COST IS ' Cost of equipment';

COMMENT ON COLUMN EQUIPMENT.EQPT_DSPL_DATE IS 'Equipment disposal date, or date calibration expires.';

COMMENT ON COLUMN EQUIPMENT.EQPT_DSPL_RMRK IS ' Equipment disposal remark';

COMMENT ON COLUMN EQUIPMENT.EQPT_LAST_UPDATED_DATE IS 'Date at which this equipment was inserted or last updated';


--
-- PKEQUIPMENT  (Index) 
--
--  Dependencies: 
--   EQUIPMENT (Table)
--
CREATE UNIQUE INDEX PKEQUIPMENT ON EQUIPMENT
(EQUIPMENT_ID);

ALTER TABLE EQUIPMENT ADD (
  CONSTRAINT PKEQUIPMENT
  PRIMARY KEY
  (EQUIPMENT_ID)
  USING INDEX PKEQUIPMENT
  ENABLE VALIDATE);



--
-- EQUIPMENT_CALIBRATION  (Table) 
--
--   Row Count: 16
CREATE TABLE EQUIPMENT_CALIBRATION
(
  EQPT_CALIB_ID             NUMBER(6)           NOT NULL,
  EQUIPMENT_ID              NUMBER(6)           NOT NULL,
  EQPT_CALIB_DATE           DATE                NOT NULL,
  CALIB_MTHD_CODE           VARCHAR2(4 BYTE)    NOT NULL,
  EQPT_CALIB_NEXT_DUE_DATE  DATE,
  EQPT_CALIB_NAME           VARCHAR2(28 BYTE),
  CHECK_EQUIPMENT_ID        NUMBER(6),
  EQPT_CALIB_RMRK           VARCHAR2(200 BYTE)
);

COMMENT ON COLUMN EQUIPMENT_CALIBRATION.EQPT_CALIB_ID IS ' Unique identifier for calibration of this equipment';

COMMENT ON COLUMN EQUIPMENT_CALIBRATION.EQUIPMENT_ID IS ' Unique identifier of equipment';

COMMENT ON COLUMN EQUIPMENT_CALIBRATION.EQPT_CALIB_DATE IS ' Date on which calibration was carried out';

COMMENT ON COLUMN EQUIPMENT_CALIBRATION.CALIB_MTHD_CODE IS ' Code for method of calibration';

COMMENT ON COLUMN EQUIPMENT_CALIBRATION.EQPT_CALIB_NEXT_DUE_DATE IS 'Date on which next calibration is due';

COMMENT ON COLUMN EQUIPMENT_CALIBRATION.EQPT_CALIB_NAME IS ' Name of person carrying out calibration';

COMMENT ON COLUMN EQUIPMENT_CALIBRATION.CHECK_EQUIPMENT_ID IS ' Unique identifier for check equipment used';

COMMENT ON COLUMN EQUIPMENT_CALIBRATION.EQPT_CALIB_RMRK IS ' Remark on the calibration';


--
-- PKEQUIPMENT_CALIBRATION  (Index) 
--
--  Dependencies: 
--   EQUIPMENT_CALIBRATION (Table)
--
CREATE UNIQUE INDEX PKEQUIPMENT_CALIBRATION ON EQUIPMENT_CALIBRATION
(EQPT_CALIB_ID);

ALTER TABLE EQUIPMENT_CALIBRATION ADD (
  CONSTRAINT PKEQUIPMENT_CALIBRATION
  PRIMARY KEY
  (EQPT_CALIB_ID)
  USING INDEX PKEQUIPMENT_CALIBRATION
  ENABLE VALIDATE);



--
-- INSPECTION  (Table) 
--
--   Row Count: 3
CREATE TABLE INSPECTION
(
  INSPECTION_ID      NUMBER(6)                  NOT NULL,
  SRC_ID             NUMBER(6)                  NOT NULL,
  INSPECTION_DATE    DATE                       NOT NULL,
  INSPECTORS_NAME    VARCHAR2(70 BYTE)          NOT NULL,
  REVIEW_DATE        DATE,
  INSPECTION_REMARK  VARCHAR2(700 BYTE)
);

COMMENT ON TABLE INSPECTION IS 'Provides a record of inspections carried out at stations and related to the midas.source table';

COMMENT ON COLUMN INSPECTION.INSPECTION_ID IS ' Unique identifier for the inspection';

COMMENT ON COLUMN INSPECTION.SRC_ID IS ' Unique identifier for the station';

COMMENT ON COLUMN INSPECTION.INSPECTION_DATE IS ' Date of inspection';

COMMENT ON COLUMN INSPECTION.INSPECTORS_NAME IS ' Name of inspector';

COMMENT ON COLUMN INSPECTION.REVIEW_DATE IS ' Date on which inspection should be reviewed';

COMMENT ON COLUMN INSPECTION.INSPECTION_REMARK IS ' Remark on inspection';


--
-- PKINSPECTION  (Index) 
--
--  Dependencies: 
--   INSPECTION (Table)
--
CREATE UNIQUE INDEX PKINSPECTION ON INSPECTION
(INSPECTION_ID);

ALTER TABLE INSPECTION ADD (
  CONSTRAINT C_I_SRC_ID
  CHECK (  SRC_ID >= 0)
  ENABLE VALIDATE);

ALTER TABLE INSPECTION ADD (
  CONSTRAINT PKINSPECTION
  PRIMARY KEY
  (INSPECTION_ID)
  USING INDEX PKINSPECTION
  ENABLE VALIDATE);



--
-- INSPECTION_DETAIL  (Table) 
--
--   Row Count: 0
CREATE TABLE INSPECTION_DETAIL
(
  INSP_DETL_ID        NUMBER(8)                 NOT NULL,
  INSPECTION_ITEM_ID  NUMBER(5)                 NOT NULL,
  INSP_DETL_RSLT_TXT  VARCHAR2(1000 BYTE)       NOT NULL,
  DEPLOYMENT_ID       NUMBER(6),
  INSPECTION_ID       NUMBER(6)                 NOT NULL
);

COMMENT ON TABLE INSPECTION_DETAIL IS 'Related to the inspection table and provides the inspection details (the results) of the inspections carried out.';

COMMENT ON COLUMN INSPECTION_DETAIL.INSP_DETL_ID IS ' Unique identifier of record';

COMMENT ON COLUMN INSPECTION_DETAIL.INSPECTION_ITEM_ID IS ' Unique identifier of inspection item';

COMMENT ON COLUMN INSPECTION_DETAIL.INSP_DETL_RSLT_TXT IS ' Result of the inspection item for this inspection';

COMMENT ON COLUMN INSPECTION_DETAIL.DEPLOYMENT_ID IS ' Deployment which this item refers to';

COMMENT ON COLUMN INSPECTION_DETAIL.INSPECTION_ID IS ' Equipment which this item refers to';


--
-- PKINSPECTION_DETAIL  (Index) 
--
--  Dependencies: 
--   INSPECTION_DETAIL (Table)
--
CREATE UNIQUE INDEX PKINSPECTION_DETAIL ON INSPECTION_DETAIL
(INSP_DETL_ID);

ALTER TABLE INSPECTION_DETAIL ADD (
  CONSTRAINT PKINSPECTION_DETAIL
  PRIMARY KEY
  (INSP_DETL_ID)
  USING INDEX PKINSPECTION_DETAIL
  ENABLE VALIDATE);



--
-- OBSERVING_SCHEDULE  (Table) 
--
--   Row Count: 0
CREATE TABLE OBSERVING_SCHEDULE
(
  OB_SCHD_ID           NUMBER(6)                NOT NULL,
  STN_RPT_ELEM_ID      NUMBER(6)                NOT NULL,
  OB_SCHD_BGN_DATE     DATE                     NOT NULL,
  OB_SCHD_END_DATE     DATE                     NOT NULL,
  YEAR_DATE_BGN        CHAR(5 BYTE)             NOT NULL,
  YEAR_DATE_END        CHAR(5 BYTE)             NOT NULL,
  WEEK_DAY_BGN         NUMBER(1)                NOT NULL,
  WEEK_DAY_END         NUMBER(1)                NOT NULL,
  TIME_OF_DAY_BGN      NUMBER(4)                NOT NULL,
  TIME_OF_DAY_END      NUMBER(4)                NOT NULL,
  OBSERVING_INTERVAL   NUMBER(4)                NOT NULL,
  PUBLIC_HOLIDAY_FLAG  CHAR(1 BYTE)             NOT NULL,
  OB_SCHD_RMRK         VARCHAR2(200 BYTE)
);

COMMENT ON COLUMN OBSERVING_SCHEDULE.OB_SCHD_ID IS ' Unique number of the record';

COMMENT ON COLUMN OBSERVING_SCHEDULE.STN_RPT_ELEM_ID IS ' Unique identifier of the element for the station';

COMMENT ON COLUMN OBSERVING_SCHEDULE.OB_SCHD_BGN_DATE IS ' Start date of record';

COMMENT ON COLUMN OBSERVING_SCHEDULE.OB_SCHD_END_DATE IS ' End date of record';

COMMENT ON COLUMN OBSERVING_SCHEDULE.YEAR_DATE_BGN IS ' First month/year of report (format mm/yy)';

COMMENT ON COLUMN OBSERVING_SCHEDULE.YEAR_DATE_END IS ' Last month/year of report (format mm/yy)';

COMMENT ON COLUMN OBSERVING_SCHEDULE.WEEK_DAY_BGN IS ' First day of week of report';

COMMENT ON COLUMN OBSERVING_SCHEDULE.WEEK_DAY_END IS ' Last day of week of report';

COMMENT ON COLUMN OBSERVING_SCHEDULE.TIME_OF_DAY_BGN IS ' First time of day of report';

COMMENT ON COLUMN OBSERVING_SCHEDULE.TIME_OF_DAY_END IS ' Last time of day of report';

COMMENT ON COLUMN OBSERVING_SCHEDULE.OBSERVING_INTERVAL IS ' Number of minutes between each report';

COMMENT ON COLUMN OBSERVING_SCHEDULE.PUBLIC_HOLIDAY_FLAG IS ' T or F. Shows whether the report comes in on a bank holiday';

COMMENT ON COLUMN OBSERVING_SCHEDULE.OB_SCHD_RMRK IS ' Remark for the record';


--
-- C_OBS_UNQ  (Index) 
--
--  Dependencies: 
--   OBSERVING_SCHEDULE (Table)
--
CREATE UNIQUE INDEX C_OBS_UNQ ON OBSERVING_SCHEDULE
(STN_RPT_ELEM_ID, OB_SCHD_BGN_DATE, OB_SCHD_END_DATE, YEAR_DATE_BGN, YEAR_DATE_END, 
WEEK_DAY_BGN, WEEK_DAY_END, TIME_OF_DAY_BGN, TIME_OF_DAY_END, OBSERVING_INTERVAL, 
PUBLIC_HOLIDAY_FLAG);
--
-- PKOBSERVING_SCHEDULE  (Index) 
--
--  Dependencies: 
--   OBSERVING_SCHEDULE (Table)
--
CREATE UNIQUE INDEX PKOBSERVING_SCHEDULE ON OBSERVING_SCHEDULE
(OB_SCHD_ID);

ALTER TABLE OBSERVING_SCHEDULE ADD (
  CONSTRAINT PKOBSERVING_SCHEDULE
  PRIMARY KEY
  (OB_SCHD_ID)
  USING INDEX PKOBSERVING_SCHEDULE
  ENABLE VALIDATE);

ALTER TABLE OBSERVING_SCHEDULE ADD (
  CONSTRAINT C_OBS_UNQ
  UNIQUE (STN_RPT_ELEM_ID, OB_SCHD_BGN_DATE, OB_SCHD_END_DATE, YEAR_DATE_BGN, YEAR_DATE_END, WEEK_DAY_BGN, WEEK_DAY_END, TIME_OF_DAY_BGN, TIME_OF_DAY_END, OBSERVING_INTERVAL, PUBLIC_HOLIDAY_FLAG)
  USING INDEX C_OBS_UNQ
  ENABLE VALIDATE);



--
-- OBSERVING_SYSTEM_INSTALLATION  (Table) 
--
--   Row Count: 8
CREATE TABLE OBSERVING_SYSTEM_INSTALLATION
(
  OB_SYS_INTL_ID        NUMBER(6)               NOT NULL,
  OB_SYS_VRSN_ID        NUMBER(6)               NOT NULL,
  SRC_ID                NUMBER(6)               NOT NULL,
  OB_SYS_INTL_BGN_DATE  DATE                    NOT NULL,
  OB_SYS_INTL_END_DATE  DATE                    NOT NULL
);

COMMENT ON COLUMN OBSERVING_SYSTEM_INSTALLATION.OB_SYS_INTL_ID IS ' Unique number for each record';

COMMENT ON COLUMN OBSERVING_SYSTEM_INSTALLATION.OB_SYS_VRSN_ID IS ' Unique number for observing system version';

COMMENT ON COLUMN OBSERVING_SYSTEM_INSTALLATION.SRC_ID IS ' Unique number for station';

COMMENT ON COLUMN OBSERVING_SYSTEM_INSTALLATION.OB_SYS_INTL_BGN_DATE IS ' Start date of installation of observing sys at station';

COMMENT ON COLUMN OBSERVING_SYSTEM_INSTALLATION.OB_SYS_INTL_END_DATE IS ' End date of installation of observing sys at station';


--
-- PKOBS_SYSTEM_INSTALL  (Index) 
--
--  Dependencies: 
--   OBSERVING_SYSTEM_INSTALLATION (Table)
--
CREATE UNIQUE INDEX PKOBS_SYSTEM_INSTALL ON OBSERVING_SYSTEM_INSTALLATION
(OB_SYS_INTL_ID);

ALTER TABLE OBSERVING_SYSTEM_INSTALLATION ADD (
  CONSTRAINT C_OSI_SRC_ID
  CHECK (  SRC_ID >= 0)
  ENABLE VALIDATE);

ALTER TABLE OBSERVING_SYSTEM_INSTALLATION ADD (
  CONSTRAINT PKOBS_SYSTEM_INSTALL
  PRIMARY KEY
  (OB_SYS_INTL_ID)
  USING INDEX PKOBS_SYSTEM_INSTALL
  ENABLE VALIDATE);



--
-- REPORTING_SCHEDULE  (Table) 
--
--   Row Count: 34
CREATE TABLE REPORTING_SCHEDULE
(
  REPORT_SCHEDULE_ID   NUMBER(6)                NOT NULL,
  ID                   VARCHAR2(8 BYTE),
  ID_TYPE              VARCHAR2(4 BYTE)         NOT NULL,
  MET_DOMAIN_NAME      VARCHAR2(8 BYTE)         NOT NULL,
  SRC_CAP_BGN_DATE     DATE                     NOT NULL,
  RPT_SCHD_BGN_DATE    DATE                     NOT NULL,
  RPT_SCHD_END_DATE    DATE                     NOT NULL,
  YEAR_DATE_BGN        CHAR(5 BYTE)             NOT NULL,
  YEAR_DATE_END        CHAR(5 BYTE)             NOT NULL,
  WEEK_DAY_BGN         NUMBER(1)                NOT NULL,
  WEEK_DAY_END         NUMBER(1)                NOT NULL,
  TIME_OF_DAY_BGN      NUMBER(4)                NOT NULL,
  TIME_OF_DAY_END      NUMBER(4)                NOT NULL,
  REPORTING_INTERVAL   NUMBER(4)                NOT NULL,
  REPORTING_METHOD     VARCHAR2(9 BYTE)         NOT NULL,
  PUBLIC_HOLIDAY_FLAG  CHAR(1 BYTE)             NOT NULL,
  RPT_SCHD_RMRK        VARCHAR2(200 BYTE)
);

COMMENT ON COLUMN REPORTING_SCHEDULE.REPORT_SCHEDULE_ID IS ' Unique identifier for each record';

COMMENT ON COLUMN REPORTING_SCHEDULE.ID IS ' Non unique identifier for station';

COMMENT ON COLUMN REPORTING_SCHEDULE.ID_TYPE IS ' Type of identifier above';

COMMENT ON COLUMN REPORTING_SCHEDULE.MET_DOMAIN_NAME IS ' Describes the route from which the data came';

COMMENT ON COLUMN REPORTING_SCHEDULE.SRC_CAP_BGN_DATE IS ' Start date of the SRC_CAPABILITY record';

COMMENT ON COLUMN REPORTING_SCHEDULE.RPT_SCHD_BGN_DATE IS ' Start date of record';

COMMENT ON COLUMN REPORTING_SCHEDULE.RPT_SCHD_END_DATE IS ' End date of record';

COMMENT ON COLUMN REPORTING_SCHEDULE.YEAR_DATE_BGN IS ' First month/year of report (format mm/yy)';

COMMENT ON COLUMN REPORTING_SCHEDULE.YEAR_DATE_END IS ' Last month/year of report (format mm/yy)';

COMMENT ON COLUMN REPORTING_SCHEDULE.WEEK_DAY_BGN IS ' First day of week of report';

COMMENT ON COLUMN REPORTING_SCHEDULE.WEEK_DAY_END IS ' Last day of week of report';

COMMENT ON COLUMN REPORTING_SCHEDULE.TIME_OF_DAY_BGN IS ' First time of day of report';

COMMENT ON COLUMN REPORTING_SCHEDULE.TIME_OF_DAY_END IS ' Last time of day of report';

COMMENT ON COLUMN REPORTING_SCHEDULE.REPORTING_INTERVAL IS ' Number of minutes between each report';

COMMENT ON COLUMN REPORTING_SCHEDULE.REPORTING_METHOD IS ' Either Manual or Automatic';

COMMENT ON COLUMN REPORTING_SCHEDULE.PUBLIC_HOLIDAY_FLAG IS ' T or F. Shows whether the report comes in on a bank holiday';

COMMENT ON COLUMN REPORTING_SCHEDULE.RPT_SCHD_RMRK IS ' Remark for the record';


--
-- C_RPS_UNQ  (Index) 
--
--  Dependencies: 
--   REPORTING_SCHEDULE (Table)
--
CREATE UNIQUE INDEX C_RPS_UNQ ON REPORTING_SCHEDULE
(ID, ID_TYPE, MET_DOMAIN_NAME, SRC_CAP_BGN_DATE, RPT_SCHD_BGN_DATE, 
RPT_SCHD_END_DATE, YEAR_DATE_BGN, YEAR_DATE_END, WEEK_DAY_BGN, WEEK_DAY_END, 
TIME_OF_DAY_BGN, TIME_OF_DAY_END, REPORTING_INTERVAL, REPORTING_METHOD, PUBLIC_HOLIDAY_FLAG);
--
-- PKREPORTING_SCHEDULE  (Index) 
--
--  Dependencies: 
--   REPORTING_SCHEDULE (Table)
--
CREATE UNIQUE INDEX PKREPORTING_SCHEDULE ON REPORTING_SCHEDULE
(REPORT_SCHEDULE_ID);

ALTER TABLE REPORTING_SCHEDULE ADD (
  CONSTRAINT PKREPORTING_SCHEDULE
  PRIMARY KEY
  (REPORT_SCHEDULE_ID)
  USING INDEX PKREPORTING_SCHEDULE
  ENABLE VALIDATE);

ALTER TABLE REPORTING_SCHEDULE ADD (
  CONSTRAINT C_RPS_UNQ
  UNIQUE (ID, ID_TYPE, MET_DOMAIN_NAME, SRC_CAP_BGN_DATE, RPT_SCHD_BGN_DATE, RPT_SCHD_END_DATE, YEAR_DATE_BGN, YEAR_DATE_END, WEEK_DAY_BGN, WEEK_DAY_END, TIME_OF_DAY_BGN, TIME_OF_DAY_END, REPORTING_INTERVAL, REPORTING_METHOD, PUBLIC_HOLIDAY_FLAG)
  USING INDEX C_RPS_UNQ
  ENABLE VALIDATE);



--
-- SOURCE  (Table) 
--
--  Dependencies: 
--   SDO_GEOMETRY (Type)
--   STANDARD (Package)
--
CREATE TABLE SOURCE
(
  SRC_ID              NUMBER(6)                 NOT NULL,
  SRC_NAME            VARCHAR2(40 BYTE)         NOT NULL,
  HIGH_PRCN_LAT       NUMBER(7,5)               NOT NULL,
  HIGH_PRCN_LON       NUMBER(8,5)               NOT NULL,
  LOC_GEOG_AREA_ID    VARCHAR2(4 BYTE)          NOT NULL,
  REC_ST_IND          NUMBER(4)                 NOT NULL,
  SRC_BGN_DATE        DATE,
  SRC_TYPE            VARCHAR2(15 BYTE),
  GRID_REF_TYPE       VARCHAR2(4 BYTE)          DEFAULT 'XX'                  NOT NULL,
  EAST_GRID_REF       NUMBER(6),
  NORTH_GRID_REF      NUMBER(7),
  HYDR_AREA_ID        NUMBER(4),
  POST_CODE           VARCHAR2(9 BYTE),
  SRC_END_DATE        DATE,
  ELEVATION           NUMBER(6,2),
  WMO_REGION_CODE     CHAR(1 BYTE),
  PARENT_SRC_ID       NUMBER(6),
  ZONE_TIME           NUMBER(2),
  DRAINAGE_STREAM_ID  VARCHAR2(4 BYTE),
  SRC_UPD_DATE        DATE,
  MTCE_CTRE_CODE      VARCHAR2(4 BYTE),
  PLACE_ID            NUMBER(6)                 DEFAULT NULL,
  LAT_WGS84           NUMBER(7,5),
  LON_WGS84           NUMBER(8,5),
  SRC_GUID            RAW(32)                   DEFAULT SYS_GUID(),
  SRC_GEOM            MDSYS.SDO_GEOMETRY,
  SRC_LOCATION_TYPE   VARCHAR2(50 BYTE)
)
COLUMN SRC_GEOM NOT SUBSTITUTABLE AT ALL LEVELS;

COMMENT ON TABLE SOURCE IS 'Midas.Source table contains details of the location where observations are made, i.e. a Source is a station where meteorological readings are made.  The location of a source is defined as the location of the barometer or the rain gauge, or other principal instrument.
A source changes its identity (i.e. it becomes a new source) when the location of the principal instrument changes by more than a specified amount, e.g. by 400 metres or more for a rainfall station.  A source may change its identity under other circumstances, e.g. a change of exposure or if it closes and re-opens.  A source must have at least one capability, and that must use an identifier of a specified id-type.
Begin and end dates refer to the opening and closing of the source.  A source may be re-opened, and re-use a src_id, provided the details defined in this entity are the same.  Sources will not exist if they have no observations, but they may be created in advance, where it is known that a station is due to open.
Sources are in a fixed position.  Met (OPR) cannot supply or maintain source information for ships.  On-station Ocean Weather Ships are treated as fixed sources; they have a notional latitude and longitude.  They have a source record, with a Src_Name of OWS ALPHA, OWS BRAVO, etc., and appropriate call-sign identifiers.  Latitude and longitude at time of report are attributes of the report.
This entity does not describe the reporting practice of individual elements or report types.
NB: The entity has a self-referencing relationship, using parent_src_id, as required by the Metadata project.  It also supports cross-referencing to other sources for a specified purpose, using relationships with the cross_reference entity.  This duplication will be resolved at the next opportunity.

MidasUpd.Source is an updateable view, with one-for-one projection from the base table.
MidasVu.Source is a read-only view, with one-for-one projection from the base table.
Carlos.Source is a read-only view, for a sub-set of the columns.';

COMMENT ON COLUMN SOURCE.SRC_ID IS '
This is an identifier for each source of meteorological data within the system. It acts as a unique identifier when a source may be of various types.  It consists of a 6 digit integer, assigned from a high-number record, and has no external significance.
';

COMMENT ON COLUMN SOURCE.SRC_NAME IS '
Name of source
';

COMMENT ON COLUMN SOURCE.HIGH_PRCN_LAT IS '
When source is an on-station OWS, latitude is notional.

Latitude expressed in thousandths of a degree.  South if negative
';

COMMENT ON COLUMN SOURCE.HIGH_PRCN_LON IS '
When source is an on-station OWS, longitude is notional.

Longitude express in thousandths of a degree.  West if negative
';

COMMENT ON COLUMN SOURCE.LOC_GEOG_AREA_ID IS '
Geographic area where the source is located, connected at the lowest level by using the geographic area id of the location.
';

COMMENT ON COLUMN SOURCE.REC_ST_IND IS '
An indicator of the present state of the database row. It can be set by data evaluators to indicate that the record can be deleted by a sweep process.

The known uses of Rec_St_Ind are:
 10 Unset
 20 Record values have been adjusted
 30 Record has been moved forward one hour
 40 Observation marked for deletion, i.e. logically deleted
 50 Observation unmarked for deletion i.e. restored from logical deletion.
 60 Observation level (e.g. a point in an upper air ascent) marked for deletion
 70 Observation level unmarked for deletion
 80 Source marked for deletion
 90 Source unmarked for deletion i.e. restored from logical deletion.
 100 Identifier change
 110 Delete observation level

Rec_St_Ind for observations is composed of two values, i.e. aabb
1001 Normal ingestion of observation at creation
1002 Normal ingestion of a multi-level observation such as upper air at creation
1003 Addition of observation level
1004 Receive a COR before normal observation received
1005 Receive a COR before normal multi level observation received
1006 Receive a COR to observation level
1007 Addition of a missing value
1008 Receive a COR after the observation received but before QC started.
1009 Receive a COR to an observation level after normal receipt but before QC started
1010 Start of QC, ob has been extracted for QC checks
1011 The QC run has updated the QC level on Version_Num = 1
1012 With Version_Num = 0 indicates that there should be a version 1 which can be anything between 1022 and 1026 depending on whether it has more than 1 amend to it.
1013 Version_Num = 1 has been killed, Version_Num = 0 exists.
1014 Version_Num = 1 has apportioned/corrected data. Corresponding Version_Num = 0 does not exist.
1022 Version_Num = 1. A corresponding Version_Num = 0 has been created because of first change to the observation (Version_Num = 0 has Rec_St_Ind = 1012).
1023 Version_Num = 1 of multi level ob
1024 QC amend to Version_Num = 1 observation multi level
1025 Change to QC level in Version_Num = 1
1026 Receive subsequent QC amendments
1027 Decision to Archive
1028 Archive observation
1029 COR of Key item- pre QC - mark for deletion
';

COMMENT ON COLUMN SOURCE.SRC_BGN_DATE IS '
source.src_bgn_date is the date when the station opened.
';

COMMENT ON COLUMN SOURCE.SRC_TYPE IS '
e.g. land station, ship, coastal station.

Types of location for a source, e.g. land, marine, coastal.  A marine station may be a ship or buoy or rig or platform.  NB: This data item describes the type of source location, not the type of report.
';

COMMENT ON COLUMN SOURCE.GRID_REF_TYPE IS '
This attribute describes the type of grid reference.
Value List:
CI = Channel Islands grid
IRL = Irish grid
OS = Ordnance Survey British National grid reference
Unspecified, usually over-seas.
';

COMMENT ON COLUMN SOURCE.EAST_GRID_REF IS '
As a compound with North Grid reference can indicate a location to within a 100 metre square.
';

COMMENT ON COLUMN SOURCE.NORTH_GRID_REF IS '
As a compound with east grid reference can give a location of a site to a 100 m square.
';

COMMENT ON COLUMN SOURCE.HYDR_AREA_ID IS '
Hydrometric area identification number.  Rainfall stations are located in a hydrometric area assigned clockwise round the country starting in North Scotland.
Hydrometric area numbers are in the HHHh format, where HHH is the original number allocated in the 1930s, and h is the sub-division resulting from water authority re-organizations.  Thus, when h=0 the boundary remains that defined n the 1930s.
In MIDAS, it links an area to sources.
';

COMMENT ON COLUMN SOURCE.POST_CODE IS '
Allows searches on post code, without access to full postal address.

There is a requirement to retrieve data by post code.  Post area, district and sector are stored, i.e. RG12 2, but not post walk, i.e. not RG12 2SZ.
';

COMMENT ON COLUMN SOURCE.SRC_END_DATE IS '
source.src_end_date is the date when the station closed
';

COMMENT ON COLUMN SOURCE.ELEVATION IS '
Height of ground surface above mean sea level.  See also height.
';

COMMENT ON COLUMN SOURCE.WMO_REGION_CODE IS '
WMO Code A1 Code table 0161. WMO Regional Association area in which buoy, drilling rig or oil- or gas-production platform has been deployed.
Values: 1 = Africa, 2 = Asia, 3 = South America, 4 = North America, 5 = Australasia, 6 = Europe, 7 = Antactica.
';

COMMENT ON COLUMN SOURCE.PARENT_SRC_ID IS '
';

COMMENT ON COLUMN SOURCE.ZONE_TIME IS '
Difference from UTC (hours) for overseas stations.
';

COMMENT ON COLUMN SOURCE.DRAINAGE_STREAM_ID IS '
Drainage streams or coastal name identification number to link area to source information. New item but drainage stream information from ML.HYDROSET
';

COMMENT ON COLUMN SOURCE.SRC_UPD_DATE IS '
source_updated_date
';

COMMENT ON COLUMN SOURCE.MTCE_CTRE_CODE IS '
Abbreviated form of the maintenance centre name.
';

COMMENT ON COLUMN SOURCE.PLACE_ID IS '
Attribute Description -
';

COMMENT ON COLUMN SOURCE.SRC_GUID IS 'Global Unique ID - RAW32 - default sys_guid()';

COMMENT ON COLUMN SOURCE.SRC_GEOM IS 'SRID 8307 geometry (WGS84 lat/lon)';

COMMENT ON COLUMN SOURCE.SRC_LOCATION_TYPE IS 'Categorisation of location e.g. UKMO_SURFACE_LAND';


--
-- C_SRC_PK  (Index) 
--
--  Dependencies: 
--   SOURCE (Table)
--
CREATE UNIQUE INDEX C_SRC_PK ON SOURCE
(SRC_ID);

ALTER TABLE SOURCE ADD (
  CONSTRAINT CHIGH_PRCN_LAT41838
  CHECK (  high_prcn_lat BETWEEN -90.000 AND 90.000)
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT CHIGH_PRCN_LON41839
  CHECK (  high_prcn_lon BETWEEN -179.999 AND 180.000)
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT CREC_ST_IND41850
  CHECK (  REC_ST_IND >= 1001)
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT CSRC_BGN_DATE
  CHECK (   SRC_BGN_DATE BETWEEN TO_DATE('01011677','DDMMYYYY') AND TO_DATE('31123999','DDMMYYYY'))
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT CSRC_END_DATE
  CHECK (   SRC_END_DATE BETWEEN TO_DATE('01011677','DDMMYYYY') AND TO_DATE('31123999','DDMMYYYY'))
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT CSRC_ID41834
  CHECK (  SRC_ID >= 0)
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT C_SOURCE_NOT_SELF_REFERENCING
  CHECK (  SRC_ID <> parent_src_id)
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT C_SOURCE_SRC_TYPE_VALUES
  CHECK (src_type IN ('SFC','SFC UA','SFC ANEMO','SFC AWS','SFC BUOY','SFC LV','SFC OCEAN',
                                      'SFC OWS','SFC PLAT','SFC RIG','SFC SAMOS','SFC SIESAWS','BOGUS1',
                                      'BOGUS2','UA'))
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT C_SRC_EAST_GRID_REF
  CHECK (   EAST_GRID_REF >= 0)
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT C_SRC_END_DATE
  CHECK (  SRC_END_DATE >= SRC_BGN_DATE)
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT C_SRC_GRID_REF_TYPE_CHK
  CHECK (grid_ref_type IN ('CI','IRL','OS','XX','ROI'))
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT C_SRC_NORTH_GRID_REF
  CHECK (   NORTH_GRID_REF >= 0)
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT C_SRC_PARENT_SRC_ID
  CHECK (   parent_src_id >= 0)
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT C_SRC_UPD_DATE
  CHECK (   SRC_UPD_DATE BETWEEN TO_DATE('01011677','DDMMYYYY') AND TO_DATE('31123999','DDMMYYYY'))
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT C_SRC_WMO_REGION_CODE
  CHECK (  wmo_region_code BETWEEN '1' AND '7')
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT C_SRC_ZONE_TIME
  CHECK (  ZONE_TIME BETWEEN -12 AND 12)
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  CONSTRAINT C_SRC_PK
  PRIMARY KEY
  (SRC_ID)
  USING INDEX C_SRC_PK
  ENABLE VALIDATE);

ALTER TABLE SOURCE ADD (
  UNIQUE (SRC_GUID)
  ENABLE VALIDATE);



--
-- SRC_CAPABILITY  (Table) 
--
CREATE TABLE SRC_CAPABILITY
(
  ID                     VARCHAR2(8 BYTE)       NOT NULL,
  ID_TYPE                VARCHAR2(4 BYTE)       NOT NULL,
  MET_DOMAIN_NAME        VARCHAR2(8 BYTE)       NOT NULL,
  SRC_CAP_BGN_DATE       DATE                   NOT NULL,
  SRC_ID                 NUMBER(6)              NOT NULL,
  REC_ST_IND             NUMBER(4)              NOT NULL,
  PRIME_CAPABILITY_FLAG  CHAR(1 BYTE)           DEFAULT 'F'                   NOT NULL,
  SRC_CAP_END_DATE       DATE,
  FIRST_ONLINE_OB_YR     NUMBER(4),
  DB_SEGMENT_NAME        VARCHAR2(12 BYTE),
  RCPT_METHOD_NAME       VARCHAR2(20 BYTE),
  DATA_RETENTION_PERIOD  NUMBER(3),
  COMM_MTHD_ID           NUMBER(6)
);

COMMENT ON TABLE SRC_CAPABILITY IS 'Midas.Src_Capability table defines which types of observation  (met domain) a source is capable of producing (and MIDAS will store), e.g. London/Gatwick is capable of producing synops and NCMs, while Southend is only capable of producing metars.
Some stations, e.g. Beaufort Park, use more than one identifier of the same type, e.g. WMO number 03693 for manned observations and 03694 for SAMOS, therefore there will be two capabilities for this source.
Changes over time are recorded using dates.  A source capability is closed when attribute Src_Cap_End_Date is set to a date that is before the current date.  If the capability is subsequently required again by the source, then the record may either be re-opened, by resetting the Src_Cap_End_Date or by creating a new record.
A capability is not automatically created upon receipt of a new source or new meteorological domain.  A source capability can be deleted when it is open.
Rcpt_method_name is currently used to store ID cross-references, while communication_method_code is required by the MetaData project.
MidasUpd.Src_Capability is the corresponding updatable view, with one-for-one projection of the columns.  To prevent accidental deletion of CLIMAT rows, delete privilege is not available for this view.
MidasUpd.Delete_Src_Capability allows delete privilege on rows other than CLIMAT ones.
MidasUpd.Clm_Src_Capability is an updatable view, restricted to CLIMAT rows.
MidasVu.Src_Capability is a non-updatable view, with one-for-one projection of the columns.
When the Src_Capability is valid, but MIDAS has no data, Rec_St_Ind = 2000.  These rows are excluded from the MidasVu views.';

COMMENT ON COLUMN SRC_CAPABILITY.ID IS '
The value of an identifier for the source.  Eight left-justified identifier characters, eg 03772, EGGW , etc.  This ID has no meaning unless interpreted with the associated identifier type.
Identifier has a length of eight characters to allow for ship call-signs and to achieve alignment.  The WMO definition of symbolic letter D....D is Ships call sign consisting of three or more alphanumeric characters.  B Fullagar (OPR3) confirms that the maximum length of a WMO call-sign is seven characters.  The GreenPeace ship uses an eight character call-sign, but OPR truncate this to seven characters.
Some identifiers have been re-used, e.g. when a WMO station number is re-allocated at a later date for a site that is deemed suitable for synoptic purposes.  Where this has happened already the oldest use will have the character Z appended to the identifier, the next oldest Y, etc, with the over-riding proviso that the newest version will NOT have an appendage.
';

COMMENT ON COLUMN SRC_CAPABILITY.ID_TYPE IS '
The name of the type of identifier used to identify a source,  e.g. WMO, SHIP, OWS, RAIN, DCNN etc.  See BUFR table B, class 02, 002001.
';

COMMENT ON COLUMN SRC_CAPABILITY.MET_DOMAIN_NAME IS '
A met domain is uniquely identified by its name.
The names of input domains correspond to existing code forms, but are structured to facilitate sorting, e.g. SYNOP FM12, SHIP FM13, DRIFTER FM18-IX, CLIMAT UA FM75-VI, etc.
NB: Synop is not a unique name for an input met domain; the domain name must include a FM session number or date.    Synop pre 1982 is not a unique name, the name may have changed on several previous occasions.
OP3 marine QC have specifically asked for a met domain of Ship synop - GTS, or similar, so that they can distinguish GTS ships from VOF ones.  The names of storage domains will correspond to MIDAS table names.
';

COMMENT ON COLUMN SRC_CAPABILITY.SRC_CAP_BGN_DATE IS '
src_capability.src_bgn_date is the first date for which we have observations of the id_ type / met_domain_name combination.
';

COMMENT ON COLUMN SRC_CAPABILITY.SRC_ID IS '
This is an identifier for each source of meterological data within the system. It acts as a unique identifier when a source may be of various types.  It consists of a 6 digit integer, assigned from a high-number record, and has no external significance.
';

COMMENT ON COLUMN SRC_CAPABILITY.REC_ST_IND IS '
rec_st_ind = 2000 indicates that Midas has no obs for this src_capability.

An indicator of the present state of the database row. It can be set by data evaluators to indicate that the record can be deleted by a sweep process.

The known uses of Rec_St_Ind are:
 10 Unset
 20 Record values have been adjusted
 30 Record has been moved forward one hour
 40 Observation marked for deletion, i.e. logically deleted
 50 Observation unmarked for deletion i.e. restored from logical deletion.
 60 Observation level (e.g. a point in an upper air ascent) marked for deletion
 70 Observation level unmarked for deletion
 80 Source marked for deletion
 90 Source unmarked for deletion i.e. restored from logical deletion.
 100 Identifier change
 110 Delete observation level

Rec_St_Ind for observations is composed of two values, i.e. aabb
1001 Normal ingestion of observation at creation
1002 Normal ingestion of a multi-level observation such as upper air at creation
1003 Addition of observation level
1004 Receive a COR before normal observation received
1005 Receive a COR before normal multi level observation received
1006 Receive a COR to observation level
1007 Addition of a missing value
1008 Receive a COR after the observation received but before QC started.
1009 Receive a COR to an observation level after normal receipt but before QC started
1010 Start of QC, ob has been extracted for QC checks
1011 The QC run has updated the QC level on Version_Num = 1
1012 With Version_Num = 0 indicates that there should be a version 1 which can be anything between 1022 and 1026 depending on whether it has more than 1 amend to it.
1013 Version_Num = 1 has been killed, Version_Num = 0 exists.
1014 Version_Num = 1 has apportioned/corrected data. Corresponding Version_Num = 0 does not exist.
1022 Version_Num = 1. A corresponding Version_Num = 0 has been created because of first change to the observation (Version_Num = 0 has Rec_St_Ind = 1012).
1023 Version_Num = 1 of multi level ob
1024 QC amend to Version_Num = 1 observation multi level
1025 Change to QC level in Version_Num = 1
1026 Receive subsequent QC amendments
1027 Decision to Archive
1028 Archive observation
1029 COR of Key item- pre QC - mark for deletion
';

COMMENT ON COLUMN SRC_CAPABILITY.PRIME_CAPABILITY_FLAG IS 'Single character to indicate if the capability is the prime one of its type for the specified station, i.e. the prime daily rainfall capability for the station.  Valid values are T and F.  For each met_domain, one and only one capability can be set to prime at one time.  When SAMOS or similar equipment is trialed at a site, the site may continue to report using its current ID and prime_capability_flag = T while the SAMOS uses a new src_capability and ID with prime_capability_flag = F.  When the trial concludes and the SAMOS becomes operational, the old capability is changed to prime_capability_flag = F (and is usually closed), while the new src_capability (and ID) is updated to prime_capability_flag = T.';

COMMENT ON COLUMN SRC_CAPABILITY.SRC_CAP_END_DATE IS '
src_capability.src_end_date is the last date for which we have observations of the id_ type / met_domain_name combination.
';

COMMENT ON COLUMN SRC_CAPABILITY.FIRST_ONLINE_OB_YR IS '
Year of first online observation.  This attribute indicates when the data are online or offline thus:
0000 implies all data are offline, because we will not store capabilities for which we do not have data;
nnnn, i.e. any valid year, implies all data from that year onwards are online, and previous years are offline;
nnnn where nnnn = "capability effective from year" implies all data are online.
';

COMMENT ON COLUMN SRC_CAPABILITY.DB_SEGMENT_NAME IS '
The name of a database segment, e.g. source, raindrnl, etc.
';

COMMENT ON COLUMN SRC_CAPABILITY.RCPT_METHOD_NAME IS '
Formerly the method of receiving these reports from this source, e.g. GTS, metform, postcard, etc.  This attribute is now used to cross-reference between IDs in use at a SOURCE.  It will be renamed to ID_CROSS_REF at the next convenient opportunity.
 ';

COMMENT ON COLUMN SRC_CAPABILITY.DATA_RETENTION_PERIOD IS '
Character string indicating the period for which data are retained in MIDAS.
';

COMMENT ON COLUMN SRC_CAPABILITY.COMM_MTHD_ID IS '
Abbreviated code to identify the various communication methods on which data can be sent back to the Office.
';


--
-- C_SRCCAP_END_DATE  (Index) 
--
--  Dependencies: 
--   SRC_CAPABILITY (Table)
--
CREATE UNIQUE INDEX C_SRCCAP_END_DATE ON SRC_CAPABILITY
(ID, ID_TYPE, MET_DOMAIN_NAME, SRC_CAP_END_DATE);
--
-- C_SRCCAP_PK  (Index) 
--
--  Dependencies: 
--   SRC_CAPABILITY (Table)
--
CREATE UNIQUE INDEX C_SRCCAP_PK ON SRC_CAPABILITY
(ID, ID_TYPE, MET_DOMAIN_NAME, SRC_CAP_BGN_DATE);

ALTER TABLE SRC_CAPABILITY ADD (
  CONSTRAINT CPRIME_CAPABILITY_FLAG43745
  CHECK (  prime_capability_flag IN ('T',  'F') )
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY ADD (
  CONSTRAINT CREC_ST_IND41801
  CHECK (REC_ST_IND >= 0001)
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY ADD (
  CONSTRAINT CSRC_CAP_BGN_DATE
  CHECK (   SRC_CAP_BGN_DATE BETWEEN TO_DATE('16770101','YYYYMMDD') AND TO_DATE('39991231','YYYYMMDD'))
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY ADD (
  CONSTRAINT CSRC_CAP_END_DATE43445
  CHECK ( SRC_CAP_END_DATE BETWEEN TO_DATE('01011677','DDMMYYYY') AND TO_DATE('31123999','DDMMYYYY')  )
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY ADD (
  CONSTRAINT CSRC_ID40906
  CHECK (  SRC_ID >= 0)
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY ADD (
  CONSTRAINT C_SRCCAP_DATA_RETN_PER
  CHECK (  data_retention_period >= 0000)
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY ADD (
  CONSTRAINT C_SRCCAP_FIRST_ONLINE_OB_YR
  CHECK (  FIRST_ONLINE_OB_YR BETWEEN 1738 AND 3999)
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY ADD (
  CONSTRAINT C_SRC_CAP_END_DATE
  CHECK (  SRC_CAP_END_DATE >= SRC_CAP_BGN_DATE)
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY ADD (
  CONSTRAINT C_SRC_CAP_ID_XREF
  CHECK (   SUBSTR(RCPT_METHOD_NAME,1,8) = 'ID XREF ')
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY ADD (
  CONSTRAINT C_SRCCAP_PK
  PRIMARY KEY
  (ID, ID_TYPE, MET_DOMAIN_NAME, SRC_CAP_BGN_DATE)
  USING INDEX C_SRCCAP_PK
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY ADD (
  CONSTRAINT C_SRCCAP_END_DATE
  UNIQUE (ID, ID_TYPE, MET_DOMAIN_NAME, SRC_CAP_END_DATE)
  USING INDEX C_SRCCAP_END_DATE
  ENABLE VALIDATE);



--
-- SRC_CAPABILITY_NODATA  (Table) 
--
CREATE TABLE SRC_CAPABILITY_NODATA
(
  ID                     VARCHAR2(8 BYTE)       NOT NULL,
  ID_TYPE                VARCHAR2(4 BYTE)       NOT NULL,
  MET_DOMAIN_NAME        VARCHAR2(8 BYTE)       NOT NULL,
  SRC_CAP_BGN_DATE       DATE                   NOT NULL,
  SRC_ID                 NUMBER(6)              NOT NULL,
  REC_ST_IND             NUMBER(4)              NOT NULL,
  PRIME_CAPABILITY_FLAG  VARCHAR2(1 BYTE)       NOT NULL,
  SRC_CAP_END_DATE       DATE,
  FIRST_ONLINE_OB_YR     NUMBER(4),
  DB_SEGMENT_NAME        VARCHAR2(12 BYTE),
  RCPT_METHOD_NAME       VARCHAR2(20 BYTE),
  DATA_RETENTION_PERIOD  NUMBER(3),
  COMM_MTHD_ID           NUMBER(6)
);


--
-- C_SCND_PK  (Index) 
--
--  Dependencies: 
--   SRC_CAPABILITY_NODATA (Table)
--
CREATE UNIQUE INDEX C_SCND_PK ON SRC_CAPABILITY_NODATA
(ID, ID_TYPE, MET_DOMAIN_NAME, SRC_CAP_BGN_DATE);
--
-- C_SCND_UNQ  (Index) 
--
--  Dependencies: 
--   SRC_CAPABILITY_NODATA (Table)
--
CREATE UNIQUE INDEX C_SCND_UNQ ON SRC_CAPABILITY_NODATA
(ID, ID_TYPE, MET_DOMAIN_NAME, SRC_CAP_END_DATE);

ALTER TABLE SRC_CAPABILITY_NODATA ADD (
  CONSTRAINT C_SCND_BGN_DATE_CHK
  CHECK (src_cap_bgn_date BETWEEN TO_DATE('16770101','YYYYMMDD') AND TO_DATE('39991231','YYYYMMDD'))
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY_NODATA ADD (
  CONSTRAINT C_SCND_BGN_END_DATE_CHK
  CHECK (src_cap_end_date >= src_cap_bgn_date)
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY_NODATA ADD (
  CONSTRAINT C_SCND_DATA_RETN_PER_CHK
  CHECK (data_retention_period >= 0000)
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY_NODATA ADD (
  CONSTRAINT C_SCND_END_DATE_CHK
  CHECK (src_cap_end_date BETWEEN TO_DATE('01011677','DDMMYYYY') AND TO_DATE('31123999','DDMMYYYY'))
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY_NODATA ADD (
  CONSTRAINT C_SCND_FIRST_OL_OB_YR_CHK
  CHECK (first_online_ob_yr BETWEEN 1738 AND 3999)
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY_NODATA ADD (
  CONSTRAINT C_SCND_ID_XREF_CHK
  CHECK (SUBSTR(rcpt_method_name,1,8) = 'ID XREF ')
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY_NODATA ADD (
  CONSTRAINT C_SCND_PRIME_CAP_FLAG_CHK
  CHECK (prime_capability_flag IN ('T','F'))
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY_NODATA ADD (
  CONSTRAINT C_SCND_RSI_CHK
  CHECK (rec_st_ind >= 0001)
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY_NODATA ADD (
  CONSTRAINT C_SCND_PK
  PRIMARY KEY
  (ID, ID_TYPE, MET_DOMAIN_NAME, SRC_CAP_BGN_DATE)
  USING INDEX C_SCND_PK
  ENABLE VALIDATE);

ALTER TABLE SRC_CAPABILITY_NODATA ADD (
  CONSTRAINT C_SCND_UNQ
  UNIQUE (ID, ID_TYPE, MET_DOMAIN_NAME, SRC_CAP_END_DATE)
  USING INDEX C_SCND_UNQ
  ENABLE VALIDATE);



--
-- STATION_AUTHORITY_HISTORY  (Table) 
--
--   Row Count: 2
CREATE TABLE STATION_AUTHORITY_HISTORY
(
  AUTHORITY_ID       NUMBER(6)                  NOT NULL,
  SRC_ID             NUMBER(6)                  NOT NULL,
  STN_AUTH_BGN_DATE  DATE                       NOT NULL,
  STN_AUTH_END_DATE  DATE                       NOT NULL,
  AUTH_HIST_RMRK     VARCHAR2(200 BYTE)
);

COMMENT ON COLUMN STATION_AUTHORITY_HISTORY.AUTHORITY_ID IS ' Foreign key to attribute in the AUTHORITY table';

COMMENT ON COLUMN STATION_AUTHORITY_HISTORY.SRC_ID IS ' Foreign key to attribute in the SOURCE table';

COMMENT ON COLUMN STATION_AUTHORITY_HISTORY.STN_AUTH_BGN_DATE IS ' Start date of relationship between station and authority';

COMMENT ON COLUMN STATION_AUTHORITY_HISTORY.STN_AUTH_END_DATE IS ' End date of relationship between station and authority';

COMMENT ON COLUMN STATION_AUTHORITY_HISTORY.AUTH_HIST_RMRK IS ' Remark on relationship';


--
-- PKSTATION_AUTHORITY_HISTORY  (Index) 
--
--  Dependencies: 
--   STATION_AUTHORITY_HISTORY (Table)
--
CREATE UNIQUE INDEX PKSTATION_AUTHORITY_HISTORY ON STATION_AUTHORITY_HISTORY
(AUTHORITY_ID, SRC_ID, STN_AUTH_BGN_DATE);

ALTER TABLE STATION_AUTHORITY_HISTORY ADD (
  CONSTRAINT C_SAH_SRC_ID
  CHECK (  SRC_ID >= 0)
  ENABLE VALIDATE);

ALTER TABLE STATION_AUTHORITY_HISTORY ADD (
  CONSTRAINT PKSTATION_AUTHORITY_HISTORY
  PRIMARY KEY
  (AUTHORITY_ID, SRC_ID, STN_AUTH_BGN_DATE)
  USING INDEX PKSTATION_AUTHORITY_HISTORY
  ENABLE VALIDATE);



--
-- STATION_GEOGRAPHY  (Table) 
--
--   Row Count: 2
CREATE TABLE STATION_GEOGRAPHY
(
  SRC_ID                    NUMBER(6)           NOT NULL,
  GEOG_UPD_DATE             DATE                NOT NULL,
  PR_GEOG_TYPE_CODE         VARCHAR2(8 BYTE)    NOT NULL,
  SCDY_GEOG_TYPE_CODE       VARCHAR2(8 BYTE),
  SITE_TYPE_CODE            VARCHAR2(20 BYTE)   NOT NULL,
  LAND_USE_TYPE_ID          NUMBER(2)           NOT NULL,
  GRND_SLPE_DSC             VARCHAR2(20 BYTE),
  GRND_SLPE_UP_DIR          NUMBER(3),
  GRADIENT                  NUMBER(3),
  PRC_MAN_WTHN_10M          NUMBER(3),
  PRC_VEG_WTHN_10M          NUMBER(3),
  PRC_MAN_WTHN_50M          NUMBER(3),
  PRC_VEG_WTHN_50M          NUMBER(3),
  SOIL_TYPE_ID              NUMBER(3),
  PRC_HEAT_SRC_WTHN_30M     NUMBER(3),
  PRC_VEG_WTHN_30M          NUMBER(3),
  PRC_HEAT_SRC_WTHN_100M    NUMBER(3),
  PRC_VEG_WTHN_100M         NUMBER(3),
  SFC_COVER_CLASS_SCHEME    VARCHAR2(20 BYTE),
  SFC_COVER_LESS_THAN_100M  VARCHAR2(20 BYTE),
  SFC_COVER_100M_3KM        VARCHAR2(20 BYTE),
  SFC_COVER_3KM_100KM       VARCHAR2(20 BYTE)
);

COMMENT ON TABLE STATION_GEOGRAPHY IS 'Table providing details of the geography associated with a station.';

COMMENT ON COLUMN STATION_GEOGRAPHY.SRC_ID IS 'Unique identifier of station';

COMMENT ON COLUMN STATION_GEOGRAPHY.GEOG_UPD_DATE IS 'Date on which record was updated';

COMMENT ON COLUMN STATION_GEOGRAPHY.PR_GEOG_TYPE_CODE IS 'Primary geography type at station';

COMMENT ON COLUMN STATION_GEOGRAPHY.SCDY_GEOG_TYPE_CODE IS 'Secondary geography type at station';

COMMENT ON COLUMN STATION_GEOGRAPHY.SITE_TYPE_CODE IS 'Unique code of site type';

COMMENT ON COLUMN STATION_GEOGRAPHY.LAND_USE_TYPE_ID IS 'Unique identifier of land use';

COMMENT ON COLUMN STATION_GEOGRAPHY.GRND_SLPE_DSC IS 'Description of ground slope (Level, Simple Complex)';

COMMENT ON COLUMN STATION_GEOGRAPHY.GRND_SLPE_UP_DIR IS 'Upward direction of ground slope (0-360)';

COMMENT ON COLUMN STATION_GEOGRAPHY.GRADIENT IS 'Gradient of ground slope (0-90)';

COMMENT ON COLUMN STATION_GEOGRAPHY.PRC_MAN_WTHN_10M IS 'Percentage manmade ground cover within 10m radius';

COMMENT ON COLUMN STATION_GEOGRAPHY.PRC_VEG_WTHN_10M IS 'Percentage vegetation ground cover greater than 0.3m height within 10m radius';

COMMENT ON COLUMN STATION_GEOGRAPHY.PRC_MAN_WTHN_50M IS 'Percentage manmade ground cover within 50m radius';

COMMENT ON COLUMN STATION_GEOGRAPHY.PRC_VEG_WTHN_50M IS 'Percentage vegetation ground cover greater than 0.3m height within 50m radius';

COMMENT ON COLUMN STATION_GEOGRAPHY.SOIL_TYPE_ID IS 'Unique identifier of soil type at station';

COMMENT ON COLUMN STATION_GEOGRAPHY.PRC_HEAT_SRC_WTHN_30M IS 'Percentage of area occupied by sources of heat within 30m radius';

COMMENT ON COLUMN STATION_GEOGRAPHY.PRC_VEG_WTHN_30M IS 'Percentage vegetation ground cover greater than 0.3m height within 30m radius';

COMMENT ON COLUMN STATION_GEOGRAPHY.PRC_HEAT_SRC_WTHN_100M IS 'Percentage of area occupied by sources of heat within 100m radius';

COMMENT ON COLUMN STATION_GEOGRAPHY.PRC_VEG_WTHN_100M IS 'Percentage vegetation ground cover greater than 0.3m height within 100m radius';

COMMENT ON COLUMN STATION_GEOGRAPHY.SFC_COVER_CLASS_SCHEME IS 'The surface cover classification scheme used to define the surface cover';

COMMENT ON COLUMN STATION_GEOGRAPHY.SFC_COVER_LESS_THAN_100M IS 'The type of surface over a radius of the station of less then 100m';

COMMENT ON COLUMN STATION_GEOGRAPHY.SFC_COVER_100M_3KM IS 'The type of surface over a radius of the station between 100m and 3km';

COMMENT ON COLUMN STATION_GEOGRAPHY.SFC_COVER_3KM_100KM IS 'The type of surface over a radius of the station between 100m and 3km';


--
-- PKSTATION_GEOGRAPHY  (Index) 
--
--  Dependencies: 
--   STATION_GEOGRAPHY (Table)
--
CREATE UNIQUE INDEX PKSTATION_GEOGRAPHY ON STATION_GEOGRAPHY
(SRC_ID, GEOG_UPD_DATE);

ALTER TABLE STATION_GEOGRAPHY ADD (
  CONSTRAINT C_SG_PRC_HSRC_100M
  CHECK (prc_heat_src_wthn_100m between 0 and 100)
  ENABLE VALIDATE);

ALTER TABLE STATION_GEOGRAPHY ADD (
  CONSTRAINT C_SG_PRC_HSRC_30M
  CHECK (prc_heat_src_wthn_30m between 0 and 100)
  ENABLE VALIDATE);

ALTER TABLE STATION_GEOGRAPHY ADD (
  CONSTRAINT C_SG_PRC_MAN_10M
  CHECK (  PRC_MAN_WTHN_10M BETWEEN 0 AND 100)
  ENABLE VALIDATE);

ALTER TABLE STATION_GEOGRAPHY ADD (
  CONSTRAINT C_SG_PRC_MAN_50M
  CHECK (  PRC_MAN_WTHN_50M BETWEEN 0 AND 100)
  ENABLE VALIDATE);

ALTER TABLE STATION_GEOGRAPHY ADD (
  CONSTRAINT C_SG_PRC_VEG_100M
  CHECK (prc_veg_wthn_100m between 0 and 100)
  ENABLE VALIDATE);

ALTER TABLE STATION_GEOGRAPHY ADD (
  CONSTRAINT C_SG_PRC_VEG_10M
  CHECK (  PRC_VEG_WTHN_10M BETWEEN 0 AND 100)
  ENABLE VALIDATE);

ALTER TABLE STATION_GEOGRAPHY ADD (
  CONSTRAINT C_SG_PRC_VEG_30M
  CHECK (prc_veg_wthn_30m between 0 and 100)
  ENABLE VALIDATE);

ALTER TABLE STATION_GEOGRAPHY ADD (
  CONSTRAINT C_SG_PRC_VEG_50M
  CHECK (  PRC_VEG_WTHN_50M BETWEEN 0 AND 100)
  ENABLE VALIDATE);

ALTER TABLE STATION_GEOGRAPHY ADD (
  CONSTRAINT C_SG_SRC_ID
  CHECK (  SRC_ID >= 0)
  ENABLE VALIDATE);

ALTER TABLE STATION_GEOGRAPHY ADD (
  CONSTRAINT PKSTATION_GEOGRAPHY
  PRIMARY KEY
  (SRC_ID, GEOG_UPD_DATE)
  USING INDEX PKSTATION_GEOGRAPHY
  ENABLE VALIDATE);



--
-- STATION_HISTORY  (Table) 
--
--   Row Count: 3
CREATE TABLE STATION_HISTORY
(
  SRC_ID             NUMBER(6)                  NOT NULL,
  EVENT_DATE         DATE                       NOT NULL,
  EVENT_TEXT         VARCHAR2(150 BYTE)         NOT NULL,
  EVENT_RESULT_TEXT  VARCHAR2(150 BYTE)         NOT NULL
);

COMMENT ON COLUMN STATION_HISTORY.SRC_ID IS ' Unique identifier of station';

COMMENT ON COLUMN STATION_HISTORY.EVENT_DATE IS ' Date of event';

COMMENT ON COLUMN STATION_HISTORY.EVENT_TEXT IS ' Textual description of event';

COMMENT ON COLUMN STATION_HISTORY.EVENT_RESULT_TEXT IS ' Any result of the event';


--
-- PKSTATION_HISTORY  (Index) 
--
--  Dependencies: 
--   STATION_HISTORY (Table)
--
CREATE UNIQUE INDEX PKSTATION_HISTORY ON STATION_HISTORY
(SRC_ID, EVENT_DATE);

ALTER TABLE STATION_HISTORY ADD (
  CONSTRAINT C_SEH_SRC_ID
  CHECK (  SRC_ID >= 0)
  ENABLE VALIDATE);

ALTER TABLE STATION_HISTORY ADD (
  CONSTRAINT PKSTATION_HISTORY
  PRIMARY KEY
  (SRC_ID, EVENT_DATE)
  USING INDEX PKSTATION_HISTORY
  ENABLE VALIDATE);



--
-- STATION_INVENTORY_STATUS  (Table) 
--
--   Row Count: 1
CREATE TABLE STATION_INVENTORY_STATUS
(
  SRC_ID             NUMBER(6)                  NOT NULL,
  INVENTORY_CODE     CHAR(1 BYTE)               NOT NULL,
  INVT_STS_BGN_DATE  DATE                       NOT NULL,
  INVT_STS_END_DATE  DATE                       NOT NULL,
  INVT_STS_RMRK      VARCHAR2(200 BYTE)
);

COMMENT ON COLUMN STATION_INVENTORY_STATUS.SRC_ID IS ' Unique identifier of station';

COMMENT ON COLUMN STATION_INVENTORY_STATUS.INVENTORY_CODE IS ' Unique code for inventory status';

COMMENT ON COLUMN STATION_INVENTORY_STATUS.INVT_STS_BGN_DATE IS ' Date at which this status starts for this station';

COMMENT ON COLUMN STATION_INVENTORY_STATUS.INVT_STS_END_DATE IS ' Date at which this status ends for this station';

COMMENT ON COLUMN STATION_INVENTORY_STATUS.INVT_STS_RMRK IS ' Any remarks applicable to this record';


--
-- PKSTATION_INVENTORY_STATUS  (Index) 
--
--  Dependencies: 
--   STATION_INVENTORY_STATUS (Table)
--
CREATE UNIQUE INDEX PKSTATION_INVENTORY_STATUS ON STATION_INVENTORY_STATUS
(SRC_ID, INVENTORY_CODE, INVT_STS_BGN_DATE);

ALTER TABLE STATION_INVENTORY_STATUS ADD (
  CONSTRAINT C_SIS_SRC_ID
  CHECK (  SRC_ID >= 0)
  ENABLE VALIDATE);

ALTER TABLE STATION_INVENTORY_STATUS ADD (
  CONSTRAINT PKSTATION_INVENTORY_STATUS
  PRIMARY KEY
  (SRC_ID, INVENTORY_CODE, INVT_STS_BGN_DATE)
  USING INDEX PKSTATION_INVENTORY_STATUS
  ENABLE VALIDATE);



--
-- STATION_OBSERVER  (Table) 
--
--   Row Count: 1
CREATE TABLE STATION_OBSERVER
(
  OBSERVER_ID         NUMBER(6)                 NOT NULL,
  SRC_ID              NUMBER(6)                 NOT NULL,
  STN_OBSR_BGN_DATE   DATE                      NOT NULL,
  STN_OBSR_END_DATE   DATE                      NOT NULL,
  OBSERVER_ROLE_CODE  CHAR(4 BYTE)              NOT NULL
);

COMMENT ON COLUMN STATION_OBSERVER.OBSERVER_ID IS ' Unique identifier of observer';

COMMENT ON COLUMN STATION_OBSERVER.SRC_ID IS ' Unique identifier of station';

COMMENT ON COLUMN STATION_OBSERVER.STN_OBSR_BGN_DATE IS ' Date at which observer started at station';

COMMENT ON COLUMN STATION_OBSERVER.STN_OBSR_END_DATE IS ' Date at which observer ended at station';

COMMENT ON COLUMN STATION_OBSERVER.OBSERVER_ROLE_CODE IS ' Code describing the role of the observer at the station';


--
-- PKSTATION_OBSERVER  (Index) 
--
--  Dependencies: 
--   STATION_OBSERVER (Table)
--
CREATE UNIQUE INDEX PKSTATION_OBSERVER ON STATION_OBSERVER
(OBSERVER_ID, SRC_ID, STN_OBSR_BGN_DATE);

ALTER TABLE STATION_OBSERVER ADD (
  CONSTRAINT C_SO_SRC_ID
  CHECK (  SRC_ID >= 0)
  ENABLE VALIDATE);

ALTER TABLE STATION_OBSERVER ADD (
  CONSTRAINT PKSTATION_OBSERVER
  PRIMARY KEY
  (OBSERVER_ID, SRC_ID, STN_OBSR_BGN_DATE)
  USING INDEX PKSTATION_OBSERVER
  ENABLE VALIDATE);



--
-- STATION_REPORT_ELEMENT  (Table) 
--
--   Row Count: 386
CREATE TABLE STATION_REPORT_ELEMENT
(
  STN_RPT_ELEM_ID    NUMBER(6)                  NOT NULL,
  ID                 VARCHAR2(8 BYTE),
  ID_TYPE            VARCHAR2(4 BYTE)           NOT NULL,
  SRC_CAP_BGN_DATE   DATE                       NOT NULL,
  MET_DOMAIN_NAME    VARCHAR2(8 BYTE)           NOT NULL,
  MET_ELEMENT_ID     NUMBER(5)                  NOT NULL,
  RPT_ELEM_BGN_DATE  DATE                       NOT NULL,
  RPT_ELEM_END_DATE  DATE                       NOT NULL
);


--
-- PKSTATION_REPORT_ELEMENT  (Index) 
--
--  Dependencies: 
--   STATION_REPORT_ELEMENT (Table)
--
CREATE UNIQUE INDEX PKSTATION_REPORT_ELEMENT ON STATION_REPORT_ELEMENT
(STN_RPT_ELEM_ID);

ALTER TABLE STATION_REPORT_ELEMENT ADD (
  CONSTRAINT PKSTATION_REPORT_ELEMENT
  PRIMARY KEY
  (STN_RPT_ELEM_ID)
  USING INDEX PKSTATION_REPORT_ELEMENT
  ENABLE VALIDATE);



--
-- STATION_ROLE  (Table) 
--
--   Row Count: 10
CREATE TABLE STATION_ROLE
(
  SRC_ID          NUMBER(6)                     NOT NULL,
  ROLE_NAME_CODE  VARCHAR2(11 BYTE)             NOT NULL,
  ROLE_BGN_DATE   DATE                          NOT NULL,
  ROLE_END_DATE   DATE                          NOT NULL
);

COMMENT ON COLUMN STATION_ROLE.SRC_ID IS ' Unique identifier of the station';

COMMENT ON COLUMN STATION_ROLE.ROLE_NAME_CODE IS ' Unique code for the particular role ';

COMMENT ON COLUMN STATION_ROLE.ROLE_BGN_DATE IS ' Date on which station is first associated with role';

COMMENT ON COLUMN STATION_ROLE.ROLE_END_DATE IS ' Date on which station is last associated with role';


--
-- PKSTATION_ROLE  (Index) 
--
--  Dependencies: 
--   STATION_ROLE (Table)
--
CREATE UNIQUE INDEX PKSTATION_ROLE ON STATION_ROLE
(SRC_ID, ROLE_NAME_CODE, ROLE_BGN_DATE);

ALTER TABLE STATION_ROLE ADD (
  CONSTRAINT C_SR_SRC_ID
  CHECK (  SRC_ID >= 0)
  ENABLE VALIDATE);

ALTER TABLE STATION_ROLE ADD (
  CONSTRAINT PKSTATION_ROLE
  PRIMARY KEY
  (SRC_ID, ROLE_NAME_CODE, ROLE_BGN_DATE)
  USING INDEX PKSTATION_ROLE
  ENABLE VALIDATE);



--
-- STATION_STATUS  (Table) 
--
--   Row Count: 3
CREATE TABLE STATION_STATUS
(
  STATUS_CODE      CHAR(4 BYTE)                 NOT NULL,
  SRC_ID           NUMBER(6)                    NOT NULL,
  STATUS_BGN_DATE  DATE                         NOT NULL,
  STATUS_END_DATE  DATE                         NOT NULL,
  ROLE_NAME_CODE   VARCHAR2(8 BYTE)
);

COMMENT ON COLUMN STATION_STATUS.STATUS_CODE IS ' Unique code for status';

COMMENT ON COLUMN STATION_STATUS.SRC_ID IS ' Unique identifier for station';

COMMENT ON COLUMN STATION_STATUS.STATUS_BGN_DATE IS ' Begin date for status record';

COMMENT ON COLUMN STATION_STATUS.STATUS_END_DATE IS ' End date for status record';

COMMENT ON COLUMN STATION_STATUS.ROLE_NAME_CODE IS ' Role name associated with status record';


--
-- PKSTATION_STATUS  (Index) 
--
--  Dependencies: 
--   STATION_STATUS (Table)
--
CREATE UNIQUE INDEX PKSTATION_STATUS ON STATION_STATUS
(STATUS_CODE, SRC_ID, STATUS_BGN_DATE);

ALTER TABLE STATION_STATUS ADD (
  CONSTRAINT C_SS_SRC_ID
  CHECK (  SRC_ID >= 0)
  ENABLE VALIDATE);

ALTER TABLE STATION_STATUS ADD (
  CONSTRAINT PKSTATION_STATUS
  PRIMARY KEY
  (STATUS_CODE, SRC_ID, STATUS_BGN_DATE)
  USING INDEX PKSTATION_STATUS
  ENABLE VALIDATE);



--
-- EC_CALIB_EQUIP_CHECK_FK  (Index) 
--
--  Dependencies: 
--   EQUIPMENT_CALIBRATION (Table)
--
CREATE INDEX EC_CALIB_EQUIP_CHECK_FK ON EQUIPMENT_CALIBRATION
(CHECK_EQUIPMENT_ID);

--
-- EC_EQUIPMENT_FK  (Index) 
--
--  Dependencies: 
--   EQUIPMENT_CALIBRATION (Table)
--
CREATE INDEX EC_EQUIPMENT_FK ON EQUIPMENT_CALIBRATION
(EQUIPMENT_ID);

--
-- PKDEPLOYMENT  (Index) 
--
--  Dependencies: 
--   DEPLOYMENT_DETAIL (Table)
--
CREATE INDEX PKDEPLOYMENT ON DEPLOYMENT_DETAIL
(DEPLOYMENT_ID);

--
-- PKDEPLOYMENT_ATTRIBUTE  (Index) 
--
--  Dependencies: 
--   DEPLOYMENT_DETAIL (Table)
--
CREATE INDEX PKDEPLOYMENT_ATTRIBUTE ON DEPLOYMENT_DETAIL
(DEPL_ATTR_ID);

--
-- PKD_EQUIPMENT  (Index) 
--
--  Dependencies: 
--   DEPLOYMENT (Table)
--
CREATE INDEX PKD_EQUIPMENT ON DEPLOYMENT
(EQUIPMENT_ID);

--
-- PKD_EQUIPMENT_TYPE  (Index) 
--
--  Dependencies: 
--   DEPLOYMENT (Table)
--
CREATE INDEX PKD_EQUIPMENT_TYPE ON DEPLOYMENT
(EQUIPMENT_TYPE_ID);

--
-- PKD_ID  (Index) 
--
--  Dependencies: 
--   DEPLOYMENT (Table)
--
CREATE INDEX PKD_ID ON DEPLOYMENT
(ID, ID_TYPE);

--
-- PKD_MET_ROLE  (Index) 
--
--  Dependencies: 
--   DEPLOYMENT (Table)
--
CREATE INDEX PKD_MET_ROLE ON DEPLOYMENT
(MET_ROLE_ID);

--
-- PKD_OBSERVING_SYSTEM  (Index) 
--
--  Dependencies: 
--   DEPLOYMENT (Table)
--
CREATE INDEX PKD_OBSERVING_SYSTEM ON DEPLOYMENT
(OB_SYS_NAME);

--
-- PKD_STATION  (Index) 
--
--  Dependencies: 
--   DEPLOYMENT (Table)
--
CREATE INDEX PKD_STATION ON DEPLOYMENT
(SRC_ID);

--
-- PKI_STATION  (Index) 
--
--  Dependencies: 
--   INSPECTION (Table)
--
CREATE INDEX PKI_STATION ON INSPECTION
(SRC_ID);

--
-- PKOSI_OBS_SYSTEM_VERSION  (Index) 
--
--  Dependencies: 
--   OBSERVING_SYSTEM_INSTALLATION (Table)
--
CREATE INDEX PKOSI_OBS_SYSTEM_VERSION ON OBSERVING_SYSTEM_INSTALLATION
(OB_SYS_VRSN_ID);

--
-- PKOSI_STATION  (Index) 
--
--  Dependencies: 
--   OBSERVING_SYSTEM_INSTALLATION (Table)
--
CREATE INDEX PKOSI_STATION ON OBSERVING_SYSTEM_INSTALLATION
(SRC_ID);

--
-- PKSIS_STATION  (Index) 
--
--  Dependencies: 
--   STATION_INVENTORY_STATUS (Table)
--
CREATE INDEX PKSIS_STATION ON STATION_INVENTORY_STATUS
(SRC_ID);

--
-- PKSO_OBSERVER  (Index) 
--
--  Dependencies: 
--   STATION_OBSERVER (Table)
--
CREATE INDEX PKSO_OBSERVER ON STATION_OBSERVER
(OBSERVER_ID);

--
-- PKSO_OBSERVER_ROLE  (Index) 
--
--  Dependencies: 
--   STATION_OBSERVER (Table)
--
CREATE INDEX PKSO_OBSERVER_ROLE ON STATION_OBSERVER
(OBSERVER_ROLE_CODE);

--
-- PKSO_STATION  (Index) 
--
--  Dependencies: 
--   STATION_OBSERVER (Table)
--
CREATE INDEX PKSO_STATION ON STATION_OBSERVER
(SRC_ID);

--
-- PKSS_ROLE  (Index) 
--
--  Dependencies: 
--   STATION_STATUS (Table)
--
CREATE INDEX PKSS_ROLE ON STATION_STATUS
(ROLE_NAME_CODE);

--
-- PKSS_STATION  (Index) 
--
--  Dependencies: 
--   STATION_STATUS (Table)
--
CREATE INDEX PKSS_STATION ON STATION_STATUS
(SRC_ID);

--
-- PKSS_STATUS  (Index) 
--
--  Dependencies: 
--   STATION_STATUS (Table)
--
CREATE INDEX PKSS_STATUS ON STATION_STATUS
(STATUS_CODE);

--
-- SIS_INVENTORY_TYPE  (Index) 
--
--  Dependencies: 
--   STATION_INVENTORY_STATUS (Table)
--
CREATE INDEX SIS_INVENTORY_TYPE ON STATION_INVENTORY_STATUS
(INVENTORY_CODE);
