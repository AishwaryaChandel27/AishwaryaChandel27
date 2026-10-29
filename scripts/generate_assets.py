#!/usr/bin/env python3
"""Build the local visual identity. No dependencies, credentials or remote images."""
from pathlib import Path
from html import escape
import math
from generate_city import write_if_changed
ROOT=Path(__file__).resolve().parents[1]
C='#22D3EE'; P='#A855F7'; K='#F472B6'; T='#E5E7EB'; M='#ACB7CE'

def txt(x,y,s,size=20,color=T,extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {extra}>{escape(s)}</text>'

def frame(w,h,title,body,desc='',style=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc or title)}</desc><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#080B16"/><stop offset="1" stop-color="#10182B"/></linearGradient><linearGradient id="neon"><stop stop-color="{C}"/><stop offset=".6" stop-color="{P}"/><stop offset="1" stop-color="{K}"/></linearGradient><radialGradient id="glow"><stop stop-color="{P}" stop-opacity=".32"/><stop offset="1" stop-color="{P}" stop-opacity="0"/></radialGradient></defs><style>text{{font-family:DejaVu Sans,Arial,sans-serif}} {style} @media(prefers-reduced-motion:reduce){{*{{animation:none!important}} .role{{opacity:0}} .role.first{{opacity:1}} .typing{{clip-path:none!important}}}}</style><rect width="{w}" height="{h}" rx="24" fill="url(#bg)"/><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="24" fill="none" stroke="#2c3550"/>{body}</svg>\n'''

def save(name,svg):write_if_changed(ROOT/'assets'/name,svg)

def hero():
    b='<ellipse cx="1010" cy="200" rx="420" ry="300" fill="url(#glow)"/>'
    # A deliberately decorative skyline, separate from the data visualization.
    for i in range(20):
        x=680+i*27; h=42+(i*43)%138
        b+=f'<path d="M{x} 380v-{h}h20v{h}" fill="#111d32" stroke="#514275" stroke-width="1"/>'
        for y in range(390-h,370,14):
            b+=f'<path d="M{x+5} {y}h3m4 0h3" stroke="{C if i%2 else P}" opacity=".5"/>'
    b+='<path d="M750 90h90l30 30h170m-120 30h90l30-30h100M810 310h90l30 30h230" fill="none" stroke="#596087" opacity=".4"/>'
    for i in range(20):
        x=600+(i*137)%570;y=35+(i*73)%300
        b+=f'<circle class="star" cx="{x}" cy="{y}" r="{1+i%2}" fill="{C}" style="animation-delay:{i%5}s"/>'
    b+='<path d="M40 398h1120" stroke="url(#neon)" stroke-width="2"/>'
    b+=txt(48,52,'A / C    ENGINEERING AFTER DARK',14,C,'letter-spacing="3"')
    b+=txt(48,150,'Aishwarya',76,T,'font-weight="700" class="name"')
    b+=txt(48,201,'Full Stack & AI Developer',32)
    b+=txt(48,246,'Intelligent applications. Thoughtful interfaces.',22,M)
    b+=txt(48,277,'Built with purpose, one useful idea at a time.',22,M)
    b+='<rect x="48" y="321" width="359" height="40" rx="20" fill="#102d37" stroke="#1e6170"/>'
    b+='<circle cx="69" cy="341" r="4" fill="#22D3EE"/>'+txt(83,348,'INDIA  /  OPEN TO COLLABORATION',14,C)
    b+=txt(48,426,'PYTHON  /  REACT  /  AUTOMATION  /  DATA QUALITY',13,M,'letter-spacing="2"')
    save('hero.svg',frame(1200,450,'Aishwarya | Full Stack & AI Developer',b,'India. Python, React, automation and data quality. Open to collaboration.', '@keyframes shimmer{50%{fill:#baf6ff}} .name{animation:shimmer 7s ease-in-out infinite} @keyframes twinkle{50%{opacity:.15;transform:translateY(-4px)}} .star{animation:twinkle 8s ease-in-out infinite}'))

def typing():
    roles=['Python & AI Automation Developer','Full Stack Developer','RAG & Intelligent Systems Builder','Data Engineering & Quality Enthusiast','Building Technology with Purpose']
    b=txt(32,42,'>',25,C)
    for i,r in enumerate(roles):
        b+=f'<g class="role {"first" if i==0 else ""}" style="animation-delay:{i*5}s"><g class="typing">'+txt(66,42,r,23)+'</g></g>'
    style='@keyframes role{0%,19.99%{opacity:1}20%,100%{opacity:0}} .role{opacity:0;animation:role 25s steps(1,end) infinite} @keyframes type{0%{clip-path:inset(0 100% 0 0)}40%,95%{clip-path:inset(0 0 0 0)}100%{clip-path:inset(0 100% 0 0)}} .typing{animation:type 5s steps(40,end) infinite}'
    save('typing.svg',frame(760,70,'What I build',b,'; '.join(roles),style))

def terminal():
    b='<path d="M0 57h1200" stroke="#2c3550"/>'
    for i,c in enumerate([K,P,C]):b+=f'<circle cx="{34+i*23}" cy="29" r="5" fill="{c}"/>'
    b+=txt(132,36,'developer.os / aishwarya',16,M)
    b+=txt(35,103,'> initializing developer_profile...',21,C)
    fields=[('IDENTITY','Aishwarya · India'),('SPECIALIZATION','Python / AI / Full Stack'),('FOCUS','Useful, intelligent applications'),('MISSION','Build technology with purpose')]
    for i,(a,v) in enumerate(fields):
        y=148+i*37;b+=txt(35,y,a,15,M,'letter-spacing="1"')+txt(220,y,v,20)
    b+='<path d="M742 90v200" stroke="#2c3550"/>'
    for i,(a,v) in enumerate([('CURRENT MODE','BUILDING'),('CREATIVE MODE','ENABLED'),('LEARNING MODE','ACTIVE'),('COLLABORATION','OPEN')]):
        y=112+i*49;b+=txt(780,y,a,13,M,'letter-spacing="1.5"')+txt(780,y+24,v,20,C)
    b+=txt(35,326,'> system.status: OPEN_TO_COLLABORATION',18,C)
    save('developer-terminal.svg',frame(1200,355,'Developer operating system',b))

def art(kind,color):
    # Original conceptual artwork: no simulated product screenshots.
    b=f'<circle cx="470" cy="106" r="64" fill="{color}" opacity=".06"/><circle cx="470" cy="106" r="48" fill="none" stroke="{color}" opacity=".25"/>'
    if kind=='vihaara':
        for rotation in [-60,-30,0,30,60]:b+=f'<ellipse cx="470" cy="97" rx="15" ry="36" fill="{color}" fill-opacity=".1" stroke="{color}" transform="rotate({rotation} 470 128)"/>'
        b+='<path d="M421 141q49 24 98 0" fill="none" stroke="#22D3EE"/>'
    elif kind=='aura':
        for i in range(6):
            x=470+48*math.cos(i*math.pi/3);y=106+48*math.sin(i*math.pi/3)
            b+=f'<path d="M470 106L{x} {y}" stroke="{color}"/><circle cx="{x}" cy="{y}" r="6" fill="#10182B" stroke="{color}"/>'
        b+=f'<circle cx="470" cy="106" r="18" fill="#10182B" stroke="{color}"/>'
    elif kind=='rag':
        for i in range(3):b+=f'<rect x="{429+i*13}" y="{64+i*13}" width="55" height="65" rx="5" fill="#10182B" stroke="{color}"/>'
        b+=f'<path d="M468 110h23m-23 10h23m-23 10h14" stroke="{color}"/>'
    elif kind=='travel':
        b+=f'<ellipse cx="470" cy="106" rx="26" ry="48" fill="none" stroke="{color}"/><path d="M422 106h96m-88-22h80m-80 44h80" stroke="{color}"/><path d="M430 130q26-72 75-44" stroke="#F472B6" stroke-width="3" fill="none" stroke-dasharray="4 5"/>'
    else:
        b+=f'<rect x="423" y="70" width="94" height="70" rx="8" fill="#10182B" stroke="{color}"/><path d="M423 88h94m-65 21-10 8 10 8m36-16 10 8-10 8m-14-20-8 24" fill="none" stroke="{color}"/>'
    return b

def cards():
    projects=[('vihaara','01 / FLAGSHIP · PROTOTYPE','Vihaara','A calmer space to reflect.','REACT / TYPESCRIPT / WEBLLM',C),('aura','02 / RESEARCH · PROTOTYPE','AURA','From papers to research questions.','PYTHON / FLASK / SQLALCHEMY',P),('rag','03 / RETRIEVAL · PROTOTYPE','RAG Assistant','Make research easier to find.','PYTHON / FLASK / KEYWORD SEARCH',C),('travel','04 / DISCOVERY · PROTOTYPE','TasteTravel','Culture, shaped around curiosity.','REACT / TYPESCRIPT / EXPRESS',K),('portfolio','05 / FRONTEND · ACTIVE','Engineering Portfolio','A playful home for serious work.','JAVASCRIPT / HTML / CSS',P)]
    for key,eyebrow,name,line,stack,c in projects:
        b=art(key,c)+txt(26,35,eyebrow,12,c,'letter-spacing="1.5"')+txt(26,93,name,28,T,'font-weight="700"')+txt(26,133,line,17,M)+txt(26,204,stack,12,c,'letter-spacing=".5"')
        b+='<path d="M26 174h510" stroke="#2c3550"/>'+txt(26,237,'EXPLORE THE BUILD',12,M,'letter-spacing="2"')+txt(510,239,'↗',23,c)
        save(f'project-cards/{key}.svg',frame(560,260,name,b,'Concept artwork. '+line))

def journey():
    cells=[('PYTHON BACKEND','AdventX','REST APIs & debugging'),('FRONTEND','Capital Rush','15+ React / TypeScript pages'),('DATA QUALITY','Bitwise','ETL validation & reconciliation')]
    b=txt(32,34,'ENGINEERING JOURNEY / EXPERIENCE THREADS',13,C,'letter-spacing="2"')
    for i,(a,n,d) in enumerate(cells):
        x=32+i*395
        b+=f'<path d="M{x} 65h350" stroke="url(#neon)"/><circle cx="{x}" cy="65" r="4" fill="{C}"/>'
        b+=txt(x,98,a,12,M,'letter-spacing="1.5"')+txt(x,131,n,24)+txt(x,164,d,17,M)
    b+=txt(32,215,'2024  /  Third prize · National-level hackathon',20,C)
    save('journey.svg',frame(1200,247,'Experience and 2024 hackathon achievement',b,'Experience threads are not a dated employment timeline.'))

if __name__=='__main__':
    hero();typing();terminal();cards();journey()
    print('Generated 9 local brand assets')
