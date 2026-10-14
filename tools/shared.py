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


def dropdown(base):
    return f'''<div class="nav-item has-dd">
        <a href="{base}who-its-for/" class="dd-link">Who it's for</a>
        <button class="dd-toggle" type="button" aria-expanded="false" aria-controls="ddList" aria-label="Show industries"><svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4.5l4 4 4-4"/></svg></button>
        <ul class="dd" id="ddList">
          <li><a href="{base}healthcare/">Healthcare</a></li>
          <li><a href="{base}financial-services/">Financial services</a></li>
          <li><a href="{base}legal/">Legal</a></li>
          <li><a href="{base}growing-businesses/">Growing businesses</a></li>
        </ul>
      </div>'''


def header(base, cta_href='#assessment'):
    return f'''<header class="nav-wrap">
  <nav class="nav" id="nav" aria-label="Primary">
    <a href="{base}" class="logo" aria-label="Trisian home"><img src="{base}assets/img/trisian-logo.png" alt="Trisian"></a>
    <div class="nav-links" id="navLinks">
      <a href="{base}#proof">The three answers</a>
      <a href="{base}#product">Safe Workspace</a>
      {dropdown(base)}
      <a href="{base}#plans">Plans</a>
      <a href="{base}#faq">Questions</a>
      <a href="{cta_href}" class="btn btn-sm">Book an assessment</a>
    </div>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="navLinks"><span></span><span></span></button>
  </nav>
</header>'''


# [slug, label, data-ind, question, rule line, link text]
CARDS = [
    ('healthcare', 'Healthcare', 'healthcare', 'Whose records. Which systems. Since when.',
     'HIPAA starts a 60-day clock the day a breach is discovered.', 'See the healthcare answers'),
    ('financial-services', 'Financial services', 'financial', 'The examiner asks for the log. Not the policy.',
     'Under Regulation S-P, customers hear within 30 days of you becoming aware. The program has to exist first.',
     'See the financial answers'),
    ('legal', 'Legal', 'legal', 'The rule says reasonable. Be ready to show it.',
     'ABA Formal Opinion 483: monitor, plan, keep clients informed. Not strict liability. Not optional.',
     'See the legal answers'),
    ('growing-businesses', 'Growing businesses', 'growing', 'The big client is coming. So is their questionnaire.',
     "Cleared for the deal before it's on paper.", 'See the growth answers'),
]


def cards(base):
    out = []
    for slug, label, ind, q, rule, link in CARDS:
        out.append(f'''<a class="ind-card" href="{base}{slug}/" data-ind="{ind}">
        <span class="ip-kicker">{esc(label)}</span>
        <h3 class="ind-q">{esc(q)}</h3>
        <p class="ind-rule">{esc(rule)}</p>
        <span class="ind-link">{esc(link)}<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg></span>
      </a>''')
    return '\n      '.join(out)


def footer(base):
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="{base}assets/img/trisian-logo.png" alt="Trisian" class="foot-logo">
        <p>Managed IT for regulated industries. 28 years in.</p>
      </div>
      <div class="foot-col" role="group" aria-label="Product">
        <b>Product</b>
        <a href="{base}#product">Safe Workspace</a>
        <a href="{base}#plans">Plans</a>
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
