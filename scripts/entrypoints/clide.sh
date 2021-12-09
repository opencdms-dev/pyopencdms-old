#!/bin/bash
set -e
POSTGRES="psql --username ${POSTGRES_USER}"

echo "Creating database role: clideadmin"
$POSTGRES <<-EOSQL
CREATE USER clideadmin;
EOSQL

echo "Creating database role: clidegui"
$POSTGRES <<-EOSQL
CREATE USER clidegui;
EOSQL

echo "Creating database role: clide"
$POSTGRES <<-EOSQL
CREATE USER clide;
EOSQL

echo "Creating database role: datacomp"
$POSTGRES <<-EOSQL
CREATE USER datacomp;
EOSQL


echo "Creating database: clideDB"

$POSTGRES <<EOSQL
CREATE DATABASE clideDB OWNER postgres;
EOSQL
