This directory contains SQL DDL for Climate and Hydrology Data Management Systems related to [OpenCDMS](http://opencdms.org) (not all systems are currently supported).

### Testing with original database technologies

Information is provided below for installing these systems using Docker.

For local development and testing, original database systems can be ran using docker containers.

| CDMS               | Database    | Database image | Description |
|--------------------|-------------|----------------|-------------|
| OpenCDMS RI / WMDR | TimescaleDB | `docker pull timescale/timescaledb-postgis:latest-pg13` | [overview](https://github.com/timescale/timescaledb-docker) |
| CliDE              | PostgreSQL  | `docker pull postgres:13`                               | [overview](https://hub.docker.com/_/postgres) |
| Climsoft 4         | MySQL 8     | `docker pull mysql:8`                                   | [overview](https://hub.docker.com/_/mysql)) |
| MCH                | MySQL 5.1   | `docker pull opencdms/mysql:5.1.73`                     | [overview](https://github.com/opencdms/mysql-5.1.73) |
| MIDAS              | Oracle      | `docker pull opencdms/oracle:18.4.0-xe`                 | [overview](https://github.com/oracle/docker-images/tree/main/OracleDatabase/SingleInstance) |

Note: Docker hub has the official mysql repository (debian) and an additional mysql-server reposority "Created, maintained and supported by the MySQL team at Oracle" (on Oracle Linux/RedHat)[⬞](https://stackoverflow.com/questions/44854843/docker-is-there-any-difference-between-the-two-mysql-docker-images).

| Database    | Running a container |
|-------------|---------------------|
| TimescaleDB | `docker run --name timescaledb -p 5430:5430 -e POSTGRES_PASSWORD=admin -d timescale/timescaledb-postgis:latest-pg12` |
| PostgreSQL  | `docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=admin -d postgres:13` |
| MySQL 8     | `docker run --name mysql8 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=admin -d mysql:8` |
| MySQL 5.1   | `docker run --name mysql51 -p 3307:3306 -e MYSQL_ROOT_PASSWORD=admin -d opencdms/mysql:5.1.73` |
| Oracle      | `docker run --name oracle-xe -p 1521:1521 -e ORACLE_PWD=admin opencdms/oracle:18.4.0-xe` |

Nuke option: `docker rm local-mysql`

Running commands within a container (example resets Oracle XE password):
```
docker exec -it oracle-xe bash
./setPassword.sh admin
su oracle
sqlplus  # system / admin
```
