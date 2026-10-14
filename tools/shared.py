"""Fragments shared by gen_home.py and gen_industry_pages.py: nav, footer, industry cards, head tags."""
import html, json, re

BASE_URL = 'https://schil79.github.io/Trisian/'   # staging host; swap at launch


def esc(s):
    return html.escape(s, quote=False)


def t(s):
    """escape, then turn **x** into <b>x</b>"""
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', esc(s))


def plain(s):
    return s.replace('**', '')


def dropdown(base, active=None):
    on = ' aria-current="page"' if active == 'who' else ''
    return f'''<div class="nav-item has-dd{' is-active' if active == 'who' else ''}">
        <a href="{base}who-its-for/" class="dd-link"{on}>Who it's for</a>
        <button class="dd-toggle" type="button" aria-expanded="false" aria-controls="ddList" aria-label="Show industries"><svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4.5l4 4 4-4"/></svg></button>
        <ul class="dd" id="ddList">
          <li><a href="{base}who-its-for/">All industries</a></li>
          <li><a href="{base}healthcare/">Healthcare</a></li>
          <li><a href="{base}financial-services/">Financial services</a></li>
          <li><a href="{base}legal/">Legal</a></li>
          <li><a href="{base}growing-businesses/">Growing businesses</a></li>
        </ul>
      </div>'''


def header(base, cta_href='#assessment', active=None):
    def a(key, href, label):
        cur = ' aria-current="page"' if active == key else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<header class="nav-wrap" id="navWrap">
  <span class="prog" id="prog" aria-hidden="true"></span>
  <nav class="nav" id="nav" aria-label="Primary">
    <a href="{base}" class="logo" aria-label="Trisian home"><img src="{base}assets/img/trisian-logo.png" alt="Trisian"></a>
    <div class="nav-links" id="navLinks">
      {a('answers', base + '#answers', 'The 3 answers')}
      {a('offer', base + '#offer', 'What we offer')}
      {dropdown(base, active)}
      {a('coverage', base + 'coverage/', 'Coverage')}
      {a('services', base + 'services/', 'Services')}
      {a('insights', base + 'insights/', 'Insights')}
      <a href="{cta_href}" class="btn btn-sm">Book an assessment</a>
    </div>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="navLinks"><span></span><span></span></button>
  </nav>
</header>'''


# sector cards for the "Industries we serve" header. [slug, name, icon, chips, description]
SECTORS = [
    ('financial-services', 'Financial services', 'receipt', ['DORA', 'SOX', 'PCI-DSS', 'GLBA'],
     'Evidence ready for the examiner. Privileged access for segregation of duties. Long-term record retention available.'),
    ('healthcare', 'Healthcare', 'activity', ['HIPAA', 'HITECH'],
     'Patient data protected, and provably so. Audit trails with long-term retention available.'),
    ('legal', 'Legal', 'file-text', ['SOC 2', 'GDPR'],
     'Client confidences kept apart. Premium eDiscovery and data loss prevention for privileged work.'),
    ('growing-businesses', 'Growing businesses', 'growth', ['SOC 2', 'GDPR', 'ISO 27001'],
     "Enterprise-grade protection at your size. Start on Core. Add coverage as your clients' requirements grow."),
]


def industries(base, current=None, compact=False):
    """the Industries we serve header: on the hub and every sector page. The current sector is solid indigo."""
    import icons
    out = []
    for slug, name, icon, chips, desc in SECTORS:
        cur = slug == current
        chips_h = ''.join(f'<li>{esc(c)}</li>' for c in chips)
        body = '' if compact else f'<p>{esc(desc)}</p>'
        ac = ' aria-current="page"' if cur else ''
        out.append(f'''<a class="sector{' is-current' if cur else ''}" href="{base}{slug}/"{ac}>
        <span class="sector-ico">{icons.ic(icon, 24)}</span>
        <b>{esc(name)}</b>
        <ul class="sector-chips">{chips_h}</ul>
        {body}
      </a>''')
    cls = 'sectors sectors--compact' if compact else 'sectors'
    return f'''<section class="ind-head" aria-label="Industries we serve">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      <span class="pill">Industries we serve</span>
      <h2 class="h2"><span class="bd">Built for regulated sectors.</span></h2>
      <p class="sub-p">Same architecture everywhere. Configured for the rules your industry answers to.</p>
    </header>
    <div class="{cls}" data-stagger>
      {''.join(out)}
    </div>
  </div>
</section>'''


def cta_end(line, label, href):
    """end-of-section call to action: a hairline, a line in bold, a button. Never the same words twice."""
    return f'''<div class="cta-end" data-reveal>
      <p class="cta-line">{esc(line)}</p>
      <a class="btn" href="{href}">{esc(label)}</a>
    </div>'''


def form_band(bold, light, sub, base=''):
    """the assessment band: indigo, white form card, hidden interest field (set from ?topic= or the hash)."""
    return f'''<section class="sec s-indigo" id="assessment">
  <div class="wrap">
    <div class="cta">
      <div class="cta-copy" data-reveal="left">
        <h2 class="h2 on-dark"><span class="bd">{esc(bold)}</span><span class="lt">{esc(light)}</span></h2>
        <p class="sub-p">{esc(sub)}</p>
      </div>
      <div class="form-card" data-reveal="right">
        <form class="form" id="form" novalidate>
          <input type="hidden" name="interest" id="f-interest" value="">
          <label for="f-name">Name<input id="f-name" name="name" autocomplete="name" required></label>
          <label for="f-email">Work email<input id="f-email" name="email" type="email" autocomplete="email" required></label>
          <label for="f-co">Company<input id="f-co" name="company" autocomplete="organization" required></label>
          <label for="f-ind">Industry
            <select id="f-ind" name="industry" required>
              <option value="">Choose one</option>
              <option>Healthcare</option><option>Financial services</option><option>Legal</option><option>Growing business</option><option>Other regulated industry</option>
            </select>
          </label>
          <button class="btn" type="submit">Book an assessment</button>
          <p class="form-msg" id="formMsg" role="status" aria-live="polite"></p>
        </form>
        <p class="prefer">Prefer to write? <a href="mailto:contact@trisian.com">contact@trisian.com</a></p>
      </div>
    </div>
  </div>
</section>'''


def ph(ratio, scene, alt, cls=''):
    """picture placeholder. Staging-only label. Swap for the real photo, keep the alt."""
    r = ratio.replace(':', '/')
    return (f'<div class="ph {cls}" style="aspect-ratio:{r}" role="img" aria-label="{html.escape(alt)}" data-parallax="0.06">'
            f'<span class="ph-label">PHOTO PENDING \u00b7 {ratio} \u00b7 {esc(scene)}</span></div>')


def footer(base):
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="{base}assets/img/trisian-logo.png" alt="Trisian" class="foot-logo">
        <p>Managed IT for regulated industries. 28 years in business.</p>
      </div>
      <div class="foot-col" role="group" aria-label="Product">
        <b>Product</b>
        <a href="{base}#offer">What we offer</a>
        <a href="{base}coverage/">Coverage</a>
        <a href="{base}services/">Services</a>
        <a href="{base}insights/">Insights</a>
        <a href="{base}#faq">Questions</a>
      </div>
      <div class="foot-col" role="group" aria-label="Who it's for">
        <b>Who it's for</b>
        <a href="{base}who-its-for/">All industries</a>
        <a href="{base}healthcare/">Healthcare</a>
        <a href="{base}financial-services/">Financial services</a>
        <a href="{base}legal/">Legal</a>
        <a href="{base}growing-businesses/">Growing businesses</a>
      </div>
      <div class="foot-col" role="group" aria-label="Company">
        <b>Company</b>
        <a href="mailto:contact@trisian.com">contact@trisian.com</a>
        <a href="{base}#assessment">Book an assessment</a>
      </div>
    </div>
    <p class="foot-legal">&copy; 2026 Trisian</p>
  </div>
</footer>'''


def head_common(base, title, desc, slug, jsonld=(), home=False):
    url = BASE_URL + (slug + '/' if slug else '')
    og = f'''<meta property="og:type" content="website">
<meta property="og:site_name" content="Trisian">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">'''
    ld = '\n'.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="noindex, nofollow">
<!-- REMOVE noindex AT LAUNCH -->
<link rel="canonical" href="{url}">
{og}
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%231800AD'/%3E%3Cpath d='M7 9h18v4h-7v11h-4V13H7z' fill='%23fff'/%3E%3C/svg%3E">
<link rel="preload" href="{base}assets/fonts/Graphik-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{base}assets/fonts/Graphik-Bold.woff2" as="font" type="font/woff2" crossorigin>
<meta name="theme-color" content="#FFFFFF">
<link rel="stylesheet" href="{base}css/styles.css">
<link rel="stylesheet" href="{base}css/industry.css">
{ld}
<script>document.documentElement.classList.add('js')</script>
</head>'''


def breadcrumbs(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u}
                                for i, (n, u) in enumerate(items)]}


def faqld(faq):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': plain(q),
                            'acceptedAnswer': {'@type': 'Answer', 'text': plain(a)}} for q, a in faq]}
