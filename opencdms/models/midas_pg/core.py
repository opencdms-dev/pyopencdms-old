# coding: utf-8
from sqlalchemy import CHAR, CheckConstraint, Column, DateTime, Enum, \
    ForeignKey, Index, VARCHAR, text, NUMERIC, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class Equipment(Base):
    __tablename__ = 'equipment'
    __table_args__ = {
        'comment': 'The details of the items of equipment deployed at a '
                   'station. Related by the equipment ID to the deployment '
                   'table. The EQPT_PRCT_DATE and EQPT_DSPL_DATE are for '
                   'equipment procurement and equipment disposal dates '
                   'respectively.\nHowever, they are more often used to '
                   'record calibration validity start and end dates '
                   'respectively.'}

    equipment_id = Column(NUMERIC(6, 0, False), primary_key=True,
                          comment='Unique identifier for piece of equipment '
                                  'in Metadata')
    equipment_type_id = Column(NUMERIC(6, 0, False), nullable=False,
                               comment='Unique identifier for equipment type')
    manufacturer_name = Column(VARCHAR(28), nullable=False,
                               comment='Name of equipment manufacturer')
    manufacturer_sn_txt = Column(VARCHAR(24), nullable=False,
                                 comment='Manufacturer serial number or SI '
                                         'database Sensor_serial_no ')
    met_ref_txt = Column(VARCHAR(24),
                         comment='Met Office reference number or SI database '
                                 'Asset_id')
    eqpt_prct_date = Column(DateTime,
                            comment='Equipment procurement date, or date of '
                                    'calibration')
    equipment_cost = Column(NUMERIC(6, 2, True), comment='Cost of equipment')
    eqpt_dspl_date = Column(DateTime,
                            comment='Equipment disposal date, or date '
                                    'calibration expires.')
    eqpt_dspl_rmrk = Column(VARCHAR(200), comment='Equipment disposal remark')
    eqpt_last_updated_date = Column(DateTime,
                                    comment='Date at which this equipment was '
                                            'inserted or last updated')


class ReportingSchedule(Base):
    __tablename__ = 'reporting_schedule'
    __table_args__ = (
        Index('c_rps_unq', 'id', 'id_type', 'met_domain_name',
              'src_cap_bgn_date', 'rpt_schd_bgn_date', 'rpt_schd_end_date',
              'year_date_bgn', 'year_date_end', 'week_day_bgn', 'week_day_end',
              'time_of_day_bgn', 'time_of_day_end', 'reporting_interval',
              'reporting_method', 'public_holiday_flag', unique=True),
    )

    report_schedule_id = Column(NUMERIC(6, 0, False), primary_key=True,
                                comment='Unique identifier for each record')
    id = Column(VARCHAR(8), comment='Non unique identifier for station')
    id_type = Column(VARCHAR(4), nullable=False,
                     comment='Type of identifier above')
    met_domain_name = Column(VARCHAR(8), nullable=False,
                             comment='Describes the route from which the data '
                                     'came')
    src_cap_bgn_date = Column(DateTime, nullable=False,
                              comment='Start date of the SRC_CAPABILITY record')
    rpt_schd_bgn_date = Column(DateTime, nullable=False,
                               comment='Start date of record')
    rpt_schd_end_date = Column(DateTime, nullable=False,
                               comment='End date of record')
    year_date_bgn = Column(CHAR(5), nullable=False,
                           comment='First month/year of report (format mm/yy)')
    year_date_end = Column(CHAR(5), nullable=False,
                           comment='Last month/year of report (format mm/yy)')
    week_day_bgn = Column(NUMERIC(1, 0, False), nullable=False,
                          comment='First day of week of report')
    week_day_end = Column(NUMERIC(1, 0, False), nullable=False,
                          comment='Last day of week of report')
    time_of_day_bgn = Column(NUMERIC(4, 0, False), nullable=False,
                             comment='First time of day of report')
    time_of_day_end = Column(NUMERIC(4, 0, False), nullable=False,
                             comment='Last time of day of report')
    reporting_interval = Column(NUMERIC(4, 0, False), nullable=False,
                                comment='Number of minutes between each report')
    reporting_method = Column(VARCHAR(9), nullable=False,
                              comment='Either Manual or Automatic')
    public_holiday_flag = Column(CHAR(1), nullable=False,
                                 comment='T or F. Shows whether the report'
                                         ' comes in on a bank holiday')
    rpt_schd_rmrk = Column(VARCHAR(200), comment='Remark for the record')


class Source(Base):
    __tablename__ = 'source'
    __table_args__ = (
        CheckConstraint('REC_ST_IND >= 1001'),
        CheckConstraint('SRC_END_DATE >= SRC_BGN_DATE'),
        CheckConstraint('SRC_END_DATE >= SRC_BGN_DATE'),
        CheckConstraint('SRC_ID <> parent_src_id'),
        CheckConstraint('SRC_ID <> parent_src_id'),
        CheckConstraint('SRC_ID >= 0'),
        CheckConstraint('ZONE_TIME BETWEEN -12 AND 12'),
        CheckConstraint('high_prcn_lat BETWEEN -90.000 AND 90.000'),
        CheckConstraint('high_prcn_lon BETWEEN -179.999 AND 180.000'),
        CheckConstraint(" wmo_region_code BETWEEN '1'AND '7'"),
        CheckConstraint('EAST_GRID_REF >= 0'),
        CheckConstraint('NORTH_GRID_REF >= 0'),
        CheckConstraint(
            "SRC_BGN_DATE BETWEEN "
            " TO_DATE('01011677','DDMMYYYY') AND TO_DATE('31123999','DDMMYYYY')"),
        CheckConstraint(
            "SRC_END_DATE BETWEEN"
            " TO_DATE('01011677','DDMMYYYY') AND TO_DATE('31123999','DDMMYYYY')"),
        CheckConstraint(
            "SRC_UPD_DATE BETWEEN"
            " TO_DATE('01011677','DDMMYYYY') AND TO_DATE('31123999','DDMMYYYY')"),
        CheckConstraint('parent_src_id >= 0'),
        CheckConstraint(
            "src_type IN "
            "('SFC','SFC UA','SFC ANEMO','SFC AWS'"
            ",'SFC BUOY','SFC LV','SFC OCEAN',\n"
            "'SFC OWS','SFC PLAT','SFC RIG',"
            "'SFC SAMOS','SFC SIESAWS','BOGUS1',\n"
            "'BOGUS2','UA')")
    )

    src_id = Column(NUMERIC(6, 0, False), primary_key=True,
                    comment='\nThis is an identifier for each source'
                            ' of meteorological data within the system. '
                            'It acts as a unique identifier when a source may '
                            'be of various types.  It consists of a 6 digit '
                            'integer, assigned from a high-number record, '
                            'and has no external significance.\n')
    src_name = Column(VARCHAR(40), nullable=False, comment='\nName of source\n')
    high_prcn_lat = Column(NUMERIC(7, 5, True), nullable=False)
    high_prcn_lon = Column(NUMERIC(8, 5, True), nullable=False)
    loc_geog_area_id = Column(VARCHAR(4), nullable=False,
                              comment='\nGeographic area where the source is'
                                      ' located, connected at the lowest level'
                                      ' by using the geographic area id'
                                      ' of the location.\n')
    rec_st_ind = Column(NUMERIC(4, 0, False), nullable=False)
    src_bgn_date = Column(DateTime,
                          comment='\nsource.src_bgn_date '
                                  'is the date when the station opened.\n')
    src_type = Column(VARCHAR(15))
    grid_ref_type = Column(
        Enum('CI', 'IRL', 'OS', 'XX', 'ROI', name="grid_ref_type_enum"),
        nullable=False, server_default=text("'XX'"),
        comment='\nThis attribute describes the type of grid '
                'reference.\nValue List:\nCI = Channel Islands grid\n'
                'IRL = Irish grid\nOS = Ordnance Survey British National grid '
                'reference\nUnspecified, usually over-seas.\n')
    east_grid_ref = Column(NUMERIC(6, 0, False),
                           comment='\nAs a compound with North Grid reference can indicate a location to within a 100 metre square.\n')
    north_grid_ref = Column(NUMERIC(7, 0, False),
                            comment='\nAs a compound with east grid reference can give a location of a site to a 100 m square.\n')
    hydr_area_id = Column(NUMERIC(4, 0, False),
                          comment='\nHydrometric area identification number.  Rainfall stations are located in a hydrometric area assigned clockwise round the country starting in North Scotland.\nHydrometric area numbers are in the HHHh format, where HHH is the original number allocated in the 1930s, and h is the sub-division resulting from water authority re-organizations.  Thus, when h=0 the boundary remains that defined n the 1930s.\nIn MIDAS, it links an area to sources.\n')
    post_code = Column(VARCHAR(9))
    src_end_date = Column(DateTime,
                          comment='\nsource.src_end_date is the date when the station closed\n')
    elevation = Column(NUMERIC(6, 2, True),
                       comment='\nHeight of ground surface above mean sea level.  See also height.\n')
    wmo_region_code = Column(CHAR(1),
                             comment='\nWMO Code A1 Code table 0161. WMO Regional Association area in which buoy, drilling rig or oil- or gas-production platform has been deployed.\nValues: 1 = Africa, 2 = Asia, 3 = South America, 4 = North America, 5 = Australasia, 6 = Europe, 7 = Antactica.\n')
    parent_src_id = Column(NUMERIC(6, 0, False), comment='\n')
    zone_time = Column(NUMERIC(2, 0, False),
                       comment='\nDifference from UTC (hours) for overseas stations.\n')
    drainage_stream_id = Column(VARCHAR(4),
                                comment='\nDrainage streams or coastal name identification number to link area to source information. New item but drainage stream information from ML.HYDROSET\n')
    src_upd_date = Column(DateTime, comment='\nsource_updated_date\n')
    mtce_ctre_code = Column(VARCHAR(4),
                            comment='\nAbbreviated form of the maintenance centre name.\n')
    place_id = Column(NUMERIC(6, 0, False), server_default=text("NULL"),
                      comment='\nAttribute Description -\n')
    lat_wgs84 = Column(NUMERIC(7, 5, True))
    lon_wgs84 = Column(NUMERIC(8, 5, True))
    src_guid = Column(UUID, unique=True,
                      server_default=text("gen_random_uuid()"),
                      comment='Global Unique ID - RAW32 - default sys_guid()')
    src_geom = Column(JSON, comment='SRID 8307 geometry (WGS84 lat/lon)')
    src_location_type = Column(VARCHAR(50),
                               comment='Categorisation of location e.g. UKMO_SURFACE_LAND')


class StationReportElement(Base):
    __tablename__ = 'station_report_element'

    stn_rpt_elem_id = Column(NUMERIC(6, 0, False), primary_key=True)
    id = Column(VARCHAR(8))
    id_type = Column(VARCHAR(4), nullable=False)
    src_cap_bgn_date = Column(DateTime, nullable=False)
    met_domain_name = Column(VARCHAR(8), nullable=False)
    met_element_id = Column(NUMERIC(5, 0, False), nullable=False)
    rpt_elem_bgn_date = Column(DateTime, nullable=False)
    rpt_elem_end_date = Column(DateTime, nullable=False)


class Deployment(Base):
    __tablename__ = 'deployment'
    __table_args__ = (
        CheckConstraint('HIGH_PRCN_LAT BETWEEN -90.000 AND 90.000'),
        CheckConstraint('HIGH_PRCN_LON BETWEEN -179.999 AND 180.000'),
        CheckConstraint('SRC_ID >= 0'),
        Index('pkd_id', 'id', 'id_type'),
        {
            'comment': 'An instance of a piece of equipment being deployed for a purpose. Provision is made for the situation where only the type of equipment is known, by carrying Instrument Type ID as a foreign key, and making the relationship with the Equipment entity optional. Need to ensure that, if a specific piece of equipment is recorded (via Equipment ID), the attribute Equipment Type ID is automatically set to the value of the corresponding attribute in Equipment.'}
    )

    deployment_id = Column(NUMERIC(6, 0, False), primary_key=True,
                           comment='Unique identifier of each deployment record')
    src_id = Column(ForeignKey('source.src_id'), nullable=False, index=True,
                    comment='Unique identifier for station in MIDAS  ')
    id = Column(VARCHAR(8), comment='Identifier associated with station')
    id_type = Column(VARCHAR(4), nullable=False,
                     comment='Identifier type describing identifier above')
    # equipment_id = Column(ForeignKey('equipment.equipment_id'), index=True,
    #                       comment='Unique identifier of piece of equipment')
    equipment_type_id = Column(NUMERIC(6, 0, False), nullable=False, index=True,
                               comment='Unique identifier for equipment type')
    met_office_eqpt_flag = Column(CHAR(1), nullable=False,
                                  comment='Flag describing whether Met Office owns equipment or not (T or F)')
    ob_sys_name = Column(VARCHAR(12), index=True,
                         comment='Name of observing system if present')
    met_role_id = Column(NUMERIC(3, 0, False), index=True,
                         comment='Identifier describing the purpose of the equipment')
    depl_bgn_date = Column(DateTime, nullable=False,
                           comment='Begin date of deployment')
    depl_end_date = Column(DateTime, nullable=False,
                           comment='End date of deployment')
    grid_ref_type = Column(VARCHAR(4),
                           comment='Grid reference type (OS, IRL or CI)')
    east_grid_ref = Column(NUMERIC(6, 0, False),
                           comment='East grid reference of deployment')
    north_grid_ref = Column(NUMERIC(7, 0, False),
                            comment='North grid reference of deployment')
    high_prcn_lat = Column(NUMERIC(7, 5, True),
                           comment='Latitude of deployment in degrees to 5 decimal places')
    high_prcn_lon = Column(NUMERIC(8, 5, True),
                           comment='Longitude of deployment in degrees to 5 decimal places')
    elevation = Column(NUMERIC(6, 2, True), comment='Elevation of deployment')
    deployment_remark = Column(VARCHAR(250), comment='Remark about deployment')
    lat_wgs84 = Column(NUMERIC(7, 5, True),
                       comment='WGS84 Latitude of deployment in degrees to 5 decimal places')
    lon_wgs84 = Column(NUMERIC(8, 5, True),
                       comment='WGS84 Longitude of deployment in degrees to 5 decimal places')
    ipr_owner = Column(VARCHAR(12),
                       comment='Code identifying who owns the intellectual property rights of the deployed equipment.')
    egm96_elevation = Column(NUMERIC(6, 2, True))

    # equipment = relationship('Equipment')
    src = relationship('Source')

###
# For now, it's disabled. It throws this error
#
#     def do_execute(self, cursor, statement, parameters, context=None):
# >       cursor.execute(statement, parameters)
# E       sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn) column "equipment_id" referenced in foreign key constraint does not exist
# E
# E       [SQL:
# E       CREATE TABLE equipment_calibration (
# E       	eqpt_calib_id NUMERIC(6, 0) NOT NULL,
# E       	equipment_id INTEGER NOT NULL,
# E       	eqpt_calib_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
# E       	calib_mthd_code VARCHAR(4) NOT NULL,
# E       	eqpt_calib_next_due_date TIMESTAMP WITHOUT TIME ZONE,
# E       	eqpt_calib_name VARCHAR(28),
# E       	check_equipment_id INTEGER,
# E       	eqpt_calib_rmrk VARCHAR(200),
# E       	PRIMARY KEY (eqpt_calib_id),
# E       	FOREIGN KEY(equipment_id) REFERENCES equipment (equipment_id),
# E       	FOREIGN KEY(check_equipment_id) REFERENCES equipment (equipment_id)
# E       )
# E
# E       ]
# E       (Background on this error at: https://sqlalche.me/e/14/f405)
#
# /opt/hostedtoolcache/Python/3.8.12/x64/lib/python3.8/site-packages/sqlalchemy/engine/default.py:717: ProgrammingError
#
class EquipmentCalibration(Base):
    __tablename__ = 'equipment_calibration'

    eqpt_calib_id = Column(NUMERIC(6, 0, False), primary_key=True,
                           comment='Unique identifier for calibration of this equipment')
    # equipment_id = Column(Integer, ForeignKey('equipment.equipment_id'),
    #                       nullable=False, index=True,
    #                       comment='Unique identifier of equipment')
    eqpt_calib_date = Column(DateTime, nullable=False,
                             comment='Date on which calibration was carried out')
    calib_mthd_code = Column(VARCHAR(4), nullable=False,
                             comment='Code for method of calibration')
    eqpt_calib_next_due_date = Column(DateTime,
                                      comment='Date on which next calibration is due')
    eqpt_calib_name = Column(VARCHAR(28),
                             comment='Name of person carrying out calibration')
    # check_equipment_id = Column(Integer, ForeignKey('equipment.equipment_id'),
    #                             index=True,
    #                             comment='Unique identifier for check equipment used')
    eqpt_calib_rmrk = Column(VARCHAR(200), comment='Remark on the calibration')

    # check_equipment = relationship('Equipment',
    #                                foreign_keys=[check_equipment_id])
    # equipment = relationship('Equipment')


class Inspection(Base):
    __tablename__ = 'inspection'
    __table_args__ = (
        CheckConstraint('SRC_ID >= 0'),
        {
            'comment': 'Provides a record of inspections carried out at stations and related to the midas.source table'}
    )

    inspection_id = Column(NUMERIC(6, 0, False), primary_key=True,
                           comment='Unique identifier for the inspection')
    src_id = Column(ForeignKey('source.src_id'), nullable=False, index=True,
                    comment='Unique identifier for the station')
    inspection_date = Column(DateTime, nullable=False,
                             comment='Date of inspection')
    inspectors_name = Column(VARCHAR(70), nullable=False,
                             comment='Name of inspector')
    review_date = Column(DateTime,
                         comment='Date on which inspection should be reviewed')
    inspection_remark = Column(VARCHAR(700), comment='Remark on inspection')

    src = relationship('Source')


class ObservingSchedule(Base):
    __tablename__ = 'observing_schedule'
    __table_args__ = (
        Index('c_obs_unq', 'stn_rpt_elem_id', 'ob_schd_bgn_date',
              'ob_schd_end_date', 'year_date_bgn', 'year_date_end',
              'week_day_bgn', 'week_day_end', 'time_of_day_bgn',
              'time_of_day_end', 'observing_interval', 'public_holiday_flag',
              unique=True),
    )

    ob_schd_id = Column(NUMERIC(6, 0, False), primary_key=True,
                        comment='Unique number of the record')
    stn_rpt_elem_id = Column(
        ForeignKey('station_report_element.stn_rpt_elem_id',
                   ondelete='CASCADE'), nullable=False,
        comment='Unique identifier of the element for the station')
    ob_schd_bgn_date = Column(DateTime, nullable=False,
                              comment='Start date of record')
    ob_schd_end_date = Column(DateTime, nullable=False,
                              comment='End date of record')
    year_date_bgn = Column(CHAR(5), nullable=False,
                           comment='First month/year of report (format mm/yy)')
    year_date_end = Column(CHAR(5), nullable=False,
                           comment='Last month/year of report (format mm/yy)')
    week_day_bgn = Column(NUMERIC(1, 0, False), nullable=False,
                          comment='First day of week of report')
    week_day_end = Column(NUMERIC(1, 0, False), nullable=False,
                          comment='Last day of week of report')
    time_of_day_bgn = Column(NUMERIC(4, 0, False), nullable=False,
                             comment='First time of day of report')
    time_of_day_end = Column(NUMERIC(4, 0, False), nullable=False,
                             comment='Last time of day of report')
    observing_interval = Column(NUMERIC(4, 0, False), nullable=False,
                                comment='Number of minutes between each report')
    public_holiday_flag = Column(CHAR(1), nullable=False,
                                 comment='T or F. Shows whether the report comes in on a bank holiday')
    ob_schd_rmrk = Column(VARCHAR(200), comment='Remark for the record')

    stn_rpt_elem = relationship('StationReportElement')


class ObservingSystemInstallation(Base):
    __tablename__ = 'observing_system_installation'
    __table_args__ = (
        CheckConstraint('SRC_ID >= 0'),
    )

    ob_sys_intl_id = Column(NUMERIC(6, 0, False), primary_key=True,
                            comment='Unique number for each record')
    ob_sys_vrsn_id = Column(NUMERIC(6, 0, False), nullable=False, index=True,
                            comment='Unique number for observing system version')
    src_id = Column(ForeignKey('source.src_id'), nullable=False, index=True,
                    comment='Unique number for station')
    ob_sys_intl_bgn_date = Column(DateTime, nullable=False,
                                  comment='Start date of installation of observing sys at station')
    ob_sys_intl_end_date = Column(DateTime, nullable=False,
                                  comment='End date of installation of observing sys at station')

    src = relationship('Source')


class SrcCapability(Base):
    __tablename__ = 'src_capability'
    __table_args__ = (
        CheckConstraint('FIRST_ONLINE_OB_YR BETWEEN 1738 AND 3999'),
        CheckConstraint('SRC_CAP_END_DATE >= SRC_CAP_BGN_DATE'),
        CheckConstraint('SRC_CAP_END_DATE >= SRC_CAP_BGN_DATE'),
        CheckConstraint('SRC_ID >= 0'),
        CheckConstraint('data_retention_period >= 0000'),
        CheckConstraint(
            "SRC_CAP_END_DATE BETWEEN TO_DATE('01011677','DDMMYYYY') AND TO_DATE('31123999','DDMMYYYY')  "),
        CheckConstraint('REC_ST_IND >= 0001'),
        CheckConstraint(
            "SRC_CAP_BGN_DATE BETWEEN TO_DATE('16770101','YYYYMMDD') AND TO_DATE('39991231','YYYYMMDD')"),
        CheckConstraint("SUBSTR(RCPT_METHOD_NAME,1,8) = 'ID XREF '"),
        Index('c_srccap_end_date', 'id', 'id_type', 'met_domain_name',
              'src_cap_end_date', unique=True),
        {
            'comment': 'Midas.Src_Capability table defines which types of observation  (met domain) a source is capable of producing (and MIDAS will store), e.g. London/Gatwick is capable of producing synops and NCMs, while Southend is only capable of producing metars.\nSome stations, e.g. Beaufort Park, use more than one identifier of the same type, e.g. WMO number 03693 for manned observations and 03694 for SAMOS, therefore there will be two capabilities for this source.\nChanges over time are recorded using dates.  A source capability is closed when attribute Src_Cap_End_Date is set to a date that is before the current date.  If the capability is subsequently required again by the source, then the record may either be re-opened, by resetting the Src_Cap_End_Date or by creating a new record.\nA capability is not automatically created upon receipt of a new source or new meteorological domain.  A source capability can be deleted when it is open.\nRcpt_method_name is currently used to store ID cross-references, while communication_method_code is required by the MetaData project.\nMidasUpd.Src_Capability is the corresponding updatable view, with one-for-one projection of the columns.  To prevent accidental deletion of CLIMAT rows, delete privilege is not available for this view.\nMidasUpd.Delete_Src_Capability allows delete privilege on rows other than CLIMAT ones.\nMidasUpd.Clm_Src_Capability is an updatable view, restricted to CLIMAT rows.\nMidasVu.Src_Capability is a non-updatable view, with one-for-one projection of the columns.\nWhen the Src_Capability is valid, but MIDAS has no data, Rec_St_Ind = 2000.  These rows are excluded from the MidasVu views.'}
    )

    id = Column(VARCHAR(8), primary_key=True, nullable=False,
                comment='\nThe value of an identifier for the source.  Eight left-justified identifier characters, eg 03772, EGGW , etc.  This ID has no meaning unless interpreted with the associated identifier type.\nIdentifier has a length of eight characters to allow for ship call-signs and to achieve alignment.  The WMO definition of symbolic letter D....D is Ships call sign consisting of three or more alphanumeric characters.  B Fullagar (OPR3) confirms that the maximum length of a WMO call-sign is seven characters.  The GreenPeace ship uses an eight character call-sign, but OPR truncate this to seven characters.\nSome identifiers have been re-used, e.g. when a WMO station number is re-allocated at a later date for a site that is deemed suitable for synoptic purposes.  Where this has happened already the oldest use will have the character Z appended to the identifier, the next oldest Y, etc, with the over-riding proviso that the newest version will NOT have an appendage.\n')
    id_type = Column(VARCHAR(4), primary_key=True, nullable=False,
                     comment='\nThe name of the type of identifier used to identify a source,  e.g. WMO, SHIP, OWS, RAIN, DCNN etc.  See BUFR table B, class 02, 002001.\n')
    met_domain_name = Column(VARCHAR(8), primary_key=True, nullable=False,
                             comment='\nA met domain is uniquely identified by its name.\nThe names of input domains correspond to existing code forms, but are structured to facilitate sorting, e.g. SYNOP FM12, SHIP FM13, DRIFTER FM18-IX, CLIMAT UA FM75-VI, etc.\nNB: Synop is not a unique name for an input met domain; the domain name must include a FM session number or date.    Synop pre 1982 is not a unique name, the name may have changed on several previous occasions.\nOP3 marine QC have specifically asked for a met domain of Ship synop - GTS, or similar, so that they can distinguish GTS ships from VOF ones.  The names of storage domains will correspond to MIDAS table names.\n')
    src_cap_bgn_date = Column(DateTime, primary_key=True, nullable=False,
                              comment='\nsrc_capability.src_bgn_date is the first date for which we have observations of the id_ type / met_domain_name combination.\n')
    src_id = Column(ForeignKey('source.src_id'), nullable=False,
                    comment='\nThis is an identifier for each source of meterological data within the system. It acts as a unique identifier when a source may be of various types.  It consists of a 6 digit integer, assigned from a high-number record, and has no external significance.\n')
    rec_st_ind = Column(NUMERIC(4, 0, False), nullable=False)
    prime_capability_flag = Column(
        Enum('T', 'F', name="prime_capability_flag_enum"), nullable=False,
        server_default=text("'F'"),
        comment='Single character to indicate if the capability is the prime one of its type for the specified station, i.e. the prime daily rainfall capability for the station.  Valid values are T and F.  For each met_domain, one and only one capability can be set to prime at one time.  When SAMOS or similar equipment is trialed at a site, the site may continue to report using its current ID and prime_capability_flag = T while the SAMOS uses a new src_capability and ID with prime_capability_flag = F.  When the trial concludes and the SAMOS becomes operational, the old capability is changed to prime_capability_flag = F (and is usually closed), while the new src_capability (and ID) is updated to prime_capability_flag = T.')
    src_cap_end_date = Column(DateTime,
                              comment='\nsrc_capability.src_end_date is the last date for which we have observations of the id_ type / met_domain_name combination.\n')
    first_online_ob_yr = Column(NUMERIC(4, 0, False))
    db_segment_name = Column(VARCHAR(12),
                             comment='\nThe name of a database segment, e.g. source, raindrnl, etc.\n')
    rcpt_method_name = Column(VARCHAR(20),
                              comment='\nFormerly the method of receiving these reports from this source, e.g. GTS, metform, postcard, etc.  This attribute is now used to cross-reference between IDs in use at a SOURCE.  It will be renamed to ID_CROSS_REF at the next convenient opportunity.\n ')
    data_retention_period = Column(NUMERIC(3, 0, False),
                                   comment='\nCharacter string indicating the period for which data are retained in MIDAS.\n')
    comm_mthd_id = Column(NUMERIC(6, 0, False),
                          comment='\nAbbreviated code to identify the various communication methods on which data can be sent back to the Office.\n')

    src = relationship('Source')


class SrcCapabilityNodatum(Base):
    __tablename__ = 'src_capability_nodata'
    __table_args__ = (
        CheckConstraint("SUBSTR(rcpt_method_name,1,8) = 'ID XREF '"),
        CheckConstraint('data_retention_period >= 0000'),
        CheckConstraint('first_online_ob_yr BETWEEN 1738 AND 3999'),
        CheckConstraint('rec_st_ind >= 0001'),
        CheckConstraint(
            "src_cap_bgn_date BETWEEN TO_DATE('16770101','YYYYMMDD') AND TO_DATE('39991231','YYYYMMDD')"),
        CheckConstraint('src_cap_end_date >= src_cap_bgn_date'),
        CheckConstraint('src_cap_end_date >= src_cap_bgn_date'),
        CheckConstraint(
            "src_cap_end_date BETWEEN TO_DATE('01011677','DDMMYYYY') AND TO_DATE('31123999','DDMMYYYY')"),
        Index('c_scnd_unq', 'id', 'id_type', 'met_domain_name',
              'src_cap_end_date', unique=True)
    )

    id = Column(VARCHAR(8), primary_key=True, nullable=False)
    id_type = Column(VARCHAR(4), primary_key=True, nullable=False)
    met_domain_name = Column(VARCHAR(8), primary_key=True, nullable=False)
    src_cap_bgn_date = Column(DateTime, primary_key=True, nullable=False)
    src_id = Column(ForeignKey('source.src_id'), nullable=False)
    rec_st_ind = Column(NUMERIC(4, 0, False), nullable=False)
    prime_capability_flag = Column(Enum('T', 'F', name="prime_capability_flag"),
                                   nullable=False)
    src_cap_end_date = Column(DateTime)
    first_online_ob_yr = Column(NUMERIC(4, 0, False))
    db_segment_name = Column(VARCHAR(12))
    rcpt_method_name = Column(VARCHAR(20))
    data_retention_period = Column(NUMERIC(3, 0, False))
    comm_mthd_id = Column(NUMERIC(6, 0, False))

    src = relationship('Source')


class StationAuthorityHistory(Base):
    __tablename__ = 'station_authority_history'
    __table_args__ = (
        CheckConstraint('SRC_ID >= 0'),
    )

    authority_id = Column(NUMERIC(6, 0, False), primary_key=True,
                          nullable=False,
                          comment='Foreign key to attribute in the AUTHORITY table')
    src_id = Column(ForeignKey('source.src_id'), primary_key=True,
                    nullable=False,
                    comment='Foreign key to attribute in the SOURCE table')
    stn_auth_bgn_date = Column(DateTime, primary_key=True, nullable=False,
                               comment='Start date of relationship between station and authority')
    stn_auth_end_date = Column(DateTime, nullable=False,
                               comment='End date of relationship between station and authority')
    auth_hist_rmrk = Column(VARCHAR(200), comment='Remark on relationship')

    src = relationship('Source')


class StationGeography(Base):
    __tablename__ = 'station_geography'
    __table_args__ = (
        CheckConstraint('PRC_MAN_WTHN_10M BETWEEN 0 AND 100'),
        CheckConstraint('PRC_MAN_WTHN_50M BETWEEN 0 AND 100'),
        CheckConstraint('PRC_VEG_WTHN_10M BETWEEN 0 AND 100'),
        CheckConstraint('PRC_VEG_WTHN_50M BETWEEN 0 AND 100'),
        CheckConstraint('SRC_ID >= 0'),
        CheckConstraint('prc_heat_src_wthn_100m between 0 and 100'),
        CheckConstraint('prc_heat_src_wthn_30m between 0 and 100'),
        CheckConstraint('prc_veg_wthn_100m between 0 and 100'),
        CheckConstraint('prc_veg_wthn_30m between 0 and 100'),
        {
            'comment': 'Table providing details of the geography associated with a station.'}
    )

    src_id = Column(ForeignKey('source.src_id'), primary_key=True,
                    nullable=False, comment='Unique identifier of station')
    geog_upd_date = Column(DateTime, primary_key=True, nullable=False,
                           comment='Date on which record was updated')
    pr_geog_type_code = Column(VARCHAR(8), nullable=False,
                               comment='Primary geography type at station')
    scdy_geog_type_code = Column(VARCHAR(8),
                                 comment='Secondary geography type at station')
    site_type_code = Column(VARCHAR(20), nullable=False,
                            comment='Unique code of site type')
    land_use_type_id = Column(NUMERIC(2, 0, False), nullable=False,
                              comment='Unique identifier of land use')
    grnd_slpe_dsc = Column(VARCHAR(20),
                           comment='Description of ground slope (Level, Simple Complex)')
    grnd_slpe_up_dir = Column(NUMERIC(3, 0, False),
                              comment='Upward direction of ground slope (0-360)')
    gradient = Column(NUMERIC(3, 0, False),
                      comment='Gradient of ground slope (0-90)')
    prc_man_wthn_10m = Column(NUMERIC(3, 0, False),
                              comment='Percentage manmade ground cover within 10m radius')
    prc_veg_wthn_10m = Column(NUMERIC(3, 0, False),
                              comment='Percentage vegetation ground cover greater than 0.3m height within 10m radius')
    prc_man_wthn_50m = Column(NUMERIC(3, 0, False),
                              comment='Percentage manmade ground cover within 50m radius')
    prc_veg_wthn_50m = Column(NUMERIC(3, 0, False),
                              comment='Percentage vegetation ground cover greater than 0.3m height within 50m radius')
    soil_type_id = Column(NUMERIC(3, 0, False),
                          comment='Unique identifier of soil type at station')
    prc_heat_src_wthn_30m = Column(NUMERIC(3, 0, False),
                                   comment='Percentage of area occupied by sources of heat within 30m radius')
    prc_veg_wthn_30m = Column(NUMERIC(3, 0, False),
                              comment='Percentage vegetation ground cover greater than 0.3m height within 30m radius')
    prc_heat_src_wthn_100m = Column(NUMERIC(3, 0, False),
                                    comment='Percentage of area occupied by sources of heat within 100m radius')
    prc_veg_wthn_100m = Column(NUMERIC(3, 0, False),
                               comment='Percentage vegetation ground cover greater than 0.3m height within 100m radius')
    sfc_cover_class_scheme = Column(VARCHAR(20),
                                    comment='The surface cover classification scheme used to define the surface cover')
    sfc_cover_less_than_100m = Column(VARCHAR(20),
                                      comment='The type of surface over a radius of the station of less then 100m')
    sfc_cover_100m_3km = Column(VARCHAR(20),
                                comment='The type of surface over a radius of the station between 100m and 3km')
    sfc_cover_3km_100km = Column(VARCHAR(20),
                                 comment='The type of surface over a radius of the station between 100m and 3km')

    src = relationship('Source')


class StationHistory(Base):
    __tablename__ = 'station_history'
    __table_args__ = (
        CheckConstraint('SRC_ID >= 0'),
    )

    src_id = Column(ForeignKey('source.src_id'), primary_key=True,
                    nullable=False, comment='Unique identifier of station')
    event_date = Column(DateTime, primary_key=True, nullable=False,
                        comment='Date of event')
    event_text = Column(VARCHAR(150), nullable=False,
                        comment='Textual description of event')
    event_result_text = Column(VARCHAR(150), nullable=False,
                               comment='Any result of the event')

    src = relationship('Source')


class StationInventoryStatu(Base):
    __tablename__ = 'station_inventory_status'
    __table_args__ = (
        CheckConstraint('SRC_ID >= 0'),
    )

    src_id = Column(ForeignKey('source.src_id'), primary_key=True,
                    nullable=False, index=True,
                    comment='Unique identifier of station')
    inventory_code = Column(CHAR(1), primary_key=True, nullable=False,
                            index=True,
                            comment='Unique code for inventory status')
    invt_sts_bgn_date = Column(DateTime, primary_key=True, nullable=False,
                               comment='Date at which this status starts for this station')
    invt_sts_end_date = Column(DateTime, nullable=False,
                               comment='Date at which this status ends for this station')
    invt_sts_rmrk = Column(VARCHAR(200),
                           comment='Any remarks applicable to this record')

    src = relationship('Source')


class StationObserver(Base):
    __tablename__ = 'station_observer'
    __table_args__ = (
        CheckConstraint('SRC_ID >= 0'),
    )

    observer_id = Column(NUMERIC(6, 0, False), primary_key=True, nullable=False,
                         index=True, comment='Unique identifier of observer')
    src_id = Column(ForeignKey('source.src_id'), primary_key=True,
                    nullable=False, index=True,
                    comment='Unique identifier of station')
    stn_obsr_bgn_date = Column(DateTime, primary_key=True, nullable=False,
                               comment='Date at which observer started at station')
    stn_obsr_end_date = Column(DateTime, nullable=False,
                               comment='Date at which observer ended at station')
    observer_role_code = Column(CHAR(4), nullable=False, index=True,
                                comment='Code describing the role of the observer at the station')

    src = relationship('Source')


class StationRole(Base):
    __tablename__ = 'station_role'
    __table_args__ = (
        CheckConstraint('SRC_ID >= 0'),
    )

    src_id = Column(ForeignKey('source.src_id'), primary_key=True,
                    nullable=False, comment='Unique identifier of the station')
    role_name_code = Column(VARCHAR(11), primary_key=True, nullable=False,
                            comment='Unique code for the particular role ')
    role_bgn_date = Column(DateTime, primary_key=True, nullable=False,
                           comment='Date on which station is first associated with role')
    role_end_date = Column(DateTime, nullable=False,
                           comment='Date on which station is last associated with role')

    src = relationship('Source')


class StationStatu(Base):
    __tablename__ = 'station_status'
    __table_args__ = (
        CheckConstraint('SRC_ID >= 0'),
    )

    status_code = Column(CHAR(4), primary_key=True, nullable=False, index=True,
                         comment='Unique code for status')
    src_id = Column(ForeignKey('source.src_id'), primary_key=True,
                    nullable=False, index=True,
                    comment='Unique identifier for station')
    status_bgn_date = Column(DateTime, primary_key=True, nullable=False,
                             comment='Begin date for status record')
    status_end_date = Column(DateTime, nullable=False,
                             comment='End date for status record')
    role_name_code = Column(VARCHAR(8), index=True,
                            comment='Role name associated with status record')

    src = relationship('Source')


class DeploymentDetail(Base):
    __tablename__ = 'deployment_detail'
    __table_args__ = {
        'comment': 'The details of attributes associated with deployments of equipment. related to the deplyment and the deployment attribute tables.'}

    depl_attr_id = Column(NUMERIC(6, 0, False), primary_key=True,
                          nullable=False, index=True,
                          comment='Deployment attribute unique identifier')
    deployment_id = Column(ForeignKey('deployment.deployment_id'),
                           primary_key=True, nullable=False, index=True,
                           comment='Deployment record unique identifier')
    depl_attr_bgn_date = Column(DateTime, primary_key=True, nullable=False,
                                comment='Begin date for which attribute value is valid')
    depl_dtl_val = Column(NUMERIC(4, 0, False), nullable=False,
                          comment='Value associated with attribute')
    depl_attr_end_date = Column(DateTime, nullable=False,
                                comment='End date for which attribute value is valid')

    deployment = relationship('Deployment')


class EqptCalibCoeff(Base):
    __tablename__ = 'eqpt_calib_coeff'

    calib_coeff_msrt_id = Column(NUMERIC(6, 0, False), primary_key=True)
    eqpt_type_calib_coeff_id = Column(NUMERIC(6, 0, False), nullable=False)
    eqpt_calib_id = Column(ForeignKey('equipment_calibration.eqpt_calib_id'),
                           nullable=False)
    calib_coeff_val = Column(NUMERIC(10, 2, True))

    eqpt_calib = relationship('EquipmentCalibration')


class InspectionDetail(Base):
    __tablename__ = 'inspection_detail'
    __table_args__ = {
        'comment': 'Related to the inspection table and provides the inspection details (the results) of the inspections carried out.'}

    insp_detl_id = Column(NUMERIC(8, 0, False), primary_key=True,
                          comment='Unique identifier of record')
    inspection_item_id = Column(NUMERIC(5, 0, False), nullable=False,
                                comment='Unique identifier of inspection item')
    insp_detl_rslt_txt = Column(VARCHAR(1000), nullable=False,
                                comment='Result of the inspection item for this inspection')
    deployment_id = Column(ForeignKey('deployment.deployment_id'),
                           comment='Deployment which this item refers to')
    inspection_id = Column(ForeignKey('inspection.inspection_id'),
                           nullable=False,
                           comment='Equipment which this item refers to')

    deployment = relationship('Deployment')
    inspection = relationship('Inspection')
