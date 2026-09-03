#!/bin/bash

# AURA - Database Migration & Restore Script
# This script restores the AURA PostgreSQL dump into a target PostgreSQL database.

echo "==========================================="
echo " AURA PostgreSQL Database Migration Script "
echo "==========================================="

if [ -z "$1" ]; then
    echo "Usage: ./migrate.sh <TARGET_DATABASE_URL>"
    echo "Example: ./migrate.sh postgres://user:password@localhost:5432/new_aura_db"
    exit 1
fi

TARGET_DB_URL="$1"
DUMP_FILE="aura_db_export.sql"

if [ ! -f "$DUMP_FILE" ]; then
    echo "Error: Dump file '$DUMP_FILE' not found in the current directory."
    exit 1
fi

echo "Connecting to target database and applying migration..."
# We use psql to execute the SQL dump against the target DB.
psql "$TARGET_DB_URL" -f "$DUMP_FILE"

if [ $? -eq 0 ]; then
    echo "==========================================="
    echo "✅ Migration completed successfully!"
    echo "The AURA database has been restored."
    echo "==========================================="
else
    echo "==========================================="
    echo "❌ Migration encountered errors."
    echo "Please check your database connection string and ensure the target database exists."
    echo "==========================================="
fi
