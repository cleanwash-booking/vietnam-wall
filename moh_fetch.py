"""Fetch posthumous Vietnam War Medal of Honor recipients from Wikipedia: name, date of action,
free-licensed portrait (if any) and the text of the official citation. Writes build/moh.json.
Run by the GitHub Actions build; if Wikipedia cannot be reached, the build keeps the committed moh.json."""
import json, os, re, sys, time, html, urllib.request, urllib.parse

API = 'https://en.wikipedia.org/w/api.php'
UA = 'LKNWallBuilder/1.0 (https://wall.lkn-law.com; remembrance site build)'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'moh.json')
MONTHS = {m: i + 1 for i, m in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July',
                                           'August', 'September', 'October', 'November', 'December'])}

def api(**p):
    p.update(format='json', formatversion='2')
    url = API + '?' + urllib.parse.urlencode(p)
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=30) as f:
                return json.load(f)
        except Exception as e:
            if attempt == 3: raise
            time.sleep(2 + attempt * 3)

def strip(h):
    h = re.sub(r'(?s)<style.*?</style>', '', h)
    h = re.sub(r'(?s)<figure.*?</figure>', '', h)
    h = re.sub(r'(?s)<div[^>]*class="[^"]*(?:thumb|hatnote|navbox|reflist)[^"]*".*?</div>\s*</div>', '', h)
    h = re.sub(r'(?s)<sup[^>]*class="[^"]*reference[^"]*"[^>]*>.*?</sup>', '', h)
    h = re.sub(r'(?s)<span class="mw-editsection.*?</span>\s*</span>', '', h)
    h = re.sub(r'(?s)<div class="mw-heading.*?</div>', '', h)
    h = re.sub(r'(?s)<h[1-6].*?</h[1-6]>', '', h)
    h = re.sub(r'(?i)</p>|<br\s*/?>|</li>|</blockquote>|</dd>|</div>', '\n', h)
    h = re.sub(r'<[^>]+>', '', h)
    h = html.unescape(h)
    h = re.sub(r'\[\s*(\d+|edit|citation needed)\s*\]', '', h)
    lines = [re.sub(r'\s+', ' ', l).strip() for l in h.split('\n')]
    return '\n'.join(l for l in lines if l)

def main():
    t = api(action='parse', page='List of Medal of Honor recipients for the Vietnam War', prop='text', redirects=1)['parse']['text']
    rows = re.split(r'(?i)<tr[\s>]', t)
    recs = []
    for row in rows:
        cells = re.findall(r'(?s)<t[dh][^>]*>(.*?)</t[dh]>', row)
        name_cell = None
        for c in cells:
            if '<img' in c: continue
            txt = strip(c)
            if '†' in txt and re.search(r'<a href="/wiki/', c) and len(txt) < 70:
                name_cell = c; break
        if not name_cell: continue
        m = re.search(r'<a href="/wiki/([^"#]+)"[^>]*>', name_cell)
        title = urllib.parse.unquote(m.group(1)).replace('_', ' ')
        name = strip(name_cell).replace('†', '').strip()
        rowtxt = strip(row)
        d = re.search(r'([A-Z][a-z]+) (\d{1,2}), (19\d\d)', rowtxt)
        date = '%s-%02d-%02d' % (d.group(3), MONTHS.get(d.group(1), 1), int(d.group(2))) if d and d.group(1) in MONTHS else ''
        recs.append({'name': name, 'title': title, 'date': date})
    print('posthumous recipients found', len(recs))
    # portraits (free licenses only)
    for i in range(0, len(recs), 40):
        ch = recs[i:i + 40]
        q = api(action='query', redirects=1, prop='pageimages', piprop='name|thumbnail', pithumbsize=400, pilicense='free', titles='|'.join(r['title'] for r in ch))['query']
        alias = {}
        for n in q.get('normalized', []) + q.get('redirects', []): alias[n['from']] = n['to']
        pages = {p['title']: p for p in q.get('pages', [])}
        for r in ch:
            tt = alias.get(r['title'], r['title']); tt = alias.get(tt, tt)
            p = pages.get(tt)
            if not p: continue
            r['page'] = p['title']
            if p.get('thumbnail'):
                r['thumb'] = p['thumbnail']['source']; r['file'] = p['pageimage']
        time.sleep(0.3)
    withimg = [r for r in recs if r.get('file')]
    for i in range(0, len(withimg), 40):
        ch = withimg[i:i + 40]
        q = api(action='query', prop='imageinfo', iiprop='extmetadata', iiextmetadatafilter='LicenseShortName|Artist', titles='|'.join('File:' + r['file'] for r in ch))['query']
        alias = {n['to']: n['from'] for n in q.get('normalized', [])}
        for p in q.get('pages', []):
            src = alias.get(p['title'], p['title'])
            r = next((z for z in ch if ('File:' + z['file']) in (src, p['title']) or ('File:' + z['file']).replace('_', ' ') == p['title']), None)
            if not r or not p.get('imageinfo'): continue
            em = p['imageinfo'][0].get('extmetadata', {})
            r['lic'] = (em.get('LicenseShortName') or {}).get('value', '')
            r['artist'] = strip((em.get('Artist') or {}).get('value', ''))[:90]
            r['filepage'] = 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(p['title'].replace(' ', '_'))
        time.sleep(0.3)
    # citations
    for r in recs:
        if not r.get('page'): continue
        try:
            secs = api(action='parse', page=r['page'], prop='sections', redirects=1)['parse']['sections']
            s = next((x for x in secs if re.search(r'citation', re.sub(r'<[^>]+>', '', x['line']), re.I)), None)
            if s:
                txt = api(action='parse', page=r['page'], prop='text', section=s['index'], redirects=1)['parse']['text']
                r['cit'] = strip(txt)
        except Exception as e:
            print('citation failed', r['name'], e)
        time.sleep(0.15)
    good = [r for r in recs if r.get('page')]
    print('pages', len(good), 'portraits', sum(1 for r in good if r.get('thumb')), 'citations', sum(1 for r in good if len(r.get('cit', '')) > 200))
    if len(good) < 100:
        sys.exit('too few records; keeping existing moh.json')
    json.dump(good, open(OUT, 'w'), indent=0, ensure_ascii=False)

if __name__ == '__main__':
    main()
