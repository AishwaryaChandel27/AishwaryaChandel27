#!/usr/bin/env python3
"""Public repository snapshot and precisely defined calendar metrics."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from generate_city import USER, ROOT, request, validate_days, metrics, write_if_changed
from generate_assets import frame, txt


def collect():
    repos=[]
    for page in range(1,101):
        # Public endpoint only: no private repository names enter the artifact.
        batch=json.loads(request(f'https://api.github.com/users/{USER}/repos?type=owner&per_page=100&page={page}',os.getenv('GH_TOKEN')))
        if not isinstance(batch,list):raise ValueError('Expected repository list')
        repos.extend({'name':r['name'],'url':r['html_url'],'language':r['language'],'stars':r['stargazers_count']} for r in batch if not r['fork'] and not r['private'] and r['owner']['login'].lower()==USER.lower())
        if len(batch)<100:break
    else:raise ValueError('Pagination limit exceeded')
    if not repos:raise ValueError('Empty repository snapshot')
    return {'as_of':datetime.now(timezone.utc).date().isoformat(),'scope':'Owned public non-fork repositories; primary language per repository','repositories':sorted(repos,key=lambda r:r['name'].lower())}


def render(snapshot,calendar):
    days=validate_days(calendar['days']); m=metrics(days); repos=snapshot['repositories']
    lang=Counter(r['language'] or 'Unclassified' for r in repos)
    b=txt(34,38,'04 / ENGINEERING SIGNALS',13,'#22D3EE','letter-spacing="2"')+txt(34,67,f'Repositories as of {snapshot["as_of"]} · Calendar through {days[-1]["date"]}',15,'#ACB7CE')
    for x,n,label in [(34,len(repos),'PUBLIC ORIGINAL REPOS'),(335,sum(r['stars'] for r in repos),'STARS ACROSS THESE REPOS'),(650,m['longest'],'LONGEST OBSERVED STREAK'),(957,m['peak'],'BUSIEST DAY')]:
        b+=txt(x,129,str(n),42,'#E5E7EB')+txt(x,154,label,11,'#22D3EE','letter-spacing=".5"')
    b+=txt(34,203,'PRIMARY LANGUAGE / REPOSITORY COUNT',12,'#ACB7CE','letter-spacing="1.5"')
    colors=['#22D3EE','#A855F7','#F472B6','#7DD3FC','#C4B5FD','#94A3B8']
    top=sorted(lang.items(),key=lambda r:(-r[1],r[0]))[:5]
    other=sum(lang.values())-sum(n for _,n in top)
    if other:top.append(('Other',other))
    x=34
    for (name,n),c in zip(top,colors):
        width=n/len(repos)*1132
        b+=f'<rect x="{x:.2f}" y="222" width="{width:.2f}" height="14" fill="{c}"/>';x+=width
    for i,((name,n),c) in enumerate(zip(top,colors)):
        x=34+(i%3)*395;y=270+(i//3)*32
        b+=f'<circle cx="{x+4}" cy="{y-5}" r="4" fill="{c}"/>'+txt(x+17,y,f'{name} · {n}',16)
    b+=txt(34,342,'Streak = consecutive active dates within the displayed calendar, not a lifetime record.',13,'#ACB7CE')
    b+=txt(34,367,'Languages describe repositories, not proficiency. Forks and private repositories are excluded.',13,'#ACB7CE')
    return frame(1200,395,'Engineering activity and public repository languages',b)


def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path);a=p.parse_args()
    try:
        snap=json.loads(a.input.read_text()) if a.input else collect()
        calendar=json.loads((ROOT/'data/contributions.json').read_text())
        svg=render(snap,calendar)
        write_if_changed(ROOT/'data/repositories.json',json.dumps(snap,indent=2)+'\n')
        write_if_changed(ROOT/'assets/activity-dashboard.svg',svg)
        print(f'Validated {len(snap["repositories"])} public non-fork repositories')
    except Exception as exc:
        print(f'::error::Statistics refresh failed ({type(exc).__name__}); previous assets preserved.',file=sys.stderr);return 1
    return 0

if __name__=='__main__':sys.exit(main())
