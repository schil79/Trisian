/* Trisian home page behaviour. No libraries. CSS does the drawing; this adds classes and numbers.
   Under prefers-reduced-motion: no counters, no hero sequence, no autoplay. Pages render their final state. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasIO = 'IntersectionObserver' in window;
  const ease = t => 1 - Math.pow(1 - t, 3);                 // ease-out cubic

  /* ---------- enter-view classes ---------- */
  const watch = (els, cb, threshold) => {
    if (!hasIO) { els.forEach(e => cb(e)); return; }
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting) { cb(en.target); io.unobserve(en.target); }
    }), { threshold });
    els.forEach(e => io.observe(e));
  };
  $$('[data-stagger]').forEach(g => [...g.children].forEach((c, i) => c.style.setProperty('--i', i)));
  watch($$('[data-reveal],[data-stagger]'), e => e.classList.add('in'), 0.12);
  watch($$('.anim:not(#stage)'), e => e.classList.add('in'), 0.4);

  /* ---------- progress widget ---------- */
  const setStep = (w, n, done) => {
    if (!w) return;
    w.style.setProperty('--p', (n / 3 * 100) + '%');
    $$('.pw-dots i', w).forEach((d, i) => d.classList.toggle('on', i < n));
    $('[data-pw-n]', w).textContent = n;
    w.classList.toggle('done', !!done);
    $('[data-pw-label]', w).textContent = done ? 'Answered' : 'Answers on file';
  };

  /* ---------- hero: sequence, tabs ---------- */
  const stage = $('#stage'), heroPw = $('#heroPw'), hero = $('.hero');
  if (stage) {
    if (reduce) { stage.classList.add('in'); }
    else {
      setStep(heroPw, 0, false);
      requestAnimationFrame(() => requestAnimationFrame(() => {
        stage.classList.add('in');
        [[700, 1], [1100, 2], [1500, 3]].forEach(([t, n]) => setTimeout(() => setStep(heroPw, n, false), t));
        setTimeout(() => { setStep(heroPw, 3, true); hero.classList.add('go'); }, 1650);
      }));
    }
  }

  const data = JSON.parse(($('#roomData') || {}).textContent || '{}');
  const tabs = $$('.rt-tab'), panel = $('#roomPanel'), chips = $('#roomChips'), link = $('#roomLink'), sr = $('#roomSr');
  const keys = tabs.map(t => t.dataset.room);
  let cur = -1;
  const select = (i, focus) => {
    cur = i;
    const k = keys[i], d = data[k];
    tabs.forEach((t, j) => { const on = j === i; t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1; });
    $$('.room').forEach(r => r.classList.toggle('on', r.dataset.room === k));
    chips.innerHTML = d.chips.map(c => `<li>${c}</li>`).join('');
    link.href = d.href;
    link.setAttribute('aria-label', 'See this room: ' + tabs[i].textContent);
    sr.textContent = d.stamp + '. ' + d.q;
    panel.hidden = false;
    panel.setAttribute('aria-labelledby', tabs[i].id);
    if (focus) tabs[i].focus();
  };
  if (tabs.length && data.healthcare) {
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => select(i));
      t.addEventListener('keydown', e => {
        const n = tabs.length;
        const to = { ArrowRight: (i + 1) % n, ArrowLeft: (i + n - 1) % n, Home: 0, End: n - 1 }[e.key];
        if (to !== undefined) { e.preventDefault(); select(to, true); }
      });
    });
    // autoplay: every 6s, only while the stage is on screen and not hovered or focused. Never under reduced motion.
    if (!reduce) {
      let paused = false, visible = false;
      const bar = $('.stage');
      ['mouseenter', 'focusin'].forEach(ev => bar.addEventListener(ev, () => { paused = true; }));
      ['mouseleave', 'focusout'].forEach(ev => bar.addEventListener(ev, () => { paused = false; }));
      if (hasIO) new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(bar);
      setInterval(() => { if (!paused && visible) select((cur + 1) % tabs.length); }, 6000);
    }
  }

  /* ---------- which framework chips light up (hover or focus on an industry) ---------- */
  const hi = k => { if (k) document.body.dataset.hi = k; else delete document.body.dataset.hi; };
  tabs.forEach(t => { t.addEventListener('mouseenter', () => hi(t.dataset.room)); t.addEventListener('focus', () => hi(t.dataset.room));
    t.addEventListener('mouseleave', () => hi()); t.addEventListener('blur', () => hi()); });
  $$('.ind-card').forEach(c => { c.addEventListener('mouseenter', () => hi(c.dataset.ind)); c.addEventListener('focus', () => hi(c.dataset.ind));
    c.addEventListener('mouseleave', () => hi()); c.addEventListener('blur', () => hi()); });

  /* ---------- receipts: counters run once ---------- */
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

  /* ---------- answers: sticky widget advances, illustrations play once ---------- */
  const side = $('#sidePw'), arts = $$('.ans');
  if (side && arts.length) {
    let last = -1, queued = false;
    const update = () => {
      queued = false;
      const line = innerHeight * 0.6;
      let n = 0;
      arts.forEach((a, i) => { if (a.getBoundingClientRect().top < line) n = i + 1; });
      n = Math.max(1, n);
      const done = n === 3 && arts[2].getBoundingClientRect().top < innerHeight * 0.45;
      const key = n + (done ? 'd' : '');
      if (key !== last) { last = key; setStep(side, n, done); }
    };
    addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  const room = $('[data-viz="room"]');
  if (room) {
    const time = $('[data-rs-time]', room), pct = $('[data-rs-pct]', room), fill = $('[data-rs-fill]', room);
    const paint = p => {
      const m = Math.round((1 - p) * 60);
      time.textContent = p >= 1 ? '00:00' : '23:' + String(Math.max(0, 60 - Math.round(p * 60)) % 60).padStart(2, '0');
      pct.textContent = 'Reset ' + Math.round(p * 100) + '%';
      fill.parentNode.style.setProperty('--p', p * 100 + '%');
      void m;
    };
    if (!reduce) {
      paint(0);
      watch([room], () => {
        const t0 = performance.now() + 700;
        const tick = now => {
          const p = Math.max(0, Math.min(1, (now - t0) / 1300));
          paint(ease(p));
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      }, 0.4);
    }
  }

  $$('.dots').forEach(d => {
    for (let i = 0; i < +d.dataset.dots; i++) { const s = document.createElement('span'); s.style.setProperty('--i', i); d.appendChild(s); }
  });
})();
