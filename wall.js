(function(){
  'use strict';
  var META = window.WALL_META;               // {panels:[{p:'70W',n:1},...], order:[...], v:'..'}
  var scroller = document.getElementById('scroller');
  var wall = document.getElementById('wall');
  var tip = document.getElementById('tip');
  var zoomIn = document.getElementById('zoom');
  var BR = {A:'U.S. Army',M:'U.S. Marine Corps',F:'U.S. Air Force',N:'U.S. Navy',C:'U.S. Coast Guard'};
  var MAXL = 0, cache = {}, panelEls = {};
  var PROLOGUE = 'In honor of the men and women of the Armed Forces of the United States who served in the Vietnam War. The names of those who gave their lives and of those who remain missing are inscribed in the order they were taken from us.';
  var EPILOGUE = 'Our nation honors the courage, sacrifice and devotion to duty and country of its Vietnam veterans. This memorial was built with private contributions from the American people. November 11, 1982.';
  var INSCR_LINES = 5;

  META.panels.forEach(function(x){ if (x.n > MAXL) MAXL = x.n; });

  // ---------- build panel shells ----------
  META.panels.forEach(function(x, i){
    var el = document.createElement('div');
    el.className = 'panel';
    el.dataset.p = x.p;
    var lines = x.n + ((x.p === '01E' || x.p === '01W') ? INSCR_LINES : 0);
    el.style.height = (lines * 1.42 + 4.2) + 'em';
    if (x.p === '01W') el.classList.add('apex-l');
    var no = document.createElement('div'); no.className = 'pno'; no.textContent = x.p.replace(/^0/, '');
    el.appendChild(no);
    wall.appendChild(el);
    panelEls[x.p] = el;
  });

  function fmtDate(s){ if(!s) return ''; var m=['Jan.','Feb.','March','April','May','June','July','Aug.','Sept.','Oct.','Nov.','Dec.'];
    return m[+s.slice(4,6)-1]+' '+(+s.slice(6,8))+', '+s.slice(0,4); }
  function title(s){ return (s||'').toLowerCase().replace(/(^|[\s-])([a-z])/g,function(a,b,c){return b+c.toUpperCase();}); }

  function load(p){
    if (cache[p]) return cache[p];
    cache[p] = fetch('data/panels/' + p + '.json?v=' + META.v).then(function(r){ return r.json(); });
    return cache[p];
  }

  function render(el){
    if (el.dataset.r) return; el.dataset.r = '1';
    var p = el.dataset.p;
    load(p).then(function(d){
      var frag = document.createDocumentFragment();
      if (p === '01E') frag.appendChild(inscr(PROLOGUE));
      var byLine = {}; d.forEach(function(r){ (byLine[r[2]] = byLine[r[2]] || []).push(r); });
      var n = META.panels.find ? null : null;
      var maxLine = 0; d.forEach(function(r){ if (r[2] > maxLine) maxLine = r[2]; });
      var total = Math.max(maxLine, (META.panels.filter(function(x){return x.p===p;})[0]||{}).n || 0);
      for (var L = 1; L <= total; L++){
        var row = document.createElement('div'); row.className = 'ln';
        var names = byLine[L] || [];
        if (names.length < 2) row.classList.add('one');
        names.forEach(function(r){
          var s = document.createElement('span');
          s.className = 'nm'; s.tabIndex = 0; s.textContent = r[1];
          s.dataset.i = r[0]; s.id = 'n-' + r[0];
          s._r = r;
          row.appendChild(s);
        });
        frag.appendChild(row);
      }
      if (p === '01W') frag.appendChild(inscr(EPILOGUE));
      el.insertBefore(frag, el.firstChild);
      fit(el);
      el.dispatchEvent(new CustomEvent('rendered'));
    });
  }
  function inscr(t){ var d=document.createElement('div'); d.className='inscr'; d.style.height=(INSCR_LINES*1.42)+'em'; d.style.display='flex'; d.style.alignItems='center'; d.textContent=t; return d; }
  function fit(el){
    // shrink any line wider than the panel
    var w = el.clientWidth - parseFloat(getComputedStyle(el).paddingLeft) * 2;
    el.querySelectorAll('.ln').forEach(function(row){
      var sw = 0; for (var c = row.firstChild; c; c = c.nextSibling) sw += c.offsetWidth;
      if (sw > w * 0.985 && sw > 0) row.style.fontSize = Math.max(0.7, (w * 0.98) / sw) + 'em';
    });
  }

  var io = new IntersectionObserver(function(es){
    es.forEach(function(e){ if (e.isIntersecting) render(e.target); });
  }, { root: scroller, rootMargin: '0px 150% 0px 150%' });
  Object.keys(panelEls).forEach(function(k){ io.observe(panelEls[k]); });

  // ---------- zoom ----------
  var fs = 6;
  function fitFs(){ var h = scroller.clientHeight - 40; return Math.max(2.2, h / ((MAXL) * 1.42 + 4.2)); }
  function setFs(v, cx, cy){
    var old = fs; fs = Math.max(fitFs(), Math.min(26, v));
    var rect = scroller.getBoundingClientRect();
    cx = cx == null ? rect.width / 2 : cx; cy = cy == null ? rect.height / 2 : cy;
    var ax = (scroller.scrollLeft + cx), ay = (scroller.scrollTop + cy);
    var padL = window.innerWidth * 0.4;
    var k = fs / old;
    wall.style.fontSize = fs + 'px';
    wall.classList.toggle('engr', fs >= 9);
    scroller.scrollLeft = (ax - padL) * k + padL - cx;
    scroller.scrollTop = Math.max(0, (ay - 22) * k + 22 - cy);
    zoomIn.value = String(Math.round(Math.log(fs / fitFs()) / Math.log(26 / fitFs()) * 100));
    clearTimeout(setFs.t); setFs.t = setTimeout(function(){
      wall.querySelectorAll('.panel[data-r]').forEach(function(el){ el.querySelectorAll('.ln').forEach(function(r){ r.style.fontSize=''; }); fit(el); });
    }, 250);
  }
  zoomIn.addEventListener('input', function(){
    var f0 = fitFs(); setFs(f0 * Math.pow(26 / f0, zoomIn.value / 100));
  });
  document.getElementById('zin').onclick = function(){ setFs(fs * 1.5); };
  document.getElementById('zout').onclick = function(){ setFs(fs / 1.5); };
  scroller.addEventListener('wheel', function(e){
    if (e.ctrlKey || e.metaKey){ e.preventDefault(); var r = scroller.getBoundingClientRect(); setFs(fs * (e.deltaY < 0 ? 1.15 : 1/1.15), e.clientX - r.left, e.clientY - r.top); }
    else if (Math.abs(e.deltaY) > Math.abs(e.deltaX) && fs <= fitFs() * 1.05){ e.preventDefault(); scroller.scrollLeft += e.deltaY; }
  }, { passive: false });

  // drag to pan
  var drag = null;
  scroller.addEventListener('pointerdown', function(e){ if (e.pointerType !== 'mouse' || e.button !== 0) return; drag = {x:e.clientX, y:e.clientY, l:scroller.scrollLeft, t:scroller.scrollTop, moved:false}; });
  window.addEventListener('pointermove', function(e){ if (!drag) return; var dx=e.clientX-drag.x, dy=e.clientY-drag.y;
    if (Math.abs(dx)+Math.abs(dy) > 4){ drag.moved = true; scroller.classList.add('drag'); }
    if (drag.moved){ scroller.scrollLeft = drag.l - dx; scroller.scrollTop = drag.t - dy; } });
  window.addEventListener('pointerup', function(){ setTimeout(function(){ drag = null; scroller.classList.remove('drag'); }, 0); });

  // ---------- tooltip / click ----------
  var touch = false, armed = null;
  function card(r){
    var bits = [r[3] + ' · ' + (BR[r[4]] || '')];
    var home = [title(r[5]), r[6]].filter(Boolean).join(', ');
    tip.innerHTML = '<b></b><span></span><span></span><em></em>';
    tip.children[0].textContent = r[1];
    tip.children[1].textContent = bits[0];
    tip.children[2].textContent = (home ? home + ' · ' : '') + fmtDate(r[7]);
    tip.children[3].textContent = 'Panel ' + r[8] + ', Line ' + r[2] + (touch ? '' : ' · click to remember');
    if (touch){ var a=document.createElement('a'); a.className='btn gold'; a.style.marginTop='8px'; a.href='name/'+r[0]+'/'; a.textContent='Open his or her page'; if(r[9]==='F') a.textContent='Open her page'; else a.textContent='Open his page'; tip.appendChild(a); }
  }
  function place(x, y){
    var w = tip.offsetWidth, h = tip.offsetHeight;
    var L = Math.min(window.innerWidth - w - 10, x + 16), T = y + 18;
    if (T + h > window.innerHeight - 10) T = y - h - 14;
    tip.style.left = Math.max(10, L) + 'px'; tip.style.top = Math.max(10, T) + 'px';
  }
  wall.addEventListener('pointerover', function(e){
    if (e.pointerType !== 'mouse') return;
    var t = e.target.closest('.nm'); if (!t) return;
    touch = false; card(t._r); tip.classList.remove('touch'); tip.classList.add('on'); place(e.clientX, e.clientY);
  });
  wall.addEventListener('pointermove', function(e){ if (e.pointerType === 'mouse' && tip.classList.contains('on')) place(e.clientX, e.clientY); });
  wall.addEventListener('pointerout', function(e){ if (e.pointerType === 'mouse' && e.target.closest('.nm')) tip.classList.remove('on'); });
  wall.addEventListener('click', function(e){
    var t = e.target.closest('.nm'); if (!t) return;
    if (drag && drag.moved) return;
    if (e.pointerType && e.pointerType !== 'mouse' || matchMedia('(hover: none)').matches){
      if (armed !== t){ e.preventDefault(); armed && armed.classList.remove('hl'); armed = t; t.classList.add('hl');
        touch = true; card(t._r); tip.classList.add('on','touch'); place(e.clientX, e.clientY); return; }
    }
    location.href = 'name/' + t._r[0] + '/';
  });
  wall.addEventListener('keydown', function(e){ var t = e.target.closest('.nm'); if (t && e.key === 'Enter') location.href = 'name/' + t._r[0] + '/'; });
  wall.addEventListener('focusin', function(e){ var t = e.target.closest('.nm'); if (!t) return; touch=false; card(t._r); var r=t.getBoundingClientRect(); tip.classList.add('on'); place(r.left, r.bottom); });
  scroller.addEventListener('scroll', function(){ if (!touch) tip.classList.remove('on'); }, {passive:true});
  document.addEventListener('click', function(e){ if (touch && !e.target.closest('.nm') && !e.target.closest('#tip')){ tip.classList.remove('on','touch'); armed && armed.classList.remove('hl'); armed=null; } });

  // ---------- navigation ----------
  function centerOn(el, smooth){
    var r = el.getBoundingClientRect(), s = scroller.getBoundingClientRect();
    scroller.scrollTo({ left: scroller.scrollLeft + r.left - s.left - s.width / 2 + r.width / 2,
                        top: scroller.scrollTop + r.top - s.top - s.height / 2 + r.height / 2, behavior: smooth ? 'smooth' : 'auto' });
  }
  function goPanel(p, smooth){ var el = panelEls[p]; if (!el) return; var r = el.getBoundingClientRect(), s = scroller.getBoundingClientRect();
    scroller.scrollTo({ left: scroller.scrollLeft + r.left - s.left - (p==='01W'? s.width - r.width - 20 : (p==='01E'? 20 : s.width/2 - r.width/2)), top: 0, behavior: smooth ? 'smooth' : 'auto' }); }
  function findName(slug, panel){
    var el = panelEls[panel]; if (!el) return;
    if (fs < 13) setFs(14);
    var go = function(){ var n = document.getElementById('n-' + slug); if (!n) return;
      wall.querySelectorAll('.found').forEach(function(x){ x.classList.remove('found'); });
      n.classList.add('found'); centerOn(n, true); };
    if (el.dataset.r && document.getElementById('n-' + slug)) go();
    else { el.addEventListener('rendered', function h(){ el.removeEventListener('rendered', h); setTimeout(go, 30); }); render(el); }
  }
  window.WALL = { findName: findName, goPanel: goPanel };
  document.querySelectorAll('[data-go]').forEach(function(b){ b.onclick = function(){ if (fs > fitFs()*1.6) setFs(fitFs()); goPanel(b.dataset.go, true); }; });

  // ---------- search ----------
  var q = document.getElementById('q'), res = document.getElementById('res'), idx = null, idxP = null, sel = -1;
  function getIdx(){ if (!idxP) idxP = fetch('data/index.json?v=' + META.v).then(function(r){ return r.json(); }).then(function(d){ idx = d; return d; }); return idxP; }
  q.addEventListener('focus', getIdx);
  function norm(s){ return s.toUpperCase().replace(/[^A-Z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim(); }
  function search(){
    var v = norm(q.value); if (v.length < 2){ res.classList.remove('open'); return; }
    getIdx().then(function(d){
      var toks = v.split(' '), out = [];
      for (var i = 0; i < d.length && out.length < 40; i++){
        var r = d[i], hay = r[1] + ' ' + (r[7] || '') + ' ' + r[2] + ' ' + r[3];
        var ok = true; for (var j = 0; j < toks.length; j++){ if (hay.indexOf(toks[j]) < 0){ ok = false; break; } }
        if (ok) out.push(r);
      }
      res.innerHTML = ''; sel = -1;
      if (!out.length){ res.innerHTML = '<button disabled>No names found. Try a last name or a hometown.</button>'; }
      out.forEach(function(r){
        var b = document.createElement('button'); b.type = 'button';
        b.textContent = r[1]; var sm = document.createElement('small');
        sm.textContent = [title(r[2]), r[3]].filter(Boolean).join(', ') + ' · ' + r[5] + ' · Panel ' + r[4] + ', Line ' + r[6];
        b.appendChild(sm);
        b.onclick = function(){ res.classList.remove('open'); q.value = r[1]; history.replaceState(null, '', '?p=' + r[4] + '&n=' + r[0]); findName(r[0], r[4]); };
        res.appendChild(b);
      });
      res.classList.add('open');
    });
  }
  var st; q.addEventListener('input', function(){ clearTimeout(st); st = setTimeout(search, 140); });
  q.addEventListener('keydown', function(e){
    var bs = res.querySelectorAll('button:not([disabled])'); if (!bs.length) return;
    if (e.key === 'ArrowDown'){ sel = Math.min(bs.length - 1, sel + 1); }
    else if (e.key === 'ArrowUp'){ sel = Math.max(0, sel - 1); }
    else if (e.key === 'Enter'){ (bs[sel] || bs[0]).click(); return; }
    else if (e.key === 'Escape'){ res.classList.remove('open'); return; } else return;
    e.preventDefault(); bs.forEach(function(b, i){ b.classList.toggle('sel', i === sel); }); bs[sel] && bs[sel].scrollIntoView({block:'nearest'});
  });
  document.addEventListener('click', function(e){ if (!e.target.closest('.search')) res.classList.remove('open'); });

  // ---------- start ----------
  function start(){
    setFs(fitFs());
    var u = new URLSearchParams(location.search);
    if (u.get('n') && u.get('p')) { goPanel(u.get('p')); findName(u.get('n'), u.get('p')); }
    else if (u.get('p')) goPanel(u.get('p'));
    else { var a = panelEls['01E']; var s = scroller.getBoundingClientRect(); scroller.scrollLeft = a.offsetLeft - s.width / 2; }
  }
  window.addEventListener('resize', function(){ if (fs < fitFs()) setFs(fitFs()); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(start); else start();
})();
