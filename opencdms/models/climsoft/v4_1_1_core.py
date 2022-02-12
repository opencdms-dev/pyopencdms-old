# coding: utf-8
from sqlalchemy import BigInteger, CHAR, Column, DECIMAL, DateTime, Float, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.dialects.mysql import TINYINT, DOUBLE
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
    "climsoftusers"
]


class ClimsoftUser(Base):
    __tablename__ = 'climsoftusers'

    userName = Column(String(50), primary_key=True, unique=True, nullable=False)
    userRole = Column(String(50), nullable=False)


class Acquisitiontype(Base):
    __tablename__ = 'acquisitiontype'

    code = Column(Integer, primary_key=True, server_default=text("'0'"))
    description = Column(String(255))


class DataForm(Base):
    __tablename__ = 'data_forms'

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
    entry_mode = Column(TINYINT(2), nullable=False, server_default=text("'00'"))


class Flag(Base):
    __tablename__ = 'flags'

    characterSymbol = Column(String(255), primary_key=True, server_default=text("''"))
    numSymbol = Column(Integer)
    description = Column(String(255))


class Obselement(Base):
    __tablename__ = 'obselement'
    __table_args__ = ( Index('elementCode', 'elementId'),)

    elementId = Column(BigInteger, primary_key=True, server_default=text("'0'"))
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
    __tablename__ = 'paperarchivedefinition'
    __table_args__ = (Index('paperarchivedef','formId'),)

    formId = Column(String(50), primary_key=True)
    description = Column(String(255))


class Qcstatusdefinition(Base):
    __tablename__ = 'qcstatusdefinition'

    code = Column(Integer, primary_key=True, server_default=text("'0'"))
    description = Column(String(255))


class Qctype(Base):
    __tablename__ = 'qctype'

    code = Column(Integer, primary_key=True, server_default=text("'0'"))
    description = Column(String(255))


class Regkey(Base):
    __tablename__ = 'regkeys'

    keyName = Column(String(255), primary_key=True, server_default=text("''"))
    keyValue = Column(String(255))
    keyDescription = Column(String(255))


class Station(Base):
    __tablename__ = 'station'
    __table_args__ = (Index('StationStationId', 'stationId'),)

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
    __tablename__ = 'synopfeature'

    abbreviation = Column(String(255), primary_key=True)
    description = Column(String(255))


class Featuregeographicalposition(Base):
    __tablename__ = 'featuregeographicalposition'
    __table_args__ = (
        Index('FK_mysql_climsoft_db_v4_synopfeatureFeatureGeographicalPosition', 'belongsTo', 'observedOn', unique=True),
    )

    belongsTo = Column(ForeignKey('synopfeature.abbreviation'), primary_key=True, nullable=False)
    observedOn = Column(String(50), primary_key=True, nullable=False)
    latitude = Column(DOUBLE(precision=11, scale=6, asdecimal=True))
    longitude = Column(DOUBLE(precision=11, scale=6, asdecimal=True))

    synopfeature = relationship('Synopfeature')


class Instrument(Base):
    __tablename__ = 'instrument'
    __table_args__ = (Index('code', 'instrumentId'),)

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
    installedAt = Column(ForeignKey('station.stationId'))

    station = relationship('Station')


class Observationfinal(Base):
    __tablename__ = 'observationfinal'
    __table_args__ = (
        Index('obsFinalIdentification', 'recordedFrom', 'describedBy', 'obsDatetime', unique=True),
        Index('obsElementObservationInitial', 'describedBy'),
        Index('stationObservationInitial', 'recordedFrom')
    )

    recordedFrom = Column(ForeignKey('station.stationId'), primary_key=True, nullable=False)
    describedBy = Column(ForeignKey('obselement.elementId'), primary_key=True, nullable=False)
    obsDatetime = Column(DateTime, primary_key=True, nullable=False)
    obsLevel = Column(String(255), primary_key=True, nullable=False, server_default=text("'surface'"))
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

    obselement = relationship('Obselement')
    station = relationship('Station')


class Observationinitial(Base):
    __tablename__ = 'observationinitial'
    __table_args__ = (
        Index('obsInitialIdentification', 'recordedFrom', 'describedBy', 'obsDatetime', 'qcStatus', 'acquisitionType', unique=True),
        Index('obsElementObservationInitial', 'describedBy'),
        Index('stationObservationInitial', 'recordedFrom')
    )

    recordedFrom = Column(ForeignKey('station.stationId'), primary_key=True, nullable=False)
    describedBy = Column(ForeignKey('obselement.elementId'), primary_key=True, nullable=False)
    obsDatetime = Column(DateTime, primary_key=True, nullable=False)
    obsLevel = Column(String(255), primary_key=True, nullable=False)
    obsValue = Column(String(255))
    flag = Column(String(255))
    period = Column(Integer)
    qcStatus = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    qcTypeLog = Column(Text)
    acquisitionType = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    dataForm = Column(String(255))
    capturedBy = Column(String(255))
    mark = Column(TINYINT)
    temperatureUnits = Column(String(255))
    precipitationUnits = Column(String(255))
    cloudHeightUnits = Column(String(255))
    visUnits = Column(String(255))
    dataSourceTimeZone = Column(Integer, server_default=text("'0'"))

    obselement = relationship('Obselement')
    station = relationship('Station')


class Obsscheduleclas(Base):
    __tablename__ = 'obsscheduleclass'
    __table_args__ = (Index('scheduleClassIdeification', 'scheduleClass'),)

    scheduleClass = Column(String(255), primary_key=True, server_default=text("''"))
    description = Column(String(255))
    refersTo = Column(ForeignKey('station.stationId'))

    station = relationship('Station')


class Paperarchive(Base):
    __tablename__ = 'paperarchive'
    __table_args__ = (
        Index('paper_archive_identification', 'belongsTo', 'formDatetime', 'classifiedInto', unique=True),
    )

    belongsTo = Column(ForeignKey('station.stationId'), primary_key=True, nullable=False)
    formDatetime = Column(DateTime, primary_key=True, nullable=False)
    image = Column(String(255))
    classifiedInto = Column(ForeignKey('paperarchivedefinition.formId'), primary_key=True, nullable=False)

    station = relationship('Station')
    paperarchivedefinition = relationship('Paperarchivedefinition')


class Physicalfeatureclas(Base):
    __tablename__ = 'physicalfeatureclass'
    __table_args__ = (Index('stationFeatureClass', 'featureClass'),)

    featureClass = Column(String(255), primary_key=True)
    description = Column(String(255))
    refersTo = Column(ForeignKey('station.stationId'))

    station = relationship('Station')


class Stationlocationhistory(Base):
    __tablename__ = 'stationlocationhistory'
    __table_args__ = (
        Index('history', 'belongsTo', 'openingDatetime', unique=True),
    )

    belongsTo = Column(ForeignKey('station.stationId'), primary_key=True, nullable=False)
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

    station = relationship('Station')


class Stationqualifier(Base):
    __tablename__ = 'stationqualifier'
    __table_args__ = (
        Index('stationid_qualifier_identification', 'qualifier', 'qualifierBeginDate', 'qualifierEndDate', 'belongsTo', unique=True),
        Index('stationQualifierIdentification', 'belongsTo')
    )

    qualifier = Column(String(255), primary_key=True, nullable=False)
    qualifierBeginDate = Column(String(50), primary_key=True, nullable=False)
    qualifierEndDate = Column(String(50), primary_key=True, nullable=False)
    stationTimeZone = Column(Integer, server_default=text("'0'"))
    stationNetworkType = Column(String(255))
    belongsTo = Column(ForeignKey('station.stationId'), primary_key=True, nullable=False)

    station = relationship('Station')


class Instrumentfaultreport(Base):
    __tablename__ = 'instrumentfaultreport'
    __table_args__ = (
        Index('instrument_report', 'refersTo', 'reportDatetime', 'reportedFrom', unique=True),
        Index('report_id', 'reportId')
    )

    refersTo = Column(ForeignKey('instrument.instrumentId'))
    reportId = Column(BigInteger, primary_key=True)
    reportDatetime = Column(String(50))
    faultDescription = Column(String(255))
    reportedBy = Column(String(255))
    receivedDatetime = Column(String(50))
    receivedBy = Column(String(255))
    reportedFrom = Column(ForeignKey('station.stationId'))

    instrument = relationship('Instrument')
    station = relationship('Station')


class Instrumentinspection(Base):
    __tablename__ = 'instrumentinspection'
    __table_args__ = (
        Index('inspection', 'performedOn', 'inspectionDatetime', unique=True),
    )

    performedOn = Column(ForeignKey('instrument.instrumentId'), primary_key=True, nullable=False)
    inspectionDatetime = Column(String(50), primary_key=True, nullable=False)
    performedBy = Column(String(255))
    status = Column(String(255))
    remarks = Column(String(255))
    performedAt = Column(ForeignKey('station.stationId'))

    station = relationship('Station')
    instrument = relationship('Instrument')


class Observationschedule(Base):
    __tablename__ = 'observationschedule'
    __table_args__ = (
        Index('scheduleIdentification', 'classifiedInto', 'startTime', 'endTime', unique=True),
    )

    classifiedInto = Column(ForeignKey('obsscheduleclass.scheduleClass'), primary_key=True, nullable=False)
    startTime = Column(String(50), primary_key=True, nullable=False)
    endTime = Column(String(50), primary_key=True, nullable=False)
    interval = Column(String(255))
    additionalObsTime = Column(String(255))

    obsscheduleclas = relationship('Obsscheduleclas')


class Physicalfeature(Base):
    __tablename__ = 'physicalfeature'
    __table_args__ = (
        Index('featureIdentification', 'associatedWith', 'beginDate', 'classifiedInto', 'description', unique=True),
        Index('physicalFeatureidentification_idx', 'classifiedInto'),
        Index('stationfeature', 'associatedWith')
    )

    associatedWith = Column(ForeignKey('station.stationId'), primary_key=True, nullable=False)
    beginDate = Column(String(50), primary_key=True, nullable=False)
    endDate = Column(String(50))
    image = Column(String(255))
    description = Column(String(255), primary_key=True, nullable=False)
    classifiedInto = Column(ForeignKey('physicalfeatureclass.featureClass'), primary_key=True, nullable=False)

    station = relationship('Station')
    physicalfeatureclas = relationship('Physicalfeatureclas')


class Stationelement(Base):
    __tablename__ = 'stationelement'
    __table_args__ = (
        Index('stationElementIdentification', 'recordedFrom', 'describedBy', 'recordedWith', 'beginDate', unique=True),
        Index('obsElementobservationInitial', 'describedBy'),
        Index('stationobservationInitial', 'recordedFrom')
    )

    recordedFrom = Column(ForeignKey('station.stationId'), primary_key=True, nullable=False)
    describedBy = Column(ForeignKey('obselement.elementId'), primary_key=True, nullable=False)
    recordedWith = Column(ForeignKey('instrument.instrumentId'), primary_key=True, nullable=False)
    instrumentcode = Column(String(6))
    scheduledFor = Column(ForeignKey('obsscheduleclass.scheduleClass'))
    height = Column(Float(6))
    beginDate = Column(String(50), primary_key=True, nullable=False)
    endDate = Column(String(50))

    obselement = relationship('Obselement')
    station = relationship('Station')
    instrument = relationship('Instrument')
    obsscheduleclas = relationship('Obsscheduleclas')


class Faultresolution(Base):
    __tablename__ = 'faultresolution'
    __table_args__ = (
        Index('solution', 'resolvedDatetime', 'associatedWith', unique=True),
    )

    resolvedDatetime = Column(String(50), primary_key=True, nullable=False)
    resolvedBy = Column(String(255))
    associatedWith = Column(ForeignKey('instrumentfaultreport.reportId'), primary_key=True, nullable=False)
    remarks = Column(String(255))

    instrumentfaultreport = relationship('Instrumentfaultreport')
