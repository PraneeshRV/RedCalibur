"""
Planner Agent - Strategic planning and task orchestration
"""

from ..base_agent import BaseAgent, AgentThought, AgentAction
from typing import Dict, Any

class PlannerAgent(BaseAgent):
    """
    Strategic planning agent that breaks down high-level objectives
    into actionable tasks and delegates to specialized agents.
    """
    
    def __init__(self):
        super().__init__(
            name="Planner",
            description="Strategic planning and task orchestration",
            tools=["task_decomposition", "agent_router", "goal_validator"]
        )
        
    def think(self, context: Dict[str, Any]) -> AgentThought:
        """Analyze the goal and break it down into subtasks"""
        
        objective = context.get('objective', 'Unknown objective')
        target = context.get('target', 'Unknown target')
        
        # Use AI reasoning if available
        if self.use_ai:
            prompt = f"""You are a strategic planner for a penetration testing engagement.

Objective: {objective}
Target: {target}

Analyze this penetration testing objective and provide:
1. Target assessment (what type of target is this?)
2. Recommended phases (reconnaissance, vulnerability scanning, exploitation, reporting)
3. Which specialized agents should handle each phase
4. Potential risks and blockers
5. Success criteria

Available specialized agents:
- ReconAgent: OSINT and reconnaissance (whois, nmap, subfinder, shodan)
- ExploitAgent: Vulnerability scanning and exploitation (metasploit, sqlmap, nuclei)
- ReportingAgent: Documentation and report generation

Provide a structured strategic analysis in 3-4 paragraphs."""

            analysis = self._call_llm(prompt)
        else:
            # Fallback to rule-based
            analysis = f"""
Target Analysis: {target}
Objective: {objective}

Recommended Phases:
1. Reconnaissance - Gather information about the target
2. Vulnerability Scanning - Identify potential weaknesses
3. Exploitation - Attempt to exploit vulnerabilities
4. Reporting - Document findings and recommendations

Agent Delegation:
- Phase 1: ReconAgent (OSINT and network scanning)
- Phase 2: ExploitAgent (vulnerability assessment)
- Phase 3: ExploitAgent (exploitation attempts)
- Phase 4: ReportingAgent (documentation)
"""
        
        return AgentThought(
            observation=f"Analyzing objective: {objective} for target: {target}",
            analysis=analysis,
            plan="Start with reconnaissance using ReconAgent",
            confidence=0.90
        )
    
    def act(self, thought: AgentThought) -> AgentAction:
        """Create a structured action plan"""
        
        return AgentAction(
            tool="task_decomposition",
            parameters={
                "objective": thought.observation,
                "phases": ["reconnaissance", "scanning", "exploitation", "reporting"],
                "first_agent": "ReconAgent"
            },
            reasoning="Breaking down the penetration test into manageable phases",
            expected_outcome="Structured task tree for execution"
        )
