/* The Wall home page: photo slideshow behind the title, and names remembered today */
(function(){
  var H = window.HERO || [], hero = document.getElementById('hero');
  if (hero && H.length){
    var imgs = [].slice.call(hero.querySelectorAll('img.hs')), cap = document.getElementById('hcap'), dots = document.getElementById('hdots'), i = 0, timer;
    imgs.forEach(function(_, k){ var b = document.createElement('button'); b.setAttribute('aria-label', 'Photograph ' + (k + 1)); b.onclick = function(){ show(k); restart(); }; dots.appendChild(b); });
    function show(k){
      imgs[i].classList.remove('on'); dots.children[i].classList.remove('on');
      i = (k + imgs.length) % imgs.length;
      imgs[i].classList.add('on'); dots.children[i].classList.add('on');
      cap.textContent = H[i][0] + ' Photo: ' + H[i][1] + '.';
    }
    function restart(){ clearInterval(timer); if (!matchMedia('(prefers-reduced-motion: reduce)').matches) timer = setInterval(function(){ show(i + 1); }, 7000); }
    show(0); restart();
    window.addEventListener('scroll', function(){
      var t = Math.min(1, (window.scrollY || 0) / (hero.offsetHeight || 1));
      hero.style.setProperty('--fade', (1 - t * 0.8).toFixed(3)); hero.style.setProperty('--shift', ((window.scrollY || 0) * 0.3).toFixed(1) + 'px');
    }, {passive:true});
  }
  var L = document.getElementById('tdl');
  if (L){
    var M = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    var d = new Date(), key = String(d.getMonth() + 1).padStart(2, '0') + String(d.getDate()).padStart(2, '0');
    document.getElementById('tdh').textContent = 'Lost on ' + M[d.getMonth()] + ' ' + d.getDate();
    document.getElementById('tdall').href = 'on-this-day/#' + key;
    fetch('data/days/' + key + '.json').then(function(r){ return r.ok ? r.json() : []; }).then(function(v){
      v.sort(function(a, b){ return (b[6] - a[6]) || (Math.random() - 0.5); });
      var show = v.slice(0, 12);
      L.innerHTML = show.map(function(x){
        return '<a class="ncard" href="name/' + x[0] + '/"><span class="ncard-t"><b>' + x[1] + (x[6] ? ' <i class="medal" title="Medal of Honor">★</i>' : '') + '</b><small>' + x[3] + ' · ' + x[2] + '</small><small>' + [x[4], x[5]].filter(Boolean).join(', ') + '</small></span></a>';
      }).join('');
      document.getElementById('tdall').textContent = 'All ' + v.length + ' names lost on ' + M[d.getMonth()] + ' ' + d.getDate() + ' →';
    });
  }
})();
