"""
Reporting Agent - Documentation and report generation specialist
"""

from ..base_agent import BaseAgent, AgentThought, AgentAction
from typing import Dict, Any
from datetime import datetime

class ReportingAgent(BaseAgent):
    """
    Documentation specialist that creates comprehensive
    penetration testing reports.
    """
    
    def __init__(self):
        super().__init__(
            name="Reporting",
            description="Report generation and documentation specialist",
            tools=[
                "pdf_generator", "mitre_mapper", "cvss_calculator",
                "markdown_formatter", "risk_assessor"
            ]
        )
        
    def think(self, context: Dict[str, Any]) -> AgentThought:
        """Analyze findings and plan report structure"""
        
        findings = context.get('findings', [])
        target = context.get('target', 'Unknown')
        objective = context.get('objective', 'Penetration Test')
        
        num_findings = len(findings) if isinstance(findings, list) else 0
        
        analysis = f"""
Engagement: {objective}
Target: {target}
Findings: {num_findings} issues identified
Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Report Structure:
1. Executive Summary
   - High-level overview for management
   - Risk assessment and business impact
   
2. Technical Findings
   - Detailed vulnerability descriptions
   - Proof-of-concept demonstrations
   - CVSS scoring
   
3. MITRE ATT&CK Mapping
   - Tactics and techniques used
   - Attack path visualization
   
4. Recommendations
   - Prioritized remediation steps
   - Security improvements
   
5. Appendix
   - Tools used
   - Methodology
   - Timeline
"""
        
        return AgentThought(
            observation=f"Processing engagement results for {target}",
            analysis=analysis,
            plan="Generate comprehensive penetration test report",
            confidence=0.95
        )
    
    def act(self, thought: AgentThought) -> AgentAction:
        """Generate report"""
        
        return AgentAction(
            tool="pdf_generator",
            parameters={
                "template": "pentest_report",
                "format": "pdf",
                "include_executive_summary": True,
                "include_mitre_mapping": True,
                "include_recommendations": True
            },
            reasoning="Creating professional penetration test report with all findings",
            expected_outcome="Comprehensive PDF report with executive summary and technical details"
        )
