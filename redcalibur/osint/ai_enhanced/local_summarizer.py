import json
from typing import Any, Dict

def _safe(obj: Any, default: str = "-") -> str:
    try:
        if obj is None:
            return default
        s = str(obj)
        return s if s.strip() else default
    except Exception:
        return default

def local_bullet_summary(raw_json: str) -> str:
    """Produce a quick local summary without external AI.

    Attempts to parse the JSON payload and extract a few key points.
    This is used as a fallback when the online AI model is slow/unavailable.
    """
    try:
        data: Dict[str, Any] = json.loads(raw_json)
    except Exception:
        # If not JSON, just return a trimmed snippet
        snippet = raw_json[:800]
        return (
            "Local Summary (fallback)\n\n"
            "Received non-JSON data. Showing first 800 chars:\n\n"
            f"{snippet}…"
        )

    lines = [
        "Local Summary (fallback)",
        "",  # spacer
    ]

    target = _safe(data.get("target"))
    ts = _safe(data.get("timestamp"))
    if target != "-" or ts != "-":
        lines.append(f"- Target: {target}")
        lines.append(f"- Time: {ts}")

    # Errors
    errs = data.get("errors")
    if isinstance(errs, dict) and errs:
        err_list = ", ".join(sorted(errs.keys()))
        lines.append(f"- Noted errors: {err_list}")

    # DNS
    dns = data.get("dns")
    if isinstance(dns, dict) and dns:
        a_count = len(dns.get("A", []) or [])
        mx_count = len(dns.get("MX", []) or [])
        txt = dns.get("TXT")
        lines.append(f"- DNS: A={a_count}, MX={mx_count}, TXT={'yes' if txt else 'no'}")

    # Subdomains
    subs = data.get("subdomains")
    if isinstance(subs, list):
        preview = ", ".join(subs[:3]) if subs else "none"
        lines.append(f"- Subdomains: {len(subs)} found. Examples: {preview}")

    # SSL
    ssl = data.get("ssl")
    if isinstance(ssl, dict):
        if ssl.get("error"):
            lines.append("- SSL: error fetching certificate details")
        else:
            issuer = _safe(ssl.get("issuer", {}).get("commonName") if isinstance(ssl.get("issuer"), dict) else ssl.get("issuer"))
            subject = _safe(ssl.get("subject", {}).get("commonName") if isinstance(ssl.get("subject"), dict) else ssl.get("subject"))
            lines.append(f"- SSL: subject={subject}, issuer={issuer}")

    # Port scan
    ps = data.get("port_scan")
    if isinstance(ps, dict):
        open_ports = [p for p, st in ps.items() if str(st).lower() == 'open']
        lines.append(f"- Open ports: {', '.join(map(str, open_ports)) if open_ports else 'none visible'}")

    # Risk score
    if "risk_score" in data:
        try:
            rs = float(data["risk_score"])  # type: ignore[arg-type]
            lines.append(f"- Risk score: {rs:.3f} (0 low → 1 high)")
        except Exception:
            pass

    # VT URL stats (if present)
    vt = data.get("virustotal") or data.get("urlscan")
    if isinstance(vt, dict):
        stats = vt.get("last_analysis_stats") or vt.get("stats")
        if isinstance(stats, dict):
            harmful = stats.get("malicious", 0) + stats.get("suspicious", 0)
            lines.append(f"- VT vendors: malicious+suspicious={harmful}")

    # Final suggestion
    lines += [
        "",
        "Recommendations:",
        "- Review DNS records for anomalies (unexpected MX/TXT changes).",
        "- Verify SSL certificate details and expiry.",
        "- Sanity-check exposed services on open ports; restrict where possible.",
        "- If VT shows detections, avoid visiting the URL and investigate further.",
    ]

    return "\n".join(lines)
