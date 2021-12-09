## Tables

| Table names | Description |
|-------------|-------------|
|Codes||
|Basins||
|Definiclineascontorno||
|DisponibDD||
|Estacautoma||
|stations||
|estacionesinstrum||
|metadatastations||
|states||
|Ftpbitacproc||
|regManager||
|StationGroups||
|TimeZones||
|Isolinbitac||
|Logbitacproc||
|Maps||
|MapasCroquis||
|mapsstations||
|MapasGenxCoord||
|mapsgroups||
|MapasMchxCoord||
|Mapaspixelgeogr||
|Mapaspixelgeogr4||
|mapasbycoord||
|Mapasxcoordclrs||
|Mapasxcoordgeogr||
|Mapasxcoordzonas||
|MensajesMetar||
|MensajesSynop||
|Counties||
|Opcionesmapasintxxnet||
|Opcxvariabautom||
|DataSources||
|Recepdefs||
|Recepsdatos||
|Recepsping||
|Hydrregions||
|subbasins||
|synopcrexdatos||
|synopcrexplant||
|TransfTables||
|Tablaswebconst||
|Tablaswebdef||
|tipoEstacionVariable||
|Transftp||
|Transmchamch||
|Units||
|users||
|typeusers||
|validdata||
|Valsvariabaut||
|Variabautomatv||
|Variabautomaxfecha||
|VariabDeriv2||
|VariabDeriv3||
|Variables||
|Variablestransf||
|VerifCerca||
|Verific||
|Webbitacoraproc||
|Webcontadores||
|ZonasAreas||

## MCHtablasycampos.def

The configuration of the fields and the names of the tables (the basic tables of the system) is done through a definition file the structure in the tables is the same regardless of the language used (see [#7](https://github.com/opencdms/datamodel/issues/7))

Translated to English below

```
# File with the names of the fields and the tables in several languages ​​in the database for the MCH-BD.
# Columns 1, 2 and 3 (sequence, type and key sequence) must not be modified
# Column 4 which is the message in the development base language is inserted only as a reference for the
# translation into other languages ​​and if it is modified it is not taken into account.
# Columns 5, 6 and 7 are the messages in languages ​​2, 3 and 4. Language 2 is intended to be English and
# language 3 french. Language 4 can be any other language or can be used for regionalisms
# in language 1 (Spanish).
# When a message is not defined in a language and that language is used, the value of the base language is taken
# of development as a value for that message.
# Column 8 is a comment that may exist to explain something about the message
#
# Messages can be of three types:
# 1) menu in the main form of the system,
# 2) message on command buttons, labels or displayed on forms
# 3) of contents of some boxes composed in some ways
#
# The file format is:
# One message on each line
# Line that begins with the symbol # is a comment and is not taken into account
# The data in each line must be separated by tabs (Chr (9), 0x9, \ t)

################
# field names in tables
################

...

```
