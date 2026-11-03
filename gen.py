import json, os, re, sys, html, collections, datetime, shutil
sys.path.insert(0, os.path.dirname(__file__))
from ranks import rank_full, SVC

ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'site')
BASE = 'https://wall.lkn-law.com'
HUB = 'https://lkn-law.com/vietnam-war/'
SHARE = 'https://lkn-law.com/vietnam-war/the-wall/share-a-memory/'
V = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H%M')
LIMIT = int(os.environ.get('LIMIT', '0'))  # for quick test builds

R = json.load(open(os.path.join(ROOT, 'build/records.json')))
fixes = json.load(open(os.path.join(ROOT, 'build/panel_fixes.json')))
adds = json.load(open(os.path.join(ROOT, 'build/additions.json'))) if os.path.exists(os.path.join(ROOT, 'build/additions.json')) else []
for r in R:
    if r['wall'] in fixes:
        p, l = fixes[r['wall']].split()
        r['panel'] = '%02d%s' % (int(p[:-1]), p[-1]); r['line'] = int(l)
for a in adds:
    R.append(a)
R = [r for r in R if r['panel']]

E = html.escape
MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']
def ldate(iso):
    if not iso: return ''
    y, m, d = iso.split('-'); return '%s %d, %s' % (MONTHS[int(m)-1], int(d), y)
def tc(s):
    if not s: return ''
    return re.sub(r"(^|[\s\-/(])([a-z])", lambda m: m.group(1)+m.group(2).upper(), s.lower())
STATES = {}
for r in R:
    if r['st'] and r['state']: STATES[r['st']] = tc(r['state'])
STATES.update({'DC':'District of Columbia','GU':'Guam','VI':'U.S. Virgin Islands','AS':'American Samoa','CZ':'Panama Canal Zone','PR':'Puerto Rico'})

# ---------- slugs ----------
def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
base = collections.Counter(slugify(r['wall']) for r in R)
seen = set()
for r in R:
    s = slugify(r['wall'])
    if base[s] > 1: s = '%s-%s-%d' % (s, r['panel'].lower().lstrip('0'), r['line'])
    while s in seen: s += '-' + (r['birth'] or 'x')[:4]
    seen.add(s); r['slug'] = s

# ---------- ordering ----------
def pkey(p):
    n, side = int(p[:-1]), p[-1]
    return (0, n) if side == 'E' else (1, -n)   # chronological: 1E..70E, 70W..1W
for r in R: r['_k'] = (pkey(r['panel']), r['line'], r['death'] or '', r['last'], r['given'])
R.sort(key=lambda r: r['_k'])
panels = collections.OrderedDict()
for r in R: panels.setdefault(r['panel'], []).append(r)
maxline = {p: max(x['line'] for x in v) for p, v in panels.items()}
visual = ['%02dW' % i for i in range(70, 0, -1)] + ['%02dE' % i for i in range(1, 71)]   # left to right as you face the Wall

def wname(r):
    g = r['given'].split()
    g = ([g[0]] + [x[0] for x in g[1:]]) if g else []
    return ' '.join(g + [r['last']] + ([r['suf']] if r['suf'] else []))
def sx(r): return {'ARMY':'A','MARINE CORPS':'M','AIR FORCE':'F','NAVY':'N','COAST GUARD':'C'}.get(r['svc'], '')

# ---------- data files ----------
os.makedirs(os.path.join(OUT, 'data/panels'), exist_ok=True)
for p, v in panels.items():
    rows = [[r['slug'], wname(r), r['line'], r['rank'], sx(r), r['city'], r['st'], (r['death'] or '').replace('-', ''), p.lstrip('0'), r['sex']] for r in v]
    json.dump(rows, open(os.path.join(OUT, 'data/panels/%s.json' % p), 'w'), separators=(',', ':'))
idx = [[r['slug'], wname(r), r['city'], r['st'], r['panel'], (r['death'] or '')[:4], r['line']] + ([r['wall']] if r['wall'] != wname(r) else []) for r in R]
json.dump(idx, open(os.path.join(OUT, 'data/index.json'), 'w'), separators=(',', ':'))
meta = {'v': V, 'panels': [{'p': p, 'n': maxline.get(p, 1)} for p in visual]}

# ---------- shared chrome ----------
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500&family=Tenor+Sans&display=swap" rel="stylesheet">'
def head(title, desc, path, depth, extra=''):
    up = '../' * depth
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title><meta name="description" content="%s"><link rel="canonical" href="%s/%s">'
            '<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:type" content="website"><meta property="og:url" content="%s/%s">'
            '<meta name="theme-color" content="#0a0b0d">%s<link rel="stylesheet" href="%sassets/style.css?v=%s">%s</head><body>'
            % (E(title), E(desc), BASE, path, E(title), E(desc), BASE, path, FONTS, up, V, extra))
def topbar(depth, cur=''):
    up = '../' * depth
    links = [('', 'The Wall'), ('states/', 'By state'), ('about/', 'About &amp; sources')]
    nav = ''.join('<a href="%s%s"%s>%s</a>' % (up, h, ' aria-current="page"' if h == cur else '', t) for h, t in links)
    return ('<header class="top"><div class="wrap"><a class="brand" href="%s">The Wall<small>Vietnam Veterans Memorial · The Lake Norman Brief</small></a>'
            '<nav>%s<a href="%s">Vietnam War history &rarr;</a></nav></div></header>' % (up, nav, HUB))
def foot(depth):
    up = '../' * depth
    return ('<footer class="foot"><div class="wrap"><p>An independent online remembrance of the names on the Vietnam Veterans Memorial in Washington, D.C., published by '
            '<a href="https://lkn-law.com/">The Lake Norman Brief</a> (Adkins Law, PLLC). Service records come from the U.S. Department of Defense casualty file held by the National Archives. '
            'This site is not affiliated with the Vietnam Veterans Memorial Fund or the National Park Service. See <a href="%sabout/">About &amp; sources</a> to report a correction.</p></div></footer></body></html>' % up)

def write(path, s):
    full = os.path.join(OUT, path); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(s)

# ---------- locator image (all 140 panels, top-aligned) ----------
MAXL = max(maxline.values()) + 5
W, H = 1400, 160
pw = W / 140.0
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"><rect width="%d" height="%d" fill="#2c2d2f"/><rect width="%d" height="8" fill="#1c2a1e"/>' % (W, H, W, H, W)]
for i, p in enumerate(visual):
    lines = maxline.get(p, 1) + (5 if p in ('01E', '01W') else 0)
    h = (lines + 3) / (MAXL + 3) * (H - 18)
    svg.append('<rect x="%.2f" y="8" width="%.2f" height="%.2f" fill="#0e1013" stroke="#000" stroke-width=".4"/>' % (i * pw, pw, h))
svg.append('<text x="%.1f" y="%d" fill="#8d9298" font-family="sans-serif" font-size="11" text-anchor="middle">WEST WALL</text>' % (W*0.25, H-4))
svg.append('<text x="%.1f" y="%d" fill="#8d9298" font-family="sans-serif" font-size="11" text-anchor="middle">EAST WALL</text>' % (W*0.75, H-4))
svg.append('</svg>')
write('assets/locator.svg', ''.join(svg))
def loc_pos(p, line):
    i = visual.index(p)
    x = (i + 0.5) / 140 * 100
    off = 5 if p == '01E' else 0
    y = (8 + ((line + off + 0.5) / (MAXL + 3)) * (H - 18) + 2) / H * 100
    return x, y

FLAG = ('<svg viewBox="0 0 100 100" aria-hidden="true"><path d="M8 82 L50 18 L92 82 Z" fill="#1c2b4a" stroke="#c9a24e" stroke-width="2"/>'
        '<g fill="#e7e5e0">' + ''.join('<circle cx="%d" cy="%d" r="2.2"/>' % (x, y) for x, y in [(50,34),(42,48),(58,48),(34,62),(50,62),(66,62),(26,74),(42,74),(58,74),(74,74)]) +
        '</g></svg>')

# ---------- casualty wording ----------
def casualty(r):
    cat = r['cat']
    if cat in ('SELF-INFLICTED', 'HOMICIDE'): return 'Non-hostile', 'Died of other causes', ''
    h = 'Hostile' if r['hostile'] == 'H' else 'Non-hostile'
    reason = tc(r['reason']).replace('Mc)', 'MC)').replace('(Mc', '(MC').replace('--', '—') if r['reason'] else ''
    if r['reason'] and r['reason'].startswith('AIRCRAFT') or 'CRASH' in (r['reason'] or ''):
        reason = reason.replace('Crew (MC)', 'crew').replace('Crew (Mc)', 'crew')
    return h, tc(cat).replace('In Action', 'in Action').replace('Of Wounds', 'of Wounds'), reason

def comp(r):
    c = r['comp']
    if c == 'SELECTED SERVICE': return 'Drafted (Selective Service)'
    if c == 'ACTIVE - REGULAR': return 'Regular'
    if c == 'ACTIVE - GUARD/RESERVE': return 'Reserve / National Guard'
    return tc(c) if c else ''

def lead(r):
    he, his = ('She', 'her') if r['sex'] == 'F' else ('He', 'his')
    rank = rank_full(r['svc'], r['rank'])
    home = ', '.join(x for x in [tc(r['city']), STATES.get(r['st'], r['st'])] if x)
    s = E(r['display'])
    if home: s += ', of ' + E(home) + ','
    s += ' served as %s %s in the %s.' % ('an' if rank[:1] in 'AEIOU' else 'a', E(rank), E(SVC.get(r['svc'], tc(r['svc']))))
    where = ''
    if r['prov']: where = ' in %s Province, %s' % (E(tc(r['prov'])), E(tc(r['country'])))
    elif r['country']: where = ' in %s' % E(tc(r['country']))
    if not r['death']:
        s += ' %s died as a result of the Vietnam War.' % he
    elif r['cat'] in ('DECLARED DEAD', 'PRESUMED DEAD'):
        s += ' %s was lost on %s%s and was later declared dead.' % (he, ldate(r['death']) + (',' if where else ''), (where + ',') if where else '')
    else:
        age = (' at age %d' % r['age']) if r['age'] else ''
        s += ' %s died on %s%s%s.' % (he, ldate(r['death']) + (',' if where or age else ''), where, (',' if where and age else '') + age)
    s += ' %s name is inscribed on Panel %s, Line %d of the Vietnam Veterans Memorial.' % (his.capitalize(), r['panel'].lstrip('0'), r['line'])
    return s

by_line = collections.defaultdict(list)
by_unit_day = collections.defaultdict(list)
by_town = collections.defaultdict(list)
for r in R:
    by_line[(r['panel'], r['line'])].append(r)
    if r['unit']: by_unit_day[(r['unit'], r['death'])].append(r)
    if r['city'] and r['st']: by_town[(r['city'], r['st'])].append(r)

def name_li(x, depth, sub):
    return '<li><a href="%sname/%s/">%s</a><small>%s</small></li>' % ('../' * depth, x['slug'], E(x['wall']), E(sub))

def vvmf(r):
    q = ' '.join(x for x in [r['given'].split(' ')[0] if r['given'] else '', r['last']] if x)
    return 'https://www.vvmf.org/Wall-of-Faces/search/results/?search-term=' + q.replace(' ', '+')

def profile(r):
    d = 2
    rank = rank_full(r['svc'], r['rank'])
    svc = SVC.get(r['svc'], tc(r['svc']))
    pn = r['panel'].lstrip('0')
    hos, cat, reason = casualty(r)
    home = ', '.join(x for x in [tc(r['city']), STATES.get(r['st'], r['st'])] if x)
    title = '%s, %s, %s — Vietnam Veterans Memorial Panel %s, Line %d' % (r['display'], rank, svc, pn, r['line'])
    desc = 'Service record and remembrance page for %s%s, %s, %s%s. Panel %s, Line %d of the Vietnam Veterans Memorial.' % (
        r['display'], (' of ' + home) if home else '', rank, svc, (', who died ' + ldate(r['death'])) if r['death'] else '', pn, r['line'])
    ld = {'@context': 'https://schema.org', '@type': 'Person', 'name': r['display'], 'deathDate': r['death'],
          'memberOf': {'@type': 'Organization', 'name': svc}, 'jobTitle': rank}
    if r['birth']: ld['birthDate'] = r['birth']
    if home: ld['homeLocation'] = {'@type': 'Place', 'name': home}
    x, y = loc_pos(r['panel'], r['line'])
    rows = [('Branch', svc), ('Rank', '%s (%s)' % (rank, r['rank']) if rank != r['rank'] else rank)]
    if comp(r): rows.append(('Service', comp(r)))
    if r['mos_desc'] and r['mos_desc'].strip(): rows.append(('Occupation', tc(r['mos_desc']) + (' (%s)' % r['mos'] if r['mos'] else '')))
    if r['unit']: rows.append(('Unit (as recorded)', r['unit']))
    if r['birth']: rows.append(('Born', ldate(r['birth'])))
    if home: rows.append(('Home of record', home + (' (%s County)' % tc(r['county']) if r['county'] and r['st'] not in ('AK','LA') else '')))
    crows = []
    if r['death']: crows.append(('Date of loss' if r['cat'] in ('DECLARED DEAD','PRESUMED DEAD') else 'Date of death', ldate(r['death'])))
    if r['age'] and r['cat'] not in ('DECLARED DEAD','PRESUMED DEAD'): crows.append(('Age', str(r['age'])))
    if r['prov']: crows.append(('Province', tc(r['prov'])))
    if r['country']: crows.append(('Country', tc(r['country'])))
    if r.get('src') != 'vvmf':
        crows.append(('Casualty type', hos))
        crows.append(('Category', cat))
    if reason: crows.append(('Circumstance', reason))
    if r.get('added'): crows.append(('Added to the Wall', r['added']))
    if r.get('aircraft'): crows.append(('Aircraft', r['aircraft']))
    if r.get('op') and r['op'] not in ('VIETNAM CONFLICT', ''): crows.append(('Incident', tc(r['op'])))
    if r.get('inc_short') in ('MIA', 'MSG', 'POW'):
        crows.append(('First reported', {'MIA': 'Missing in action', 'MSG': 'Missing', 'POW': 'Captured / prisoner of war'}[r['inc_short']]))
    if r.get('body') == 'N': crows.append(('Remains', 'Not recovered as of the 2008 DoD record'))
    dl = lambda rs: '<dl class="rec">' + ''.join('<dt>%s</dt><dd>%s</dd>' % (E(a), E(b)) for a, b in rs) + '</dl>'
    he = 'her' if r['sex'] == 'F' else 'his'
    line_mates = [z for z in by_line[(r['panel'], r['line'])] if z is not r]
    unit_mates = [z for z in by_unit_day.get((r['unit'], r['death']), []) if z is not r][:24] if r['unit'] else []
    town = [z for z in by_town.get((r['city'], r['st']), []) if z is not r]
    rel = ''
    if line_mates:
        rel += '<div class="box"><h2>Also on Panel %s, Line %d</h2><ul class="names">%s</ul></div>' % (pn, r['line'], ''.join(name_li(z, d, '%s · %s' % (rank_full(z['svc'], z['rank']), ldate(z['death']))) for z in line_mates))
    if unit_mates:
        rel += '<div class="box"><h2>Same unit, same day</h2><ul class="names">%s</ul></div>' % ''.join(name_li(z, d, '%s · Panel %s, Line %d' % (rank_full(z['svc'], z['rank']), z['panel'].lstrip('0'), z['line'])) for z in unit_mates)
    if town:
        more = ''
        if len(town) > 10: more = '<p class="note" style="margin-top:8px"><a href="../../states/%s/#%s">All %d names from %s &rarr;</a></p>' % (r['st'].lower(), slugify(r['city']), len(town) + 1, E(tc(r['city'])))
        rel += '<div class="box"><h2>From %s</h2><ul class="names">%s</ul>%s</div>' % (E(tc(r['city'])), ''.join(name_li(z, d, '%s · %s' % (rank_full(z['svc'], z['rank']), ldate(z['death']))) for z in town[:10]), more)
    story = ''
    sp = os.path.join(ROOT, 'build/stories/%s.html' % r['slug'])
    if os.path.exists(sp):
        story = '<section class="box prose" style="margin-top:18px"><h2>His story</h2>%s</section>'.replace('His', 'Her' if r['sex'] == 'F' else 'His') % open(sp).read()
    portrait, portrait_attr, photo_credit = FLAG, ' title="No photograph has been shared here yet"', ''
    pp = os.path.join(ROOT, 'build/photos/%s.json' % r['slug'])
    if os.path.exists(pp):
        ph = json.load(open(pp))
        portrait = '<img src="%s" alt="%s" loading="lazy">' % (E(ph['src']), E(r['display']))
        portrait_attr = ''
        photo_credit = 'Photograph: %s' % E(ph.get('credit', ''))
    share = SHARE + '?name=' + r['wall'].replace(' ', '+') + '&panel=' + pn + '&line=' + str(r['line'])
    body = (topbar(d) + '<main class="wrap">'
        '<p class="crumbs"><a href="../../">The Wall</a> &rsaquo; <a href="../../?p=%s">Panel %s</a>%s &rsaquo; %s</p>' % (r['panel'], pn,
            (' &rsaquo; <a href="../../states/%s/">%s</a>' % (r['st'].lower(), E(STATES.get(r['st'], r['st'])))) if r['st'] in STATES else '', E(r['display'])) +
        '<section class="pf-head"><div class="portrait"%s>%s</div><div>'
        '<h1>%s</h1><p class="pf-sub">%s &middot; %s</p><p class="pf-dates">%s%s</p><span class="badge">%s</span></div></section>' % (
            portrait_attr, portrait, E(r['wall']), E(rank), E(svc), (E(ldate(r['birth'])) + ' &ndash; ') if r['birth'] else '', E(ldate(r['death'])), 'Story' if story else 'Service record') +
        (('<p class="note" style="margin:-4px 0 0">%s</p>' % photo_credit) if photo_credit else '') +
        '<p class="lead">%s</p>' % lead(r) + story +
        '<div class="grid2"><div class="box"><h2>On the Wall</h2><p class="where">Panel %s &middot; Line %d</p>'
        '<div class="locator"><img src="../../assets/locator.svg" alt="Position of Panel %s on the Vietnam Veterans Memorial" width="1400" height="160" loading="lazy"><i style="left:%.2f%%;top:%.2f%%"></i></div>'
        '<p class="note">Names are inscribed in the order of loss, starting at Panel 1E at the apex and ending at Panel 1W. At the Memorial, find the panel number at the base and count down from the top line.</p>'
        '<div class="acts"><a class="btn gold" href="../../?p=%s&amp;n=%s">See this name on the Wall</a></div></div>'
        '<div class="box"><h2>Remember</h2><div class="candle" id="candle"><span class="flame"></span><button class="btn" type="button" id="light">Light a candle</button></div>'
        '<p class="note" style="margin-top:10px">Did you know %s? Family members and friends are invited to share a photograph or a memory. Nothing is posted until it has been reviewed.</p>'
        '<div class="acts"><a class="btn gold" href="%s">Share a photo or memory</a><a class="btn" href="%s" rel="noopener" target="_blank">Photos &amp; remembrances on VVMF&rsquo;s Wall of Faces &#8599;</a></div></div></div>' % (
            pn, r['line'], pn, x, y, r['panel'], r['slug'], 'her' if r['sex'] == 'F' else 'him', E(share), E(vvmf(r))) +
        '<div class="grid2"><div class="box"><h2>Service</h2>%s</div><div class="box"><h2>Casualty</h2>%s</div></div>' % (dl(rows), dl(crows)) +
        ('<div class="grid2">%s</div>' % rel if rel else '') +
        '<div class="src"><p><strong>Source.</strong> ' + (('This name was added to the Wall in %s, after the 2008 Department of Defense casualty file used for most of this site was compiled. Panel, line and the details above are as listed for this name on the Vietnam Veterans Memorial Fund&rsquo;s Wall of Faces. ' % (r.get('added') or 'a later year')) if r.get('src') == 'vvmf' else
        'U.S. Department of Defense, Defense Casualty Analysis System, Vietnam Conflict Extract Data File (as of April 29, 2008), '
        'Records of the Office of the Secretary of Defense, Record Group 330, National Archives (NAID 2240992). Panel and line as recorded in that file' + ('; panel and line confirmed against the Vietnam Veterans Memorial Fund&rsquo;s Wall of Faces because the federal record was incomplete' if r['wall'] in fixes else '') + '. ') +
        'This page presents the official record only; no biography has been written for %s yet. See something wrong? <a href="../../about/#corrections">Report a correction</a>.</p></div>'
        '</main>' % ('her' if r['sex'] == 'F' else 'him') +
        '<script type="application/ld+json">%s</script>' % json.dumps(ld) +
        '<script>(function(){var k="candle:%s",c=document.getElementById("candle"),b=document.getElementById("light");function on(){c.classList.add("lit");b.textContent="A candle is lit";b.disabled=true;}'
        'try{if(localStorage.getItem(k))on();}catch(e){}b.onclick=function(){on();try{localStorage.setItem(k,"1")}catch(e){}};})();</script>' % r['slug'] +
        foot(d))
    write('name/%s/index.html' % r['slug'], head(title, desc, 'name/%s/' % r['slug'], d) + body)

todo = R[:LIMIT] if LIMIT else R
for i, r in enumerate(todo):
    profile(r)
print('profiles', len(todo))

# ---------- state pages ----------
by_state = collections.defaultdict(list)
for r in R: by_state[r['st'] or '??'].append(r)
st_list = sorted([s for s in by_state if s in STATES], key=lambda s: STATES[s])
for s in st_list:
    v = sorted(by_state[s], key=lambda r: (r['city'], r['last'], r['given']))
    cities = collections.OrderedDict()
    for r in v: cities.setdefault(r['city'] or 'Hometown not recorded', []).append(r)
    nav = ' &middot; '.join('<a href="#%s">%s</a>' % (slugify(c), E(tc(c))) for c in cities)
    blocks = ''.join('<div class="city" id="%s"><h3>%s <small style="color:var(--dim);font-size:14px">%d</small></h3><ul class="names">%s</ul></div>' % (
        slugify(c), E(tc(c)), len(rs), ''.join(name_li(r, 2, '%s · %s · Panel %s, Line %d' % (rank_full(r['svc'], r['rank']), ldate(r['death']), r['panel'].lstrip('0'), r['line'])) for r in rs)) for c, rs in cities.items())
    name = STATES[s]
    write('states/%s/index.html' % s.lower(), head('%s names on the Vietnam Veterans Memorial (%d) | The Wall' % (name, len(v)),
        'All %d service members from %s whose names are on the Vietnam Veterans Memorial, listed by hometown with panel and line.' % (len(v), name), 'states/%s/' % s.lower(), 2) +
        topbar(2, 'states/') + '<main class="wrap"><p class="crumbs"><a href="../../">The Wall</a> &rsaquo; <a href="../">By state</a> &rsaquo; %s</p>'
        '<h1 style="font-size:40px;margin:10px 0 0">%s</h1><p class="note">%d names, listed by home of record. Select a name for the service record and its place on the Wall.</p>'
        '<p class="note" style="font-size:13px">%s</p>%s</main>' % (E(name), E(name), len(v), nav, blocks) + foot(2))
write('states/index.html', head('Vietnam Veterans Memorial names by state | The Wall', 'Browse the names on the Vietnam Veterans Memorial by state and hometown.', 'states/', 1) +
    topbar(1, 'states/') + '<main class="wrap"><h1 style="font-size:40px;margin:24px 0 4px">Names by state</h1><p class="note">Home of record as listed in the Department of Defense casualty file.</p>'
    '<ul class="list-state">%s</ul></main>' % ''.join('<li><a href="%s/">%s</a> <span style="color:var(--dim)">%s</span></li>' % (s.lower(), E(STATES[s]), format(len(by_state[s]), ',')) for s in st_list) + foot(1))

# ---------- Lake Norman / Charlotte region ----------
REGION = ['MECKLENBURG','IREDELL','CABARRUS','LINCOLN','CATAWBA','GASTON','ROWAN','UNION','STANLY']
reg = sorted([r for r in R if r['st'] == 'NC' and r['county'] in REGION], key=lambda r: (r['county'], r['city'], r['last']))
blocks = ''
for cty in REGION:
    rs = [r for r in reg if r['county'] == cty]
    if not rs: continue
    blocks += '<div class="city" id="%s"><h3>%s County <small style="color:var(--dim);font-size:14px">%d</small></h3><ul class="names">%s</ul></div>' % (
        slugify(cty), E(tc(cty)), len(rs), ''.join(name_li(r, 2, '%s · %s · %s · Panel %s, Line %d' % (tc(r['city']), rank_full(r['svc'], r['rank']), ldate(r['death']), r['panel'].lstrip('0'), r['line'])) for r in rs))
write('local/lake-norman-charlotte/index.html', head('Lake Norman and Charlotte-area names on the Vietnam Veterans Memorial (%d) | The Wall' % len(reg),
    'The %d service members from Mecklenburg, Iredell, Cabarrus, Lincoln, Catawba, Gaston, Rowan, Union and Stanly counties whose names are on the Vietnam Veterans Memorial.' % len(reg), 'local/lake-norman-charlotte/', 2) +
    topbar(2) + '<main class="wrap"><p class="crumbs"><a href="../../">The Wall</a> &rsaquo; <a href="../../states/nc/">North Carolina</a> &rsaquo; Lake Norman &amp; Charlotte area</p>'
    '<h1 style="font-size:40px;margin:10px 0 0">Lake Norman &amp; the Charlotte region</h1><p class="note">%d service members from Mecklenburg, Iredell, Cabarrus, Lincoln, Catawba, Gaston, Rowan, Union and Stanly counties are named on the Vietnam Veterans Memorial, listed here by county of record. Select a name to see the service record and its place on the Wall.</p>%s</main>' % (len(reg), blocks) + foot(2))

# ---------- stats ----------
N = len(R)
cnt = collections.Counter(r['svc'] for r in R)
draft = sum(1 for r in R if r['comp'] == 'SELECTED SERVICE')
ages = [r['age'] for r in R if r['age']]
stats = [(format(N, ','), 'names in this record'), (format(cnt['ARMY'], ','), 'U.S. Army'), (format(cnt['MARINE CORPS'], ','), 'U.S. Marine Corps'),
         (format(cnt['AIR FORCE'], ','), 'U.S. Air Force'), (format(cnt['NAVY'], ','), 'U.S. Navy'), (format(draft, ','), 'were draftees'),
         (str(sorted(ages)[len(ages)//2]), 'median age at death'), (str(sum(1 for r in R if r['sex'] == 'F')), 'women')]
stat_html = ''.join('<div class="stat"><b>%s</b><span>%s</span></div>' % s for s in stats)

# ---------- home / the Wall ----------
home = (head('The Wall — every name on the Vietnam Veterans Memorial | The Lake Norman Brief',
        'Scroll the full Vietnam Veterans Memorial, panel by panel. Hover over a name to read it, and select it to open that service member\'s record and remembrance page.', '', 0) +
    topbar(0, '') +
    '<section class="hero wrap"><h1>The Wall</h1><p>Every name on the Vietnam Veterans Memorial, in the order they were taken from us. Scroll along the Wall, hover over a name and it turns to gold; select it to remember the person behind it.</p></section>'
    '<div class="controls"><div class="wrap"><div class="search"><input id="q" type="search" placeholder="Find a name or hometown…" autocomplete="off" aria-label="Find a name or hometown"><div class="results" id="res" role="listbox"></div></div>'
    '<div class="zoom"><button class="btn" id="zout" aria-label="Zoom out">&minus;</button><input id="zoom" type="range" min="0" max="100" value="0" aria-label="Zoom"><button class="btn" id="zin" aria-label="Zoom in">+</button></div>'
    '<div class="jump"><button class="btn" data-go="70W">West end</button><button class="btn" data-go="01E">Apex &middot; 1959</button><button class="btn" data-go="70E">East end</button></div>'
    '<p class="hint">Drag or scroll to move along the Wall · Ctrl + scroll or the slider to zoom · Hover a name for details, select it to open the page</p></div></div>'
    '<div id="scroller" aria-label="The Vietnam Veterans Memorial, all 140 inscribed panels"><div id="wall"></div></div><div id="tip" role="tooltip"></div>'
    '<main class="wrap"><div class="stats">%s</div>'
    '<div class="intro"><div><h2>How to read the Wall</h2><p>The names begin at the apex, at the top of Panel 1E, with the first deaths in 1959. They continue to the east end at Panel 70E, resume at the far west end at Panel 70W, and return to the apex, ending at the bottom of Panel 1W in 1975. The beginning and the end meet at the center.</p></div>'
    '<div><h2>Each name has a page</h2><p>Select any name to see the official service record: rank and branch, unit, hometown, date and place of loss, and the panel and line where the name is inscribed. Families and friends can share a photograph or a memory, and every submission is reviewed before it appears.</p></div>'
    '<div><h2>Where the records come from</h2><p>The names and records come from the Department of Defense casualty file preserved by the National Archives. Nothing on a name page is invented. When a fuller story has been researched from sources, it will be marked <em>Story</em>; until then, the page is marked <em>Service record</em>. <a href="about/">Read more</a>.</p></div></div>'
    '<p style="margin-top:28px"><a class="btn" href="states/">Browse names by state</a> <a class="btn" href="local/lake-norman-charlotte/">Lake Norman &amp; Charlotte area</a> <a class="btn" href="%s">The Vietnam War on The Lake Norman Brief &rarr;</a></p></main>'
    '<script>window.WALL_META=%s;</script><script src="assets/wall.js?v=%s" defer></script>' % (stat_html, HUB, json.dumps(meta, separators=(',', ':')), V) + foot(0))
write('index.html', home)

# ---------- about ----------
write('about/index.html', head('About this remembrance and its sources | The Wall', 'How The Wall was built, where its records come from, and how to share a photograph or report a correction.', 'about/', 1) + topbar(1, 'about/') +
 '<main class="wrap prose"><h1 style="font-size:40px;margin:24px 0 8px">About this remembrance</h1>'
 '<p>The Vietnam Veterans Memorial in Washington, D.C., designed by Maya Lin and dedicated on November 13, 1982, bears the names of the men and women of the U.S. armed forces who died or remain missing as a result of the Vietnam War. As of 2026, the Wall holds 58,281 names. This site lets you walk the whole Wall from anywhere and stop at any name.</p>'
 '<h2>Where the records come from</h2><p>Every service record on this site comes from the <em>Vietnam Conflict Extract Data File, as of April 29, 2008</em>, produced by the Defense Manpower Data Center from the Defense Casualty Analysis System and preserved by the National Archives (Record Group 330, NAID 2240992). That file lists 58,220 people, with panel and line. The %s names added to the Wall since 2008 were taken from the Vietnam Veterans Memorial Fund&rsquo;s announcements and its Wall of Faces listings, and their pages say so. About two dozen records in the federal file had a missing or malformed panel and line; those were checked one by one against the Wall of Faces. In all, this site lists %s names, against the Memorial&rsquo;s official count of 58,281; if you know of a name that is missing, please tell us.</p>'
 '<p>We have deliberately left out parts of the federal file that do not belong on a memorial page: service numbers (which for this era are often Social Security numbers), race, religion and marital status. For deaths the file classifies as self-inflicted or homicide, the page says &ldquo;died of other causes,&rdquo; following the practice of other memorial sites. Units appear exactly as the military recorded them.</p>'
 '<h2>Order on the Wall</h2><p>On the panorama, names are written the way the Memorial usually inscribes them: first name, middle initial and last name. Name pages give the full name from the service record. Within each line, names are shown by date of loss and then alphabetically. Panel and line come from the record; the position of a name within its line, and the exact spelling or form of an individual inscription, may differ slightly from the stone.</p>'
 '<h2>Photographs and memories</h2><p>Most photographs of the fallen belong to their families. We do not copy them from other sites. A photograph appears on a page only when it is in the public domain (for example, an official military portrait) or when a family member or friend shares it with us and gives permission. Every submission is reviewed before it is posted. To share one, use the <em>Share a photo or memory</em> button on any name page.</p>'
 '<p>The Vietnam Veterans Memorial Fund&rsquo;s <a href="https://www.vvmf.org/Wall-of-Faces/">Wall of Faces</a> has gathered a photograph for nearly every name, along with thousands of remembrances. Every name page here links to it.</p>'
 '<h2 id="corrections">Corrections</h2><p>If you find an error, or if you are a family member who would like a page changed, please write through the <a href="%s">Share a photo or memory</a> form and tell us which name and what should change. We will check it against the record and reply.</p>'
 '<h2>Who made this</h2><p>The Wall is published by <a href="https://lkn-law.com/">The Lake Norman Brief</a>, the history and legal-education site of Adkins Law, PLLC, in Mooresville and Huntersville, North Carolina. It is an independent remembrance and is not affiliated with the Vietnam Veterans Memorial Fund, the National Park Service, or the Department of Defense.</p></main>' % (len(adds), format(N, ','), SHARE) + foot(1))

# ---------- misc ----------
write('404.html', head('Page not found | The Wall', 'Page not found.', '404.html', 0) + topbar(0) + '<main class="wrap" style="padding:60px 16px"><h1>That page was not found</h1><p><a href="/">Return to the Wall</a> or search for a name there.</p></main>' + foot(0).replace('href="about/"', 'href="/about/"'))
write('CNAME', 'wall.lkn-law.com\n')
write('.nojekyll', '')
write('robots.txt', 'User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % BASE)
urls = ['%s/' % BASE, '%s/states/' % BASE, '%s/about/' % BASE] + ['%s/local/lake-norman-charlotte/' % BASE] + ['%s/states/%s/' % (BASE, s.lower()) for s in st_list] + ['%s/name/%s/' % (BASE, r['slug']) for r in R]
chunks = [urls[i:i+40000] for i in range(0, len(urls), 40000)]
for i, c in enumerate(chunks):
    write('sitemap-%d.xml' % (i+1), '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<url><loc>%s</loc></url>' % u for u in c) + '</urlset>')
write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<sitemap><loc>%s/sitemap-%d.xml</loc></sitemap>' % (BASE, i+1) for i in range(len(chunks))) + '</sitemapindex>')
print('names', N, 'panels', len(panels), 'states', len(st_list))
