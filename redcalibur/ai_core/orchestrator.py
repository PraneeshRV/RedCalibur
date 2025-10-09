"""
Agent Orchestrator - Coordinates multiple agents to accomplish complex tasks
"""

from typing import Dict, List, Optional, Any
from .agents import PlannerAgent, ReconAgent, ExploitAgent, ReportingAgent
import logging

class AgentOrchestrator:
    """
    Coordinates multiple agents to accomplish complex penetration testing tasks.
    Implements handoff mechanism and manages agent lifecycle.
    """
    
    def __init__(self):
        self.agents = {
            'planner': PlannerAgent(),
            'recon': ReconAgent(),
            'exploit': ExploitAgent(),
            'reporting': ReportingAgent()
        }
        self.current_agent = None
        self.execution_history = []
        self.logger = logging.getLogger("orchestrator")
        
    def execute_workflow(
        self,
        objective: str,
        target: str,
        max_iterations: int = 10
    ) -> Dict[str, Any]:
        """
        Execute a multi-agent workflow to accomplish an objective.
        
        Args:
            objective: High-level goal (e.g., "Perform penetration test")
            target: Target system (URL, IP, domain)
            max_iterations: Maximum number of agent interactions
            
        Returns:
            Complete workflow results including all agent outputs
        """
        
        print(f"\n{'='*70}")
        print(f"🎯 RedCalibur Multi-Agent System")
        print(f"{'='*70}")
        print(f"Objective: {objective}")
        print(f"Target: {target}")
        print(f"{'='*70}\n")
        
        # Start with planner agent
        context = {
            'objective': objective,
            'target': target
        }
        
        # Agent workflow sequence
        agent_sequence = ['planner', 'recon', 'exploit', 'reporting']
        
        for iteration, agent_name in enumerate(agent_sequence, 1):
            print(f"\n{'─'*70}")
            print(f"🤖 Iteration {iteration}: {agent_name.upper()} Agent")
            print(f"{'─'*70}")
            
            # Get current agent
            agent = self.agents[agent_name]
            self.current_agent = agent
            
            # Execute agent
            try:
                result = agent.execute(context)
                
                # Log execution
                self.execution_history.append({
                    'iteration': iteration,
                    'agent': agent.name,
                    'result': result
                })
                
                # Display results
                self._display_agent_output(agent, result)
                
                # Update context for next agent
                context['previous_results'] = result
                context[f'{agent_name}_output'] = result
                
            except Exception as e:
                self.logger.error(f"Agent {agent_name} failed: {str(e)}")
                print(f"❌ Error: {str(e)}")
                break
        
        print(f"\n{'='*70}")
        print(f"✅ Workflow Completed")
        print(f"{'='*70}")
        
        return {
            'success': True,
            'iterations': len(self.execution_history),
            'history': self.execution_history,
            'target': target,
            'objective': objective
        }
    
    def _display_agent_output(self, agent, result: Dict[str, Any]):
        """Display formatted agent output"""
        
        print(f"\n📊 Agent: {agent.name}")
        print(f"State: {agent.state.value}")
        
        if agent.memory:
            last_memory = agent.memory[-1]
            thought = last_memory['thought']
            action = last_memory['action']
            
            print(f"\n💭 Reasoning:")
            print(f"   Observation: {thought.observation}")
            print(f"   Confidence: {thought.confidence:.0%}")
            print(f"   Plan: {thought.plan}")
            
            print(f"\n⚡ Action:")
            print(f"   Tool: {action.tool}")
            print(f"   Reasoning: {action.reasoning}")
            print(f"   Expected: {action.expected_outcome}")
            
            print(f"\n✓ Result:")
            if result.get('success'):
                print(f"   Status: Success ✅")
                print(f"   Message: {result.get('message', 'N/A')}")
            else:
                print(f"   Status: Failed ❌")
                print(f"   Error: {result.get('error', 'N/A')}")
    
    def get_summary(self) -> str:
        """Get a summary of the workflow execution"""
        
        summary = f"\n{'='*70}\n"
        summary += "📋 Workflow Execution Summary\n"
        summary += f"{'='*70}\n"
        summary += f"Total Iterations: {len(self.execution_history)}\n"
        summary += f"Agents Used: {', '.join([h['agent'] for h in self.execution_history])}\n"
        summary += f"\nAgent Memory:\n"
        
        for agent_name, agent in self.agents.items():
            summary += agent.get_memory_summary()
        
        return summary
    
    def list_agents(self) -> List[str]:
        """List all available agents"""
        return list(self.agents.keys())
    
    def get_agent_info(self, agent_name: str) -> Dict[str, Any]:
        """Get information about a specific agent"""
        if agent_name not in self.agents:
            return {'error': f'Agent {agent_name} not found'}
        
        agent = self.agents[agent_name]
        return {
            'name': agent.name,
            'description': agent.description,
            'tools': agent.tools,
            'state': agent.state.value,
            'memory_entries': len(agent.memory)
        }
