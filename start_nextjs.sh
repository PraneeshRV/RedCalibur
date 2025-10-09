#!/bin/bash

cd /home/crimson/Praneesh/RedCalibur

echo "🚀 Starting RedCalibur AI - Next.js Edition"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    pkill -f "uvicorn api.agent_api" 2>/dev/null
    pkill -f "next dev" 2>/dev/null
    if [ -n "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ -n "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    exit 0
}

trap cleanup INT TERM

# Check for Gemini API key
if [ ! -f ".env" ] || ! grep -q "GEMINI_API_KEY" .env; then
    echo -e "${YELLOW}⚠️  Warning: GEMINI_API_KEY not found in .env${NC}"
    echo "AI features may not work. Add your key to .env file"
    echo ""
fi

# Start Python backend
echo "🔧 Starting Python Backend API (Port 8000)..."
pkill -f "uvicorn api.agent_api" 2>/dev/null
sleep 1

(source redcalibur-env/bin/activate && uvicorn api.agent_api:app --host 0.0.0.0 --port 8000) > /tmp/redcalibur_backend.log 2>&1 &
BACKEND_PID=$!

sleep 4

# Check if backend started
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend API running on http://localhost:8000 (PID: $BACKEND_PID)${NC}"
else
    echo -e "${RED}❌ Backend failed to start. Check /tmp/redcalibur_backend.log${NC}"
    tail -20 /tmp/redcalibur_backend.log
    exit 1
fi

echo ""

# Start Next.js frontend
echo "🎨 Starting Next.js Frontend (Port 3000)..."
cd redcalibur-nextjs
npm run dev > /tmp/redcalibur_nextjs.log 2>&1 &
FRONTEND_PID=$!

sleep 5

# Check if frontend started
if lsof -i :3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Next.js running on http://localhost:3000${NC}"
else
    echo -e "${RED}❌ Next.js failed to start. Check /tmp/redcalibur_nextjs.log${NC}"
    pkill -f "uvicorn api.agent_api"
    tail -20 /tmp/redcalibur_nextjs.log
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 RedCalibur AI Platform is READY!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Open your browser:"
echo "   → ${GREEN}http://localhost:3000/${NC}"
echo ""
echo "🔧 Backend API:"
echo "   → http://localhost:8000"
echo "   → http://localhost:8000/docs (API Documentation)"
echo ""
echo "📝 Logs:"
echo "   → Backend: /tmp/redcalibur_backend.log"
echo "   → Frontend: /tmp/redcalibur_nextjs.log"
echo ""
echo "⌨️  Press Ctrl+C to stop all servers"
echo ""

# Keep script running and wait for both processes
echo "Monitoring servers... (Backend PID: $BACKEND_PID, Frontend PID: $FRONTEND_PID)"
while kill -0 $BACKEND_PID 2>/dev/null && kill -0 $FRONTEND_PID 2>/dev/null; do
    sleep 2
done

# If we get here, one of the processes died
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}❌ Backend process died! Check /tmp/redcalibur_backend.log${NC}"
fi
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}❌ Next.js process died! Check /tmp/redcalibur_nextjs.log${NC}"
fi

cleanup
