from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import json
from typing import Optional
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="RedCalibur Red Teaming API",
    version="2.0.0",
    description="AI-Powered Red Teaming Toolkit Backend"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
else:
    model = None

class ToolRequest(BaseModel):
    target: str

@app.get("/")
async def root():
    return {
        "name": "RedCalibur Red Teaming API",
        "version": "2.0.0",
        "status": "operational",
        "ai_enabled": model is not None,
        "tools": 12
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "ai": model is not None}

@app.post("/api/tools/nmap")
async def nmap_scan(request: ToolRequest):
    """Nmap port scanner with AI enhancement"""
    try:
        # Basic nmap scan
        result = subprocess.run(
            ["nmap", "-sV", "-T4", request.target],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout if result.returncode == 0 else result.stderr
        
        # AI enhancement
        if model and output:
            prompt = f"""Analyze this Nmap scan result and provide security insights:

{output}

Provide:
1. Summary of open ports
2. Potential security risks
3. Recommended actions"""
            
            response = model.generate_content(prompt)
            output += f"\n\n--- AI Analysis ---\n{response.text}"
        
        return {"success": True, "output": output}
    except subprocess.TimeoutExpired:
        return {"success": False, "output": "Scan timed out"}
    except FileNotFoundError:
        return {"success": False, "output": "Nmap not installed. Install with: sudo apt install nmap"}
    except Exception as e:
        return {"success": False, "output": f"Error: {str(e)}"}

@app.post("/api/tools/subdomain")
async def subdomain_enum(request: ToolRequest):
    """Subdomain enumeration with AI"""
    try:
        if not model:
            return {"success": False, "output": "AI model not configured"}
        
        prompt = f"""Generate a list of potential subdomains for {request.target}. 
        Include common subdomains like:
        - www, mail, ftp, admin, portal, api, dev, staging
        - Also suggest creative ones based on the domain purpose
        
        Format: one subdomain per line, just the subdomain name"""
        
        response = model.generate_content(prompt)
        subdomains = response.text
        
        # Try DNS lookup for each
        found_subdomains = []
        for sub in subdomains.split('\n'):
            sub = sub.strip()
            if sub and not sub.startswith('-'):
                full_domain = f"{sub}.{request.target}" if sub != 'www' else request.target
                try:
                    result = subprocess.run(
                        ["host", full_domain],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if "has address" in result.stdout:
                        found_subdomains.append(f"✓ {full_domain} - FOUND")
                except:
                    pass
        
        output = "Subdomain Enumeration Results:\n\n"
        output += "\n".join(found_subdomains) if found_subdomains else "No subdomains found"
        output += f"\n\nAI Suggested Subdomains:\n{subdomains}"
        
        return {"success": True, "output": output}
    except Exception as e:
        return {"success": False, "output": f"Error: {str(e)}"}

@app.post("/api/tools/portscan")
async def port_scan(request: ToolRequest):
    """Fast port scanner"""
    try:
        common_ports = "21,22,23,25,53,80,110,143,443,445,3306,3389,5432,8080,8443"
        result = subprocess.run(
            ["nmap", "-p", common_ports, "--open", request.target],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout if result.returncode == 0 else result.stderr
        return {"success": True, "output": output}
    except FileNotFoundError:
        return {"success": False, "output": "Nmap not installed"}
    except Exception as e:
        return {"success": False, "output": f"Error: {str(e)}"}

@app.post("/api/tools/whois")
async def whois_lookup(request: ToolRequest):
    """WHOIS domain information"""
    try:
        result = subprocess.run(
            ["whois", request.target],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        output = result.stdout if result.returncode == 0 else result.stderr
        
        if model and output:
            prompt = f"""Analyze this WHOIS data and extract key security information:

{output[:2000]}

Provide:
1. Domain owner/registrar
2. Registration/expiry dates
3. Security concerns
4. Privacy protection status"""
            
            response = model.generate_content(prompt)
            output += f"\n\n--- AI Analysis ---\n{response.text}"
        
        return {"success": True, "output": output}
    except FileNotFoundError:
        return {"success": False, "output": "whois not installed. Install with: sudo apt install whois"}
    except Exception as e:
        return {"success": False, "output": f"Error: {str(e)}"}

@app.post("/api/tools/dns")
async def dns_enum(request: ToolRequest):
    """DNS enumeration"""
    try:
        record_types = ["A", "AAAA", "MX", "NS", "TXT", "SOA"]
        output = f"DNS Records for {request.target}:\n\n"
        
        for rtype in record_types:
            result = subprocess.run(
                ["dig", "+short", request.target, rtype],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.stdout.strip():
                output += f"{rtype} Records:\n{result.stdout}\n"
        
        return {"success": True, "output": output}
    except FileNotFoundError:
        return {"success": False, "output": "dig not installed. Install with: sudo apt install dnsutils"}
    except Exception as e:
        return {"success": False, "output": f"Error: {str(e)}"}

@app.post("/api/tools/vulnscan")
async def vuln_scan(request: ToolRequest):
    """AI-powered vulnerability analysis"""
    try:
        if not model:
            return {"success": False, "output": "AI model not configured"}
        
        prompt = f"""Perform a security assessment for {request.target}:

1. Common vulnerabilities to check
2. OWASP Top 10 considerations
3. Potential attack vectors
4. Recommended security tests
5. Compliance considerations

Be specific and actionable."""
        
        response = model.generate_content(prompt)
        return {"success": True, "output": response.text}
    except Exception as e:
        return {"success": False, "output": f"Error: {str(e)}"}

@app.post("/api/tools/exploits")
async def exploit_search(request: ToolRequest):
    """Search for exploits and CVEs"""
    try:
        if not model:
            return {"success": False, "output": "AI model not configured"}
        
        prompt = f"""Search for known exploits and vulnerabilities for: {request.target}

Provide:
1. Recent CVEs
2. Known exploits
3. Exploit frameworks (Metasploit, etc.)
4. Mitigation strategies
5. Patch recommendations"""
        
        response = model.generate_content(prompt)
        return {"success": True, "output": response.text}
    except Exception as e:
        return {"success": False, "output": f"Error: {str(e)}"}

@app.post("/api/tools/payload")
async def payload_gen(request: ToolRequest):
    """AI-powered payload generation"""
    try:
        if not model:
            return {"success": False, "output": "AI model not configured"}
        
        prompt = f"""Generate security testing payloads for: {request.target}

Include:
1. SQL injection payloads
2. XSS payloads
3. Command injection tests
4. Path traversal attempts
5. Usage instructions

Note: For authorized testing only."""
        
        response = model.generate_content(prompt)
        return {"success": True, "output": response.text}
    except Exception as e:
        return {"success": False, "output": f"Error: {str(e)}"}

@app.post("/api/tools/webcrawl")
async def web_crawl(request: ToolRequest):
    """Web application crawling"""
    try:
        # Simple curl-based crawl
        result = subprocess.run(
            ["curl", "-sL", "-I", request.target],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        output = f"HTTP Headers for {request.target}:\n\n{result.stdout}"
        
        if model:
            prompt = f"""Analyze these HTTP headers for security issues:

{result.stdout}

Check for:
1. Missing security headers
2. Server information disclosure
3. Cookie security
4. HTTPS/TLS configuration"""
            
            response = model.generate_content(prompt)
            output += f"\n\n--- Security Analysis ---\n{response.text}"
        
        return {"success": True, "output": output}
    except Exception as e:
        return {"success": False, "output": f"Error: {str(e)}"}

@app.post("/api/tools/phishing")
async def phishing_detect(request: ToolRequest):
    """Phishing URL analysis"""
    try:
        if not model:
            return {"success": False, "output": "AI model not configured"}
        
        prompt = f"""Analyze this URL for phishing indicators: {request.target}

Check for:
1. Domain reputation
2. URL structure anomalies
3. Known phishing patterns
4. Risk score (1-10)
5. Recommendations"""
        
        response = model.generate_content(prompt)
        return {"success": True, "output": response.text}
    except Exception as e:
        return {"success": False, "output": f"Error: {str(e)}"}

@app.post("/api/tools/password")
async def password_audit(request: ToolRequest):
    """Password security audit"""
    try:
        if not model:
            return {"success": False, "output": "AI model not configured"}
        
        prompt = f"""Analyze password security for: {request.target}

Provide:
1. Common password policies
2. Brute force resistance
3. Dictionary attack vectors
4. Password strength requirements
5. Best practices"""
        
        response = model.generate_content(prompt)
        return {"success": True, "output": response.text}
    except Exception as e:
        return {"success": False, "output": f"Error: {str(e)}"}

@app.post("/api/tools/report")
async def report_gen(request: ToolRequest):
    """Generate penetration test report"""
    try:
        if not model:
            return {"success": False, "output": "AI model not configured"}
        
        prompt = f"""Generate a professional penetration test report template for: {request.target}

Include:
1. Executive Summary
2. Methodology
3. Findings (High/Medium/Low)
4. Technical Details
5. Recommendations
6. Conclusion

Format professionally."""
        
        response = model.generate_content(prompt)
        return {"success": True, "output": response.text}
    except Exception as e:
        return {"success": False, "output": f"Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
