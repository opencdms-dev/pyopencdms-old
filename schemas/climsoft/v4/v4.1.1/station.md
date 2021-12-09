```
CREATE TABLE IF NOT EXISTS `station` (
  `stationId` varchar(255) NOT NULL,
  `stationName` varchar(255) DEFAULT NULL,
  `wmoid` varchar(20) DEFAULT NULL,
  `icaoid` varchar(20) DEFAULT NULL,
  `latitude` double(11,6) DEFAULT NULL,
  `qualifier` varchar(20) DEFAULT NULL,
  `longitude` double(11,6) DEFAULT NULL,
  `elevation` varchar(255) DEFAULT NULL,
  `geoLocationMethod` varchar(255) DEFAULT NULL,
  `geoLocationAccuracy` float(11,6) DEFAULT NULL,
  `openingDatetime` varchar(50) DEFAULT NULL,
  `closingDatetime` varchar(50) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `authority` varchar(255) DEFAULT NULL,
  `adminRegion` varchar(255) DEFAULT NULL,
  `drainageBasin` varchar(255) DEFAULT NULL,
  `wacaSelection` tinyint(4) DEFAULT '0',
  `cptSelection` tinyint(4) DEFAULT '0',
  `stationOperational` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`stationId`),
  KEY `StationStationId` (`stationId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```
