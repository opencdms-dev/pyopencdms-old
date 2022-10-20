# coding: utf-8
from sqlalchemy import (
    BigInteger,
    CHAR,
    Column,
    DECIMAL,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.mysql import TINYINT, DOUBLE, BIGINT, INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


TARGET_TABLES = [
    "acquisitiontype",
    "data_forms",
    "flags",
    "obselement",
    "paperarchivedefinition",
    "qcstatusdefinition",
    "qctype",
    "regkeys",
    "station",
    "synopfeature",
    "featuregeographicalposition",
    "instrument",
    "observationfinal",
    "observationinitial",
    "obsscheduleclass",
    "paperarchive",
    "physicalfeatureclass",
    "stationlocationhistory",
    "stationqualifier",
    "instrumentfaultreport",
    "instrumentinspection",
    "observationschedule",
    "physicalfeature",
    "stationelement",
    "faultresolution",
    "climsoftusers",
    "form_agro1",
    "form_daily2",
    "form_hourly",
    "form_hourlywind",
    "form_hourly_time_selection",
    "form_monthly",
    "form_synoptic2_tdcf",
    "form_synoptic_2_ra1",
]


class ClimsoftUser(Base):
    __tablename__ = "climsoftusers"

    userName = Column(
        String(50), primary_key=True, unique=True, nullable=False
    )
    userRole = Column(String(50), nullable=False)


class Acquisitiontype(Base):
    __tablename__ = "acquisitiontype"

    code = Column(Integer, primary_key=True, server_default=text("'0'"))
    description = Column(String(255))


class DataForm(Base):
    __tablename__ = "data_forms"

    id = Column(BigInteger, nullable=False, server_default=text("'0'"))
    order_num = Column(BigInteger, server_default=text("'0'"))
    table_name = Column(String(255))
    form_name = Column(String(250), primary_key=True)
    description = Column(Text)
    selected = Column(TINYINT)
    val_start_position = Column(BigInteger, server_default=text("'0'"))
    val_end_position = Column(BigInteger, server_default=text("'0'"))
    elem_code_location = Column(String(255))
    sequencer = Column(String(50))
    entry_mode = Column(
        TINYINT(2), nullable=False, server_default=text("'00'")
    )


class Flag(Base):
    __tablename__ = "flags"

    characterSymbol = Column(
        String(255), primary_key=True, server_default=text("''")
    )
    numSymbol = Column(Integer)
    description = Column(String(255))


class Obselement(Base):
    __tablename__ = "obselement"
    __table_args__ = (Index("elementCode", "elementId"),)

    elementId = Column(
        BigInteger, primary_key=True, server_default=text("'0'")
    )
    abbreviation = Column(String(255))
    elementName = Column(String(255))
    description = Column(String(255))
    elementScale = Column(DECIMAL(8, 2))
    upperLimit = Column(String(255))
    lowerLimit = Column(String(255))
    units = Column(String(255))
    elementtype = Column(String(50))
    qcTotalRequired = Column(Integer, server_default=text("'0'"))
    selected = Column(TINYINT, nullable=False, server_default=text("'0'"))


class Paperarchivedefinition(Base):
    __tablename__ = "paperarchivedefinition"
    __table_args__ = (Index("paperarchivedef", "formId"),)

    formId = Column(String(50), primary_key=True)
    description = Column(String(255))


class Qcstatusdefinition(Base):
    __tablename__ = "qcstatusdefinition"

    code = Column(Integer, primary_key=True, server_default=text("'0'"))
    description = Column(String(255))


class Qctype(Base):
    __tablename__ = "qctype"

    code = Column(Integer, primary_key=True, server_default=text("'0'"))
    description = Column(String(255))


class Regkey(Base):
    __tablename__ = "regkeys"

    keyName = Column(String(255), primary_key=True, server_default=text("''"))
    keyValue = Column(String(255))
    keyDescription = Column(String(255))


class Station(Base):
    __tablename__ = "station"
    __table_args__ = (Index("StationStationId", "stationId"),)

    stationId = Column(String(255), primary_key=True)
    stationName = Column(String(255))
    wmoid = Column(String(20))
    icaoid = Column(String(20))
    latitude = Column(DOUBLE(precision=11, scale=6, asdecimal=True))
    qualifier = Column(String(20))
    longitude = Column(DOUBLE(precision=11, scale=6, asdecimal=True))
    elevation = Column(String(255))
    geoLocationMethod = Column(String(255))
    geoLocationAccuracy = Column(Float(11))
    openingDatetime = Column(String(50))
    closingDatetime = Column(String(50))
    country = Column(String(50))
    authority = Column(String(255))
    adminRegion = Column(String(255))
    drainageBasin = Column(String(255))
    wacaSelection = Column(TINYINT, server_default=text("'0'"))
    cptSelection = Column(TINYINT, server_default=text("'0'"))
    stationOperational = Column(TINYINT, server_default=text("'0'"))


class Synopfeature(Base):
    __tablename__ = "synopfeature"

    abbreviation = Column(String(255), primary_key=True)
    description = Column(String(255))


class Featuregeographicalposition(Base):
    __tablename__ = "featuregeographicalposition"
    __table_args__ = (
        Index(
            "FK_mysql_climsoft_db_v4_synopfeatureFeatureGeographicalPosition",
            "belongsTo",
            "observedOn",
            unique=True,
        ),
    )

    belongsTo = Column(
        ForeignKey("synopfeature.abbreviation"),
        primary_key=True,
        nullable=False,
    )
    observedOn = Column(String(50), primary_key=True, nullable=False)
    latitude = Column(DOUBLE(precision=11, scale=6, asdecimal=True))
    longitude = Column(DOUBLE(precision=11, scale=6, asdecimal=True))

    synopfeature = relationship("Synopfeature")


class Instrument(Base):
    __tablename__ = "instrument"
    __table_args__ = (Index("code", "instrumentId"),)

    instrumentName = Column(String(255))
    instrumentId = Column(String(255), primary_key=True)
    serialNumber = Column(String(255))
    abbreviation = Column(String(255))
    model = Column(String(255))
    manufacturer = Column(String(255))
    instrumentUncertainty = Column(Float(11))
    installationDatetime = Column(String(50))
    deinstallationDatetime = Column(String(50))
    height = Column(String(255))
    instrumentPicture = Column(CHAR(255))
    installedAt = Column(ForeignKey("station.stationId"))

    station = relationship("Station")


class Observationfinal(Base):
    __tablename__ = "observationfinal"
    __table_args__ = (
        Index(
            "obsFinalIdentification",
            "recordedFrom",
            "describedBy",
            "obsDatetime",
            unique=True,
        ),
        Index("obsElementObservationInitial", "describedBy"),
        Index("stationObservationInitial", "recordedFrom"),
    )

    recordedFrom = Column(
        ForeignKey("station.stationId"), primary_key=True, nullable=False
    )
    describedBy = Column(
        ForeignKey("obselement.elementId"), primary_key=True, nullable=False
    )
    obsDatetime = Column(DateTime, primary_key=True, nullable=False)
    obsLevel = Column(
        String(255),
        primary_key=True,
        nullable=False,
        server_default=text("'surface'"),
    )
    obsValue = Column(DECIMAL(8, 2))
    flag = Column(String(255), server_default=text("'N'"))
    period = Column(Integer)
    qcStatus = Column(Integer, server_default=text("'0'"))
    qcTypeLog = Column(Text)
    acquisitionType = Column(Integer, server_default=text("'0'"))
    dataForm = Column(String(255))
    capturedBy = Column(String(255))
    mark = Column(TINYINT)
    temperatureUnits = Column(String(255))
    precipitationUnits = Column(String(255))
    cloudHeightUnits = Column(String(255))
    visUnits = Column(String(255))
    dataSourceTimeZone = Column(Integer, server_default=text("'0'"))

    obselement = relationship("Obselement")
    station = relationship("Station")


class Observationinitial(Base):
    __tablename__ = "observationinitial"
    __table_args__ = (
        Index(
            "obsInitialIdentification",
            "recordedFrom",
            "describedBy",
            "obsDatetime",
            "qcStatus",
            "acquisitionType",
            unique=True,
        ),
        Index("obsElementObservationInitial", "describedBy"),
        Index("stationObservationInitial", "recordedFrom"),
    )

    recordedFrom = Column(
        ForeignKey("station.stationId"), primary_key=True, nullable=False
    )
    describedBy = Column(
        ForeignKey("obselement.elementId"), primary_key=True, nullable=False
    )
    obsDatetime = Column(DateTime, primary_key=True, nullable=False)
    obsLevel = Column(String(255), primary_key=True, nullable=False)
    obsValue = Column(String(255))
    flag = Column(String(255))
    period = Column(Integer)
    qcStatus = Column(
        Integer, primary_key=True, nullable=False, server_default=text("'0'")
    )
    qcTypeLog = Column(Text)
    acquisitionType = Column(
        Integer, primary_key=True, nullable=False, server_default=text("'0'")
    )
    dataForm = Column(String(255))
    capturedBy = Column(String(255))
    mark = Column(TINYINT)
    temperatureUnits = Column(String(255))
    precipitationUnits = Column(String(255))
    cloudHeightUnits = Column(String(255))
    visUnits = Column(String(255))
    dataSourceTimeZone = Column(Integer, server_default=text("'0'"))

    obselement = relationship("Obselement")
    station = relationship("Station")


class Obsscheduleclas(Base):
    __tablename__ = "obsscheduleclass"
    __table_args__ = (Index("scheduleClassIdeification", "scheduleClass"),)

    scheduleClass = Column(
        String(255), primary_key=True, server_default=text("''")
    )
    description = Column(String(255))
    refersTo = Column(ForeignKey("station.stationId"))

    station = relationship("Station")


class Paperarchive(Base):
    __tablename__ = "paperarchive"
    __table_args__ = (
        Index(
            "paper_archive_identification",
            "belongsTo",
            "formDatetime",
            "classifiedInto",
            unique=True,
        ),
    )

    belongsTo = Column(
        ForeignKey("station.stationId"), primary_key=True, nullable=False
    )
    formDatetime = Column(DateTime, primary_key=True, nullable=False)
    image = Column(String(255))
    classifiedInto = Column(
        ForeignKey("paperarchivedefinition.formId"),
        primary_key=True,
        nullable=False,
    )

    station = relationship("Station")
    paperarchivedefinition = relationship("Paperarchivedefinition")


class Physicalfeatureclas(Base):
    __tablename__ = "physicalfeatureclass"
    __table_args__ = (Index("stationFeatureClass", "featureClass"),)

    featureClass = Column(String(255), primary_key=True)
    description = Column(String(255))
    refersTo = Column(ForeignKey("station.stationId"))

    station = relationship("Station")


class Stationlocationhistory(Base):
    __tablename__ = "stationlocationhistory"
    __table_args__ = (
        Index("history", "belongsTo", "openingDatetime", unique=True),
    )

    belongsTo = Column(
        ForeignKey("station.stationId"), primary_key=True, nullable=False
    )
    stationType = Column(String(255))
    geoLocationMethod = Column(String(255))
    geoLocationAccuracy = Column(Float(11))
    openingDatetime = Column(String(50), primary_key=True, nullable=False)
    closingDatetime = Column(String(50))
    latitude = Column(DOUBLE(precision=11, scale=6, asdecimal=True))
    longitude = Column(DOUBLE(precision=11, scale=6, asdecimal=True))
    elevation = Column(BigInteger)
    authority = Column(String(255))
    adminRegion = Column(String(255))
    drainageBasin = Column(String(255))

    station = relationship("Station")


class Stationqualifier(Base):
    __tablename__ = "stationqualifier"
    __table_args__ = (
        Index(
            "stationid_qualifier_identification",
            "qualifier",
            "qualifierBeginDate",
            "qualifierEndDate",
            "belongsTo",
            unique=True,
        ),
        Index("stationQualifierIdentification", "belongsTo"),
    )

    qualifier = Column(String(255), primary_key=True, nullable=False)
    qualifierBeginDate = Column(String(50), primary_key=True, nullable=False)
    qualifierEndDate = Column(String(50), primary_key=True, nullable=False)
    stationTimeZone = Column(Integer, server_default=text("'0'"))
    stationNetworkType = Column(String(255))
    belongsTo = Column(
        ForeignKey("station.stationId"), primary_key=True, nullable=False
    )

    station = relationship("Station")


class Instrumentfaultreport(Base):
    __tablename__ = "instrumentfaultreport"
    __table_args__ = (
        Index(
            "instrument_report",
            "refersTo",
            "reportDatetime",
            "reportedFrom",
            unique=True,
        ),
        Index("report_id", "reportId"),
    )

    refersTo = Column(ForeignKey("instrument.instrumentId"))
    reportId = Column(BigInteger, primary_key=True)
    reportDatetime = Column(String(50))
    faultDescription = Column(String(255))
    reportedBy = Column(String(255))
    receivedDatetime = Column(String(50))
    receivedBy = Column(String(255))
    reportedFrom = Column(ForeignKey("station.stationId"))

    instrument = relationship("Instrument")
    station = relationship("Station")


class Instrumentinspection(Base):
    __tablename__ = "instrumentinspection"
    __table_args__ = (
        Index("inspection", "performedOn", "inspectionDatetime", unique=True),
    )

    performedOn = Column(
        ForeignKey("instrument.instrumentId"), primary_key=True, nullable=False
    )
    inspectionDatetime = Column(String(50), primary_key=True, nullable=False)
    performedBy = Column(String(255))
    status = Column(String(255))
    remarks = Column(String(255))
    performedAt = Column(ForeignKey("station.stationId"))

    station = relationship("Station")
    instrument = relationship("Instrument")


class Observationschedule(Base):
    __tablename__ = "observationschedule"
    __table_args__ = (
        Index(
            "scheduleIdentification",
            "classifiedInto",
            "startTime",
            "endTime",
            unique=True,
        ),
    )

    classifiedInto = Column(
        ForeignKey("obsscheduleclass.scheduleClass"),
        primary_key=True,
        nullable=False,
    )
    startTime = Column(String(50), primary_key=True, nullable=False)
    endTime = Column(String(50), primary_key=True, nullable=False)
    interval = Column(String(255))
    additionalObsTime = Column(String(255))

    obsscheduleclas = relationship("Obsscheduleclas")


class Physicalfeature(Base):
    __tablename__ = "physicalfeature"
    __table_args__ = (
        Index(
            "featureIdentification",
            "associatedWith",
            "beginDate",
            "classifiedInto",
            "description",
            unique=True,
        ),
        Index("physicalFeatureidentification_idx", "classifiedInto"),
        Index("stationfeature", "associatedWith"),
    )

    associatedWith = Column(
        ForeignKey("station.stationId"), primary_key=True, nullable=False
    )
    beginDate = Column(String(50), primary_key=True, nullable=False)
    endDate = Column(String(50))
    image = Column(String(255))
    description = Column(String(255), primary_key=True, nullable=False)
    classifiedInto = Column(
        ForeignKey("physicalfeatureclass.featureClass"),
        primary_key=True,
        nullable=False,
    )

    station = relationship("Station")
    physicalfeatureclas = relationship("Physicalfeatureclas")


class Stationelement(Base):
    __tablename__ = "stationelement"
    __table_args__ = (
        Index(
            "stationElementIdentification",
            "recordedFrom",
            "describedBy",
            "recordedWith",
            "beginDate",
            unique=True,
        ),
        Index("obsElementobservationInitial", "describedBy"),
        Index("stationobservationInitial", "recordedFrom"),
    )

    recordedFrom = Column(
        ForeignKey("station.stationId"), primary_key=True, nullable=False
    )
    describedBy = Column(
        ForeignKey("obselement.elementId"), primary_key=True, nullable=False
    )
    recordedWith = Column(
        ForeignKey("instrument.instrumentId"), primary_key=True, nullable=False
    )
    instrumentcode = Column(String(6))
    scheduledFor = Column(ForeignKey("obsscheduleclass.scheduleClass"))
    height = Column(Float(6))
    beginDate = Column(String(50), primary_key=True, nullable=False)
    endDate = Column(String(50))

    obselement = relationship("Obselement")
    station = relationship("Station")
    instrument = relationship("Instrument")
    obsscheduleclas = relationship("Obsscheduleclas")


class Faultresolution(Base):
    __tablename__ = "faultresolution"
    __table_args__ = (
        Index("solution", "resolvedDatetime", "associatedWith", unique=True),
    )

    resolvedDatetime = Column(String(50), primary_key=True, nullable=False)
    resolvedBy = Column(String(255))
    associatedWith = Column(
        ForeignKey("instrumentfaultreport.reportId"),
        primary_key=True,
        nullable=False,
    )
    remarks = Column(String(255))

    instrumentfaultreport = relationship("Instrumentfaultreport")


class FormAgro1(Base):
    __tablename__ = "form_agro1"

    stationId = Column(
        String(50), primary_key=True, nullable=False, server_default=text("''")
    )
    yyyy = Column(INTEGER(11), primary_key=True, nullable=False)
    mm = Column(INTEGER(11), primary_key=True, nullable=False)
    dd = Column(INTEGER(11), primary_key=True, nullable=False)
    Val_Elem101 = Column(String(6))
    Val_Elem102 = Column(String(6))
    Val_Elem103 = Column(String(6))
    Val_Elem105 = Column(String(6))
    Val_Elem002 = Column(String(6))
    Val_Elem003 = Column(String(6))
    Val_Elem099 = Column(String(6))
    Val_Elem072 = Column(String(6))
    Val_Elem073 = Column(String(6))
    Val_Elem074 = Column(String(6))
    Val_Elem554 = Column(String(6))
    Val_Elem075 = Column(String(6))
    Val_Elem076 = Column(String(6))
    Val_Elem561 = Column(String(6))
    Val_Elem562 = Column(String(6))
    Val_Elem563 = Column(String(6))
    Val_Elem513 = Column(String(6))
    Val_Elem005 = Column(String(6))
    Val_Elem504 = Column(String(6))
    Val_Elem532 = Column(String(6))
    Val_Elem137 = Column(String(6))
    Val_Elem018 = Column(String(6))
    Val_Elem518 = Column(String(6))
    Val_Elem511 = Column(String(6))
    Val_Elem512 = Column(String(6))
    Val_Elem503 = Column(String(6))
    Val_Elem515 = Column(String(6))
    Val_Elem564 = Column(String(6))
    Val_Elem565 = Column(String(6))
    Val_Elem566 = Column(String(6))
    Val_Elem531 = Column(String(6))
    Val_Elem530 = Column(String(6))
    Val_Elem541 = Column(String(6))
    Val_Elem542 = Column(String(6))
    Flag101 = Column(String(1))
    Flag102 = Column(String(1))
    Flag103 = Column(String(1))
    Flag105 = Column(String(1))
    Flag002 = Column(String(1))
    Flag003 = Column(String(1))
    Flag099 = Column(String(1))
    Flag072 = Column(String(1))
    Flag073 = Column(String(1))
    Flag074 = Column(String(1))
    Flag554 = Column(String(1))
    Flag075 = Column(String(1))
    Flag076 = Column(String(1))
    Flag561 = Column(String(1))
    Flag562 = Column(String(1))
    Flag563 = Column(String(1))
    Flag513 = Column(String(1))
    Flag005 = Column(String(1))
    Flag504 = Column(String(1))
    Flag532 = Column(String(1))
    Flag137 = Column(String(1))
    Flag018 = Column(String(1))
    Flag518 = Column(String(1))
    Flag511 = Column(String(1))
    Flag512 = Column(String(1))
    Flag503 = Column(String(1))
    Flag515 = Column(String(1))
    Flag564 = Column(String(1))
    Flag565 = Column(String(1))
    Flag566 = Column(String(1))
    Flag531 = Column(String(1))
    Flag530 = Column(String(1))
    Flag541 = Column(String(1))
    Flag542 = Column(String(1))
    signature = Column(String(45))
    entryDatetime = Column(DateTime)


class FormDaily2(Base):
    __tablename__ = "form_daily2"

    stationId = Column(String(50), primary_key=True, nullable=False)
    elementId = Column(INTEGER(11), primary_key=True, nullable=False)
    yyyy = Column(INTEGER(11), primary_key=True, nullable=False)
    mm = Column(INTEGER(11), primary_key=True, nullable=False)
    hh = Column(INTEGER(11), primary_key=True, nullable=False)
    day01 = Column(String(45))
    day02 = Column(String(45))
    day03 = Column(String(45))
    day04 = Column(String(45))
    day05 = Column(String(45))
    day06 = Column(String(45))
    day07 = Column(String(45))
    day08 = Column(String(45))
    day09 = Column(String(45))
    day10 = Column(String(45))
    day11 = Column(String(45))
    day12 = Column(String(45))
    day13 = Column(String(45))
    day14 = Column(String(45))
    day15 = Column(String(45))
    day16 = Column(String(45))
    day17 = Column(String(45))
    day18 = Column(String(45))
    day19 = Column(String(45))
    day20 = Column(String(45))
    day21 = Column(String(45))
    day22 = Column(String(45))
    day23 = Column(String(45))
    day24 = Column(String(45))
    day25 = Column(String(45))
    day26 = Column(String(45))
    day27 = Column(String(45))
    day28 = Column(String(45))
    day29 = Column(String(45))
    day30 = Column(String(45))
    day31 = Column(String(45))
    flag01 = Column(String(1))
    flag02 = Column(String(1))
    flag03 = Column(String(1))
    flag04 = Column(String(1))
    flag05 = Column(String(1))
    flag06 = Column(String(1))
    flag07 = Column(String(1))
    flag08 = Column(String(1))
    flag09 = Column(String(1))
    flag10 = Column(String(1))
    flag11 = Column(String(1))
    flag12 = Column(String(1))
    flag13 = Column(String(1))
    flag14 = Column(String(1))
    flag15 = Column(String(1))
    flag16 = Column(String(1))
    flag17 = Column(String(1))
    flag18 = Column(String(1))
    flag19 = Column(String(1))
    flag20 = Column(String(1))
    flag21 = Column(String(1))
    flag22 = Column(String(1))
    flag23 = Column(String(1))
    flag24 = Column(String(1))
    flag25 = Column(String(1))
    flag26 = Column(String(1))
    flag27 = Column(String(1))
    flag28 = Column(String(1))
    flag29 = Column(String(1))
    flag30 = Column(String(1))
    flag31 = Column(String(1))
    period01 = Column(String(45))
    period02 = Column(String(45))
    period03 = Column(String(45))
    period04 = Column(String(45))
    period05 = Column(String(45))
    period06 = Column(String(45))
    period07 = Column(String(45))
    period08 = Column(String(45))
    period09 = Column(String(45))
    period10 = Column(String(45))
    period11 = Column(String(45))
    period12 = Column(String(45))
    period13 = Column(String(45))
    period14 = Column(String(45))
    period15 = Column(String(45))
    period16 = Column(String(45))
    period17 = Column(String(45))
    period18 = Column(String(45))
    period19 = Column(String(45))
    period20 = Column(String(45))
    period21 = Column(String(45))
    period22 = Column(String(45))
    period23 = Column(String(45))
    period24 = Column(String(45))
    period25 = Column(String(45))
    period26 = Column(String(45))
    period27 = Column(String(45))
    period28 = Column(String(45))
    period29 = Column(String(45))
    period30 = Column(String(45))
    period31 = Column(String(45))
    total = Column(String(45))
    signature = Column(String(45))
    entryDatetime = Column(DateTime)
    temperatureUnits = Column(String(45))
    precipUnits = Column(String(45))
    cloudHeightUnits = Column(String(45))
    visUnits = Column(String(45))


class FormHourly(Base):
    __tablename__ = "form_hourly"

    stationId = Column(String(50), primary_key=True, nullable=False)
    elementId = Column(INTEGER(11), primary_key=True, nullable=False)
    yyyy = Column(INTEGER(11), primary_key=True, nullable=False)
    mm = Column(INTEGER(11), primary_key=True, nullable=False)
    dd = Column(INTEGER(11), primary_key=True, nullable=False)
    hh_00 = Column(String(50))
    hh_01 = Column(String(50))
    hh_02 = Column(String(50))
    hh_03 = Column(String(50))
    hh_04 = Column(String(50))
    hh_05 = Column(String(50))
    hh_06 = Column(String(50))
    hh_07 = Column(String(50))
    hh_08 = Column(String(50))
    hh_09 = Column(String(50))
    hh_10 = Column(String(50))
    hh_11 = Column(String(50))
    hh_12 = Column(String(50))
    hh_13 = Column(String(50))
    hh_14 = Column(String(50))
    hh_15 = Column(String(50))
    hh_16 = Column(String(50))
    hh_17 = Column(String(50))
    hh_18 = Column(String(50))
    hh_19 = Column(String(50))
    hh_20 = Column(String(50))
    hh_21 = Column(String(50))
    hh_22 = Column(String(50))
    hh_23 = Column(String(50))
    flag00 = Column(String(50))
    flag01 = Column(String(50))
    flag02 = Column(String(50))
    flag03 = Column(String(50))
    flag04 = Column(String(50))
    flag05 = Column(String(50))
    flag06 = Column(String(50))
    flag07 = Column(String(50))
    flag08 = Column(String(50))
    flag09 = Column(String(50))
    flag10 = Column(String(50))
    flag11 = Column(String(50))
    flag12 = Column(String(50))
    flag13 = Column(String(50))
    flag14 = Column(String(50))
    flag15 = Column(String(50))
    flag16 = Column(String(50))
    flag17 = Column(String(50))
    flag18 = Column(String(50))
    flag19 = Column(String(50))
    flag20 = Column(String(50))
    flag21 = Column(String(50))
    flag22 = Column(String(50))
    flag23 = Column(String(50))
    total = Column(String(50))
    signature = Column(String(50))
    entryDatetime = Column(DateTime)


class FormHourlyTimeSelection(Base):
    __tablename__ = "form_hourly_time_selection"

    hh = Column(INTEGER(11), primary_key=True)
    hh_selection = Column(TINYINT(4))


class FormHourlywind(Base):
    __tablename__ = "form_hourlywind"

    stationId = Column(String(255), primary_key=True, nullable=False)
    yyyy = Column(INTEGER(11), primary_key=True, nullable=False)
    mm = Column(INTEGER(11), primary_key=True, nullable=False)
    dd = Column(INTEGER(11), primary_key=True, nullable=False)
    elem_112_00 = Column(String(255))
    elem_112_01 = Column(String(255))
    elem_112_02 = Column(String(255))
    elem_112_03 = Column(String(255))
    elem_112_04 = Column(String(255))
    elem_112_05 = Column(String(255))
    elem_112_06 = Column(String(255))
    elem_112_07 = Column(String(255))
    elem_112_08 = Column(String(255))
    elem_112_09 = Column(String(255))
    elem_112_10 = Column(String(255))
    elem_112_11 = Column(String(255))
    elem_112_12 = Column(String(255))
    elem_112_13 = Column(String(255))
    elem_112_14 = Column(String(255))
    elem_112_15 = Column(String(255))
    elem_112_16 = Column(String(255))
    elem_112_17 = Column(String(255))
    elem_112_18 = Column(String(255))
    elem_112_19 = Column(String(255))
    elem_112_20 = Column(String(255))
    elem_112_21 = Column(String(255))
    elem_112_22 = Column(String(255))
    elem_112_23 = Column(String(255))
    ddflag00 = Column(String(255))
    ddflag01 = Column(String(255))
    ddflag02 = Column(String(255))
    ddflag03 = Column(String(255))
    ddflag04 = Column(String(255))
    ddflag05 = Column(String(255))
    ddflag06 = Column(String(255))
    ddflag07 = Column(String(255))
    ddflag08 = Column(String(255))
    ddflag09 = Column(String(255))
    ddflag10 = Column(String(255))
    ddflag11 = Column(String(255))
    ddflag12 = Column(String(255))
    ddflag13 = Column(String(255))
    ddflag14 = Column(String(255))
    ddflag15 = Column(String(255))
    ddflag16 = Column(String(255))
    ddflag17 = Column(String(255))
    ddflag18 = Column(String(255))
    ddflag19 = Column(String(255))
    ddflag20 = Column(String(255))
    ddflag21 = Column(String(255))
    ddflag22 = Column(String(255))
    ddflag23 = Column(String(255))
    elem_111_00 = Column(String(255))
    elem_111_01 = Column(String(255))
    elem_111_02 = Column(String(255))
    elem_111_03 = Column(String(255))
    elem_111_04 = Column(String(255))
    elem_111_05 = Column(String(255))
    elem_111_06 = Column(String(255))
    elem_111_07 = Column(String(255))
    elem_111_08 = Column(String(255))
    elem_111_09 = Column(String(255))
    elem_111_10 = Column(String(255))
    elem_111_11 = Column(String(255))
    elem_111_12 = Column(String(255))
    elem_111_13 = Column(String(255))
    elem_111_14 = Column(String(255))
    elem_111_15 = Column(String(255))
    elem_111_16 = Column(String(255))
    elem_111_17 = Column(String(255))
    elem_111_18 = Column(String(255))
    elem_111_19 = Column(String(255))
    elem_111_20 = Column(String(255))
    elem_111_21 = Column(String(255))
    elem_111_22 = Column(String(255))
    elem_111_23 = Column(String(255))
    total = Column(String(50))
    signature = Column(String(50))
    entryDatetime = Column(DateTime)


class FormMonthly(Base):
    __tablename__ = "form_monthly"

    stationId = Column(String(255), primary_key=True, nullable=False)
    elementId = Column(INTEGER(11), primary_key=True, nullable=False)
    yyyy = Column(INTEGER(11), primary_key=True, nullable=False)
    mm_01 = Column(String(255))
    mm_02 = Column(String(255))
    mm_03 = Column(String(255))
    mm_04 = Column(String(255), nullable=False)
    mm_05 = Column(String(255))
    mm_06 = Column(String(255))
    mm_07 = Column(String(255))
    mm_08 = Column(String(255))
    mm_09 = Column(String(255))
    mm_10 = Column(String(255))
    mm_11 = Column(String(255))
    mm_12 = Column(String(255))
    flag01 = Column(String(255))
    flag02 = Column(String(255))
    flag03 = Column(String(255))
    flag04 = Column(String(255))
    flag05 = Column(String(255))
    flag06 = Column(String(255))
    flag07 = Column(String(255))
    flag08 = Column(String(255))
    flag09 = Column(String(255))
    flag10 = Column(String(255))
    flag11 = Column(String(255))
    flag12 = Column(String(255))
    period01 = Column(String(255))
    period02 = Column(String(255))
    period03 = Column(String(255))
    period04 = Column(String(255))
    period05 = Column(String(255))
    period06 = Column(String(255))
    period07 = Column(String(255))
    period08 = Column(String(255))
    period09 = Column(String(255))
    period10 = Column(String(255))
    period11 = Column(String(255))
    period12 = Column(String(255))
    signature = Column(String(50))
    entryDatetime = Column(DateTime)


class FormSynoptic2Tdcf(Base):
    __tablename__ = "form_synoptic2_tdcf"
    __table_args__ = (
        Index(
            "Identification",
            "stationId",
            "yyyy",
            "mm",
            "dd",
            "hh",
            unique=True,
        ),
    )

    stationId = Column(String(10), primary_key=True, nullable=False)
    yyyy = Column(BIGINT(20), primary_key=True, nullable=False)
    mm = Column(BIGINT(20), primary_key=True, nullable=False)
    dd = Column(BIGINT(20), primary_key=True, nullable=False)
    hh = Column(String(5), primary_key=True, nullable=False)
    _106 = Column("106", String(6))
    _107 = Column("107", String(6))
    _399 = Column("399", String(5))
    _301 = Column("301", String(8))
    _185 = Column("185", String(6))
    _101 = Column("101", String(5))
    _103 = Column("103", String(5))
    _105 = Column("105", String(50))
    _110 = Column("110", String(5))
    _114 = Column("114", String(5))
    _115 = Column("115", String(5))
    _168 = Column("168", String(5))
    _192 = Column("192", String(5))
    _169 = Column("169", String(5))
    _170 = Column("170", String(5))
    _171 = Column("171", String(5))
    _119 = Column("119", String(5))
    _116 = Column("116", String(5))
    _117 = Column("117", String(5))
    _118 = Column("118", String(5))
    _123 = Column("123", String(5))
    _120 = Column("120", String(5))
    _121 = Column("121", String(5))
    _122 = Column("122", String(5))
    _127 = Column("127", String(5))
    _124 = Column("124", String(5))
    _125 = Column("125", String(5))
    _126 = Column("126", String(5))
    _131 = Column("131", String(5))
    _128 = Column("128", String(5))
    _129 = Column("129", String(5))
    _130 = Column("130", String(5))
    _167 = Column("167", String(5))
    _197 = Column("197", String(50))
    _193 = Column("193", String(5))
    _18 = Column("18", String(6))
    _532 = Column("532", String(6))
    _132 = Column("132", String(6))
    _5 = Column("5", String(6))
    _174 = Column("174", String(50))
    _3 = Column("3", String(5))
    _2 = Column("2", String(5))
    _112 = Column("112", String(5))
    _111 = Column("111", String(5))
    _85 = Column("85", String(50))
    flag1 = Column(String(1))
    flag2 = Column(String(1))
    flag3 = Column(String(1))
    flag4 = Column(String(1))
    flag5 = Column(String(1))
    flag6 = Column(String(1))
    flag7 = Column(String(1))
    flag8 = Column(String(1))
    flag9 = Column(String(1))
    flag10 = Column(String(1))
    flag11 = Column(String(1))
    flag12 = Column(String(1))
    flag13 = Column(String(1))
    flag14 = Column(String(1))
    flag15 = Column(String(1))
    flag16 = Column(String(1))
    flag17 = Column(String(1))
    flag18 = Column(String(1))
    flag19 = Column(String(1))
    flag20 = Column(String(1))
    flag21 = Column(String(1))
    flag22 = Column(String(1))
    flag23 = Column(String(1))
    flag24 = Column(String(1))
    flag25 = Column(String(1))
    flag26 = Column(String(1))
    flag27 = Column(String(1))
    flag28 = Column(String(1))
    flag29 = Column(String(1))
    flag30 = Column(String(1))
    flag31 = Column(String(1))
    flag32 = Column(String(1))
    flag33 = Column(String(1))
    flag34 = Column(String(1))
    flag35 = Column(String(1))
    flag36 = Column(String(1))
    flag37 = Column(String(1))
    flag38 = Column(String(1))
    flag39 = Column(String(1))
    flag40 = Column(String(1))
    flag41 = Column(String(1))
    flag42 = Column(String(1))
    flag43 = Column(String(1))
    flag44 = Column(String(1))
    flag45 = Column(String(1))
    signature = Column(String(50))
    entryDatetime = Column(DateTime)


class FormSynoptic2Ra1(Base):
    __tablename__ = "form_synoptic_2_ra1"

    stationId = Column(
        String(50), primary_key=True, nullable=False, server_default=text("''")
    )
    yyyy = Column(INTEGER(11), primary_key=True, nullable=False)
    mm = Column(INTEGER(11), primary_key=True, nullable=False)
    dd = Column(INTEGER(11), primary_key=True, nullable=False)
    hh = Column(INTEGER(11), primary_key=True, nullable=False)
    Val_Elem106 = Column(String(6))
    Val_Elem107 = Column(String(6))
    Val_Elem400 = Column(String(6))
    Val_Elem814 = Column(String(6))
    Val_Elem399 = Column(String(6))
    Val_Elem301 = Column(String(6))
    Val_Elem185 = Column(String(6))
    Val_Elem101 = Column(String(6))
    Val_Elem102 = Column(String(6))
    Val_Elem103 = Column(String(6))
    Val_Elem105 = Column(String(6))
    Val_Elem192 = Column(String(6))
    Val_Elem110 = Column(String(6))
    Val_Elem114 = Column(String(6))
    Val_Elem112 = Column(String(6))
    Val_Elem111 = Column(String(6))
    Val_Elem167 = Column(String(6))
    Val_Elem197 = Column(String(6))
    Val_Elem193 = Column(String(6))
    Val_Elem115 = Column(String(6))
    Val_Elem168 = Column(String(6))
    Val_Elem169 = Column(String(6))
    Val_Elem170 = Column(String(6))
    Val_Elem171 = Column(String(6))
    Val_Elem119 = Column(String(6))
    Val_Elem116 = Column(String(6))
    Val_Elem117 = Column(String(6))
    Val_Elem118 = Column(String(6))
    Val_Elem123 = Column(String(6))
    Val_Elem120 = Column(String(6))
    Val_Elem121 = Column(String(6))
    Val_Elem122 = Column(String(6))
    Val_Elem127 = Column(String(6))
    Val_Elem124 = Column(String(6))
    Val_Elem125 = Column(String(6))
    Val_Elem126 = Column(String(6))
    Val_Elem131 = Column(String(6))
    Val_Elem128 = Column(String(6))
    Val_Elem129 = Column(String(6))
    Val_Elem130 = Column(String(6))
    Val_Elem002 = Column(String(6))
    Val_Elem003 = Column(String(6))
    Val_Elem099 = Column(String(6))
    Val_Elem018 = Column(String(6))
    Val_Elem084 = Column(String(6))
    Val_Elem132 = Column(String(6))
    Val_Elem005 = Column(String(6))
    Val_Elem174 = Column(String(6))
    Val_Elem046 = Column(String(6))
    Flag106 = Column(String(1))
    Flag107 = Column(String(1))
    Flag400 = Column(String(1))
    Flag814 = Column(String(1))
    Flag399 = Column(String(1))
    Flag301 = Column(String(1))
    Flag185 = Column(String(1))
    Flag101 = Column(String(1))
    Flag102 = Column(String(1))
    Flag103 = Column(String(1))
    Flag105 = Column(String(1))
    Flag192 = Column(String(1))
    Flag110 = Column(String(1))
    Flag114 = Column(String(1))
    Flag112 = Column(String(1))
    Flag111 = Column(String(1))
    Flag167 = Column(String(1))
    Flag197 = Column(String(1))
    Flag193 = Column(String(1))
    Flag115 = Column(String(1))
    Flag168 = Column(String(1))
    Flag169 = Column(String(1))
    Flag170 = Column(String(1))
    Flag171 = Column(String(1))
    Flag119 = Column(String(1))
    Flag116 = Column(String(1))
    Flag117 = Column(String(1))
    Flag118 = Column(String(1))
    Flag123 = Column(String(1))
    Flag120 = Column(String(1))
    Flag121 = Column(String(1))
    Flag122 = Column(String(1))
    Flag127 = Column(String(1))
    Flag124 = Column(String(1))
    Flag125 = Column(String(1))
    Flag126 = Column(String(1))
    Flag131 = Column(String(1))
    Flag128 = Column(String(1))
    Flag129 = Column(String(1))
    Flag130 = Column(String(1))
    Flag002 = Column(String(1))
    Flag003 = Column(String(1))
    Flag099 = Column(String(1))
    Flag018 = Column(String(1))
    Flag084 = Column(String(1))
    Flag132 = Column(String(1))
    Flag005 = Column(String(1))
    Flag174 = Column(String(1))
    Flag046 = Column(String(1))
    signature = Column(String(45))
    entryDatetime = Column(DateTime)
