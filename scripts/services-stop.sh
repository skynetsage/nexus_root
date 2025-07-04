#!/bin/bash

# This script stops the core service of the application.

echo "Stopping All services"

# Find and kill uvicorn process running on the expected app
PIDS=$(ps aux | grep 'uvicorn src.main:app' | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
  echo "No core service process found."
else
  echo "Killing process IDs: $PIDS"
  kill $PIDS
  echo "Core service stopped."
fi
