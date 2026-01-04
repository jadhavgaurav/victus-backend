import socket
import ipaddress
from urllib.parse import urlparse

def is_safe_url(url: str) -> bool:
    """
    Validates that a URL does not point to a private or loopback address (SSRF protection).
    """
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False
            
        # Resolve IP
        try:
            ip_str = socket.gethostbyname(hostname)
        except socket.gaierror:
            return False # Cannot resolve
            
        ip = ipaddress.ip_address(ip_str)
        
        # Check against private, loopback, link-local, multicast
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast:
            return False
            
        return True
    except Exception:
        return False
