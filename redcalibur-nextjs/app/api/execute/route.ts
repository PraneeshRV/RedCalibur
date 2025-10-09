import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { tool, target } = body;

    if (!tool || !target) {
      return NextResponse.json(
        { success: false, error: 'Tool and target are required' },
        { status: 400 }
      );
    }

    // Map tool commands to backend endpoints
    const toolMap: { [key: string]: string } = {
      nmap: '/api/tools/nmap',
      subdomain_enum: '/api/tools/subdomain',
      port_scan: '/api/tools/portscan',
      whois: '/api/tools/whois',
      dns_enum: '/api/tools/dns',
      vuln_scan: '/api/tools/vulnscan',
      exploit_search: '/api/tools/exploits',
      payload_gen: '/api/tools/payload',
      web_crawl: '/api/tools/webcrawl',
      phishing_detect: '/api/tools/phishing',
      password_audit: '/api/tools/password',
      report_gen: '/api/tools/report',
    };

    const endpoint = toolMap[tool];
    if (!endpoint) {
      return NextResponse.json(
        { success: false, error: 'Unknown tool' },
        { status: 400 }
      );
    }

    // Execute the tool via backend API
    const response = await fetch(`${BACKEND_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ target }),
    });

    const data = await response.json();
    
    return NextResponse.json({
      success: true,
      output: data.output || data.result || JSON.stringify(data, null, 2),
      tool: tool,
      target: target,
    });
  } catch (error) {
    console.error('Execution error:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: error instanceof Error ? error.message : 'Execution failed',
        output: 'Failed to execute tool. Check if the backend is running.'
      },
      { status: 500 }
    );
  }
}
