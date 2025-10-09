#!/bin/bash

# RedCalibur Backend Startup Script
# Use this to start the backend API server

cd /home/crimson/Praneesh/RedCalibur

echo "🚀 Starting RedCalibur Backend API..."

# Activate virtual environment
source redcalibur-env/bin/activate

# Kill any existing backend process
pkill -f "uvicorn api.agent_api" 2>/dev/null

# Start backend
nohup uvicorn api.agent_api:app --host 0.0.0.0 --port 8000 > /tmp/redcalibur_backend.log 2>&1 &

# Wait for server to start
sleep 3

# Test if it's running
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Backend API started successfully!"
    echo ""
    echo "📍 Backend running at: http://localhost:8000"
    echo "📚 API docs at: http://localhost:8000/docs"
    echo "📝 Logs at: /tmp/redcalibur_backend.log"
    echo ""
    echo "Test it:"
    echo "  curl http://localhost:8000/"
    echo "  curl http://localhost:8000/api/agents/status"
else
    echo "❌ Failed to start backend. Check logs:"
    echo "  tail -f /tmp/redcalibur_backend.log"
    exit 1
fi
