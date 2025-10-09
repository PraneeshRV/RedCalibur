"""
Service Detector - Detect and fingerprint services on open ports
"""

import socket
import logging
from typing import Dict, List, Any, Tuple

logger = logging.getLogger(__name__)

# Common service signatures
SERVICE_SIGNATURES = {
    "SSH": [b"SSH", b"OpenSSH"],
    "HTTP": [b"HTTP/", b"Server:"],
    "FTP": [b"220", b"FTP"],
    "SMTP": [b"220", b"SMTP", b"ESMTP"],
    "MySQL": [b"mysql", b"MariaDB"],
    "PostgreSQL": [b"PostgreSQL"],
    "Redis": [b"Redis"],
    "MongoDB": [b"MongoDB"],
    "Telnet": [b"Telnet"],
    "HTTPS": [b"SSL", b"TLS"],
}


def detect_services(target: str, ports: List[int], timeout: int = 3) -> List[Dict[str, Any]]:
    """
    Detect services running on specified ports
    
    Args:
        target: Target IP or hostname
        ports: List of ports to check
        timeout: Socket timeout in seconds
        
    Returns:
        List of detected services with details
    """
    services = []
    
    for port in ports:
        try:
            service_info = fingerprint_service(target, port, timeout)
            if service_info:
                services.append(service_info)
                # Only log identified services, not unknown ones
                service_name = service_info.get('service', 'unknown')
                if service_name != 'unknown':
                    logger.info(f"Detected service on {target}:{port} - {service_name}")
                else:
                    logger.debug(f"Port {port} open but service unknown")
        except Exception as e:
            logger.error(f"Error detecting service on port {port}: {e}")
    
    return services


def fingerprint_service(target: str, port: int, timeout: int = 3) -> Dict[str, Any]:
    """
    Fingerprint a service on a specific port
    
    Args:
        target: Target IP or hostname
        port: Port number
        timeout: Socket timeout
        
    Returns:
        Dictionary with service information
    """
    result = {
        "port": port,
        "state": "unknown",
        "service": "unknown",
        "version": "",
        "banner": ""
    }
    
    try:
        # Try to connect
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        connection_result = sock.connect_ex((target, port))
        
        if connection_result == 0:
            result["state"] = "open"
            
            # Try to grab banner
            try:
                # Send a generic request
                sock.send(b"GET / HTTP/1.0\r\n\r\n")
                banner = sock.recv(1024)
                
                if banner:
                    result["banner"] = banner.decode('utf-8', errors='ignore').strip()
                    
                    # Identify service from banner
                    service_name, version = identify_service_from_banner(banner)
                    result["service"] = service_name
                    result["version"] = version
                    
            except Exception as e:
                logger.debug(f"Could not grab banner from {target}:{port} - {e}")
            
            # If banner grab failed, use common port mappings
            if result["service"] == "unknown":
                result["service"] = get_service_by_port(port)
        else:
            result["state"] = "closed"
            
        sock.close()
        
    except socket.timeout:
        result["state"] = "filtered"
        logger.debug(f"Timeout connecting to {target}:{port}")
    except socket.error as e:
        result["state"] = "error"
        result["error"] = str(e)
        logger.debug(f"Socket error on {target}:{port} - {e}")
    except Exception as e:
        result["error"] = str(e)
        logger.error(f"Error fingerprinting {target}:{port} - {e}")
    
    return result


def identify_service_from_banner(banner: bytes) -> Tuple[str, str]:
    """
    Identify service and version from banner
    
    Args:
        banner: Banner bytes
        
    Returns:
        Tuple of (service_name, version)
    """
    banner_str = banner.decode('utf-8', errors='ignore').lower()
    
    # Check for SSH
    if b"ssh" in banner.lower():
        service = "SSH"
        # Try to extract version
        if b"openssh" in banner.lower():
            version = extract_version_from_banner(banner_str, "openssh")
            return service, f"OpenSSH {version}" if version else "OpenSSH"
        return service, ""
    
    # Check for HTTP/HTTPS
    if b"http/" in banner.lower():
        service = "HTTP"
        # Try to find server header
        if "server:" in banner_str:
            server_line = [line for line in banner_str.split('\n') if 'server:' in line]
            if server_line:
                version = server_line[0].split('server:')[1].strip()
                return service, version
        return service, ""
    
    # Check for FTP
    if b"220" in banner and b"ftp" in banner.lower():
        service = "FTP"
        version = extract_version_from_banner(banner_str, "ftp")
        return service, version if version else ""
    
    # Check for SMTP
    if b"220" in banner and (b"smtp" in banner.lower() or b"esmtp" in banner.lower()):
        service = "SMTP"
        version = extract_version_from_banner(banner_str, "smtp")
        return service, version if version else ""
    
    # Check for MySQL
    if b"mysql" in banner.lower():
        return "MySQL", extract_version_from_banner(banner_str, "mysql")
    
    # Check for Redis
    if b"redis" in banner.lower():
        return "Redis", extract_version_from_banner(banner_str, "redis")
    
    return "unknown", ""


def extract_version_from_banner(banner: str, service: str) -> str:
    """
    Extract version number from banner string
    
    Args:
        banner: Banner string
        service: Service name
        
    Returns:
        Version string or empty string
    """
    import re
    
    # Try to find version pattern (e.g., 2.4.41, 8.0.23)
    version_pattern = r'\d+\.\d+(?:\.\d+)?'
    matches = re.findall(version_pattern, banner)
    
    if matches:
        return matches[0]
    
    return ""


def get_service_by_port(port: int) -> str:
    """
    Get common service name by port number
    
    Args:
        port: Port number
        
    Returns:
        Service name
    """
    common_ports = {
        20: "FTP-DATA",
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        465: "SMTPS",
        587: "SMTP",
        993: "IMAPS",
        995: "POP3S",
        1433: "MSSQL",
        1521: "Oracle",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        6379: "Redis",
        8080: "HTTP-Proxy",
        8443: "HTTPS-Alt",
        27017: "MongoDB"
    }
    
    return common_ports.get(port, "unknown")
