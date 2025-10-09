#!/bin/bash

cd /home/crimson/Praneesh/RedCalibur

echo "🚀 Starting RedCalibur - Red Teaming Toolkit"
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    pkill -f "uvicorn api.tools_api" 2>/dev/null
    pkill -f "next dev" 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# Check for Gemini API key
if [ ! -f ".env" ] || ! grep -q "GEMINI_API_KEY" .env; then
    echo -e "${YELLOW}⚠️  Warning: GEMINI_API_KEY not found in .env${NC}"
    echo "AI features will not work. Add your Gemini API key to .env"
    echo ""
fi

# Start Python backend
echo "🔧 Starting Backend API (Port 8000)..."
pkill -f "uvicorn api.tools_api" 2>/dev/null
sleep 1

(source redcalibur-env/bin/activate && uvicorn api.tools_api:app --host 0.0.0.0 --port 8000) > /tmp/redcalibur_api.log 2>&1 &
BACKEND_PID=$!

sleep 4

if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend API running (PID: $BACKEND_PID)${NC}"
else
    echo -e "${RED}❌ Backend failed. Check /tmp/redcalibur_api.log${NC}"
    tail -20 /tmp/redcalibur_api.log
    exit 1
fi

echo ""

# Start Next.js
echo "🎨 Starting Next.js Frontend (Port 3000)..."
cd redcalibur-nextjs
npm run dev > /tmp/redcalibur_frontend.log 2>&1 &
FRONTEND_PID=$!

sleep 6

if lsof -i :3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend running${NC}"
else
    echo -e "${RED}❌ Frontend failed. Check /tmp/redcalibur_frontend.log${NC}"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 RedCalibur Red Teaming Toolkit Ready!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Open: ${GREEN}http://localhost:3000${NC}"
echo "🔧 API: http://localhost:8000/docs"
echo ""
echo "🛠️  12 Tools Available:"
echo "   • Nmap Scanner"
echo "   • Subdomain Enumeration"
echo "   • Port Scanner"
echo "   • WHOIS Lookup"
echo "   • DNS Enumeration"
echo "   • Vulnerability Scanner"
echo "   • Exploit Search"
echo "   • Payload Generator"
echo "   • Web Crawler"
echo "   • Phishing Detection"
echo "   • Password Audit"
echo "   • Report Generator"
echo ""
echo "⚠️  For authorized testing only!"
echo "⌨️  Press Ctrl+C to stop"
echo ""

while kill -0 $BACKEND_PID 2>/dev/null && kill -0 $FRONTEND_PID 2>/dev/null; do
    sleep 2
done

cleanup
