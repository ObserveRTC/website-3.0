"""Check local HTML links and fragments in the built documentation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import sys
root = Path(__file__).resolve().parents[1] / 'public'
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.links=[]; self.ids=set(); self.feed(text)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs: self.ids.add(attrs['id'])
        if tag=='a' and attrs.get('href'): self.links.append(attrs['href'])
files=[p for p in root.rglob('*.html') if 'reference/source-atlas.html' not in p.as_posix()]
pages={p:Page(p.read_text()) for p in files}; errors=[]
for file,page in pages.items():
    route='/' + file.relative_to(root).as_posix().removesuffix('index.html')
    for link in page.links:
        url=urlsplit(urljoin('http://local'+route,link))
        if url.netloc not in ('local','localhost','localhost:1313') or url.scheme not in ('http','https'): continue
        path=root/unquote(url.path).lstrip('/')
        if path.is_dir(): path=path/'index.html'
        if not path.exists(): errors.append(f'{route}: missing {link}')
        elif url.fragment and path in pages and unquote(url.fragment) not in pages[path].ids:
            errors.append(f'{route}: missing fragment {link}')
for error in sorted(set(errors)): print(error)
print(f'Checked {len(pages)} HTML pages; {len(set(errors))} broken local links/fragments.')
sys.exit(bool(errors))
