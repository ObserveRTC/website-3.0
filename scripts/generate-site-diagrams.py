from pathlib import Path
import re,html
# Source text retains each diagram's original spatial relationships.
root=Path(__file__).resolve().parents[1] / 'assets/images/docs'
for p in root.glob('*.txt'):
 lines=p.read_text().rstrip().splitlines();cols=max(map(len,lines));cw=10;rh=27;pad=24;w=cols*cw+pad*2;h=len(lines)*rh+pad*2
 key=p.stem
 parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{key}-title" style="font-family:Jost,system-ui,sans-serif;width:100%;height:auto;display:block"><title id="{key}-title">{html.escape(key.replace("-"," "))}</title><rect width="{w}" height="{h}" rx="12" fill="var(--rtc-surface, #f6f8fa)"/><g stroke="var(--rtc-accent, #bc4319)" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round">']
 labels=[]
 for row,line in enumerate(lines):
  chars=list(line); masks=set()
  for i,c in enumerate(chars):
   before=line[i-1] if i else ' ';after=line[i+1] if i+1<len(line) else ' '
   connect=c in '|+│─└├┬┐┘┌┤↓→' or c in '<>' and (before=='-' or after=='-') or c=='-' and (before in '-+<>' or after in '-+<>') or c=='v' and before==' ' and after==' '
   if not connect:continue
   masks.add(i);x=pad+i*cw+cw/2;y=pad+row*rh+rh/2
   def path(d):parts.append(f'<path d="{d}"/>')
   if c in '-─':path(f'M{x-cw/2} {y} Q{x} {y-.5} {x+cw/2} {y}')
   elif c in '|│':path(f'M{x} {y-rh/2} Q{x+.4} {y} {x} {y+rh/2}')
   elif c=='+':
    if before in '-+':path(f'M{x-cw/2} {y} L{x} {y}')
    if after in '-+':path(f'M{x} {y} L{x+cw/2} {y}')
    above=lines[row-1][i:i+1] if row else '';below=lines[row+1][i:i+1] if row+1<len(lines) else ''
    if above in ('|','+'):path(f'M{x} {y-rh/2} L{x} {y}')
    if below in ('|','+'):path(f'M{x} {y} L{x} {y+rh/2}')
   elif c in '└├':
    path(f'M{x} {y-rh/2} L{x} {y} L{x+cw/2} {y}')
    if c=='├':path(f'M{x} {y} L{x} {y+rh/2}')
   elif c in '>→':
    path(f'M{x-cw/2} {y} L{x+cw/2} {y} M{x} {y-4} L{x+cw/2} {y} L{x} {y+4}')
   elif c=='<':path(f'M{x+cw/2} {y} L{x-cw/2} {y} M{x} {y-4} L{x-cw/2} {y} L{x} {y+4}')
   elif c in 'v↓':path(f'M{x} {y-rh/2} L{x} {y+4} M{x-4} {y} L{x} {y+4} L{x+4} {y}')
  cleaned=''.join(' ' if i in masks else c for i,c in enumerate(chars))
  for m in re.finditer(r'\S(?:.*?\S)?(?= {2,}|$)',cleaned):
   label=m.group();x=pad+m.start()*cw;y=pad+row*rh+rh/2+6
   # Jost stays sharp, with the original grid reserving room for every label.
   labels.append(f'<text x="{x}" y="{y}" font-size="18">{html.escape(label)}</text>')
 parts+=['</g><g fill="var(--bs-body-color, #28323b)">',*labels,'</g></svg>']
 p.with_suffix('.svg').write_text(''.join(parts))

# These process diagrams use explicit rectangular nodes with the same branches.
import runpy
runpy.run_path(str(Path(__file__).with_name('generate-architecture-figures.py')))
runpy.run_path(str(Path(__file__).with_name('generate-issue-lifecycle.py')))
