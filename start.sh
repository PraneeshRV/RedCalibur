#!/bin/bash

# RedCalibur Quick Start Script
# Run this to start everything

cd /home/crimson/Praneesh/RedCalibur

echo "🚀 Starting RedCalibur Red Teaming Toolkit..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Kill any existing processes
echo "🧹 Cleaning up old processes..."
pkill -f "uvicorn api.tools_api" 2>/dev/null
pkill -f "next dev" 2>/dev/null
sleep 2

# Start Backend
echo ""
echo "🔧 Starting Backend API..."
source redcalibur-env/bin/activate
nohup uvicorn api.tools_api:app --host 0.0.0.0 --port 8000 > /tmp/redcalibur_backend.log 2>&1 &
BACKEND_PID=$!

sleep 4

# Check backend
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend running on http://localhost:8000${NC}"
else
    echo -e "${RED}❌ Backend failed. Check: tail -f /tmp/redcalibur_backend.log${NC}"
    exit 1
fi

# Start Frontend
echo ""
echo "🎨 Starting Frontend..."
cd redcalibur-nextjs
nohup npm run dev > /tmp/redcalibur_frontend.log 2>&1 &
FRONTEND_PID=$!

sleep 6

# Find which port frontend is using
if lsof -i :3000 > /dev/null 2>&1; then
    PORT=3000
elif lsof -i :3001 > /dev/null 2>&1; then
    PORT=3001
else
    echo -e "${RED}❌ Frontend failed. Check: tail -f /tmp/redcalibur_frontend.log${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Frontend running on http://localhost:$PORT${NC}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}🎉 RedCalibur is READY!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "📱 ${GREEN}Open: http://localhost:$PORT${NC}"
echo ""
echo "🛠️  12 Tools Available:"
echo "   • DNS Enumeration"
echo "   • Subdomain Discovery"
echo "   • Vulnerability Scanner"
echo "   • Exploit Search"
echo "   • Payload Generator"
echo "   • Web Crawler"
echo "   • Phishing Detection"
echo "   • Report Generator"
echo "   • And more..."
echo ""
echo "📊 Backend: http://localhost:8000/docs"
echo ""
echo "📝 Logs:"
echo "   Backend: tail -f /tmp/redcalibur_backend.log"
echo "   Frontend: tail -f /tmp/redcalibur_frontend.log"
echo ""
echo "🛑 To stop: pkill -f uvicorn && pkill -f 'next dev'"
echo ""
echo -e "${YELLOW}⚠️  For authorized security testing only!${NC}"
