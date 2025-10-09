#!/bin/bash

# RedCalibur AI - Complete Stack Startup Script
# Starts Backend API + Frontend Dev Server

echo "🚀 Starting RedCalibur AI Platform..."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "api/agent_api.py" ]; then
    echo -e "${RED}Error: Please run this script from the RedCalibur root directory${NC}"
    exit 1
fi

# Check Python dependencies
echo "📦 Checking Python dependencies..."
python3 -c "import fastapi, uvicorn, google.generativeai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    pip install fastapi uvicorn[standard] websockets google-generativeai python-dotenv
fi

# Check Node dependencies
echo "📦 Checking Node dependencies..."
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}Installing Node dependencies...${NC}"
    cd frontend && npm install && cd ..
fi

# Check for Gemini API key
if [ ! -f ".env" ] || ! grep -q "GEMINI_API_KEY" .env; then
    echo -e "${RED}Warning: GEMINI_API_KEY not found in .env${NC}"
    echo "AI features may not work. Add your key to .env file"
fi

echo ""
echo -e "${GREEN}✅ All dependencies checked${NC}"
echo ""

# Create a script to run both servers
cat > /tmp/redcalibur_start.sh << 'EOF'
#!/bin/bash

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# Start backend
echo "🔧 Starting Backend API (Port 8000)..."
cd /home/crimson/Praneesh/RedCalibur
python3 api/agent_api.py > /tmp/redcalibur_backend.log 2>&1 &
BACKEND_PID=$!

sleep 3

# Check if backend started
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start. Check /tmp/redcalibur_backend.log"
    exit 1
fi

echo "✅ Backend running on http://localhost:8000"
echo ""

# Start frontend
echo "🎨 Starting Frontend (Port 5173)..."
cd /home/crimson/Praneesh/RedCalibur/frontend
npm run dev > /tmp/redcalibur_frontend.log 2>&1 &
FRONTEND_PID=$!

sleep 5

# Check if frontend started
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "❌ Frontend failed to start. Check /tmp/redcalibur_frontend.log"
    kill $BACKEND_PID
    exit 1
fi

echo "✅ Frontend running on http://localhost:5173"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 RedCalibur AI Platform is READY!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Open your browser:"
echo "   → http://localhost:5173/"
echo ""
echo "📚 Backend API docs:"
echo "   → http://localhost:8000/docs"
echo ""
echo "📝 Logs:"
echo "   → Backend: /tmp/redcalibur_backend.log"
echo "   → Frontend: /tmp/redcalibur_frontend.log"
echo ""
echo "⌨️  Press Ctrl+C to stop all servers"
echo ""

# Wait for both processes
wait
EOF

chmod +x /tmp/redcalibur_start.sh
/tmp/redcalibur_start.sh
