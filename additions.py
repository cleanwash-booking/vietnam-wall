"""Merge VVMF lookups: panel/line fixes for DCAS records, and names added to the Wall after the 2008 DCAS file."""
import json, os, re
B = os.path.dirname(__file__)
fixes = json.load(open(os.path.join(B, 'panel_fixes.json')))
for line in open(os.path.join(B, 'vvmf_fix.tsv')):
    if not line.strip(): continue
    n, pl = line.rstrip('\n').split('\t')
    fixes[n] = pl
json.dump(fixes, open(os.path.join(B, 'panel_fixes.json'), 'w'), indent=1)

years = {}
for l in open(os.path.join(B, 'adds_src.txt')):
    y, n, pl, rk = l.strip().split('|'); years[n.upper().replace(',', '')] = y
SVC = {'ARMY': 'A', 'MARINE CORPS': 'M', 'AIR FORCE': 'F', 'NAVY': 'N', 'COAST GUARD': 'C'}
STATE_NAMES = {}
for r in json.load(open(os.path.join(B, 'records.json'))):
    if r['st'] and r['state']: STATES = STATE_NAMES.setdefault(r['st'], r['state'])
RANKFIX = {('ARMY', 'SSGT'): 'SSG', ('MARINE CORPS', 'GSGT'): 'GYSGT'}
def iso(d):
    m = re.match(r'(\d\d)/(\d\d)/(\d{4})', d or '')
    return '%s-%s-%s' % (m.group(3), m.group(1), m.group(2)) if m else None
out = []
for line in open(os.path.join(B, 'vvmf_adds.tsv')):
    if not line.strip(): continue
    n, pl, dob, prov, doc, city, county, st, br, rank = line.rstrip('\n').split('|')
    t = n.split(); suf = t.pop() if t[-1] in ('JR', 'SR', 'II', 'III', 'IV') else ''
    last = t[-1]; given = ' '.join(t[:-1])
    p, ln = pl.split('/')
    b, d = iso(dob), iso(doc)
    age = None
    if b and d:
        by, bm, bd = map(int, b.split('-')); dy, dm, dd = map(int, d.split('-'))
        age = dy - by - ((dm, dd) < (bm, bd))
    disp = ' '.join(w.capitalize() for w in (given + ' ' + last).split()) + (' ' + suf if suf else '')
    out.append(dict(wall=n, last=last, given=given, suf=suf, display=disp, comp='', svc=br, svc_code=SVC.get(br, ''),
        rank=RANKFIX.get((br, rank), rank), pg='', mos='', mos_desc='', birth=b, sex='M', city=city, county=county, st=st,
        state=STATE_NAMES.get(st, ''), prov=prov if prov not in ('UNKNOWN', 'LZ') else '', country='', unit='', death=d, year=(d or '')[:4],
        op='', loc='', aircraft='', hostile='', cat='', reason='', body='', closure='', inc_cat='', inc_date=None, inc_short='',
        panel='%02d%s' % (int(p[:-1]), p[-1]), line=int(ln), age=age, raw_panel=pl, src='vvmf', added=years.get(n, '')))
json.dump(out, open(os.path.join(B, 'additions.json'), 'w'), indent=0)
print('fixes', len(fixes), 'additions', len(out))
