# ⚡ QUICK START - DO THIS NOW!

## 1️⃣ Start the Platform

```bash
cd /home/crimson/Praneesh/RedCalibur
./start_platform.sh
```

Wait ~10 seconds for both servers to start.

---

## 2️⃣ Open Browser

Navigate to:
```
http://localhost:5173/
```

You should see:
- ✅ RedCalibur AI header
- ✅ 4 agent cards (Planner, Recon, Exploit, Reporting)
- ✅ "🤖 AI Enabled" badge
- ✅ Chat and Workflow tabs

---

## 3️⃣ Try the Chat Interface

**Click the "Chat Interface" tab**

Type:
```
Target: demo.testfire.net
Message: Find SQL injection vulnerabilities
```

**Click Send** (or press Enter)

You'll see:
- Your message appears
- Loading indicator shows
- AI generates ~2000-3000 character strategic analysis
- Professional pentesting plan with tools and phases

---

## 4️⃣ Try Full Workflow

**Click the "Workflow" tab**

Fill in:
```
Target: testphp.vulnweb.com
Objective: Comprehensive security assessment
```

**Click "Execute Full Workflow (Real-time)"**

Watch:
- 🚀 Workflow starts
- ⏳ Planner agent executes
- ✅ Planner completes with AI analysis
- ⏳ Recon agent executes
- ✅ Recon completes with AI analysis
- ⏳ Exploit agent executes
- ✅ Exploit completes with AI analysis
- ⏳ Reporting agent executes
- ✅ Reporting completes with AI analysis
- 🎉 Workflow complete!

---

## 5️⃣ What to Show Your Professors

### Opening Statement
*"I've built an AI-powered penetration testing platform with a professional web interface. Let me show you..."*

### Demo 1: Chat Interface (1 minute)
1. Show the dashboard: "Here are our 4 AI agents, all using Gemini 2.0 Flash"
2. Enter target and objective in chat
3. Click send
4. Point out: "Watch the AI generate a strategic analysis..."
5. Scroll through response: "This is real AI reasoning, not templates"

### Demo 2: Live Workflow (1.5 minutes)
1. Switch to Workflow tab
2. Enter target and objective
3. Click "Execute Full Workflow (Real-time)"
4. Point out each agent as it executes:
   - "Planner creates the strategy"
   - "Recon gathers intelligence"
   - "Exploit identifies vulnerabilities"
   - "Reporting structures findings"
5. Show final results

### Key Points to Emphasize
- ✅ "Real AI integration using Google Gemini"
- ✅ "Multi-agent architecture with specialized roles"
- ✅ "Professional full-stack application"
- ✅ "Real-time WebSocket updates"
- ✅ "Production-ready interface"

---

## 🎯 Example Inputs to Try

### SQL Injection Testing
```
Target: webapp.example.com
Message: Test all forms for SQL injection vulnerabilities
```

### API Security
```
Target: api.company.com/v2
Message: Assess REST API security for authentication flaws
```

### Network Scanning
```
Target: 192.168.1.0/24
Message: Internal network penetration test
```

### Web Application
```
Target: https://shop.example.com
Message: E-commerce security assessment focusing on payment processing
```

### OWASP Top 10
```
Target: testphp.vulnweb.com
Message: Test for OWASP Top 10 vulnerabilities
```

---

## ✅ Success Indicators

You'll know it's working when:

1. **Dashboard shows:**
   - ✅ 4 agent cards visible
   - ✅ "AI Active" status on all agents
   - ✅ Model shows "models/gemini-2.0-flash"
   - ✅ "🤖 AI Enabled" badge in header

2. **Chat works:**
   - ✅ Messages send successfully
   - ✅ AI responds with 2000-3000 character analysis
   - ✅ Suggested agents appear
   - ✅ Professional formatting

3. **Workflow works:**
   - ✅ Real-time updates stream in
   - ✅ Each agent completes with analysis
   - ✅ Results show in structured format
   - ✅ History tracks all actions

---

## 🐛 If Something Doesn't Work

### Backend won't start
```bash
# Check if port 8000 is free
lsof -i :8000

# If something is using it, kill it
kill -9 $(lsof -t -i:8000)

# Try again
python api/agent_api.py
```

### Frontend won't start
```bash
cd frontend
npm install
npm run dev
```

### Can't see agents
- Refresh the page (F5)
- Check browser console for errors (F12)
- Verify backend is running: `curl http://localhost:8000/api/agents/status`

### AI not responding
```bash
# Check API key
cat .env | grep GEMINI_API_KEY

# Should show: GEMINI_API_KEY=AIzaSy...
```

---

## 📚 Documentation to Read

**Before demo:**
1. **START_HERE.md** - Complete usage guide
2. **FRONTEND_READY.md** - Quick reference

**After demo:**
3. **HOW_TO_FEED_DATA.md** - Input/output examples
4. **FRONTEND_BACKEND_SETUP.md** - Technical details
5. **COMPLETE_INTEGRATION_SUMMARY.md** - What was built

---

## 🎉 YOU'RE READY!

Everything is set up. Just:

```bash
./start_platform.sh
```

Then open `http://localhost:5173/` and show your professors!

**Good luck! 🚀✨**
