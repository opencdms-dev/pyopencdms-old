## observationfinal

| Column name | Definition |
|-------------|-------------|
|recordedFrom | varchar(255) NOT NULL |
|describedBy  | bigint(20) DEFAULT NULL |
|obsDatetime  | datetime DEFAULT NULL|
|obsLevel     | varchar(255) DEFAULT 'surface'|
|obsValue     | decimal(8,2) DEFAULT NULL|
|flag         | varchar(255) DEFAULT 'N'|
|period       | int(11) DEFAULT NULL|
|qcStatus     | int(11) DEFAULT '0'|
|qcTypeLog    | text|
|acquisitionType | int(11) DEFAULT '0'|
|dataForm     | varchar(255) DEFAULT NULL|
|capturedBy   | varchar(255) DEFAULT NULL|
|mark         | tinyint(4) DEFAULT NULL|
|temperatureUnits | varchar(255) DEFAULT NULL|
|precipitationUnits | varchar(255) DEFAULT NULL|
|cloudHeightUnits | varchar(255) DEFAULT NULL|
|visUnits | varchar(255) DEFAULT NULL|
|dataSourceTimeZone | int(11) DEFAULT '0'|

```
UNIQUE KEY `obsFinalIdentification` (`recordedFrom`,`describedBy`,`obsDatetime`),
  KEY `obsElementObservationInitial` (`describedBy`),
  KEY `stationObservationInitial` (`recordedFrom`),
  CONSTRAINT `FK_mysql_climsoft_db_v4_obselement_observationFinal` FOREIGN KEY (`describedBy`) REFERENCES `obselement` (`elementId`),
  CONSTRAINT `FK_mysql_climsoft_db_v4_station_observationFinal` FOREIGN KEY (`recordedFrom`) REFERENCES `station` (`stationId`)
```
