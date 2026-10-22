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
  $$('[data-stagger]').forEach(g => [...g.children].forEach((c, i) => c.style.setProperty('--i', Math.min(i, 5))));
  $$('[data-split]').forEach(el => {
    const words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words.map((w, i) => `<span class="w" style="--i:${i}"><span>${w}</span></span>`).join(' ');
  });
  // blocks trigger at 25% in view (5.4); anything taller than three viewports can never reach that, so it goes at 5%
  const tall = e => e.getBoundingClientRect().height > innerHeight * 3;
  const blocks = $$('[data-reveal],[data-stagger],[data-split],.vs-mid,.cert');
  const onIn = e => { e.classList.add('in'); if (e.hasAttribute('data-stagger')) setTimeout(() => e.classList.add('settled'), 1800); };
  watch(blocks.filter(e => !tall(e)), onIn, 0.25);
  watch(blocks.filter(tall), onIn, 0.05);
  watch($$('.anim,[data-viz]'), e => e.classList.add('in'), 0.35);

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

  /* ---------- questions: open and close with the rows technique (css), not a height tween ---------- */
  $$('.faq-list details').forEach(d => {
    const sum = $('summary', d);
    sum.addEventListener('click', e => {
      if (reduce) return;
      e.preventDefault();
      if (!d.open) { d.open = true; requestAnimationFrame(() => requestAnimationFrame(() => d.classList.add('is-open'))); }
      else { d.classList.remove('is-open'); setTimeout(() => { d.open = false; }, 300); }
    });
  });

  /* ---------- counters (receipts), run once. Only 28 and 9 count: a response time that counts up from zero is not a response time. ---------- */
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
  const hosts = $$('[data-ico-host]').filter(h => !h.classList.contains('hs'));
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

  /* ---------- scenes: play once at 60% in view; scene 1 replays on click or tap; layers lean toward a fine pointer ---------- */
  const scenes = $$('.scene-card[data-scene],.versus[data-scene]');
  const playScene = c => { c.classList.remove('play'); void c.getBoundingClientRect(); c.classList.add('play'); };
  if (reduce || !hasIO) scenes.forEach(c => c.classList.add('play'));
  else watch(scenes, playScene, 0.6);
  const nf = $('#sc-nothing-to-find');
  if (nf && !reduce) {
    const again = () => { if (nf.classList.contains('play')) playScene(nf); };
    const m = $('.s1-machine', nf); if (m) m.addEventListener('click', again);
    const rb = $('.scene-replay', nf); if (rb) rb.addEventListener('click', again);
  }
  if (!reduce && matchMedia('(hover:hover) and (pointer:fine)').matches) {
    let cur = null, raf = 0, lx = 0, ly = 0;
    const lean = () => { raf = 0; if (cur) { cur.style.setProperty('--lx', lx.toFixed(3)); cur.style.setProperty('--ly', ly.toFixed(3)); } };
    scenes.forEach(c => {
      c.addEventListener('pointermove', e => { const r = c.getBoundingClientRect(); cur = c; lx = clamp(((e.clientX - r.left) / r.width) * 2 - 1, -1, 1); ly = clamp(((e.clientY - r.top) / r.height) * 2 - 1, -1, 1); if (!raf) raf = requestAnimationFrame(lean); }, { passive: true });
      c.addEventListener('pointerleave', () => { c.style.setProperty('--lx', 0); c.style.setProperty('--ly', 0); });
    });
  }

  /* ---------- scene 3: hover, focus or tap a row and its pair lights on the other sheet ---------- */
  const zm = $('.sc-markup');
  if (zm) {
    const set = i => { [0, 1, 2].forEach(n => zm.classList.toggle('pair-' + n, n === i)); };
    $$('.s3-row', zm).forEach(r => {
      const i = +r.dataset.row;
      r.addEventListener('pointerenter', () => set(i)); r.addEventListener('pointerleave', () => set(-1));
      r.addEventListener('focus', () => set(i)); r.addEventListener('blur', () => set(-1));
      r.addEventListener('pointerdown', e => { if (e.pointerType === 'touch') set(i); });
    });
    document.addEventListener('pointerdown', e => { if (!e.target.closest || !e.target.closest('.s3-row')) set(-1); }, { passive: true });
  }

  /* ---------- the regulation row: a visible pause control (WCAG 2.2.2) ---------- */
  const cert = $('#cert'), pauseBtn = cert && $('.cert-pause', cert);
  if (pauseBtn) pauseBtn.addEventListener('click', () => {
    const on = cert.classList.toggle('is-paused');
    pauseBtn.setAttribute('aria-pressed', on);
    pauseBtn.setAttribute('aria-label', on ? 'Play the scrolling row' : 'Pause the scrolling row');
    $('span', pauseBtn).textContent = on ? 'Play' : 'Pause';
  });

  /* ---------- depth roots: the nearest [data-scene] or section of every .depth layer. --p is written on the root, once per frame. ---------- */
  const depthRoots = [...new Set($$('.depth').map(d => d.closest('[data-scene],section') || d.parentElement))];
  const liveRoots = new Set();
  if (depthRoots.length && hasIO && !reduce) {
    const dio = new IntersectionObserver(es => es.forEach(en => {
      en.target.classList.toggle('depth-live', en.isIntersecting);
      en.isIntersecting ? liveRoots.add(en.target) : liveRoots.delete(en.target);
    }), { rootMargin: '10% 0px' });
    depthRoots.forEach(r => dio.observe(r));
  }

  /* ---------- scrubbed sections: how it works, one partner, the staircase (scroll position, not time; nothing is pinned) ---------- */
  const hsteps = $('#hsteps'), hsNodes = hsteps ? $$('.hs', hsteps) : [];
  let hsGeo = null;
  const measureHs = () => {
    if (!hsteps) return;
    const vertical = innerWidth < 1024, box = hsteps.getBoundingClientRect();
    const pts = hsNodes.map(h => { const r = $('.hs-node', h).getBoundingClientRect(); return vertical ? r.top + r.height / 2 - box.top : r.left + r.width / 2 - box.left; });
    hsGeo = { vertical, pts, a: pts[0], b: pts[pts.length - 1] };
    const fill = $('.hs-fill', hsteps), dot = $('.hs-dot', hsteps);
    if (vertical) {
      fill.style.cssText = `left:19px;right:auto;top:${hsGeo.a}px;height:${hsGeo.b - hsGeo.a}px;width:1.5px`;
      dot.style.cssText = `left:19px;top:${hsGeo.a}px`;
      hsteps.style.setProperty('--hy', (hsGeo.b - hsGeo.a) + 'px'); hsteps.style.setProperty('--hx', '0px');
    } else {
      fill.style.cssText = `left:${hsGeo.a}px;right:auto;width:${hsGeo.b - hsGeo.a}px`;
      dot.style.cssText = `left:${hsGeo.a}px`;
      hsteps.style.setProperty('--hx', (hsGeo.b - hsGeo.a) + 'px'); hsteps.style.setProperty('--hy', '0px');
    }
  };
  if (hsteps && !reduce) {
    hsteps.classList.add('scrub');
    measureHs(); if (document.fonts && document.fonts.ready) document.fonts.ready.then(measureHs); addEventListener('resize', measureHs);
  }
  const scene5 = $('#sc-one-partner'), partnerRows = $('.one-r'), stair = $('.stair');

  /* ---------- one loop for everything tied to scroll ---------- */
  const navWrap = $('#navWrap'), intro = $('#ansIntro'), introIn = intro && $('.ans-intro-in', intro);
  const ans = $$('[data-ans]'), steps = $('#steps'), parallax = $$('[data-parallax]'), pimgs = $$('[data-parallax-img]');
  const navLinks = $$('.nav-links a').filter(a => /#(seats|offer)$/.test(a.getAttribute('href') || ''));
  const secOf = id => (id === 'seats' ? [$('#seats')] : [$('#offer'), $('#partner')]).filter(Boolean);
  const footMark = $('.foot-mark');
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
    if (innerWidth >= 768) liveRoots.forEach(r => {
      const b = r.getBoundingClientRect();
      r.style.setProperty('--p', clamp(((H - b.top) / (H + b.height)) * 2 - 1, -1, 1).toFixed(3));
    });
    if (hsteps && hsGeo && !reduce) {
      const r = hsteps.getBoundingClientRect();
      const hp = clamp((H * 0.72 - r.top) / (r.height + H * 0.1 > 0 ? Math.min(r.height * 0.9, H * 0.7) : 1));
      hsteps.style.setProperty('--hp', hp.toFixed(3));
      const head = hsGeo.a + hp * (hsGeo.b - hsGeo.a);
      hsNodes.forEach((h, i) => h.classList.toggle('on', head >= hsGeo.pts[i] - 1));
    }
    if (scene5 && !reduce) {
      const r = scene5.getBoundingClientRect(), cy = r.top + r.height / 2;
      const sa = clamp((H * 0.95 - cy) / (H * 0.45)), sc = clamp((H * 0.5 - cy) / (H * 0.2));
      const svg = $('svg', scene5);
      svg.style.setProperty('--sa', sa.toFixed(3)); svg.style.setProperty('--sc', sc.toFixed(3)); svg.style.setProperty('--do', sc > 0 && sc < 1 ? 1 : 0);
      if (sc >= 1 && partnerRows) partnerRows.classList.add('ticked');
    }
    if (stair) { const r = stair.getBoundingClientRect(); stair.style.setProperty('--sk', clamp((H * 0.92 - r.top) / (H * 0.45)).toFixed(3)); }
    if (footMark) footMark.style.setProperty('--fr', clamp((y - (max - 400)) / 400).toFixed(3));
    if (innerWidth >= 768) parallax.forEach(el => { const r = el.getBoundingClientRect(); if (r.bottom < -100 || r.top > H + 100) return; const f = +el.dataset.parallax; el.style.transform = `translateY(${(((r.top + r.height / 2) - H / 2) * -f).toFixed(1)}px)`; });
    if (innerWidth >= 768) pimgs.forEach(im => { const c = im.parentElement.getBoundingClientRect(); if (c.bottom < -100 || c.top > H + 100) return; im.style.transform = `translateY(${clamp(((c.top + c.height / 2) - H / 2) * -.06, -c.height * .1, c.height * .1).toFixed(1)}px)`; });
  };
  const queue = () => { if (!queued) { queued = true; requestAnimationFrame(frame); } };
  addEventListener('scroll', queue, { passive: true });
  addEventListener('resize', queue);
  frame();
})();
