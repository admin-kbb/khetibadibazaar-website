"""Dependency-free checks for the exact directory published to GitHub Pages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

ROOT = Path(__file__).resolve().parents[1] / 'site'
errors = []

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.refs = path, set(), []
        self.h1s = self.mains = self.titles = 0
        self.lang = self.viewport = self.description = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                errors.append(f'{self.path.name}: duplicate ID {attrs["id"]}')
            self.ids.add(attrs['id'])
        self.h1s += tag == 'h1'
        self.mains += tag == 'main'
        self.titles += tag == 'title'
        if tag == 'html': self.lang = bool(attrs.get('lang'))
        if tag == 'meta':
            self.viewport |= attrs.get('name') == 'viewport'
            self.description |= attrs.get('name') == 'description' and bool(attrs.get('content'))
        if tag == 'img' and 'alt' not in attrs:
            errors.append(f'{self.path.name}: image needs alternative text')
        for attr in ('href', 'src'):
            if attrs.get(attr): self.refs.append(attrs[attr])

pages = {}
for path in ROOT.rglob('*'):
    if path.is_symlink(): errors.append(f'Symlink cannot be published: {path}')
    if path.is_file() and path.suffix.lower() not in {'.html', '.css', '.js', '.png', '.webp', '.ttf', '.txt'} and path.name != '.nojekyll':
        errors.append(f'Unexpected public file: {path.relative_to(ROOT)}')
for path in ROOT.glob('*.html'):
    page = Page(path)
    page.feed(path.read_text())
    pages[path.resolve()] = page
    if not (page.h1s == page.mains == page.titles == 1 and page.lang and page.viewport and page.description):
        errors.append(f'{path.name}: needs one title/h1/main, language, viewport and description')
for path, page in pages.items():
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc: continue
        if url.path.startswith('/'):
            errors.append(f'{path.name}: root-relative link breaks GitHub project URLs: {ref}')
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
            errors.append(f'{path.name}: missing or out-of-site target {ref}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{path.name}: missing fragment {ref}')
for path in ROOT.rglob('*.css'):
    for ref in re.findall(r'url\([\'\"]?([^\)\'\"]+)', path.read_text()):
        if not urlsplit(ref).scheme and not (path.parent / ref).is_file():
            errors.append(f'{path.name}: missing CSS asset {ref}')
for name in ('machinery', 'crops', 'cattle', 'seeds', 'farming_land'):
    if not (ROOT / f'assets/{name}.webp').is_file(): errors.append(f'Missing category image: {name}')
if len(pages) < 3: errors.append('Expected Home, About and Future pages')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print(f'Validated {len(pages)} pages, local links, fragments, image text and public assets.')
