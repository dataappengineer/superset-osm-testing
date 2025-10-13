#!/bin/bash

# Initialize Superset Database and Create Admin User
echo "=== Initializing Superset Database ==="

# Upgrade database to latest schema
superset db upgrade

echo "=== Creating Admin User ==="
# Create admin user (only if it doesn't exist)
superset fab create-admin \
    --username admin \
    --firstname Admin \
    --lastname User \
    --email admin@superset.com \
    --password admin

echo "=== Loading Example Data ==="
# Load example datasets (optional)
superset load_examples

echo "=== Initializing Superset ==="
# Initialize Superset (create default roles and permissions)
superset init

echo "=== Starting Superset Server ==="
# Start the Gunicorn server
exec gunicorn --bind 0.0.0.0:8088 --workers 4 --timeout 60 --limit-request-line 0 --limit-request-field_size 0 "superset.app:create_app()"