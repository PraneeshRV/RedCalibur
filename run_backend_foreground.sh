#!/bin/bash

# Simple Backend Startup
# This script starts only the backend in the foreground so you can see logs

cd /home/crimson/Praneesh/RedCalibur

echo "🚀 Starting RedCalibur Backend API..."
echo ""
echo "This will run in the foreground. Press Ctrl+C to stop."
echo "Backend will be available at: http://localhost:8000"
echo ""

# Kill any existing backend
pkill -f "uvicorn api.agent_api" 2>/dev/null
sleep 1

# Activate venv and start
source redcalibur-env/bin/activate
uvicorn api.agent_api:app --host 0.0.0.0 --port 8000 --reload
