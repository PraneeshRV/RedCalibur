from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from redcalibur.config import Config, setup_logging
from redcalibur.osint.domain_infrastructure.whois_lookup import perform_whois_lookup
from redcalibur.osint.domain_infrastructure.dns_enumeration import enumerate_dns_records
from redcalibur.osint.domain_infrastructure.subdomain_discovery import discover_subdomains
from redcalibur.osint.domain_infrastructure.port_scanning import perform_port_scan
from redcalibur.osint.domain_infrastructure.ssl_tls_details import get_ssl_details
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import time
from redcalibur.osint.network_threat_intel.shodan_integration import perform_shodan_scan
from redcalibur.osint.user_identity.username_lookup import lookup_username
from redcalibur.osint.virustotal_integration import scan_url_full
from redcalibur.osint.url_health_check import basic_url_health
from redcalibur.osint.ai_enhanced.recon_summarizer import summarize_recon_data
from redcalibur.osint.ai_enhanced.local_summarizer import local_bullet_summary
from redcalibur.osint.ai_enhanced.risk_scoring import calculate_risk_score

logger = setup_logging()
config = Config()

app = FastAPI(title="RedCalibur API", version="0.1.0")

# CORS for dev convenience
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DomainRequest(BaseModel):
    target: str
    whois: bool = False
    dns: bool = False
    subdomains: bool = False
    ssl: bool = False
    all: bool = False


class ScanRequest(BaseModel):
    target: str
    ports: Optional[List[int]] = None
    shodan: bool = False


class UsernameRequest(BaseModel):
    target: str
    platforms: Optional[List[str]] = None


class URLScanRequest(BaseModel):
    url: str


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "time": datetime.now().isoformat()}


@app.post("/domain")
def domain_recon(req: DomainRequest):
    results: Dict[str, Any] = {"target": req.target, "timestamp": datetime.now().isoformat()}
    errors: Dict[str, Any] = {}

    tasks = []

    def wrap(name, fn, *args, **kwargs):
        try:
            res = fn(*args, **kwargs)
            results[name] = res
        except Exception as e:
            logger.error(f"{name} error: {e}")
            errors[name] = str(e)

    ex = ThreadPoolExecutor(max_workers=4)
    try:
        fut_to_name: Dict[Any, str] = {}
        if req.whois or req.all:
            fut = ex.submit(wrap, "whois", perform_whois_lookup, req.target)
            tasks.append(fut)
            fut_to_name[fut] = "whois"
        if req.dns or req.all:
            fut = ex.submit(wrap, "dns", enumerate_dns_records, req.target)
            tasks.append(fut)
            fut_to_name[fut] = "dns"
        if req.subdomains or req.all:
            fut = ex.submit(wrap, "subdomains", discover_subdomains, req.target, config.SUBDOMAIN_WORDLIST)
            tasks.append(fut)
            fut_to_name[fut] = "subdomains"
        if req.ssl or req.all:
            fut = ex.submit(wrap, "ssl", get_ssl_details, req.target)
            tasks.append(fut)
            fut_to_name[fut] = "ssl"

        deadline = time.time() + 12.0
        pending = set(tasks)
        while time.time() < deadline and pending:
            try:
                for fut in as_completed(list(pending), timeout=0.5):
                    try:
                        fut.result()
                    except Exception as e:
                        logger.error(f"Task future error: {e}")
                    finally:
                        pending.discard(fut)
            except TimeoutError:
                # No futures completed in this slice; loop again until deadline
                pass

        # Mark any remaining as timed out by task name
        for fut in list(pending):
            name = fut_to_name.get(fut, "task")
            errors[name] = "timeout"
    finally:
        # Do not wait for running tasks; return partial results promptly
        ex.shutdown(wait=False, cancel_futures=True)

    # AI enrichment (optional)
    if req.all:
        try:
            import json
            raw_data = json.dumps(results, indent=2, default=str)
            # Run summarization with a strict timeout to avoid long external calls
            ex_ai = ThreadPoolExecutor(max_workers=1)
            try:
                fut = ex_ai.submit(summarize_recon_data, raw_data[:2000])
                try:
                    results["ai_summary"] = fut.result(timeout=9.0)
                except TimeoutError:
                    # Fallback to local summarizer
                    results["ai_summary"] = local_bullet_summary(raw_data[:2000])
                    errors["ai"] = "timeout (used local fallback)"
            finally:
                # Don't wait for the AI call to finish if it's slow
                ex_ai.shutdown(wait=False, cancel_futures=True)

            # Risk scoring is local and fast
            features = [
                len(results.get("subdomains", [])),
                1 if isinstance(results.get("ssl", {}), dict) and "error" not in results.get("ssl", {}) else 0,
                len(results.get("dns", {}).get("A", [])) if isinstance(results.get("dns", {}), dict) else 0,
            ]
            results["risk_score"] = calculate_risk_score(features)
        except Exception as e:
            logger.error(f"AI enrichment failed: {e}")
            errors["ai"] = str(e)

    if errors:
        results["errors"] = errors
    return results


@app.post("/scan")
def scan(req: ScanRequest):
    results: Dict[str, Any] = {"target": req.target, "timestamp": datetime.now().isoformat()}
    try:
        ports = req.ports or config.DEFAULT_PORTS
        results["port_scan"] = perform_port_scan(req.target, ports)
        if req.shodan:
            if not config.SHODAN_API_KEY:
                results["shodan_error"] = "SHODAN_API_KEY not configured"
            else:
                results["shodan"] = perform_shodan_scan(config.SHODAN_API_KEY, req.target)
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    return results


@app.post("/username")
def username(req: UsernameRequest):
    try:
        platforms = req.platforms or ["twitter", "linkedin", "github", "instagram"]
        return {
            "target": req.target,
            "timestamp": datetime.now().isoformat(),
            "username_lookup": lookup_username(req.target, platforms),
        }
    except Exception as e:
        logger.error(f"Username lookup failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/urlscan")
def urlscan(req: URLScanRequest):
    try:
        # Run the scan in a short-lived thread with a strict timeout
        def runner():
            if not config.VIRUSTOTAL_API_KEY:
                return {"note": "VIRUSTOTAL_API_KEY not configured", "health": basic_url_health(req.url)}
            return scan_url_full(config.VIRUSTOTAL_API_KEY, req.url) or {"error": "no_data"}

        with ThreadPoolExecutor(max_workers=1) as ex_url:
            fut = ex_url.submit(runner)
            try:
                return fut.result(timeout=10.0)
            except TimeoutError:
                return {"error": "timeout"}
            finally:
                ex_url.shutdown(wait=False, cancel_futures=True)
    except Exception as e:
        logger.error(f"URL scan failed: {e}")
        return {"error": str(e)}


class SummarizeRequest(BaseModel):
    payload: Dict[str, Any]


@app.post("/summarize")
def summarize(req: SummarizeRequest):
    try:
        import json
        raw = json.dumps(req.payload, indent=2, default=str)
        # Try online AI with a bounded worker and use local fallback on failure/timeout
        ex_ai = ThreadPoolExecutor(max_workers=1)
        try:
            fut = ex_ai.submit(summarize_recon_data, raw[:4000])
            try:
                return {"summary": fut.result(timeout=10.0)}
            except TimeoutError:
                return {"summary": local_bullet_summary(raw[:4000]), "note": "ai_timeout_fallback"}
        finally:
            ex_ai.shutdown(wait=False, cancel_futures=True)
    except Exception as e:
        logger.error(f"Summarize failed: {e}")
        # On unexpected errors, still return a local summary if possible
        try:
            import json
            raw = json.dumps(req.payload, indent=2, default=str)
            return {"summary": local_bullet_summary(raw[:4000]), "note": "ai_error_fallback", "error": str(e)}
        except Exception:
            raise HTTPException(status_code=500, detail=str(e))
