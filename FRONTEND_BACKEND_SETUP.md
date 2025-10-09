# 🚀 FRONTEND + BACKEND SETUP GUIDE

## Complete Integration: AI Agents → FastAPI → React Frontend

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│  React Frontend (Port 5173)                     │
│  - Chat Interface                               │
│  - Workflow Execution                           │
│  - Real-time WebSocket Updates                  │
└─────────────┬───────────────────────────────────┘
              │ HTTP/WebSocket
┌─────────────▼───────────────────────────────────┐
│  FastAPI Backend (Port 8000)                    │
│  - REST API Endpoints                           │
│  - WebSocket for Real-time                      │
│  - Agent Orchestration                          │
└─────────────┬───────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────┐
│  AI Multi-Agent System                          │
│  - PlannerAgent (Gemini AI)                     │
│  - ReconAgent (Gemini AI)                       │
│  - ExploitAgent (Gemini AI)                     │
│  - ReportingAgent (Gemini AI)                   │
└─────────────────────────────────────────────────┘
```

---

## 📦 What We've Created

### 1. **Backend API** (`api/agent_api.py`)
- ✅ FastAPI server with CORS enabled
- ✅ REST endpoints for agent execution
- ✅ WebSocket for real-time workflow updates
- ✅ Chat interface with AI reasoning
- ✅ Workflow orchestration
- ✅ Execution history tracking

### 2. **Frontend UI** (`frontend/src/AIAgentsApp.jsx`)
- ✅ Modern React interface with Lucide icons
- ✅ Chat interface for natural language interaction
- ✅ Workflow tab for structured execution
- ✅ Real-time agent status display
- ✅ WebSocket integration for live updates
- ✅ Professional red team styling

### 3. **Styling** (`frontend/src/AIAgentsApp.css`)
- ✅ Cybersecurity-themed design
- ✅ Red/black color scheme
- ✅ Glassmorphism effects
- ✅ Responsive layout
- ✅ Smooth animations

---

## 🚀 Quick Start

### Step 1: Install Backend Dependencies

```bash
cd /home/crimson/Praneesh/RedCalibur

# Install FastAPI and WebSocket support
pip install fastapi uvicorn[standard] websockets python-multipart

# Install AI agents (already done)
pip install google-generativeai python-dotenv
```

### Step 2: Install Frontend Dependencies

```bash
cd frontend

# Install React dependencies
npm install lucide-react
```

### Step 3: Update Frontend Main Entry

Add the AI Agents App to your frontend:

```javascript
// frontend/src/main.jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import AIAgentsApp from './AIAgentsApp'
import './AIAgentsApp.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AIAgentsApp />
  </React.StrictMode>,
)
```

### Step 4: Start Backend Server

Open Terminal 1:
```bash
cd /home/crimson/Praneesh/RedCalibur
python api/agent_api.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Start Frontend Dev Server

Open Terminal 2:
```bash
cd /home/crimson/Praneesh/RedCalibur/frontend
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Step 6: Open Browser

Navigate to: **http://localhost:5173/**

---

## 🎯 Features You Can Use Now

### 1. **Chat Interface**

Talk to RedCalibur AI naturally:

**Examples:**
```
Target: example.com
Message: "Analyze this target for SQL injection vulnerabilities"

Target: 192.168.1.1
Message: "Perform comprehensive reconnaissance"

Target: webapp.acme.com
Message: "Find all vulnerabilities and create exploitation plan"
```

### 2. **Full Workflow Execution**

Execute complete penetration test workflow:
- Enter target
- Enter objective
- Click "Execute Full Workflow"
- Watch all 4 agents work in sequence

### 3. **Real-time Streaming**

Use WebSocket for live updates:
- Click "Execute Full Workflow (Real-time)"
- See each agent execute live
- Watch AI reasoning in real-time

### 4. **Agent Status Monitoring**

Top dashboard shows:
- ✅ AI Active/Inactive status
- Model name (gemini-2.0-flash)
- Memory size
- Agent capabilities

---

## 🔌 API Endpoints

### REST Endpoints

```bash
# Get agents status
GET http://localhost:8000/api/agents/status

# Execute single agent
POST http://localhost:8000/api/agent/execute
{
  "agent_type": "planner",
  "objective": "Find SQL injection",
  "target": "example.com"
}

# Execute full workflow
POST http://localhost:8000/api/workflow/execute
{
  "objective": "Security assessment",
  "target": "example.com",
  "workflow_type": "full"
}

# Chat with AI
POST http://localhost:8000/api/chat
{
  "message": "Analyze this target",
  "target": "example.com"
}

# Get execution history
GET http://localhost:8000/api/history

# Clear history
DELETE http://localhost:8000/api/history
```

### WebSocket Endpoint

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/workflow');

ws.send(JSON.stringify({
  objective: 'Security assessment',
  target: 'example.com',
  workflow_type: 'full'
}));

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // data.type: 'workflow_start', 'agent_start', 'agent_complete', 'workflow_complete'
};
```

---

## 🧪 Testing the Integration

### Test 1: Backend Health Check

```bash
curl http://localhost:8000/
```

Expected output:
```json
{
  "name": "RedCalibur AI Agent API",
  "version": "1.0.0",
  "status": "operational",
  "ai_enabled": true,
  "timestamp": "2025-10-09T..."
}
```

### Test 2: Agent Status

```bash
curl http://localhost:8000/api/agents/status
```

Expected: 4 agents with AI enabled

### Test 3: Chat Message

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test SQL injection", "target": "example.com"}'
```

Expected: AI-generated response with analysis

### Test 4: Frontend Connection

1. Open http://localhost:5173/
2. Should see 4 agent cards with "AI Active" status
3. Type message in chat
4. Should receive AI response

---

## 🎨 UI Features

### Visual Elements

- **Header**: Status bar with AI enabled indicator
- **Agent Cards**: Live status of all 4 agents
- **Chat Tab**: Natural language interaction
- **Workflow Tab**: Structured execution interface
- **Real-time Updates**: WebSocket streaming
- **History Tracking**: View past executions

### User Interactions

1. **Natural Chat**
   - Type target and objective
   - Get AI analysis
   - See suggested agents

2. **Structured Workflow**
   - Fill target and objective
   - Choose workflow type (Full/Recon/Exploit)
   - Execute and view results

3. **Real-time Execution**
   - Connect WebSocket
   - Execute workflow
   - Watch live agent updates

---

## 🎯 For Your Presentation

### Demo Flow

**1. Show the Interface** (30 seconds)
- Open http://localhost:5173/
- Point out 4 AI agents active
- Show Gemini AI enabled badge

**2. Chat Demo** (1 minute)
```
Target: demo.testfire.net
Message: "Find all SQL injection vulnerabilities"
```
- Show AI generates intelligent analysis
- Point out suggested agents
- Highlight strategic reasoning

**3. Full Workflow Demo** (2 minutes)
```
Target: testphp.vulnweb.com
Objective: "Comprehensive security assessment"
```
- Click "Execute Full Workflow (Real-time)"
- Watch all 4 agents execute live
- Show AI reasoning for each agent
- Display final results

**4. Key Talking Points**
- "Real AI reasoning, not templates"
- "Each agent uses Gemini 2.0 Flash"
- "Generates 2,000+ character strategic analysis"
- "Professional pentesting workflow"
- "Scalable multi-agent architecture"

---

## 🐛 Troubleshooting

### Backend won't start?
```bash
# Check port 8000 is free
lsof -i :8000

# Install missing dependencies
pip install fastapi uvicorn[standard] websockets
```

### Frontend won't connect?
```bash
# Check CORS settings in agent_api.py
# Ensure allow_origins includes your frontend URL

# Check frontend API URL
# In AIAgentsApp.jsx, API_BASE_URL should be http://localhost:8000
```

### AI not working?
```bash
# Verify .env has GEMINI_API_KEY
cat .env | grep GEMINI_API_KEY

# Test AI directly
python -c "from redcalibur.ai_core.agents import PlannerAgent; 
agent = PlannerAgent(); 
print(f'AI: {agent.use_ai}')"
```

### WebSocket not connecting?
- Check backend is running on port 8000
- Check browser console for errors
- Verify WebSocket endpoint: `ws://localhost:8000/ws/workflow`

---

## 📝 Next Steps

### Enhancements You Can Add

1. **Authentication**
   - Add JWT tokens
   - User sessions
   - API key management

2. **Real Tool Integration**
   - Connect to nmap, sqlmap, etc.
   - Execute real scans
   - Parse tool outputs with AI

3. **Reporting**
   - Generate PDF reports
   - Export to JSON/CSV
   - Email reports

4. **Advanced Features**
   - Multi-target scanning
   - Scheduled workflows
   - Result comparison
   - Vulnerability database

---

## ✅ Checklist

Before presentation:

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] All 4 agents showing "AI Active"
- [ ] Gemini API key in .env
- [ ] Test chat message works
- [ ] Test workflow execution works
- [ ] WebSocket real-time updates working
- [ ] Browser at http://localhost:5173/

---

## 🎉 You're Ready!

You now have a **complete, professional, AI-powered penetration testing platform**!

- ✅ Backend API with 8 endpoints
- ✅ Modern React frontend
- ✅ Real-time WebSocket updates
- ✅ 4 AI-powered agents
- ✅ Chat and workflow interfaces
- ✅ Professional UI/UX

**Start the servers and show your professors! 🚀**

```bash
# Terminal 1
python api/agent_api.py

# Terminal 2  
cd frontend && npm run dev

# Browser
http://localhost:5173/
```
