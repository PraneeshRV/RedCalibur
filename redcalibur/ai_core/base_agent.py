"""
Base Agent Implementation for RedCalibur
Simple but functional multi-agent system with ReACT pattern
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
import json

class AgentState(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class AgentThought:
    """Represents an agent's reasoning process"""
    observation: str
    analysis: str
    plan: str
    confidence: float

@dataclass
class AgentAction:
    """Represents an action the agent wants to take"""
    tool: str
    parameters: Dict[str, Any]
    reasoning: str
    expected_outcome: str

class BaseAgent(ABC):
    """
    Base class for all RedCalibur agents.
    Implements ReACT (Reasoning + Action) pattern.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        tools: Optional[List[str]] = None
    ):
        self.name = name
        self.description = description
        self.tools = tools or []
        self.state = AgentState.IDLE
        self.memory = []
        self.logger = logging.getLogger(f"agent.{name}")
        
    @abstractmethod
    def think(self, context: Dict[str, Any]) -> AgentThought:
        """
        Reasoning phase: Analyze the situation and plan next steps.
        """
        pass
    
    @abstractmethod
    def act(self, thought: AgentThought) -> AgentAction:
        """
        Action phase: Decide what action to take based on reasoning.
        """
        pass
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution loop: Think → Act → Execute cycle.
        """
        try:
            self.state = AgentState.THINKING
            self.logger.info(f"{self.name} is thinking...")
            thought = self.think(context)
            
            self.state = AgentState.ACTING
            self.logger.info(f"{self.name} decided to act: {thought.plan}")
            action = self.act(thought)
            
            # Execute the action
            result = self._execute_action(action, context)
            
            # Store in memory
            self.memory.append({
                'thought': thought,
                'action': action,
                'result': result
            })
            
            self.state = AgentState.COMPLETED
            return result
            
        except Exception as e:
            self.state = AgentState.ERROR
            self.logger.error(f"{self.name} error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.name
            }
    
    def _execute_action(self, action: AgentAction, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the action - simplified for demo"""
        # In real implementation, this would call the tool manager
        self.logger.info(f"Executing {action.tool} with params: {action.parameters}")
        
        # Simulate tool execution
        return {
            'success': True,
            'tool': action.tool,
            'parameters': action.parameters,
            'reasoning': action.reasoning,
            'simulated': True,
            'message': f"Successfully executed {action.tool}"
        }
    
    def handoff_to(self, agent_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handoff control to another agent"""
        return {
            'handoff': True,
            'target_agent': agent_name,
            'context': context,
            'reason': f"{self.name} recommends {agent_name} for this task"
        }
    
    def get_memory_summary(self) -> str:
        """Get a summary of agent's memory"""
        if not self.memory:
            return f"{self.name} has no memory yet."
        
        summary = f"\n{self.name} Memory ({len(self.memory)} entries):\n"
        for i, entry in enumerate(self.memory, 1):
            summary += f"  {i}. {entry['action'].tool}: {entry['action'].reasoning}\n"
        return summary
