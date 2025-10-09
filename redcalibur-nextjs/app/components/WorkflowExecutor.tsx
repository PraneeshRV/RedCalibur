'use client';

import { useState } from 'react';
import { Play, Clock, CheckCircle, XCircle, Loader } from 'lucide-react';

interface WorkflowStep {
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: string;
}

export default function WorkflowExecutor() {
  const [target, setTarget] = useState('');
  const [running, setRunning] = useState(false);
  const [workflowId, setWorkflowId] = useState<string | null>(null);
  const [steps, setSteps] = useState<WorkflowStep[]>([]);
  const [results, setResults] = useState<any>(null);

  const executeWorkflow = async () => {
    if (!target.trim() || running) return;

    setRunning(true);
    setSteps([
      { name: 'Planning', status: 'running' },
      { name: 'Reconnaissance', status: 'pending' },
      { name: 'Analysis', status: 'pending' },
      { name: 'Reporting', status: 'pending' },
    ]);

    try {
      const response = await fetch('/api/workflow', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          target,
          workflow_type: 'full_recon',
        }),
      });

      const data = await response.json();
      setWorkflowId(data.workflow_id);

      // Simulate workflow progress
      await updateWorkflowProgress(data.workflow_id);
    } catch (error) {
      console.error('Workflow error:', error);
      setSteps((prev) =>
        prev.map((step, idx) =>
          idx === 0 ? { ...step, status: 'failed', result: 'Execution failed' } : step
        )
      );
    } finally {
      setRunning(false);
    }
  };

  const updateWorkflowProgress = async (id: string) => {
    // Simulate step-by-step execution
    for (let i = 0; i < 4; i++) {
      await new Promise((resolve) => setTimeout(resolve, 2000));
      setSteps((prev) =>
        prev.map((step, idx) => {
          if (idx === i) return { ...step, status: 'completed', result: 'Success' };
          if (idx === i + 1) return { ...step, status: 'running' };
          return step;
        })
      );
    }

    // Fetch final results
    try {
      const response = await fetch(`/api/workflow?id=${id}`);
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Failed to fetch results:', error);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running':
        return <Loader className="animate-spin text-yellow-500" size={20} />;
      case 'completed':
        return <CheckCircle className="text-green-500" size={20} />;
      case 'failed':
        return <XCircle className="text-red-500" size={20} />;
      default:
        return <Clock className="text-gray-500" size={20} />;
    }
  };

  return (
    <div className="flex flex-col h-full p-6">
      {/* Workflow Input */}
      <div className="bg-gray-900/50 backdrop-blur-sm border border-red-500/20 rounded-lg p-6 mb-6">
        <h2 className="text-xl font-bold text-gray-200 mb-4 flex items-center gap-2">
          <Play className="text-red-500" size={24} />
          Automated Workflow Execution
        </h2>
        <div className="flex gap-3">
          <input
            type="text"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            placeholder="Enter target (domain, IP, or description)..."
            className="flex-1 bg-gray-800 border border-red-500/30 text-gray-200 rounded-lg px-4 py-3 focus:outline-none focus:border-red-500"
            disabled={running}
          />
          <button
            onClick={executeWorkflow}
            disabled={running || !target.trim()}
            className="bg-red-500 hover:bg-red-600 disabled:bg-gray-700 disabled:text-gray-500 text-white rounded-lg px-8 py-3 transition-colors flex items-center gap-2 font-semibold"
          >
            {running ? (
              <>
                <Loader className="animate-spin" size={20} />
                Running...
              </>
            ) : (
              <>
                <Play size={20} />
                Execute
              </>
            )}
          </button>
        </div>
      </div>

      {/* Workflow Steps */}
      {steps.length > 0 && (
        <div className="bg-gray-900/50 backdrop-blur-sm border border-red-500/20 rounded-lg p-6 mb-6">
          <h3 className="text-lg font-bold text-gray-200 mb-4">Workflow Progress</h3>
          <div className="space-y-3">
            {steps.map((step, index) => (
              <div
                key={index}
                className="flex items-center gap-4 bg-gray-800/50 rounded-lg p-4 border border-gray-700"
              >
                {getStatusIcon(step.status)}
                <div className="flex-1">
                  <div className="text-gray-300 font-medium">{step.name}</div>
                  {step.result && <div className="text-sm text-gray-500">{step.result}</div>}
                </div>
                {step.status === 'running' && (
                  <div className="h-2 w-32 bg-gray-700 rounded-full overflow-hidden">
                    <div className="h-full bg-red-500 animate-pulse w-3/4"></div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Results */}
      {results && (
        <div className="bg-gray-900/50 backdrop-blur-sm border border-green-500/20 rounded-lg p-6 flex-1 overflow-y-auto">
          <h3 className="text-lg font-bold text-gray-200 mb-4 flex items-center gap-2">
            <CheckCircle className="text-green-500" size={24} />
            Workflow Results
          </h3>
          <pre className="text-gray-300 text-sm bg-gray-800/50 rounded-lg p-4 overflow-x-auto">
            {JSON.stringify(results, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
