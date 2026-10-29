#!/usr/bin/env python3
"""Render actual GitHub contributions as an isometric SVG city. Stdlib only."""
import json, math, os, pathlib, urllib.request, datetime, html
USER = os.environ.get("GITHUB_USERNAME", "AishwaryaChandel27")
TOKEN = os.environ["GH_TOKEN"]
query = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"""
req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query":query,"variables":{"login":USER}}).encode(),headers={"Authorization":"Bearer "+TOKEN,"Content-Type":"application/json","User-Agent":"github-contribution-city"})
with urllib.request.urlopen(req, timeout=30) as response:
    payload = json.load(response)
if payload.get("errors"): raise RuntimeError(str(payload["errors"]))
weeks = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
days = [(i,j,d) for i,w in enumerate(weeks) for j,d in enumerate(w["contributionDays"])]
# Isometric projection. Blocks are drawn back to front to preserve layering.
W,H=1420,650
xscale,yscale=14,8
polys=[]
for i,j,d in days:
    count=int(d["contributionCount"])
    if count <= 0: continue
    height=6+min(82,round(13*math.log2(count+1)))
    x=270+(i-j)*xscale
    y=175+(i+j)*yscale
    a,b=xscale*.78,yscale*.78
    top=f"{x},{y-height} {x+a},{y+b-height} {x},{y+2*b-height} {x-a},{y+b-height}"
    left=f"{x-a},{y+b-height} {x},{y+2*b-height} {x},{y+2*b} {x-a},{y+b}"
    right=f"{x},{y+2*b-height} {x+a},{y+b-height} {x+a},{y+b} {x},{y+2*b}"
    color="#22d3ee" if count < 3 else "#a855f7" if count < 7 else "#f472b6"
    polys.extend([f'<polygon points="{left}" fill="#12374c" stroke="#30445f" stroke-width=".5"/>',
                  f'<polygon points="{right}" fill="#312451" stroke="#51406c" stroke-width=".5"/>',
                  f'<polygon points="{top}" fill="{color}" stroke="#b8faff" stroke-width=".5"/>'])
svg=f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Isometric city of actual GitHub contribution counts for {html.escape(USER)}">
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#080b16"/><stop offset="1" stop-color="#18102f"/></linearGradient></defs>
<rect width="{W}" height="{H}" rx="20" fill="url(#bg)"/>
<text x="45" y="57" fill="#22d3ee" font-size="28" font-family="monospace">CONTRIBUTION CITY / {html.escape(USER)}</text>
<text x="45" y="88" fill="#a7a7bc" font-size="17" font-family="monospace">Each tower represents real contribution activity · generated {datetime.date.today().isoformat()}</text>
<g>{''.join(polys)}</g><text x="45" y="616" fill="#e5e7eb" font-size="18" font-family="monospace">Building height = log-scaled daily contribution count</text>
</svg>"""
target=pathlib.Path("assets/contribution-city.svg")
target.parent.mkdir(parents=True,exist_ok=True)
target.write_text(svg,encoding="utf-8")
print(f"Generated {target} with {len(days)} days")
