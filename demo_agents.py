#!/usr/bin/env python3
"""
RedCalibur Multi-Agent System Demo
Simple demonstration of the AI-powered agent system for penetration testing
"""

import sys
import logging
from redcalibur.ai_core.orchestrator import AgentOrchestrator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def demo_basic_workflow():
    """Demonstrate basic multi-agent workflow"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║              RedCalibur Multi-Agent System Demo                     ║
║              AI-Powered Penetration Testing Framework               ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Create orchestrator
    orchestrator = AgentOrchestrator()
    
    # Display available agents
    print("\n🤖 Available Agents:")
    for agent_name in orchestrator.list_agents():
        info = orchestrator.get_agent_info(agent_name)
        print(f"   • {info['name']}: {info['description']}")
        print(f"     Tools: {', '.join(info['tools'][:3])}...")
    
    # Demo 1: Simple penetration test workflow
    print("\n\n" + "="*70)
    print("Demo 1: Automated Penetration Test Workflow")
    print("="*70)
    
    result1 = orchestrator.execute_workflow(
        objective="Perform comprehensive penetration test",
        target="example.com"
    )
    
    # Display summary
    print(orchestrator.get_summary())
    
    # Demo 2: OSINT focused workflow
    print("\n\n" + "="*70)
    print("Demo 2: OSINT Reconnaissance Workflow")
    print("="*70)
    
    orchestrator2 = AgentOrchestrator()
    result2 = orchestrator2.execute_workflow(
        objective="Gather intelligence on target organization",
        target="testcompany.com"
    )
    
    print(orchestrator2.get_summary())
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    Demo Completed Successfully!                      ║
║                                                                      ║
║  Key Features Demonstrated:                                          ║
║  ✓ Multi-agent coordination                                          ║
║  ✓ ReACT pattern (Reasoning + Action)                                ║
║  ✓ Agent handoffs and orchestration                                  ║
║  ✓ Memory and context management                                     ║
║  ✓ Tool selection and execution                                      ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)

def demo_individual_agents():
    """Demonstrate individual agent capabilities"""
    
    print("\n" + "="*70)
    print("Individual Agent Demonstrations")
    print("="*70)
    
    from redcalibur.ai_core.agents import PlannerAgent, ReconAgent, ExploitAgent, ReportingAgent
    
    # Demo Planner Agent
    print("\n1. Planner Agent")
    print("-" * 70)
    planner = PlannerAgent()
    result = planner.execute({
        'objective': 'Test web application security',
        'target': 'webapp.example.com'
    })
    print(f"✓ Planner created strategy: {result.get('message', 'N/A')}")
    
    # Demo Recon Agent
    print("\n2. Recon Agent")
    print("-" * 70)
    recon = ReconAgent()
    result = recon.execute({
        'target': '192.168.1.1',
        'scan_type': 'comprehensive'
    })
    print(f"✓ Recon completed: {result.get('message', 'N/A')}")
    
    # Demo Exploit Agent
    print("\n3. Exploit Agent")
    print("-" * 70)
    exploit = ExploitAgent()
    result = exploit.execute({
        'target': 'vulnerable-app.com',
        'vulnerabilities': ['SQL Injection', 'XSS']
    })
    print(f"✓ Exploit assessment: {result.get('message', 'N/A')}")
    
    # Demo Reporting Agent
    print("\n4. Reporting Agent")
    print("-" * 70)
    reporting = ReportingAgent()
    result = reporting.execute({
        'target': 'example.com',
        'objective': 'Penetration Test',
        'findings': ['Critical: SQL Injection', 'High: XSS']
    })
    print(f"✓ Report generated: {result.get('message', 'N/A')}")

def interactive_demo():
    """Interactive demonstration"""
    
    print("\n" + "="*70)
    print("Interactive Mode")
    print("="*70)
    
    orchestrator = AgentOrchestrator()
    
    # Get user input
    try:
        target = input("\n🎯 Enter target (domain, IP, or URL): ").strip()
        if not target:
            target = "demo.testfire.net"
            print(f"   Using default: {target}")
        
        objective = input("📝 Enter objective (or press Enter for default): ").strip()
        if not objective:
            objective = "Perform security assessment"
            print(f"   Using default: {objective}")
        
        # Execute workflow
        print("\n🚀 Starting multi-agent workflow...\n")
        result = orchestrator.execute_workflow(
            objective=objective,
            target=target
        )
        
        print(orchestrator.get_summary())
        
    except KeyboardInterrupt:
        print("\n\n❌ Demo cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

def main():
    """Main demo function"""
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "interactive":
            interactive_demo()
        elif mode == "individual":
            demo_individual_agents()
        else:
            print(f"Unknown mode: {mode}")
            print("Usage: python demo_agents.py [interactive|individual]")
    else:
        # Default: Run basic workflow demo
        demo_basic_workflow()

if __name__ == "__main__":
    main()
