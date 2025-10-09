'use client';

import { useState } from 'react';
import { 
  Terminal, 
  Search, 
  Shield, 
  Bug, 
  Database, 
  Globe, 
  Wifi, 
  Lock,
  Zap,
  FileText,
  Eye,
  Target,
  Activity
} from 'lucide-react';

interface Tool {
  id: string;
  name: string;
  category: string;
  icon: any;
  description: string;
  command: string;
  placeholder: string;
}

const tools: Tool[] = [
  {
    id: 'nmap',
    name: 'Nmap Scanner',
    category: 'reconnaissance',
    icon: Search,
    description: 'Network discovery and security auditing',
    command: 'nmap',
    placeholder: 'Enter target IP or domain (e.g., 192.168.1.1 or example.com)'
  },
  {
    id: 'subdomain',
    name: 'Subdomain Enumeration',
    category: 'reconnaissance',
    icon: Globe,
    description: 'Discover subdomains using AI-powered techniques',
    command: 'subdomain_enum',
    placeholder: 'Enter domain (e.g., example.com)'
  },
  {
    id: 'port_scan',
    name: 'Port Scanner',
    category: 'reconnaissance',
    icon: Wifi,
    description: 'Fast port scanning and service detection',
    command: 'port_scan',
    placeholder: 'Enter target IP (e.g., 192.168.1.1)'
  },
  {
    id: 'whois',
    name: 'WHOIS Lookup',
    category: 'reconnaissance',
    icon: FileText,
    description: 'Domain registration and ownership information',
    command: 'whois',
    placeholder: 'Enter domain (e.g., example.com)'
  },
  {
    id: 'dns_enum',
    name: 'DNS Enumeration',
    category: 'reconnaissance',
    icon: Database,
    description: 'Enumerate DNS records and zone information',
    command: 'dns_enum',
    placeholder: 'Enter domain (e.g., example.com)'
  },
  {
    id: 'vuln_scan',
    name: 'Vulnerability Scanner',
    category: 'exploitation',
    icon: Bug,
    description: 'AI-powered vulnerability detection',
    command: 'vuln_scan',
    placeholder: 'Enter target URL or IP'
  },
  {
    id: 'exploit_search',
    name: 'Exploit Search',
    category: 'exploitation',
    icon: Target,
    description: 'Search for exploits and CVEs',
    command: 'exploit_search',
    placeholder: 'Enter software name or CVE ID'
  },
  {
    id: 'payload_gen',
    name: 'Payload Generator',
    category: 'exploitation',
    icon: Zap,
    description: 'Generate custom payloads with AI',
    command: 'payload_gen',
    placeholder: 'Describe payload requirements'
  },
  {
    id: 'web_crawl',
    name: 'Web Crawler',
    category: 'reconnaissance',
    icon: Eye,
    description: 'Crawl and map web applications',
    command: 'web_crawl',
    placeholder: 'Enter website URL'
  },
  {
    id: 'phishing_detect',
    name: 'Phishing Detection',
    category: 'analysis',
    icon: Shield,
    description: 'Analyze URLs for phishing indicators',
    command: 'phishing_detect',
    placeholder: 'Enter URL to analyze'
  },
  {
    id: 'password_audit',
    name: 'Password Audit',
    category: 'exploitation',
    icon: Lock,
    description: 'Test password strength and common attacks',
    command: 'password_audit',
    placeholder: 'Enter password hash or service URL'
  },
  {
    id: 'report_gen',
    name: 'Report Generator',
    category: 'reporting',
    icon: FileText,
    description: 'Generate professional penetration test reports',
    command: 'report_gen',
    placeholder: 'Enter target for report generation'
  }
];

export default function ToolSelector({ onSelectTool }: { onSelectTool: (tool: Tool, target: string) => void }) {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTool, setSelectedTool] = useState<Tool | null>(null);
  const [target, setTarget] = useState('');

  const categories = [
    { id: 'all', name: 'All Tools', icon: Terminal },
    { id: 'reconnaissance', name: 'Reconnaissance', icon: Search },
    { id: 'exploitation', name: 'Exploitation', icon: Bug },
    { id: 'analysis', name: 'Analysis', icon: Activity },
    { id: 'reporting', name: 'Reporting', icon: FileText }
  ];

  const filteredTools = tools.filter(tool => {
    const matchesCategory = selectedCategory === 'all' || tool.category === selectedCategory;
    const matchesSearch = tool.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         tool.description.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const handleExecute = () => {
    if (selectedTool && target.trim()) {
      onSelectTool(selectedTool, target);
      setTarget('');
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Search and Categories */}
      <div className="bg-gray-900/50 backdrop-blur-sm border-b border-red-500/20 p-4 space-y-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" size={20} />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search tools..."
            className="w-full bg-gray-800 border border-red-500/30 text-gray-200 rounded-lg pl-10 pr-4 py-3 focus:outline-none focus:border-red-500"
          />
        </div>

        <div className="flex gap-2 flex-wrap">
          {categories.map((category) => {
            const Icon = category.icon;
            return (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                  selectedCategory === category.id
                    ? 'bg-red-500 text-white'
                    : 'bg-gray-800/50 text-gray-400 hover:text-gray-200 hover:bg-gray-800'
                }`}
              >
                <Icon size={16} />
                <span className="text-sm font-medium">{category.name}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Tools Grid */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredTools.map((tool) => {
            const Icon = tool.icon;
            return (
              <button
                key={tool.id}
                onClick={() => setSelectedTool(tool)}
                className={`text-left bg-gray-900/50 backdrop-blur-sm border rounded-lg p-4 transition-all hover:scale-105 ${
                  selectedTool?.id === tool.id
                    ? 'border-red-500 shadow-lg shadow-red-500/20'
                    : 'border-gray-700 hover:border-red-500/50'
                }`}
              >
                <div className="flex items-start gap-3">
                  <div className="bg-red-500/10 p-2 rounded-lg">
                    <Icon className="text-red-500" size={24} />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-white font-semibold mb-1">{tool.name}</h3>
                    <p className="text-gray-400 text-sm">{tool.description}</p>
                    <div className="mt-2">
                      <span className="text-xs px-2 py-1 bg-gray-800 text-gray-400 rounded">
                        {tool.category}
                      </span>
                    </div>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Execute Panel */}
      {selectedTool && (
        <div className="bg-gray-900/80 backdrop-blur-sm border-t border-red-500/30 p-4">
          <div className="flex items-center gap-3 mb-3">
            {(() => {
              const Icon = selectedTool.icon;
              return <Icon className="text-red-500" size={20} />;
            })()}
            <h3 className="text-white font-semibold">{selectedTool.name}</h3>
          </div>
          <div className="flex gap-3">
            <input
              type="text"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleExecute()}
              placeholder={selectedTool.placeholder}
              className="flex-1 bg-gray-800 border border-red-500/30 text-gray-200 rounded-lg px-4 py-3 focus:outline-none focus:border-red-500"
            />
            <button
              onClick={handleExecute}
              disabled={!target.trim()}
              className="bg-red-500 hover:bg-red-600 disabled:bg-gray-700 disabled:text-gray-500 text-white rounded-lg px-8 py-3 transition-colors font-semibold flex items-center gap-2"
            >
              <Terminal size={20} />
              Execute
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
