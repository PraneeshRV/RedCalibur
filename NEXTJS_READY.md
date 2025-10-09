# 🚀 RedCalibur AI - Next.js Edition

**Professional Full-Stack Security Platform with Integrated Frontend & Backend**

## 🎯 What's New

This is a **complete Next.js application** that integrates:
- ✅ **Frontend UI** (React + TypeScript + Tailwind CSS)
- ✅ **API Routes** (Next.js serverless functions)
- ✅ **Backend Proxy** (Connects to Python FastAPI backend)
- ✅ **Production-Ready** (Single unified application)

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Next.js App (Port 3000)          │
│  ┌──────────────┐  ┌──────────────┐│
│  │   Frontend   │  │  API Routes  ││
│  │  (React UI)  │  │   (Proxy)    ││
│  └──────────────┘  └──────┬───────┘│
└────────────────────────────┼────────┘
                             │ HTTP
                             ▼
                ┌────────────────────────┐
                │  Python Backend        │
                │  FastAPI (Port 8000)   │
                │  ┌──────────────────┐  │
                │  │  AI Agents       │  │
                │  │  • Planner       │  │
                │  │  • Recon         │  │
                │  │  • Exploit       │  │
                │  │  • Reporting     │  │
                │  └──────────────────┘  │
                └────────────────────────┘
                           │
                           ▼
                  Gemini 2.0 Flash AI
```

## 🚀 Quick Start

### **One Command to Start Everything:**

```bash
./start_nextjs.sh
```

This will:
1. ✅ Start Python Backend (Port 8000)
2. ✅ Start Next.js App (Port 3000)
3. ✅ Open browser automatically

### **Access the Platform:**

🌐 **Main Application:** http://localhost:3000

## 📁 Project Structure

```
redcalibur-nextjs/
├── app/
│   ├── api/                    # Next.js API Routes (Backend Proxy)
│   │   ├── agents/route.ts     # GET /api/agents - List AI agents
│   │   ├── chat/route.ts       # POST /api/chat - Chat with agents
│   │   ├── workflow/route.ts   # POST /api/workflow - Execute workflows
│   │   └── health/route.ts     # GET /api/health - Health check
│   │
│   ├── components/             # React Components
│   │   ├── ChatInterface.tsx   # AI Chat UI
│   │   └── WorkflowExecutor.tsx # Workflow execution UI
│   │
│   ├── page.tsx               # Main page (Chat + Workflow tabs)
│   ├── layout.tsx             # Root layout
│   └── globals.css            # Global styles
│
├── .env.local                 # Environment config
└── package.json               # Dependencies
```

## 🎨 Features

### 1. **Chat Interface**
- 💬 Real-time conversation with AI agents
- 🤖 Auto-select or manually choose agents
- 📝 Beautiful message history
- ⚡ Live agent status indicators

### 2. **Workflow Executor**
- 🔄 Automated reconnaissance workflows
- 📊 Step-by-step progress tracking
- 📈 Visual status indicators
- 📄 JSON results display

### 3. **Modern UI**
- 🎨 Cybersecurity-themed design (Red & Black)
- ✨ Glassmorphism effects
- 📱 Fully responsive
- 🌙 Dark mode optimized

## 🔧 API Endpoints

### Frontend Routes (Next.js)
- `GET /` - Main application
- `GET /api/agents` - List AI agents
- `POST /api/chat` - Send chat message
- `POST /api/workflow` - Execute workflow
- `GET /api/workflow?id=<workflow_id>` - Get workflow status
- `GET /api/health` - System health check

### Backend Routes (Python FastAPI - Auto-proxied)
- Automatically proxied through Next.js API routes
- No CORS issues
- Unified domain

## 🛠️ Development

### Start Development Mode:
```bash
cd redcalibur-nextjs
npm run dev
```

### Build for Production:
```bash
npm run build
npm start
```

## 📦 Technologies Used

**Frontend:**
- ⚛️ Next.js 15 (App Router)
- 📘 TypeScript
- 🎨 Tailwind CSS
- 🎯 Lucide React Icons
- ⚡ React Hooks

**Backend:**
- 🐍 Python FastAPI
- 🤖 Google Gemini AI (2.0 Flash)
- 🔄 Async/Await
- 📡 WebSocket support

## 🎯 Benefits Over Separate Frontend/Backend

✅ **Single Port** - Everything on http://localhost:3000
✅ **No CORS Issues** - API routes handle proxying
✅ **Better Performance** - Server-side rendering available
✅ **Production Ready** - Easy deployment to Vercel/Netlify
✅ **TypeScript** - Type safety across frontend & API routes
✅ **SEO Friendly** - Next.js optimizations
✅ **Hot Reload** - Fast development iteration

## 📊 Workflow Examples

### Reconnaissance Workflow:
```bash
Target: example.com
 ├── 🔍 Planning (AI determines strategy)
 ├── 📡 Reconnaissance (Port scan, DNS lookup)
 ├── 🔎 Analysis (Vulnerability assessment)
 └── 📄 Reporting (Generate PDF/JSON report)
```

### Chat Examples:
```
User: "Scan 192.168.1.1 for open ports"
Agent: [Recon Agent processes request with AI]

User: "Analyze vulnerabilities in example.com"
Agent: [Exploit Agent provides security assessment]
```

## 🔒 Security Notes

- ⚠️ This is a **security testing tool** - use responsibly
- 🔑 Store API keys in `.env` files (never commit them)
- 🎯 Only test systems you have permission to assess
- 📜 Follow ethical hacking guidelines

## 🐛 Troubleshooting

### Backend won't start:
```bash
# Check if virtual environment is activated
source redcalibur-env/bin/activate

# Check backend logs
tail -f /tmp/redcalibur_backend.log
```

### Frontend won't start:
```bash
# Check Next.js logs
tail -f /tmp/redcalibur_nextjs.log

# Reinstall dependencies
cd redcalibur-nextjs
rm -rf node_modules package-lock.json
npm install
```

### Port already in use:
```bash
# Kill processes on port 3000
lsof -ti:3000 | xargs kill -9

# Kill processes on port 8000
lsof -ti:8000 | xargs kill -9
```

## 📚 Documentation

- **Backend API:** http://localhost:8000/docs
- **Next.js:** https://nextjs.org/docs
- **Gemini AI:** https://ai.google.dev/

## 🎉 Ready to Use!

Your professional, production-ready security platform is complete!

```bash
./start_nextjs.sh
```

Then open: **http://localhost:3000** 🚀
