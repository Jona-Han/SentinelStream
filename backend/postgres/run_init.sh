#!/bin/bash

# Variables
DB_NAME="postgres"
DB_USER="postgres"
DB_PASSWORD="temppass"
DB_HOST="localhost"
DB_PORT="5432"
SQL_FILE="init.sql"

export PGPASSWORD=$DB_PASSWORD

psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f $SQL_FILE

unset PGPASSWORD
