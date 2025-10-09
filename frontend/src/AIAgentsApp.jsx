import React, { useState, useEffect, useRef } from 'react';
import { Send, Terminal, Brain, Shield, Search, FileText, Zap, CheckCircle, XCircle, Loader, Trash2, Activity } from 'lucide-react';
import './AIAgentsApp.css';

const API_BASE_URL = 'http://localhost:8000';

function AIAgentsApp() {
  const [activeTab, setActiveTab] = useState('chat');
  const [message, setMessage] = useState('');
  const [target, setTarget] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [agentsStatus, setAgentsStatus] = useState(null);
  const [workflowResults, setWorkflowResults] = useState(null);
  const [wsConnected, setWsConnected] = useState(false);
  const wsRef = useRef(null);
  const chatEndRef = useRef(null);

  // Agent icons mapping
  const agentIcons = {
    'Planner': Brain,
    'Recon': Search,
    'Exploit': Zap,
    'Reporting': FileText
  };

  // Scroll to bottom of chat
  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  // Fetch agents status on mount
  useEffect(() => {
    fetchAgentsStatus();
  }, []);

  const fetchAgentsStatus = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/agents/status`);
      const data = await response.json();
      setAgentsStatus(data);
    } catch (error) {
      console.error('Failed to fetch agents status:', error);
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    const userMessage = {
      type: 'user',
      content: message,
      target: target || 'Not specified',
      timestamp: new Date().toISOString()
    };

    setChatHistory(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, target: target || null })
      });

      const data = await response.json();

      const aiMessage = {
        type: 'ai',
        content: data.response,
        suggested_agents: data.suggested_agents,
        suggested_workflow: data.suggested_workflow,
        timestamp: data.timestamp
      };

      setChatHistory(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = {
        type: 'error',
        content: `Error: ${error.message}`,
        timestamp: new Date().toISOString()
      };
      setChatHistory(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setMessage('');
    }
  };

  const executeWorkflow = async (workflowType = 'full') => {
    if (!target.trim()) {
      alert('Please enter a target');
      return;
    }

    setLoading(true);
    setWorkflowResults(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/workflow/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          objective: message || 'Comprehensive security assessment',
          target: target,
          workflow_type: workflowType
        })
      });

      const data = await response.json();
      setWorkflowResults(data);
    } catch (error) {
      alert(`Workflow failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const connectWebSocket = () => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    const ws = new WebSocket(`ws://localhost:8000/ws/workflow`);
    
    ws.onopen = () => {
      setWsConnected(true);
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      const wsMessage = {
        type: 'workflow',
        subtype: data.type,
        content: data,
        timestamp: data.timestamp
      };
      
      setChatHistory(prev => [...prev, wsMessage]);
    };

    ws.onclose = () => {
      setWsConnected(false);
      console.log('WebSocket disconnected');
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    wsRef.current = ws;
  };

  const executeWorkflowWS = () => {
    if (!target.trim()) {
      alert('Please enter a target');
      return;
    }

    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      connectWebSocket();
      setTimeout(() => executeWorkflowWS(), 1000);
      return;
    }

    const workflow = {
      objective: message || 'Comprehensive security assessment',
      target: target,
      workflow_type: 'full'
    };

    wsRef.current.send(JSON.stringify(workflow));
    setMessage('');
  };

  const clearHistory = async () => {
    try {
      await fetch(`${API_BASE_URL}/api/history`, { method: 'DELETE' });
      setChatHistory([]);
      setWorkflowResults(null);
    } catch (error) {
      console.error('Failed to clear history:', error);
    }
  };

  return (
    <div className="ai-agents-app">
      {/* Header */}
      <header className="app-header">
        <div className="container">
          <div className="header-content">
            <div className="brand">
              <Shield className="brand-icon" />
              <h1 className="brand-title">RedCalibur AI</h1>
              <span className="ai-badge">
                {agentsStatus?.ai_enabled ? '🤖 AI Enabled' : '📋 Rule-Based'}
              </span>
            </div>
            <div className="header-actions">
              <button onClick={fetchAgentsStatus} className="btn btn-secondary">
                <Activity className="btn-icon" />
                Refresh Status
              </button>
              <button onClick={clearHistory} className="btn btn-danger">
                <Trash2 className="btn-icon" />
                Clear
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container main-content">
        {/* Agents Status Grid */}
        {agentsStatus && (
          <div className="agents-grid">
            {agentsStatus.agents.map((agent) => {
              const Icon = agentIcons[agent.name];
              return (
                <div key={agent.name} className="agent-card">
                  <div className="agent-header">
                    {Icon && <Icon className="agent-icon" />}
                    <h3 className="agent-name">{agent.name}</h3>
                  </div>
                  <div className="agent-details">
                    <p>Model: {agent.model}</p>
                    <p>Memory: {agent.memory_size} items</p>
                  </div>
                  <div className="agent-status">
                    {agent.ai_enabled ? (
                      <span className="status-active">
                        <CheckCircle className="status-icon" />
                        AI Active
                      </span>
                    ) : (
                      <span className="status-inactive">
                        <XCircle className="status-icon" />
                        Rule-Based
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Tabs */}
        <div className="tabs">
          <button
            onClick={() => setActiveTab('chat')}
            className={`tab ${activeTab === 'chat' ? 'active' : ''}`}
          >
            <Terminal className="tab-icon" />
            Chat Interface
          </button>
          <button
            onClick={() => setActiveTab('workflow')}
            className={`tab ${activeTab === 'workflow' ? 'active' : ''}`}
          >
            <Zap className="tab-icon" />
            Workflow
          </button>
        </div>

        {/* Chat Interface */}
        {activeTab === 'chat' && (
          <div className="chat-container">
            <div className="chat-messages">
              {chatHistory.length === 0 && (
                <div className="chat-empty">
                  <Brain className="empty-icon" />
                  <p>Start a conversation with RedCalibur AI</p>
                  <p className="empty-subtitle">Ask about targets, vulnerabilities, or pentesting strategies</p>
                </div>
              )}
              
              {chatHistory.map((msg, idx) => (
                <div key={idx} className={`message message-${msg.type}`}>
                  {msg.type === 'user' ? (
                    <div className="message-content user-message">
                      <p>{msg.content}</p>
                      {msg.target !== 'Not specified' && (
                        <p className="message-target">Target: {msg.target}</p>
                      )}
                    </div>
                  ) : msg.type === 'ai' ? (
                    <div className="message-content ai-message">
                      <div className="ai-header">
                        <Brain className="ai-icon" />
                        <span>AI Analysis</span>
                      </div>
                      <p className="ai-content">{msg.content}</p>
                      {msg.suggested_agents && msg.suggested_agents.length > 0 && (
                        <div className="ai-suggestions">
                          <p>Suggested agents: {msg.suggested_agents.join(', ')}</p>
                        </div>
                      )}
                    </div>
                  ) : msg.type === 'workflow' ? (
                    <div className="message-content workflow-message">
                      {msg.subtype === 'workflow_start' && (
                        <p className="workflow-start">🚀 Workflow started: {msg.content.objective}</p>
                      )}
                      {msg.subtype === 'agent_start' && (
                        <p className="workflow-pending">⏳ {msg.content.agent} agent executing...</p>
                      )}
                      {msg.subtype === 'agent_complete' && (
                        <div>
                          <p className="workflow-complete">✅ {msg.content.agent} completed</p>
                          {msg.content.thought && (
                            <p className="workflow-thought">{msg.content.thought}</p>
                          )}
                        </div>
                      )}
                      {msg.subtype === 'workflow_complete' && (
                        <p className="workflow-success">🎉 Workflow completed successfully!</p>
                      )}
                    </div>
                  ) : (
                    <div className="message-content error-message">
                      <p>{msg.content}</p>
                    </div>
                  )}
                </div>
              ))}
              
              {loading && (
                <div className="message message-ai">
                  <div className="message-content ai-message">
                    <Loader className="loader-icon" />
                  </div>
                </div>
              )}
              
              <div ref={chatEndRef} />
            </div>
            
            <div className="chat-input-container">
              <form onSubmit={handleChatSubmit} className="chat-form">
                <input
                  type="text"
                  value={target}
                  onChange={(e) => setTarget(e.target.value)}
                  placeholder="Target (domain, IP, or URL)..."
                  className="input-field"
                />
                <div className="input-row">
                  <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="What would you like to analyze or test?"
                    className="input-field flex-1"
                    disabled={loading}
                  />
                  <button
                    type="submit"
                    disabled={loading}
                    className="btn btn-primary"
                  >
                    <Send className="btn-icon" />
                  </button>
                </div>
                <button
                  type="button"
                  onClick={executeWorkflowWS}
                  disabled={loading}
                  className="btn btn-workflow"
                >
                  <Zap className="btn-icon" />
                  <span>Execute Full Workflow (Real-time)</span>
                  {wsConnected && <span className="ws-indicator">● Connected</span>}
                </button>
              </form>
            </div>
          </div>
        )}

        {/* Workflow Interface */}
        {activeTab === 'workflow' && (
          <div className="workflow-container">
            <div className="workflow-form-container">
              <h2 className="workflow-title">Execute Workflow</h2>
              
              <div className="form-fields">
                <div className="form-field">
                  <label>Target</label>
                  <input
                    type="text"
                    value={target}
                    onChange={(e) => setTarget(e.target.value)}
                    placeholder="example.com, 192.168.1.1, https://target.com"
                    className="input-field"
                  />
                </div>
                
                <div className="form-field">
                  <label>Objective</label>
                  <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Describe your penetration testing objective..."
                    rows="3"
                    className="input-field"
                  />
                </div>
                
                <div className="workflow-buttons">
                  <button
                    onClick={() => executeWorkflow('full')}
                    disabled={loading}
                    className="btn btn-primary flex-1"
                  >
                    {loading ? <Loader className="btn-icon animate-spin" /> : <Zap className="btn-icon" />}
                    <span>Full Workflow</span>
                  </button>
                  
                  <button
                    onClick={() => executeWorkflow('recon_only')}
                    disabled={loading}
                    className="btn btn-secondary flex-1"
                  >
                    <Search className="btn-icon" />
                    <span>Recon Only</span>
                  </button>
                  
                  <button
                    onClick={() => executeWorkflow('exploit_only')}
                    disabled={loading}
                    className="btn btn-warning flex-1"
                  >
                    <Zap className="btn-icon" />
                    <span>Exploit Only</span>
                  </button>
                </div>
              </div>
            </div>
            
            {/* Workflow Results */}
            {workflowResults && (
              <div className="workflow-results">
                <h2 className="workflow-title">Workflow Results</h2>
                
                <div className="results-list">
                  {workflowResults.history.map((entry, idx) => {
                    const Icon = agentIcons[entry.agent];
                    return (
                      <div key={idx} className="result-item">
                        <div className="result-header">
                          {Icon && <Icon className="result-icon" />}
                          <h3>{entry.agent}</h3>
                          <span className="result-time">{new Date(entry.timestamp).toLocaleTimeString()}</span>
                        </div>
                        <p className="result-action">Action: {entry.action}</p>
                        <div className="result-data">
                          <pre>{JSON.stringify(entry.result, null, 2)}</pre>
                        </div>
                      </div>
                    );
                  })}
                </div>
                
                <div className="workflow-success">
                  <p>✅ Workflow completed successfully!</p>
                  <p className="success-details">
                    {workflowResults.agents_used} agents executed • {new Date(workflowResults.timestamp).toLocaleString()}
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default AIAgentsApp;
