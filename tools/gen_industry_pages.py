#!/usr/bin/env python3
"""Generates the "Who it's for" pages (hub + four industries) into site/.

Not part of the site build. The site is plain static files and does not need this to run.
It exists so the locked copy lives in one place. Edit copy here, run it, commit the output:

    python3 tools/gen_industry_pages.py

Copy is transcribed from Trisian_Who_Its_For_Spec.md. Blocks tagged [HOLD] in the spec are
deliberately not present here. See SKIPPED at the bottom of this file.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
BASE_URL = 'https://schil79.github.io/Trisian/'   # staging host; swap at launch


def esc(s):
    return html.escape(s, quote=False)


def t(s):
    """escape, then turn **x** into <b>x</b>"""
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', esc(s))


def plain(s):
    return s.replace('**', '')


# ------------------------------------------------------------------ shared fragments
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


CARDS = [
    ('healthcare', 'Healthcare', 'Whose records. Which systems. Since when.',
     'HIPAA starts a 60-day clock the day a breach is discovered.', 'See the healthcare answers'),
    ('financial-services', 'Financial services', 'The examiner asks for the log. Not the policy.',
     'Under Regulation S-P, customers hear within 30 days of you becoming aware. The program has to exist first.',
     'See the financial answers'),
    ('legal', 'Legal', 'The rule says reasonable. Be ready to show it.',
     'ABA Formal Opinion 483: monitor, plan, keep clients informed. Not strict liability. Not optional.',
     'See the legal answers'),
    ('growing-businesses', 'Growing businesses', 'The big client is coming. So is their questionnaire.',
     "Cleared for the deal before it's on paper.", 'See the growth answers'),
]


def cards(base):
    out = []
    for slug, label, q, rule, link in CARDS:
        out.append(f'''<a class="ind-card" href="{base}{slug}/">
        <span class="ip-kicker">{esc(label)}</span>
        <h3 class="ind-q">{esc(q)}</h3>
        <p class="ind-rule">{esc(rule)}</p>
        <span class="ind-link">{esc(link)}<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg></span>
      </a>''')
    return '\n      '.join(out)


def footer(base):
    return f'''<footer class="foot">
  <div class="wrap foot-in">
    <img src="{base}assets/img/trisian-logo.png" alt="Trisian" class="foot-logo">
    <p>Managed IT for regulated industries. 28 years in.</p>
    <nav aria-label="Footer"><a href="{base}#proof">The three answers</a><a href="{base}#plans">Plans</a><a href="{base}#faq">Questions</a><a href="{base}#assessment">Book an assessment</a></nav>
    <div class="foot-col" role="group" aria-label="Who it's for">
      <b>Who it's for</b>
      <a href="{base}who-its-for/">All industries</a>
      <a href="{base}healthcare/">Healthcare</a>
      <a href="{base}financial-services/">Financial services</a>
      <a href="{base}legal/">Legal</a>
      <a href="{base}growing-businesses/">Growing businesses</a>
    </div>
    <small>&copy; 2026 Trisian</small>
  </div>
</footer>'''


def header(base):
    return f'''<header class="nav-wrap">
  <nav class="nav" id="nav" aria-label="Primary">
    <a href="{base}" class="logo" aria-label="Trisian home"><img src="{base}assets/img/trisian-logo.png" alt="Trisian"></a>
    <div class="nav-links" id="navLinks">
      <a href="{base}#proof">The three answers</a>
      <a href="{base}#included">What's included</a>
      {dropdown(base)}
      <a href="{base}#plans">Plans</a>
      <a href="{base}#faq">Questions</a>
      <a href="#assessment" class="btn btn-black btn-sm">Book an assessment</a>
    </div>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="navLinks"><span></span><span></span></button>
  </nav>
</header>'''


def head(page, base, jsonld):
    og = f'''<meta property="og:type" content="website">
<meta property="og:site_name" content="Trisian">
<meta property="og:title" content="{html.escape(page['title'])}">
<meta property="og:description" content="{html.escape(page['desc'])}">
<meta property="og:url" content="{BASE_URL}{page['slug']}/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{html.escape(page['title'])}">
<meta name="twitter:description" content="{html.escape(page['desc'])}">'''
    ld = '\n'.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(page['title'])}</title>
<meta name="description" content="{html.escape(page['desc'])}">
<meta name="robots" content="noindex, nofollow">
<!-- REMOVE noindex AT LAUNCH -->
<link rel="canonical" href="{BASE_URL}{page['slug']}/">
{og}
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%231800AD'/%3E%3Cpath d='M7 9h18v4h-7v11h-4V13H7z' fill='%23fff'/%3E%3C/svg%3E">
<link rel="preload" href="{base}assets/fonts/Archivo.woff2" as="font" type="font/woff2" crossorigin>
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


# ------------------------------------------------------------------ section builders
def split_h(light, black, tag='h1', cls='ip-h1'):
    return f'<{tag} class="{cls}"><span class="lt">{esc(light)}</span> <span class="bk">{esc(black)}</span></{tag}>'


def panel(p, grow=False, stag=None):
    chips = '\n            '.join(
        f'<li style="--r:{r}deg;--i:{i}">{esc(c)}</li>' for i, (c, r) in enumerate(zip(p['chips'], p['tilt'])))
    rows = '\n            '.join(
        f'<li style="--i:{i}"><i></i><span><b>{esc(a)}</b> <span>{esc(b)}</span></span></li>'
        for i, (a, b) in enumerate(p['rows']))
    sty = f' style="--stag:{stag}ms"' if stag else ''
    return f'''<div class="dap{' dap--grow' if grow else ''}" data-dap{sty}>
        <p class="dap-label">Illustration</p>
        <div class="dap-grid">
          <div class="dap-l">
            <p class="dap-ts">{esc(p['ts'])}</p>
            <p class="dap-q">{esc(p['q'])}</p>
            <ul class="dap-chips">
            {chips}
            </ul>
          </div>
          <div class="dap-r">
            <p class="dap-t">{esc(p['title'])}</p>
            <ul class="dap-rows">
            {rows}
            </ul>
          </div>
        </div>
      </div>'''


def hero(pg, surface):
    h = pg['hero']
    grow = pg.get('grow', False)
    return f'''<section class="ip-hero ip-dark {surface}" id="top">
  <div class="ip-wrap ip-hero-grid">
    <div>
      <p class="ip-kicker">{esc(h['kicker'])}</p>
      {split_h(h['light'], h['black'])}
      <p class="ip-sub">{esc(h['sub'])}</p>
      <div class="ip-cta-row">
        <a class="ip-btn on-dark" href="#assessment">{esc(h['primary'])}</a>
        <a class="link-arrow" href="#answers">{esc(h['secondary'])}</a>
      </div>
    </div>
    {panel(pg['panel'], grow, pg.get('stag'))}
  </div>
</section>'''


def photo(img):
    src, alt = img
    return f'''<figure class="ip-photo"><img src="../assets/img/{src}" alt="{html.escape(alt)}" width="1600" height="1066" loading="lazy"></figure>'''


def two_col(h2, bodies, fig, img, note=None):
    paras = '\n        '.join(f'<p>{esc(b)}</p>' for b in bodies)
    n = f'\n        <p class="ip-note">{esc(note)}</p>' if note else ''
    return f'''<section class="ip-s ip-white">
  <div class="ip-wrap ip-two">
    <div class="ip-lead">
      <h2 class="ip-h2">{esc(h2)}</h2>
        {paras}{n}
    </div>
    <div>
      {fig}
      {photo(img)}
    </div>
  </div>
</section>'''


def answers(items):
    cs = []
    for i, (q, a, label, href) in enumerate(items, 1):
        cs.append(f'''<article class="ip-qcard">
        <p class="ip-num" aria-hidden="true">0{i}</p>
        <h3 class="ip-h3">{esc(q)}</h3>
        <p>{t(a)}</p>
        <a class="link-arrow" href="{href}">{esc(label)}</a>
      </article>''')
    return f'''<section class="ip-s ip-grey" id="answers">
  <div class="ip-wrap">
    <h2 class="ip-h2">Three questions. Three answers.</h2>
    <div class="ip-q3">
      {chr(10).join('      ' + c if k else c for k, c in enumerate(cs))}
    </div>
  </div>
</section>'''


def rules(h2, intro, rows, foot, chips=None, head=False):
    tr = '\n          '.join(
        f'<tr><th scope="row">{esc(a)}</th><td data-label="What the meeting asks">{esc(b)}</td><td data-label="What Trisian has ready">{esc(c)}</td></tr>'
        for a, b, c in rows)
    i = f'\n    <p class="ip-intro">{esc(intro)}</p>' if intro else ''
    ch = ''
    if chips:
        ch = f'''
    <div class="ip-chiprow"><p>{esc(chips[0])}</p>
      <ul class="ip-chips">{''.join(f'<li>{esc(c)}</li>' for c in chips[1])}</ul></div>'''
    return f'''<section class="ip-s ip-navy ip-dark">
  <div class="ip-wrap">
    <h2 class="ip-h2" style="color:#fff">{esc(h2)}</h2>{i}
    <table class="rt{' rt--head' if head else ''}">
      <thead><tr><th scope="col">Rule</th><th scope="col">What the meeting asks</th><th scope="col">What Trisian has ready</th></tr></thead>
      <tbody>
          {tr}
      </tbody>
    </table>{ch}
    <p class="ip-note">{esc(foot)}</p>
  </div>
</section>'''


def seats(h2, items):
    cs = '\n      '.join(
        f'<article class="ip-seat"><h3 class="ip-h3">{esc(r)}</h3><p>{esc(w)}</p><p>{esc(g)}</p></article>'
        for r, w, g in items)
    return f'''<section class="ip-s ip-white">
  <div class="ip-wrap">
    <h2 class="ip-h2">{esc(h2)}</h2>
    <div class="ip-seats">
      {cs}
    </div>
  </div>
</section>'''


def plans(items):
    cs = '\n      '.join(
        f'<article class="ip-plan"><h3 class="ip-h3">{esc(n)}</h3><p>{esc(d)}</p></article>' for n, d in items)
    return f'''<section class="ip-s ip-grey">
  <div class="ip-wrap">
    <h2 class="ip-h2">Which plan fits. The assessment decides.</h2>
    <div class="ip-plans">
      {cs}
    </div>
    <p class="ip-plans-link"><a class="link-arrow" href="../#plans">Compare the plans</a></p>
  </div>
</section>'''


def faq(items, h2='Questions'):
    ds = '\n      '.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in items)
    return f'''<section class="ip-s ip-white">
  <div class="ip-wrap">
    <h2 class="ip-h2">{h2}</h2>
    <div class="ip-faq">
      {ds}
    </div>
  </div>
</section>'''


def cta(pg):
    c = pg['cta']
    return f'''<section class="ip-cta ip-indigo" id="assessment">
  <div class="ip-wrap ip-cta-grid">
    <div>
      {split_h(c['light'], c['black'], 'h2', 'ip-h2')}
      <p class="ip-sub">{esc(c['sub'])}</p>
    </div>
    <form class="ip-cta-form" id="form" data-industry="{pg['industry']}" novalidate>
      <label for="f-name">Name<input id="f-name" name="name" autocomplete="name" required></label>
      <label for="f-email">Work email<input id="f-email" name="email" type="email" autocomplete="email" required></label>
      <label for="f-co">Company<input id="f-co" name="company" autocomplete="organization" required></label>
      <label for="f-ind">Industry
        <select id="f-ind" name="industry" required>
          <option value="">Choose one</option>
          {''.join(f'<option{" selected" if o == pg["industry_label"] else ""}>{o}</option>' for o in ['Healthcare', 'Financial services', 'Legal', 'Growing business', 'Other regulated industry'])}
        </select>
      </label>
      <button class="ip-btn on-light" type="submit">{esc(c['button'])}</button>
      <p class="form-msg" id="formMsg" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>'''


def page_shell(pg, base, body, jsonld, with_industry_js=True):
    js = f'<script src="{base}js/common.js"></script>\n' + (f'<script src="{base}js/industry.js"></script>\n' if with_industry_js else '')
    return f'''{head(pg, base, jsonld)}
<body class="ip">
<a class="skip" href="#main">Skip to content</a>
{header(base)}
<main id="main">
{body}
</main>
{footer(base)}
{js}</body>
</html>
'''


# ------------------------------------------------------------------ graphics
def svg_clock_health():
    return '''<figure class="ip-fig"><svg viewBox="0 0 560 150" role="img" aria-label="A line that starts at Discovered, with a bracket labeled 60 days above it.">
        <path class="st" d="M40 92h480"/>
        <circle class="dt" cx="40" cy="92" r="8"/>
        <text x="40" y="128">Discovered</text>
        <path class="st" d="M40 66V54h480v12"/>
        <text x="280" y="38" text-anchor="middle">60 days</text>
      </svg></figure>'''


def svg_clock_fin():
    return '''<figure class="ip-fig"><svg viewBox="0 0 560 210" role="img" aria-label="Three steps: Aware, then 30 days, then Customers notified. A second line beneath: 72 hours, Service provider notifies you.">
        <path class="st" d="M40 70h480"/>
        <circle class="dt" cx="40" cy="70" r="8"/>
        <circle class="dt" cx="520" cy="70" r="8"/>
        <text x="40" y="104">Aware</text>
        <text x="280" y="50" text-anchor="middle">30 days</text>
        <text x="520" y="104" text-anchor="end">Customers notified</text>
        <path class="st" d="M40 160h170"/>
        <circle class="dt" cx="40" cy="160" r="8"/>
        <circle class="dt" cx="210" cy="160" r="8"/>
        <text x="125" y="142" text-anchor="middle">72 hours</text>
        <text x="40" y="194">Service provider notifies you</text>
      </svg></figure>'''


def fig_quote():
    return '''<figure class="ip-fig"><p class="ip-quote ip-q">not a <b>strict liability</b> standard</p>
        <p class="ip-cite">ABA Formal Opinion 483, 2018</p></figure>'''


# ------------------------------------------------------------------ the copy (locked)
FAQ_AZURE = ('What does Azure actually cost us?',
             "What Azure charges. It's billed as a straight pass-through with full visibility, and Trisian adds no markup. We optimize the spend and profit nothing on it.")
FAQ_ASSESS = ('What does an assessment cover?',
              'We review your current environment against the rules you answer to, then tell you where the day-after meeting would go badly today and which plan closes the gap.')
TILT5 = [-1.5, 1, -0.5, 2, -1]
TILT4 = [-1, 1.5, -0.5, 1]

HEALTH = dict(
    slug='healthcare', industry='healthcare', industry_label='Healthcare', surface='ip-navy',
    title='Managed IT for Healthcare Practices and Clinics | Trisian',
    desc='Whose records, which systems, since when. Trisian gives healthcare practices the answers before the meeting. Nightly-reset desktops, Azure at cost.',
    hero=dict(kicker='HEALTHCARE', light='Whose records. Which systems.', black='Since when.',
              sub='Those are the first three questions after an incident in a practice, a clinic or a hospital. Trisian has the answers written before anyone asks.',
              primary='Book a healthcare assessment', secondary='See the three answers'),
    panel=dict(ts='THE DAY AFTER · 8:15 AM', q='Whose records were reachable?',
               chips=["The EHR host says not their system", "Counsel on line two", "Last year's risk analysis, in a binder",
                      "Who has the access list?", "The IT contractor is driving"], tilt=TILT5,
               title='Trisian answers first',
               rows=[('Access log.', 'Already written.'), ('Desktops.', 'Reset at midnight.'), ('Audit trail.', 'On file.'), ('Azure bill.', 'At cost.')]),
    clock=dict(h2='The clock starts when you knew.',
               bodies=["HIPAA's Breach Notification Rule gives you 60 days to notify affected patients, counted from the day a breach is discovered. Discovered means known, or should have been known. Nobody gets to start the clock when the investigation ends. So the meeting after an incident is mostly a meeting about timing.",
                       'Most practices spend it rebuilding a timeline from logs they have to go find. A practice with the answers already on file spends it deciding what to say.'],
               img=('healthcare.webp', 'A clinical lab technician in a protective suit and gloves touching a monitor in a bright white room.')),
    answers=[('Whose records were reachable?',
              '**The Empty Room.** Every desktop resets at night. Patient files and profiles live apart from the session, so whoever got in at midnight finds a room nobody lives in.',
              'How the reset works', '../#answer-1'),
             ('Does a 40-person practice answer to a lower standard?',
              "**Industry-bound, not size-bound.** A 50-person practice carries the same HIPAA exposure as a 5,000-person hospital. Trisian builds to the rule, not the headcount.",
              "Why size doesn't change the rule", '../#answer-2'),
             ('What does the cloud cost, line by line?',
              '**Zero markup.** Azure is billed at cost, straight pass-through, every dollar visible. Trisian optimizes the spend and makes nothing on it. Your administrator can read the invoice.',
              'See the line items', '../#answer-3')],
    rules=dict(h2='The rules in the room.', intro='Three things get asked for, in this order.',
               rows=[('HIPAA Breach Notification Rule', 'How long did you know? Who was affected?', 'Logs and audit trail written before anyone asks. 24/7 monitoring on every plan.'),
                     ('HIPAA Security Rule', 'Show us the risk analysis and the safeguards.', 'Nightly reset. MFA and Conditional Access. Scheduled patching. CIS-hardened images on Advanced.'),
                     ('Vendor oversight', 'Which of your vendors held the data?', 'One contract, one team, one name.')],
               foot='Information, not legal advice. Your counsel decides what applies to your organization.'),
    seats=("Who's in the room.",
           [('The administrator.', 'Wants the audit to stop being an event.', 'Gets plain language, a predictable invoice and one number to call.'),
            ('The IT lead.', 'Wants to look good to leadership without carrying it alone.', 'Gets a co-managed team that takes the off-hours load.'),
            ('The compliance officer.', 'Wants the paper trail before they have to ask for it.', 'Gets it.')]),
    plans=[('Core', 'Single-site practices and clinics, up to 300 users. Business-hours support, 1-hour critical response.'),
           ('Advanced', 'Clinics and groups that run after hours. Unlimited users, 24/7/365 support.'),
           ('Enterprise', 'Multi-site groups and health systems with a security team to feed. SIEM/SOAR, Zero Trust, a named technical account manager, 30-minute critical response.')],
    faq=[('Where do patient files live if the desktop resets every night?',
          'Not on the desktop. Files and profiles are stored separately from the session, so the reset clears the workspace and keeps the work.'),
         ('Does a small practice answer to the same rules as a hospital?',
          'Yes. HIPAA applies by what you do with patient information, not by how many people you employ. Size changes what you can afford to hire to meet it. Trisian builds to the rule, not the headcount.'),
         FAQ_ASSESS, FAQ_AZURE],
    cta=dict(light='Have the answer', black='before the meeting.',
             sub='We review your environment against the rules you answer to. Then we tell you where the meeting would go badly today.',
             button='Book a healthcare assessment'))

FIN = dict(
    slug='financial-services', industry='financial', industry_label='Financial services', surface='ip-black',
    title='Managed IT for Financial Services Firms | Trisian',
    desc='The examiner asks for the log, not the policy. Trisian writes the evidence before anyone asks, with nightly-reset desktops and Azure at cost.',
    hero=dict(kicker='FINANCIAL SERVICES', light='The examiner asks for the log.', black='Not the policy.',
              sub='Regulators measure firms on what they can show. Trisian writes the evidence before anyone asks for it.',
              primary='Book a financial services assessment', secondary='See the three answers'),
    panel=dict(ts='THE DAY AFTER · 2:00 PM', q='What did you know, and when did clients hear it?',
               chips=['The policy binder, last revised in 2023', 'The vendor will investigate', 'Which clients were affected?',
                      'Outside counsel on line two', "The examiner's letter is on the table"], tilt=TILT5,
               title='Trisian answers first',
               rows=[('Access log.', 'Already written.'), ('Desktops.', 'Reset at midnight.'), ('Audit trail.', 'On file.'), ('Azure invoice.', 'At cost.')]),
    clock=dict(h2='Thirty days, and a program that has to exist first.',
               bodies=['Since the 2024 amendments, SEC Regulation S-P requires covered firms to run a written incident response program and to notify affected customers within 30 days of becoming aware of unauthorized access to their sensitive information. Service providers are expected to tell you within 72 hours of discovering a breach.',
                       "Larger firms had to comply by December 3, 2025. Everyone else by June 3, 2026. The date moved. The rule didn't.",
                       "Non-bank lenders, tax preparers and other firms under the FTC's Safeguards Rule have their own version. When a breach involves 500 or more consumers, tell the FTC within 30 days."],
               note="Information, not legal advice. Scope depends on your registration and your counsel's reading.",
               img=('financial-services.webp', 'Two colleagues reviewing a stock chart on a laptop and a printed list of securities.')),
    answers=[('What was reachable, and what did an attacker find?',
              "**The Empty Room.** Every desktop resets at night. Client files and profiles live apart from the session. Someone who got in at 11 PM finds nothing at midnight. That's a short meeting.",
              'How the reset works', '../#answer-1'),
             ("We're small. Does the later date mean a lighter rule?",
              '**Industry-bound, not size-bound.** A later date, not a lighter rule. A 12-person adviser answers to the same rule as a 1,200-person firm. Trisian builds to the rule, not the headcount.',
              "Why size doesn't change the rule", '../#answer-2'),
             ('Can the CFO read the cloud bill?',
              '**Zero markup.** Azure is billed at cost, straight pass-through, every dollar visible. Trisian optimizes the spend and makes nothing on it. The invoice reads like an invoice.',
              'See the line items', '../#answer-3')],
    rules=dict(h2='The rules in the room.', intro=None,
               rows=[('SEC Regulation S-P (2024 amendments)', 'Show us the incident response program and the notice timeline.', 'Logs and audit trails written before anyone asks. 24/7 monitoring on every plan.'),
                     ('FTC Safeguards Rule (GLBA)', 'Show us the controls, and who you told.', 'MFA and Conditional Access. Scheduled patching. Nightly reset.'),
                     ('Service provider oversight', 'Which vendor held the data, and how fast did they tell you?', 'One contract, one team, one name.')],
               chips=('Frameworks Trisian covers', ['SOX', 'PCI-DSS', 'SOC 2', 'GLBA', 'DORA', 'ISO 27001']),
               foot='Information, not legal advice.', head=True),
    seats=("Who's in the room.",
           [('The managing principal.', 'Wants to stop thinking about it.', 'Gets plain language, predictable pricing and proof from firms their size.'),
            ('The CTO.', "Already knows what's broken. Wants to be augmented, not replaced.", "Gets a co-managed partner who works inside the team's decisions."),
            ('The chief compliance officer.', "Wants the evidence on file before the examiner's letter arrives.", 'Gets it.')]),
    plans=[('Core', 'Small advisers, lenders and boutique firms, up to 300 users. Business-hours support, 1-hour critical response.'),
           ('Advanced', 'Firms that serve clients across time zones or run after hours. Unlimited users, 24/7/365 support.'),
           ('Enterprise', 'Firms with a compliance team and an examiner on the calendar. SIEM/SOAR, Zero Trust, a named technical account manager, 30-minute critical response.')],
    faq=[('What does Regulation S-P require now?',
          'A written incident response program, notice to affected customers within 30 days of becoming aware of unauthorized access to their sensitive information, and oversight of service providers, who are expected to notify you within 72 hours of discovering a breach. Compliance dates were December 3, 2025 for larger firms and June 3, 2026 for everyone else. Ask your counsel how it applies to your registration.'),
         ("We're a small adviser. Did the later date mean a lighter rule?", 'A later date, not a lighter rule. The requirements are the same. The calendar was longer.'),
         FAQ_AZURE,
         ('Who do we call at 2 AM?', 'One partner. Advanced and Enterprise run 24/7/365. Enterprise adds a named technical account manager and a 30-minute critical response.')],
    cta=dict(light='Have the answer', black='before the examiner.',
             sub="We review your environment against the rules you answer to. Then we tell you where the day-after meeting would go badly today.",
             button='Book a financial services assessment'))

LEGAL = dict(
    slug='legal', industry='legal', industry_label='Legal', surface='ip-navy', stag=110,
    title='Managed IT for Law Firms | Trisian',
    desc='The rule says reasonable. Be ready to show it. Trisian keeps the evidence on file for law firms, with nightly-reset desktops and Azure at cost.',
    hero=dict(kicker='LEGAL', light='The rule says reasonable.', black='Be ready to show it.',
              sub="ABA Model Rule 1.6(c) asks for reasonable efforts to protect client information. It doesn't ask for the impossible. It asks you to be able to show your work.",
              primary='Book a law firm assessment', secondary='See the three answers'),
    panel=dict(ts='THE DAY AFTER · 9:00 AM', q='Whose files, and have the clients heard it from you?',
               chips=['The matter list, by client', 'The managing partner is on the phone', 'The carrier wants a timeline',
                      "The IT contractor isn't sure yet", 'A client is calling'], tilt=TILT5,
               title='Trisian answers first',
               rows=[('Access log.', 'Already written.'), ('Desktops.', 'Reset at midnight.'), ('Audit trail.', 'On file.'), ('One call.', 'One owner.')]),
    clock=dict(h2="Reasonable is a standard. It's also a test.",
               bodies=['ABA Formal Opinion 483 says lawyers should make reasonable efforts to monitor their systems, keep an incident response plan, and keep current clients informed when a breach touches their matters. It calls the duty "not a strict liability standard."',
                       'Nobody expects an impenetrable firm. Everybody expects one that can explain itself. The explanation is the hard part to produce on the day. So it gets produced before.'],
               note="Your state's version of the rules governs. Information, not legal advice.",
               img=('legal.webp', 'People around a wooden conference table writing on documents, with a laptop and a coffee cup.')),
    answers=[('Whose files were open?',
              '**The Empty Room.** Every desktop resets at night. Documents live in storage, apart from the session, so what a session touched is gone by morning. Someone who got in at midnight finds a room nobody lives in.',
              'How the reset works', '../#answer-1'),
             ('Does a twenty-lawyer firm get a lighter standard?',
              '**Industry-bound, not size-bound.** What counts as reasonable weighs the sensitivity of the information against the cost of the safeguards. Trisian changes the second number. Trisian builds to the rule, not the headcount.',
              "Why size doesn't change the rule", '../#answer-2'),
             ('Can the firm administrator read the cloud bill?',
              '**Zero markup.** Azure is billed at cost, straight pass-through, every dollar visible. Trisian optimizes the spend and makes nothing on it.',
              'See the line items', '../#answer-3')],
    rules=dict(h2='The rules in the room.', intro=None,
               rows=[('ABA Model Rule 1.6(c)', 'What efforts did you make to prevent unauthorized access?', 'Nightly reset. MFA and Conditional Access. Scheduled patching. 24/7 monitoring on every plan.'),
                     ('Model Rule 1.1, technology competence', 'Did you understand the risks of the tools you chose?', 'One partner who explains the environment in plain language.'),
                     ('Model Rule 1.4 and Formal Opinion 483', 'When did you tell the client, and what did you know?', 'A timeline already on file. Logs and audit trails written before anyone asks.')],
               foot="Your state's version of the rules governs."),
    seats=("Who's in the room.",
           [('The managing partner.', 'Wants to stop thinking about it.', 'Gets plain language, predictable pricing and proof from firms their size.'),
            ('The firm administrator.', 'Wants the audit to stop being an event.', 'Gets one invoice, one team, one number to call.'),
            ('The IT manager.', 'Wants to look good to the partners without doing it alone.', 'Gets a co-managed team that takes the off-hours load.')]),
    plans=[('Core', 'Firms up to 300 users. Business-hours support, 1-hour critical response.'),
           ('Advanced', "Closings and trial prep don't keep business hours. Unlimited users, 24/7/365 support."),
           ('Enterprise', 'Large firms and groups with a security function. SIEM/SOAR, Zero Trust, a named technical account manager, 30-minute critical response.')],
    faq=[('What does "reasonable efforts" mean in practice?',
          'ABA Formal Opinion 483 points to monitoring your systems, having an incident response plan, and being able to find out what happened after an event. It calls the duty "not a strict liability standard." The test is whether your efforts were reasonable and whether you can show them.'),
         ('Do we have to tell clients about a breach?',
          "The ABA's view is that Rule 1.4 requires keeping current clients reasonably informed, including about a breach that affects their matters. On former clients, the opinion stops short of requiring notice. Your state's rules and your engagement letters may go further. Ask your ethics counsel."),
         ('Where do client files live if the desktop resets every night?',
          'Not on the desktop. Files and profiles are stored separately from the session, so the reset clears the workspace and keeps the work.'),
         FAQ_AZURE],
    cta=dict(light='Have the answer', black='before the client calls.',
             sub="We review your environment against the rules you answer to. Then we tell you where the day-after meeting would go badly today.",
             button='Book a law firm assessment'))

GROW = dict(
    slug='growing-businesses', industry='growing', industry_label='Growing business', surface='ip-navy', grow=True,
    title='Managed IT for Growing Businesses | Trisian',
    desc="The big client is coming. So is their questionnaire. Trisian builds you to enterprise standards before the first proposal lands.",
    hero=dict(kicker='GROWING BUSINESSES', light='The big client is coming.', black='So is their questionnaire.',
              sub='Growing companies get measured by the standards of the clients they want. Trisian builds you to that standard before the first proposal lands.',
              primary='Book an assessment', secondary='See the three answers'),
    panel=dict(ts='THE DAY THE PROPOSAL ARRIVES · 4:30 PM', q='Can your infrastructure carry a client twice your size?',
               chips=['The proposal is bigger than the last five combined', 'Section 7: describe your ability to scale',
                      'The security questionnaire is due Friday', 'Nobody wants to be the one who answers'], tilt=TILT4,
               title='Trisian answers first',
               rows=[('Scale.', 'No redesign.'), ('Nightly reset.', 'On the record.'), ('Nine frameworks.', 'Mapped.'), ('Azure.', 'At cost.')]),
    clock=dict(h2='The proposal is bigger than the last five combined.',
               bodies=["Somewhere inside it: describe your infrastructure's ability to scale. Then a pause, while everyone waits for someone to admit nobody knows the answer.",
                       "Regulated clients pass their rules down to the vendors they hire. So a thirty-person company ends up answering a bank's questions. Trisian closes the pause before the paperwork goes out."],
               img=('growing-businesses.webp', 'A small team working along a long desk by large windows while one colleague stands and talks.')),
    answers=[('Can you carry a client twice your size?',
              "Yes, and without a rebuild. Core covers up to 300 users. Advanced is unlimited. The architecture is the same on both, so growth doesn't mean redesign.",
              'Compare the plans', '../#plans'),
             ("Will their security team accept your answers?",
              '**The Empty Room.** Every desktop resets at night, and a written answer for each question on the form already exists. Nine frameworks, mapped and ready.',
              'How the reset works', '../#answer-1'),
             ('What does this cost as we grow?',
              '**Zero markup.** Azure is billed at cost, straight pass-through, so growth shows up as your consumption, not as our margin. Every dollar visible.',
              'See the line items', '../#answer-3')],
    proof=dict(h2='What clears the deal.',
               lines=['Nine frameworks named, with what Trisian covers for each.',
                      'A desktop that resets every night, and the log to show it.',
                      'An invoice a procurement team can read in a minute.'],
               link='See the three answers'),
    seats=("Who's in the room.",
           [('The founder or owner.', 'Wants to say yes to the big client without wondering about the servers.', 'Gets plain language and predictable pricing.'),
            ('The operations lead.', 'Wants the next hire to start on day one.', "Gets a desktop that's ready before they are."),
            ('The IT manager.', 'Wants to stop being the answer to every questionnaire.', 'Gets a partner who writes the answers.')]),
    plans=[('Core', 'Up to 300 users. Nightly reset, MFA and Conditional Access, automated patching. Business-hours support, 1-hour critical response.'),
           ('Advanced', 'When you outgrow 300, or when the clients you want need 24/7. Unlimited users, 24/7/365 support.'),
           ('Enterprise', "When a client's security team asks for a SIEM and a named contact. SIEM/SOAR, Zero Trust, a named technical account manager, 30-minute critical response.")],
    faq=[("We're not regulated. Why does this matter?",
          "Your clients are. Regulated companies pass their requirements down to the vendors they hire, and that includes you. Trisian builds you to the standard they'll ask about."),
         ('Is Core enough for us?',
          'Core covers up to 300 users with nightly reset, MFA and Conditional Access, and automated patching, with business-hours support and a 1-hour critical response. The assessment tells you whether the clients you\'re after need more.'),
         ('What happens when we outgrow 300 users?', 'Advanced is unlimited users with 24/7/365 support. Same nightly reset. No redesign.'),
         FAQ_AZURE],
    cta=dict(light='Have the answer', black='before the proposal.',
             sub='We review your environment against the clients you want. Then we tell you where the questionnaire would go badly today.',
             button='Book an assessment'))


def build_industry(pg):
    base = '../'
    fig = {'healthcare': svg_clock_health(), 'financial-services': svg_clock_fin(), 'legal': fig_quote()}.get(pg['slug'], '')
    parts = [hero(pg, pg['surface'])]
    c = pg['clock']
    parts.append(two_col(c['h2'], c['bodies'], fig, c['img'], c.get('note')))
    parts.append(answers(pg['answers']))
    if 'rules' in pg:
        r = pg['rules']
        parts.append(rules(r['h2'], r['intro'], r['rows'], r['foot'], r.get('chips'), r.get('head', False)))
    else:
        p = pg['proof']
        rows = '\n      '.join(f'<div class="ip-proof-row"><p class="ip-num" aria-hidden="true">0{i}</p><p>{esc(l)}</p></div>' for i, l in enumerate(p['lines'], 1))
        parts.append(f'''<section class="ip-s ip-navy ip-dark">
  <div class="ip-wrap">
    <h2 class="ip-h2" style="color:#fff">{esc(p['h2'])}</h2>
    <div class="ip-proof">
      {rows}
    </div>
    <p style="margin-top:32px"><a class="link-arrow" href="../#proof">{esc(p['link'])}</a></p>
  </div>
</section>''')
    parts.append(seats(*pg['seats']))
    parts.append(plans(pg['plans']))
    parts.append(faq(pg['faq']))
    parts.append(cta(pg))
    crumbs = breadcrumbs([('Home', BASE_URL), ("Who it's for", BASE_URL + 'who-its-for/'), (pg['industry_label'] if pg['slug'] != 'growing-businesses' else 'Growing businesses', f"{BASE_URL}{pg['slug']}/")])
    ld = [crumbs, faqld(pg['faq'])]
    return page_shell(pg, base, '\n\n'.join(parts), ld)


HUB = dict(slug='who-its-for',
           title='Who Trisian is for | Healthcare, Financial Services, Legal',
           desc="The room changes. The question doesn't. See how Trisian answers it for healthcare, financial services, legal and growing businesses.")


def build_hub():
    base = '../'
    seats_html = '\n      '.join(
        f'<article class="ip-seat"><h3 class="ip-h3">{esc(r)}</h3><p><b style="font-weight:500;color:var(--ink-1)">{esc(q)}</b></p><p>{esc(b)}</p></article>'
        for r, q, b in [
            ('The CTO', "You already know what's broken.", "You filed the ticket eighteen months ago. We work co-managed: we augment your team, we don't replace it."),
            ('The IT manager', 'The 2am call. And the 9am question.', 'Off your plate, not out of the room. We make you look good to leadership, with receipts.'),
            ('The owner', 'You want to stop thinking about it.', 'Plain language. Predictable pricing. Peers in your industry who already made the call.')])
    body = f'''<section class="ip-hero ip-hub-hero ip-dark ip-navy" id="top">
  <div class="ip-wrap">
    <p class="ip-kicker">WHO IT'S FOR</p>
    {split_h("The room changes.", "The question doesn't.")}
    <p class="ip-sub">After an incident, every regulated business ends up in a meeting. The people are different. The first question is the same: what did you know, and when? Pick your room.</p>
  </div>
</section>

<section class="ip-s ip-grey">
  <div class="ip-wrap">
    <h2 class="sr-only">Industries</h2>
    <div class="ind-grid">
      {cards('../')}
    </div>
  </div>
</section>

<section class="ip-s ip-white">
  <div class="ip-wrap">
    <h2 class="ip-h2">One table. Every seat covered.</h2>
    <p class="ip-sub" style="margin-top:0">Between seven and twelve people weigh in on this decision. Each one needs a different answer. Same table, same partner.</p>
    <div class="ip-seats">
      {seats_html}
    </div>
  </div>
</section>

<section class="ip-s ip-tint ip-strip">
  <div class="ip-wrap">
    <h3 class="ip-h3">Not on the list?</h3>
    <p>Tell us the regulator you answer to. We'll tell you if we fit. If we don't, we'll say so.</p>
    <a class="ip-btn on-light" href="../#assessment">Book an assessment</a>
  </div>
</section>

<section class="ip-cta ip-indigo ip-cta-center ip-dark" id="assessment">
  <div class="ip-wrap">
    {split_h("Have the answer", "before the meeting.", "h2", "ip-h2")}
    <p style="margin-top:32px"><a class="ip-btn on-indigo" href="../#assessment">Book an assessment</a></p>
  </div>
</section>'''
    crumbs = breadcrumbs([('Home', BASE_URL), ("Who it's for", BASE_URL + 'who-its-for/')])
    return page_shell(HUB, base, body, [crumbs], with_industry_js=False)


# ------------------------------------------------------------------ run
def write(slug, content):
    d = os.path.join(SITE, slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    pages = [HEALTH, FIN, LEGAL, GROW]
    problems = []
    for pg in pages + [HUB]:
        if len(pg['title']) > 60:
            problems.append(f"title too long ({len(pg['title'])}): {pg['slug']}")
        if len(pg['desc']) > 155:
            problems.append(f"description too long ({len(pg['desc'])}): {pg['slug']}")
    for pg in pages:
        write(pg['slug'], build_industry(pg))
    write('who-its-for', build_hub())
    # no em or en dashes in anything we wrote
    for slug in [p['slug'] for p in pages] + ['who-its-for']:
        txt = open(os.path.join(SITE, slug, 'index.html'), encoding='utf-8').read()
        if chr(0x2014) in txt or chr(0x2013) in txt:
            problems.append(f'dash character found in {slug}')
    print('titles/desc:', [(p['slug'], len(p['title']), len(p['desc'])) for p in pages + [HUB]])
    print('PROBLEMS:' if problems else 'checks passed', *problems, sep='\n  ')
    sys.exit(1 if problems else 0)

# Photos: client-supplied, one per industry page (see img= in each page's clock section).
# SKIPPED (tagged [HOLD] in the spec; nothing from these renders):
#   healthcare: Business associate agreement row; SOC 2 and ISO 27001 due-diligence row; proof slot
#   financial services: notification-window line; attestation-status line; proof slot
#   legal: client security questionnaires and outside counsel guidelines row; proof slot
#   growing businesses: proof slot
