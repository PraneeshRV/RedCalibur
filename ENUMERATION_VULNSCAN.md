# RedCalibur - Enumeration & Vulnerability Scanning

## New Features Added

### 1. Service Enumeration (`enumerate`)
Detect and fingerprint services running on target systems.

**Features:**
- Port scanning with service detection
- Banner grabbing for version identification
- Directory enumeration on web servers
- Service version fingerprinting

**Usage:**
```bash
# Basic service enumeration
redcalibur enumerate --target 192.168.1.1

# With custom ports
redcalibur enumerate --target example.com --ports 80,443,22,3306

# With banner grabbing
redcalibur enumerate --target 192.168.1.1 --banner

# With directory enumeration
redcalibur enumerate --target example.com --dir-enum http://example.com
```

### 2. Vulnerability Scanning (`vuln-scan`)
Scan for known CVEs and vulnerabilities using free APIs.

**Data Sources:**
- NVD (National Vulnerability Database)
- CVE databases
- Exploit-DB references

**Usage:**
```bash
# Scan by software name
redcalibur vuln-scan --software apache --version 2.4.41

# Scan specific target
redcalibur vuln-scan --target 192.168.1.1 --ports 80,443

# Look up specific CVE
redcalibur vuln-scan --cve-id CVE-2021-44228
```

### 3. Automated Penetration Testing (`auto-pentest`)
Run a complete automated pentest workflow combining all features.

**Workflow Phases:**
1. **Reconnaissance** - Domain and network information gathering
2. **Enumeration** - Service detection and fingerprinting
3. **Vulnerability Scanning** - CVE detection and analysis
4. **Risk Assessment** - Automated risk level calculation

**Usage:**
```bash
# Basic automated pentest
redcalibur auto-pentest --target 192.168.1.1

# With domain reconnaissance
redcalibur auto-pentest --target 192.168.1.1 --domain example.com

# Custom output filename
redcalibur auto-pentest --target 192.168.1.1 --output my_pentest
```

## Module Structure

### Enumeration Module (`redcalibur/enumeration/`)
- `service_detector.py` - Service detection and fingerprinting
- `banner_grabber.py` - Network banner grabbing
- `directory_enumeration.py` - Web directory discovery

### Vulnerability Scanning Module (`redcalibur/vulnerability_scanning/`)
- `cve_scanner.py` - CVE database integration
- `service_vuln_check.py` - Service-specific vulnerability checks
- `exploit_finder.py` - Public exploit search

## Output Format

All commands save results in JSON format to the `reports/` directory with timestamps.

Example output structure:
```json
{
  "timestamp": "2025-10-09T...",
  "target": "192.168.1.1",
  "services": [...],
  "vulnerabilities": [...],
  "risk_summary": {
    "total_vulnerabilities": 5,
    "risk_level": "MEDIUM"
  }
}
```

## API Rate Limits

**NVD API:**
- No API key: 5 requests per 30 seconds
- With API key: 50 requests per 30 seconds

To avoid rate limits:
- Use specific version numbers when possible
- Add delays between scans
- Cache results locally

## Next Steps

Future enhancements planned:
- AI-powered vulnerability prioritization
- Automated exploit verification
- Integration with Metasploit modules
- Custom vulnerability signatures
- Machine learning for service detection
