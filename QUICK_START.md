# RedCalibur - Quick Start Guide

## Installation

```bash
cd /home/crimson/Praneesh/RedCalibur
source redcalibur-env/bin/activate
```

## Available Commands

### 🔍 Enumeration

**Basic Service Scan**
```bash
redcalibur enumerate --target 192.168.1.1
```

**With Banner Grabbing**
```bash
redcalibur enumerate --target example.com --banner
```

**With Directory Enumeration**
```bash
redcalibur enumerate --target example.com --dir-enum http://example.com
```

**Custom Ports**
```bash
redcalibur enumerate --target 192.168.1.1 --ports 80,443,22,3306,5432
```

### 🛡️ Vulnerability Scanning

**Scan by Software Name**
```bash
redcalibur vuln-scan --software apache --version 2.4.41
redcalibur vuln-scan --software nginx --version 1.18.0
redcalibur vuln-scan --software openssh --version 8.2
```

**Scan Target System**
```bash
redcalibur vuln-scan --target 192.168.1.1 --ports 80,443,22
```

**Lookup Specific CVE**
```bash
redcalibur vuln-scan --cve-id CVE-2021-44228  # Log4Shell
redcalibur vuln-scan --cve-id CVE-2014-0160   # Heartbleed
```

### 🎯 Automated Penetration Testing

**Full Automated Pentest**
```bash
redcalibur auto-pentest --target 192.168.1.1 --domain example.com
```

**Target Only (No Domain)**
```bash
redcalibur auto-pentest --target 10.0.0.5
```

**Custom Output Name**
```bash
redcalibur auto-pentest --target 192.168.1.1 --output my_pentest_2025
```

### 📊 Existing Features

**Domain Reconnaissance**
```bash
redcalibur domain --target example.com --all
redcalibur domain --target example.com --whois --dns --ssl
```

**Network Scanning**
```bash
redcalibur scan --target 192.168.1.1 --ports 80,443,22
redcalibur scan --target example.com --shodan
```

**Username OSINT**
```bash
redcalibur username --target johndoe --platforms twitter,linkedin,github
```

**URL Scanning**
```bash
redcalibur urlscan --url http://example.com
```

**File OSINT**
```bash
redcalibur file-osint extract-doc-meta --path /path/to/document.pdf
redcalibur file-osint extract-exif --path /path/to/image.jpg
```

## Output Locations

All results are saved to: `reports/`

**File Naming Convention:**
- `enumeration_YYYYMMDD_HHMMSS.json`
- `vulnerability_scan_YYYYMMDD_HHMMSS.json`
- `pentest_report_YYYYMMDD_HHMMSS.json`
- `pentest_report_YYYYMMDD_HHMMSS.md`

## Common Use Cases

### 1. Quick Security Check
```bash
# Scan a web server for vulnerabilities
redcalibur enumerate --target example.com --ports 80,443
redcalibur vuln-scan --target example.com --ports 80,443
```

### 2. Full Infrastructure Audit
```bash
# Complete pentest with all phases
redcalibur auto-pentest --target 192.168.1.100 --domain example.com
```

### 3. CVE Research
```bash
# Look up specific vulnerabilities
redcalibur vuln-scan --cve-id CVE-2021-44228
redcalibur vuln-scan --software log4j --version 2.14.1
```

### 4. Web Application Testing
```bash
# Enumerate web directories and check for vulnerabilities
redcalibur enumerate --target example.com --dir-enum http://example.com
redcalibur vuln-scan --software apache --version 2.4.41
```

## Tips & Best Practices

### Rate Limiting
- NVD API: 5 requests per 30 seconds (without API key)
- Add delays between scans for large target lists
- Use specific version numbers to reduce API calls

### Target Specification
- IP addresses: `192.168.1.1`
- Hostnames: `example.com`
- URLs for dir-enum: `http://example.com` or `https://example.com`

### Port Selection
- Leave ports blank to use default common ports
- Specify custom ports: `--ports 80,443,22,3306`
- Use ranges: `--ports 1-1000` (for custom scripts)

### Output Management
- Check `reports/` directory for all saved results
- JSON files for programmatic processing
- Markdown files for human-readable reports

## Troubleshooting

### Import Errors
```bash
# Activate virtual environment first
source redcalibur-env/bin/activate
```

### NVD API Errors
- **403 Forbidden**: Rate limit exceeded, wait 30 seconds
- **Timeout**: Check internet connection
- **No results**: Verify software name spelling

### Permission Issues
- Ensure write access to `reports/` directory
- Run as appropriate user for network scans

## Getting Help

```bash
# General help
redcalibur --help

# Command-specific help
redcalibur enumerate --help
redcalibur vuln-scan --help
redcalibur auto-pentest --help
```

## Example Workflow

```bash
# 1. Activate environment
source redcalibur-env/bin/activate

# 2. Run reconnaissance
redcalibur domain --target example.com --all

# 3. Enumerate services
redcalibur enumerate --target example.com --banner

# 4. Check for vulnerabilities
redcalibur vuln-scan --target example.com

# 5. Generate comprehensive pentest report
redcalibur auto-pentest --target example.com

# 6. Check results
ls -lh reports/
```

## Real-World Examples

### Example 1: Apache Server Audit
```bash
redcalibur vuln-scan --software apache --version 2.4.41
# Output: Found 3 CVEs (1 HIGH, 2 MEDIUM)
```

### Example 2: Log4Shell Detection
```bash
redcalibur vuln-scan --cve-id CVE-2021-44228
# Output: Detailed Log4Shell vulnerability information
```

### Example 3: Network Enumeration
```bash
redcalibur enumerate --target 192.168.1.0/24 --ports 80,443,22
# Output: Services on multiple hosts
```

---

**Remember:** Always ensure you have proper authorization before scanning any systems!
