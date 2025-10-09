"""
Banner Grabber - Grab service banners for identification
"""

import socket
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def grab_banner(target: str, port: int, timeout: int = 3, send_data: bytes = None) -> Dict[str, Any]:
    """
    Grab banner from a service
    
    Args:
        target: Target IP or hostname
        port: Port number
        timeout: Socket timeout in seconds
        send_data: Optional data to send before receiving
        
    Returns:
        Dictionary with banner information
    """
    result = {
        "target": target,
        "port": port,
        "banner": "",
        "success": False
    }
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        sock.connect((target, port))
        
        # If custom data provided, send it
        if send_data:
            sock.send(send_data)
        else:
            # Try common probes based on port
            probe = get_default_probe(port)
            if probe:
                sock.send(probe)
        
        # Receive banner
        banner = sock.recv(4096)
        
        if banner:
            result["banner"] = banner.decode('utf-8', errors='ignore').strip()
            result["success"] = True
            logger.info(f"Successfully grabbed banner from {target}:{port}")
        
        sock.close()
        
    except socket.timeout:
        result["error"] = "Connection timeout"
        logger.debug(f"Timeout grabbing banner from {target}:{port}")
    except ConnectionRefusedError:
        result["error"] = "Connection refused"
        logger.debug(f"Connection refused on {target}:{port}")
    except Exception as e:
        result["error"] = str(e)
        logger.error(f"Error grabbing banner from {target}:{port} - {e}")
    
    return result


def get_default_probe(port: int) -> bytes:
    """
    Get default probe for common ports
    
    Args:
        port: Port number
        
    Returns:
        Probe bytes or None
    """
    probes = {
        80: b"GET / HTTP/1.0\r\n\r\n",
        443: b"GET / HTTP/1.0\r\n\r\n",
        8080: b"GET / HTTP/1.0\r\n\r\n",
        8443: b"GET / HTTP/1.0\r\n\r\n",
        21: b"USER anonymous\r\n",
        25: b"EHLO test\r\n",
        110: b"USER test\r\n",
        143: b"A001 CAPABILITY\r\n",
        # Most other services will send banner on connect
    }
    
    return probes.get(port, b"")


def batch_grab_banners(target: str, ports: list, timeout: int = 3) -> list:
    """
    Grab banners from multiple ports
    
    Args:
        target: Target IP or hostname
        ports: List of ports
        timeout: Socket timeout
        
    Returns:
        List of banner results
    """
    results = []
    
    for port in ports:
        banner_result = grab_banner(target, port, timeout)
        if banner_result["success"]:
            results.append(banner_result)
    
    return results
