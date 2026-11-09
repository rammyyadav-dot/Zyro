#!/usr/bin/env python3
"""Check generated SEO invariants after rebuilding the static site."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://zyrostyle.com'


class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.title = ''; self.h1 = 0; self.meta = {}; self.canonical = []; self.json = []; self.links = []; self.mode = ''; self.buf = ''
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'title' or tag == 'script' and a.get('type') == 'application/ld+json':
            self.mode = tag; self.buf = ''
        if tag == 'h1': self.h1 += 1
        if tag == 'meta': self.meta[a.get('name')] = a.get('content')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical.append(a.get('href'))
        if tag in ('a', 'script', 'img'): self.links.append(a.get('href', a.get('src', '')))
    def handle_data(self, data):
        if self.mode: self.buf += data
    def handle_endtag(self, tag):
        if tag == self.mode:
            if tag == 'title': self.title = self.buf
            else: self.json.append(json.loads(self.buf))
            self.mode = ''


def check():
    titles = []; descriptions = []; urls = set(); pages = list(ROOT.glob('*/index.html')) + [ROOT/'index.html', ROOT/'404.html']
    for file in pages:
        s = file.read_text(); p = Page(); p.feed(s)
        slug = '' if file.parent == ROOT else file.parent.name + '/'
        assert p.canonical == [BASE + '/' + slug], file
        assert p.h1 == 1 and p.title and p.meta.get('description'), file
        assert p.json, file
        assert 'https://www.zyrostyle.com' not in s, file
        assert 'award-winning' not in s.lower(), file
        assert s.count('js/measurement.js') == 1, file
        titles.append(p.title); descriptions.append(p.meta['description'])
        if file.name != '404.html': urls.add(p.canonical[0])
        else: assert 'noindex' in p.meta['robots']
        for href in p.links:
            u = urlsplit(href)
            if u.netloc and u.hostname != 'zyrostyle.com' or u.scheme and u.scheme not in ('http', 'https'): continue
            if not u.path: continue
            target = ROOT / unquote(u.path.lstrip('/')) if u.path.startswith('/') or u.netloc else file.parent / unquote(u.path)
            if target.is_dir(): target /= 'index.html'
            assert target.exists(), (file, href)
    assert max(Counter(titles).values()) == 1
    assert max(Counter(descriptions).values()) == 1
    sm = ET.parse(ROOT/'sitemap.xml'); ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    assert {n.text for n in sm.findall('.//s:loc', ns)} == urls
    assert not sm.findall('.//s:lastmod', ns), 'Do not use build dates as content modification dates'
    assert f'Sitemap: {BASE}/sitemap.xml' in (ROOT/'robots.txt').read_text()
    print(f'Passed SEO checks on {len(pages)} pages and {len(urls)} sitemap URLs')


if __name__ == '__main__': check()
