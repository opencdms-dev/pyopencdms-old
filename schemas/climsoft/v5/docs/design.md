# Overview

This proposal builds on the model changes first discussed at the [Climsoft Developers Workshop, Kitale, Kenya 18 – 22 March 2019](https://github.com/climsoft/Climsoft/wiki/Climsoft-Developers-Workshop,Kitale,-18th-to--22nd-March-2019) and further discussed on GitHub issues including [#475](https://github.com/climsoft/Climsoft/issues/475).

The database model in this proposal is built from three key ideas:

- The Climsoft long data format. The observation table follows this structure and we have also replicated it for other components of the database. This generalisation means there is the potential to store spatial data and the paper archive images in powerful ways as well as increase the software&#39;s flexibility through flexible storage of properties.
- Git versioning. We have conceptualised the version control of records in tables which will allow for a full audit trail of changes. The version control system proposed closely resembles the basis of the Git version control software (which is the basis for GitHub). This should be reassuring as it shows we are mirroring and building on established concepts. The proposed version control system is a simplified Git versioning system which can provide a robust full audit trail for all database actions.
- The Open Geospatial Consortium (OGC) Standards. It is important to be aware of and, where possible, align with relevant international standard to ensure Climsoft is considered as a serious software worldwide. The database model in this proposal closely follows the standard&#39;s concept of a &quot;feature&quot;, which generalises the concept of a &quot;station&quot;. This has proved useful in simplifying the database implementation.

The sections below describe the core ideas of the database design and describe each proposed table, its use, and examples. The example tables are intended to illustrative of a use of the table, but may not show the complete functionality, or all possible variations. However, the examples are intended to be consistent with each other, so data in tables which are linked should have links that are consistent. Tables are prefixed with c5_ to identify them as Climsoft version 5 tables and distinguish them from version 4 tables that they may sit along in the same database.

The proposed database design is intended to enable replicating the current functionality of Climsoft, as well as providing notable additional features, particularly around the use of metadata (properties, auditing, comments and events). This is intended to be a minimal design, and additional tables/fields may need to be added to ensure all current functionality can be achieved.

When implementing this database, fixed views can be used to improve efficiency and usability. For example, fixed views may be created for (all) tables showing only the most current version of each record. This would also restore many-to-one relations.

![Climsoft v5](https://user-images.githubusercontent.com/11214914/72787409-ea052280-3c40-11ea-804c-ce76a8566e87.png)
Figure 1: Proposed version 5 database model
# Table of Contents
- [Overview](#overview)
- [Audit Trail](#audit-trail)
- [Observation tables](#observation-tables)
  - [c5_observation](#c5_observation)
  - [c5_observation_property](#c5_observation_property)
  - [c5_observation_property_value](#c5_observation_property_value)
- [Feature tables](#feature-tables)
  - [c5_feature_type](#c5_feature_type)
  - [c5_feature_type_property](#c5_feature_type_property)
  - [c5_feature](#c5_feature)
  - [c5_feature_property_value](#c5_feature_property_value)
  - [c5_feature_collection](#c5_feature_collection)
  - [c5_feature_geometry](#c5_feature_geometry)
- [Auditing tables](#auditing-tables)
  - [c5_audit](#c5_audit)
  - [c5_event](#c5_event)
  - [c5_event_effect](#c5_event_effect)
  - [c5_action_type](#c5_action_type)
  - [c5_action](#c5_action)
  - [c5_observation_entry_action_type](#c5_observation_entry_action_type)
  - [c5_comment](#c5_comment)
- [Elements and Measurement tables](#elements-and-measurement-tables)
  - [c5_element](#c5_element)
  - [c5_measurement](#c5_measurement)
  - [c5_instrument](#c5_instrument)
  - [c5_instrument_instance](#c5_instrument_instance)
  - [c5_feature_measurement_instrument_instance](#c5_feature_measurement_instrument_instance)
- [Artifact and Measure group tables](#artifact-and-measure-group-tables)
  - [c5_artifact](#c5_artifact)
  - [c5_measurement_group, c5_measure_group_type, c5_measure_group_definition, c5_feature_measure_group](#c5_measurement_group-c5_measure_group_type-c5_measure_group_definition-c5_feature_measure_group)

# Audit Trail

A major addition in the proposed database design is the audit trail. The audit trail ensures that it is possible to record every change to the database. This is achieved through the audit table and related tables, as well as the addition of `version_number` and `current` (or `current_best`) fields to all tables excluding the audit tables.

All tables, apart from `c5_audit` and `c5_observation_entry_action_type` tables, will have the fields: `id`, `version_number` and `current` (or `current_best`). `id` and `version_number` form a composite primary key for each table.

For observation data, `current_best` indicates which version is the current best version for each id by a positive integer value. The value of the positive integer indicates the state of the observation. Rows which are not the current best will either be `NULL` or `-1`. `NULL` indicates not the current best and `-1` indicates a candidate current best which requires action (a different value from double data entry). For example, a correction to an observation will lead to a new row in the `c5_observation` table for the corrected value. The `current_best` field will indicate that this is the current best value for that observation. The record with the previous value will remain in the `c5_observation` table but its `current_best` field will be modified to indicate it is no longer the current best value for that observation. Retaining the previous values ensures a full audit of changes is recorded.

For metadata, the `current` field is used in a similar way. However, the value of the positive integers in the `current` field have a different meaning and multiple positive integer values per id is possible. The positive integers are defined by events. For example, if a station moved actual location then the new record with the new location would have `current` equal to `2` and row with the previous location before the move event would have current equal to `1`. The positive integers therefore show the history of the station. Moving the location of a station would also be recorded in the `c5_event` table, which records the date of the event. This allows for reconstructing the history.

For both observation data and metadata, each change to a value is also recorded in the `c5_audit` table. When a change is made, the change and the previous and new value of the `version_number` field is recorded in the `c5_audit` table to allow for reconstructing the history of changes.

The [Auditing tables section](#auditing-tables) provides a detailed description of the tables used for auditing.

# Observation tables

## c5_observation

This table records all observations. This replaces the functionality of the data entry form tables, and the observation initial table, through the use of `current_best`. The value of `current_best` can be used to replicate the save and upload processes in Climsoft.

| `id` | `feature_measurement_instrument_id` | `obs_date` | `version_number` | `qc_log` | `current_best` | `value` | `flag` | `period` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 17/01/2020 | 1 | 1 | 1 | 20 |   |   |
| 2 | 2 | 17/01/2020 | 1 | 1 | 1 | 12.5 |   |   |

- `feature_measurement_instrument_id` – The feature_measurement_instrument_id that this observation is for. `feature_measurement_instrument_id` includes the station, measurement (element) and instrument details.

- `obs_date` – The date the observation was made on.

- `qc_log` – The QC processes that have been run on the observation. This may be stored as numbers separated by comas.

- `current_best` – Integer values can be codes to replicate the current Climsoft save and upload processes, as described here [#475](https://github.com/climsoft/Climsoft/issues/475). Negative values for current best can be used to indicate proposed values which are waiting to be confirmed, probably requiring human action.

- `value` – The actual value of the observation.

- `flag` – The flag associated with the observation.

period – The period associated with the observation.

## c5_observation_property

Properties of observations are separated out into property tables. This allows for greater flexibility of user defined properties. This table defines the properties that may be recorded for observations.

| `id` | `version_number` | `name` | `type` | `current` |
| --- | --- | --- | --- | --- |
| 1 | 1 | acquisitiontype | Int | 1 |
| 2 | 1 | units | char | 1 |

- `name` – The name of the property.

- `type` – The data type of the property. This could be stored as coded integers.

## c5_observation_property_value

This table records property values of observations.

| `id` | `version_number` | `property_id` | `observation_id` | `val_int` | `val_num` | `val_char` | `current` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 0 | NULL | NULL | 1 |
| 2 | 1 | 2 | 1 | NULL | NULL | mm | 1 |
| 3 | 1 | 2 | 2 | NULL | NULL | Celsius | 1 |

- `property_id` – The ID of the property the value is recorded for.

- `observation_id` – The ID of the observation the property value is recorded on.

- `val_int` – The property value if the property type is integer.

- `val_num` – The property value if the property type is numeric.

- `val_char` – The property value if the property type is character.

# Feature tables

## c5_feature_type

This table defines types of features. A feature is a geographical shape (point, polygon etc.) and/or a collection of other features. This is similar to use of [feature](http://docs.opengeospatial.org/is/17-069r3/17-069r3.html#_feature) and [feature_collection](http://docs.opengeospatial.org/is/17-069r3/17-069r3.html#_feature_collection) in the Open Geospatial Standards documents. This generalises the concept of station to include other geographical features.

In Climsoft, features will be of different types. Examples of feature types are: station, country, county, authority, admin region, drainage basin, and qualifier.

| `id` | `version_number` | `name` | `current` |
| --- | --- | --- | --- |
| 1 | 1 | station | 1 |
| 2 | 1 | country | 1 |
| 3 | 1 | admin region | 1 |
| 4 | 1 | provinces | 1 |
| 4 | 2 | county | 2 |

- `name` – This will store the different types of features.

## c5_feature_type_property

This table defines the properties of feature types. For example the station feature have properties StationId, WMOId, ICAOid. The country feature type may have CountryId as a property.

| `id` | `version_number` | `feature_type_id` | `name` | `type` | `unique` | `required` | `current` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | StationId | String | true | true | 1 |
| 2 | 1 | 1 | WMOId | Int | true | false | 1 |
| 3 | 1 | 1 | ICAOId | Int | true | false | 1 |
| 4 | 1 | 2 | CountryId | String | true | true | 1 |
| 5 | 1 | 2 | Agricultural_practice | String | false | false | 1 |

- `feature_type_id` – The ID of the feature type the property is being defined for.

- `name` – The name of the feature.

- `type` – The data type of the property. This field may be coded by integers.

- `unique` – Whether the property should be unique for each features of that type.

- `required` - Whether the property is required for all features of that type.

## c5_feature

This define the features. Features will belong to a feature type. All features will have a name that could be used to display them.

| `id` | `version_number` | `feature_type_id` | `name` | `current` |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | BINGA | NULL |
| 2 | 1 | 1 | KARIBA AIRPORT | NULL |
| 3 | 1 | 1 | KAROI | 1 |
| 4 | 1 | 2 | Kenya | 1 |
| 5 | 1 | 2 | Uganda | 1 |
| 6 | 1 | 2 | Rwanda | 1 |
| 7 | 1 | 1 | RUKOMICHE RES. STN. | 1 |
| 8 | 2 | 1 | BINGA AGROMET | 1 |
| 9 | 1 | 1 | Kisumu Station | 1 |
| 10 | 1 | 1 | Kisian Station | 1 |
| 11 | 1 | 1 | Ahero Station | 1 |
| 12 | 1 | 1 | Awasi Station | 1 |
| 13 | 1 | 4 | Kisumu County | 1 |

- `feature_type_id` – The ID of the feature type of this feature.

- `name` – The name of the feature.

For the station feature type, it may be desirable to have either the station&#39;s name stored in the name field or the station ID in the name field. Either implementation is possible depending on the requirements of a individual Met Service. If the station id is used in the &quot;Name&quot; field then the station name will be a property of station, or vice versa.

Therefore, an alternative to the first seven rows of the table above is:

| `id` | `version_number` | `feature_type_id` | `name` | `active` | `current` |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 67755030 | true | 1 |
| 2 | 1 | 1 | 67761060 | true | 1 |
| 3 | 1 | 1 | 67765020 | true | 1 |
| 4 | 1 | 2 | Kenya | true | 1 |
| 5 | 1 | 2 | Uganda | true | 1 |
| 6 | 1 | 2 | Rwanda | true | 1 |
| 7 | 1 | 1 | 67766010 | true | 1 |

## c5_feature_property_value

This table defines property values of features. Each row corresponds to a single property value of a single feature. The advantage of a property table over having properties as additional fields in the features table is that users can define their own features and properties can be defined differently for different feature types.

Only one of the `val_*` fields will be non-`NULL` since property values can be of different types. Other data type can be added if necessary.

| `id` | `version_number` | `feature_id` | `feature_type_property_id` | `val_int` | `val_double` | `val_char` | `val_date` | `current` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | 14578 | NULL | NULL | NULL | 1 |
| 2 | 1 | 1 | 3 | 536 | NULL | NULL | NULL | 1 |
| 3 | 1 | 4 | 4 | NULL | NULL | KE | NULL | 1 |
| 4 | 1 | 5 | 4 | NULL | NULL | UG | NULL | 1 |
| 5 | 1 | 4 | 5 | NULL | NULL | Maize | NULL | 1 |

- `feature_id` – The ID of the feature this property value is for.

- `feature_type_property_id` – The ID of the property this value is for.

- `val_int` – If the property value is an integer, the value is stored here.

- `val_double` - If the property value is a double, the value is stored here.

- `val_char` - If the property value is  character, the value is stored here.

- `val_date` - If the property value is a date, the value is stored here.

## c5_feature_collection

This table defines a collection of features. This can be used to group features together. For example, `Kisumu County` could be a feature collection containing the stations `Kisumu`, `Ahero`, `Awasi` and `Kisian`.

| `id` | `version_number` | `feature_id` | `includes_feature_id` | `current` |
| --- | --- | --- | --- | --- |
| 1 | 1 | 13 | 9 | 1 |
| 2 | 1 | 13 | 10 | 1 |
| 3 | 1 | 13 | 11 | 1 |
| 4 | 1 | 13 | 12 | 1 |

- `feature_id` - this is the id of the feature that contains the collection of other features in this case – `Kisumu County`.

- `includes_feature_id` – these are the ids for the features in the collection in this case the ids of `Kisumu`, `Ahero`, `Awasi` and `Kisian` stations.

The example above shows that the stations with id: `9`, `10`, `11`, `12` are contained in feature collection with id `4` (`Kisumu County`).

## c5_feature_geometry

This table defines the geometry of features. We expect features to be of different geospatial types: e.g. polygons, points, lines. For example, `Kisumu County` may be defined as a polygon. Given that previous Climsoft installations only require points, we intend to additionally include `latitude` and `longitude` columns for compatibility with existing software in order to not require any new dependencies.

| `id` | `version_number` | `feature_id` | `geometry_type` | `shape` | `current` |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 13 | polygon | () | 1 |

- `geometry_type` - The type of geospatial object  (geometry) of the feature.

- `shape` – The geospatial object of the feature.

# Auditing tables

There are two tables that record changes to data and metadata. The `c5_audit` table records changes to observation data and metadata. This includes making corrections to data.

The `c5_event` table records events i.e. a change of state. For example, if a station moves location then its geographical information will change. The station moving on a specific date will be recorded as an event. Changes to the stations geographical information will be recorded in the `c5_audit` table.

The `c5_audit` table records changes from a previous version to a new version by making a correction. The event table records the date an event happened. The event dates provides the history.

## c5_audit

| `id`   | `action_id` | `table` | `entry_id` | `version_old` | `version_new` |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | feature_type | 4 | NULL | 1 |
| 2 | 2 | feature_type | 4 | 1 | 2 |
| 3 | 1 | event | 1 | NULL | 1 |
| 4 | 1 | feature_type_property | 1 | NULL | 1 |
| 5 | 1 | feature | 1 | NULL | 1 |
| 6 | 2 | feature | 1 | 1 | 2 |
| 7 | 1 | feature | 2 | NULL | 1 |
| 8 | 3 | feature | 2 | 1 | NULL |
| 9 | 1 | feature_defination | 2 | NULL | 1 |
| 10 | 2 | feature_defination | 2 | 1 | 2 |
| 11 | 1 | event | 2 | NULL | 1 |
| 12 | 2 | feature_defination | 2 | 2 | 3 |
| 13 | 1 | event | 3 | NULL | 1 |

- `action_id` – Actions performed by users in the front end will often result in multiple changes to the database (almost) simultaneously. It may be useful to group these changes to enable viewing/undoing all changes resulting from a single action. The action ID allows for this.

- `table` – The name of the table in which the change was done.

- `entry_id` – The ID of the entry in table that was changed.

- `version_old` – The `version_number` of the value within entry_id that the change is being made on.

- `version_new` – The new `version_number` of the changed value within `entry_id`.

## c5_event

| `id` | `version_number` | `description` | `event_date` | `current` |
| --- | --- | --- | --- | --- |
| 1 | 1 | Provinces changed to counties in Kenya. |  15/01/2010 | 1 |
| 2 | 1 | Station BINGA was opened. |  15/01/2020 | 1 |
| 3 | 1 | Station KAROI moved to a new location. | 17/01/2021 | 1 |

- `description` - A human readable description of the event.

- `event_date` – The date the event happened.

## c5_event_effect

This table indicates which records in observation and metadata tables are affected by an event.

| `id` | `version_number` | `event_id` | `table_id` | `entry_id` | `entry_current_before` | `entry_current_after` | `current` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | c5_feature_type | 1 | Province | County | 1 |

- `event_id` – The event that affects the record.

- `table_id` – The name of the table that contains the record affected by the event.

- `entry_id` – The id in `table_id` of the record affected by the event.

- `entry_current_before` – The value of `current` in `entry_id` before the event happened.

- `entry_current_after` – The value of `current` in `entry_id` after the event happened.

## c5_action_type

This table defines the types of actions. Actions performed by users in the front end will often result in multiple changes to the database (almost) simultaneously. An action corresponds to an action by the user in the front end. This table defines types of action, which may be useful when searching for actions of different types.

Action types may correspond to clicking a particular button on a form in the front end. For example, `FrmDaily2:Save` is the event of a user clicking the save button in `FrmDaily2`.

If the front end attempts to perform an action where the action type does not exist in the database, a new action type will be added to the database with the corresponding name and an empty `description`.

| `id` | `version_number` | `name` | `description` | `current` |
| --- | --- | --- | --- | --- |
| 1 | 1 | frmDaily:Save | Save executed on frmDaily. | 1 |
| 2 | 1 | frmDaily:Upload | Upload executed on frmDaily. | 1 |
| 3 | 1 | frmMetadataStation:Import | Import of stations executed on frmMetadata. | 1 |
| 4 | 1 | frmDaily2:Save | Save executed on frmDaily2. | 1 |

- `name` – The name of the action type. This is unique for each `id`.

- `description` – A human readable description of the action.

## c5_action

This table records all performed actions.

| `id` | `version_number` | `action_type_id` | `operator_id` | `action_date` | `current` |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 11 | 17/01/2020 14:27:00 | 1 |
| 2 | 1 | 2 | 12 | 18/01/2020 17:43:00 | 1 |
| 3 | 1 | 5 | 06 | 18/01/2020 18:44:00 | 1 |

- `action_type_id` – The id of the action type of this action.

- `operator_id` – The id of the operator who performed the action.

- `action_date` – The datetime when the action was performed.

In the table above, the first row demonstrates that the operator with `id` `11` clicked the save button on frmDaily2. On the next day, operator with `id` `12`, (possibly an administrator), uploaded data from frmDaily2.

The last row demonstrates that operator with `id` `06`, clicked on Import for stations on the metadata form.

Other identifiers of an action e.g. the application used, IP address, may be desired as extra fields in this table.

## c5_observation_entry_action_type

This table provides a more direct links between `c5_observation` and `c5_action_type`. This could be important, for example, to efficiently determine which data entry form was used to enter each observation. This information is already available through `c5_audit`, although this could be inefficient, particularly if `c5_audit` becomes large. This table could be replaced by a fixed view in implementation.

| `id` | `observation_id` | `version_number` | `action_type_id` |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 2 | 1 | 1 |

## c5_comment

This table records comments on records in any other table. Comments may be recorded on individual observations or metadata for example, to note something unusual about a record.

| `id` | `version_number` | `table_id` | `entry_id` | `comment` | `current` |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | event | 3 | The station was moved due to construction of a new road. | 1 |
| 2 | 1 | action_type | 4 | This record has been auto generated. | 1 |

- `table_id` – The name of the table in which the comment is associated.

- `entry_id` – The id of the record in table_id that the comment is associated with.

- `comment` – The comment.

# Elements and Measurement tables

## c5_element

This table defines elements. Elements are independent of periods. For example, there is only a single rainfall element. But there would be multiple rainfall measurements for different measurement periods.

The [WMO's essential climate variables](https://gcos.wmo.int/en/essential-climate-variables/table) was a starting point for this concept, but it is likely too broad for use in this context. The exact classification of elements needs further discussion.

| `id` | `version_number` | `name` | `current` |
| --- | --- | --- | --- |
| 1 | 1 | rainfall | 1 |
| 2 | 1 | mintemp | 1 |
| 3 | 1 | maxtemp | 1 |
| 4 | 1 | windspeed | 1 |
| 5 | 1 | wet bulb | 1 |
| 6 | 1 | dry bulb | 1 |

- `name` – The name of the element.

## c5_measurement

This table records measurements they are made. A measurement is something that is recorded for an element over a specific period at a specific height. For example, daily rainfall.

| `id` | `version_number` | `element_id` | `period` | `height` | `units` | `current` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | Day |   | mm | 1 |
| 2 | 1 | 1 | Hour |   | mm | 1 |
| 2 | 1 | 2 | Day |   | Celsius | 1 |
| 3 | 1 | 3 | Day |   | Celsius | 1 |
| 4 | 1 | 4 | Hour |   | Celsius | 1 |
| 5 | 1 | 5 | Day |   | Celsius | 1 |

- `period` – The time period of the measurement.

- `height` - The height at which the measurement is recorded.

- `units` – The units the measurement is recorded in.

## c5_instrument

This table defines types of instruments.

| `id` | `version_number` | `name` | `current` |
| --- | --- | --- | --- |
| 1 | 1 | Rain gauge | 1 |
| 2 | 1 | Maximum temperature thermometer | 1 |
| 3 | 1 | Minimum temperature thermometer | 1 |
| 4 | 1 | Wind Sock | 1 |

- `name` – The name of the instrument type.

## c5_instrument_instance

This tables records instances of instruments that exists as physical objects.

| `id` | `version_number` | `instrument_id` | `location` | `current` |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 |   | 1 |
| 2 | 1 | 2 |   | 1 |
| 3 | 1 | 3 |   | 1 |
| 4 | 1 | 4 |   | 1 |

- `instrument_id` – The ID of the type of instrument of this record.

- `location` – The location of the instrument.

## c5_feature_measurement_instrument_instance

A record in this table defines a combinations of a feature, a measurement and an instrument instance. This links directly to `c5_observation` as part of uniquely defining observations.

| `id` | `version_number` | `feature_id` | `measurement_id` | `instrument_instance_id` | `current` |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 2 | 2 | 1 |
| 3 | 1 | 2 | 1 | 3 | 1 |

- `feature_id` – The ID of the feature this record refers to.

- `measurement_id` – The ID of the measurement this record refers to.

- `instrument_instance_id` – The ID of the instrument instance this record refers to.

# Artifact and Measure group tables

## c5_artifact

This table records artifacts, which is a generalisation of observations to include other data types. Examples of artifacts could be files received from an AWS, text messages, or a pixel from satellite data.

| `id` | `version_number` | `feature_measure_group_id` | `obs_date` | `qc_log` | `current_best` | `value` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 13/1/2020 |   | 1 | [satellite image] |



- `feature_measure_group_id` – The ID of the `feature_measure_group` this artifact refers to.

- `obs_date` – The date the artifact was recorded on.

- `qc_log` – The quality control that has been carried out on the artifact.

- `value` – The artifact value. This may be need to be multiple fields depending on implementation.

## c5_measurement_group, c5_measure_group_type, c5_measure_group_definition, c5_feature_measure_group

These table defines groups of measurements. For example, tmin, tmax, wet bulb and dry bulb may form a temperature measure group. This is analogues to features and feature groups.
