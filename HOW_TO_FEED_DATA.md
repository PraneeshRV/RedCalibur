# 📥 HOW TO FEED DATA TO THE FRONTEND

## Quick Guide: Input → Processing → Output

---

## 🎯 What You Can Input

### 1. **Targets**

The frontend accepts any of these target formats:

```javascript
// Domains
"example.com"
"subdomain.example.com"
"admin.company.org"

// IP Addresses
"192.168.1.1"
"10.0.0.50"
"203.0.113.42"

// URLs
"https://app.example.com"
"http://api.company.com/v1"
"https://admin.site.com/login"

// Ranges (for future)
"192.168.1.0/24"
"10.0.0.1-255"
```

### 2. **Objectives (Natural Language)**

The AI understands natural language. Here are examples:

```javascript
// SQL Injection
"Find all SQL injection vulnerabilities"
"Test for SQL injection in login forms"
"Identify database injection points"

// XSS
"Check for cross-site scripting vulnerabilities"
"Test all input fields for XSS"
"Find reflected and stored XSS"

// Comprehensive
"Comprehensive security assessment"
"Full penetration test"
"Complete vulnerability scan"

// Specific Areas
"Test authentication mechanisms"
"Check for sensitive data exposure"
"Enumerate subdomains and services"
"Test API endpoints for vulnerabilities"
"Check for broken access control"

// OWASP Top 10
"Test for OWASP Top 10 vulnerabilities"
"Check for security misconfigurations"
"Test for using components with known vulnerabilities"
```

### 3. **Context (Optional)**

You can provide additional context:

```javascript
{
  "target": "example.com",
  "message": "Find SQL injection",
  "context": {
    "application_type": "e-commerce",
    "authentication": "JWT tokens",
    "framework": "Django",
    "previous_findings": ["XSS in search"],
    "constraints": ["avoid DoS", "test after hours"]
  }
}
```

---

## 📤 What You Get Back

### 1. **AI Analysis**

The AI generates 2000-3000 character strategic analysis:

```
EXAMPLE OUTPUT:

## Strategic Analysis: SQL Injection Vulnerability Assessment

This penetration testing engagement focuses on example.com, 
an e-commerce platform built with Django framework. The objective 
implies focus on areas where user input interacts with the database 
(login forms, search bars, product pages, checkout process).

Recommended phases:
1. Reconnaissance → Identify all input endpoints
2. Vulnerability Scanning → Test for SQL injection with sqlmap
3. Manual Testing → Verify findings and test bypass techniques
4. Exploitation → Demonstrate impact with data extraction
5. Reporting → Document findings with remediation steps

The ReconAgent will identify all user-facing forms and API endpoints. 
ExploitAgent will use sqlmap with various payloads and tamper scripts.
Success criteria: Identify at least one exploitable SQL injection 
vulnerability with data extraction proof.

Risk considerations:
- Potential for database lockout if testing is too aggressive
- Need to avoid disrupting e-commerce operations
- Test during specified hours only
- Follow responsible disclosure procedures

Tools recommended:
- sqlmap for automated testing
- Burp Suite for manual verification
- Nikto for initial reconnaissance
- nmap for service enumeration
```

### 2. **Structured Results**

For workflows, you get structured JSON:

```json
{
  "success": true,
  "workflow": {
    "objective": "Find SQL injection",
    "target": "example.com",
    "workflow_type": "full"
  },
  "results": {
    "Planner": {
      "plan": "...",
      "agents": ["Recon", "Exploit", "Reporting"],
      "phases": ["reconnaissance", "scanning", "exploitation"]
    },
    "Recon": {
      "tools": ["nmap", "subfinder", "httpx"],
      "findings": {...}
    },
    "Exploit": {
      "vulnerabilities": [...],
      "risk_level": "high",
      "exploitability": "easy"
    },
    "Reporting": {
      "summary": "...",
      "recommendations": [...]
    }
  },
  "history": [
    {
      "agent": "Planner",
      "action": "created_strategy",
      "result": {...},
      "timestamp": "2025-10-09T..."
    }
  ]
}
```

---

## 🔄 Complete Data Flow

### Step-by-Step Process

```
1. USER INPUT (Frontend)
   └─ Target: "example.com"
   └─ Message: "Find SQL injection"
   
2. FRONTEND PROCESSING
   └─ Validates input
   └─ Sends HTTP POST to /api/chat
   
3. BACKEND API
   └─ Receives request
   └─ Routes to PlannerAgent
   
4. AI AGENT (Gemini)
   └─ Analyzes objective
   └─ Generates strategy
   └─ Returns analysis
   
5. BACKEND RESPONSE
   └─ Formats results
   └─ Adds metadata
   └─ Returns to frontend
   
6. FRONTEND DISPLAY
   └─ Shows AI analysis
   └─ Displays suggestions
   └─ Updates UI
   
7. USER SEES OUTPUT
   └─ Strategic analysis
   └─ Recommended agents
   └─ Suggested workflow
```

---

## 💻 API Usage Examples

### Example 1: Simple Chat

**Input:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find SQL injection vulnerabilities",
    "target": "example.com"
  }'
```

**Output:**
```json
{
  "success": true,
  "response": "## Strategic Analysis: SQL Injection...",
  "suggested_agents": ["Recon", "Exploit"],
  "suggested_workflow": "full",
  "ai_enabled": true,
  "timestamp": "2025-10-09T12:34:56.789Z"
}
```

### Example 2: Execute Single Agent

**Input:**
```bash
curl -X POST http://localhost:8000/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "recon",
    "objective": "Enumerate services",
    "target": "192.168.1.1"
  }'
```

**Output:**
```json
{
  "success": true,
  "agent": "recon",
  "result": {
    "tools": ["nmap", "masscan"],
    "strategy": "Port scan followed by service detection",
    "commands": ["nmap -sV -sC 192.168.1.1"]
  },
  "thought": {
    "analysis": "For IP address target, immediate port scanning...",
    "action": "execute_reconnaissance",
    "timestamp": "2025-10-09T12:34:56.789Z"
  },
  "ai_enabled": true
}
```

### Example 3: Full Workflow

**Input:**
```bash
curl -X POST http://localhost:8000/api/workflow/execute \
  -H "Content-Type: application/json" \
  -d '{
    "objective": "Comprehensive security assessment",
    "target": "webapp.example.com",
    "workflow_type": "full"
  }'
```

**Output:**
```json
{
  "success": true,
  "workflow": {
    "objective": "Comprehensive security assessment",
    "target": "webapp.example.com",
    "workflow_type": "full"
  },
  "results": {
    "Planner": {...},
    "Recon": {...},
    "Exploit": {...},
    "Reporting": {...}
  },
  "history": [
    {"agent": "Planner", "action": "...", "result": {...}},
    {"agent": "Recon", "action": "...", "result": {...}},
    {"agent": "Exploit", "action": "...", "result": {...}},
    {"agent": "Reporting", "action": "...", "result": {...}}
  ],
  "agents_used": 4,
  "timestamp": "2025-10-09T12:34:56.789Z"
}
```

---

## 🎨 Frontend Input Methods

### Method 1: Chat Interface

```javascript
// User types in chat:
Target: example.com
Message: Find XSS vulnerabilities

// Frontend sends:
{
  "message": "Find XSS vulnerabilities",
  "target": "example.com"
}

// AI responds with analysis
```

### Method 2: Workflow Form

```javascript
// User fills form:
Target: [192.168.1.1]
Objective: [Port scan and service enumeration]
Button: [Execute Full Workflow]

// Frontend sends:
{
  "objective": "Port scan and service enumeration",
  "target": "192.168.1.1",
  "workflow_type": "full"
}

// Returns structured results
```

### Method 3: WebSocket Streaming

```javascript
// User clicks "Execute Full Workflow (Real-time)"
const ws = new WebSocket('ws://localhost:8000/ws/workflow');

ws.send(JSON.stringify({
  "objective": "Security assessment",
  "target": "example.com",
  "workflow_type": "full"
}));

// Receives real-time updates:
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  // Updates:
  // 1. workflow_start
  // 2. agent_start (Planner)
  // 3. agent_complete (Planner + analysis)
  // 4. agent_start (Recon)
  // 5. agent_complete (Recon + analysis)
  // ... and so on
};
```

---

## 📊 Data Formats

### Input Format

```typescript
interface ChatInput {
  message: string;        // Required: Natural language objective
  target?: string;        // Optional: Target specification
  context?: {            // Optional: Additional context
    [key: string]: any;
  };
}

interface WorkflowInput {
  objective: string;      // Required: What to do
  target: string;         // Required: Where to do it
  workflow_type: string;  // Required: "full" | "recon_only" | "exploit_only"
}

interface AgentInput {
  agent_type: string;     // Required: "planner" | "recon" | "exploit" | "reporting"
  objective: string;      // Required: What to do
  target?: string;        // Optional: Target
  context?: object;       // Optional: Context
}
```

### Output Format

```typescript
interface ChatOutput {
  success: boolean;
  response: string;              // AI-generated analysis
  suggested_agents: string[];    // Recommended agents
  suggested_workflow: string;    // Recommended workflow type
  ai_enabled: boolean;
  timestamp: string;
}

interface WorkflowOutput {
  success: boolean;
  workflow: object;              // Original request
  results: {                     // Results from each agent
    [agentName: string]: object;
  };
  history: Array<{              // Execution history
    agent: string;
    action: string;
    result: object;
    timestamp: string;
  }>;
  agents_used: number;
  timestamp: string;
}
```

---

## 🎯 Real-World Examples

### Example 1: E-Commerce Site Assessment

**Input:**
```
Target: shop.example.com
Message: Perform security assessment focusing on payment processing
```

**AI Output:**
```
Strategic focus on PCI-DSS compliance areas:
1. Payment form injection testing
2. Session management analysis
3. SSL/TLS configuration review
4. Sensitive data exposure checks

Recommended tools:
- Burp Suite for intercepting payment requests
- SQLMap for database injection testing
- SSLyze for SSL/TLS analysis
- Nikto for web server vulnerabilities

Priority: Payment processing endpoints (highest risk)
```

### Example 2: API Security Testing

**Input:**
```
Target: api.company.com/v2
Message: Test REST API for authentication and authorization vulnerabilities
```

**AI Output:**
```
API Security Testing Strategy:

Phase 1: Endpoint Discovery
- Use gobuster to find all API endpoints
- Analyze OpenAPI/Swagger documentation if available

Phase 2: Authentication Testing
- Test JWT token manipulation
- Check for token expiration
- Test refresh token security
- Verify logout mechanism

Phase 3: Authorization Testing
- IDOR (Insecure Direct Object Reference)
- Broken access control
- Privilege escalation

Tools: Postman, Burp Suite, jwt_tool, OWASP ZAP
```

### Example 3: Internal Network Assessment

**Input:**
```
Target: 192.168.1.0/24
Message: Internal network penetration test
```

**AI Output:**
```
Internal Network Assessment Plan:

Reconnaissance:
- nmap full network scan (-sn, -sV, -sC)
- Service enumeration on all hosts
- NetBIOS/SMB enumeration
- SNMP community string testing

Vulnerability Assessment:
- Nessus scan for known vulnerabilities
- Manual testing of discovered services
- Check for default credentials
- Test for weak protocols (telnet, FTP)

Exploitation:
- Metasploit for known vulnerabilities
- Password attacks on discovered services
- Lateral movement opportunities
```

---

## 🚀 Quick Reference

### Send Chat Message
```javascript
POST /api/chat
{
  "message": "Your objective here",
  "target": "your-target.com"
}
```

### Execute Workflow
```javascript
POST /api/workflow/execute
{
  "objective": "Your objective",
  "target": "your-target.com",
  "workflow_type": "full"
}
```

### Real-time Streaming
```javascript
ws://localhost:8000/ws/workflow
Send: {
  "objective": "...",
  "target": "...",
  "workflow_type": "full"
}
```

---

## ✅ Summary

**You Can Feed:**
- Any target (domain/IP/URL)
- Natural language objectives
- Additional context

**You Get Back:**
- AI strategic analysis (2000-3000 chars)
- Tool recommendations
- Execution plan
- Risk assessment
- Suggested next steps

**Through:**
- Chat interface (natural language)
- Workflow interface (structured)
- WebSocket (real-time streaming)

**The AI understands and generates professional pentesting strategies! 🎯**
