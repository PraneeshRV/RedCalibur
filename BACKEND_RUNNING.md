# ✅ BACKEND IS NOW RUNNING!

## Current Status

🟢 **Backend API**: Running on http://localhost:8000
🟢 **All 4 AI Agents**: Active with Gemini AI
🟢 **API Endpoints**: Working correctly

---

## What Was Fixed

The issue was that the backend needed to run with the **virtual environment activated**.

### Solution Applied:
```bash
source redcalibur-env/bin/activate
uvicorn api.agent_api:app --host 0.0.0.0 --port 8000
```

Also fixed: Removed `get_capabilities()` call that was causing Internal Server Error.

---

## Quick Start Commands

### Start Backend Only:
```bash
cd /home/crimson/Praneesh/RedCalibur
./start_backend.sh
```

### Start Full Platform (Backend + Frontend):
```bash
cd /home/crimson/Praneesh/RedCalibur
./start_platform.sh
```

### Check Backend Status:
```bash
curl http://localhost:8000/
curl http://localhost:8000/api/agents/status
```

### View Backend Logs:
```bash
tail -f /tmp/redcalibur_backend.log
```

### Stop Backend:
```bash
pkill -f "uvicorn api.agent_api"
```

---

## Test the API

### 1. Check Root Endpoint
```bash
curl -s http://localhost:8000/ | python3 -m json.tool
```

**Expected Output:**
```json
{
    "name": "RedCalibur AI Agent API",
    "version": "1.0.0",
    "status": "operational",
    "ai_enabled": true,
    "timestamp": "2025-10-09T..."
}
```

### 2. Check Agents Status
```bash
curl -s http://localhost:8000/api/agents/status | python3 -m json.tool
```

**Expected Output:**
```json
{
    "agents": [
        {
            "name": "planner",
            "type": "PlannerAgent",
            "ai_enabled": true,
            "model": "models/gemini-2.0-flash",
            "memory_size": 0
        },
        ... (3 more agents)
    ],
    "total_agents": 4,
    "ai_enabled": true
}
```

### 3. Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test SQL injection", "target": "example.com"}' | python3 -m json.tool
```

**Expected:** AI-generated strategic analysis

---

## Frontend Setup

The backend is running. Now you need to start the frontend:

### Option 1: Use the Complete Platform Script
```bash
./start_platform.sh
```
This starts both backend and frontend together.

### Option 2: Manual Frontend Start
```bash
cd frontend
npm run dev
```

Then open: **http://localhost:5173/**

---

## API Documentation

Once the backend is running, you can view interactive API docs:

**Swagger UI:**
```
http://localhost:8000/docs
```

**ReDoc:**
```
http://localhost:8000/redoc
```

---

## Current Backend Process

```bash
# Check if backend is running
ps aux | grep uvicorn

# Check port 8000
lsof -i :8000

# Check logs
tail -f /tmp/redcalibur_backend.log
```

---

## Scripts Created

1. **`start_backend.sh`** - Start backend only
2. **`start_platform.sh`** - Start backend + frontend
3. Both scripts:
   - Activate virtual environment automatically
   - Start services in background
   - Display status
   - Handle cleanup

---

## Next Steps

1. ✅ Backend is running
2. 🔄 Start frontend:
   ```bash
   cd frontend
   npm run dev
   ```
3. 🌐 Open browser: http://localhost:5173/
4. 🎯 Start using the platform!

---

## Troubleshooting

### Backend stops immediately?
```bash
# Check logs for errors
tail -50 /tmp/redcalibur_backend.log
```

### Port 8000 already in use?
```bash
# Kill existing process
pkill -f "uvicorn api.agent_api"

# Or kill by port
kill -9 $(lsof -t -i:8000)
```

### Virtual environment issues?
```bash
# Recreate venv if needed
python3 -m venv redcalibur-env
source redcalibur-env/bin/activate
pip install fastapi uvicorn[standard] websockets google-generativeai python-dotenv
```

---

## ✅ Summary

**Backend Status: RUNNING ✅**
- URL: http://localhost:8000
- Agents: 4 AI agents active
- Model: Gemini 2.0 Flash
- Logs: /tmp/redcalibur_backend.log

**Next: Start the frontend and you're ready to go!**

```bash
cd frontend && npm run dev
```
