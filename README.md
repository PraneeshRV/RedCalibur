# RedCalibur 🗡️

> "Forged at the intersection of artificial intelligence and offensive cybersecurity."

**RedCalibur** is a professional, AI-powered red teaming toolkit designed to automate  and enhance various phases of penetration testing, with a primary focus on comprehensive OSINT (Open Source Intelligence) reconnaissance. It leverages machine learning and large language models (LLMs) to supercharge ethical hacking workflows.

This project serves both as a practical cybersecurity tool and as a demonstration of applying neural networks and AI in cybersecurity for academic purposes.

---
## 🚀 Quickstart (cloned repo)

Prerequisites
- Python 3.10+ (3.11/3.12/3.13 supported)
- Node.js 18+ and npm

1) Clone and enter the folder
```bash
git clone https://github.com/PraneeshRV/RedCalibur.git
cd RedCalibur
```

2) Create and activate a virtual environment, install deps
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
python -m pip install -r api/requirements.txt
```

3) Configure environment variables (optional but recommended)
```bash
cp .env.example .env
# edit .env and add keys as needed: SHODAN_API_KEY, VIRUSTOTAL_API_KEY, GEMINI_API_KEY
# RedCalibur — AI‑Powered Red Teaming Toolkit

> Forged at the intersection of artificial intelligence and offensive security.

RedCalibur is a professional, extensible red teaming toolkit with an integrated web UI and a FastAPI backend. It automates common offensive workflows (recon, enumeration, vulnerability analysis, exploitation research, and reporting) and augments results with AI (Google Gemini) for faster, insight‑driven assessments.

This project is for authorized security testing and research only.

---

## Highlights

- Full‑stack app: Next.js 15 (TypeScript, Tailwind) + FastAPI
- 12 ready‑to‑use tools available from the UI and API
- AI assistance via Google Gemini for analysis, suggestions, and report drafting
- Clean output artifacts in `reports/` and logs in `logs/`
- Linux‑friendly and CLI‑friendly library under `redcalibur/`

---

## What’s inside

- Frontend: `redcalibur-nextjs/` (Next.js 15)
- Backend API: `api/tools_api.py` (FastAPI)
- Core library: `redcalibur/` (enumeration, vuln scanning, reporting, etc.)
- Outputs: `reports/` (JSON/PDF/MD), `logs/`

### AI usage (at a glance)
- Nmap results: AI explains risk/next steps (when GEMINI_API_KEY is set)
- Subdomain enumeration: AI suggests likely subdomains for a target
- Vulnerability analysis: AI drafts impact/mitigation from findings
- Exploit search: AI surfaces relevant CVEs/exploits from a query
- Payload generation: AI proposes testing payloads based on context
- Web crawl/headers: AI flags common misconfigurations
- WHOIS/Recon: AI summarizes key risks and takeaways
- Phishing detection & Password audit: AI provides safety guidance
- Report generation: AI composes a readable executive summary

---

## Requirements

- Linux recommended
- Python 3.10+
- Node.js 18+ and npm
- Optional system tools: `nmap`, `whois`, `dig` (install via your package manager)
- A Google Gemini API key (set `GEMINI_API_KEY`)

---

## Quick start

1) Clone
```bash
git clone https://github.com/PraneeshRV/RedCalibur.git
cd RedCalibur
```

2) Python env and deps
```bash
python3 -m venv redcalibur-env
source redcalibur-env/bin/activate
pip install -U pip
pip install -r requirements.txt
```

3) Node deps (UI)
```bash
cd redcalibur-nextjs
npm install
cd ..
```

4) Environment
```bash
cp .env.example .env  # then edit and add your GEMINI_API_KEY
```

5) Run
```bash
# Terminal 1 — Backend
source redcalibur-env/bin/activate
uvicorn api.tools_api:app --host 0.0.0.0 --port 8000

# Terminal 2 — Frontend
cd redcalibur-nextjs
npm run dev
```

- UI: http://localhost:3000 (auto‑selects 3001 if busy)
- API: http://localhost:8000 (docs at /docs)

Optional: one‑command start (if present)
```bash
./start.sh
```
Logs: `/tmp/redcalibur_backend.log`, `/tmp/redcalibur_frontend.log`

---

## Using the web app

- Open the app and pick a tool from the left (Recon, Exploitation, Analysis, Reporting)
- Enter a target (domain/IP/URL) and Run
- See live output and an AI analysis panel
- Generated artifacts are saved in `reports/`

Good first runs:
- DNS enumeration on `google.com`
- WHOIS lookup on a domain you own
- Vulnerability analysis using a product/version or a target host
- Report generator to produce a Markdown/PDF summary

---

## API reference (FastAPI)

All tools accept a JSON body: `{ "target": "<domain|ip|url|query>" }`

- GET `/` → API metadata
- GET `/health` → `{ status, ai }`
- POST `/api/tools/nmap` → Port/service scan (+ AI summary)
- POST `/api/tools/subdomain` → AI‑suggested subdomains list
- POST `/api/tools/portscan` → Fast TCP scan
- POST `/api/tools/whois` → WHOIS lookup (+ AI summary)
- POST `/api/tools/dns` → DNS enumeration (A/AAAA/MX/NS/TXT/SOA)
- POST `/api/tools/vulnscan` → AI‑powered vulnerability analysis
- POST `/api/tools/exploits` → Exploit/CVE search by keyword
- POST `/api/tools/payload` → AI payload generation
- POST `/api/tools/webcrawl` → Basic header/crawl checks (+ AI)
- POST `/api/tools/phishing` → URL phishing heuristics (+ AI)
- POST `/api/tools/password` → Password policy/safety audit (+ AI)
- POST `/api/tools/report` → AI report generation

Example (DNS):
```bash
curl -s -X POST http://localhost:8000/api/tools/dns \
  -H 'Content-Type: application/json' \
  -d '{"target":"google.com"}'
```

---

## Project structure (simplified)

```
RedCalibur/
├─ api/
│  └─ tools_api.py            # FastAPI backend (12 tools)
├─ redcalibur/                # Core Python library
│  ├─ enumeration/
│  ├─ vulnerability_scanning/
│  ├─ reporting/
│  └─ cli.py
├─ redcalibur-nextjs/         # Next.js 15 web UI
├─ reports/                   # Output artifacts (JSON/PDF/MD)
├─ logs/                      # Runtime logs
├─ requirements.txt
├─ README.md
└─ start.sh                   # Optional helper (starts both services)
```

---

## Troubleshooting

- Frontend doesn’t start: check `/tmp/redcalibur_frontend.log`; `npm run dev` will auto‑pick a free port
- Backend errors on AI: ensure `.env` has `GEMINI_API_KEY` and internet access
- `nmap`/`whois` not found: install via your package manager (e.g., `sudo apt install nmap whois dnsutils`)
- Port in use: stop prior processes (`pkill -f uvicorn` / `pkill -f "next dev"`), or let the UI choose 3001
- CVE/NVD rate limits: scans backoff automatically; try again later

---

## Development

```bash
# Lint/format config can be added; tests live under tests/
pytest -q
```

---

## Security & ethics

- Use only on systems you own or have explicit permission to test
- Follow responsible disclosure and applicable laws
- Built‑in delays and safe defaults help avoid accidental stress on targets

> Disclaimer: This toolkit is for educational and authorized testing purposes only. Unauthorized use is illegal and unethical.

---

## Contributing

PRs and issues are welcome. Please open an issue to discuss larger changes.

## License

MIT — see `LICENSE`

---

**RedCalibur** — forging the future of AI‑assisted red teaming.
