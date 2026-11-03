import json, re, collections, datetime
RAW='raw/DCAS.VN.EXT08.DAT'
SURNAME2={'DELA','SANTA','TEN','VANDER'}
SUFFIX={'JR','SR','II','III','IV'}
def split_name(n):
    t=n.split()
    k=2 if t[0] in SURNAME2 and len(t)>2 else 1
    last=t[:k]; rest=t[k:]
    suf=[]
    if rest and rest[-1] in SUFFIX: suf=[rest[-1]]; rest=rest[:-1]
    return ' '.join(last), ' '.join(rest), ' '.join(suf)
def tc(s):
    out=[]
    for w in s.split(' '):
        parts=[]
        for p in w.split('-'):
            if p in SUFFIX: parts.append(p); continue
            q=p.capitalize()
            if re.match(r'^MC[A-Z]{2,}',p): q='Mc'+p[2:].capitalize()
            parts.append(q)
        out.append('-'.join(parts))
    return ' '.join(out)
def fixpanel(p):
    p=p.strip()
    m=re.match(r'^(\d{1,2})([EW])\s+(\d{1,3})$',p)
    if not m: return None
    return '%02d%s'%(int(m.group(1)),m.group(2)), int(m.group(3))
def d(s):
    s=s.strip()
    if len(s)!=8 or not s.isdigit(): return None
    try: return datetime.date(int(s[:4]),int(s[4:6]),int(s[6:]))
    except: return None
recs=[]; missing=[]
for line in open(RAW,encoding='latin-1'):
    if not line.strip(): continue
    r=[x.strip() for x in line.rstrip('\r\n').split('|')]
    last,given,suf=split_name(r[4])
    wall=' '.join(x for x in [given,last,suf] if x)
    pl=fixpanel(r[49])
    b=d(r[11]); dd=d(r[34])
    age=None
    if b and dd: age=dd.year-b.year-((dd.month,dd.day)<(b.month,b.day))
    rec=dict(wall=wall, last=last, given=given, suf=suf, display=tc(' '.join(x for x in [given,last] if x))+(' '+suf if suf else ''),
      comp=r[3], svc=r[6], svc_code=r[5], rank=r[7], pg=r[8], mos=r[9], mos_desc=r[10].strip('"'), birth=b.isoformat() if b else None,
      sex=r[12], city=r[13], county=r[14], st=r[16], state=r[17], prov=r[26], country=r[30], unit=r[31],
      death=dd.isoformat() if dd else None, year=r[35], op=r[38], loc=r[39], aircraft=r[41] or r[54],
      hostile=r[42], cat=r[44], reason=r[45], body=r[47], closure=r[48], inc_cat=r[50], inc_date=(d(r[51]).isoformat() if d(r[51]) else None), inc_short=r[52],
      panel=pl[0] if pl else None, line=pl[1] if pl else None, age=age, raw_panel=r[49])
    if not pl: missing.append(rec)
    recs.append(rec)
# order: panel/line, then death date, then surname
json.dump(recs,open('build/records.json','w'))
json.dump([{k:m[k] for k in ('wall','death','cat','city','st','raw_panel','svc')} for m in missing],open('build/missing_panel.json','w'),indent=1)
print(len(recs),'missing panel',len(missing))
print(collections.Counter(r['age'] for r in recs).most_common(5), min(r['age'] for r in recs if r['age'] is not None), max(r['age'] for r in recs if r['age'] is not None))
print(sum(1 for r in recs if r['age'] is None))
