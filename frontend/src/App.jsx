import React, { useEffect, useMemo, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import VisualFX from './components/FX'
import Landing from './components/Landing'

const API_BASE = import.meta.env.VITE_API_BASE || '/api'

const Section = ({ title, children }) => (
  <div className="card">
    <div className="flex items-center justify-between mb-4">
      <h2 className="text-xl font-semibold accent-text">{title}</h2>
    </div>
    {children}
  </div>
)

const Header = ({ palette, setPalette, fx, setFx, apiStatus }) => {
  const [openFx, setOpenFx] = useState(false)
  return (
    <header className="sticky top-0 z-20 backdrop-blur bg-black/60 border-b border-zinc-800">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center gap-3">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L4 6v5c0 5.55 3.84 10.74 8 12 4.16-1.26 8-6.45 8-12V6l-8-4z" fill="rgba(var(--primary-rgb),1)"/>
          <path d="M12 6v12M9 10h6" stroke="#fff" strokeWidth="1.5" strokeLinecap="round"/>
        </svg>
        <div className="flex-1 min-w-0">
          <div className="text-2xl font-bold tracking-tight">RedCalibur</div>
          <div className="text-sm text-zinc-400 -mt-1">Red Teaming AI — Recon, Scan, Report</div>
        </div>
        <div className="relative flex items-center gap-3">
          <div className="text-xs px-2 py-1 rounded border border-zinc-700/60 bg-black/40">
            API: <span className={apiStatus==='ok' ? 'text-green-400' : 'text-red-400'}>{apiStatus}</span>
          </div>
          <select aria-label="Theme" className="input w-auto" value={palette} onChange={e=>setPalette(e.target.value)}>
            <option value="red">Red</option>
            <option value="blue">Blue</option>
          </select>
          <div className="relative">
            <button className="btn" onClick={()=>setOpenFx(v=>!v)} aria-expanded={openFx} aria-haspopup="menu" title="Toggle Effects">FX</button>
            {openFx && (
              <div className="absolute right-0 mt-2 w-72 card z-30">
                <div className="text-sm text-zinc-400 mb-2">Effects</div>
                <div className="grid grid-cols-2 gap-2 mb-3">
                  {Object.keys(fx).map(key => (
                    <label key={key} className="flex items-center gap-2 text-sm">
                      <input type="checkbox" checked={fx[key]} onChange={()=>setFx(prev=>({ ...prev, [key]: !prev[key] }))} />
                      <span className="capitalize">{key.replace(/([A-Z])/g,' $1').trim()}</span>
                    </label>
                  ))}
                </div>
                <div className="flex justify-end">
                  <button className="btn" onClick={()=>{ setPalette('red'); setFx({ matrix:true,constellation:true,ripple:true,mouseTrail:true,noise:true,scanlines:true,sweep:true,vignette:true,parallax:true }) }}>Reset Defaults</button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}

export default function App() {
  const [showLanding, setShowLanding] = useState(true)
  // Independent loading flags per section so only the triggered action shows a spinner
  const [domainLoading, setDomainLoading] = useState(false)
  const [scanLoading, setScanLoading] = useState(false)
  const [usernameLoading, setUsernameLoading] = useState(false)
  const [urlLoading, setUrlLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [logs, setLogs] = useState([])
  const [apiStatus, setApiStatus] = useState('unknown')

  const defaultFx = { matrix:true,constellation:true,ripple:true,mouseTrail:true,noise:true,scanlines:true,sweep:true,vignette:true,parallax:true }
  const [palette, setPalette] = useState(() => (typeof window==='undefined' ? 'red' : (localStorage.getItem('rc_palette')||'red')))
  const [fx, setFx] = useState(() => {
    if (typeof window==='undefined') return defaultFx
    try {
      const saved = JSON.parse(localStorage.getItem('rc_fx')||'null')
      return saved && typeof saved==='object' ? { ...defaultFx, ...saved } : defaultFx
    } catch { return defaultFx }
  })
  const [showSummary, setShowSummary] = useState(false)
  const [summaryText, setSummaryText] = useState('')
  const [summaryLoading, setSummaryLoading] = useState(false)

  useEffect(() => {
    const root = document.documentElement
    if (palette==='blue') {
      root.style.setProperty('--primary-rgb','59,130,246')
      root.style.setProperty('--secondary-rgb','244,63,94')
      root.style.setProperty('--primary-color','#4299E1')
      root.style.setProperty('--glow-color','rgba(66,153,225,0.75)')
    } else {
      root.style.setProperty('--primary-rgb','244,63,94')
      root.style.setProperty('--secondary-rgb','59,130,246')
      root.style.setProperty('--primary-color','#E53E3E')
      root.style.setProperty('--glow-color','rgba(229,62,62,0.75)')
    }
    try { localStorage.setItem('rc_palette', palette) } catch {}
  }, [palette])

  useEffect(() => { try { localStorage.setItem('rc_fx', JSON.stringify(fx)) } catch {} }, [fx])

  const api = useMemo(()=>({
    post: async (path, body, {updateResult=true}={}) => {
      const start = performance.now()
      try {
        const res = await fetch(`${API_BASE}${path}`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body) })
        const json = await res.json(); if (!res.ok) throw new Error(json?.detail||'Request failed')
        if (updateResult) setResult(json)
        setLogs(l=>[{ time:new Date().toLocaleTimeString(), path, ok:true, ms:Math.round(performance.now()-start) }, ...l])
        return json
      } catch(e) {
        setLogs(l=>[{ time:new Date().toLocaleTimeString(), path, ok:false, error:e.message }, ...l])
        throw e
      }
    }
  }), [])

  useEffect(()=>{
    let mounted=true
    const ping=async()=>{ try{ const res=await fetch(`${API_BASE}/health`); if(!mounted) return; setApiStatus(res.ok?'ok':'down') } catch { if(!mounted) return; setApiStatus('down') } }
    ping(); const id=setInterval(ping,10000); return ()=>{mounted=false; clearInterval(id)}
  },[])

  // Simple Gemini mission generator placeholder via backend summarize
  const generateMission = async () => {
    // Reuse summarize endpoint with a themed prompt to avoid exposing keys in frontend
    const payload = { payload: { brief: 'Generate a short cryptic hacker mission briefing (<40 words). Code name: Archangel. Target: corporate project. Style: tense, high-stakes.' } }
    try {
      const res = await fetch(`${API_BASE}/summarize`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) })
      const json = await res.json(); return json?.summary || 'No mission received.'
    } catch { return 'Error contacting mission service.' }
  }

  return (
    <div>
      {showLanding && (
        <Landing
          palette={palette}
          setPalette={setPalette}
          onEnter={()=>setShowLanding(false)}
          generateMission={generateMission}
        />
      )}
      <VisualFX palette={palette} flags={fx} />
      <Header palette={palette} setPalette={setPalette} fx={fx} setFx={setFx} apiStatus={apiStatus} />
      <main className="relative z-10 max-w-7xl mx-auto px-4 py-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="space-y-6">
          <Section title="Domain Reconnaissance">
            <DomainForm
              onSubmit={async (data)=>{ setDomainLoading(true); try { await api.post('/domain', data) } finally { setDomainLoading(false) } }}
              loading={domainLoading}
            />
          </Section>
          <Section title="Network Scan">
            <ScanForm
              onSubmit={async (data)=>{ setScanLoading(true); try { await api.post('/scan', data) } finally { setScanLoading(false) } }}
              loading={scanLoading}
            />
          </Section>
          <Section title="Username Lookup">
            <UsernameForm
              onSubmit={async (data)=>{ setUsernameLoading(true); try { await api.post('/username', data) } finally { setUsernameLoading(false) } }}
              loading={usernameLoading}
            />
          </Section>
          <Section title="URL Malware Scan (VirusTotal)">
            <URLScanForm
              onSubmit={async (data)=>{ setUrlLoading(true); try { await api.post('/urlscan', data) } finally { setUrlLoading(false) } }}
              loading={urlLoading}
            />
          </Section>
        </div>
        <div className="space-y-6">
          <Section title="Results">
            {result ? <ResultViewer data={result} /> : <Placeholder />}
            {result && (
              <div className="mt-4">
                <button className="btn" onClick={async()=>{ setShowSummary(true); setSummaryLoading(true); setSummaryText(''); try{ const r=await api.post('/summarize',{payload:result},{updateResult:false}); setSummaryText(r?.summary||'No summary returned') } catch(e){ setSummaryText(`Error: ${e?.message||'Failed to summarize'}`) } finally { setSummaryLoading(false) } }}>AI Summarize</button>
              </div>
            )}
          </Section>
          <Section title="Activity Log"><Logs logs={logs} /></Section>
        </div>
      </main>
      {showSummary && (
        <div className="fixed inset-0 z-30 flex items-center justify-center">
          <div className="absolute inset-0 bg-black/60" onClick={()=>setShowSummary(false)} />
          <div className="relative z-10 w-full max-w-2xl mx-auto card">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold accent-text">AI Summary</h3>
              <div className="flex items-center gap-2">
                <button className="btn" onClick={()=>{ if(!summaryText) return; navigator.clipboard?.writeText(summaryText) }}>Copy</button>
                <button className="btn" onClick={()=>setShowSummary(false)}>Close</button>
              </div>
            </div>
            <div className="bg-black/40 border border-zinc-800 rounded-lg p-4 max-h-[60vh] overflow-auto text-sm">
              {summaryLoading ? 'Summarizing…' : (summaryText ? (
                <ReactMarkdown remarkPlugins={[remarkGfm]} components={{
                  h1:({node,...props})=> <h1 className="text-xl font-bold mb-2" {...props} />,
                  h2:({node,...props})=> <h2 className="text-lg font-semibold mt-3 mb-1" {...props} />,
                  h3:({node,...props})=> <h3 className="text-base font-semibold mt-3 mb-1" {...props} />,
                  p: ({node,...props})=> <p className="mb-2 leading-relaxed" {...props} />,
                  ul:({node,...props})=> <ul className="list-disc pl-5 mb-2 space-y-1" {...props} />,
                  ol:({node,...props})=> <ol className="list-decimal pl-5 mb-2 space-y-1" {...props} />,
                  code:({inline,...props})=> inline? <code className="px-1 py-0.5 rounded bg-zinc-800/70" {...props} /> : <code className="block p-2 rounded bg-zinc-900/70 overflow-auto" {...props} />,
                  blockquote:({node,...props})=> <blockquote className="border-l-2 border-zinc-700 pl-3 text-zinc-300 italic" {...props} />,
                  a:({node,...props})=> <a className="text-blue-400 underline" target="_blank" rel="noreferrer" {...props} />
                }}>{summaryText}</ReactMarkdown>
              ) : 'No content')}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function Field({ label, children }) {
  return (
    <div className="mb-4">
      <div className="text-xs uppercase tracking-wide text-zinc-400 mb-1">{label}</div>
      {children}
    </div>
  )
}

function DomainForm({ onSubmit, loading }) {
  const [domain, setDomain] = useState('example.com')
  return (
    <form onSubmit={async (e)=>{e.preventDefault(); await onSubmit({ target: domain, all: true })}}>
      <Field label="Domain">
        <input className="input" value={domain} onChange={e=>setDomain(e.target.value)} />
      </Field>
      <button className="btn" disabled={loading}>{loading ? 'Running…' : 'Run Recon'}</button>
    </form>
  )
}

function ScanForm({ onSubmit, loading }) {
  const [target, setTarget] = useState('1.1.1.1')
  const [ports, setPorts] = useState('80,443,22')
  const [shodan, setShodan] = useState(false)

  return (
    <form onSubmit={async (e)=>{e.preventDefault(); const p = ports.split(',').map(x=>parseInt(x.trim())).filter(Boolean); await onSubmit({ target, ports:p, shodan })}}>
      <Field label="Target IP or Hostname">
        <input className="input" value={target} onChange={e=>setTarget(e.target.value)} />
      </Field>
      <Field label="Ports (comma-separated)">
        <input className="input" value={ports} onChange={e=>setPorts(e.target.value)} />
      </Field>
      <label className="flex items-center gap-2 text-sm mb-4">
        <input type="checkbox" checked={shodan} onChange={()=>setShodan(v=>!v)} /> Use Shodan
      </label>
      <button className="btn" disabled={loading}>{loading ? 'Scanning…' : 'Run Scan'}</button>
    </form>
  )
}

function UsernameForm({ onSubmit, loading }) {
  const [target, setTarget] = useState('johndoe')
  const [platforms, setPlatforms] = useState('twitter,linkedin,github')
  return (
    <form onSubmit={async (e)=>{e.preventDefault(); await onSubmit({ target, platforms: platforms.split(',').map(x=>x.trim()).filter(Boolean) })}}>
      <Field label="Username">
        <input className="input" value={target} onChange={e=>setTarget(e.target.value)} />
      </Field>
      <Field label="Platforms (comma-separated)">
        <input className="input" value={platforms} onChange={e=>setPlatforms(e.target.value)} />
      </Field>
      <button className="btn" disabled={loading}>{loading ? 'Searching…' : 'Lookup'}</button>
    </form>
  )
}

function URLScanForm({ onSubmit, loading }) {
  const [url, setUrl] = useState('http://example.com')
  return (
    <form onSubmit={async (e)=>{e.preventDefault(); await onSubmit({ url })}}>
      <Field label="URL">
        <input className="input" value={url} onChange={e=>setUrl(e.target.value)} />
      </Field>
      <button className="btn" disabled={loading}>{loading ? 'Submitting…' : 'Scan URL'}</button>
    </form>
  )
}

function ResultViewer({ data }) {
  return (
    <div className="bg-black/40 border border-zinc-800 rounded-lg">
      <pre className="text-sm p-4 overflow-auto max-h-[480px]">{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}

function Logs({ logs }) {
  if (!logs.length) return <div className="text-zinc-400">No activity yet.</div>
  return (
    <ul className="space-y-2 text-sm">
      {logs.map((l, i) => (
        <li key={i} className="flex items-center justify-between bg-zinc-900/50 border border-zinc-800 rounded-md px-3 py-2">
          <span className={l.ok ? 'text-green-400' : ''} style={!l.ok ? { color: 'rgba(var(--primary-rgb), 0.9)' } : undefined}>
            {l.ok ? 'OK' : 'ERR'} <span className="text-zinc-400">{l.path}</span>
          </span>
          <span className="text-zinc-500">{l.ms ? `${l.ms}ms` : ''} — {l.time}</span>
        </li>
      ))}
    </ul>
  )
}

function Placeholder() {
  return (
    <div className="text-zinc-400">
      Trigger any action from the left. Results will appear here.
    </div>
  )
}

