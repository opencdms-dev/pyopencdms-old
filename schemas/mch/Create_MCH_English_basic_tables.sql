CREATE TABLE Codes(
    Codee char(10) NOT NULL default "",
    Message char(150),
    PRIMARY KEY  (Codee)
    ) ENGINE=MyISAM;
CREATE TABLE Basins (
    Basin char(5) NOT NULL default "",
    Basin2 char(20),
    BasinName char(150),
    PRIMARY KEY  (Basin)
    ) ENGINE=MyISAM;
CREATE TABLE Definiclineascontorno (
    Map varchar(30) NOT NULL default "",
    StationGroup varchar(20) NOT NULL default "",
    `Variable` varchar(15) NOT NULL default "",
    period varchar(15) NOT NULL default "",
    maptype varchar(15),
    Colors varchar(15),
    Resolucjpg int(11),
    Header1 varchar(150),
    Header2 varchar(150),
    FormatoGrados int(11),
    TamEtiq varchar(10),
    TamEncab varchar(10),
    TamAnotac varchar(10),
    CeldaMedios varchar(5),
    LineasInter varchar(10),
    LineasEstado varchar(10),
    LineasRios varchar(10),
    ColorRivers varchar(12),
    ColorSea varchar(12),
    CeldaSuperf varchar(5),
    SuperfImagen varchar(5),
    RegularizNiv varchar(5),
    SeparacAnotac varchar(12),
    TamLinAnotac varchar(12),
    ColorLinAnot varchar(12),
    TamLinComun varchar(12),
    ColorLinComun varchar(12),
    IntervAnotac varchar(10),
    IntervComun varchar(10),
    typevalue varchar(15),
    TrazoEjes varchar(30),
    LineaTrazo varchar(10),
    DatosEncab1 varchar(30),
    DatosEncab2 varchar(30),
    AngleProj varchar(10),
    HeightProj varchar(10),
    UbicGeograf varchar(30),
    Portrait char(1),
    BegEndInterv varchar(20),
    BaseWidth varchar(10),
    PorcAcept double,
    FormatAutom char(1),
    NombreHtm varchar(250),
    DescripHtm text,
    WithRivers char(1),
    PRIMARY KEY  (Map,StationGroup,`Variable`,period)
    ) ENGINE=MyISAM;
CREATE TABLE DisponibDD (
    Station char(20) NOT NULL default "",
    `Variable` char(15) NOT NULL default "",
    Ndatos int(11),
    BegDate datetime,
    EndDate datetime,
    Porcen1 double,
    Ndatos2 int(11),
    MedDate datetime,
    Porcen2 double,
    PRIMARY KEY  (Station,`Variable`)
    ) ENGINE=MyISAM;
CREATE TABLE Estacautoma (
    SatelliteID char(8) NOT NULL default "",
    Name char(15),
    Namee char(50),
    Station char(20),
    Management char(10),
    Tipo char(25),
    Code char(4),
    State char(5),
    State2 char(20),
    Regional char(50),
    Latitud char(9),
    Longitud char(10),
    Altitud char(5),
    TimeTransm char(8),
    Image char(80),
    NombreHtml char(80),
    Genera char(2),
    DayLigthTime char(2),
    HoursToUTC int(11),
    DTBegDate datetime,
    DTEndDate datetime,
    PRIMARY KEY  (SatelliteID)
    ) ENGINE=MyISAM;
CREATE TABLE stations (
    Station char(20) NOT NULL default "",
    StationName char(150),
    StationName2 char(50),
    TimeZone char(4),
    Longitud int(11),
    Latitud int(11),
    Altitud double,
    Longitud2 double,
    Latitud2 double,
    LongitudGMS char(15),
    LatitudGMS char(15),
    State char(5),
    RegManagmt char(5),
    Basin char(5),
    SubBasin char(5),
    Regopera char(5),
    Reghidr char(5),
    RH char(2),
    County char(5),
    CodB int(11),
    CodG char(5),
    CodCB char(5),
    CodPB char(6),
    CodE char(5),
    CodCL char(5),
    CodHG char(5),
    CodPG char(5),
    CodNw char(5),
    Cod1 char(5),
    Cod2 char(5),
    Cod3 char(5),
    NamoElev double,
    NamoAlmac double,
    NameElev double,
    NameAlmac double,
    VerteElev double,
    VerteAlmac double,
    VertlElev double,
    VertlAlmac double,
    CapMuertaElev double,
    CapMuertaAlmac double,
    CapUtilElev double,
    CapUtilAlmac double,
    AlmacConserv double,
    Clav1fil char(5),
    Clav2fil char(5),
    Clav3fil char(5),
    EscCrit double,
    EscMinimoRang double,
    EscMaximoRang double,
    GastCrit double,
    GastMinimoRang double,
    GastMaximoRang double,
    Corriente char(20),
    Distance double,
    Infraestruc char(20),
    Tipo char(20),
    usee char(15),
    PRIMARY KEY  (Station)
    ) ENGINE=MyISAM;
CREATE TABLE estacionesinstrum (
    Station char(20) NOT NULL,
    `Variable` char(15) NOT NULL,
    BeginDate datetime NOT NULL,
    elevation double,
    tipo1 char(15),
    Descrip char(120),
    PRIMARY KEY  (Station,`Variable`,BeginDate)
    ) ENGINE=MyISAM;
CREATE TABLE metadatastations (
    Station char(20) NOT NULL default "",
    MetaDato char(30) NOT NULL default "",
    Datee date NOT NULL,
    Description char(255),
    PRIMARY KEY  (Station,MetaDato,Datee)
    ) ENGINE=MyISAM;
CREATE TABLE states (
    State char(5) NOT NULL default "",
    State2 char(20),
    StateName char(150),
    PRIMARY KEY  (State)
    ) ENGINE=MyISAM;
CREATE TABLE Ftpbitacproc (
    Filee char(250) NOT NULL default "",
    Datee datetime,
    PRIMARY KEY  (Filee)
    ) ENGINE=MyISAM;
CREATE TABLE regManager (
    RegManagmt char(5) NOT NULL default "",
    GerenReg2 char(20),
    Nomgerencia char(150),
    PRIMARY KEY  (RegManagmt)
    ) ENGINE=MyISAM;
CREATE TABLE StationGroups (
    StationGroup char(20) NOT NULL default "",
    Secuen int(11) NOT NULL default "0",
    Station char(20),PRIMARY KEY  (StationGroup,Secuen)
    ) ENGINE=MyISAM;
CREATE TABLE TimeZones (
    TimeZone char(4) NOT NULL default "",
    Description char(100),
    HoursToUTC double,
    DayLigthTime int(11),
    PRIMARY KEY  (TimeZone)
    ) ENGINE=MyISAM;
CREATE TABLE Isolinbitac (
    Opcion char(60) NOT NULL default "",
    DateTime datetime,
    NumRegs int(11),
    ActDate datetime,
    PRIMARY KEY  (Opcion)
    ) ENGINE=MyISAM;
CREATE TABLE Logbitacproc (
    Filee char(250) NOT NULL default "",
    Datee datetime,
    PRIMARY KEY  (Filee)
    ) ENGINE=MyISAM;
CREATE TABLE Maps (
    Map char(30) NOT NULL default "",
    Ubicacion char(250),
    PRIMARY KEY  (Map)
    ) ENGINE=MyISAM;
CREATE TABLE MapasCroquis (
    Map char(30) NOT NULL default "",
    `Variable` char(15) NOT NULL default "",
    Userr char(20) NOT NULL default "",
    period char(5) NOT NULL default "",
    Interv1 double NOT NULL default "0",
    Color1 int(11) NOT NULL default "0",
    Interv2 double NOT NULL default "0",
    Color2 int(11) NOT NULL default "0",
    Interv3 double NOT NULL default "0",
    Color3 int(11) NOT NULL default "0",
    Interv4 double NOT NULL default "0",
    Color4 int(11) NOT NULL default "0",
    Interv5 double NOT NULL default "0",
    Color5 int(11) NOT NULL default "0",
    Interv6 double NOT NULL default "0",
    Color6 int(11) NOT NULL default "0",
    PRIMARY KEY  (Map,`Variable`,Userr,period)
    ) ENGINE=MyISAM;
CREATE TABLE mapsstations (
    Map char(30) NOT NULL default "",
    Station char(20) NOT NULL default "",
    Xp double,
    Yp double,
    namemap char(250),
    PRIMARY KEY  (Map,Station)
    ) ENGINE=MyISAM;
CREATE TABLE MapasGenxCoord (
    Map char(30) NOT NULL default "",
    Longitud1 double NOT NULL default "0",
    Latitud1 double NOT NULL default "0",
    Longitud2 double NOT NULL default "0",
    Latitud2 double NOT NULL default "0",
    resoluc int(11) NOT NULL default "0",
    costaslinea int(11) NOT NULL default "0",
    costascolor int(11) NOT NULL default "0",
    fronteralinea int(11) NOT NULL default "0",
    fronteracolor int(11) NOT NULL default "0",
    rioslinea int(11) NOT NULL default "0",
    rioscolor int(11) NOT NULL default "0",
    projection char(10) NOT NULL default "",
    elipsoide char(10) NOT NULL default "",
    lat0 double NOT NULL default "0",
    lon0 double NOT NULL default "0",
    xm double NOT NULL default "0",
    yn double NOT NULL default "0",
    lat1 double NOT NULL default "0",
    lon1 double NOT NULL default "0",
    lat2 double NOT NULL default "0",
    lon2 double NOT NULL default "0",
    lat3 double NOT NULL default "0",
    lon3 double NOT NULL default "0",
    zone int(11) NOT NULL default "1",
    sur int(11) NOT NULL default "0",
    x0 double NOT NULL default "0",
    y0 double NOT NULL default "0",
    h double NOT NULL default "0",
    r double NOT NULL default "6350",
    latts double NOT NULL default "0",
    poligperim char(30) NOT NULL default "",
    PRIMARY KEY  (Map)
    ) ENGINE=MyISAM;
CREATE TABLE mapsgroups (
    Map char(30) NOT NULL default "",
    `Group` char(15) NOT NULL default "",
    `Variable` char(15) NOT NULL default "",
    Userr char(20) NOT NULL default "",
    period char(5) NOT NULL default "",
    Interv1 double NOT NULL default "0",
    Color1 int(11) NOT NULL default "0",
    Interv2 double NOT NULL default "0",
    Color2 int(11) NOT NULL default "0",
    Interv3 double NOT NULL default "0",
    Color3 int(11) NOT NULL default "0",
    Interv4 double NOT NULL default "0",
    Color4 int(11) NOT NULL default "0",
    Interv5 double NOT NULL default "0",
    Color5 int(11) NOT NULL default "0",
    Interv6 double NOT NULL default "0",
    Color6 int(11) NOT NULL default "0",
    PRIMARY KEY  (Map,`Variable`,Userr,period)
    ) ENGINE=MyISAM;
CREATE TABLE MapasMchxCoord (
    Map char(30) NOT NULL default "",
    Longitud1 double NOT NULL default "0",
    Latitud1 double NOT NULL default "0",
    Longitud2 double NOT NULL default "0",
    Latitud2 double NOT NULL default "0",
    fronteralinea int(11) NOT NULL default "0",
    fronteracolor int(11) NOT NULL default "0",
    estadoslinea int(11) NOT NULL default "0",
    estadoscolor int(11) NOT NULL default "0",
    rioslinea int(11) NOT NULL default "0",
    rioscolor int(11) NOT NULL default "0",
    isolinprim int(11) NOT NULL default "0",
    isolprimlinea int(11) NOT NULL default "0",
    isolprimcolor int(11) NOT NULL default "0",
    isolinsec int(11) NOT NULL default "0",
    isolseclinea int(11) NOT NULL default "0",
    isolseccolor int(11) NOT NULL default "0",
    roadline int(11) NOT NULL default "0",
    roadcolor int(11) NOT NULL default "0",
    poblaclinea int(11) NOT NULL default "0",
    poblaccolor int(11) NOT NULL default "0",
    conduclinea int(11) NOT NULL default "0",
    conduccolor int(11) NOT NULL default "0",
    conisolineas int(11) NOT NULL default "0",
    poligperim char(30) NOT NULL default "",
    projection char(10) NOT NULL default "",
    elipsoide char(10) NOT NULL default "",
    lat0 double NOT NULL default "0",
    lon0 double NOT NULL default "0",
    xm double NOT NULL default "0",
    yn double NOT NULL default "0",
    lat1 double NOT NULL default "0",
    lon1 double NOT NULL default "0",
    lat2 double NOT NULL default "0",
    lon2 double NOT NULL default "0",
    lat3 double NOT NULL default "0",
    lon3 double NOT NULL default "0",
    zone int(11) NOT NULL default "1",
    sur int(11) NOT NULL default "0",
    x0 double NOT NULL default "0",
    y0 double NOT NULL default "0",
    h double NOT NULL default "0",
    r double NOT NULL default "6350",
    latts double NOT NULL default "0",
    PRIMARY KEY  (Map)
    ) ENGINE=MyISAM;
CREATE TABLE Mapaspixelgeogr (
    Map char(30) NOT NULL default "",
    Longitud1 double,
    Latitud1 double,
    Xp1 double,
    Yp1 double,
    Longitud2 double,
    Latitud2 double,
    Xp2 double,
    Yp2 double,
    namemap char(250),
    PRIMARY KEY  (Map)
    ) ENGINE=MyISAM;
CREATE TABLE Mapaspixelgeogr4 (
    Map char(30) NOT NULL default "",
    Longitud1 double NOT NULL default "0",
    Latitud1 double NOT NULL default "0",
    Xp1 double,
    Yp1 double,
    Longitud2 double,
    Latitud2 double,
    Xp2 double,
    Yp2 double,
    Longitud3 double,
    Latitud3 double,
    Xp3 double,
    Yp3 double,
    Longitud4 double,
    Latitud4 double,
    Xp4 double,
    Yp4 double,
    namemap char(250),
    PRIMARY KEY  (Map,Longitud1,Latitud1)
    ) ENGINE=MyISAM;
CREATE TABLE mapasbycoord (
    Map char(30) NOT NULL default "",
    Secuen int(11) NOT NULL default "0",
    zone char(20),
    CoordX double,
    CoordY double,
    Indic char(1),
    HeightLetter double,
    Descrip char(40),
    Angle double,
    PRIMARY KEY  (Map,Secuen)
    ) ENGINE=MyISAM;
CREATE TABLE Mapasxcoordclrs (
    Map char(30) NOT NULL default "",
    `Variable` char(15) NOT NULL default "",
    Userr char(20) NOT NULL default "",
    period char(5) NOT NULL default "",
    Interv1 double,
    Color1 int(11),
    Rellen1 int(11),
    Interv2 double,
    Color2 int(11),
    Rellen2 int(11),
    Interv3 double,
    Color3 int(11),
    Rellen3 int(11),
    Interv4 double,
    Color4 int(11),
    Rellen4 int(11),
    Interv5 double,
    Color5 int(11),
    Rellen5 int(11),
    Interv6 double,
    Color6 int(11),
    Rellen6 int(11),
    Units char(10),
    LetPosX double,
    LetPosY double,
    IntInc double,
    IncX double,
    IncY double,
    PRIMARY KEY  (Map,`Variable`,Userr,period)
    ) ENGINE=MyISAM;
CREATE TABLE Mapasxcoordgeogr (
    Map char(30) NOT NULL default "",
    Secuen int(11) NOT NULL default "0",
    CoordX double,
    CoordY double,
    Indic char(1),
    PRIMARY KEY  (Map,Secuen)
    ) ENGINE=MyISAM;
CREATE TABLE Mapasxcoordzonas (
    Map char(30) NOT NULL default "",
    Secuen int(11) NOT NULL default "0",
    zone char(40),
    PRIMARY KEY  (Map,Secuen)
    ) ENGINE=MyISAM;
CREATE TABLE MensajesMetar (
    Station char(20) NOT NULL default "",
    Datee datetime NOT NULL default "1901-01-01 00:00:00",
    Tipo char(5),
    Codee char(10),
    Message text,
    PRIMARY KEY  (Station,Datee)
    ) ENGINE=MyISAM;
CREATE TABLE MensajesSynop (
    Station char(20) NOT NULL default "",
    Datee datetime NOT NULL default "1901-01-01 00:00:00",
    Codee char(10),
    Message text,
    PRIMARY KEY  (Station,Datee)
    ) ENGINE=MyISAM;
CREATE TABLE Counties (
    County char(5) NOT NULL default "",
    County2 char(20),
    NomMunicipio char(150),
    PRIMARY KEY  (County)
    ) ENGINE=MyISAM;
CREATE TABLE Opcionesmapasintxxnet (
    Opcion char(15) NOT NULL default "",
    `Variable` char(15) NOT NULL default "",
    Map char(30),
    StationGroup char(20),
    Name char(30),
    stationtype char(15),
    PRIMARY KEY  (Opcion,`Variable`)
    ) ENGINE=MyISAM;
CREATE TABLE Opcxvariabautom (
    Opcion char(15) NOT NULL default "",
    Opcx int(11) NOT NULL default "0",
    `Variable` char(15),
    Variable2 char(15),
    PRIMARY KEY  (Opcion,Opcx)
    ) ENGINE=MyISAM;
CREATE TABLE DataSources (
    Source char(10) NOT NULL default "",
    SourceDesc char(150),
    PRIMARY KEY  (Source)
    ) ENGINE=MyISAM;
CREATE TABLE Recepdefs (
    Opcion char(15) NOT NULL default "",
    Name char(25) NOT NULL default "",
    StationGroup char(20) NOT NULL default "",
    `Variable` char(15) NOT NULL default "",
    PRIMARY KEY  (Opcion,Name,StationGroup,`Variable`)
    ) ENGINE=MyISAM;
CREATE TABLE Recepsdatos (
    Opcion char(15) NOT NULL default "",
    Name char(25) NOT NULL default "",
    StationGroup char(20) NOT NULL default "",
    `Variable` char(15) NOT NULL default "",
    Datee datetime NOT NULL default "1901-01-01 00:00:00",
    NumEstac int(11),
    Recep09 int(11),
    Recep10 int(11),
    Recep11 int(11),
    Recep18 int(11),
    RecepSem int(11),
    RecepMes int(11),
    RecepAgno int(11),
    PRIMARY KEY  (Opcion,Name,StationGroup,`Variable`,Datee)
    ) ENGINE=MyISAM;
CREATE TABLE Recepsping (
    IPDir char(120) NOT NULL default "",
    Datee datetime NOT NULL default "0000-00-00 00:00:00",
    Med7 double,
    Min7 double,
    Max7 double,
    Com7 char(40),
    Med8 double,
    Min8 double,
    Max8 double,
    Com8 char(40),
    Med9 double,
    Min9 double,
    Max9 double,
    Com9 char(40),
    Med10 double,
    Min10 double,
    Max10 double,
    Com10 char(40),
    Med11 double,
    Min11 double,
    Max11 double,
    Com11 char(40),
    Med12 double,
    Min12 double,
    Max12 double,
    Com12 char(40),
    Med18 double,
    Min18 double,
    Max18 double,
    Com18 char(40),
    PRIMARY KEY  (IPDir,Datee)
    ) ENGINE=MyISAM;
CREATE TABLE Hydrregions (
    Reghidr char(5) NOT NULL default "",
    RegHidr2 char(20),
    NomRegHidr char(150),
    PRIMARY KEY  (Reghidr)
    ) ENGINE=MyISAM;
CREATE TABLE subbasins (
    SubBasin char(5) NOT NULL default "",
    SubBasin2 char(20),
    NomSubcuenca char(150),
    PRIMARY KEY  (SubBasin)
    ) ENGINE=MyISAM;
CREATE TABLE synopcrexdatos (
    elemento char(6) NOT NULL,
    Units char(20) NOT NULL,
    Width int(11) NOT NULL default "1",
    escala int(11) NOT NULL default "0",
    Description char(120) NOT NULL,
    PRIMARY KEY  (elemento)
    ) ENGINE=MyISAM;
CREATE TABLE synopcrexplant (
    template char(6) NOT NULL,
    Secuen int(11) NOT NULL,
    elemento char(6) NOT NULL,
    PRIMARY KEY  (template,Secuen)
    ) ENGINE=MyISAM;
CREATE TABLE TransfTables (
    TablaTransf char(15) NOT NULL default "",
    ValorX double NOT NULL default "0",
    ValorY double,
    PRIMARY KEY  (TablaTransf,ValorX)
    ) ENGINE=MyISAM;
CREATE TABLE Tablaswebconst (
    OpcionCons char(15) NOT NULL default "",
    Opcion char(15),
    `Variable` char(15),
    Description char(150),
    BegnDate datetime,
    EndDate datetime,
    NombreHtml char(40),
    WithExtremes char(2),
    WithDataNumb char(2),
    Dsn char(15),
    DirectHtml char(250),
    PriorMonth char(60),
    NextMonth char(60),
    PRIMARY KEY  (OpcionCons)
    ) ENGINE=MyISAM;
CREATE TABLE Tablaswebdef (
    Opcion char(15) NOT NULL default "",
    Secuen int(11) NOT NULL default "0",
    StationGroup char(20),
    Image char(250),
    Description char(150),
    PRIMARY KEY  (Opcion,Secuen)
    ) ENGINE=MyISAM;
CREATE TABLE tipoEstacionVariable (
    stationtype char(15) NOT NULL,
    Secuen int(11) NOT NULL,
    `Variable` char(15),
    PRIMARY KEY  (stationtype,Secuen)
    ) ENGINE=MyISAM;
CREATE TABLE Transftp (
    OpcionTrans char(30) NOT NULL default "",
    IPAddress char(90),
    Userr char(30),
    password char(30),
    PRIMARY KEY  (OpcionTrans)
    ) ENGINE=MyISAM;
CREATE TABLE Transmchamch (
    OpcionTrans char(30) NOT NULL default "",
    StationGroup char(20) NOT NULL default "",
    Secuenc int(11) NOT NULL default "0",
    `Variable` char(15),
    Tipo char(2),
    Active char(2),
    PRIMARY KEY  (OpcionTrans,StationGroup,Secuenc)
    ) ENGINE=MyISAM;
CREATE TABLE Units (
    Units char(10) NOT NULL default "",
    DescripcionUnidad char(60),
    PRIMARY KEY  (Units)
    ) ENGINE=MyISAM;
CREATE TABLE users (
    Userr char(20) NOT NULL default "",
    Name char(60),
    password char(30),
    TipoUsuario int(11),
    StationGroup char(20),
    PRIMARY KEY  (Userr)
    ) ENGINE=MyISAM;
CREATE TABLE typeusers (
    TipoUsuario int(11) NOT NULL default "0",
    TypeName char(50),
    DescripTipo char(150),
    PRIMARY KEY  (TipoUsuario)
    ) ENGINE=MyISAM;
CREATE TABLE validdata (
    Station char(20) NOT NULL,
    `Variable` char(15) NOT NULL,
    `Data` char(1) NOT NULL,
    Datee date NOT NULL default "1901-01-01",
    EndDate date,
    IniHour time,
    EndHour time,
    `MinValue` double,
    alert1min double,
    alert2min double,
    alert2max double,
    alert1max double,
    `MaxValue` double,
    Variac double,
    Minutes int(11),
    PRIMARY KEY  (Station,`Variable`,`Data`,Datee)
    ) ENGINE=MyISAM;
CREATE TABLE Valsvariabaut (
    Station char(20) NOT NULL default "",
    `Variable` char(15) NOT NULL default "",
    Adjust1 double NOT NULL default "0",
    Adjust2 double NOT NULL default "0",
    `MaxValue` double,
    `MinValue` double,
    ValorNoHayDato double,
    CriticoArriba double,
    CriticoAbajo double,
    PRIMARY KEY  (Station,`Variable`)
    ) ENGINE=MyISAM;
CREATE TABLE Variabautomatv (
    Station char(20) NOT NULL default "",
    `Variable` char(15) NOT NULL default "",
    period int(11),
    PRIMARY KEY  (Station,`Variable`)
    ) ENGINE=MyISAM;
CREATE TABLE Variabautomaxfecha (
    SatelliteID char(8) NOT NULL default "",
    DateTime datetime NOT NULL default "2001-01-01 00:00:00",
    Secuen int(11) NOT NULL default "0",
    Area char(15),
    Name char(30),
    `Variable` char(15),
    period int(11),
    PRIMARY KEY  (SatelliteID,DateTime,Secuen)
    ) ENGINE=MyISAM;
CREATE TABLE VariabDeriv2 (
    Station char(20) NOT NULL default "",
    `Variable` char(15) NOT NULL default "",
    FormCalculo text,
    PRIMARY KEY  (Station,`Variable`)
    ) ENGINE=MyISAM;
CREATE TABLE VariabDeriv3 (
    Station char(20) NOT NULL default "",
    `Variable` char(15) NOT NULL default "",
    FormCalculo text,
    PRIMARY KEY  (Station,`Variable`)
    ) ENGINE=MyISAM;
CREATE TABLE `Variables` (
    `Variable` char(15) NOT NULL default "",
    ShortName char(4),
    DescripVariab char(150),
    TableName char(15),
    Units char(10),
    TypeDDoDE char(2),
    TipAcum char(4),
    NDecim int(11),
    CalcxGrp char(8),
    CalcDTaD char(8),
    PRIMARY KEY  (`Variable`)
    ) ENGINE=MyISAM;
CREATE TABLE Variablestransf (
    Station char(20) NOT NULL default "",
    `Variable` char(15) NOT NULL default "",
    BegnDate datetime NOT NULL default "1901-01-01 00:00:00",
    Adjust1 double NOT NULL default "0",
    Adjust2 double NOT NULL default "0",
    VariabTransf1 char(20),
    TablaTransf1 char(15),
    VariabTransf2 char(20),
    TablaTransf2 char(15),
    VariabTransf3 char(20),
    TablaTransf3 char(15),
    VariabTransf4 char(20),
    TablaTransf4 char(15),
    PRIMARY KEY  (Station,`Variable`,BegnDate)
    ) ENGINE=MyISAM;
CREATE TABLE VerifCerca (
    Station char(20) NOT NULL,
    `Variable` char(15) NOT NULL,
    Distance double,
    difaltura double,
    StationGroup char(20),
    variacion double,
    intervmin int(11),
    PRIMARY KEY  (Station,`Variable`)
    ) ENGINE=MyISAM;
CREATE TABLE Verific (
    `Variable` char(15) NOT NULL,
    `Data` char(1) NOT NULL,
    Secuen int(11) NOT NULL,
    Tipo char(1),
    Verif text,
    PRIMARY KEY  (`Variable`,`Data`,Secuen)
    ) ENGINE=MyISAM;
CREATE TABLE Webbitacoraproc (
    Tally int(11) NOT NULL auto_increment,
    program char(20),
    Userr char(50),
    proctype char(20),
    OpcionProc char(15),
    DateTime datetime,
    PRIMARY KEY  (Tally)
    ) ENGINE=MyISAM;
CREATE TABLE Webcontadores (
    program char(30) NOT NULL default "",
    Userr char(50) NOT NULL default "",
    proctype char(20) NOT NULL default "",
    OpcionProc char(20) NOT NULL default "",
    Tally int(11),
    PRIMARY KEY  (program,Userr,proctype,OpcionProc)
    ) ENGINE=MyISAM;
CREATE TABLE ZonasAreas (
    zone char(50) NOT NULL,
    Area double,
    PRIMARY KEY  (zone)
    ) ENGINE=MyISAM;
