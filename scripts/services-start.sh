#!/bin/bash

# This script starts the core service of the application.

set -e  # Exit immediately if a command exits with a non-zero status

# Navigate to the core service directory
cd "$(dirname "$0")/../services/core-service"

# Install dependencies
pip install -r requirements.txt

sleep 3

# Start the core service in the background
uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload

# Wait a few seconds for the server to start
sleep 3

# Check if the service is running by hitting the health check endpoints
curl --request GET -sL http://localhost:8080/api/v1/health/db || {
    echo "Health check failed. Core service may not have started properly."
}

cd "$(dirname "$0")/../services/ai-service"

# Install dependencies for the AI service
pip install -r requirements.txt

# Start the AI service in the background
uvicorn src.main:app --host 0.0.0.0 --port 8081 --reload --log-level debug

# Wait a few seconds for the AI service to start
sleep 10

