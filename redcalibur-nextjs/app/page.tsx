'use client';

import { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import WorkflowExecutor from './components/WorkflowExecutor';
import { MessageSquare, Workflow, Shield, Activity, Terminal } from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'chat' | 'workflow'>('chat');

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
                  RedCalibur AI
                </h1>
                <p className="text-xs text-gray-500">Powered by Gemini 2.0 Flash</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 bg-green-500/10 border border-green-500/30 px-3 py-1 rounded-full">
                <Activity className="text-green-500" size={16} />
                <span className="text-sm text-green-400">AI Active</span>
              </div>
              <a
                href="/api/health"
                target="_blank"
                className="flex items-center gap-2 bg-gray-800/50 border border-gray-700 px-3 py-1 rounded-full hover:border-red-500/50 transition-colors"
              >
                <Terminal size={16} />
                <span className="text-sm">Health</span>
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="container mx-auto px-6 py-6">
        <div className="bg-gray-900/50 backdrop-blur-sm border border-red-500/20 rounded-lg p-2 inline-flex gap-2">
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg transition-all font-medium ${
              activeTab === 'chat'
                ? 'bg-red-500 text-white shadow-lg shadow-red-500/50'
                : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'
            }`}
          >
            <MessageSquare size={20} />
            Chat Interface
          </button>
          <button
            onClick={() => setActiveTab('workflow')}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg transition-all font-medium ${
              activeTab === 'workflow'
                ? 'bg-red-500 text-white shadow-lg shadow-red-500/50'
                : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'
            }`}
          >
            <Workflow size={20} />
            Workflow Executor
          </button>
        </div>
      </div>

      {/* Main Content */}
      <main className="container mx-auto px-6 pb-6">
        <div className="bg-gray-900/30 backdrop-blur-sm border border-red-500/20 rounded-lg overflow-hidden h-[calc(100vh-280px)]">
          {activeTab === 'chat' ? <ChatInterface /> : <WorkflowExecutor />}
        </div>
      </main>

      {/* Footer */}
      <footer className="container mx-auto px-6 py-4 text-center text-gray-500 text-sm">
        <p>
          RedCalibur AI Security Platform • Built with Next.js & FastAPI • 
          <a href="http://localhost:8000/docs" target="_blank" className="text-red-500 hover:text-red-400 ml-1">
            API Documentation
          </a>
        </p>
      </footer>
    </div>
  );
}
