"""
Recon Agent - OSINT and reconnaissance specialist
"""

from ..base_agent import BaseAgent, AgentThought, AgentAction
from typing import Dict, Any

class ReconAgent(BaseAgent):
    """
    Reconnaissance specialist that gathers information about targets
    using OSINT techniques and scanning tools.
    """
    
    def __init__(self):
        super().__init__(
            name="Recon",
            description="OSINT and reconnaissance specialist",
            tools=[
                "whois", "nmap", "subfinder", "theHarvester",
                "shodan", "virustotal", "dns_enum", "port_scan"
            ]
        )
        
    def think(self, context: Dict[str, Any]) -> AgentThought:
        """Analyze what reconnaissance is needed"""
        
        target = context.get('target', 'Unknown')
        scan_type = context.get('scan_type', 'comprehensive')
        
        # Determine target type
        target_type = self._identify_target_type(target)
        
        analysis = f"""
Target: {target}
Target Type: {target_type}
Scan Type: {scan_type}

Reconnaissance Strategy:
1. WHOIS lookup - Domain registration information
2. DNS enumeration - Discover subdomains and DNS records
3. Port scanning - Identify open ports and services
4. Technology detection - Identify web technologies used
5. OSINT gathering - Search for exposed information

Tools to use: whois → dns_enum → nmap → subfinder
"""
        
        return AgentThought(
            observation=f"Target identified: {target} (Type: {target_type})",
            analysis=analysis,
            plan=f"Execute multi-phase reconnaissance starting with WHOIS",
            confidence=0.85
        )
    
    def act(self, thought: AgentThought) -> AgentAction:
        """Execute reconnaissance tool"""
        
        # Start with WHOIS as first step
        return AgentAction(
            tool="whois",
            parameters={
                "target": thought.observation.split(":")[1].strip().split("(")[0].strip(),
                "verbose": True
            },
            reasoning="Starting reconnaissance with WHOIS lookup to gather domain information",
            expected_outcome="Domain registration details, nameservers, contact information"
        )
    
    def _identify_target_type(self, target: str) -> str:
        """Identify target type (domain, IP, URL)"""
        if target.startswith('http'):
            return "URL"
        elif '.' in target and not target.replace('.', '').isdigit():
            return "Domain"
        elif target.replace('.', '').isdigit():
            return "IP Address"
        else:
            return "Unknown"
