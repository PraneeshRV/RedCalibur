import React, { useEffect, useRef, useState } from 'react'

export default function Landing({ palette, setPalette, onEnter, generateMission }) {
  const [toggleState, setToggleState] = useState(0)
  const [isGenerating, setIsGenerating] = useState(false)
  const missionRef = useRef(null)

  // Inject Share Tech Mono font for landing
  useEffect(() => {
    const link1 = document.createElement('link')
    link1.rel = 'preconnect'; link1.href = 'https://fonts.googleapis.com'
    const link2 = document.createElement('link')
    link2.rel = 'preconnect'; link2.href = 'https://fonts.gstatic.com'; link2.crossOrigin = 'anonymous'
    const link3 = document.createElement('link')
    link3.href = 'https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap'; link3.rel = 'stylesheet'
    document.head.append(link1, link2, link3)
    return () => { link1.remove(); link2.remove(); link3.remove(); }
  }, [])

  // Typewriter effect
  const typeWriter = (el, text, speed = 30) => {
    if (!el) return
    let i = 0
    el.innerHTML = ''
    const cursor = document.createElement('span')
    cursor.style.borderRight = '3px solid var(--primary-color)'
    cursor.style.animation = 'blink-caret .75s step-end infinite'
    el.appendChild(cursor)
    const typing = () => {
      if (i < text.length) {
        cursor.insertAdjacentText('beforebegin', text.charAt(i))
        i++
        window.setTimeout(typing, speed)
      } else {
        cursor.style.animation = 'none'; cursor.style.borderRight = 'none'
      }
    }
    typing()
  }

  const themes = [
    { name: 'red', primary: '#E53E3E', glow: 'rgba(229, 62, 62, 0.75)' },
    { name: 'blue', primary: '#4299E1', glow: 'rgba(66, 153, 225, 0.75)' },
  ]

  const cycleTheme = () => {
    const next = (toggleState + 1) % themes.length
    setToggleState(next)
    const t = themes[next]
    document.documentElement.style.setProperty('--primary-color', t.primary)
    document.documentElement.style.setProperty('--glow-color', t.glow)
    setPalette(t.name)
  }

  const handleGenerate = async () => {
    if (isGenerating) return
    setIsGenerating(true)
    if (missionRef.current) missionRef.current.innerHTML = '<div class="loader"></div>'
    try {
      const mission = await generateMission()
      typeWriter(missionRef.current, (mission || 'Transmission failed.').trim())
    } catch (e) {
      if (missionRef.current) missionRef.current.textContent = 'Error: Could not connect to Archangel network. Please try again.'
    } finally { setIsGenerating(false) }
  }

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center p-4 hacker-bg">
      <style>{`
        :root { --primary-color:#E53E3E; --glow-color: rgba(229,62,62,0.75); }
        .hacker-bg{ background:#0a0a0a; position:relative; overflow:hidden; font-family:'Share Tech Mono',monospace; color:var(--primary-color); text-shadow:0 0 5px var(--glow-color),0 0 10px var(--glow-color); }
        .hacker-bg::before{ content:''; position:absolute; inset:0; background-image:linear-gradient(0deg, rgba(0,0,0,0) 50%, rgba(255,255,255,0.05) 50%); background-size:100% 4px; animation:scanlines 5s linear infinite; opacity:.2; pointer-events:none }
        @keyframes scanlines { 0%{background-position:0 0} 100%{background-position:0 100px} }
        .smooth-transition{ transition: opacity .8s ease, transform .8s ease }
        .glowing-btn{ border:2px solid var(--primary-color); box-shadow: 0 0 10px var(--glow-color), 0 0 20px var(--glow-color) inset; color:var(--primary-color) }
        .glowing-btn:hover{ background:var(--primary-color); color:#0a0a0a; box-shadow: 0 0 20px var(--glow-color), 0 0 30px var(--glow-color) inset }
        .loader{ width:24px; height:24px; border:3px solid var(--primary-color); border-bottom-color:transparent; border-radius:50%; display:inline-block; animation:rotation 1s linear infinite }
        @keyframes rotation { 0%{transform:rotate(0)} 100%{transform:rotate(360deg)} }
        @keyframes blink-caret { from,to{border-color:transparent} 50%{border-color:var(--primary-color)} }
      `}</style>

      {/* Theme toggle in top-right */}
      <div className="fixed top-4 right-4 flex items-center z-50" style={{textShadow:'none'}}>
        <span className="mr-4 uppercase tracking-widest text-sm text-gray-300">Theme:</span>
        <button onClick={cycleTheme} className="rounded-full w-[120px] h-[40px] flex items-center justify-center bg-gradient-to-r from-rose-600 via-purple-500 to-blue-500 shadow-inner">
          <span className="text-white text-xs">Cycle</span>
        </button>
      </div>

      {/* Card */}
      <div className="text-center smooth-transition w-full max-w-3xl">
        <h1 className="text-3xl md:text-5xl font-bold mb-4">Welcome to Red Calibur</h1>
        <button onClick={onEnter} className="underline decoration-dotted hover:decoration-solid text-lg">Click here to open the website</button>

        <div className="opacity-100 translate-y-0 w-full max-w-3xl mx-auto mt-8">
          <div className="w-full mx-auto p-6 border-2 rounded-lg mb-8 flex items-center justify-center" style={{borderColor:'var(--primary-color)', boxShadow:'0 0 10px var(--glow-color)'}}>
            <p ref={missionRef} className="text-lg text-left">Awaiting transmission...</p>
          </div>
          <button onClick={handleGenerate} disabled={isGenerating} className="glowing-btn font-bold py-3 px-8 rounded-lg text-xl uppercase tracking-widest">
            {isGenerating ? 'Contacting…' : '✨ Generate Mission'}
          </button>
        </div>
      </div>
    </div>
  )
}
