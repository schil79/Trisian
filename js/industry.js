/* Day-after panel: plays once when it enters the viewport.
   CSS does the animation; this only arms the panel and starts it.
   Without JavaScript, or with reduced motion, the panel shows its final state. */
(() => {
  'use strict';
  const panels = [...document.querySelectorAll('[data-dap]')];
  if (!panels.length) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced || !('IntersectionObserver' in window)) return;
  panels.forEach(p => p.setAttribute('data-armed', ''));
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('go'); io.unobserve(e.target); }
  }), { threshold: 0.35 });
  panels.forEach(p => io.observe(p));
})();
