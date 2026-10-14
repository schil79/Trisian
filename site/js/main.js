/* Trisian homepage behaviour.
   Built on Motion (vanilla build of the library Framer Motion is based on), the same family the reference sites use.
   Everything degrades: without Motion, or with reduced motion, all content shows in its final state. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const Mo = window.Motion || {};
  const { animate, scroll, inView, stagger, spring } = Mo;
  const live = !!(animate && scroll && inView) && !reduced;
  const desktop = () => matchMedia('(min-width: 981px)').matches;
  if (live) document.documentElement.classList.add('mo');

  const once = (el, fn, opts) => { let done = false; inView(el, () => { if (!done) { done = true; fn(); } }, opts); };

  /* ---------- nav ---------- */
  const burger = $('#burger'), links = $('#navLinks');
  burger.addEventListener('click', () => { const o = links.classList.toggle('open'); burger.setAttribute('aria-expanded', o); });
  links.addEventListener('click', e => { if (e.target.closest('a')) { links.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); } });

  /* ---------- marquee (Jitter): duplicate the list so the -50% loop is seamless ---------- */
  const mq = $('#marquee');
  if (mq) [...mq.children].forEach(li => { const c = li.cloneNode(true); c.setAttribute('aria-hidden', 'true'); mq.appendChild(c); });

  /* ---------- small looping room grids (hero graph + bento) ---------- */
  $$('[data-mini]').forEach(m => {
    const n = +m.dataset.mini, cols = m.classList.contains('lg') ? 12 : 6;
    for (let i = 0; i < n; i++) {
      const c = document.createElement('i');
      c.style.setProperty('--d', ((i % cols) * 0.09 + Math.floor(i / cols) * 0.05).toFixed(2) + 's');
      m.appendChild(c);
    }
  });

  /* ---------- diagram: The Empty Room ---------- */
  const room = (() => {
    const grid = $('#roomGrid'); if (!grid) return () => {};
    const cells = Array.from({ length: 40 }, () => { const c = document.createElement('i'); c.className = 'cell'; grid.appendChild(c); return c; });
    const steps = $$('#roomSteps span'), clock = $('#roomClock'), bar = $('#roomBar'), note = $('#roomNote');
    const OUT = 9 / 21, RESET = 15 / 21;   // 18:00 and 00:00 on a 09:00 -> 06:00 timeline
    const notes = ['Users signing in.', 'Users at work.', 'Users gone. Machines idle.', 'Midnight. Every desktop reset.', '06:00. Anyone who got in at midnight finds nothing.'];
    return p => {
      const t = 9 + p * 21, h = Math.floor(t % 24), m = Math.floor((t % 1) * 60);
      clock.textContent = String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0');
      bar.style.width = p * 100 + '%';
      cells.forEach((c, i) => {
        const col = i % 10;
        const s = p >= RESET + col * 0.012 ? 'gone' : p >= OUT ? 'out' : p >= 0.02 + (i / 40) * 0.08 ? 'on' : '';
        c.className = 'cell' + (s ? ' ' + s : '');
      });
      const s = p < 0.1 ? 0 : p < OUT ? 1 : p < RESET ? 2 : 3;
      steps.forEach((el, i) => el.classList.toggle('act', i === s));
      note.textContent = p < 0.1 ? notes[0] : p < OUT ? notes[1] : p < RESET ? notes[2] : p < 0.92 ? notes[3] : notes[4];
    };
  })();

  /* ---------- diagram: Industry-Bound (isometric tiles, the Clutch "coin" look) ---------- */
  const bound = (() => {
    const card = $('[data-viz="bound"]'); if (!card) return () => {};
    const labels = ['HIPAA', 'SOC 2', 'PCI', 'GDPR', 'SOX', 'DORA', 'CMMC', 'GLBA', 'ISO'];
    const planes = $$('[data-iso]', card).map(el => {
      const pl = document.createElement('div'); pl.className = 'iso-plane';
      labels.forEach(l => { const i = document.createElement('i'); i.textContent = l; pl.appendChild(i); });
      el.appendChild(pl); return [...pl.children];
    });
    const dots = $$('[data-dots]', card).map(d => {
      const n = +d.dataset.dots; for (let i = 0; i < n; i++) d.appendChild(document.createElement('i')); return [...d.children];
    });
    const verdict = $('#boundVerdict');
    return p => {
      dots.forEach(ds => { const n = Math.ceil(clamp(p / 0.3) * ds.length); ds.forEach((d, i) => d.classList.toggle('lit', i < n)); });
      const lit = Math.round(clamp((p - 0.3) / 0.45) * 9);
      planes.forEach(ts => ts.forEach((t, i) => t.classList.toggle('lit', i < lit)));
      verdict.style.opacity = p > 0.85 ? 1 : 0;
    };
  })();

  /* ---------- diagram: Zero Markup ---------- */
  const markup = (() => {
    const rows = $$('.led-row'); if (!rows.length) return () => {};
    return p => rows.forEach(r => r.classList.toggle('on', p >= +r.dataset.at));
  })();

  /* Diagrams loop while their card is on screen (Jitter and Clutch both loop product visuals). */
  const apply = { room, bound, markup };
  const DUR = 7500, HOLD = 2800;
  $$('[data-viz]').forEach(card => {
    const fn = apply[card.dataset.viz]; let run = false, t0 = 0;
    fn(reduced ? 1 : 0);
    if (reduced) return;
    const tick = now => { if (!run) return; fn(clamp(((now - t0) % (DUR + HOLD)) / DUR)); requestAnimationFrame(tick); };
    new IntersectionObserver(es => es.forEach(e => {
      const was = run; run = e.isIntersecting;
      if (run && !was) { t0 = performance.now(); requestAnimationFrame(tick); }
    }), { threshold: 0.4 }).observe(card);
  });

  /* ---------- hero: orchestrated answer graph (Clutch pattern: a state machine of springs) ---------- */
  const graph = $('#graph');
  const G = (() => {
    if (!graph) return {};
    const svg = $('#graphLines'), q = $('#gq'), nodes = $$('.gn', graph), rows = $$('#gqRows li'), status = $('#gqStatus');
    let paths = [], lens = [], pkt = null;
    const draw = () => {
      svg.innerHTML = ''; paths = []; lens = []; pkt = null;
      const g = graph.getBoundingClientRect(), qr = q.getBoundingClientRect();
      if (getComputedStyle(svg).display === 'none' || nodes[0].getBoundingClientRect().left <= qr.right) return;
      const NS = 'http://www.w3.org/2000/svg';
      const el = (tag, attrs) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); svg.appendChild(e); return e; };
      const sx = qr.right - g.left, sy = qr.top + qr.height / 2 - g.top;
      nodes.forEach(n => {
        const r = n.getBoundingClientRect(), ex = r.left - g.left, ey = r.top + r.height / 2 - g.top, dx = (ex - sx) * 0.55;
        const p = el('path', { d: `M${sx} ${sy} C${sx + dx} ${sy}, ${ex - dx} ${ey}, ${ex} ${ey}` });
        paths.push(p); lens.push(p.getTotalLength());
        el('circle', { class: 'end', cx: ex, cy: ey, r: 5 });
      });
      el('circle', { class: 'end', cx: sx, cy: sy, r: 5 });
      pkt = el('circle', { class: 'pkt', cx: sx, cy: sy, r: 6, opacity: 0 });
    };
    const bounce = { type: 'spring', stiffness: 300, damping: 15 };   // same spring Clutch uses
    const stage = async k => {
      const n = nodes[k];
      n.classList.add('active');
      await animate(n, { y: -8, scale: 1.03 }, { duration: 0.35, ease: 'easeInOut' });        // lift
      if (pkt) {                                                                                 // packet travels to the question
        pkt.setAttribute('opacity', 1);
        await animate(0, lens[k], {
          duration: 0.7, ease: 'easeInOut',
          onUpdate: v => { const pt = paths[k].getPointAtLength(lens[k] - v); pkt.setAttribute('cx', pt.x); pkt.setAttribute('cy', pt.y); }
        });
        pkt.setAttribute('opacity', 0);
      }
      animate(q, { scale: [0.96, 1] }, bounce);                                                  // land
      rows[k].classList.add('done');
      status.textContent = ['1 of 3 answered', '2 of 3 answered', 'Answered in advance.'][k];
      await animate(n, { y: 0, scale: 1 }, bounce);
      n.classList.remove('active');
    };
    const finalState = () => { rows.forEach(r => r.classList.add('done')); status.textContent = 'Answered in advance.'; };
    let seen = false;
    const start = async () => {
      if (!live) { draw(); finalState(); return; }
      await sleep(900);
      draw();
      animate(q, { opacity: [0, 1], y: [20, 0] }, { duration: 0.6, ease: 'easeOut' });
      await animate(nodes, { opacity: [0, 1], y: [20, 0] }, { delay: stagger(0.14), duration: 0.6, ease: 'easeOut' });
      draw();
      while (true) {
        rows.forEach(r => r.classList.remove('done')); status.textContent = 'Building the answer';
        await sleep(700);
        for (let k = 0; k < 3; k++) { while (!seen) await sleep(250); await stage(k); await sleep(280); }
        await sleep(3200);
      }
    };
    if (live) inView(graph, () => { seen = true; return () => { seen = false; }; }, { amount: 0.25 }); else seen = true;
    addEventListener('resize', () => { if (graph) draw(); });
    return { draw, start };
  })();
  if (G.start) G.start();

  /* ---------- hero entrance + reveals (Clutch's FadeIn: opacity + rise, once, on intersect) ---------- */
  if (live) {
    animate($$('.hero-head [data-in], .hero > .wrap[data-in], .strip[data-in]'), { opacity: [0, 1], y: [24, 0] }, { delay: stagger(0.12), duration: 0.8, ease: 'easeOut' });
    $$('[data-reveal]').forEach(el => once(el, () => animate(el, { opacity: [0, 1], y: [28, 0] }, { duration: 0.75, ease: 'easeOut' }), { amount: 0.2 }));
    $$('[data-stagger]').forEach(el => once(el, () => animate([...el.children], { opacity: [0, 1], y: [28, 0] }, { delay: stagger(0.09), duration: 0.7, ease: 'easeOut' }), { amount: 0.12 }));
  }

  /* ---------- Jitter: as the next card slides over, the one beneath scales back ---------- */
  const cards = $$('.pcard');
  if (live) cards.forEach((c, i) => {
    const next = cards[i + 1]; if (!next) return;
    scroll(animate(c, { scale: [1, 0.94] }, { ease: 'linear' }), { target: next, offset: ['start end', 'start 30%'] });
  });

  /* ---------- big quote (Jitter): rotates between the two client quotes ---------- */
  const quotes = [
    { t: '“Client quote goes here, dropped in verbatim from the audit.”', w: '<b>Mark D.</b> Avora Foods' },
    { t: '“Second client quote goes here, also from the audit.”', w: '<b>Ben F.</b> Crafter &amp; Co' }
  ];
  const bqT = $('#bqText'), bqW = $('#bqWho'), dots = $$('#bqDots button');
  let qi = 0, qTimer;
  const show = async i => {
    qi = i; dots.forEach((d, k) => d.classList.toggle('on', k === i));
    if (live) await animate([bqT, bqW], { opacity: 0, y: -10 }, { duration: 0.25 });
    bqT.textContent = quotes[i].t; bqW.innerHTML = quotes[i].w;
    if (live) await animate([bqT, bqW], { opacity: [0, 1], y: [12, 0] }, { duration: 0.4, ease: 'easeOut' });
  };
  const cycle = () => { clearInterval(qTimer); if (live) qTimer = setInterval(() => show((qi + 1) % quotes.length), 7000); };
  dots.forEach((d, i) => d.addEventListener('click', () => { show(i); cycle(); }));
  cycle();

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
