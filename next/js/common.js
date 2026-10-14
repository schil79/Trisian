/* Shared by every page: mobile menu, industries dropdown, assessment form.
   No dependencies. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* ---------- mobile menu ---------- */
  const burger = $('#burger'), links = $('#navLinks');
  if (burger && links) {
    burger.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
    });
    links.addEventListener('click', e => {
      if (e.target.closest('a')) { links.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }
    });
  }

  /* ---------- industries dropdown (mouse, keyboard, touch) ---------- */
  const dd = $('.has-dd');
  if (dd) {
    const btn = $('.dd-toggle', dd);
    const set = open => { dd.classList.toggle('open', open); btn.setAttribute('aria-expanded', open); };
    btn.addEventListener('click', e => { e.stopPropagation(); set(!dd.classList.contains('open')); });
    document.addEventListener('click', e => { if (!dd.contains(e.target)) set(false); });
    dd.addEventListener('keydown', e => { if (e.key === 'Escape') { set(false); btn.focus(); } });
    dd.addEventListener('focusout', e => { if (!dd.contains(e.relatedTarget)) set(false); });
  }

  /* ---------- topic links: /#assessment?topic=x sets the hidden interest field ---------- */
  // The query sits inside the hash, so read it from there as well as from ?topic=.
  const topicOf = str => { const m = /[?&]topic=([a-z-]+)/.exec(str || ''); return m ? m[1] : ''; };
  const interest = $('#f-interest');
  const applyTopic = t => { if (t && interest) interest.value = t; };
  applyTopic(topicOf(location.search) || topicOf(location.hash));
  if (/^#assessment/.test(location.hash)) {
    const t = $('#assessment');
    if (t) setTimeout(() => t.scrollIntoView(), 60);
  }
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href*="#assessment?topic="]');
    if (!a) return;
    const url = new URL(a.getAttribute('href'), location.href);
    if (url.pathname !== location.pathname || !$('#assessment')) return;      // another page: let the browser go
    e.preventDefault();
    applyTopic(topicOf(url.hash));
    $('#assessment').scrollIntoView({ behavior: 'smooth' });
    history.replaceState(null, '', '#assessment');
  });

  /* ---------- assessment form ---------- */
  // Front-end only for now. Nothing is sent anywhere yet; wire to email/CRM before launch.
  const form = $('#form'), msg = $('#formMsg');
  if (form) {
    const map = { healthcare: 'Healthcare', financial: 'Financial services', legal: 'Legal', growing: 'Growing business' };
    const sel = $('#f-ind', form);
    const want = new URLSearchParams(location.search).get('industry') || form.dataset.industry;
    if (sel && map[want]) sel.value = map[want];
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); msg.textContent = ''; return; }
      msg.textContent = 'Thanks. We will be in touch.';
      form.reset();
      if (sel && map[want]) sel.value = map[want];
    });
  }
})();
