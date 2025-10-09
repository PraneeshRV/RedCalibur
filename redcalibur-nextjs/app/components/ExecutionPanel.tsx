'use client';

import { useEffect, useRef } from 'react';
import { Terminal, CheckCircle, XCircle, Loader, Clock } from 'lucide-react';

interface ExecutionResult {
  id: string;
  tool: string;
  target: string;
  status: 'running' | 'completed' | 'failed';
  output: string;
  timestamp: string;
  duration?: number;
}

export default function ExecutionPanel({ 
  results 
}: { 
  results: ExecutionResult[] 
}) {
  const outputRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [results]);

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

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'border-yellow-500/30 bg-yellow-500/5';
      case 'completed':
        return 'border-green-500/30 bg-green-500/5';
      case 'failed':
        return 'border-red-500/30 bg-red-500/5';
      default:
        return 'border-gray-700 bg-gray-900/30';
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="bg-gray-900/50 backdrop-blur-sm border-b border-red-500/20 p-4">
        <div className="flex items-center gap-2">
          <Terminal className="text-red-500" size={20} />
          <h2 className="text-lg font-bold text-gray-200">Execution Results</h2>
          <span className="ml-auto text-sm text-gray-500">{results.length} task(s)</span>
        </div>
      </div>

      <div ref={outputRef} className="flex-1 overflow-y-auto p-4 space-y-4">
        {results.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <Terminal className="text-gray-600 mb-4" size={64} />
            <h3 className="text-xl font-bold text-gray-400 mb-2">
              No Tasks Executed Yet
            </h3>
            <p className="text-gray-600">
              Select a tool and execute a command to see results here
            </p>
          </div>
        ) : (
          results.map((result) => (
            <div
              key={result.id}
              className={`border rounded-lg p-4 ${getStatusColor(result.status)}`}
            >
              <div className="flex items-start gap-3 mb-3">
                {getStatusIcon(result.status)}
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <h3 className="text-white font-semibold">{result.tool}</h3>
                    <span className="text-gray-500">→</span>
                    <span className="text-gray-400">{result.target}</span>
                  </div>
                  <div className="flex items-center gap-3 mt-1 text-xs text-gray-500">
                    <span>{new Date(result.timestamp).toLocaleTimeString()}</span>
                    {result.duration && (
                      <span>Duration: {result.duration}s</span>
                    )}
                  </div>
                </div>
              </div>

              {result.output && (
                <div className="bg-black/30 rounded-lg p-3 mt-3">
                  <pre className="text-sm text-gray-300 whitespace-pre-wrap font-mono overflow-x-auto">
                    {result.output}
                  </pre>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
