# coding: utf-8
from sqlalchemy import CHAR, Column, Date, DateTime, Float, Integer, String, Text, Time, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Basin(Base):
    __tablename__ = 'Basins'

    Basin = Column(CHAR(5), primary_key=True, server_default=text("''"))
    Basin2 = Column(CHAR(20))
    BasinName = Column(CHAR(150))


class Code(Base):
    __tablename__ = 'Codes'

    Codee = Column(CHAR(10), primary_key=True, server_default=text("''"))
    Message = Column(CHAR(150))


class County(Base):
    __tablename__ = 'Counties'

    County = Column(CHAR(5), primary_key=True, server_default=text("''"))
    County2 = Column(CHAR(20))
    NomMunicipio = Column(CHAR(150))


class DataSource(Base):
    __tablename__ = 'DataSources'

    Source = Column(CHAR(10), primary_key=True, server_default=text("''"))
    SourceDesc = Column(CHAR(150))


class Definiclineascontorno(Base):
    __tablename__ = 'Definiclineascontorno'

    Map = Column(String(30), primary_key=True, nullable=False, server_default=text("''"))
    StationGroup = Column(String(20), primary_key=True, nullable=False, server_default=text("''"))
    Variable = Column(String(15), primary_key=True, nullable=False, server_default=text("''"))
    period = Column(String(15), primary_key=True, nullable=False, server_default=text("''"))
    maptype = Column(String(15))
    Colors = Column(String(15))
    Resolucjpg = Column(Integer)
    Header1 = Column(String(150))
    Header2 = Column(String(150))
    FormatoGrados = Column(Integer)
    TamEtiq = Column(String(10))
    TamEncab = Column(String(10))
    TamAnotac = Column(String(10))
    CeldaMedios = Column(String(5))
    LineasInter = Column(String(10))
    LineasEstado = Column(String(10))
    LineasRios = Column(String(10))
    ColorRivers = Column(String(12))
    ColorSea = Column(String(12))
    CeldaSuperf = Column(String(5))
    SuperfImagen = Column(String(5))
    RegularizNiv = Column(String(5))
    SeparacAnotac = Column(String(12))
    TamLinAnotac = Column(String(12))
    ColorLinAnot = Column(String(12))
    TamLinComun = Column(String(12))
    ColorLinComun = Column(String(12))
    IntervAnotac = Column(String(10))
    IntervComun = Column(String(10))
    typevalue = Column(String(15))
    TrazoEjes = Column(String(30))
    LineaTrazo = Column(String(10))
    DatosEncab1 = Column(String(30))
    DatosEncab2 = Column(String(30))
    AngleProj = Column(String(10))
    HeightProj = Column(String(10))
    UbicGeograf = Column(String(30))
    Portrait = Column(CHAR(1))
    BegEndInterv = Column(String(20))
    BaseWidth = Column(String(10))
    PorcAcept = Column(Float(asdecimal=True))
    FormatAutom = Column(CHAR(1))
    NombreHtm = Column(String(250))
    DescripHtm = Column(Text)
    WithRivers = Column(CHAR(1))


class DisponibDD(Base):
    __tablename__ = 'DisponibDD'

    Station = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    Variable = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    Ndatos = Column(Integer)
    BegDate = Column(DateTime)
    EndDate = Column(DateTime)
    Porcen1 = Column(Float(asdecimal=True))
    Ndatos2 = Column(Integer)
    MedDate = Column(DateTime)
    Porcen2 = Column(Float(asdecimal=True))


class Estacautoma(Base):
    __tablename__ = 'Estacautoma'

    SatelliteID = Column(CHAR(8), primary_key=True, server_default=text("''"))
    Name = Column(CHAR(15))
    Namee = Column(CHAR(50))
    Station = Column(CHAR(20))
    Management = Column(CHAR(10))
    Tipo = Column(CHAR(25))
    Code = Column(CHAR(4))
    State = Column(CHAR(5))
    State2 = Column(CHAR(20))
    Regional = Column(CHAR(50))
    Latitud = Column(CHAR(9))
    Longitud = Column(CHAR(10))
    Altitud = Column(CHAR(5))
    TimeTransm = Column(CHAR(8))
    Image = Column(CHAR(80))
    NombreHtml = Column(CHAR(80))
    Genera = Column(CHAR(2))
    DayLigthTime = Column(CHAR(2))
    HoursToUTC = Column(Integer)
    DTBegDate = Column(DateTime)
    DTEndDate = Column(DateTime)


class Ftpbitacproc(Base):
    __tablename__ = 'Ftpbitacproc'

    Filee = Column(CHAR(250), primary_key=True, server_default=text("''"))
    Datee = Column(DateTime)


class Hydrregion(Base):
    __tablename__ = 'Hydrregions'

    Reghidr = Column(CHAR(5), primary_key=True, server_default=text("''"))
    RegHidr2 = Column(CHAR(20))
    NomRegHidr = Column(CHAR(150))


class Isolinbitac(Base):
    __tablename__ = 'Isolinbitac'

    Opcion = Column(CHAR(60), primary_key=True, server_default=text("''"))
    DateTime_ = Column("DateTime", DateTime)
    NumRegs = Column(Integer)
    ActDate = Column(DateTime)


class Logbitacproc(Base):
    __tablename__ = 'Logbitacproc'

    Filee = Column(CHAR(250), primary_key=True, server_default=text("''"))
    Datee = Column(DateTime)


class MapasCroqui(Base):
    __tablename__ = 'MapasCroquis'

    Map = Column(CHAR(30), primary_key=True, nullable=False, server_default=text("''"))
    Variable = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    Userr = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    period = Column(CHAR(5), primary_key=True, nullable=False, server_default=text("''"))
    Interv1 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Color1 = Column(Integer, nullable=False, server_default=text("'0'"))
    Interv2 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Color2 = Column(Integer, nullable=False, server_default=text("'0'"))
    Interv3 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Color3 = Column(Integer, nullable=False, server_default=text("'0'"))
    Interv4 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Color4 = Column(Integer, nullable=False, server_default=text("'0'"))
    Interv5 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Color5 = Column(Integer, nullable=False, server_default=text("'0'"))
    Interv6 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Color6 = Column(Integer, nullable=False, server_default=text("'0'"))


class MapasGenxCoord(Base):
    __tablename__ = 'MapasGenxCoord'

    Map = Column(CHAR(30), primary_key=True, server_default=text("''"))
    Longitud1 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Latitud1 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Longitud2 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Latitud2 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    resoluc = Column(Integer, nullable=False, server_default=text("'0'"))
    costaslinea = Column(Integer, nullable=False, server_default=text("'0'"))
    costascolor = Column(Integer, nullable=False, server_default=text("'0'"))
    fronteralinea = Column(Integer, nullable=False, server_default=text("'0'"))
    fronteracolor = Column(Integer, nullable=False, server_default=text("'0'"))
    rioslinea = Column(Integer, nullable=False, server_default=text("'0'"))
    rioscolor = Column(Integer, nullable=False, server_default=text("'0'"))
    projection = Column(CHAR(10), nullable=False, server_default=text("''"))
    elipsoide = Column(CHAR(10), nullable=False, server_default=text("''"))
    lat0 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    lon0 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    xm = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    yn = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    lat1 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    lon1 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    lat2 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    lon2 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    lat3 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    lon3 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    zone = Column(Integer, nullable=False, server_default=text("'1'"))
    sur = Column(Integer, nullable=False, server_default=text("'0'"))
    x0 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    y0 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    h = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    r = Column(Float(asdecimal=True), nullable=False, server_default=text("'6350'"))
    latts = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    poligperim = Column(CHAR(30), nullable=False, server_default=text("''"))


class MapasMchxCoord(Base):
    __tablename__ = 'MapasMchxCoord'

    Map = Column(CHAR(30), primary_key=True, server_default=text("''"))
    Longitud1 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Latitud1 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Longitud2 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Latitud2 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    fronteralinea = Column(Integer, nullable=False, server_default=text("'0'"))
    fronteracolor = Column(Integer, nullable=False, server_default=text("'0'"))
    estadoslinea = Column(Integer, nullable=False, server_default=text("'0'"))
    estadoscolor = Column(Integer, nullable=False, server_default=text("'0'"))
    rioslinea = Column(Integer, nullable=False, server_default=text("'0'"))
    rioscolor = Column(Integer, nullable=False, server_default=text("'0'"))
    isolinprim = Column(Integer, nullable=False, server_default=text("'0'"))
    isolprimlinea = Column(Integer, nullable=False, server_default=text("'0'"))
    isolprimcolor = Column(Integer, nullable=False, server_default=text("'0'"))
    isolinsec = Column(Integer, nullable=False, server_default=text("'0'"))
    isolseclinea = Column(Integer, nullable=False, server_default=text("'0'"))
    isolseccolor = Column(Integer, nullable=False, server_default=text("'0'"))
    roadline = Column(Integer, nullable=False, server_default=text("'0'"))
    roadcolor = Column(Integer, nullable=False, server_default=text("'0'"))
    poblaclinea = Column(Integer, nullable=False, server_default=text("'0'"))
    poblaccolor = Column(Integer, nullable=False, server_default=text("'0'"))
    conduclinea = Column(Integer, nullable=False, server_default=text("'0'"))
    conduccolor = Column(Integer, nullable=False, server_default=text("'0'"))
    conisolineas = Column(Integer, nullable=False, server_default=text("'0'"))
    poligperim = Column(CHAR(30), nullable=False, server_default=text("''"))
    projection = Column(CHAR(10), nullable=False, server_default=text("''"))
    elipsoide = Column(CHAR(10), nullable=False, server_default=text("''"))
    lat0 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    lon0 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    xm = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    yn = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    lat1 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    lon1 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    lat2 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    lon2 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    lat3 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    lon3 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    zone = Column(Integer, nullable=False, server_default=text("'1'"))
    sur = Column(Integer, nullable=False, server_default=text("'0'"))
    x0 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    y0 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    h = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    r = Column(Float(asdecimal=True), nullable=False, server_default=text("'6350'"))
    latts = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))


class Mapaspixelgeogr(Base):
    __tablename__ = 'Mapaspixelgeogr'

    Map = Column(CHAR(30), primary_key=True, server_default=text("''"))
    Longitud1 = Column(Float(asdecimal=True))
    Latitud1 = Column(Float(asdecimal=True))
    Xp1 = Column(Float(asdecimal=True))
    Yp1 = Column(Float(asdecimal=True))
    Longitud2 = Column(Float(asdecimal=True))
    Latitud2 = Column(Float(asdecimal=True))
    Xp2 = Column(Float(asdecimal=True))
    Yp2 = Column(Float(asdecimal=True))
    namemap = Column(CHAR(250))


class Mapaspixelgeogr4(Base):
    __tablename__ = 'Mapaspixelgeogr4'

    Map = Column(CHAR(30), primary_key=True, nullable=False, server_default=text("''"))
    Longitud1 = Column(Float(asdecimal=True), primary_key=True, nullable=False, server_default=text("'0'"))
    Latitud1 = Column(Float(asdecimal=True), primary_key=True, nullable=False, server_default=text("'0'"))
    Xp1 = Column(Float(asdecimal=True))
    Yp1 = Column(Float(asdecimal=True))
    Longitud2 = Column(Float(asdecimal=True))
    Latitud2 = Column(Float(asdecimal=True))
    Xp2 = Column(Float(asdecimal=True))
    Yp2 = Column(Float(asdecimal=True))
    Longitud3 = Column(Float(asdecimal=True))
    Latitud3 = Column(Float(asdecimal=True))
    Xp3 = Column(Float(asdecimal=True))
    Yp3 = Column(Float(asdecimal=True))
    Longitud4 = Column(Float(asdecimal=True))
    Latitud4 = Column(Float(asdecimal=True))
    Xp4 = Column(Float(asdecimal=True))
    Yp4 = Column(Float(asdecimal=True))
    namemap = Column(CHAR(250))


class Mapasxcoordclr(Base):
    __tablename__ = 'Mapasxcoordclrs'

    Map = Column(CHAR(30), primary_key=True, nullable=False, server_default=text("''"))
    Variable = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    Userr = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    period = Column(CHAR(5), primary_key=True, nullable=False, server_default=text("''"))
    Interv1 = Column(Float(asdecimal=True))
    Color1 = Column(Integer)
    Rellen1 = Column(Integer)
    Interv2 = Column(Float(asdecimal=True))
    Color2 = Column(Integer)
    Rellen2 = Column(Integer)
    Interv3 = Column(Float(asdecimal=True))
    Color3 = Column(Integer)
    Rellen3 = Column(Integer)
    Interv4 = Column(Float(asdecimal=True))
    Color4 = Column(Integer)
    Rellen4 = Column(Integer)
    Interv5 = Column(Float(asdecimal=True))
    Color5 = Column(Integer)
    Rellen5 = Column(Integer)
    Interv6 = Column(Float(asdecimal=True))
    Color6 = Column(Integer)
    Rellen6 = Column(Integer)
    Units = Column(CHAR(10))
    LetPosX = Column(Float(asdecimal=True))
    LetPosY = Column(Float(asdecimal=True))
    IntInc = Column(Float(asdecimal=True))
    IncX = Column(Float(asdecimal=True))
    IncY = Column(Float(asdecimal=True))


class Mapasxcoordgeogr(Base):
    __tablename__ = 'Mapasxcoordgeogr'

    Map = Column(CHAR(30), primary_key=True, nullable=False, server_default=text("''"))
    Secuen = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    CoordX = Column(Float(asdecimal=True))
    CoordY = Column(Float(asdecimal=True))
    Indic = Column(CHAR(1))


class Mapasxcoordzona(Base):
    __tablename__ = 'Mapasxcoordzonas'

    Map = Column(CHAR(30), primary_key=True, nullable=False, server_default=text("''"))
    Secuen = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    zone = Column(CHAR(40))


class Map(Base):
    __tablename__ = 'Maps'

    Map = Column(CHAR(30), primary_key=True, server_default=text("''"))
    Ubicacion = Column(CHAR(250))


class MensajesMetar(Base):
    __tablename__ = 'MensajesMetar'

    Station = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    Datee = Column(DateTime, primary_key=True, nullable=False, server_default=text("'1901-01-01 00:00:00'"))
    Tipo = Column(CHAR(5))
    Codee = Column(CHAR(10))
    Message = Column(Text)


class MensajesSynop(Base):
    __tablename__ = 'MensajesSynop'

    Station = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    Datee = Column(DateTime, primary_key=True, nullable=False, server_default=text("'1901-01-01 00:00:00'"))
    Codee = Column(CHAR(10))
    Message = Column(Text)


class Opcionesmapasintxxnet(Base):
    __tablename__ = 'Opcionesmapasintxxnet'

    Opcion = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    Variable = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    Map = Column(CHAR(30))
    StationGroup = Column(CHAR(20))
    Name = Column(CHAR(30))
    stationtype = Column(CHAR(15))


class Opcxvariabautom(Base):
    __tablename__ = 'Opcxvariabautom'

    Opcion = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    Opcx = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    Variable = Column(CHAR(15))
    Variable2 = Column(CHAR(15))


class Recepdef(Base):
    __tablename__ = 'Recepdefs'

    Opcion = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    Name = Column(CHAR(25), primary_key=True, nullable=False, server_default=text("''"))
    StationGroup = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    Variable = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))


class Recepsdato(Base):
    __tablename__ = 'Recepsdatos'

    Opcion = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    Name = Column(CHAR(25), primary_key=True, nullable=False, server_default=text("''"))
    StationGroup = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    Variable = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    Datee = Column(DateTime, primary_key=True, nullable=False, server_default=text("'1901-01-01 00:00:00'"))
    NumEstac = Column(Integer)
    Recep09 = Column(Integer)
    Recep10 = Column(Integer)
    Recep11 = Column(Integer)
    Recep18 = Column(Integer)
    RecepSem = Column(Integer)
    RecepMes = Column(Integer)
    RecepAgno = Column(Integer)


class Recepsping(Base):
    __tablename__ = 'Recepsping'

    IPDir = Column(CHAR(120), primary_key=True, nullable=False, server_default=text("''"))
    Datee = Column(DateTime, primary_key=True, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    Med7 = Column(Float(asdecimal=True))
    Min7 = Column(Float(asdecimal=True))
    Max7 = Column(Float(asdecimal=True))
    Com7 = Column(CHAR(40))
    Med8 = Column(Float(asdecimal=True))
    Min8 = Column(Float(asdecimal=True))
    Max8 = Column(Float(asdecimal=True))
    Com8 = Column(CHAR(40))
    Med9 = Column(Float(asdecimal=True))
    Min9 = Column(Float(asdecimal=True))
    Max9 = Column(Float(asdecimal=True))
    Com9 = Column(CHAR(40))
    Med10 = Column(Float(asdecimal=True))
    Min10 = Column(Float(asdecimal=True))
    Max10 = Column(Float(asdecimal=True))
    Com10 = Column(CHAR(40))
    Med11 = Column(Float(asdecimal=True))
    Min11 = Column(Float(asdecimal=True))
    Max11 = Column(Float(asdecimal=True))
    Com11 = Column(CHAR(40))
    Med12 = Column(Float(asdecimal=True))
    Min12 = Column(Float(asdecimal=True))
    Max12 = Column(Float(asdecimal=True))
    Com12 = Column(CHAR(40))
    Med18 = Column(Float(asdecimal=True))
    Min18 = Column(Float(asdecimal=True))
    Max18 = Column(Float(asdecimal=True))
    Com18 = Column(CHAR(40))


class StationGroup(Base):
    __tablename__ = 'StationGroups'

    StationGroup = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    Secuen = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    Station = Column(CHAR(20))


class Tablaswebconst(Base):
    __tablename__ = 'Tablaswebconst'

    OpcionCons = Column(CHAR(15), primary_key=True, server_default=text("''"))
    Opcion = Column(CHAR(15))
    Variable = Column(CHAR(15))
    Description = Column(CHAR(150))
    BegnDate = Column(DateTime)
    EndDate = Column(DateTime)
    NombreHtml = Column(CHAR(40))
    WithExtremes = Column(CHAR(2))
    WithDataNumb = Column(CHAR(2))
    Dsn = Column(CHAR(15))
    DirectHtml = Column(CHAR(250))
    PriorMonth = Column(CHAR(60))
    NextMonth = Column(CHAR(60))


class Tablaswebdef(Base):
    __tablename__ = 'Tablaswebdef'

    Opcion = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    Secuen = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    StationGroup = Column(CHAR(20))
    Image = Column(CHAR(250))
    Description = Column(CHAR(150))


class TimeZone(Base):
    __tablename__ = 'TimeZones'

    TimeZone = Column(CHAR(4), primary_key=True, server_default=text("''"))
    Description = Column(CHAR(100))
    HoursToUTC = Column(Float(asdecimal=True))
    DayLigthTime = Column(Integer)


class TransfTable(Base):
    __tablename__ = 'TransfTables'

    TablaTransf = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    ValorX = Column(Float(asdecimal=True), primary_key=True, nullable=False, server_default=text("'0'"))
    ValorY = Column(Float(asdecimal=True))


class Transftp(Base):
    __tablename__ = 'Transftp'

    OpcionTrans = Column(CHAR(30), primary_key=True, server_default=text("''"))
    IPAddress = Column(CHAR(90))
    Userr = Column(CHAR(30))
    password = Column(CHAR(30))


class Transmchamch(Base):
    __tablename__ = 'Transmchamch'

    OpcionTrans = Column(CHAR(30), primary_key=True, nullable=False, server_default=text("''"))
    StationGroup = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    Secuenc = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    Variable = Column(CHAR(15))
    Tipo = Column(CHAR(2))
    Active = Column(CHAR(2))


class Unit(Base):
    __tablename__ = 'Units'

    Units = Column(CHAR(10), primary_key=True, server_default=text("''"))
    DescripcionUnidad = Column(CHAR(60))


class Valsvariabaut(Base):
    __tablename__ = 'Valsvariabaut'

    Station = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    Variable = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    Adjust1 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Adjust2 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    MaxValue = Column(Float(asdecimal=True))
    MinValue = Column(Float(asdecimal=True))
    ValorNoHayDato = Column(Float(asdecimal=True))
    CriticoArriba = Column(Float(asdecimal=True))
    CriticoAbajo = Column(Float(asdecimal=True))


class VariabDeriv2(Base):
    __tablename__ = 'VariabDeriv2'

    Station = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    Variable = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    FormCalculo = Column(Text)


class VariabDeriv3(Base):
    __tablename__ = 'VariabDeriv3'

    Station = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    Variable = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    FormCalculo = Column(Text)


class Variabautomatv(Base):
    __tablename__ = 'Variabautomatv'

    Station = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    Variable = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    period = Column(Integer)


class Variabautomaxfecha(Base):
    __tablename__ = 'Variabautomaxfecha'

    SatelliteID = Column(CHAR(8), primary_key=True, nullable=False, server_default=text("''"))
    DateTime = Column(DateTime, primary_key=True, nullable=False, server_default=text("'2001-01-01 00:00:00'"))
    Secuen = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    Area = Column(CHAR(15))
    Name = Column(CHAR(30))
    Variable = Column(CHAR(15))
    period = Column(Integer)


class Variable(Base):
    __tablename__ = 'Variables'

    Variable = Column(CHAR(15), primary_key=True, server_default=text("''"))
    ShortName = Column(CHAR(4))
    DescripVariab = Column(CHAR(150))
    TableName = Column(CHAR(15))
    Units = Column(CHAR(10))
    TypeDDoDE = Column(CHAR(2))
    TipAcum = Column(CHAR(4))
    NDecim = Column(Integer)
    CalcxGrp = Column(CHAR(8))
    CalcDTaD = Column(CHAR(8))


class Variablestransf(Base):
    __tablename__ = 'Variablestransf'

    Station = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    Variable = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    BegnDate = Column(DateTime, primary_key=True, nullable=False, server_default=text("'1901-01-01 00:00:00'"))
    Adjust1 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Adjust2 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    VariabTransf1 = Column(CHAR(20))
    TablaTransf1 = Column(CHAR(15))
    VariabTransf2 = Column(CHAR(20))
    TablaTransf2 = Column(CHAR(15))
    VariabTransf3 = Column(CHAR(20))
    TablaTransf3 = Column(CHAR(15))
    VariabTransf4 = Column(CHAR(20))
    TablaTransf4 = Column(CHAR(15))


class VerifCerca(Base):
    __tablename__ = 'VerifCerca'

    Station = Column(CHAR(20), primary_key=True, nullable=False)
    Variable = Column(CHAR(15), primary_key=True, nullable=False)
    Distance = Column(Float(asdecimal=True))
    difaltura = Column(Float(asdecimal=True))
    StationGroup = Column(CHAR(20))
    variacion = Column(Float(asdecimal=True))
    intervmin = Column(Integer)


class Verific(Base):
    __tablename__ = 'Verific'

    Variable = Column(CHAR(15), primary_key=True, nullable=False)
    Data = Column(CHAR(1), primary_key=True, nullable=False)
    Secuen = Column(Integer, primary_key=True, nullable=False)
    Tipo = Column(CHAR(1))
    Verif = Column(Text)


class Webbitacoraproc(Base):
    __tablename__ = 'Webbitacoraproc'

    Tally = Column(Integer, primary_key=True)
    program = Column(CHAR(20))
    Userr = Column(CHAR(50))
    proctype = Column(CHAR(20))
    OpcionProc = Column(CHAR(15))
    DateTime = Column(DateTime)


class Webcontadore(Base):
    __tablename__ = 'Webcontadores'

    program = Column(CHAR(30), primary_key=True, nullable=False, server_default=text("''"))
    Userr = Column(CHAR(50), primary_key=True, nullable=False, server_default=text("''"))
    proctype = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    OpcionProc = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    Tally = Column(Integer)


class ZonasArea(Base):
    __tablename__ = 'ZonasAreas'

    zone = Column(CHAR(50), primary_key=True)
    Area = Column(Float(asdecimal=True))


class Estacionesinstrum(Base):
    __tablename__ = 'estacionesinstrum'

    Station = Column(CHAR(20), primary_key=True, nullable=False)
    Variable = Column(CHAR(15), primary_key=True, nullable=False)
    BeginDate = Column(DateTime, primary_key=True, nullable=False)
    elevation = Column(Float(asdecimal=True))
    tipo1 = Column(CHAR(15))
    Descrip = Column(CHAR(120))


class Mapasbycoord(Base):
    __tablename__ = 'mapasbycoord'

    Map = Column(CHAR(30), primary_key=True, nullable=False, server_default=text("''"))
    Secuen = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    zone = Column(CHAR(20))
    CoordX = Column(Float(asdecimal=True))
    CoordY = Column(Float(asdecimal=True))
    Indic = Column(CHAR(1))
    HeightLetter = Column(Float(asdecimal=True))
    Descrip = Column(CHAR(40))
    Angle = Column(Float(asdecimal=True))


class Mapsgroup(Base):
    __tablename__ = 'mapsgroups'

    Map = Column(CHAR(30), primary_key=True, nullable=False, server_default=text("''"))
    Group = Column(CHAR(15), nullable=False, server_default=text("''"))
    Variable = Column(CHAR(15), primary_key=True, nullable=False, server_default=text("''"))
    Userr = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    period = Column(CHAR(5), primary_key=True, nullable=False, server_default=text("''"))
    Interv1 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Color1 = Column(Integer, nullable=False, server_default=text("'0'"))
    Interv2 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Color2 = Column(Integer, nullable=False, server_default=text("'0'"))
    Interv3 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Color3 = Column(Integer, nullable=False, server_default=text("'0'"))
    Interv4 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Color4 = Column(Integer, nullable=False, server_default=text("'0'"))
    Interv5 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Color5 = Column(Integer, nullable=False, server_default=text("'0'"))
    Interv6 = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    Color6 = Column(Integer, nullable=False, server_default=text("'0'"))


class Mapsstation(Base):
    __tablename__ = 'mapsstations'

    Map = Column(CHAR(30), primary_key=True, nullable=False, server_default=text("''"))
    Station = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    Xp = Column(Float(asdecimal=True))
    Yp = Column(Float(asdecimal=True))
    namemap = Column(CHAR(250))


class Metadatastation(Base):
    __tablename__ = 'metadatastations'

    Station = Column(CHAR(20), primary_key=True, nullable=False, server_default=text("''"))
    MetaDato = Column(CHAR(30), primary_key=True, nullable=False, server_default=text("''"))
    Datee = Column(Date, primary_key=True, nullable=False)
    Description = Column(CHAR(255))


class RegManager(Base):
    __tablename__ = 'regManager'

    RegManagmt = Column(CHAR(5), primary_key=True, server_default=text("''"))
    GerenReg2 = Column(CHAR(20))
    Nomgerencia = Column(CHAR(150))


class State(Base):
    __tablename__ = 'states'

    State = Column(CHAR(5), primary_key=True, server_default=text("''"))
    State2 = Column(CHAR(20))
    StateName = Column(CHAR(150))


class Station(Base):
    __tablename__ = 'stations'

    Station = Column(CHAR(20), primary_key=True, server_default=text("''"))
    StationName = Column(CHAR(150))
    StationName2 = Column(CHAR(50))
    TimeZone = Column(CHAR(4))
    Longitud = Column(Integer)
    Latitud = Column(Integer)
    Altitud = Column(Float(asdecimal=True))
    Longitud2 = Column(Float(asdecimal=True))
    Latitud2 = Column(Float(asdecimal=True))
    LongitudGMS = Column(CHAR(15))
    LatitudGMS = Column(CHAR(15))
    State = Column(CHAR(5))
    RegManagmt = Column(CHAR(5))
    Basin = Column(CHAR(5))
    SubBasin = Column(CHAR(5))
    Regopera = Column(CHAR(5))
    Reghidr = Column(CHAR(5))
    RH = Column(CHAR(2))
    County = Column(CHAR(5))
    CodB = Column(Integer)
    CodG = Column(CHAR(5))
    CodCB = Column(CHAR(5))
    CodPB = Column(CHAR(6))
    CodE = Column(CHAR(5))
    CodCL = Column(CHAR(5))
    CodHG = Column(CHAR(5))
    CodPG = Column(CHAR(5))
    CodNw = Column(CHAR(5))
    Cod1 = Column(CHAR(5))
    Cod2 = Column(CHAR(5))
    Cod3 = Column(CHAR(5))
    NamoElev = Column(Float(asdecimal=True))
    NamoAlmac = Column(Float(asdecimal=True))
    NameElev = Column(Float(asdecimal=True))
    NameAlmac = Column(Float(asdecimal=True))
    VerteElev = Column(Float(asdecimal=True))
    VerteAlmac = Column(Float(asdecimal=True))
    VertlElev = Column(Float(asdecimal=True))
    VertlAlmac = Column(Float(asdecimal=True))
    CapMuertaElev = Column(Float(asdecimal=True))
    CapMuertaAlmac = Column(Float(asdecimal=True))
    CapUtilElev = Column(Float(asdecimal=True))
    CapUtilAlmac = Column(Float(asdecimal=True))
    AlmacConserv = Column(Float(asdecimal=True))
    Clav1fil = Column(CHAR(5))
    Clav2fil = Column(CHAR(5))
    Clav3fil = Column(CHAR(5))
    EscCrit = Column(Float(asdecimal=True))
    EscMinimoRang = Column(Float(asdecimal=True))
    EscMaximoRang = Column(Float(asdecimal=True))
    GastCrit = Column(Float(asdecimal=True))
    GastMinimoRang = Column(Float(asdecimal=True))
    GastMaximoRang = Column(Float(asdecimal=True))
    Corriente = Column(CHAR(20))
    Distance = Column(Float(asdecimal=True))
    Infraestruc = Column(CHAR(20))
    Tipo = Column(CHAR(20))
    usee = Column(CHAR(15))


class Subbasin(Base):
    __tablename__ = 'subbasins'

    SubBasin = Column(CHAR(5), primary_key=True, server_default=text("''"))
    SubBasin2 = Column(CHAR(20))
    NomSubcuenca = Column(CHAR(150))


class Synopcrexdato(Base):
    __tablename__ = 'synopcrexdatos'

    elemento = Column(CHAR(6), primary_key=True)
    Units = Column(CHAR(20), nullable=False)
    Width = Column(Integer, nullable=False, server_default=text("'1'"))
    escala = Column(Integer, nullable=False, server_default=text("'0'"))
    Description = Column(CHAR(120), nullable=False)


class Synopcrexplant(Base):
    __tablename__ = 'synopcrexplant'

    template = Column(CHAR(6), primary_key=True, nullable=False)
    Secuen = Column(Integer, primary_key=True, nullable=False)
    elemento = Column(CHAR(6), nullable=False)


class TipoEstacionVariable(Base):
    __tablename__ = 'tipoEstacionVariable'

    stationtype = Column(CHAR(15), primary_key=True, nullable=False)
    Secuen = Column(Integer, primary_key=True, nullable=False)
    Variable = Column(CHAR(15))


class Typeuser(Base):
    __tablename__ = 'typeusers'

    TipoUsuario = Column(Integer, primary_key=True, server_default=text("'0'"))
    TypeName = Column(CHAR(50))
    DescripTipo = Column(CHAR(150))


class User(Base):
    __tablename__ = 'users'

    Userr = Column(CHAR(20), primary_key=True, server_default=text("''"))
    Name = Column(CHAR(60))
    password = Column(CHAR(30))
    TipoUsuario = Column(Integer)
    StationGroup = Column(CHAR(20))


class Validdatum(Base):
    __tablename__ = 'validdata'

    Station = Column(CHAR(20), primary_key=True, nullable=False)
    Variable = Column(CHAR(15), primary_key=True, nullable=False)
    Data = Column(CHAR(1), primary_key=True, nullable=False)
    Datee = Column(Date, primary_key=True, nullable=False, server_default=text("'1901-01-01'"))
    EndDate = Column(Date)
    IniHour = Column(Time)
    EndHour = Column(Time)
    MinValue = Column(Float(asdecimal=True))
    alert1min = Column(Float(asdecimal=True))
    alert2min = Column(Float(asdecimal=True))
    alert2max = Column(Float(asdecimal=True))
    alert1max = Column(Float(asdecimal=True))
    MaxValue = Column(Float(asdecimal=True))
    Variac = Column(Float(asdecimal=True))
    Minutes = Column(Integer)
