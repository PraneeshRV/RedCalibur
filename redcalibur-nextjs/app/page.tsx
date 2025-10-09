'use client';

import { useState } from 'react';
import ToolSelector from './components/ToolSelector';
import ExecutionPanel from './components/ExecutionPanel';
import { Shield, Terminal, Zap } from 'lucide-react';

interface Tool {
  id: string;
  name: string;
  category: string;
  icon: any;
  description: string;
  command: string;
  placeholder: string;
}

interface ExecutionResult {
  id: string;
  tool: string;
  target: string;
  status: 'running' | 'completed' | 'failed';
  output: string;
  timestamp: string;
  duration?: number;
}

export default function Home() {
  const [results, setResults] = useState<ExecutionResult[]>([]);

  const handleExecuteTool = async (tool: Tool, target: string) => {
    const executionId = Date.now().toString();
    const startTime = Date.now();

    // Add running task
    const newResult: ExecutionResult = {
      id: executionId,
      tool: tool.name,
      target: target,
      status: 'running',
      output: `Executing ${tool.name} on ${target}...\n`,
      timestamp: new Date().toISOString(),
    };

    setResults((prev) => [newResult, ...prev]);

    try {
      // Call API to execute the tool
      const response = await fetch('/api/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tool: tool.command,
          target: target,
        }),
      });

      const data = await response.json();
      const duration = Math.round((Date.now() - startTime) / 1000);

      // Update with results
      setResults((prev) =>
        prev.map((r) =>
          r.id === executionId
            ? {
                ...r,
                status: data.success ? 'completed' : 'failed',
                output: data.output || data.error || 'No output received',
                duration: duration,
              }
            : r
        )
      );
    } catch (error) {
      const duration = Math.round((Date.now() - startTime) / 1000);
      setResults((prev) =>
        prev.map((r) =>
          r.id === executionId
            ? {
                ...r,
                status: 'failed',
                output: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
                duration: duration,
              }
            : r
        )
      );
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-black text-white">
      {/* Header */}
      <header className="bg-gray-900/80 backdrop-blur-sm border-b border-red-500/30 sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Shield className="text-red-500" size={32} />
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-red-500 to-red-700 bg-clip-text text-transparent">
                  RedCalibur
                </h1>
                <p className="text-xs text-gray-500">AI-Powered Red Teaming Toolkit</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/30 px-3 py-1 rounded-full">
                <Zap className="text-red-500" size={16} />
                <span className="text-sm text-red-400">12 Tools Available</span>
              </div>
              <a
                href="http://localhost:8000/docs"
                target="_blank"
                className="flex items-center gap-2 bg-gray-800/50 border border-gray-700 px-3 py-1 rounded-full hover:border-red-500/50 transition-colors"
              >
                <Terminal size={16} />
                <span className="text-sm">API Docs</span>
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content - Split View */}
      <main className="container mx-auto px-6 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[calc(100vh-140px)]">
          {/* Left Panel - Tool Selector */}
          <div className="bg-gray-900/30 backdrop-blur-sm border border-red-500/20 rounded-lg overflow-hidden">
            <ToolSelector onSelectTool={handleExecuteTool} />
          </div>

          {/* Right Panel - Execution Results */}
          <div className="bg-gray-900/30 backdrop-blur-sm border border-red-500/20 rounded-lg overflow-hidden">
            <ExecutionPanel results={results} />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="container mx-auto px-6 py-4 text-center text-gray-500 text-sm">
        <p>
          ⚠️ For authorized security testing only • Built with Next.js + AI
        </p>
      </footer>
    </div>
  );
}
