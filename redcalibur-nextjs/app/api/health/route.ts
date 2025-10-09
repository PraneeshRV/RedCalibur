import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

export async function GET() {
  try {
    const response = await fetch(`${BACKEND_URL}/health`, {
      cache: 'no-store',
    });
    const data = await response.json();
    return NextResponse.json({
      frontend: 'operational',
      backend: data,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json({
      frontend: 'operational',
      backend: 'unreachable',
      error: 'Backend server is not responding',
      timestamp: new Date().toISOString(),
    }, { status: 503 });
  }
}
