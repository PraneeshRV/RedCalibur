import base64
import time
import requests

DEFAULT_TIMEOUT = 8.0  # per-request timeout

def scan_url(api_key: str, url: str):
    """
    Submit a URL for scanning using the VirusTotal API.

    Returns the raw submission response (often contains an analysis id).
    """
    vt_url = "https://www.virustotal.com/api/v3/urls"
    headers = {"x-apikey": api_key}
    data = {"url": url}
    try:
        response = requests.post(vt_url, headers=headers, data=data, timeout=DEFAULT_TIMEOUT)
        if response.status_code == 200:
            return response.json()
        return {"error": "virustotal_error", "status": response.status_code, "body": response.text}
    except Exception as e:
        return {"error": str(e)}

def get_url_report(api_key: str, url_id: str):
    """
    Get the latest report for a URL using the VirusTotal API (by URL ID).
    """
    vt_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    headers = {"x-apikey": api_key}
    try:
        response = requests.get(vt_url, headers=headers, timeout=DEFAULT_TIMEOUT)
        if response.status_code == 200:
            return response.json()
        return {"error": "virustotal_error", "status": response.status_code, "body": response.text}
    except Exception as e:
        return {"error": str(e)}

def get_analysis(api_key: str, analysis_id: str):
    """Fetch a specific analysis object by id."""
    vt_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    headers = {"x-apikey": api_key}
    try:
        response = requests.get(vt_url, headers=headers, timeout=DEFAULT_TIMEOUT)
        if response.status_code == 200:
            return response.json()
        return {"error": "virustotal_error", "status": response.status_code, "body": response.text}
    except Exception as e:
        return {"error": str(e)}

def url_to_vt_id(url: str) -> str:
    """Encode a URL to VirusTotal URL ID (urlsafe base64 without padding)."""
    enc = base64.urlsafe_b64encode(url.encode()).decode()
    return enc.rstrip('=')

def scan_url_full(api_key: str, url: str, overall_timeout: float = 9.0, poll_interval: float = 1.0):
    """
    End-to-end URL scan that submits, polls for completion briefly, and returns structured results.

    Returns:
      {
        "source": "virustotal",
        "submitted": { ...raw submission... },
        "analysis": { ...latest analysis object if fetched... },
        "report": {
            "last_analysis_stats": { harmless, malicious, suspicious, undetected, timeout },
            "reputation": int | None,
            "total_vendors": int,
            "malicious_vendors": [ { "engine": name, "category": cat } ... up to 5 ],
            "link": "https://www.virustotal.com/gui/url/<id>"
        }
      }
      or a pending/timeout structure if not ready in time.
    """
    start = time.time()
    result: dict = {"source": "virustotal"}

    submission = scan_url(api_key, url)
    result["submitted"] = submission

    # Try to get analysis id from submission
    analysis_id = None
    try:
        analysis_id = submission.get("data", {}).get("id")
    except Exception:
        pass

    # Compute URL ID for report link and final stats
    url_id = url_to_vt_id(url)
    result_link = f"https://www.virustotal.com/gui/url/{url_id}"

    # Poll the analysis endpoint briefly
    analysis_obj = None
    while analysis_id and (time.time() - start) < overall_timeout:
        a = get_analysis(api_key, analysis_id)
        if isinstance(a, dict) and a.get("data", {}).get("attributes", {}).get("status") == "completed":
            analysis_obj = a
            break
        time.sleep(poll_interval)

    result["analysis"] = analysis_obj or {"note": "analysis_pending"}

    # Fetch latest URL report to get last_analysis_stats
    report = get_url_report(api_key, url_id)
    rep_attrs = report.get("data", {}).get("attributes", {}) if isinstance(report, dict) else {}
    stats = rep_attrs.get("last_analysis_stats", {})
    vendors = rep_attrs.get("last_analysis_results", {})
    # extract a small list of malicious vendors (up to 5)
    mal_vendors = []
    if isinstance(vendors, dict):
        for eng, v in vendors.items():
            try:
                if (v or {}).get("category") == "malicious":
                    mal_vendors.append({"engine": eng, "category": v.get("category")})
            except Exception:
                continue
    mal_vendors = mal_vendors[:5]

    summary = {
        "last_analysis_stats": stats or None,
        "reputation": rep_attrs.get("reputation"),
        "total_vendors": len(vendors) if isinstance(vendors, dict) else None,
        "malicious_vendors": mal_vendors,
        "link": result_link,
    }
    result["report"] = summary

    # If still nothing meaningful, indicate pending
    if not stats:
        result["note"] = "analysis_pending_or_insufficient_time"

    return result
