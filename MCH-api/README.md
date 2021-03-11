# MCH API 0.1

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

## Usage

All responses will have the form

```json
{
    "Field1": "Field in the table ...",
    "Field1": "Field in the table ..."
    "..."
}
```

### stations

**Definition**

`GET /API/stations`

**Response**

- `200 OK` on success

```json
[
    {
        "Station": "01AECLIF",
        "StationName": "Eclipse Falls",
        "StationName2": "",
        "TimeZone": "GUY",
        "Longitude": 0,
        "Latitude": 0,
        "Altitude": 69.0,
        "Longitude2": -60.0632,
        "Latitude2": 7.6349,
        "DMSlongitude": "060\u00b003'48''",
        "DMSLatitude": "07\u00b038'06''",
        "Statee": "R1\r",
        "RegManagmt": null,
        "Catchment": null,
        "Subcatchment": null,
        "OperatnlRegion": null,
        "HydroReg": null,
        "RH(2)": null,
        "Municipality": null,
        "CodeB": null,
        "CodeG": null,
        "CodeCB": null,
        "CodePB": null,
        "CodeE": null,
        "CodeCL": null,
        "CodeHG": null,
        "CodePG": null,
        "CodeNw": null,
        "Code1": null,
        "Code2": null,
        "Code3": null,
        "MaxOrdStrgLvl": null,
        "MaxOrdStrgVol": null,
        "MaxExtStrgLvl": null,
        "MaxExtStrgVol": null,
        "SpillwayLevel": null,
        "SpillwayStorage": null,
        "FreeSpillwayLevel": null,
        "FreeSpillwayStorage": null,
        "DeadStrgLevel": null,
        "DeadStrgCapac": null,
        "UsableStorageCapLev": null,
        "UsableStorage": null,
        "HoldingStorage": null,
        "Key1fil": null,
        "Key2fil": null,
        "Key3fil": null,
        "CritLevelSta": null,
        "MinLevelSta": null,
        "MaxLevelSta": null,
        "CritFlow": null,
        "MinDischarge": null,
        "MaxDischarge": null,
        "Stream": null,
        "Distance": null,
        "Infrastructure": null,
        "Type": null,
        "Usee": null
    },
    {
        "Station": "01ARAKAK",
        "StationName": "ARAKAKA",
        "StationName2": "ARAKAKA",
        "TimeZone": "GUY",
        "Longitude": 0,
        "Latitude": 0,
        "Altitude": 241.0,
        "Longitude2": 0.0,
        "Latitude2": 7.495278,
        "DMSlongitude": "",
        "DMSLatitude": "07\u00b029'43''",
        "Statee": "R1\r",
        "RegManagmt": null,
        "Catchment": null,
        "Subcatchment": null,
        "OperatnlRegion": null,
        "HydroReg": null,
        "RH(2)": null,
        "Municipality": null,
        "CodeB": null,
        "CodeG": null,
        "CodeCB": null,
        "CodePB": null,
        "CodeE": null,
        "CodeCL": null,
        "CodeHG": null,
        "CodePG": null,
        "CodeNw": null,
        "Code1": null,
        "Code2": null,
        "Code3": null,
        "MaxOrdStrgLvl": null,
        "MaxOrdStrgVol": null,
        "MaxExtStrgLvl": null,
        "MaxExtStrgVol": null,
        "SpillwayLevel": null,
        "SpillwayStorage": null,
        "FreeSpillwayLevel": null,
        "FreeSpillwayStorage": null,
        "DeadStrgLevel": null,
        "DeadStrgCapac": null,
        "UsableStorageCapLev": null,
        "UsableStorage": null,
        "HoldingStorage": null,
        "Key1fil": null,
        "Key2fil": null,
        "Key3fil": null,
        "CritLevelSta": null,
        "MinLevelSta": null,
        "MaxLevelSta": null,
        "CritFlow": null,
        "MinDischarge": null,
        "MaxDischarge": null,
        "Stream": null,
        "Distance": null,
        "Infrastructure": null,
        "Type": null,
        "Usee": null
    }, ...
]
```

### Query a station

**Definition**

`GET /API/stations/qry_station`

**Arguments**

- `"stn_id":string` a globally unique identifier for this station

**Response**

- `404 Not Found` if the station does not exist
- `200 OK` on success

```json
[
    {
        "Station": "01MATTRG",
        "StationName": "MATTHEWS RIDGE",
        "StationName2": "",
        "TimeZone": "GUY",
        "Longitude": 0,
        "Latitude": 0,
        "Altitude": 0.0,
        "Longitude2": 0.0,
        "Latitude2": 0.0,
        "DMSlongitude": "",
        "DMSLatitude": "",
        "Statee": "R1\r",
        "RegManagmt": null,
        "Catchment": null,
        "Subcatchment": null,
        "OperatnlRegion": null,
        "HydroReg": null,
        "RH(2)": null,
        "Municipality": null,
        "CodeB": null,
        "CodeG": null,
        "CodeCB": null,
        "CodePB": null,
        "CodeE": null,
        "CodeCL": null,
        "CodeHG": null,
        "CodePG": null,
        "CodeNw": null,
        "Code1": null,
        "Code2": null,
        "Code3": null,
        "MaxOrdStrgLvl": null,
        "MaxOrdStrgVol": null,
        "MaxExtStrgLvl": null,
        "MaxExtStrgVol": null,
        "SpillwayLevel": null,
        "SpillwayStorage": null,
        "FreeSpillwayLevel": null,
        "FreeSpillwayStorage": null,
        "DeadStrgLevel": null,
        "DeadStrgCapac": null,
        "UsableStorageCapLev": null,
        "UsableStorage": null,
        "HoldingStorage": null,
        "Key1fil": null,
        "Key2fil": null,
        "Key3fil": null,
        "CritLevelSta": null,
        "MinLevelSta": null,
        "MaxLevelSta": null,
        "CritFlow": null,
        "MinDischarge": null,
        "MaxDischarge": null,
        "Stream": null,
        "Distance": null,
        "Infrastructure": null,
        "Type": null,
        "Usee": null
    }
]
```
**Definition**

`POST /API/stations/qry_station`

**Arguments**

- `"file":string` The file in json format to load the station definition (s) in the MCH database
- `"stn_id":string` a globally unique identifier for this station
- `"stn_name":string` the name of the station
- `"stn_name2":string` the secondary name of the station
- `"t_zone":string` timezone of the station
- `"long":string` longitude in decimal degrees of the station
- `"lat":string` latitude in decimal degrees of the station
- `"alt":string` altitude of the station
- `"state_id":string` a globally unique identifier for this state
- `"reg_m":string` a globally unique identifier for this regional management
- `"catchm":string` a globally unique identifier for this catchment
- `"s_cat":string` a globally unique identifier for this subcatchment
- `"o_reg":string` a globally unique identifier for this operational region
- `"hydro_r":string` name for this hydrological region
- `"rh":string` a globally unique identifier for this hydrological region
- `"mun_id":string` a globally unique identifier for this municipality
- `"mosl":string` Maximum Ordinary Storage Level for this station (reservoir)
- `"mosv":string` Maximum Ordinary Storage Volume for this station (reservoir)
- `"mesl":string` Maximum Extraordinary Storage Level for this station (reservoir)
- `"mesv":string` Maximum Extraordinary Storage Volume for this station (reservoir)
- `"s_level":string` Spillway Level for this station (reservoir)
- `"s_stor":string` Spillway Storage for this station (reservoir)
- `"fs_level":string` Free Spillway Level for this station (reservoir)
- `"fs_stor":string` Free Spillway Storage for this station (reservoir)
- `"ds_level":string` Dead Storage Level for this station (reservoir)
- `"ds_cap":string` Dead Storage Capacity for this station (reservoir)
- `"us_capl":string` Usable Storage Capacity Level for this station (reservoir)
- `"ustor":string` Usable Storage Capacity for this station (reservoir)
- `"hstor":string` Holding Storage Capacity for this station (reservoir)
- `"crl_s":string` Critical Level for this station (hydrometric station)
- `"mnl_s":string` Minimum channel or river level (hydrometric station)
- `"mxl_s":string` Maximum channel or river level (hydrometric station)
- `"cr_f":string` Critical Flow of the channel or river (hydrometric station)
- `"mn_dis":string` Minimum Discharge of the channel or river (hydrometric station)
- `"mx_dis":string` Minimum Discharge of the channel or river (hydrometric station)
- `"stream":string` Stream or river (hydrometric station, reservoir)
- `"dist":string` Distance at the stream or river (hydrometric station)
- `"infr":string` Infrastructure of the station (hydrometric station, reservoir)
- `"type":string` Type of the station
- `"use":string` Use of the station (reservoir)

**Response**

- `201 OK` station storaged

**Definition**

`DEL /API/stations/qry_station`

**Arguments**

- `"stn_id":string` a globally unique identifier for this station

**Response**

- `204 OK` station deleted
### Station groups

`GET /API/stngroups`

**Response**

- `200 OK` on success

```json
[
    {
        "Stngroup": "Guyana"
    },
    {
        "Stngroup": "Hydros"
    },
    {
        "Stngroup": "Myanmar"
    }
]
```

### Query an station group

**Definition**

`GET /API/stngroups/qry_stngroup`

**Arguments**

- `"stngp_id":string` a globally unique identifier for this station group

**Response**

- `404 Not Found` if the station group does not exist
- `200 OK` on success

```json
[
    {
        "Stngroup": "Guyana",
        "Secuen": 10,
        "Station": "Aishalton"
    },
    {
        "Stngroup": "Guyana",
        "Secuen": 20,
        "Station": "Albion"
    },
    {
        "Stngroup": "Guyana",
        "Secuen": 30,
        "Station": "AnnaRegina"
    }
]
```
**Definition**

`POST /API/stngroups/qry_stngroup`

**Arguments**

- `"file":string` The file in json format to load the station group definition in the MCH database

**Response**

- `201 OK` station group storaged
**Definition**

`DEL /API/stngroups/qry_stngroup`

**Arguments**

- `"stngp_id":string` a globally unique identifier for this station group

**Response**

- `204 OK` station group deleted
### Variables

`GET /API/variables`

**Response**

- `200 OK` on success

```json
[
    {
        "Variable": "AirTemp"
    },
    {
        "Variable": "BaromPresMax"
    },
    {
        "Variable": "BaromPresMin"
    },
    {
        "Variable": "BaromPressure"
    }
]
```

### Query an variable

**Definition**

`GET /API/variables/qry_variable`

**Arguments**

- `"var_id":string` a globally unique identifier for this variable

**Response**

- `404 Not Found` if the variable does not exist
- `200 OK` on success

```json
[
    {
        "Variable": "Precipitation",
        "VariabAbbrev": "PR",
        "VariabDescrn": "Precipitaci\u00f3n",
        "TableName": "precipitation",
        "Unit": "mm",
        "TypeDDorDE": "DD",
        "CumulType": "CUMU",
        "NbrDecimal": 2,
        "CalcbyGrp": "MEAN",
        "CalcDTaD": "CUMULAT"
    }
]
```
### States

`GET /API/states`

**Response**

- `200 OK` on success

```json
[
    {
        "Statee": "AG",
        "State2": "AG",
        "Statename": "AGUASCALIENTES"
    },
    {
        "Statee": "AR",
        "State2": "ARTIGAS",
        "Statename": "ARTIGAS"
    },
    {
        "Statee": "BN",
        "State2": "BN",
        "Statename": "BAJA CALIFORNIA NORTE"
    },
    {
        "Statee": "BS",
        "State2": "BS",
        "Statename": "BAJA CALIFORNIA SUR"
    }
]
```

### Query an state

**Definition**

`GET /API/stngroups/qry_state`

**Arguments**

- `"state_id":string` a globally unique identifier for this state

**Response**

- `404 Not Found` if the state does not exist
- `200 OK` on success

```json
[
    {
        "Statee": "BS",
        "State2": "BS",
        "Statename": "BAJA CALIFORNIA SUR"
    }
]
```
**Definition**

`POST /API/stngroups/qry_state`

**Arguments**

- `"file":string` The file in json format to load the state definition (s) in the MCH database
- `"state_id":string` a globally unique identifier for this state
- `"state_2":string` compact description of this state
- `"state_name":string` complete name for this state

**Response**

- `201 OK` state storaged
**Definition**

`DEL /API/stngroups/qry_state`

**Arguments**

- `"state_id":string` a globally unique identifier for this state

**Response**

- `204 OK` state deleted

### Municipalities

`GET /API/municipalities`

**Response**

- `200 OK` on success

```json
[
    {
        "Municipality": "AG001",
        "Municipality2": "AG001",
        "MunicipalityName": "AGUASCALIENTES"
    },
    {
        "Municipality": "AG002",
        "Municipality2": "AG002",
        "MunicipalityName": "ASIENTOS"
    },
    {
        "Municipality": "AG003",
        "Municipality2": "AG003",
        "MunicipalityName": "CALVILLO"
    }
]
```

### Query an municipality

**Definition**

`GET /API/municipalities/qry_municipality`

**Arguments**

- `"mun_id":string` a globally unique identifier for this municipality

**Response**

- `404 Not Found` if the municipality does not exist
- `200 OK` on success

```json
[
    {
        "Statee": "BS",
        "State2": "BS",
        "Statename": "BAJA CALIFORNIA SUR"
    }
]
```
**Definition**

`POST /API/municipalities/qry_municipality`

**Arguments**

- `"file":string` The file in json format to load the municipality definition (s) in the MCH database
- `"mun_id":string` a globally unique identifier for this municipality
- `"mun_2":string` compact description of this municipality
- `"mun_name":string` complete name for this municipality

**Response**

- `201 OK` municipality storaged
**Definition**

`DEL /API/municipalities/qry_municipality`

**Arguments**

- `"mun_id":string` a globally unique identifier for this municipality

**Response**

- `204 OK` municipality deleted

### Hydrological regions

`GET /API/hydroregions`

**Response**

- `200 OK` on success

```json
[
    {
        "Hydroreg": "RH10A",
        "Hydroreg2": "RH10A",
        "HydrRegionName": "RIO FUERTE"
    },
    {
        "Hydroreg": "RH10B",
        "Hydroreg2": "RH10B",
        "HydrRegionName": "RIO SINALOA"
    },
    {
        "Hydroreg": "RH10C",
        "Hydroreg2": "RH10C",
        "HydrRegionName": "RIO MOCORITO"
    },
    {
        "Hydroreg": "RH10D",
        "Hydroreg2": "RH10D",
        "HydrRegionName": "RIO CULIACAN"
    }
]]
```

### Query an hydrological region

**Definition**

`GET /API/hydroregions/qry_hydroregion`

**Arguments**

- `"hr_id":string` a globally unique identifier for this hydrological region

**Response**

- `404 Not Found` if the hydrological region does not exist
- `200 OK` on success

```json
[
    {
        "Statee": "BS",
        "State2": "BS",
        "Statename": "BAJA CALIFORNIA SUR"
    }
]
```
**Definition**

`POST /API/hydroregions/qry_hydroregion`

**Arguments**

- `"file":string` The file in json format to load the hydrological region definition (s) in the MCH database
- `"hr_id":string` a globally unique identifier for this hydrological region
- `"hr_2":string` compact description of this hydrological region
- `"hr_name":string` complete name for this hydrological region

**Response**

- `201 OK` hydrological region storaged
**Definition**

`DEL /API/hydroregions/qry_hydroregion`

**Arguments**

- `"hr_id":string` a globally unique identifier for this hydrological region

**Response**

- `204 OK` hydrological region deleted

### Catchments

`GET /API/catchments`

**Response**

- `200 OK` on success

```json
[
    {
        "Hydroreg": "RH10A",
        "Hydroreg2": "RH10A",
        "HydrRegionName": "RIO FUERTE"
    },
    {
        "Hydroreg": "RH10B",
        "Hydroreg2": "RH10B",
        "HydrRegionName": "RIO SINALOA"
    },
    {
        "Hydroreg": "RH10C",
        "Hydroreg2": "RH10C",
        "HydrRegionName": "RIO MOCORITO"
    },
    {
        "Hydroreg": "RH10D",
        "Hydroreg2": "RH10D",
        "HydrRegionName": "RIO CULIACAN"
    }
]
```

### Query an catchment

**Definition**

`GET /API/catchments/qry_catchment`

**Arguments**

- `"cat_id":string` a globally unique identifier for this catchment

**Response**

- `404 Not Found` if the catchment does not exist
- `200 OK` on success

```json
[
    {
        "Catchment": "C0101",
        "Catchment2": "C0101",
        "CatchmentName": "RIO TIJUANA-ARROYO MENEADERO"
    }
]
```
**Definition**

`POST /API/catchments/qry_catchment`

**Arguments**

- `"file":string` The file in json format to load the catchment definition (s) in the MCH database
- `"cat_id":string` a globally unique identifier for this catchment
- `"cat_2":string` compact description of this catchment
- `"cat_name":string` complete name for this catchment

**Response**

- `201 OK` catchment storaged
**Definition**

`DEL /API/catchments/qry_catchment`

**Arguments**

- `"cat_id":string` a globally unique identifier for this catchment

**Response**

- `204 OK` catchment deleted

### Subcatchments

`GET /API/subcatchments`

**Response**

- `200 OK` on success

```json
[
    {
        "Subcatchment": "SUB02",
        "Subcatchment2": "DOKEHTAWADY",
        "SubCatchmentName": "DOKEHTAWADY RIVER BASIN"
    },
    {
        "Subcatchment": "SUB03",
        "Subcatchment2": "DOKEHTAWADY",
        "SubCatchmentName": "DOKEHTAWADY RIVER BASIN UPSTREAM"
    }
]
```

### Query an subcatchment

**Definition**

`GET /API/subcatchments/qry_subcatchment`

**Arguments**

- `"scat_id":string` a globally unique identifier for this subcatchment

**Response**

- `404 Not Found` if the subcatchment does not exist
- `200 OK` on success

```json
[
    {
        "Subcatchment": "SUB02",
        "Subcatchment2": "DOKEHTAWADY",
        "SubCatchmentName": "DOKEHTAWADY RIVER BASIN"
    }
]
```
**Definition**

`POST /API/subcatchments/qry_subcatchment`

**Arguments**

- `"file":string` The file in json format to load the subcatchment definition (s) in the MCH database
- `"scat_id":string` a globally unique identifier for this subcatchment
- `"scat_2":string` compact description of this subcatchment
- `"scat_name":string` complete name for this subcatchment

**Response**

- `201 OK` subcatchment storaged
**Definition**

`DEL /API/subcatchments/qry_subcatchment`

**Arguments**

- `"scat_id":string` a globally unique identifier for this subcatchment

**Response**

- `204 OK` subcatchment deleted

### Units

`GET /API/units`

**Response**

- `200 OK` on success

```json
[
    {
        "Unit": "%",
        "UnitDescription": "porcentaje"
    },
    {
        "Unit": "ac.ft.",
        "UnitDescription": "acre feet"
    },
    {
        "Unit": "acre",
        "UnitDescription": "acre"
    },
    {
        "Unit": "C",
        "UnitDescription": "grados Celsius"
    },
    {
        "Unit": "cm",
        "UnitDescription": "cent\u00edmetros"
    }
]
```

### Query an unit

**Definition**

`GET /API/units/qry_unit`

**Arguments**

- `"unit_id":string` a globally unique identifier for this unit

**Response**

- `404 Not Found` if the unit does not exist
- `200 OK` on success

```json
[
    {
        "Unit": "ac.ft.",
        "UnitDescription": "acre feet"
    }
]
```
**Definition**

`POST /API/units/qry_unit`

**Arguments**

- `"file":string` The file in json format to load the unit definition (s) in the MCH database
- `"scat_id":string` a globally unique identifier for this v
- `"unit_desc":string` complete name for this unit

**Response**

- `201 OK` unit storaged
**Definition**

`DEL /API/units/qry_unit`

**Arguments**

- `"scat_id":string` a globally unique identifier for this unit

**Response**

- `204 OK` unit deleted

### Query daily data

**Definition**

`GET /API/data/dailydata`

**Arguments**

- `"stn_id":string` a globally unique identifier for this station
- `"var_id":string` a globally unique identifier for this variable
- `"date_ini":date` the period start date YYYY/MM/DD
- `"date_end":date` the period end date YYYY/MM/DD
- `"datee":date` the date for a single day

A query can be made for a date or a period depending on which parameters are entered.

**Response**

- `404 Not Found` if the variable does not exist or there is no data for the query
- `200 OK` on success

```json
[
    {
        "Station": "01MATTRG",
        "Date": "2013-11-01T00:00:00Z",
        "Value": 7.8
    },
    {
        "Station": "01MATTRG",
        "Date": "2013-11-02T00:00:00Z",
        "Value": 12.2
    },
    {
        "Station": "01MATTRG",
        "Date": "2013-11-03T00:00:00Z",
        "Value": 10.5
    },
    {
        "Station": "01MATTRG",
        "Date": "2013-11-04T00:00:00Z",
        "Value": 0.0
    },
    {
        "Station": "01MATTRG",
        "Date": "2013-11-05T00:00:00Z",
        "Value": 0.0
    },
    {
        "Station": "01MATTRG",
        "Date": "2013-11-06T00:00:00Z",
        "Value": 8.8
    },
    {
        "Station": "01MATTRG",
        "Date": "2013-11-07T00:00:00Z",
        "Value": 9.0
    }
]
```
**Definition**

`POST /API/data/dailydata`

**Arguments**

- `"file":string` The file in json format to load the subcatchment definition (s) in the MCH database
- `"stn_id":string` a globally unique identifier for this station
- `"var_id":string` a globally unique identifier for this variable
- `"datee":string` date for this value
- `"value":string` value for the variable
- `"maxvaldate":string` date for this maximum value
- `"maxvalue":string` maximum value for the variable
- `"minvaldate":string` date for the minimum value
- `"minvalue":string` minimum value for the variable

**Response**

- `201 OK` record storaged
**Definition**

`DEL /API/data/dailydata`

**Arguments**

- `"stn_id":string` a globally unique identifier for this station
- `"var_id":string` a globally unique identifier for this variable
- `"datee":string` date for this value

**Response**

- `204 OK` record deleted

### Query detail data

**Definition**

`GET /API/data/detaildata`

**Arguments**

- `"stn_id":string` a globally unique identifier for this station
- `"var_id":string` a globally unique identifier for this variable
- `"date_ini":date` the period start date YYYY/MM/DD HH:MM:SS
- `"date_end":date` the period end date YYYY/MM/DD HH:MM:SS
- `"datee":date` the date for a single day YYYY/MM/DD HH:MM:SS

A query can be made for a date or a period depending on which parameters are entered.

**Response**

- `404 Not Found` if the variable does not exist or there is no data for the query
- `200 OK` on success

```json
[
    {
        "Station": "2060",
        "Date": "2019-04-01T00:00:00Z",
        "Value": 0.0
    },
    {
        "Station": "2060",
        "Date": "2019-04-01T00:30:00Z",
        "Value": 0.0
    },
    {
        "Station": "2060",
        "Date": "2019-04-01T01:00:00Z",
        "Value": 0.0
    },
    {
        "Station": "2060",
        "Date": "2019-04-01T01:30:00Z",
        "Value": 0.0
    }
]
```
**Definition**

`POST /API/data/detaildata`

**Arguments**

- `"file":string` The file in json format to load the subcatchment definition (s) in the MCH database
- `"stn_id":string` a globally unique identifier for this station
- `"var_id":string` a globally unique identifier for this variable
- `"datee":string` date for this value
- `"value":string` value for the variable

**Response**

- `201 OK` record storaged
**Definition**

`DEL /API/data/detaildata`

**Arguments**

- `"stn_id":string` a globally unique identifier for this station
- `"var_id":string` a globally unique identifier for this variable
- `"datee":string` date for this value

**Response**

- `204 OK` record deleted
