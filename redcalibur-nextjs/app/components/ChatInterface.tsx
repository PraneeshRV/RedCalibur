'use client';

import { useState, useEffect, useRef } from 'react';
import { Send, Terminal, Shield, Zap, Activity } from 'lucide-react';

interface Message {
  role: 'user' | 'agent';
  content: string;
  timestamp: string;
  agent?: string;
}

interface Agent {
  name: string;
  status: string;
  model: string;
  capabilities: string[];
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selectedAgent, setSelectedAgent] = useState('auto');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchAgents();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchAgents = async () => {
    try {
      const response = await fetch('/api/agents');
      const data = await response.json();
      setAgents(data.agents || []);
    } catch (error) {
      console.error('Failed to fetch agents:', error);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          agent: selectedAgent,
        }),
      });

      const data = await response.json();

      const agentMessage: Message = {
        role: 'agent',
        content: data.response || 'No response received',
        timestamp: new Date().toISOString(),
        agent: data.agent,
      };

      setMessages((prev) => [...prev, agentMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        role: 'agent',
        content: 'Error: Failed to get response from agent',
        timestamp: new Date().toISOString(),
        agent: 'System',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Agent Selector */}
      <div className="bg-gray-900/50 backdrop-blur-sm border-b border-red-500/20 p-4">
        <div className="flex items-center gap-4">
          <Shield className="text-red-500" size={20} />
          <select
            value={selectedAgent}
            onChange={(e) => setSelectedAgent(e.target.value)}
            className="bg-gray-800 border border-red-500/30 text-gray-200 rounded-lg px-4 py-2 focus:outline-none focus:border-red-500"
          >
            <option value="auto">Auto Select Agent</option>
            {agents.map((agent) => (
              <option key={agent.name} value={agent.name}>
                {agent.name}
              </option>
            ))}
          </select>
          <div className="flex gap-2 ml-auto">
            {agents.map((agent) => (
              <div
                key={agent.name}
                className="flex items-center gap-2 bg-gray-800/50 px-3 py-1 rounded-full border border-red-500/20"
              >
                <Activity className="text-green-500" size={12} />
                <span className="text-xs text-gray-400">{agent.name}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <Terminal className="text-red-500/50 mb-4" size={64} />
            <h3 className="text-xl font-bold text-gray-300 mb-2">
              RedCalibur AI Agent System
            </h3>
            <p className="text-gray-500 max-w-md">
              Start a conversation with our AI-powered security agents. Ask about reconnaissance,
              vulnerability assessment, or security analysis.
            </p>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[70%] rounded-lg p-4 ${
                    message.role === 'user'
                      ? 'bg-red-500/20 border border-red-500/30 text-gray-200'
                      : 'bg-gray-800/50 border border-gray-700 text-gray-300'
                  }`}
                >
                  {message.agent && (
                    <div className="flex items-center gap-2 mb-2 text-xs text-red-400">
                      <Zap size={12} />
                      <span>{message.agent}</span>
                    </div>
                  )}
                  <div className="whitespace-pre-wrap">{message.content}</div>
                  <div className="text-xs text-gray-500 mt-2">
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input Area */}
      <div className="bg-gray-900/50 backdrop-blur-sm border-t border-red-500/20 p-4">
        <div className="flex gap-3">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter your security query or target..."
            className="flex-1 bg-gray-800 border border-red-500/30 text-gray-200 rounded-lg px-4 py-3 focus:outline-none focus:border-red-500 resize-none"
            rows={2}
            disabled={loading}
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="bg-red-500 hover:bg-red-600 disabled:bg-gray-700 disabled:text-gray-500 text-white rounded-lg px-6 py-3 transition-colors flex items-center gap-2"
          >
            {loading ? (
              <>
                <Activity className="animate-spin" size={20} />
                Processing...
              </>
            ) : (
              <>
                <Send size={20} />
                Send
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
