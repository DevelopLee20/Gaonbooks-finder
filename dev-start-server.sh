#!/bin/bash
# start_server.sh
# Starting FastAPI Server

cd "$(dirname "$0")/fullstack/backend"

echo "Starting FastAPI server..."

poetry run uvicorn app.main:app --reload --host 0.0.0.0
