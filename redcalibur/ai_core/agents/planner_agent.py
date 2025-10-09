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
        
        # Simple rule-based planning
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
