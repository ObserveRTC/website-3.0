"""Render the stateful issue lifecycle with clear nodes and directional arrows."""
from pathlib import Path
from html import escape
root=Path(__file__).resolve().parents[1]
key='issue-lifecycle'
s=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 350" role="img" aria-labelledby="{key}-title" style="font-family:Jost,system-ui,sans-serif;width:100%;height:auto;display:block"><title id="{key}-title">Stateful issue lifecycle: observations, confirmation, raise, evidence updates, recovery, resolution</title><defs><marker id="{key}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1 L9 5 L1 9" fill="none" stroke="var(--rtc-accent, #bc4319)" stroke-width="1.6"/></marker></defs><rect width="1000" height="350" rx="12" fill="var(--rtc-surface, #f6f8fa)"/>'''
for d in ['M300 87 L350 87','M640 87 L690 87','M835 127 L835 215','M690 255 L640 255','M350 255 L300 255']:
 s+=f'<path d="{d}" fill="none" stroke="var(--rtc-accent, #bc4319)" stroke-width="2" stroke-linecap="round" marker-end="url(#{key}-arrow)"/>'
for x,y,title,sub in [(20,46,'Eligible observations','Measurements and state'),(350,46,'Condition confirmed','Detector criteria met'),(690,46,'Keyed issue raised','An active occurrence begins'),(690,214,'Evidence updated','The issue remains active'),(350,214,'Recovery confirmed','Recovery criteria met'),(20,214,'Issue resolved','The active occurrence ends')]:
 w=280 if x==20 else 290
 s+=f'<path d="M{x+2} {y+2} Q{x+w/2} {y-1} {x+w-2} {y+2} L{x+w-1} {y+80} Q{x+w/2} {y+83} {x+1} {y+80} Z" fill="var(--bs-body-bg, #fff)" stroke="var(--rtc-accent, #bc4319)" stroke-width="2" stroke-linejoin="round"/>'
 s+=f'<text x="{x+w/2}" y="{y+33}" text-anchor="middle" font-size="24" fill="var(--rtc-accent, #bc4319)">{escape(title)}</text><text x="{x+w/2}" y="{y+61}" text-anchor="middle" font-size="19" fill="var(--bs-body-color, #28323b)">{escape(sub)}</text>'
s+='<text x="500" y="332" text-anchor="middle" font-size="19" fill="var(--bs-body-color, #28323b)">The same issue key links an occurrence from raise to resolution.</text></svg>'
(root/'assets/images/docs/concepts-detection-1.svg').write_text(s)
