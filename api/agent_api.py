"""
RedCalibur AI Agent API
FastAPI backend for connecting frontend to AI agents
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import json
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redcalibur.ai_core.agents import PlannerAgent, ReconAgent, ExploitAgent, ReportingAgent
from redcalibur.ai_core.orchestrator import AgentOrchestrator

app = FastAPI(
    title="RedCalibur AI Agent API",
    description="AI-Powered Penetration Testing Multi-Agent System",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
orchestrator = AgentOrchestrator()

# Pydantic models for API
class AgentRequest(BaseModel):
    agent_type: str  # "planner", "recon", "exploit", "reporting"
    objective: str
    target: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class WorkflowRequest(BaseModel):
    objective: str
    target: str
    workflow_type: str = "full"  # "full", "recon_only", "exploit_only"

class ChatMessage(BaseModel):
    message: str
    target: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

# Active WebSocket connections
active_connections: List[WebSocket] = []

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "RedCalibur AI Agent API",
        "version": "1.0.0",
        "status": "operational",
        "ai_enabled": True,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/agents/status")
async def get_agents_status():
    """Get status of all agents"""
    agents_info = []
    
    for agent_name, agent in orchestrator.agents.items():
        agents_info.append({
            "name": agent_name,
            "type": agent.__class__.__name__,
            "ai_enabled": agent.use_ai,
            "model": agent.llm.model_name if agent.use_ai else "rule-based",
            "capabilities": agent.get_capabilities(),
            "memory_size": len(agent.memory)
        })
    
    return {
        "agents": agents_info,
        "total_agents": len(agents_info),
        "ai_enabled": all(agent.use_ai for agent in orchestrator.agents.values()),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/agent/execute")
async def execute_agent(request: AgentRequest):
    """Execute a single agent"""
    try:
        # Get the agent
        agent_map = {
            "planner": orchestrator.agents.get("Planner"),
            "recon": orchestrator.agents.get("Recon"),
            "exploit": orchestrator.agents.get("Exploit"),
            "reporting": orchestrator.agents.get("Reporting")
        }
        
        agent = agent_map.get(request.agent_type.lower())
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent '{request.agent_type}' not found")
        
        # Prepare input
        input_data = {
            "objective": request.objective,
            "target": request.target or "not specified",
        }
        if request.context:
            input_data.update(request.context)
        
        # Execute agent
        result = agent.execute(input_data)
        
        # Get the latest thought
        latest_thought = agent.memory[-1] if agent.memory else None
        
        return {
            "success": True,
            "agent": request.agent_type,
            "result": result,
            "thought": {
                "analysis": latest_thought['thought'].analysis if latest_thought else None,
                "action": latest_thought['action'] if latest_thought else None,
                "timestamp": latest_thought['timestamp'].isoformat() if latest_thought else None
            },
            "ai_enabled": agent.use_ai,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workflow/execute")
async def execute_workflow(request: WorkflowRequest):
    """Execute a full workflow with multiple agents"""
    try:
        # Create workflow configuration
        workflow = {
            "objective": request.objective,
            "target": request.target,
            "workflow_type": request.workflow_type
        }
        
        # Execute workflow
        results = orchestrator.execute_workflow(workflow)
        
        # Get execution history
        history = [
            {
                "agent": entry["agent"],
                "action": entry["action"],
                "result": entry["result"],
                "timestamp": entry["timestamp"].isoformat()
            }
            for entry in orchestrator.execution_history
        ]
        
        return {
            "success": True,
            "workflow": workflow,
            "results": results,
            "history": history,
            "agents_used": len(history),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_with_ai(message: ChatMessage):
    """Chat interface - interprets user intent and executes appropriate agents"""
    try:
        # Use PlannerAgent to interpret the user's intent
        planner = orchestrator.agents["Planner"]
        
        input_data = {
            "objective": message.message,
            "target": message.target or "not specified",
        }
        if message.context:
            input_data.update(message.context)
        
        # Get AI analysis
        result = planner.execute(input_data)
        
        # Extract thought
        latest_thought = planner.memory[-1] if planner.memory else None
        
        return {
            "success": True,
            "response": latest_thought['thought'].analysis if latest_thought else result.get('plan', 'Analysis complete'),
            "suggested_agents": result.get('agents', []),
            "suggested_workflow": result.get('workflow', 'custom'),
            "ai_enabled": planner.use_ai,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/workflow")
async def websocket_workflow(websocket: WebSocket):
    """WebSocket endpoint for real-time workflow updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Receive workflow request
            data = await websocket.receive_text()
            request_data = json.loads(data)
            
            # Send start notification
            await websocket.send_json({
                "type": "workflow_start",
                "objective": request_data.get("objective"),
                "timestamp": datetime.now().isoformat()
            })
            
            # Execute workflow with real-time updates
            workflow = {
                "objective": request_data.get("objective"),
                "target": request_data.get("target"),
                "workflow_type": request_data.get("workflow_type", "full")
            }
            
            # Execute each agent and send updates
            for agent_name in ["Planner", "Recon", "Exploit", "Reporting"]:
                agent = orchestrator.agents[agent_name]
                
                # Send agent start
                await websocket.send_json({
                    "type": "agent_start",
                    "agent": agent_name,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Execute agent
                result = agent.execute({
                    "objective": workflow["objective"],
                    "target": workflow["target"]
                })
                
                # Send agent complete
                latest_thought = agent.memory[-1] if agent.memory else None
                await websocket.send_json({
                    "type": "agent_complete",
                    "agent": agent_name,
                    "result": result,
                    "thought": latest_thought['thought'].analysis if latest_thought else None,
                    "timestamp": datetime.now().isoformat()
                })
                
                await asyncio.sleep(0.5)  # Small delay for UX
            
            # Send workflow complete
            await websocket.send_json({
                "type": "workflow_complete",
                "timestamp": datetime.now().isoformat()
            })
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
        active_connections.remove(websocket)

@app.get("/api/history")
async def get_execution_history():
    """Get execution history"""
    history = [
        {
            "agent": entry["agent"],
            "action": entry["action"],
            "result": entry["result"],
            "timestamp": entry["timestamp"].isoformat()
        }
        for entry in orchestrator.execution_history
    ]
    
    return {
        "history": history,
        "total_executions": len(history),
        "timestamp": datetime.now().isoformat()
    }

@app.delete("/api/history")
async def clear_history():
    """Clear execution history"""
    orchestrator.execution_history.clear()
    for agent in orchestrator.agents.values():
        agent.memory.clear()
    
    return {
        "success": True,
        "message": "History cleared",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
