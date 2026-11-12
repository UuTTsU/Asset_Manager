#!/bin/sh
set -e  # Exit immediately if any command fails

echo "Running database migrations..."
alembic upgrade head

echo "Starting FastAPI..."
exec "$@"