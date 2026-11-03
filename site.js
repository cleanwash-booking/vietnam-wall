/* The Wall: shared page behaviour — photo lightbox and gentle scroll fade */
(function(){
  var bands = [].slice.call(document.querySelectorAll('.pf-bg, .band'));
  function onScroll(){
    var y = window.scrollY || 0;
    bands.forEach(function(b){
      var h = b.offsetHeight || 1, t = Math.min(1, Math.max(0, y / h));
      b.style.setProperty('--fade', (1 - t * 0.75).toFixed(3));
      b.style.setProperty('--shift', (y * 0.25).toFixed(1) + 'px');
    });
  }
  if (bands.length && !matchMedia('(prefers-reduced-motion: reduce)').matches){ window.addEventListener('scroll', onScroll, {passive:true}); onScroll(); }

  var box;
  function open(src, cap){
    if (!box){
      box = document.createElement('div'); box.className = 'lb'; box.setAttribute('role','dialog'); box.setAttribute('aria-modal','true');
      box.innerHTML = '<button class="lb-x" aria-label="Close">&times;</button><div class="lb-stage"><img alt=""></div><p class="lb-cap"></p><p class="lb-hint">Scroll or pinch to zoom · drag to move · Esc to close</p>';
      document.body.appendChild(box);
      var img = box.querySelector('img'), z = 1, x = 0, y0 = 0, drag = null;
      function apply(){ img.style.transform = 'translate(' + x + 'px,' + y0 + 'px) scale(' + z + ')'; }
      box._reset = function(){ z = 1; x = 0; y0 = 0; apply(); };
      box.addEventListener('wheel', function(e){ e.preventDefault(); z = Math.min(5, Math.max(1, z * (e.deltaY < 0 ? 1.15 : 0.87))); if (z === 1){ x = 0; y0 = 0; } apply(); }, {passive:false});
      img.addEventListener('dblclick', function(){ z = z > 1 ? 1 : 2.5; if (z === 1){ x = 0; y0 = 0; } apply(); });
      img.addEventListener('pointerdown', function(e){ drag = [e.clientX - x, e.clientY - y0]; img.setPointerCapture(e.pointerId); });
      img.addEventListener('pointermove', function(e){ if (drag && z > 1){ x = e.clientX - drag[0]; y0 = e.clientY - drag[1]; apply(); } });
      img.addEventListener('pointerup', function(){ drag = null; });
      box.addEventListener('click', function(e){ if (e.target === box || e.target.classList.contains('lb-x') || e.target.classList.contains('lb-stage')) close(); });
      document.addEventListener('keydown', function(e){ if (e.key === 'Escape') close(); });
    }
    box._reset(); box.querySelector('img').src = src; box.querySelector('.lb-cap').textContent = cap || '';
    box.classList.add('on'); document.documentElement.style.overflow = 'hidden'; box.querySelector('.lb-x').focus();
  }
  function close(){ if (box){ box.classList.remove('on'); document.documentElement.style.overflow = ''; } }
  function hook(el, src, cap){
    el.addEventListener('click', function(e){ if (e.target.closest('a')) return; open(src(), cap()); });
    el.addEventListener('keydown', function(e){ if (e.key === 'Enter' || e.key === ' '){ e.preventDefault(); open(src(), cap()); } });
  }
  [].forEach.call(document.querySelectorAll('.pf-bg'), function(f){
    hook(f, function(){ return f.getAttribute('data-full'); }, function(){ return f.querySelector('figcaption').textContent; });
  });
  [].forEach.call(document.querySelectorAll('.band'), function(f){
    var im = f.querySelector('img'); f.setAttribute('tabindex', '0');
    hook(f, function(){ return im.currentSrc.replace(/w=\d+/, 'w=2200'); }, function(){ var c = f.querySelector('.band-cap'); return c ? c.textContent : ''; });
  });
  [].forEach.call(document.querySelectorAll('.portrait img'), function(im){
    im.style.cursor = 'zoom-in';
    im.addEventListener('click', function(){ open(im.src.replace(/\/(\d+)px-/, '/800px-'), im.alt); });
  });
})();
