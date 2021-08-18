# coding: utf-8
from sqlalchemy import BigInteger, CHAR, Column, DECIMAL, Date, DateTime, Float, ForeignKey, Index, Integer, String, Table, Text, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_abc = Table(
    'abc', metadata,
    Column('No', Integer, nullable=False, unique=True),
    Column('Element_abbreviation', Text, nullable=False),
    Column('Element_Name', Text, nullable=False),
    Column('Element_Details', Text, nullable=False),
    Column('Climsoft_Element', Text, nullable=False),
    Column('Bufr_Element', Text, nullable=False),
    Column('unit', Text, nullable=False),
    Column('lower_limit', Text, nullable=False),
    Column('upper_limit', Text, nullable=False),
    Column('obsv', Text, nullable=False)
)


class Acquisitiontype(Base):
    __tablename__ = 'acquisitiontype'

    code = Column(Integer, primary_key=True, server_default=text("'0'"))
    description = Column(String(255))


t_aws1 = Table(
    'aws1', metadata,
    Column('No', Integer, nullable=False, unique=True),
    Column('Element_abbreviation', Text, nullable=False),
    Column('Element_Name', Text, nullable=False),
    Column('Element_Details', Text, nullable=False),
    Column('Climsoft_Element', Text, nullable=False),
    Column('Bufr_Element', Text, nullable=False),
    Column('unit', Text, nullable=False),
    Column('lower_limit', Text, nullable=False),
    Column('upper_limit', Text, nullable=False),
    Column('obsv', Text, nullable=False)
)


class AwsBasestation(Base):
    __tablename__ = 'aws_basestation'

    ftpId = Column(String(50), primary_key=True, unique=True)
    inputFolder = Column(String(20), nullable=False)
    ftpMode = Column(String(10))
    userName = Column(String(15), nullable=False)
    password = Column(String(15), nullable=False)


class AwsElement(Base):
    __tablename__ = 'aws_elements'

    aws_element = Column(String(50), primary_key=True, nullable=False)
    climsoft_element = Column(String(50), primary_key=True, nullable=False)
    element_description = Column(String(50), nullable=False)


t_aws_lsi = Table(
    'aws_lsi', metadata,
    Column('Cols', Integer, nullable=False, unique=True),
    Column('Element_abbreviation', String(20)),
    Column('Element_Name', String(20)),
    Column('Element_Details', String(25)),
    Column('Climsoft_Element', String(6)),
    Column('Bufr_Element', String(6)),
    Column('unit', String(15)),
    Column('lower_limit', String(10)),
    Column('upper_limit', String(10)),
    Column('obsv', String(25))
)


t_aws_lsi1 = Table(
    'aws_lsi1', metadata,
    Column('Cols', Integer, nullable=False, unique=True),
    Column('Element_abbreviation', String(20)),
    Column('Element_Name', String(20)),
    Column('Element_Details', String(25)),
    Column('Climsoft_Element', String(6)),
    Column('Bufr_Element', String(6)),
    Column('unit', String(15)),
    Column('lower_limit', String(10)),
    Column('upper_limit', String(10)),
    Column('obsv', String(25))
)


class AwsMalawi1(Base):
    __tablename__ = 'aws_malawi1'

    Cols = Column(Integer, primary_key=True)
    Element_abbreviation = Column(String(50))
    Element_Name = Column(String(50), index=True)
    Element_Details = Column(String(50))
    Climsoft_Element = Column(String(6))
    Bufr_Element = Column(String(6))
    unit = Column(String(15))
    lower_limit = Column(String(50))
    upper_limit = Column(String(50))
    obsv = Column(String(50))


t_aws_malawi12 = Table(
    'aws_malawi12', metadata,
    Column('No', Integer, nullable=False, unique=True),
    Column('Element_abbreviation', Text, nullable=False),
    Column('Element_Name', Text, nullable=False),
    Column('Element_Details', Text, nullable=False),
    Column('Climsoft_Element', Text, nullable=False),
    Column('Bufr_Element', Text, nullable=False),
    Column('unit', Text, nullable=False),
    Column('lower_limit', Text, nullable=False),
    Column('upper_limit', Text, nullable=False),
    Column('obsv', Text, nullable=False)
)


class AwsMs(Base):
    __tablename__ = 'aws_mss'

    ftpId = Column(String(50), primary_key=True)
    inputFolder = Column(String(20), nullable=False)
    userName = Column(String(15), nullable=False)
    ftpMode = Column(String(10))
    password = Column(String(15))


class AwsProcessParameter(Base):
    __tablename__ = 'aws_process_parameters'

    RetrieveInterval = Column(Integer, primary_key=True, server_default=text("'60'"))
    HourOffset = Column(Integer, nullable=False, server_default=text("'10'"))
    RetrievePeriod = Column(Integer, nullable=False, server_default=text("'1'"))
    RetrieveTimeout = Column(Integer, nullable=False, server_default=text("'20'"))
    DelinputFile = Column(TINYINT, nullable=False, server_default=text("'1'"))
    UTCDiff = Column(TINYINT(2), nullable=False, server_default=text("'00'"))


t_aws_rema1 = Table(
    'aws_rema1', metadata,
    Column('Cols', Integer, nullable=False, unique=True),
    Column('Element_abbreviation', String(20)),
    Column('Element_Name', String(20)),
    Column('Element_Details', String(25)),
    Column('Climsoft_Element', String(6)),
    Column('Bufr_Element', String(6)),
    Column('unit', String(15)),
    Column('lower_limit', String(10)),
    Column('upper_limit', String(10)),
    Column('obsv', String(25))
)


t_aws_rwanda1 = Table(
    'aws_rwanda1', metadata,
    Column('Cols', Integer, server_default=text("'0'")),
    Column('Element_abbreviation', String(50)),
    Column('Element_Name', String(50), index=True),
    Column('Element_Details', String(50)),
    Column('Climsoft_Element', String(6)),
    Column('Bufr_Element', String(6)),
    Column('unit', String(15)),
    Column('lower_limit', String(50)),
    Column('upper_limit', String(50)),
    Column('obsv', String(50))
)


class AwsRwanda4(Base):
    __tablename__ = 'aws_rwanda4'

    Cols = Column(Integer, primary_key=True)
    Element_Name = Column(String(20))
    Element_Abbreviation = Column(String(20))
    Element_Details = Column(String(25))
    Climsoft_Element = Column(String(6))
    Bufr_Element = Column(String(6))
    unit = Column(String(15))
    lower_limit = Column(String(10))
    upper_limit = Column(String(10))
    obsv = Column(String(25))


t_aws_rwanda_rain = Table(
    'aws_rwanda_rain', metadata,
    Column('Cols', Integer, nullable=False, unique=True),
    Column('Element_abbreviation', String(20)),
    Column('Element_Name', String(20)),
    Column('Element_Details', String(25)),
    Column('Climsoft_Element', String(6)),
    Column('Bufr_Element', String(6)),
    Column('unit', String(15)),
    Column('lower_limit', String(10)),
    Column('upper_limit', String(10)),
    Column('obsv', String(25))
)


class AwsSasscal1(Base):
    __tablename__ = 'aws_sasscal1'

    Cols = Column(Integer, primary_key=True, server_default=text("'0'"))
    Element_Abbreviation = Column(String(50))
    Element_Name = Column(String(50))
    Element_Details = Column(String(50))
    Climsoft_Element = Column(String(6))
    Bufr_Element = Column(String(6))
    unit = Column(String(15))
    lower_limit = Column(String(50))
    upper_limit = Column(String(50))
    obsv = Column(String(50))


class AwsSite(Base):
    __tablename__ = 'aws_sites'

    SiteID = Column(String(20), primary_key=True, unique=True)
    SiteName = Column(String(50))
    InputFile = Column(String(255))
    FilePrefix = Column(String(50))
    chkPrefix = Column(TINYINT(1), server_default=text("'0'"))
    DataStructure = Column(String(50))
    MissingDataFlag = Column(String(20))
    awsServerIP = Column(String(50))
    OperationalStatus = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    GTSEncode = Column(TINYINT(1), server_default=text("'0'"))
    GTSHeader = Column(String(20))


class AwsStation(Base):
    __tablename__ = 'aws_stations'

    aws_id = Column(String(50), primary_key=True, nullable=False)
    national_id = Column(String(50), primary_key=True, nullable=False)
    station_name = Column(String(50))


class AwsStructure(Base):
    __tablename__ = 'aws_structures'

    strID = Column(Integer, nullable=False, unique=True)
    strName = Column(String(20), primary_key=True)
    data_delimiter = Column(String(10), nullable=False)
    hdrRows = Column(Integer, nullable=False)
    txtQualifier = Column(String(5))


class AwsTahmo(Base):
    __tablename__ = 'aws_tahmo'

    Cols = Column(Integer, primary_key=True)
    Element_abbreviation = Column(String(50))
    Element_Name = Column(String(50))
    Element_Details = Column(String(50))
    Climsoft_Element = Column(String(6))
    Bufr_Element = Column(String(6))
    unit = Column(String(15))
    lower_limit = Column(String(50))
    upper_limit = Column(String(50))
    obsv = Column(String(50))


t_aws_test = Table(
    'aws_test', metadata,
    Column('Cols', Integer, nullable=False, unique=True),
    Column('Element_abbreviation', String(20)),
    Column('Element_Name', String(20)),
    Column('Element_Details', String(25)),
    Column('Climsoft_Element', String(6)),
    Column('Bufr_Element', String(6)),
    Column('unit', String(15)),
    Column('lower_limit', String(10)),
    Column('upper_limit', String(10)),
    Column('obsv', String(25))
)


t_aws_toa5_bw1 = Table(
    'aws_toa5_bw1', metadata,
    Column('Cols', Integer, server_default=text("'0'")),
    Column('Element_Abbreviation', String(50), unique=True),
    Column('Element_Name', String(50)),
    Column('Element_Details', String(50)),
    Column('Climsoft_Element', String(6)),
    Column('Bufr_Element', String(6)),
    Column('unit', String(15)),
    Column('lower_limit', String(50)),
    Column('upper_limit', String(50)),
    Column('obsv', String(50))
)


class AwsToa5Mg2(Base):
    __tablename__ = 'aws_toa5_mg2'

    Cols = Column(BigInteger, primary_key=True)
    Element_Abbreviation = Column(String(50))
    Element_Name = Column(String(50))
    Element_Details = Column(String(50))
    Climsoft_Element = Column(String(6))
    Bufr_Element = Column(String(6))
    unit = Column(String(15))
    lower_limit = Column(String(50))
    upper_limit = Column(String(50))
    obsv = Column(String(50))


t_bufr_crex_data = Table(
    'bufr_crex_data', metadata,
    Column('nos', Integer, server_default=text("'0'")),
    Column('Bufr_Template', String(50)),
    Column('Crex_Template', String(50)),
    Column('Sequence_Descriptor1', String(50)),
    Column('Sequence_Descriptor0', String(50)),
    Column('Bufr_Element', String(50)),
    Column('Crex_Element', String(255)),
    Column('Climsoft_Element', String(255)),
    Column('Element_Name', String(255)),
    Column('Crex_Unit', String(25)),
    Column('Crex_Scale', String(25), nullable=False),
    Column('Crex_DataWidth', String(25), nullable=False),
    Column('Bufr_Unit', String(255), nullable=False),
    Column('Bufr_Scale', String(25), nullable=False, server_default=text("'0'")),
    Column('Bufr_RefValue', String(50), server_default=text("'0'")),
    Column('Bufr_DataWidth_Bits', String(50), server_default=text("'0'")),
    Column('selected', TINYINT),
    Column('Observation', String(255)),
    Column('Crex_Data', String(30)),
    Column('Bufr_Data', String(255), server_default=text("'0'"))
)


t_bufr_crex_master = Table(
    'bufr_crex_master', metadata,
    Column('Bufr_FXY', String(6), nullable=False),
    Column('Crex_Fxxyyy', String(255), nullable=False),
    Column('ElementName', String(255), nullable=False),
    Column('Bufr_Unit', String(255), nullable=False),
    Column('Bufr_Scale', String(25), nullable=False, server_default=text("'0'")),
    Column('Bufr_RefValue', String(50), server_default=text("'0'")),
    Column('Bufr_DataWidth_Bits', String(50), server_default=text("'0'")),
    Column('Crex_Unit', String(25)),
    Column('Crex_Scale', String(25), nullable=False),
    Column('Crex_DataWidth', String(25), nullable=False),
    Column('Observation', String(255)),
    Column('Crex_Data', String(30)),
    Column('Bufr_Data', String(255), server_default=text("'0'"))
)


class BufrIndicator(Base):
    __tablename__ = 'bufr_indicators'

    Tmplate = Column(String(50), primary_key=True, server_default=text("'0'"))
    Msg_Header = Column(String(50), server_default=text("'0'"))
    BUFR_Edition = Column(String(10), server_default=text("'0'"))
    Originating_Centre = Column(String(10), server_default=text("'0'"))
    Originating_SubCentre = Column(String(10), server_default=text("'0'"))
    Update_Sequence = Column(String(10), server_default=text("'0'"))
    Optional_Section = Column(String(10), server_default=text("'0'"))
    Data_Category = Column(String(10), server_default=text("'0'"))
    Intenational_Data_SubCategory = Column(String(10), server_default=text("'0'"))
    Local_Data_SubCategory = Column(String(10), server_default=text("'0'"))
    Master_table = Column(String(10), server_default=text("'0'"))
    Local_Table = Column(String(10), server_default=text("'0'"))


t_ccitt = Table(
    'ccitt', metadata,
    Column('Characters', String(25)),
    Column('MostSignificant', Integer),
    Column('LeastSignificant', Integer)
)


class Climsoftuser(Base):
    __tablename__ = 'climsoftusers'

    userName = Column(String(50), primary_key=True)
    userRole = Column(String(50), nullable=False)


class CodeFlag(Base):
    __tablename__ = 'code_flag'

    FXY = Column(String(255), primary_key=True)
    Fxyyy = Column(String(50))
    Description = Column(String(255))
    Bufr_DataWidth_Bits = Column(Integer)
    Crex_DataWidth = Column(String(25))
    Bufr_Unit = Column(String(255))
    Bufr_Value = Column(String(50))
    Crex_Value = Column(String(10))


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


class Flagtable(Base):
    __tablename__ = 'flagtable'

    Bufr_Descriptor = Column(String(6), primary_key=True)
    Crex_Descriptor = Column(String(6))
    Details = Column(String(255))
    Widths = Column(Integer, server_default=text("'0'"))
    Missing = Column(Integer, server_default=text("'0'"))


class FormAgro1(Base):
    __tablename__ = 'form_agro1'

    stationId = Column(String(50), primary_key=True, nullable=False, server_default=text("''"))
    yyyy = Column(Integer, primary_key=True, nullable=False)
    mm = Column(Integer, primary_key=True, nullable=False)
    dd = Column(Integer, primary_key=True, nullable=False)
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
    __tablename__ = 'form_daily2'

    stationId = Column(String(50), primary_key=True, nullable=False)
    elementId = Column(Integer, primary_key=True, nullable=False)
    yyyy = Column(Integer, primary_key=True, nullable=False)
    mm = Column(Integer, primary_key=True, nullable=False)
    hh = Column(Integer, primary_key=True, nullable=False)
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
    __tablename__ = 'form_hourly'

    stationId = Column(String(50), primary_key=True, nullable=False)
    elementId = Column(Integer, primary_key=True, nullable=False)
    yyyy = Column(Integer, primary_key=True, nullable=False)
    mm = Column(Integer, primary_key=True, nullable=False)
    dd = Column(Integer, primary_key=True, nullable=False)
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
    __tablename__ = 'form_hourly_time_selection'

    hh = Column(Integer, primary_key=True)
    hh_selection = Column(TINYINT)


class FormHourlywind(Base):
    __tablename__ = 'form_hourlywind'

    stationId = Column(String(255), primary_key=True, nullable=False)
    yyyy = Column(Integer, primary_key=True, nullable=False)
    mm = Column(Integer, primary_key=True, nullable=False)
    dd = Column(Integer, primary_key=True, nullable=False)
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
    __tablename__ = 'form_monthly'

    stationId = Column(String(255), primary_key=True, nullable=False)
    elementId = Column(Integer, primary_key=True, nullable=False)
    yyyy = Column(Integer, primary_key=True, nullable=False)
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
    __tablename__ = 'form_synoptic2_tdcf'
    __table_args__ = (
        Index('Identification', 'stationId', 'yyyy', 'mm', 'dd', 'hh', unique=True),
    )

    stationId = Column(String(10), primary_key=True, nullable=False)
    yyyy = Column(BigInteger, primary_key=True, nullable=False)
    mm = Column(BigInteger, primary_key=True, nullable=False)
    dd = Column(BigInteger, primary_key=True, nullable=False)
    hh = Column(String(5), primary_key=True, nullable=False)
    _106 = Column('106', String(6))
    _107 = Column('107', String(6))
    _399 = Column('399', String(5))
    _301 = Column('301', String(8))
    _185 = Column('185', String(6))
    _101 = Column('101', String(5))
    _103 = Column('103', String(5))
    _105 = Column('105', String(50))
    _110 = Column('110', String(5))
    _114 = Column('114', String(5))
    _115 = Column('115', String(5))
    _168 = Column('168', String(5))
    _192 = Column('192', String(5))
    _169 = Column('169', String(5))
    _170 = Column('170', String(5))
    _171 = Column('171', String(5))
    _119 = Column('119', String(5))
    _116 = Column('116', String(5))
    _117 = Column('117', String(5))
    _118 = Column('118', String(5))
    _123 = Column('123', String(5))
    _120 = Column('120', String(5))
    _121 = Column('121', String(5))
    _122 = Column('122', String(5))
    _127 = Column('127', String(5))
    _124 = Column('124', String(5))
    _125 = Column('125', String(5))
    _126 = Column('126', String(5))
    _131 = Column('131', String(5))
    _128 = Column('128', String(5))
    _129 = Column('129', String(5))
    _130 = Column('130', String(5))
    _167 = Column('167', String(5))
    _197 = Column('197', String(50))
    _193 = Column('193', String(5))
    _18 = Column('18', String(6))
    _532 = Column('532', String(6))
    _132 = Column('132', String(6))
    _5 = Column('5', String(6))
    _174 = Column('174', String(50))
    _3 = Column('3', String(5))
    _2 = Column('2', String(5))
    _112 = Column('112', String(5))
    _111 = Column('111', String(5))
    _85 = Column('85', String(50))
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
    __tablename__ = 'form_synoptic_2_ra1'

    stationId = Column(String(50), primary_key=True, nullable=False, server_default=text("''"))
    yyyy = Column(Integer, primary_key=True, nullable=False)
    mm = Column(Integer, primary_key=True, nullable=False)
    dd = Column(Integer, primary_key=True, nullable=False)
    hh = Column(Integer, primary_key=True, nullable=False)
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


class Gap(Base):
    __tablename__ = 'gaps'

    Missing_STNID = Column(String(255), primary_key=True, nullable=False)
    Missing_ELEM = Column(BigInteger, primary_key=True, nullable=False)
    Missing_Date = Column(Date, primary_key=True, nullable=False)


class LanguageTranslation(Base):
    __tablename__ = 'language_translation'

    tagID = Column(String(50), primary_key=True)
    en = Column(String(100))
    fr = Column(String(100))
    de = Column(String(100))
    pt = Column(String(100))


class MissingDatum(Base):
    __tablename__ = 'missing_data'

    STN_ID = Column(String(255), primary_key=True, nullable=False)
    OBS_DATE = Column(Date, primary_key=True, nullable=False)
    ELEM = Column(BigInteger, primary_key=True, nullable=False)


class MissingStat(Base):
    __tablename__ = 'missing_stats'

    STN_ID = Column(String(255), primary_key=True, nullable=False)
    ELEM = Column(BigInteger, primary_key=True, nullable=False)
    MISSING = Column(BigInteger)
    Closing_Date = Column(Date, primary_key=True, nullable=False)
    Opening_Date = Column(Date, primary_key=True, nullable=False)


class Obselement(Base):
    __tablename__ = 'obselement'

    elementId = Column(BigInteger, primary_key=True, index=True, server_default=text("'0'"))
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

    formId = Column(String(50), primary_key=True, index=True)
    description = Column(String(255))


class QcInterelement1(Base):
    __tablename__ = 'qc_interelement_1'

    stationId_1 = Column(String(50), primary_key=True, nullable=False)
    elementId_1 = Column(Integer, primary_key=True, nullable=False)
    obsDatetime_1 = Column(DateTime, primary_key=True, nullable=False)
    obsValue_1 = Column(Integer)
    qcStatus_1 = Column(Integer)
    acquisitionType_1 = Column(Integer)
    obsLevel_1 = Column(String(50))
    capturedBy_1 = Column(String(50))
    dataForm_1 = Column(String(50))


class QcInterelement2(Base):
    __tablename__ = 'qc_interelement_2'

    stationId_2 = Column(String(50), primary_key=True, nullable=False)
    elementId_2 = Column(Integer, primary_key=True, nullable=False)
    obsDatetime_2 = Column(DateTime, primary_key=True, nullable=False)
    obsValue_2 = Column(Integer)
    qcStatus_2 = Column(Integer)
    acquisitionType_2 = Column(Integer)
    obsLevel_2 = Column(String(50))
    capturedBy_2 = Column(String(50))
    dataForm_2 = Column(String(50))


class QcInterelementRelationshipDefinition(Base):
    __tablename__ = 'qc_interelement_relationship_definition'

    elementId_1 = Column(Integer, primary_key=True, nullable=False)
    relationship = Column(String(50), primary_key=True, nullable=False)
    elementId_2 = Column(Integer, primary_key=True, nullable=False)


t_qcabslimits = Table(
    'qcabslimits', metadata,
    Column('StationId', String(15), nullable=False),
    Column('ElementId', BigInteger),
    Column('Datetime', DateTime),
    Column('YYYY', Integer),
    Column('mm', TINYINT),
    Column('dd', TINYINT),
    Column('hh', TINYINT),
    Column('obsValue', String(10)),
    Column('limitValue', String(10)),
    Column('qcStatus', Integer),
    Column('acquisitionType', Integer),
    Column('obsLevel', String(255)),
    Column('capturedBy', String(255)),
    Column('dataForm', String(255)),
    Index('obsInitialIdentification', 'StationId', 'ElementId', 'Datetime', unique=True)
)


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


class Routinereportdefinition(Base):
    __tablename__ = 'routinereportdefinition'

    reportClass = Column(String(255), primary_key=True)
    reportSchedule = Column(String(255))
    reportCode = Column(String(255), index=True)
    reportDescription = Column(String(255))


class SeqDailyElement(Base):
    __tablename__ = 'seq_daily_element'

    seq = Column(BigInteger, primary_key=True)
    elementId = Column(BigInteger, nullable=False)


t_seq_day = Table(
    'seq_day', metadata,
    Column('dd', String(50), server_default=text("'0'"))
)


class SeqElement(Base):
    __tablename__ = 'seq_element'

    seq = Column(BigInteger, primary_key=True, index=True)
    element_code = Column(String(50))


t_seq_hour = Table(
    'seq_hour', metadata,
    Column('hh', Integer, server_default=text("'0'"))
)


t_seq_leap_year = Table(
    'seq_leap_year', metadata,
    Column('yyyy', Integer)
)


t_seq_month = Table(
    'seq_month', metadata,
    Column('mm', String(50), server_default=text("'0'"))
)


class SeqMonthDay(Base):
    __tablename__ = 'seq_month_day'

    mm = Column(Integer, primary_key=True, nullable=False)
    dd = Column(Integer, primary_key=True, nullable=False)


t_seq_month_day_element = Table(
    'seq_month_day_element', metadata,
    Column('mm', Integer, nullable=False),
    Column('dd', Integer, nullable=False),
    Column('elementId', Integer, nullable=False)
)


t_seq_month_day_element_leap_yr = Table(
    'seq_month_day_element_leap_yr', metadata,
    Column('mm', Integer, nullable=False),
    Column('dd', Integer, nullable=False),
    Column('elementId', Integer, nullable=False)
)


class SeqMonthDayLeapYr(Base):
    __tablename__ = 'seq_month_day_leap_yr'

    mm = Column(Integer, primary_key=True, nullable=False)
    dd = Column(Integer, primary_key=True, nullable=False)


class SeqMonthDaySynoptime(Base):
    __tablename__ = 'seq_month_day_synoptime'

    mm = Column(Integer, primary_key=True, nullable=False)
    dd = Column(Integer, primary_key=True, nullable=False)
    hh = Column(Integer, primary_key=True, nullable=False)


class SeqMonthDaySynoptimeLeapYr(Base):
    __tablename__ = 'seq_month_day_synoptime_leap_yr'

    mm = Column(Integer, primary_key=True, nullable=False)
    dd = Column(Integer, primary_key=True, nullable=False)
    hh = Column(Integer, primary_key=True, nullable=False)


class SeqMonthlyElement(Base):
    __tablename__ = 'seq_monthly_element'

    seq = Column(BigInteger, primary_key=True)
    elementId = Column(BigInteger, nullable=False)


t_seq_year = Table(
    'seq_year', metadata,
    Column('yyyy', Integer)
)


t_ss = Table(
    'ss', metadata,
    Column('Cols', Integer, nullable=False, unique=True),
    Column('Element_abbreviation', String(20)),
    Column('Element_Name', String(20)),
    Column('Element_Details', String(25)),
    Column('Climsoft_Element', String(6)),
    Column('Bufr_Element', String(6)),
    Column('unit', String(15)),
    Column('lower_limit', String(10)),
    Column('upper_limit', String(10)),
    Column('obsv', String(25))
)


class Station(Base):
    __tablename__ = 'station'

    stationId = Column(String(255), primary_key=True, index=True)
    stationName = Column(String(255))
    wmoid = Column(String(20))
    icaoid = Column(String(20))
    latitude = Column(Float(11, True))
    qualifier = Column(String(20))
    longitude = Column(Float(11, True))
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


class Stationnetworkdefinition(Base):
    __tablename__ = 'stationnetworkdefinition'

    networkAbbreviation = Column(String(255), primary_key=True, server_default=text("''"))
    networkFullName = Column(String(255))


class Synopfeature(Base):
    __tablename__ = 'synopfeature'

    abbreviation = Column(String(255), primary_key=True)
    description = Column(String(255))


class Tblproduct(Base):
    __tablename__ = 'tblproducts'

    productId = Column(String(10), primary_key=True, index=True)
    productName = Column(String(50))
    prDetails = Column(String(50))
    prCategory = Column(String(50))


t_tdcf_indicators = Table(
    'tdcf_indicators', metadata,
    Column('CREX_Edition', Integer, server_default=text("'0'")),
    Column('CREX_Table', Integer, server_default=text("'0'")),
    Column('BUFR_Table', Integer, server_default=text("'0'")),
    Column('Local_Table', Integer, server_default=text("'0'")),
    Column('Data_Category', Integer, server_default=text("'0'")),
    Column('Data_SubCategory', Integer, server_default=text("'0'")),
    Column('Originating_Centre', Integer, server_default=text("'0'"))
)


t_testing_aws = Table(
    'testing_aws', metadata,
    Column('Cols', Integer, nullable=False, unique=True),
    Column('Element_abbreviation', String(20)),
    Column('Element_Name', String(20)),
    Column('Element_Details', String(25)),
    Column('Climsoft_Element', String(6)),
    Column('Bufr_Element', String(6)),
    Column('unit', String(15)),
    Column('lower_limit', String(10)),
    Column('upper_limit', String(10)),
    Column('obsv', String(25))
)


t_testing_aws1 = Table(
    'testing_aws1', metadata,
    Column('Cols', Integer, nullable=False, unique=True),
    Column('Element_abbreviation', String(20)),
    Column('Element_Name', String(20)),
    Column('Element_Details', String(25)),
    Column('Climsoft_Element', String(6)),
    Column('Bufr_Element', String(6)),
    Column('unit', String(15)),
    Column('lower_limit', String(10)),
    Column('upper_limit', String(10)),
    Column('obsv', String(25))
)


t_tm_307073 = Table(
    'tm_307073', metadata,
    Column('order', Float(asdecimal=True)),
    Column('Bufr_Template', String(255)),
    Column('CREX_Template', String(255)),
    Column('Sequence_Descriptor1', String(255)),
    Column('Sequence_Descriptor0', String(255)),
    Column('Bufr_Element', String(255)),
    Column('Crex_Element', String(255)),
    Column('Climsoft_Element', String(255)),
    Column('Element_Name', String(255)),
    Column('Crex_Unit', String(255)),
    Column('Crex_Scale', String(255)),
    Column('Crex_DataWidth', String(255)),
    Column('Bufr_Unit', String(255)),
    Column('Bufr_Scale', Float(asdecimal=True)),
    Column('Bufr_RefValue', Float(asdecimal=True)),
    Column('Bufr_DataWidth_Bits', Float(asdecimal=True)),
    Column('Selected', TINYINT),
    Column('Observation', String(255)),
    Column('Crex_Data', String(255)),
    Column('Bufr_Data', String(255))
)


t_tm_307080 = Table(
    'tm_307080', metadata,
    Column('order', Integer, server_default=text("'0'")),
    Column('Bufr_Template', String(50)),
    Column('Crex_Template', String(50)),
    Column('Sequence_Descriptor1', String(50)),
    Column('Sequence_Descriptor0', String(50)),
    Column('Bufr_Element', String(50)),
    Column('Crex_Element', String(255)),
    Column('Climsoft_Element', String(255)),
    Column('Element_Name', String(255)),
    Column('synop_code', String(255), index=True),
    Column('unit', String(255)),
    Column('scale', String(255)),
    Column('width', String(255)),
    Column('units_length_scale', String(255)),
    Column('data_type', String(255)),
    Column('selected', TINYINT),
    Column('observation', String(255)),
    Column('Crex_Data', String(255)),
    Column('Bufr_Data', String(50))
)


t_tm_307081 = Table(
    'tm_307081', metadata,
    Column('Nos', Integer, server_default=text("'0'")),
    Column('Bufr_Template', String(50)),
    Column('Crex_Template', String(50)),
    Column('Sequence_Descriptor1', String(50)),
    Column('Sequence_Descriptor0', String(50)),
    Column('Bufr_Element', String(50)),
    Column('Crex_Element', String(255)),
    Column('Climsoft_Element', String(255)),
    Column('Element_Name', String(255)),
    Column('synop_code', String(255), index=True),
    Column('unit', String(255)),
    Column('scale', String(255)),
    Column('width', String(255)),
    Column('units_length_scale', String(255)),
    Column('data_type', String(255)),
    Column('selected', TINYINT),
    Column('Observation', String(255)),
    Column('Crex_Data', String(255)),
    Column('Bufr_Data', String(50))
)


t_tm_307082 = Table(
    'tm_307082', metadata,
    Column('order', Integer, server_default=text("'0'")),
    Column('Bufr_Template', String(50)),
    Column('Crex_Template', String(50)),
    Column('Sequence_Descriptor1', String(50)),
    Column('Sequence_Descriptor0', String(50)),
    Column('Bufr_Element', String(50)),
    Column('Crex_Element', String(255)),
    Column('Climsoft_Element', String(255)),
    Column('Element_Name', String(255)),
    Column('synop_code', String(255), index=True),
    Column('unit', String(255)),
    Column('scale', String(255)),
    Column('width', String(255)),
    Column('units_length_scale', String(255)),
    Column('data_type', String(255)),
    Column('selected', TINYINT),
    Column('observation', String(255)),
    Column('Crex_Data', String(255)),
    Column('Bufr_Data', String(50))
)


t_tm_307083 = Table(
    'tm_307083', metadata,
    Column('order', Integer, server_default=text("'0'")),
    Column('Bufr_Template', String(50)),
    Column('Crex_Template', String(50)),
    Column('Sequence_Descriptor1', String(50)),
    Column('Sequence_Descriptor0', String(50)),
    Column('Bufr_Element', String(50)),
    Column('Crex_Element', String(255)),
    Column('Climsoft_Element', String(255)),
    Column('Element_Name', String(255)),
    Column('synop_code', String(255), index=True),
    Column('unit', String(255)),
    Column('scale', String(255)),
    Column('width', String(255)),
    Column('units_length_scale', String(255)),
    Column('data_type', String(255)),
    Column('selected', TINYINT),
    Column('observation', String(255)),
    Column('Crex_Data', String(255)),
    Column('Bufr_Data', String(50))
)


t_tm_307084 = Table(
    'tm_307084', metadata,
    Column('order', Integer, server_default=text("'0'")),
    Column('Bufr_Template', String(50)),
    Column('Crex_Template', String(50)),
    Column('Sequence_Descriptor1', String(50)),
    Column('Sequence_Descriptor0', String(50)),
    Column('Bufr_Element', String(50)),
    Column('Crex_Element', String(255)),
    Column('Climsoft_Element', String(255)),
    Column('Element_Name', String(255)),
    Column('synop_code', String(255), index=True),
    Column('unit', String(255)),
    Column('scale', String(255)),
    Column('width', String(255)),
    Column('units_length_scale', String(255)),
    Column('data_type', String(255)),
    Column('selected', TINYINT),
    Column('observation', String(255)),
    Column('Crex_Data', String(255)),
    Column('Bufr_Data', String(50))
)


t_tm_307086 = Table(
    'tm_307086', metadata,
    Column('order', Integer, server_default=text("'0'")),
    Column('Bufr_Template', String(50)),
    Column('Crex_Template', String(50)),
    Column('Sequence_Descriptor1', String(50)),
    Column('Sequence_Descriptor0', String(50)),
    Column('Bufr_Element', String(50)),
    Column('Crex_Element', String(255)),
    Column('Climsoft_Element', String(255)),
    Column('Element_Name', String(255)),
    Column('synop_code', String(255), index=True),
    Column('unit', String(255)),
    Column('scale', String(255)),
    Column('width', String(255)),
    Column('units_length_scale', String(255)),
    Column('data_type', String(255)),
    Column('selected', TINYINT),
    Column('observation', String(255)),
    Column('Crex_Data', String(255)),
    Column('Bufr_Data', String(50))
)


t_tm_307089 = Table(
    'tm_307089', metadata,
    Column('order', Integer, server_default=text("'0'")),
    Column('Bufr_Template', String(50)),
    Column('Crex_Template', String(50)),
    Column('Sequence_Descriptor1', String(10)),
    Column('Sequence_Descriptor0', String(10)),
    Column('Bufr_Element', String(50)),
    Column('Crex_Element', String(255)),
    Column('Climsoft_Element', String(50)),
    Column('Element_Name', String(255), index=True),
    Column('synop_code', String(50), index=True),
    Column('unit', String(50)),
    Column('scale', String(50)),
    Column('width', String(50)),
    Column('units_length_scale', String(255)),
    Column('data_type', String(255)),
    Column('selected', TINYINT),
    Column('observation', String(100)),
    Column('crex', String(25)),
    Column('Crex_Data', String(255)),
    Column('Bufr_Data', String(50))
)


class Tm307091(Base):
    __tablename__ = 'tm_307091'

    Rec = Column(Integer, primary_key=True, server_default=text("'0'"))
    Bufr_Template = Column(String(50))
    CREX_Template = Column(String(50))
    Sequence_Descriptor1 = Column(String(255))
    Sequence_Descriptor0 = Column(String(255))
    Bufr_Element = Column(String(255))
    Crex_Element = Column(String(50))
    Climsoft_Element = Column(String(50))
    Element_Name = Column(String(255))
    Crex_Unit = Column(String(25))
    Crex_Scale = Column(String(25))
    Crex_DataWidth = Column(String(25))
    Bufr_Unit = Column(String(255))
    Bufr_Scale = Column(Integer)
    Bufr_RefValue = Column(BigInteger)
    Bufr_DataWidth_Bits = Column(Integer)
    Selected = Column(TINYINT)
    Observation = Column(String(255))
    Crex_Data = Column(String(30))
    Bufr_Data = Column(String(255))


t_tm_307092 = Table(
    'tm_307092', metadata,
    Column('order', Integer, server_default=text("'0'")),
    Column('Bufr_Template', String(50)),
    Column('CREX_Template', String(50)),
    Column('Sequence_Descriptor1', String(255)),
    Column('Sequence_Descriptor0', String(255)),
    Column('Bufr_Element', String(255)),
    Column('Crex_Element', String(50)),
    Column('Climsoft_Element', String(50)),
    Column('Element_Name', String(255)),
    Column('Crex_Unit', String(25)),
    Column('Crex_Scale', String(25)),
    Column('Crex_DataWidth', String(25)),
    Column('Bufr_Unit', String(255)),
    Column('Bufr_Scale', Integer),
    Column('Bufr_RefValue', BigInteger),
    Column('Bufr_DataWidth_Bits', Integer),
    Column('Selected', TINYINT),
    Column('Observation', String(255)),
    Column('Crex_Data', String(30)),
    Column('Bufr_Data', String(255))
)


t_tm_309052 = Table(
    'tm_309052', metadata,
    Column('order', Integer, server_default=text("'0'")),
    Column('Bufr_Template', String(50)),
    Column('CREX_Template', String(50)),
    Column('Sequence_Descriptor1', String(255)),
    Column('Sequence_Descriptor0', String(255)),
    Column('Bufr_Element', String(255)),
    Column('Crex_Element', String(50)),
    Column('Climsoft_Element', String(50)),
    Column('Element_Name', String(255)),
    Column('Crex_Unit', String(25)),
    Column('Crex_Scale', String(25)),
    Column('Crex_DataWidth', String(25)),
    Column('Bufr_Unit', String(255)),
    Column('Bufr_Scale', Integer),
    Column('Bufr_RefValue', BigInteger),
    Column('Bufr_DataWidth_Bits', Integer),
    Column('Selected', TINYINT),
    Column('Observation', String(255)),
    Column('Crex_Data', String(30)),
    Column('Bufr_Data', String(255))
)


class Userrecord(Base):
    __tablename__ = 'userrecords'

    username = Column(String(255), primary_key=True, server_default=text("''"))
    recsexpt = Column(Integer)
    recsdone = Column(String(255))


class Featuregeographicalposition(Base):
    __tablename__ = 'featuregeographicalposition'
    __table_args__ = (
        Index('FK_mysql_climsoft_db_v4_synopfeatureFeatureGeographicalPosition', 'belongsTo', 'observedOn', unique=True),
    )

    belongsTo = Column(ForeignKey('synopfeature.abbreviation'), primary_key=True, nullable=False)
    observedOn = Column(String(50), primary_key=True, nullable=False)
    latitude = Column(Float(11, True))
    longitude = Column(Float(11, True))

    synopfeature = relationship('Synopfeature')


class Instrument(Base):
    __tablename__ = 'instrument'

    instrumentName = Column(String(255))
    instrumentId = Column(String(255), primary_key=True, index=True)
    serialNumber = Column(String(255))
    abbreviation = Column(String(255))
    model = Column(String(255))
    manufacturer = Column(String(255))
    instrumentUncertainty = Column(Float(11))
    installationDatetime = Column(String(50))
    deinstallationDatetime = Column(String(50))
    height = Column(String(255))
    instrumentPicture = Column(CHAR(255))
    installedAt = Column(ForeignKey('station.stationId'), index=True)

    station = relationship('Station')


class Observationfinal(Base):
    __tablename__ = 'observationfinal'
    __table_args__ = (
        Index('obsFinalIdentification', 'recordedFrom', 'describedBy', 'obsDatetime', unique=True),
    )

    recordedFrom = Column(ForeignKey('station.stationId'), primary_key=True, nullable=False, index=True)
    describedBy = Column(ForeignKey('obselement.elementId'), primary_key=True, nullable=False, index=True)
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
    )

    recordedFrom = Column(ForeignKey('station.stationId'), primary_key=True, nullable=False, index=True)
    describedBy = Column(ForeignKey('obselement.elementId'), primary_key=True, nullable=False, index=True)
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

    scheduleClass = Column(String(255), primary_key=True, index=True, server_default=text("''"))
    description = Column(String(255))
    refersTo = Column(ForeignKey('station.stationId'), index=True)

    station = relationship('Station')


class Paperarchive(Base):
    __tablename__ = 'paperarchive'
    __table_args__ = (
        Index('paper_archive_identification', 'belongsTo', 'formDatetime', 'classifiedInto', unique=True),
    )

    belongsTo = Column(ForeignKey('station.stationId'), primary_key=True, nullable=False)
    formDatetime = Column(DateTime, primary_key=True, nullable=False)
    image = Column(String(255))
    classifiedInto = Column(ForeignKey('paperarchivedefinition.formId'), primary_key=True, nullable=False, index=True)

    station = relationship('Station')
    paperarchivedefinition = relationship('Paperarchivedefinition')


class Physicalfeatureclas(Base):
    __tablename__ = 'physicalfeatureclass'

    featureClass = Column(String(255), primary_key=True, index=True)
    description = Column(String(255))
    refersTo = Column(ForeignKey('station.stationId'), index=True)

    station = relationship('Station')


t_routinereporttransmission = Table(
    'routinereporttransmission', metadata,
    Column('reportClass', ForeignKey('routinereportdefinition.reportClass')),
    Column('reportDatetime', DateTime),
    Column('receivedDatetime', DateTime),
    Column('reportedFrom', ForeignKey('station.stationId'), index=True),
    Index('report', 'reportClass', 'reportDatetime', 'reportedFrom', unique=True)
)


t_stationidalias = Table(
    'stationidalias', metadata,
    Column('idAlias', String(255), unique=True),
    Column('refersTo', String(255)),
    Column('belongsTo', ForeignKey('station.stationId'), index=True),
    Column('idAliasBeginDate', String(50)),
    Column('idAliasEndDate', String(50))
)


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
    latitude = Column(Float(11, True))
    longitude = Column(Float(11, True))
    elevation = Column(BigInteger)
    authority = Column(String(255))
    adminRegion = Column(String(255))
    drainageBasin = Column(String(255))

    station = relationship('Station')


class Stationqualifier(Base):
    __tablename__ = 'stationqualifier'
    __table_args__ = (
        Index('stationid_qualifier_identification', 'qualifier', 'qualifierBeginDate', 'qualifierEndDate', 'belongsTo', unique=True),
    )

    qualifier = Column(String(255), primary_key=True, nullable=False)
    qualifierBeginDate = Column(String(50), primary_key=True, nullable=False)
    qualifierEndDate = Column(String(50), primary_key=True, nullable=False)
    stationTimeZone = Column(Integer, server_default=text("'0'"))
    stationNetworkType = Column(String(255))
    belongsTo = Column(ForeignKey('station.stationId'), primary_key=True, nullable=False, index=True)

    station = relationship('Station')


class Instrumentfaultreport(Base):
    __tablename__ = 'instrumentfaultreport'
    __table_args__ = (
        Index('instrument_report', 'refersTo', 'reportDatetime', 'reportedFrom', unique=True),
    )

    refersTo = Column(ForeignKey('instrument.instrumentId'))
    reportId = Column(BigInteger, primary_key=True, index=True)
    reportDatetime = Column(String(50))
    faultDescription = Column(String(255))
    reportedBy = Column(String(255))
    receivedDatetime = Column(String(50))
    receivedBy = Column(String(255))
    reportedFrom = Column(ForeignKey('station.stationId'), index=True)

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
    performedAt = Column(ForeignKey('station.stationId'), index=True)

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
    )

    associatedWith = Column(ForeignKey('station.stationId'), primary_key=True, nullable=False, index=True)
    beginDate = Column(String(50), primary_key=True, nullable=False)
    endDate = Column(String(50))
    image = Column(String(255))
    description = Column(String(255), primary_key=True, nullable=False)
    classifiedInto = Column(ForeignKey('physicalfeatureclass.featureClass'), primary_key=True, nullable=False, index=True)

    station = relationship('Station')
    physicalfeatureclas = relationship('Physicalfeatureclas')


class Stationelement(Base):
    __tablename__ = 'stationelement'
    __table_args__ = (
        Index('stationElementIdentification', 'recordedFrom', 'describedBy', 'recordedWith', 'beginDate', unique=True),
    )

    recordedFrom = Column(ForeignKey('station.stationId'), primary_key=True, nullable=False, index=True)
    describedBy = Column(ForeignKey('obselement.elementId'), primary_key=True, nullable=False, index=True)
    recordedWith = Column(ForeignKey('instrument.instrumentId'), primary_key=True, nullable=False, index=True)
    instrumentcode = Column(String(6))
    scheduledFor = Column(ForeignKey('obsscheduleclass.scheduleClass'), index=True)
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
    associatedWith = Column(ForeignKey('instrumentfaultreport.reportId'), primary_key=True, nullable=False, index=True)
    remarks = Column(String(255))

    instrumentfaultreport = relationship('Instrumentfaultreport')
