"""
Directory Enumeration - Discover hidden directories and files on web servers
"""

import requests
import logging
from typing import Dict, List, Any
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

# Common directories and files to check
COMMON_PATHS = [
    "/admin", "/administrator", "/login", "/wp-admin", "/phpmyadmin",
    "/dashboard", "/api", "/backup", "/config", "/db", "/database",
    "/.git", "/.env", "/robots.txt", "/sitemap.xml", "/wp-config.php",
    "/config.php", "/.htaccess", "/backup.zip", "/backup.sql",
    "/test", "/dev", "/staging", "/old", "/temp", "/tmp",
    "/uploads", "/images", "/files", "/download", "/downloads",
    "/assets", "/css", "/js", "/includes", "/lib", "/vendor",
    "/cgi-bin", "/scripts", "/data", "/logs", "/log"
]


def enumerate_directories(base_url: str, wordlist: List[str] = None, timeout: int = 5) -> Dict[str, Any]:
    """
    Enumerate directories and files on a web server
    
    Args:
        base_url: Base URL (e.g., http://example.com)
        wordlist: Custom wordlist of paths to check (optional)
        timeout: Request timeout in seconds
        
    Returns:
        Dictionary with enumeration results
    """
    results = {
        "base_url": base_url,
        "found": [],
        "total_checked": 0,
        "found_count": 0
    }
    
    # Use custom wordlist or default
    paths_to_check = wordlist if wordlist else COMMON_PATHS
    
    logger.info(f"Starting directory enumeration on {base_url}")
    
    for path in paths_to_check:
        results["total_checked"] += 1
        
        try:
            full_url = urljoin(base_url, path)
            
            response = requests.get(
                full_url,
                timeout=timeout,
                allow_redirects=False,
                headers={"User-Agent": "RedCalibur/1.0"}
            )
            
            # Consider 200, 201, 204, 301, 302, 403 as interesting
            if response.status_code in [200, 201, 204, 301, 302, 403]:
                found_item = {
                    "url": full_url,
                    "status_code": response.status_code,
                    "size": len(response.content),
                    "path": path
                }
                
                results["found"].append(found_item)
                results["found_count"] += 1
                
                logger.info(f"Found: {full_url} [{response.status_code}]")
                
        except requests.exceptions.Timeout:
            logger.debug(f"Timeout checking {path}")
        except requests.exceptions.RequestException as e:
            logger.debug(f"Error checking {path}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error checking {path}: {e}")
    
    logger.info(f"Directory enumeration complete. Found {results['found_count']} items.")
    
    return results


def enumerate_with_custom_wordlist(base_url: str, wordlist_file: str, timeout: int = 5) -> Dict[str, Any]:
    """
    Enumerate using a custom wordlist file
    
    Args:
        base_url: Base URL
        wordlist_file: Path to wordlist file
        timeout: Request timeout
        
    Returns:
        Enumeration results
    """
    try:
        with open(wordlist_file, 'r') as f:
            wordlist = [line.strip() for line in f if line.strip()]
        
        return enumerate_directories(base_url, wordlist, timeout)
        
    except FileNotFoundError:
        logger.error(f"Wordlist file not found: {wordlist_file}")
        return {"error": f"Wordlist file not found: {wordlist_file}"}
    except Exception as e:
        logger.error(f"Error reading wordlist: {e}")
        return {"error": str(e)}


def quick_scan(base_url: str) -> Dict[str, Any]:
    """
    Quick scan with minimal paths
    
    Args:
        base_url: Base URL
        
    Returns:
        Scan results
    """
    quick_paths = [
        "/admin", "/login", "/robots.txt", "/.git", "/.env",
        "/backup", "/config", "/api", "/wp-admin"
    ]
    
    return enumerate_directories(base_url, quick_paths, timeout=3)
