(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- nav ---------- */
  const burger = $('#burger'), links = $('#navLinks');
  burger.addEventListener('click', () => {
    const open = links.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });
  links.addEventListener('click', e => {
    if (e.target.closest('a')) { links.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }
  });

  /* ---------- reveal on scroll ---------- */
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { threshold: 0.15 });
  $$('.reveal').forEach(el => io.observe(el));

  /* ---------- small looping room grids (hero graph + bento) ---------- */
  $$('[data-mini]').forEach(m => {
    const n = +m.dataset.mini, cols = m.classList.contains('lg') ? 12 : 6;
    for (let i = 0; i < n; i++) {
      const c = document.createElement('i');
      c.style.setProperty('--d', ((i % cols) * 0.09 + Math.floor(i / cols) * 0.05).toFixed(2) + 's');
      m.appendChild(c);
    }
  });

  /* ---------- hero answer graph: connectors from the question to each answer ---------- */
  const graph = $('#graph');
  const drawGraph = () => {
    const svg = $('#graphLines'), q = $('#gq');
    if (!graph || !svg) return;
    svg.innerHTML = '';
    const nodes = $$('.gn', graph), g = graph.getBoundingClientRect(), qr = q.getBoundingClientRect();
    if (getComputedStyle(svg).display === 'none' || nodes[0].getBoundingClientRect().left <= qr.right) return;
    const sx = qr.right - g.left, sy = qr.top + qr.height / 2 - g.top, NS = 'http://www.w3.org/2000/svg';
    const add = (tag, attrs) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); svg.appendChild(e); };
    nodes.forEach(n => {
      const r = n.getBoundingClientRect(), ex = r.left - g.left, ey = r.top + r.height / 2 - g.top, dx = (ex - sx) * 0.55;
      add('path', { d: `M${sx} ${sy} C${sx + dx} ${sy}, ${ex - dx} ${ey}, ${ex} ${ey}` });
      add('circle', { cx: ex, cy: ey, r: 5 });
    });
    add('circle', { cx: sx, cy: sy, r: 5 });
  };
  drawGraph();
  addEventListener('resize', drawGraph);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(drawGraph);
  addEventListener('load', drawGraph);
  setTimeout(drawGraph, 2100);

  /* ---------- diagram: The Empty Room ---------- */
  const room = (() => {
    const grid = $('#roomGrid'); if (!grid) return () => {};
    const cells = Array.from({ length: 40 }, (_, i) => {
      const c = document.createElement('i'); c.className = 'cell'; grid.appendChild(c); return c;
    });
    const steps = $$('#roomSteps span'), clock = $('#roomClock'), bar = $('#roomBar'), note = $('#roomNote');
    const OUT = 9 / 21, RESET = 15 / 21;               // 18:00 and 00:00 on a 09:00 -> 06:00 timeline
    const notes = ['Users signing in.', 'Users at work.', 'Users gone. Machines idle.', 'Midnight. Every desktop reset.',
      '06:00. Anyone who got in at midnight finds nothing.'];
    return p => {
      const t = 9 + p * 21, h = Math.floor(t % 24), m = Math.floor((t % 1) * 60);
      clock.textContent = String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0');
      bar.style.width = p * 100 + '%';
      cells.forEach((c, i) => {
        const col = i % 10;
        let s = '';
        if (p >= RESET + col * 0.012) s = 'gone';
        else if (p >= OUT) s = 'out';
        else if (p >= 0.02 + (i / 40) * 0.08) s = 'on';
        c.className = 'cell' + (s ? ' ' + s : '');
      });
      const s = p < 0.1 ? 0 : p < OUT ? 1 : p < RESET ? 2 : 3;
      steps.forEach((el, i) => el.classList.toggle('act', i === s));
      note.textContent = p < 0.1 ? notes[0] : p < OUT ? notes[1] : p < RESET ? notes[2] : p < 0.92 ? notes[3] : notes[4];
    };
  })();

  /* ---------- diagram: Industry-Bound ---------- */
  const bound = (() => {
    const sec = $('[data-scrub="bound"]'); if (!sec) return () => {};
    $$('[data-tower]', sec).forEach(t => { for (let i = 0; i < 10; i++) t.appendChild(document.createElement('i')); });
    const dots = $$('[data-dots]', sec).map(d => {
      const n = +d.dataset.dots; for (let i = 0; i < n; i++) d.appendChild(document.createElement('i'));
      return [...d.children];
    });
    const towers = $$('[data-tower]', sec).map(t => [...t.children]);
    const line = $('.bound-line', sec), verdict = $('#boundVerdict');
    return p => {
      dots.forEach(ds => { const n = Math.ceil(clamp(p / 0.3) * ds.length); ds.forEach((d, i) => d.classList.toggle('lit', i < n)); });
      const lit = Math.round(clamp((p - 0.3) / 0.45) * 10);
      towers.forEach(ts => ts.forEach((b, i) => b.classList.toggle('lit', i < lit)));
      line.style.width = clamp((p - 0.75) / 0.15) * 100 + '%';
      verdict.style.opacity = p > 0.9 ? 1 : 0;
    };
  })();

  /* ---------- diagram: Zero Markup ---------- */
  const markup = (() => {
    const rows = $$('.led-row'); if (!rows.length) return () => {};
    return p => rows.forEach(r => r.classList.toggle('on', p >= +r.dataset.at));
  })();

  const apply = { room, bound, markup };

  /* ---------- scroll scrub (desktop) or autoplay (mobile / reduced motion) ---------- */
  const sections = $$('[data-scrub]').map(el => ({ el, fn: apply[el.dataset.scrub], played: false, raf: 0 }));
  const scrubbing = () => !reduced && matchMedia('(min-width: 901px)').matches && innerHeight >= 600;

  const play = s => {
    if (s.played) return; s.played = true;
    if (reduced) { s.fn(1); return; }
    const t0 = performance.now(), dur = 6500;
    const tick = now => { const p = clamp((now - t0) / dur); s.fn(p); if (p < 1) s.raf = requestAnimationFrame(tick); };
    s.raf = requestAnimationFrame(tick);
  };

  const update = () => {
    if (!scrubbing()) return;
    sections.forEach(s => {
      const r = s.el.getBoundingClientRect(), span = r.height - innerHeight;
      s.fn(span > 0 ? clamp(-r.top / span) : 1);
    });
  };
  let ticking = false;
  const onScroll = () => { if (ticking) return; ticking = true; requestAnimationFrame(() => { ticking = false; update(); }); };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', () => { if (scrubbing()) update(); else sections.forEach(s => s.played || io2.observe(s.el)); });

  const io2 = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting && !scrubbing()) { const s = sections.find(x => x.el === e.target); io2.unobserve(e.target); play(s); }
  }), { threshold: 0.35 });
  sections.forEach(s => { s.fn(0); io2.observe(s.el); });
  update();

  /* ---------- assessment form ---------- */
  // Front-end only for now. Nothing is sent anywhere yet; wire to email/CRM before launch.
  const form = $('#form'), msg = $('#formMsg');
  form.addEventListener('submit', e => {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); msg.textContent = ''; return; }
    msg.textContent = 'Thanks. We will be in touch.';
    form.reset();
  });
})();
