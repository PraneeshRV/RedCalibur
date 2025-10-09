# Multi-Agent System Implementation Guide

## 🤖 Agent Architecture Overview

RedCalibur's multi-agent system is inspired by HexStrike AI, PentAGI, and CAI. It implements a **ReACT (Reasoning + Action)** architecture with specialized agents working collaboratively.

---

## 📐 Core Architecture

### 1. Base Agent Class

```python
# redcalibur/ai_core/base_agent.py

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

class AgentState(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    WAITING = "waiting"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class AgentAction:
    """Represents an action the agent wants to take"""
    tool: str
    parameters: Dict[str, Any]
    reasoning: str
    expected_outcome: str

@dataclass
class AgentThought:
    """Represents an agent's reasoning process"""
    observation: str
    analysis: str
    plan: str
    confidence: float

class BaseAgent(ABC):
    """
    Base class for all RedCalibur agents.
    Implements ReACT (Reasoning + Action) pattern.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        llm_provider: str = "gemini",
        model: str = "gemini-1.5-pro",
        tools: Optional[List[str]] = None
    ):
        self.name = name
        self.description = description
        self.llm_provider = llm_provider
        self.model = model
        self.tools = tools or []
        self.state = AgentState.IDLE
        self.memory = []
        self.logger = logging.getLogger(f"agent.{name}")
        
    @abstractmethod
    async def think(self, context: Dict[str, Any]) -> AgentThought:
        """
        Reasoning phase: Analyze the situation and plan next steps.
        
        Args:
            context: Current context including previous observations
            
        Returns:
            AgentThought with observation, analysis, and plan
        """
        pass
    
    @abstractmethod
    async def act(self, thought: AgentThought) -> AgentAction:
        """
        Action phase: Decide what action to take based on reasoning.
        
        Args:
            thought: The reasoning output from think()
            
        Returns:
            AgentAction to be executed
        """
        pass
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution loop: Think → Act → Observe cycle.
        """
        self.state = AgentState.THINKING
        thought = await self.think(context)
        
        self.state = AgentState.ACTING
        action = await self.act(thought)
        
        # Execute the action via tool manager
        result = await self._execute_action(action)
        
        # Store in memory
        self.memory.append({
            'thought': thought,
            'action': action,
            'result': result
        })
        
        self.state = AgentState.IDLE
        return result
    
    async def _execute_action(self, action: AgentAction) -> Dict[str, Any]:
        """Execute the action using the tool manager"""
        from redcalibur.ai_core.tool_manager import ToolManager
        
        tool_manager = ToolManager()
        return await tool_manager.execute_tool(
            tool_name=action.tool,
            parameters=action.parameters
        )
    
    def handoff_to(self, agent_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handoff control to another agent.
        
        Args:
            agent_name: Name of the agent to handoff to
            context: Context to pass to the next agent
            
        Returns:
            Handoff request dictionary
        """
        return {
            'handoff': True,
            'target_agent': agent_name,
            'context': context,
            'reason': f"{self.name} believes {agent_name} is better suited for this task"
        }
```

---

### 2. Specialized Agent Implementations

#### 2.1 Planner Agent
```python
# redcalibur/ai_core/agents/planner_agent.py

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
        
    async def think(self, context: Dict[str, Any]) -> AgentThought:
        """Analyze the goal and break it down into subtasks"""
        
        objective = context.get('objective', '')
        target = context.get('target', '')
        
        prompt = f"""
        You are a red team planner analyzing a penetration testing objective.
        
        Objective: {objective}
        Target: {target}
        
        Analyze this objective and:
        1. Identify the main phases needed (reconnaissance, exploitation, etc.)
        2. Determine which specialized agents should handle each phase
        3. Identify dependencies between phases
        4. Assess risks and potential blockers
        
        Provide your analysis in a structured format.
        """
        
        # Call LLM for strategic planning
        analysis = await self._call_llm(prompt)
        
        return AgentThought(
            observation=f"Analyzing objective: {objective}",
            analysis=analysis,
            plan="Break down into subtasks and delegate to specialized agents",
            confidence=0.85
        )
    
    async def act(self, thought: AgentThought) -> AgentAction:
        """Create a structured action plan"""
        
        return AgentAction(
            tool="task_decomposition",
            parameters={
                "objective": thought.observation,
                "analysis": thought.analysis
            },
            reasoning=thought.plan,
            expected_outcome="Structured task tree for execution"
        )
```

#### 2.2 Recon Agent
```python
# redcalibur/ai_core/agents/recon_agent.py

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
                "shodan", "virustotal", "dnsdumpster", "spiderfoot"
            ]
        )
        self.scan_depth = "normal"  # normal, aggressive, stealth
        
    async def think(self, context: Dict[str, Any]) -> AgentThought:
        """Analyze what reconnaissance is needed"""
        
        target = context.get('target', '')
        scan_type = context.get('scan_type', 'comprehensive')
        
        prompt = f"""
        You are performing reconnaissance on target: {target}
        Scan type: {scan_type}
        
        Available tools: {', '.join(self.tools)}
        
        Determine:
        1. Which reconnaissance tools to use in what order
        2. What information to gather (domains, IPs, technologies, employees)
        3. How to avoid detection (rate limiting, timing)
        4. What patterns or anomalies to look for
        
        Recommend a reconnaissance strategy.
        """
        
        strategy = await self._call_llm(prompt)
        
        return AgentThought(
            observation=f"Target identified: {target}",
            analysis=strategy,
            plan="Execute multi-phase reconnaissance",
            confidence=0.90
        )
    
    async def act(self, thought: AgentThought) -> AgentAction:
        """Execute reconnaissance tool"""
        
        # Parse the strategy to determine first tool to use
        tool_to_use = self._parse_next_tool(thought.analysis)
        
        return AgentAction(
            tool=tool_to_use['name'],
            parameters=tool_to_use['params'],
            reasoning=f"Starting reconnaissance with {tool_to_use['name']}",
            expected_outcome=tool_to_use['expected_output']
        )
```

#### 2.3 Exploit Agent
```python
# redcalibur/ai_core/agents/exploit_agent.py

class ExploitAgent(BaseAgent):
    """
    Exploitation specialist that identifies and exploits vulnerabilities.
    """
    
    def __init__(self):
        super().__init__(
            name="Exploit",
            description="Vulnerability exploitation specialist",
            tools=[
                "metasploit", "sqlmap", "nuclei", "ffuf",
                "hydra", "burpsuite", "nikto", "wpscan"
            ]
        )
        
    async def think(self, context: Dict[str, Any]) -> AgentThought:
        """Analyze vulnerabilities and plan exploitation"""
        
        vulnerabilities = context.get('vulnerabilities', [])
        target_info = context.get('target_info', {})
        
        prompt = f"""
        You are analyzing vulnerabilities for exploitation.
        
        Identified vulnerabilities: {vulnerabilities}
        Target information: {target_info}
        
        For each vulnerability:
        1. Assess exploitability (CVSS score, exploit availability)
        2. Determine impact (data access, code execution, privilege escalation)
        3. Plan exploitation approach (tools, payloads, evasion)
        4. Identify prerequisites and dependencies
        5. Consider detection risk
        
        Provide exploitation recommendations prioritized by impact and success probability.
        """
        
        exploitation_plan = await self._call_llm(prompt)
        
        return AgentThought(
            observation=f"Analyzing {len(vulnerabilities)} vulnerabilities",
            analysis=exploitation_plan,
            plan="Attempt exploitation in priority order",
            confidence=0.75
        )
    
    async def act(self, thought: AgentThought) -> AgentAction:
        """Execute exploitation attempt"""
        
        exploit_details = self._parse_exploit_plan(thought.analysis)
        
        return AgentAction(
            tool=exploit_details['tool'],
            parameters=exploit_details['params'],
            reasoning=thought.plan,
            expected_outcome=exploit_details['expected_outcome']
        )
```

#### 2.4 Evasion Agent
```python
# redcalibur/ai_core/agents/evasion_agent.py

class EvasionAgent(BaseAgent):
    """
    Defense evasion specialist that helps avoid detection
    and bypass security controls.
    """
    
    def __init__(self):
        super().__init__(
            name="Evasion",
            description="Defense evasion and anti-detection specialist",
            tools=[
                "invoke_obfuscation", "veil", "scarecrow", "amsi_bypass",
                "etw_bypass", "shellter", "hyperion", "covenant"
            ]
        )
        
    async def think(self, context: Dict[str, Any]) -> AgentThought:
        """Analyze security controls and plan evasion"""
        
        security_controls = context.get('security_controls', [])
        payload = context.get('payload', '')
        
        prompt = f"""
        You are analyzing security controls to plan evasion techniques.
        
        Detected security controls: {security_controls}
        Payload to deliver: {payload}
        
        Determine:
        1. Which controls pose the highest detection risk
        2. Appropriate evasion techniques for each control
        3. Obfuscation methods for the payload
        4. Delivery mechanisms that avoid detection
        5. Persistence methods that evade monitoring
        
        Recommend a multi-layered evasion strategy.
        """
        
        evasion_strategy = await self._call_llm(prompt)
        
        return AgentThought(
            observation=f"Analyzing {len(security_controls)} security controls",
            analysis=evasion_strategy,
            plan="Apply layered evasion techniques",
            confidence=0.70
        )
```

#### 2.5 Reporting Agent
```python
# redcalibur/ai_core/agents/reporting_agent.py

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
                "markdown_formatter", "screenshot_annotator"
            ]
        )
        
    async def think(self, context: Dict[str, Any]) -> AgentThought:
        """Analyze findings and plan report structure"""
        
        findings = context.get('findings', [])
        engagement_info = context.get('engagement_info', {})
        
        prompt = f"""
        You are creating a penetration testing report.
        
        Findings: {len(findings)} issues identified
        Engagement: {engagement_info}
        
        Structure the report:
        1. Executive Summary (non-technical)
        2. Technical Findings (detailed)
        3. MITRE ATT&CK mapping
        4. Risk assessment and scoring
        5. Remediation recommendations
        6. Appendix (tools used, methodology)
        
        Prioritize findings by risk and provide actionable recommendations.
        """
        
        report_plan = await self._call_llm(prompt)
        
        return AgentThought(
            observation=f"Processing {len(findings)} findings",
            analysis=report_plan,
            plan="Generate comprehensive report",
            confidence=0.95
        )
```

---

### 3. Agent Orchestrator

```python
# redcalibur/ai_core/orchestrator.py

from typing import Dict, List, Optional
import asyncio

class AgentOrchestrator:
    """
    Coordinates multiple agents to accomplish complex tasks.
    Implements handoff mechanism and manages agent lifecycle.
    """
    
    def __init__(self):
        self.agents = {
            'planner': PlannerAgent(),
            'recon': ReconAgent(),
            'exploit': ExploitAgent(),
            'evasion': EvasionAgent(),
            'reporting': ReportingAgent()
        }
        self.current_agent = None
        self.execution_history = []
        
    async def execute_workflow(
        self,
        objective: str,
        target: str,
        workflow_type: str = "autonomous"
    ) -> Dict[str, Any]:
        """
        Execute a multi-agent workflow to accomplish an objective.
        
        Args:
            objective: High-level goal (e.g., "Find XSS vulnerabilities")
            target: Target system (URL, IP, domain)
            workflow_type: "autonomous" or "supervised"
            
        Returns:
            Complete workflow results including all agent outputs
        """
        
        # Start with planner agent
        context = {
            'objective': objective,
            'target': target,
            'workflow_type': workflow_type
        }
        
        current_agent_name = 'planner'
        max_iterations = 20
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Get current agent
            agent = self.agents[current_agent_name]
            self.current_agent = agent
            
            print(f"\n[Iteration {iteration}] Agent: {agent.name}")
            
            # Execute agent
            result = await agent.execute(context)
            
            # Log execution
            self.execution_history.append({
                'iteration': iteration,
                'agent': agent.name,
                'result': result
            })
            
            # Check if handoff is requested
            if result.get('handoff'):
                current_agent_name = result['target_agent']
                context = result['context']
                print(f"→ Handing off to {current_agent_name}")
            elif result.get('completed'):
                print("✓ Workflow completed successfully")
                break
            else:
                # Update context with results
                context['previous_results'] = result
                
        return {
            'success': True,
            'iterations': iteration,
            'history': self.execution_history,
            'final_output': result
        }
    
    async def supervised_handoff(
        self,
        from_agent: str,
        to_agent: str,
        context: Dict[str, Any],
        require_approval: bool = True
    ) -> bool:
        """
        Perform supervised handoff with human approval.
        """
        
        if require_approval:
            print(f"\nHandoff requested: {from_agent} → {to_agent}")
            print(f"Context: {context}")
            approval = input("Approve handoff? (y/n): ")
            
            if approval.lower() != 'y':
                print("Handoff denied")
                return False
        
        print(f"✓ Handoff approved: {from_agent} → {to_agent}")
        return True
```

---

### 4. Pentesting Task Tree (PTT)

```python
# redcalibur/ai_core/ptt.py

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"

@dataclass
class PentestingTask:
    """Represents a node in the Pentesting Task Tree"""
    id: str
    name: str
    description: str
    agent: str
    dependencies: List[str]
    status: TaskStatus
    priority: int
    result: Optional[Dict] = None
    children: List['PentestingTask'] = None

class PTTManager:
    """
    Manages the Pentesting Task Tree (PTT) for autonomous execution.
    Inspired by PentAGI's task planning system.
    """
    
    def __init__(self):
        self.root_task = None
        self.task_registry = {}
        
    def build_tree(self, objective: str, target: str) -> PentestingTask:
        """
        Build a complete PTT from a high-level objective.
        
        Example tree:
        Root: "Complete pentest of example.com"
        ├── Task 1: "Reconnaissance" (Recon Agent)
        │   ├── Task 1.1: "DNS enumeration"
        │   ├── Task 1.2: "Subdomain discovery"
        │   └── Task 1.3: "Port scanning"
        ├── Task 2: "Vulnerability scanning" (Exploit Agent)
        │   ├── Task 2.1: "Web vulnerabilities"
        │   └── Task 2.2: "Network vulnerabilities"
        ├── Task 3: "Exploitation" (Exploit Agent)
        └── Task 4: "Reporting" (Reporting Agent)
        """
        
        root = PentestingTask(
            id="root",
            name=f"Pentest: {target}",
            description=objective,
            agent="planner",
            dependencies=[],
            status=TaskStatus.PENDING,
            priority=0,
            children=[]
        )
        
        # Build child tasks
        recon_task = PentestingTask(
            id="task_1",
            name="Reconnaissance",
            description="Gather information about the target",
            agent="recon",
            dependencies=[],
            status=TaskStatus.PENDING,
            priority=1,
            children=[
                PentestingTask(
                    id="task_1_1",
                    name="DNS Enumeration",
                    description="Enumerate DNS records",
                    agent="recon",
                    dependencies=[],
                    status=TaskStatus.PENDING,
                    priority=1
                ),
                # ... more subtasks
            ]
        )
        
        root.children.append(recon_task)
        self.root_task = root
        self._register_tasks(root)
        
        return root
    
    def _register_tasks(self, task: PentestingTask):
        """Register all tasks for quick lookup"""
        self.task_registry[task.id] = task
        if task.children:
            for child in task.children:
                self._register_tasks(child)
    
    def get_next_task(self) -> Optional[PentestingTask]:
        """
        Get the next task that's ready to execute.
        Considers dependencies and priority.
        """
        def find_ready_task(task: PentestingTask) -> Optional[PentestingTask]:
            # Check if dependencies are met
            if task.status == TaskStatus.PENDING:
                deps_met = all(
                    self.task_registry[dep_id].status == TaskStatus.COMPLETED
                    for dep_id in task.dependencies
                )
                if deps_met:
                    return task
            
            # Check children
            if task.children:
                for child in task.children:
                    ready = find_ready_task(child)
                    if ready:
                        return ready
            
            return None
        
        return find_ready_task(self.root_task)
    
    def update_task_status(self, task_id: str, status: TaskStatus, result: Optional[Dict] = None):
        """Update task status and result"""
        task = self.task_registry.get(task_id)
        if task:
            task.status = status
            task.result = result
```

---

## 🚀 Usage Examples

### Example 1: Autonomous Reconnaissance
```python
from redcalibur.ai_core.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()

result = await orchestrator.execute_workflow(
    objective="Perform comprehensive reconnaissance on the target",
    target="example.com",
    workflow_type="autonomous"
)

print(f"Completed in {result['iterations']} iterations")
print(f"Findings: {result['final_output']}")
```

### Example 2: Supervised Exploitation
```python
# Supervised mode with human approval at each step
result = await orchestrator.execute_workflow(
    objective="Find and exploit SQL injection vulnerabilities",
    target="https://vulnerable-app.com",
    workflow_type="supervised"
)
```

### Example 3: PTT-Based Workflow
```python
from redcalibur.ai_core.ptt import PTTManager

ptt = PTTManager()
tree = ptt.build_tree(
    objective="Complete penetration test",
    target="corporate-network.local"
)

# Execute tasks in order
while True:
    task = ptt.get_next_task()
    if not task:
        break
    
    # Execute via orchestrator
    agent = orchestrator.agents[task.agent]
    result = await agent.execute({'task': task})
    
    # Update PTT
    ptt.update_task_status(
        task.id,
        TaskStatus.COMPLETED,
        result
    )
```

---

## 🔧 Integration Points

### 1. Tool Manager Integration
```python
# The agents use ToolManager to execute security tools
# See: redcalibur/ai_core/tool_manager.py

from redcalibur.ai_core.tool_manager import ToolManager

tool_manager = ToolManager()
result = await tool_manager.execute_tool(
    tool_name="nmap",
    parameters={"target": "192.168.1.1", "scan_type": "full"}
)
```

### 2. MCP Integration
```python
# MCP servers can be called as tools
result = await tool_manager.execute_mcp_tool(
    server="nmap-mcp",
    tool="scan",
    arguments={"host": "192.168.1.1"}
)
```

### 3. Knowledge Base (RAG)
```python
# Agents can query past engagements
from redcalibur.ai_core.knowledge_base import KnowledgeBase

kb = KnowledgeBase()
similar_cases = await kb.query(
    "Previous SQL injection exploits against login forms"
)
```

---

## 📊 Monitoring & Observability

### Agent Tracing
```python
# OpenTelemetry integration
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("agent.execute") as span:
    span.set_attribute("agent.name", self.name)
    span.set_attribute("agent.state", self.state.value)
    result = await self.execute(context)
    span.set_attribute("agent.confidence", thought.confidence)
```

---

## 🎯 Next Steps

1. Implement base agent class
2. Create specialized agents
3. Build orchestrator
4. Integrate with existing RedCalibur tools
5. Add PTT support
6. Implement handoff mechanism
7. Add observability
8. Test with real-world scenarios

---

**Implementation Priority**: HIGH
**Estimated Time**: 4 weeks
**Dependencies**: Tool Manager, LLM integration, Knowledge Base
