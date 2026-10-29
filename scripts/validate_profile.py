#!/usr/bin/env python3
"""Offline validation of published SVGs, snapshots and README asset references."""
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from generate_city import ROOT,validate_days

class Images(HTMLParser):
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='img':
            assert a.get('alt'), 'Image needs meaningful alt text'
            assert a.get('src','').startswith('./assets/'), 'README images must be local'
            assert (ROOT/a['src']).is_file(), f'Missing {a["src"]}'

for path in (ROOT/'assets').rglob('*.svg'):
    root=ET.parse(path).getroot()
    assert root.tag=='{http://www.w3.org/2000/svg}svg'
    assert root.get('viewBox'),f'Missing viewBox: {path}'
    assert path.stat().st_size<1_000_000,f'Oversized SVG: {path}'
    for el in root.iter():
        assert not el.tag.endswith(('script','foreignObject')),f'Unsafe SVG: {path}'
        assert not any(k.lower().startswith('on') for k in el.attrib),f'Event handler: {path}'
        assert not any(k.endswith('href') and v.startswith(('http:','https:','data:')) for k,v in el.attrib.items()),f'Remote SVG dependency: {path}'
readme=(ROOT/'README.md').read_text();Images().feed(readme)
for link in re.findall(r'\]\((\./[^)#]+)',readme):assert (ROOT/link).exists(),f'Missing local link: {link}'
assert '<!-- SNAKE:START -->' in readme and '<!-- SNAKE:END -->' in readme
assert '\\<' not in readme,'Escaped HTML would render as code'
validate_days(json.loads((ROOT/'data/contributions.json').read_text())['days'])
snapshot=json.loads((ROOT/'data/repositories.json').read_text())
assert len(snapshot['repositories'])==len({r['name'] for r in snapshot['repositories']})
print('SVG safety, image paths, alt text, local links, and data snapshots validated')
