import React, { useMemo, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Landing from '../components/Landing'

const API_BASE = import.meta.env.VITE_API_BASE || '/api'

export default function LandingPage(){
  const navigate = useNavigate()
  const [palette, setPalette] = useState(() => (typeof window==='undefined' ? 'red' : (localStorage.getItem('rc_palette')||'red')))

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

  const generateMission = useMemo(()=> async () => {
    const payload = { payload: { brief: 'Generate a short cryptic hacker mission briefing (<40 words). Code name: Archangel. Target: corporate project. Style: tense, high-stakes.' } }
    try {
      const res = await fetch(`${API_BASE}/summarize`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) })
      const json = await res.json(); return json?.summary || 'No mission received.'
    } catch { return 'Error contacting mission service.' }
  }, [])

  return (
    <Landing
      palette={palette}
      setPalette={setPalette}
      generateMission={generateMission}
      onEnter={()=> navigate('/app')}
    />
  )
}
