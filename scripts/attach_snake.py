"""Insert a verified snake asset in the README's dedicated marker only."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from generate_city import ROOT, write_if_changed
path=ROOT/'assets/contribution-snake.svg'
root=ET.parse(path).getroot()
assert root.tag=='{http://www.w3.org/2000/svg}svg'
if root.get('viewBox') is None:
    width=root.get('width','1200').removesuffix('px')
    height=root.get('height','200').removesuffix('px')
    root.set('viewBox',f'0 0 {width} {height}')
# Respect reduced motion even when generated upstream animations are enabled.
ns='{http://www.w3.org/2000/svg}'
style=ET.SubElement(root,ns+'style')
style.text='@media(prefers-reduced-motion:reduce){*{animation:none!important}}'
ET.register_namespace('', 'http://www.w3.org/2000/svg')
write_if_changed(path, ET.tostring(root,encoding='unicode')+'\n')
readme=ROOT/'README.md'
text=readme.read_text()
replacement='<!-- SNAKE:START -->\n<img src="./assets/contribution-snake.svg" width="100%" alt="Animated snake traversing actual GitHub contribution activity; decorative supplement to the contribution city" />\n<!-- SNAKE:END -->'
updated,count=re.subn(r'<!-- SNAKE:START -->.*?<!-- SNAKE:END -->',lambda _:replacement,text,flags=re.S)
assert count==1, 'Expected exactly one snake marker'
write_if_changed(readme,updated)

