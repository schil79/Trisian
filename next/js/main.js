/* Trisian home and secondary pages: the motion layer. No libraries.
   CSS draws; this file adds classes and numbers, and runs one rAF loop for everything tied to scroll.
   Under prefers-reduced-motion: no loops, no counters, no parallax, no scroll-linked scaling, no word reveals.
   Every graphic is left in its final state. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasIO = 'IntersectionObserver' in window;
  const ease = t => 1 - Math.pow(1 - t, 3);                         // ease-out cubic
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const wait = ms => new Promise(r => setTimeout(r, ms));

  const watch = (els, cb, threshold = 0.15) => {
    if (!hasIO) { els.forEach(e => cb(e)); return; }
    const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { cb(en.target); io.unobserve(en.target); } }), { threshold });
    els.forEach(e => io.observe(e));
  };

  /* ---------- enter-view: reveals, staggers, word splits, anim containers ---------- */
  $$('[data-stagger]').forEach(g => [...g.children].forEach((c, i) => c.style.setProperty('--i', i)));
  $$('[data-split]').forEach(el => {
    const words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words.map((w, i) => `<span class="w" style="--i:${i}"><span>${w}</span></span>`).join(' ');
  });
  watch($$('[data-reveal],[data-stagger],[data-split],.vs-mid'), e => { e.classList.add('in'); if (e.hasAttribute('data-stagger')) setTimeout(() => e.classList.add('settled'), 1500); }, 0.12);
  watch($$('.anim:not(#hpanel),[data-viz]'), e => e.classList.add('in'), 0.35);

  /* ---------- hero: fit the line to 75% of the viewport width ----------
     This routine only sets font-size on #h1. It measures the rendered line at a 100px probe size, then scales.
     Desktop: one line. Under 768px the line breaks into two and the wider one fills 75vw (minimum 44px). */
  const hero = $('.hero'), h1 = $('#h1');
  const fit = () => {
    if (!h1) return;
    const box = $('.h1-fit', h1), target = document.documentElement.clientWidth * 0.75;
    h1.style.fontSize = '100px';
    const w = innerWidth < 768 ? Math.max(...[...box.children].map(c => c.getBoundingClientRect().width)) : box.getBoundingClientRect().width;
    h1.style.fontSize = Math.max(44, 100 * target / w).toFixed(2) + 'px';
    h1.classList.add('fit');
  };
  if (hero) {
    fit();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
    let rt; addEventListener('resize', () => { cancelAnimationFrame(rt); rt = requestAnimationFrame(fit); });
    requestAnimationFrame(() => requestAnimationFrame(() => hero.classList.add('go')));
  }
  const hs = $('#hsteps');
  if (hs) { if (reduce) hs.classList.add('go'); else watch([hs], e => e.classList.add('go'), 0.3); }
  const versus = $('#versus');
  if (versus) { if (reduce) versus.classList.add('go'); else watch([versus], e => e.classList.add('go'), 0.35); }
  const hp = $('#hpanel');
  if (hp) {
    if (reduce) hp.classList.add('play', 'done');
    else watch([hp], e => { e.classList.add('play'); setTimeout(() => e.classList.add('done'), 2900); }, 0.3);
  }

  /* ---------- counters (receipts), run once ---------- */
  const grid = $('#rcGrid');
  if (grid && !reduce) {
    const nums = $$('[data-count]', grid);
    nums.forEach(n => { n.textContent = '0'; });
    watch([grid], () => {
      const t0 = performance.now();
      const tick = now => {
        const p = Math.min(1, (now - t0) / 1200);
        nums.forEach(n => { n.textContent = Math.round(ease(p) * +n.dataset.count); });
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }, 0.5);
  }

  /* ---------- certificate row: about 60px per second ---------- */
  const certSet = $('.cert-set');
  if (certSet && !reduce) {
    const speed = () => { const w = certSet.getBoundingClientRect().width; if (w) $('.cert-track').style.setProperty('--mq-dur', (w / 60).toFixed(1) + 's'); };
    speed(); if (document.fonts && document.fonts.ready) document.fonts.ready.then(speed); addEventListener('resize', speed);
  }

  /* ---------- desktop pool (answer 1): check in, use, check out, reset, loop while in view ---------- */
  const pool = $('#pool');
  if (pool) {
    const tiles = $$('.pt', pool), cols = 6, gridEl = $('#poolGrid'), clock = $('#poolClock'), status = $('#poolStatus'), steps = $$('#poolSteps li');
    const setStep = k => steps.forEach(s => s.classList.toggle('on', s.dataset.s === k));
    const fmt = m => { m = Math.round(m) % 1440; return String(Math.floor(m / 60)).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0'); };
    const showReset = () => { tiles.forEach(t => { t.classList.remove('on', 'cursor', 'flash'); t.classList.add('rs'); }); clock.textContent = '00:00'; status.textContent = 'Reset 100%'; setStep('rs'); pool.dataset.phase = 'reset'; };
    if (reduce) showReset();
    else {
      let alive = false, token = 0;
      const run = async () => {
        const my = ++token;
        const live = () => alive && my === token;
        const tween = (a, b, ms) => new Promise(res => { const t0 = performance.now(); const f = n => { if (!live()) return res(); const p = clamp((n - t0) / ms); clock.textContent = fmt(a + (b - a) * p); p < 1 ? requestAnimationFrame(f) : res(); }; requestAnimationFrame(f); });
        while (live()) {
          // idle
          tiles.forEach(t => t.classList.remove('on', 'cursor', 'rs', 'flash'));
          pool.dataset.phase = 'idle'; clock.textContent = '14:14'; setStep(''); status.textContent = 'Desktops idle.';
          await wait(900); if (!live()) break;
          // check in
          setStep('in'); status.textContent = 'People checking in.';
          const order = [...tiles.keys()].sort(() => Math.random() - .5);
          const tw1 = tween(14 * 60 + 14, 16 * 60 + 40, 1800);
          for (const i of order) { if (!live()) break; tiles[i].classList.add('on'); await wait(70); }
          await tw1; if (!live()) break;
          // use
          setStep('use'); status.textContent = 'Users at work.';
          const tw2 = tween(16 * 60 + 40, 24 * 60 - 1, 3400);
          let cur = null;
          const cursorTimer = setInterval(() => { if (cur) cur.classList.remove('cursor'); cur = tiles[Math.floor(Math.random() * tiles.length)]; cur.classList.add('cursor'); }, 650);
          await tw2; clearInterval(cursorTimer); if (cur) cur.classList.remove('cursor'); if (!live()) break;
          // check out
          setStep('out'); status.textContent = 'Checking out.'; clock.textContent = '23:59'; await wait(900); if (!live()) break;
          // reset: a sweep line crosses the pool, each tile flashes, clears, and goes dashed
          setStep('rs'); status.textContent = 'Resetting.'; clock.textContent = '00:00';
          pool.style.setProperty('--gw', (gridEl.clientWidth - 3) + 'px');
          pool.dataset.phase = 'sweep';
          tiles.forEach((t, i) => { const c = i % cols; setTimeout(() => { if (!live()) return; t.classList.add('flash'); setTimeout(() => { t.classList.remove('on', 'flash'); t.classList.add('rs'); }, 120); }, (c + .5) / cols * 1400); });
          await wait(1700); if (!live()) break;
          pool.dataset.phase = 'reset'; status.textContent = 'Reset 100%';
          await wait(3200);
        }
      };
      // start and stop with visibility
      if (hasIO) new IntersectionObserver(es => { alive = es[0].isIntersecting; if (alive) run(); else token++; }, { threshold: 0.35 }).observe(pool);
    }
  }

  /* ---------- mini pool inside the nightly reset tile: once, on entry ---------- */
  const mini = $('#miniPool');
  if (mini) {
    const mt = $$('.mt', mini);
    if (reduce) mt.forEach(t => t.classList.add('rs'));
    else watch([mini], async () => {
      for (const t of mt) { t.classList.add('on'); await wait(60); }
      await wait(500);
      mini.dataset.phase = 'sweep';
      const sw = $('.sweep', mini); const w = mini.clientWidth;
      sw.style.cssText = `opacity:.9;transition:transform 1s linear;transform:translateX(${w}px)`;
      mt.forEach((t, i) => setTimeout(() => { t.classList.remove('on'); t.classList.add('rs'); }, (i % 3 + .5) / 3 * 1000));
      setTimeout(() => { sw.style.opacity = 0; }, 1100);
    }, 0.6);
  }

  /* ---------- magnetic buttons ---------- */
  if (!reduce && matchMedia('(hover:hover)').matches) {
    $$('[data-magnet]').forEach(b => {
      b.addEventListener('pointermove', e => {
        const r = b.getBoundingClientRect();
        b.style.translate = `${((e.clientX - r.left - r.width / 2) * .14).toFixed(1)}px ${((e.clientY - r.top - r.height / 2) * .22).toFixed(1)}px`;
      });
      b.addEventListener('pointerleave', () => { b.style.translate = ''; });
    });
  }

  /* ---------- isometric icons: one rule for all 68 (Directive v3 section 6) ----------
     Entry once (60ms stagger per icon in a group, capped at 6), ambient float only while the host is on screen,
     cursor lean through one delegated pointer handler (capped at 6px), a one-off lift on tap for touch.
     Under reduced motion none of this runs and the icons simply appear. */
  const hosts = $$('[data-ico-host]');
  hosts.forEach((h, n) => {
    const group = h.parentElement, sibs = [...group.children].filter(c => c.hasAttribute('data-ico-host'));
    const i = Math.min(sibs.indexOf(h), 5);
    h.style.setProperty('--gi', i);
    $$('.ico', h).forEach(ic => { ic.style.setProperty('--i', i); ic.style.setProperty('--fi', n % 12); });
  });
  if (hosts.length) {
    if (!hasIO || reduce) hosts.forEach(h => h.classList.add('is-in'));
    else {
      const io = new IntersectionObserver(es => es.forEach(en => {
        en.target.classList.toggle('is-live', en.isIntersecting);
        if (en.isIntersecting && !en.target.classList.contains('is-in')) { en.target.classList.add('is-in'); setTimeout(() => en.target.classList.add('done'), 900); }
      }), { threshold: 0.2 });
      hosts.forEach(h => io.observe(h));
    }
  }
  if (!reduce && matchMedia('(hover:hover) and (pointer:fine)').matches) {
    let cur = null, px = 0, py = 0, raf = 0;
    const apply = () => {
      raf = 0;
      if (cur) $$('.ico', cur).forEach(ic => { ic.style.setProperty('--px', px.toFixed(3)); ic.style.setProperty('--py', py.toFixed(3)); });
    };
    const reset = h => { if (h) $$('.ico', h).forEach(ic => { ic.style.setProperty('--px', 0); ic.style.setProperty('--py', 0); }); };
    document.addEventListener('pointermove', e => {
      const h = e.target.closest && e.target.closest('[data-ico-host]');
      if (h !== cur) { reset(cur); cur = h; }
      if (!h) return;
      const r = h.getBoundingClientRect();
      px = clamp(((e.clientX - r.left) / r.width) * 2 - 1, -1, 1);
      py = clamp(((e.clientY - r.top) / r.height) * 2 - 1, -1, 1);
      if (!raf) raf = requestAnimationFrame(apply);
    }, { passive: true });
    document.addEventListener('pointerleave', () => { reset(cur); cur = null; });
  } else if (!reduce) {
    document.addEventListener('pointerdown', e => {
      if (e.pointerType !== 'touch') return;
      const h = e.target.closest && e.target.closest('[data-ico-host]');
      if (!h) return;
      h.classList.add('is-tap'); setTimeout(() => h.classList.remove('is-tap'), 450);
    }, { passive: true });
  }

  /* ---------- one loop for everything tied to scroll ---------- */
  const navWrap = $('#navWrap'), intro = $('#ansIntro'), introIn = intro && $('.ans-intro-in', intro);
  const ans = $$('[data-ans]'), steps = $('#steps'), parallax = $$('[data-parallax]'), pimgs = $$('[data-parallax-img]');
  const navLinks = $$('.nav-links a').filter(a => /#(answers|seats|offer)$/.test(a.getAttribute('href') || ''));
  const secs = { answers: $('#answers'), offer: null };
  const secOf = id => (id === 'answers' ? [$('#answers'), $('#receipts')] : id === 'seats' ? [$('#seats')] : [$('#offer'), $('#six')]).filter(Boolean);
  let queued = false;
  const frame = () => {
    queued = false;
    const y = scrollY, H = innerHeight, max = document.documentElement.scrollHeight - H;
    if (navWrap) { navWrap.classList.toggle('scrolled', y > 8); navWrap.style.setProperty('--sp', max > 0 ? (y / max).toFixed(4) : 0); }
    navLinks.forEach(a => {
      const id = a.getAttribute('href').split('#')[1];
      const on = secOf(id).some(s => { const r = s.getBoundingClientRect(); return r.top < H * .4 && r.bottom > H * .4; });
      a.classList.toggle('is-here', on);
    });
    if (reduce) return;
    if (intro) { const r = intro.getBoundingClientRect(); const q = clamp(-r.top / r.height); introIn.style.setProperty('--is', (1 - .1 * q).toFixed(3)); introIn.style.setProperty('--io', (1 - 1.1 * q).toFixed(3)); }
    ans.forEach(a => { const r = a.getBoundingClientRect(); a.style.setProperty('--p', clamp((H * .98 - r.top) / (H * .5)).toFixed(3)); });
    if (steps) {
      const r = steps.getBoundingClientRect();
      steps.style.setProperty('--sp', clamp((H * .6 - r.top) / r.height).toFixed(3));
      $$('.step', steps).forEach(s => s.classList.toggle('here', s.getBoundingClientRect().top < H * .6));
    }
    parallax.forEach(el => { const r = el.getBoundingClientRect(); if (r.bottom < -100 || r.top > H + 100) return; const f = +el.dataset.parallax; el.style.transform = `translateY(${(((r.top + r.height / 2) - H / 2) * -f).toFixed(1)}px)`; });
    pimgs.forEach(im => { const c = im.parentElement.getBoundingClientRect(); if (c.bottom < -100 || c.top > H + 100) return; im.style.transform = `translateY(${clamp(((c.top + c.height / 2) - H / 2) * -.06, -c.height * .1, c.height * .1).toFixed(1)}px)`; });
  };
  const queue = () => { if (!queued) { queued = true; requestAnimationFrame(frame); } };
  addEventListener('scroll', queue, { passive: true });
  addEventListener('resize', queue);
  frame();
})();
