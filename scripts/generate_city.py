#!/usr/bin/env python3
"""Actual GitHub contribution calendar -> deterministic isometric SVG (stdlib)."""
from __future__ import annotations
import argparse
from datetime import date, timedelta
from html import escape
from html.parser import HTMLParser
import json
import math
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
USER = 'AishwaryaChandel27'
QUERY = '''query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}'''


def request(url, token=None, body=None):
    headers = {'User-Agent': 'contribution-metropolis', 'Accept': 'application/vnd.github+json'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    if body is not None:
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode('utf-8')


def validate_days(days, minimum=300):
    if not isinstance(days, list) or not minimum <= len(days) <= 371:
        raise ValueError('Expected a complete contribution calendar')
    result = []
    for day in days:
        d, c = date.fromisoformat(day['date']), day['count']
        if type(c) is not int or c < 0:
            raise ValueError('Contribution counts must be nonnegative integers')
        result.append({'date': d.isoformat(), 'count': c})
    result.sort(key=lambda d: d['date'])
    for a, b in zip(result, result[1:]):
        if date.fromisoformat(b['date']) - date.fromisoformat(a['date']) != timedelta(days=1):
            raise ValueError('Calendar contains missing or duplicate dates')
    return result


def graphql_days(payload):
    if payload.get('errors'):
        raise ValueError('GitHub GraphQL rejected the calendar request')
    weeks = payload['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    return validate_days([{'date': d['date'], 'count': d['contributionCount']} for w in weeks for d in w['contributionDays']])


class CalendarParser(HTMLParser):
    """Bootstrap/fallback: exact counts from GitHub's public calendar tooltips.

    Never infer counts from intensity colors. Unknown markup fails closed.
    """
    def __init__(self):
        super().__init__()
        self.dates, self.counts = {}, {}
        self.target, self.parts = None, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('data-date') and a.get('id'):
            self.dates[a['id']] = a['data-date']
        if tag == 'tool-tip':
            self.target, self.parts = a.get('for'), []

    def handle_data(self, data):
        if self.target:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == 'tool-tip' and self.target:
            match = re.match(r'^(No|[\d,]+) contributions? on ', ''.join(self.parts).strip())
            if match:
                self.counts[self.target] = 0 if match[1] == 'No' else int(match[1].replace(',', ''))
            self.target = None

    def days(self):
        if not self.dates or set(self.dates) - set(self.counts):
            raise ValueError('Unrecognized public calendar markup; counts not inferred')
        return validate_days([{'date': d, 'count': self.counts[k]} for k, d in self.dates.items()])


def collect(username, token=None):
    if not re.fullmatch(r'[A-Za-z0-9-]{1,39}', username):
        raise ValueError('Invalid GitHub username')
    if token:
        try:
            days = graphql_days(json.loads(request('https://api.github.com/graphql', token, {'query': QUERY, 'variables': {'login': username}})))
            return {'username': username, 'source': 'GitHub GraphQL contributionCalendar', 'days': days}
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError, TypeError):
            print('::warning::GraphQL unavailable; trying the public GitHub calendar. No credentials logged.', file=sys.stderr)
    parser = CalendarParser()
    parser.feed(request(f'https://github.com/users/{username}/contributions'))
    return {'username': username, 'source': 'GitHub public contribution calendar', 'days': parser.days()}


def metrics(days):
    best = run = 0
    for day in days:
        run = run + 1 if day['count'] else 0
        best = max(best, run)
    # Completed calendar dates only; an unfinished final day may still be zero.
    return {'total': sum(d['count'] for d in days), 'active': sum(d['count'] > 0 for d in days), 'longest': best, 'peak': max(d['count'] for d in days)}


def text(x, y, value, size=16, color='#E5E7EB', extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {extra}>{escape(str(value))}</text>'


def polygon(points, fill, stroke='#29415d'):
    return '<polygon points="' + ' '.join(f'{x:.2f},{y:.2f}' for x, y in points) + f'" fill="{fill}" stroke="{stroke}" stroke-width=".6"/>'


def render(snapshot):
    days = validate_days(snapshot['days'])
    m = metrics(days)
    first = date.fromisoformat(days[0]['date'])
    start = first - timedelta(days=(first.weekday() + 1) % 7)
    max_h = math.log2(m['peak'] + 1) or 1
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 680" role="img" aria-labelledby="title desc">',
         '<title id="title">Aishwarya’s Contribution Metropolis</title>',
         f'<desc id="desc">{m["total"]} contributions across {len(days)} calendar days. One block per day; zero activity is an empty platform. Height is proportional to log2(count plus one), normalized to this calendar. {escape(snapshot["source"])}.</desc>',
         '<defs><radialGradient id="halo"><stop stop-color="#63359c" stop-opacity=".4"/><stop offset="1" stop-color="#080B16" stop-opacity="0"/></radialGradient><linearGradient id="floor" x2="1" y2="1"><stop stop-color="#12263d"/><stop offset="1" stop-color="#15102b"/></linearGradient></defs>',
         '<rect width="1200" height="680" rx="24" fill="#080B16"/>',
         '<ellipse cx="650" cy="360" rx="540" ry="270" fill="url(#halo)"/>',
         '<g font-family="DejaVu Sans,Arial,sans-serif">',
         text(40, 42, '03 / CONTRIBUTION METROPOLIS', 13, '#22D3EE', 'letter-spacing="3"'),
         text(40, 83, 'Small steps. A growing skyline.', 30),
         text(40, 112, f'{days[0]["date"]} — {days[-1]["date"]}  /  GitHub-visible calendar activity', 14, '#ACB7CE')]
    for x, value, label in [(770,m['total'],'CONTRIBUTIONS'), (970,m['active'],'ACTIVE DAYS')]:
        s += [text(x, 75, value, 38, '#22D3EE'),text(x, 100, label, 11, '#ACB7CE', 'letter-spacing="1.5"')]
    def project(w, d): return (170 + (w-d)*17, 205 + (w+d)*5.6)
    weeks = ((date.fromisoformat(days[-1]['date'])-start).days // 7) + 1
    s.append(polygon([project(-1,-1),project(weeks,-1),project(weeks,7),project(-1,7)],'url(#floor)','#3a355f'))
    blocks = []
    for day in days:
        dt = date.fromisoformat(day['date']); offset=(dt-start).days
        w,d = divmod(offset,7); x,y=project(w,d); c=day['count']
        blocks.append((w+d,w,d,x,y,c,dt))
    for _,w,d,x,y,c,dt in sorted(blocks):
        a,b = 7.1,2.35
        base=[(x,y),(x+a,y+b),(x,y+2*b),(x-a,y+b)]
        s.append(f'<g data-date="{dt}" data-count="{c}"><title>{dt}: {c} contributions</title>')
        s.append(polygon(base,'#10182B','#2b3851'))
        if c:
            h=7 + 126*math.log2(c+1)/max_h
            col='#22D3EE' if c<3 else '#A855F7' if c<10 else '#F472B6'
            s.append(polygon([(x-a,y+b-h),(x,y+2*b-h),(x,y+2*b),(x-a,y+b)],'#16364c'))
            s.append(polygon([(x,y+2*b-h),(x+a,y+b-h),(x+a,y+b),(x,y+2*b)],'#3c235e'))
            for z in range(6,int(h)-3,7):
                s.append(f'<path d="M{x-5:.2f} {y+b-z:.2f}l3 1 M{x+2:.2f} {y+2*b-z:.2f}l3 -1" stroke="{col}" stroke-width="1" opacity=".7"/>')
            s.append(polygon([(px,py-h) for px,py in base],col,'#d4f6ff'))
            if c==m['peak']:
                s.append(f'<path d="M{x} {y-h}v-10" stroke="#F472B6"/><circle cx="{x}" cy="{y-h-10}" r="2" fill="#fff"/>')
        s.append('</g>')
    last_month=None
    for day in days:
        dt=date.fromisoformat(day['date'])
        if dt.month!=last_month:
            w=(dt-start).days//7; x,y=project(w,8.5)
            s.append(text(x,y+25,dt.strftime('%b'),11,'#ACB7CE'))
            last_month=dt.month
    s += [text(40,595,'ONE DAY / ONE BLOCK',12,'#22D3EE','letter-spacing="2"'),
          text(40,621,'Height = log-scaled count · Roof = activity band · Tallest = busiest day',14,'#ACB7CE'),
          text(40,648,'Calendar activity is not a measure of code quality. Private counts depend on GitHub visibility.',12,'#ACB7CE')]
    for x,c,label in [(800,'#10182B','0'),(875,'#22D3EE','1–2'),(960,'#A855F7','3–9'),(1055,'#F472B6','10+')]:
        s += [f'<rect x="{x}" y="592" width="14" height="14" rx="3" fill="{c}" stroke="#ACB7CE"/>',text(x+23,604,label,13)]
    return ''.join(s)+'</g></svg>\n'


def write_if_changed(path, content):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and path.read_text(encoding='utf-8') == content:
        return False
    temp=path.with_suffix(path.suffix+'.tmp')
    temp.write_text(content,encoding='utf-8'); temp.replace(path)
    return True


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,help='Render a saved genuine calendar; no network')
    parser.add_argument('--username',default=USER)
    args=parser.parse_args()
    try:
        snapshot=json.loads(args.input.read_text()) if args.input else collect(args.username,os.getenv('GH_TOKEN'))
        svg=render(snapshot) # validate before replacing the last successful files
        write_if_changed(ROOT/'data/contributions.json',json.dumps(snapshot,indent=2)+'\n')
        write_if_changed(ROOT/'assets/contribution-city.svg',svg)
        print(f'Validated {len(snapshot["days"])} days; {metrics(snapshot["days"])["total"]} contributions')
    except (urllib.error.URLError,TimeoutError,ValueError,KeyError,TypeError,OSError) as error:
        print(f'::error::Calendar refresh failed ({type(error).__name__}); previous assets preserved. Retry later.',file=sys.stderr)
        return 1
    return 0

if __name__=='__main__':
    sys.exit(main())
