#!/bin/bash

# Initialize Superset Database and Create Admin User
# This script runs inside the Superset container

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

echo "=== Superset Initialization Complete ==="
echo "Access Superset at: http://localhost:8088"
echo "Username: admin"
echo "Password: admin"