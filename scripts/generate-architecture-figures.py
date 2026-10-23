"""Draw architecture processes as nodes while retaining the source ASCII topology."""
from pathlib import Path
from html import escape
root=Path(__file__).resolve().parents[1]/'assets/images/docs'
def diagram(name,title,w,h,nodes,edges):
 key=name+'-arrow'
 s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{title}" style="font-family:Jost,system-ui,sans-serif;width:100%;height:auto;display:block"><title>{title}</title><defs><marker id="{key}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1 L9 5 L1 9" fill="none" stroke="var(--rtc-accent, #bc4319)" stroke-width="1.5"/></marker></defs><rect width="{w}" height="{h}" rx="12" fill="var(--rtc-surface, #f6f8fa)"/>'
 for d in edges:s+=f'<path d="{d}" fill="none" stroke="var(--rtc-accent, #bc4319)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#{key})"/>'
 for x,y,bw,bh,lines in nodes:
  s+=f'<path d="M{x+2} {y+2} Q{x+bw/2} {y-1} {x+bw-2} {y+2} L{x+bw-1} {y+bh-2} Q{x+bw/2} {y+bh+1} {x+1} {y+bh-2} Z" fill="var(--bs-body-bg, #fff)" stroke="var(--rtc-accent, #bc4319)" stroke-width="2" stroke-linejoin="round"/>'
  for i,line in enumerate(lines):
   ty=y+bh/2-(len(lines)-1)*13+7+i*26
   s+=f'<text x="{x+bw/2}" y="{ty}" text-anchor="middle" font-size="21" fill="var(--bs-body-color, #28323b)">{escape(line)}</text>'
 s+='</svg>';(root/(name+'.svg')).write_text(s)
diagram('overview-architecture-2','In the browser',1000,700,[
 (290,24,320,64,['RTCPeerConnection.getStats()']),
 (24,142,215,64,['Browser adapters']),
 (290,142,320,64,['Linked monitor graph']),
 (650,260,300,64,['Interval metrics']),
 (650,360,150,64,['Detectors']),
 (840,360,140,64,['Issues /','events']),
 (650,460,300,64,['Quality scores']),
 (310,550,280,64,['createSample()']),
 (310,636,280,48,['ClientSample'])
],['M450 88 L450 112 L132 112 L132 142','M239 174 L290 174',
 'M450 206 L450 292 L650 292','M450 292 L450 392 L650 392',
 'M800 392 L840 392','M450 392 L450 492 L650 492',
 'M450 492 L450 550','M450 614 L450 636'])
diagram('overview-architecture-3','Across the wire',1120,450,[
 (24,28,200,64,['ClientSample']),(290,28,170,64,['JSON']),
 (860,28,230,64,['ClientSample']),
 (24,166,200,64,['ClientSample']),(290,166,210,64,['Delta encoder']),
 (580,166,210,64,['Your transport']),
 (580,286,210,64,['Delta decoder']),
 (860,286,230,64,['ClientSample']),
 (850,382,250,52,['Observer.accept()'])
],['M224 60 L290 60','M460 60 L860 60','M224 198 L290 198',
 'M500 198 L580 198','M685 230 L685 286','M790 318 L860 318','M975 350 L975 382'])
