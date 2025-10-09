# RedCalibur Security Tools Catalog

## 📚 Comprehensive Tool Collection (150+ Tools)

Based on analysis of HexStrike AI, PentAGI, and RedTeam-Tools, organized by MITRE ATT&CK framework.

---

## 🎯 MITRE ATT&CK Categories

### 1️⃣ Reconnaissance (24 tools)

#### 1.1 Active Scanning
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **nmap** | Network port scanner | ✅ Yes | HIGH |
| **masscan** | Fast port scanner | ✅ Yes | HIGH |
| **RustScan** | Modern port scanner | ❌ No | MEDIUM |
| **nuclei** | Vulnerability templates | ✅ Yes | HIGH |
| **httpx** | HTTP probe | ❌ No | MEDIUM |
| **naabu** | Fast port discovery | ❌ No | MEDIUM |

#### 1.2 OSINT & Information Gathering
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **theHarvester** | Email/subdomain enumeration | ❌ No | HIGH |
| **Shodan** | Internet-wide scanner | 🔌 API | HIGH |
| **spiderfoot** | OSINT automation | ❌ No | HIGH |
| **Maltego** | Link analysis | ❌ No | MEDIUM |
| **recon-ng** | Reconnaissance framework | ❌ No | HIGH |
| **OSRFramework** | Username search | ❌ No | LOW |
| **Social Analyzer** | Social media OSINT | ❌ No | MEDIUM |

#### 1.3 Subdomain Discovery
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **subfinder** | Subdomain discovery | ❌ No | HIGH |
| **assetfinder** | Find domains/subdomains | ❌ No | HIGH |
| **amass** | In-depth subdomain enum | ❌ No | HIGH |
| **Sublist3r** | Subdomain enumeration | ❌ No | MEDIUM |
| **knock** | Subdomain scanner | ❌ No | LOW |

#### 1.4 DNS & Network Enumeration
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **dnsenum** | DNS enumeration | ❌ No | MEDIUM |
| **dnsrecon** | DNS reconnaissance | ❌ No | MEDIUM |
| **fierce** | DNS scanner | ❌ No | LOW |
| **dnsdumpster** | DNS intelligence | 🌐 Web | MEDIUM |

---

### 2️⃣ Resource Development (12 tools)

#### 2.1 Payload Generation
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **msfvenom** | Payload generator | ✅ Yes | HIGH |
| **Veil** | Payload obfuscator | ❌ No | HIGH |
| **Shellter** | Dynamic shellcode injector | ❌ No | MEDIUM |
| **ScareCrow** | Payload creation | ❌ No | MEDIUM |
| **Donut** | Shellcode generation | ❌ No | HIGH |

#### 2.2 Infrastructure
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **Cobalt Strike** | C2 framework | ❌ Commercial | HIGH |
| **Covenant** | .NET C2 framework | ❌ No | HIGH |
| **Havoc** | Modern C2 framework | ❌ No | HIGH |
| **Empire** | PowerShell C2 | ❌ No | MEDIUM |

#### 2.3 Document Weaponization
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **EvilClippy** | MS Office malware | ❌ No | MEDIUM |
| **LuckyStrike** | Malicious Excel/Word | ❌ No | LOW |
| **MacroPack** | Macro obfuscation | ❌ No | MEDIUM |

---

### 3️⃣ Initial Access (10 tools)

#### 3.1 Password Attacks
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **Hydra** | Brute force tool | ✅ Yes | HIGH |
| **Medusa** | Parallel brute forcer | ❌ No | MEDIUM |
| **Patator** | Multi-purpose brute forcer | ❌ No | MEDIUM |
| **TREVORspray** | Azure AD password spray | ❌ No | HIGH |
| **CredKing** | Password spraying | ❌ No | MEDIUM |

#### 3.2 Phishing
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **Gophish** | Phishing framework | ❌ No | HIGH |
| **EvilGoPhish** | Enhanced Gophish | ❌ No | HIGH |
| **King Phisher** | Phishing campaign | ❌ No | MEDIUM |
| **CredSniper** | Credential harvester | ❌ No | MEDIUM |

#### 3.3 Exploitation
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **Metasploit** | Exploitation framework | ✅ Yes | HIGH |

---

### 4️⃣ Execution (13 tools)

#### 4.1 Command & Scripting
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **PowerShell Empire** | PowerShell framework | ❌ No | HIGH |
| **Impacket** | Python network tools | ❌ No | HIGH |
| **evil-winrm** | WinRM shell | ❌ No | HIGH |
| **CrackMapExec** | Swiss army knife | ❌ No | HIGH |

#### 4.1 Loaders & Injectors
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **Donut** | In-memory PE loader | ❌ No | HIGH |
| **pe_to_shellcode** | PE to shellcode | ❌ No | MEDIUM |
| **Charlotte** | C# weaponization | ❌ No | MEDIUM |
| **Freeze** | Payload obfuscation | ❌ No | MEDIUM |
| **Chameleon** | PowerShell obfuscation | ❌ No | MEDIUM |

#### 4.3 Remote Access
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **PsExec** | Remote execution | ❌ No | HIGH |
| **WMIOps** | WMI attack tools | ❌ No | MEDIUM |
| **SCShell** | Fileless lateral movement | ❌ No | MEDIUM |
| **SharpRDP** | RDP hijacking | ❌ No | MEDIUM |

---

### 5️⃣ Persistence (4 tools)

| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **SharPersist** | Windows persistence | ❌ No | HIGH |
| **Empire** | PowerShell agent | ❌ No | MEDIUM |
| **Impacket** | Network protocols | ❌ No | HIGH |
| **ligolo-ng** | Tunneling tool | ❌ No | MEDIUM |

---

### 6️⃣ Privilege Escalation (11 tools)

#### 6.1 Linux
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **LinPEAS** | Linux privilege escalation | ❌ No | HIGH |
| **LinEnum** | Linux enumeration | ❌ No | HIGH |
| **linux-exploit-suggester** | Exploit suggester | ❌ No | HIGH |
| **BeRoot** | Privilege escalation | ❌ No | MEDIUM |

#### 6.2 Windows
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **WinPEAS** | Windows privilege escalation | ❌ No | HIGH |
| **PowerUp** | PowerShell privilege esc | ❌ No | HIGH |
| **Certify** | AD certificate abuse | ❌ No | HIGH |
| **Rubeus** | Kerberos abuse | ❌ No | HIGH |
| **Watson** | Windows exploit suggester | ❌ No | HIGH |
| **SharpUp** | C# privilege escalation | ❌ No | MEDIUM |
| **PEASS-ng** | Privilege escalation suite | ❌ No | HIGH |

---

### 7️⃣ Defense Evasion (8 tools)

| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **Invoke-Obfuscation** | PowerShell obfuscation | ❌ No | HIGH |
| **Veil** | AV evasion framework | ❌ No | HIGH |
| **ScareCrow** | EDR evasion | ❌ No | HIGH |
| **Donut** | Shellcode loader | ❌ No | HIGH |
| **Freeze** | Anti-virus evasion | ❌ No | MEDIUM |
| **Shellter** | Dynamic PE infector | ❌ No | MEDIUM |
| **Chameleon** | AV bypass | ❌ No | MEDIUM |
| **AMSITrigger** | AMSI detection | ❌ No | MEDIUM |

---

### 8️⃣ Credential Access (11 tools)

#### 8.1 Credential Dumping
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **Mimikatz** | Credential extractor | ❌ No | HIGH |
| **LaZagne** | Password recovery | ❌ No | HIGH |
| **pypykatz** | Python Mimikatz | ❌ No | HIGH |
| **SharpDPAPI** | DPAPI abuse | ❌ No | MEDIUM |
| **Rubeus** | Kerberos attacks | ❌ No | HIGH |

#### 8.2 Password Cracking
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **hashcat** | GPU password cracker | ❌ No | HIGH |
| **John the Ripper** | Password cracker | ❌ No | HIGH |
| **Hydra** | Online brute force | ✅ Yes | HIGH |

#### 8.3 Man-in-the-Middle
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **Responder** | LLMNR/NBT-NS poisoner | ❌ No | HIGH |
| **Inveigh** | .NET Responder | ❌ No | MEDIUM |
| **mitm6** | IPv6 MITM | ❌ No | MEDIUM |

---

### 9️⃣ Discovery (6 tools)

#### 9.1 Active Directory
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **BloodHound** | AD attack paths | ❌ No | HIGH |
| **SharpHound** | BloodHound collector | ❌ No | HIGH |
| **ADRecon** | AD reconnaissance | ❌ No | HIGH |
| **PingCastle** | AD security audit | ❌ No | HIGH |

#### 9.2 Network & System
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **Snaffler** | Credential finder | ❌ No | MEDIUM |
| **linWinPwn** | AD/Windows enumeration | ❌ No | MEDIUM |

---

### 🔟 Lateral Movement (12 tools)

| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **CrackMapExec** | Swiss army knife | ❌ No | HIGH |
| **Impacket** | Network protocols | ❌ No | HIGH |
| **evil-winrm** | WinRM shell | ❌ No | HIGH |
| **PsExec** | Remote execution | ❌ No | HIGH |
| **WMIOps** | WMI operations | ❌ No | MEDIUM |
| **SCShell** | Fileless movement | ❌ No | MEDIUM |
| **Kerbrute** | Kerberos brute force | ❌ No | MEDIUM |
| **RDP** | RDP tools | ❌ No | MEDIUM |
| **ligolo-ng** | Tunneling | ❌ No | MEDIUM |
| **chisel** | TCP/UDP tunneling | ❌ No | MEDIUM |
| **SharpRDP** | RDP hijacking | ❌ No | MEDIUM |
| **SharpMove** | Lateral movement | ❌ No | LOW |

---

### 1️⃣1️⃣ Collection (3 tools)

| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **LaZagne** | Credential browser | ❌ No | HIGH |
| **scavenger** | Automated collector | ❌ No | MEDIUM |
| **SharpChromium** | Chrome data | ❌ No | MEDIUM |

---

### 1️⃣2️⃣ Command and Control (9 tools)

| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **Metasploit Framework** | Exploitation & C2 | ✅ Yes | HIGH |
| **Cobalt Strike** | Commercial C2 | ❌ Commercial | HIGH |
| **Havoc** | Modern C2 | ❌ No | HIGH |
| **Covenant** | .NET C2 | ❌ No | HIGH |
| **Empire** | PowerShell C2 | ❌ No | MEDIUM |
| **Sliver** | Go C2 | ❌ No | HIGH |
| **Merlin** | HTTP/2 C2 | ❌ No | MEDIUM |
| **Mythic** | Multi-agent C2 | ❌ No | MEDIUM |
| **Koadic** | Windows C2 | ❌ No | LOW |

---

### 1️⃣3️⃣ Exfiltration (5 tools)

| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **dnscat2** | DNS tunneling | ❌ No | HIGH |
| **Cloakify** | Data exfiltration | ❌ No | MEDIUM |
| **PyExfil** | Python exfiltration | ❌ No | MEDIUM |
| **DET** | Data exfiltration toolkit | ❌ No | MEDIUM |
| **Egress-Assess** | Exfiltration testing | ❌ No | LOW |

---

### 1️⃣4️⃣ Impact (4 tools)

| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **SharpShares** | Share manipulation | ❌ No | MEDIUM |
| **Invoke-DOSfuscation** | DOS obfuscation | ❌ No | LOW |
| **CrackMapExec** | Multi-purpose | ❌ No | HIGH |
| **Impacket** | Network attacks | ❌ No | HIGH |

---

## 🌐 Web Application Testing Tools

### Web Vulnerability Scanners
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **Burp Suite** | Web app security testing | ✅ Partial | HIGH |
| **ZAP (OWASP)** | Web app scanner | ❌ No | HIGH |
| **Nikto** | Web server scanner | ❌ No | HIGH |
| **Wapiti** | Web vulnerability scanner | ❌ No | MEDIUM |
| **nuclei** | Template-based scanner | ✅ Yes | HIGH |
| **WPScan** | WordPress scanner | ❌ No | HIGH |
| **Joomla Scanner** | Joomla vulnerability scanner | ❌ No | MEDIUM |

### SQL Injection
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **sqlmap** | Automated SQL injection | ✅ Yes | HIGH |
| **NoSQLMap** | NoSQL injection | ❌ No | MEDIUM |

### Web Fuzzing
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **ffuf** | Fast web fuzzer | ✅ Yes | HIGH |
| **gobuster** | Directory/file brute forcer | ❌ No | HIGH |
| **feroxbuster** | Recursive content discovery | ❌ No | HIGH |
| **wfuzz** | Web application fuzzer | ❌ No | MEDIUM |
| **dirb** | Web content scanner | ❌ No | LOW |
| **dirsearch** | Web path scanner | ❌ No | MEDIUM |

### XSS & Client-Side
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **XSStrike** | XSS detection suite | ❌ No | HIGH |
| **Dalfox** | XSS scanner | ❌ No | HIGH |
| **BruteXSS** | XSS brute forcer | ❌ No | MEDIUM |

---

## 🔐 Specialized Tools

### API Testing
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **Postman** | API testing | ❌ No | HIGH |
| **Insomnia** | REST client | ❌ No | MEDIUM |
| **OWASP ZAP API** | API security | ❌ No | HIGH |
| **REST-Attacker** | API fuzzer | ❌ No | MEDIUM |

### Cloud Security
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **ScoutSuite** | Multi-cloud auditing | ❌ No | HIGH |
| **Prowler** | AWS security assessment | ❌ No | HIGH |
| **Pacu** | AWS exploitation | ❌ No | HIGH |
| **CloudSploit** | Cloud security scanner | ❌ No | MEDIUM |

### Container Security
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **Trivy** | Container scanner | ❌ No | HIGH |
| **Clair** | Container vulnerability scan | ❌ No | MEDIUM |
| **Docker Bench** | Docker security audit | ❌ No | MEDIUM |

### Mobile Security
| Tool | Description | MCP Available | Priority |
|------|-------------|---------------|----------|
| **MobSF** | Mobile security framework | ❌ No | HIGH |
| **Frida** | Dynamic instrumentation | ❌ No | HIGH |
| **Objection** | Runtime mobile exploration | ❌ No | MEDIUM |

---

## 📦 Tool Integration Priority

### Phase 1: Core Tools (Weeks 1-2) ✅
1. nmap (MCP) - Network scanning
2. metasploit (MCP) - Exploitation
3. sqlmap (MCP) - SQL injection
4. nuclei (MCP) - Vulnerability scanning
5. Hydra (MCP) - Password attacks
6. ffuf (MCP) - Web fuzzing

### Phase 2: OSINT & Recon (Weeks 3-4)
7. theHarvester - Email/subdomain enum
8. subfinder - Subdomain discovery
9. amass - In-depth reconnaissance
10. Shodan API - Internet scanning
11. VirusTotal API - Threat intelligence
12. spiderfoot - OSINT automation

### Phase 3: Exploitation & Post-Exploit (Weeks 5-6)
13. Impacket - Network protocols
14. CrackMapExec - Lateral movement
15. Mimikatz - Credential dumping
16. BloodHound - AD attack paths
17. LinPEAS/WinPEAS - Privilege escalation
18. Rubeus - Kerberos attacks

### Phase 4: Web Application (Weeks 7-8)
19. Burp Suite (MCP) - Web testing
20. gobuster - Directory brute force
21. WPScan - WordPress scanning
22. XSStrike - XSS detection
23. Nikto - Web server scanning

### Phase 5: Advanced & Specialized (Weeks 9-10)
24. Empire - PowerShell C2
25. Covenant - .NET C2
26. Veil - AV evasion
27. ScareCrow - EDR evasion
28. Invoke-Obfuscation - Code obfuscation

---

## 🛠️ Tool Configuration Templates

### Example: Nmap Configuration
```yaml
tool: nmap
category: reconnaissance
mcp_server: nmap-mcp
default_args:
  scan_type: syn
  timing: T4
  version_detection: true
  os_detection: false
presets:
  quick:
    ports: "80,443,22,21,25"
    timing: T4
  full:
    ports: "1-65535"
    timing: T3
    scripts: "default,vuln"
  stealth:
    scan_type: fin
    timing: T2
    fragments: true
```

### Example: SQLMap Configuration
```yaml
tool: sqlmap
category: exploitation
mcp_server: sqlmap-mcp
default_args:
  level: 3
  risk: 2
  threads: 5
  timeout: 30
presets:
  aggressive:
    level: 5
    risk: 3
    tamper: "space2comment,between"
  stealth:
    level: 1
    risk: 1
    delay: 2
```

---

## 📊 Tool Execution Tracking

```python
# redcalibur/ai_core/tool_tracker.py

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

@dataclass
class ToolExecution:
    tool_name: str
    start_time: datetime
    end_time: datetime
    duration: float
    success: bool
    results: Dict
    agent: str

class ToolExecutionTracker:
    """Track all tool executions for reporting"""
    
    def __init__(self):
        self.executions: List[ToolExecution] = []
    
    def track(self, execution: ToolExecution):
        self.executions.append(execution)
    
    def get_summary(self) -> Dict:
        return {
            'total_executions': len(self.executions),
            'successful': sum(1 for e in self.executions if e.success),
            'failed': sum(1 for e in self.executions if not e.success),
            'tools_used': list(set(e.tool_name for e in self.executions)),
            'total_duration': sum(e.duration for e in self.executions)
        }
```

---

## 🎯 Next Steps

1. **Prioritize MCP integrations** (6 core tools first)
2. **Implement tool abstraction layer**
3. **Create configuration management**
4. **Build execution tracking**
5. **Add result caching**
6. **Implement rate limiting**
7. **Create tool documentation**

---

**Total Tools**: 150+
**MCP-Ready**: 8 tools
**High Priority**: 45 tools
**Medium Priority**: 62 tools
**Low Priority**: 43 tools

**Last Updated**: January 2025
**Maintainer**: RedCalibur Development Team
