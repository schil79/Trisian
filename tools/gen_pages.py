#!/usr/bin/env python3
"""Generates the secondary pages: /coverage/, /services/, /insights/ and the article template (Directive v2 sections 7 to 9).

    python3 tools/gen_pages.py

Copy is locked in the directive. Items tagged [CONFIRM] or [HOLD] are listed in OMITTED at the bottom.
No em dashes anywhere in this file or its output.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import *
from icons import ic
from data import CMP, Y, NO

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
B = '../'


def shell(slug, title, desc, body, active, jsonld=(), base=B, depth_js=True):
    return f'''{head_common(base, title, desc, slug, jsonld)}
<body class="page">
<a class="skip" href="#main">Skip to content</a>
{header(base, active=active)}
<main id="main">
{body}
</main>
{footer(base)}
<script src="{base}js/common.js"></script>
<script src="{base}js/main.js"></script>
<script src="{base}js/pages.js"></script>
</body>
</html>
'''


def write(slug, content):
    d = os.path.join(SITE, slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(content)


def split_h1(a, b, a_bold=False):
    """centered page H1 in the Light and Black split. Directive order: first clause Light, last clause Black, unless a_bold."""
    ca, cb = ('bd', 'lt') if a_bold else ('lt', 'bd')
    return f'<h1 class="page-h1" data-split-lines><span class="{ca}">{esc(a)}</span> <span class="{cb}">{esc(b)}</span></h1>'


def hero(label, h1, sub, buttons='', photo=''):
    return f'''<section class="page-hero">
  <div class="wrap">
    <span class="pill">{esc(label)}</span>
    {h1}
    <p class="sub-p" data-reveal>{esc(sub)}</p>
    {f'<div class="cta-row">{buttons}</div>' if buttons else ''}
    {photo}
  </div>
</section>'''


def band(bold, light, sub, cta):
    """indigo call-to-action band (no form): a headline, one line, one button."""
    label, href = cta
    l = f'<span class="lt">{esc(light)}</span>' if light else ''
    sb = f'<p class="sub-p">{esc(sub)}</p>' if sub else ''
    return f'''<section class="sec s-indigo band">
  <div class="wrap" data-reveal>
    <h2 class="h2 on-dark"><span class="bd">{esc(bold)}</span>{l}</h2>
    {sb}
    <a class="btn btn-w" href="{href}" data-magnet>{esc(label)}</a>
  </div>
</section>'''


def head2(bold, light=None, sub=None, pill_=None, cls=''):
    p = f'<span class="pill">{esc(pill_)}</span>' if pill_ else ''
    l = f'<span class="lt">{esc(light)}</span>' if light else ''
    s = f'<p class="sub-p">{esc(sub)}</p>' if sub else ''
    return f'<header class="sec-head {cls}" data-reveal>{p}<h2 class="h2"><span class="bd">{esc(bold)}</span>{l}</h2>{s}</header>'


# ================================================================== COVERAGE
def cell(v):
    if v == Y:
        return f'<span class="yes">{ic("check", 18)}<span class="sr-only">Included</span></span>'
    if v == NO:
        return '<span class="no">Not included</span>'
    return esc(v)


def compare():
    trs = ''
    for grp, rows in CMP:
        trs += f'<tr class="grp"><th colspan="4" scope="colgroup">{esc(grp)}</th></tr>'
        for r in rows:
            trs += f'<tr><th scope="row">{esc(r[0])}</th>' + ''.join(f'<td>{cell(v)}</td>' for v in r[1:]) + '</tr>'
    table = f'''<table class="cmp-t">
        <thead><tr><th scope="col">Capability</th><th scope="col">Core</th><th scope="col">Advanced</th><th scope="col">Enterprise</th></tr></thead>
        <tbody>{trs}</tbody>
      </table>'''
    cards_ = ''
    for ci, name in enumerate(['Core', 'Advanced', 'Enterprise'], 1):
        body = ''
        for grp, rows in CMP:
            body += f'<h4>{esc(grp)}</h4><dl>' + ''.join(f'<div><dt>{esc(r[0])}</dt><dd>{cell(r[ci])}</dd></div>' for r in rows) + '</dl>'
        cards_ += f'<section class="cmp-card" aria-label="{name} in full"><h3 class="h4">{name}</h3>{body}</section>'
    return f'''<p class="legend"><span><span class="yes">{ic("check", 16)}</span> Included</span><span><span class="no">Not included</span> Not part of the level</span></p>
      {table}
      <div class="cmp-cards">{cards_}</div>'''


def build_coverage():
    four = [('user', 'Your size', 'Users and sites.'), ('filecheck', 'Your rules', 'The regulators you answer to.'),
            ('clock', 'Your hours', 'When your people actually work.'), ('gauge', 'Your appetite', 'How much you want us to own.')]
    fb = ''.join(f'<article class="box"><span class="box-ico">{ic(n, 30)}</span><h3 class="h4">{esc(t_)}</h3><p>{esc(b)}</p></article>' for n, t_, b in four)
    ladder = '''<div class="ladder anim" id="ladder" role="img" aria-label="Three coverage levels as steps. Core: nightly reset, MFA, patching. Advanced adds 24/7 support and hardened images. Enterprise adds SIEM, Zero Trust and a named person. Same architecture at every level.">
      <p class="ladder-note" aria-hidden="true"><span>Same architecture at every level</span></p>
      <div class="ladder-bars" aria-hidden="true">
        <div class="lb lb-ent" style="--w:100%;--i:2"><span class="seg s-a">Nightly reset, MFA, patching</span><span class="seg s-b">24/7 support, hardened images</span><span class="seg s-c">SIEM, Zero Trust, named person</span></div>
        <div class="lb lb-adv" style="--w:72%;--i:1"><span class="seg s-a">Nightly reset, MFA, patching</span><span class="seg s-b">24/7 support, hardened images</span></div>
        <div class="lb lb-core" style="--w:42%;--i:0"><span class="seg s-a">Nightly reset, MFA, patching</span></div>
      </div>
      <p class="ladder-keys" aria-hidden="true"><b>Enterprise</b><b>Advanced</b><b>Core</b></p>
    </div>'''

    def card(cls, name, one, facts, topic, chip=''):
        fr = ''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in facts)
        return f'''<article class="lvl {cls}">
        {chip}
        <h3 class="h3">{name}</h3><p class="one">{esc(one)}</p>
        <dl>{fr}</dl>
        <a class="link-arrow" href="#assessment?topic={topic}">Talk this through</a>
      </article>'''
    cards3 = (card('l-pale', 'Core', 'The nightly reset, MFA and patching, for up to 300 people.', [('Users', 'Up to 300'), ('Support', 'Business hours'), ('Critical response', '1 hour')], 'core') +
              card('l-peri', 'Advanced', 'Everything in Core, with the lights on 24/7.', [('Users', 'Unlimited'), ('Support', '24/7/365'), ('Critical response', '1 hour')], 'advanced', '<span class="badge">Most selected</span>') +
              card('l-indigo', 'Enterprise', 'The full stack: SIEM, Zero Trust and a named person.', [('Users', 'Unlimited'), ('Support', '24/7 priority'), ('Critical response', '30 minutes'), ('Also', 'Dedicated team and a named technical account manager')], 'enterprise'))
    which = [('One office, standard hours, a small team', 'Core'), ('Clients in other time zones, work that runs after hours', 'Advanced'),
             ('Regulated, with a security function to feed and an auditor on the calendar', 'Enterprise'), ('Somewhere in between', 'Tell us. We’ll build the blend')]
    wr = ''.join(f'<li><span>{esc(a)}</span><b>{esc(b)}</b></li>' for a, b in which)
    addons = ['Compliance log archival up to 7+ years', 'Advanced user experience monitoring', 'SIEM/SOAR', 'Email threat protection', 'Emergency readiness retainers']
    billing = [('layers', 'Platform fee', 'Per user, per month. Everything that runs on its own is in it: monitoring, patching, security updates, Microsoft 365 licensing.'),
               ('clock', 'Support hours', 'A contracted minimum for the work people do. Every hour logged, categorized and reported monthly.'),
               ('compass', 'Projects', 'Migrations, security builds, compliance programs. Scoped up front, quoted separately.'),
               ('cloud', 'Azure', 'At cost. Not a line we profit from.')]
    bl = ''.join(f'<article class="box box-w"><span class="box-ico">{ic(n, 30)}</span><h3 class="h4">{esc(a)}</h3><p>{esc(b)}</p></article>' for n, a, b in billing)
    faq = [('How does pricing work?', 'Three lines. A per-user monthly platform fee that covers everything automated, including Microsoft 365 licensing. Contracted support hours for the human work, every hour logged. And projects, scoped and quoted separately. Azure is billed at cost, with no markup.'),
           ('How do we know which level fits?', 'The assessment decides. We score your security, performance and compliance against your user count, your industry and your regulators, then recommend a starting point and show our reasoning.'),
           ('Can we move up later?', 'Yes. The architecture is the same at every level, so moving from Core to Advanced or Enterprise doesn’t mean a redesign.'),
           ('What happens outside business hours?', 'Advanced and Enterprise include 24/7/365 support at the same rate. Every level has emergency escalation through your named contacts.')]
    fq = ''.join(f'<details><summary><span>{esc(q)}</span>{ic("plus", 22)}</summary><p>{esc(a)}</p></details>' for q, a in faq)
    body = f'''{hero('Coverage', split_h1('Coverage,', 'tailored on a call.'),
        'Every client gets the same architecture and the same nightly reset. What changes is how much of the day after we cover: hours, depth, support and services. Core, Advanced and Enterprise are starting points. The call tailors them.',
        f'<a class="btn" href="#assessment" data-magnet>Book an assessment</a><a class="btn btn-o" href="#starting-points" data-magnet>See the starting points</a>',
        ph('21:9', 'two leaders at a table, mid-conversation, a closed laptop and a notebook', 'Two business leaders in conversation at a table'))}

<section class="sec s-pale" id="no-checkout">
  <div class="wrap">
    {head2("You won't find a buy button here.", None, 'Every engagement starts with an assessment, because the right coverage depends on four things.')}
    <div class="boxes4" data-stagger>{fb}</div>
  </div>
</section>

<section class="sec s-white" id="starting-points">
  <div class="wrap">
    {head2('Three starting points.', 'The same nightly reset.')}
    {ladder}
    <div class="lvls" data-stagger>{cards3}</div>
  </div>
</section>

<section class="sec s-grey" id="which">
  <div class="wrap">
    {head2('Which one sounds like you?')}
    <ul class="which" data-stagger><li class="which-h"><span>If this sounds like you</span><b>We’d start with</b></li>{wr}</ul>
  </div>
</section>

<section class="sec s-pale" id="make-it-yours">
  <div class="wrap two-ph">
    {ph('4:3', 'a team at a whiteboard sketching a plan', 'A small team sketching a plan on a whiteboard')}
    <div data-reveal="right">
      <h2 class="h2 left"><span class="bd">The levels bend.</span><span class="lt">The nightly reset doesn’t.</span></h2>
      <p class="sub-p left">Mix support hours to fit. Add what you need without changing levels. Put projects on top. Add what your regulators ask for.</p>
      <ul class="chips chips-w">{''.join(f'<li>{esc(a)}</li>' for a in addons)}</ul>
    </div>
  </div>
</section>

<section class="sec s-white" id="compare">
  <div class="wrap">
    {head2('Compare every line.')}
    <div class="compare-open">{compare()}</div>
  </div>
</section>

<section class="sec s-grey" id="billing">
  <div class="wrap">
    {head2('Three lines on the invoice.', 'Nothing hiding.', "You always know what you're paying for, what's included and what's billable before any work begins.", 'Transparent by design')}
    <div class="boxes4" data-stagger>{bl}</div>
    {'<p class="signoff" data-reveal>Hours, not adjectives.</p>'}
  </div>
</section>

<section class="sec s-white" id="faq">
  <div class="wrap">
    {head2('Questions.')}
    <div class="faq-list" data-stagger>{fq}</div>
  </div>
</section>

{form_band('Have the answer', 'before the meeting.', 'We review your environment against the rules you answer to. Then we tell you where the day-after meeting would go badly today.')}'''
    from data import FAQ
    return shell('coverage', 'Coverage and billing | Trisian',
                 'Core, Advanced and Enterprise are starting points. Every Trisian engagement is tailored on a call. See how coverage and billing work.',
                 body, 'coverage', [breadcrumbs([('Home', BASE_URL), ('Coverage', BASE_URL + 'coverage/')]),
                                    faqld(faq)])


# ================================================================== SERVICES
GROUPS = [
    ('migrations', 'Migrations', 'How you get on.', 'Every way onto Safe Workspace, from wherever you are today.',
     'boxes being unpacked in a server closet', 'A cleared server closet with equipment being removed', 'Project',
     [('cloud', 'Safe Workspace Migration', 'A full move onto the platform with zero-downtime cutover and every user onboarded.'),
      ('server', 'VDI Migration, on-prem to cloud', 'From physical or virtual servers in your building to cloud desktops on Azure.'),
      ('layers', 'Citrix to AVD Migration', 'Off Citrix and onto Azure Virtual Desktop, with profiles and configurations intact.'),
      ('monitor', 'VMware Horizon Migration', 'From Horizon to Azure Virtual Desktop, with the infrastructure redesigned and applications repackaged.'),
      ('compass', 'Multi-site and global deployment', 'Safe Workspace in more regions, under one set of rules, with failover across them.'),
      ('mail', 'Email and cross-tenant migration', 'Microsoft 365 tenant moves for mergers and restructures, plus migrations from other email systems.')]),
    ('security', 'Security', 'How your defenses get built.', 'Identity, access and detection, designed in and tuned.',
     'an engineer reviewing a monitor wall from behind, screens unreadable', 'An engineer at a desk in a quiet operations center', 'Project',
     [('target', 'Zero Trust Architecture', 'Continuous verification in place of the VPN. Nobody is trusted because of where they sit.'),
      ('key', 'Privileged Identity Management', 'Just-in-time admin access, approval workflows, credential rotation and a full audit trail.'),
      ('activity', 'Microsoft Sentinel SIEM', 'Threat detection, analytics and automated response in one place.'),
      ('radar', 'Defender XDR Integration', 'Endpoints, email, identity and cloud apps seen as one.'),
      ('filecheck', 'Data Loss Prevention', 'Microsoft Purview rules across endpoints, email and cloud, with automatic labeling.'),
      ('user', 'Passwordless Authentication', 'Windows Hello, FIDO2 keys and Authenticator. Nothing for a phisher to steal.')]),
    ('compliance', 'Compliance', 'How you become audit-ready.', 'Risk analysis, controls and evidence, built for the rules you answer to.',
     'a compliance officer reviewing tabbed printouts at a desk', 'A compliance officer reviewing tabbed documents at a desk', 'Project',
     [('file-text', 'Compliance Program', 'Risk analysis, controls and audit preparation, built for the rules you answer to.'),
      ('filecheck', 'SOC 2 Type II Preparation', 'Assessment against the trust criteria, gaps fixed, evidence collected automatically.'),
      ('activity', 'HIPAA Security Risk Assessment', 'A full risk analysis with a remediation roadmap and a map of where patient data flows.'),
      ('gauge', 'Compliance Gap Analysis', 'Measured against HIPAA, SOC 2, PCI-DSS, DORA and SOX, with a plan to close each gap.'),
      ('grid', 'Compliance Suite Deployment', 'Microsoft Purview with evidence collection, control monitoring and dashboards.'),
      ('receipt', 'SOX and Financial Controls', 'IT general controls, FINRA and SEC configuration, and segregation of duties.')]),
    ('infrastructure', 'Infrastructure and recovery', 'How the unexpected gets handled.', "Performance, cost and recovery, planned before they're needed.",
     'a data center aisle, cool light, no readable labels', 'A quiet data center aisle', 'Project',
     [('desktop', 'AVD and Citrix Deployment', 'Azure Virtual Desktop with Nerdio, or Citrix Cloud DaaS with optional NetScaler ADC.'),
      ('percent', 'Nerdio and Cost Optimization', 'Auto-scaling, reserved instances, savings plans and right-sizing, so you pay for work, not idle hours.'),
      ('backup', 'DR Architecture and Site Recovery', 'Multi-region failover, Veeam backup and Azure Site Recovery, with recovery targets defined up front.'),
      ('compass', 'Network Architecture and SD-WAN', 'LAN and WAN tuned for virtual desktops, with ExpressRoute and software-defined WAN.'),
      ('cloud', 'Azure Infrastructure Deployment', 'Virtual machines, networking and storage built for virtualization workloads.'),
      ('gauge', 'ControlUp UX Monitoring', 'Live session performance, analytics and automated fixes.')]),
    ('ongoing', 'Ongoing protection', 'How protection keeps going.', 'Managed security and compliance, under annual contract.',
     'a small operations team at a shared desk in the evening', 'A small operations team working at a shared desk in the evening', 'Annual contract',
     [('radar', 'Managed Detection and Response', '24/7 threat monitoring, detection and active response, on an annual contract.'),
      ('monitor', 'Managed SOC Services', 'A fully managed security operations center, powered by Sentinel.'),
      ('filecheck', 'Managed Compliance Monitoring', 'Continuous watch on your compliance posture, with regulatory reporting.'),
      ('clock', 'Incident Response Retainer', 'Pre-paid response hours and an agreed response time for fast containment.')]),
]


def build_services():
    move = '''<figure class="move anim" data-viz="move">
      <svg viewBox="0 0 640 250" class="move-svg" role="img" aria-label="Three starting points, Citrix, VMware Horizon and servers on site, each moving to Safe Workspace on Azure Virtual Desktop">
        <g class="mv-chips" font-family="Graphik,Helvetica,Arial,sans-serif" font-size="16" font-weight="500">
          <rect x="4" y="22" width="180" height="44" rx="22" fill="none" stroke="#1800AD" stroke-width="1.5"/><text x="94" y="50" text-anchor="middle" fill="#191919">Citrix</text>
          <rect x="4" y="103" width="180" height="44" rx="22" fill="none" stroke="#1800AD" stroke-width="1.5"/><text x="94" y="131" text-anchor="middle" fill="#191919">VMware Horizon</text>
          <rect x="4" y="184" width="180" height="44" rx="22" fill="none" stroke="#1800AD" stroke-width="1.5"/><text x="94" y="212" text-anchor="middle" fill="#191919">Servers on site</text>
        </g>
        <g fill="none" stroke="#1800AD" stroke-width="1.5">
          <path class="mv-l" pathLength="1" d="M184 44C300 44 320 125 420 125"/>
          <path class="mv-l" pathLength="1" d="M184 125H420"/>
          <path class="mv-l" pathLength="1" d="M184 206C300 206 320 125 420 125"/>
        </g>
        <g class="mv-tile"><rect x="420" y="50" width="216" height="150" rx="20" fill="#1800AD"/>
          <text x="528" y="112" text-anchor="middle" fill="#fff" font-family="Graphik,Helvetica,Arial,sans-serif" font-size="20" font-weight="700">Safe Workspace</text>
          <text x="528" y="140" text-anchor="middle" fill="#C7CBFA" font-family="Graphik,Helvetica,Arial,sans-serif" font-size="14" font-weight="500">on Azure Virtual Desktop</text></g>
      </svg>
    </figure>'''
    how = [('target', 'Scope', 'Deliverables, timeline and what done looks like, agreed up front.'),
           ('receipt', 'Quote', 'A written quote for that scope before work starts.'),
           ('check-circle', 'Finish', 'Defined deliverables, delivered. Then the project closes.')]
    hw = ''.join(f'<article class="box"><span class="box-ico">{ic(n, 30)}</span><h3 class="h4">{esc(a)}</h3><p>{esc(b)}</p></article>' for n, a, b in how)
    tabs = ''.join(f'<button class="g-tab" role="tab" type="button" id="tab-{k}" data-g="{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{esc(name)}</button>'
                   for i, (k, name, *_r) in enumerate(GROUPS))
    panels = ''
    for i, (k, name, h, sub, scene, alt, chip, items) in enumerate(GROUPS):
        cards_ = ''.join(f'''<article class="gcard"><span class="box-ico sm">{ic(n, 24)}</span><h3 class="h4">{esc(t_)}</h3><p>{esc(b)}</p><span class="chip">{chip}</span></article>'''
                         for n, t_, b in items)
        panels += f'''<div class="g-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}"{'' if i == 0 else ' data-off'} tabindex="0">
        <header class="sec-head"><h3 class="h2 h2-m"><span class="bd">{esc(h)}</span></h3><p class="sub-p">{esc(sub)}</p></header>
        {ph('16:5', scene, alt, 'ph-band')}
        <div class="gcards">{cards_}</div>
      </div>'''
    body = f'''{hero('Services', split_h1('Scoped. Quoted.', 'Finished.'),
        'Beyond running your Safe Workspace, Trisian takes on projects that change your environment. Each one has a defined scope, a quote and a finish line.',
        '', ph('21:9', 'an IT lead and an engineer at a whiteboard mapping a migration', 'Two IT colleagues mapping a migration on a whiteboard'))}

<section class="sec s-white"><div class="wrap">{move}</div></section>

<section class="sec s-pale" id="how-a-project-runs">
  <div class="wrap">
    {head2('How a project runs.')}
    <div class="boxes3" data-stagger>{hw}</div>
  </div>
</section>

<section class="sec s-white" id="groups">
  <div class="wrap">
    {head2('Five groups of work.')}
    <div class="g-tabs" role="tablist" aria-label="Service groups" id="gTabs">{tabs}</div>
    <div class="g-panels" id="gPanels">{panels}</div>
  </div>
</section>

{band("Tell us where you're starting from.", '', "Citrix, VMware, a server closet or something in between. We'll scope the way out.", ('Scope the way out', B + '#assessment?topic=services'))}'''
    return shell('services', 'Services: migrations, security, compliance | Trisian',
                 'Project-based work to move you onto Safe Workspace, build your defenses and get you audit-ready. Scoped, quoted and finished.',
                 body, 'services', [breadcrumbs([('Home', BASE_URL), ('Services', BASE_URL + 'services/')])])


# ================================================================== INSIGHTS
CATS = [('security', 'Security', 'key'), ('compliance', 'Compliance', 'filecheck'), ('performance', 'Performance', 'gauge'), ('pov', 'Point of view', 'compass')]
POSTS = [
    ('security', 'What a desktop does at midnight', 'Wiping every desktop every night changes what a breach is worth. How the reset works, and what it doesn’t touch.'),
    ('compliance', 'DORA, in plain English', 'What the regulation asks of the people running your technology, and what you should be able to see in writing.'),
    ('performance', 'Paying for the work, not the idle hours', 'How auto-scaling and schedules bring the Azure bill in line with what your people actually do.'),
    ('pov', 'The real fear isn’t the hacker. It’s the auditor.', 'Dek to be written with the article.'),
    ('pov', 'They want a single pane of glass. They know it’s a lie.', 'Dek to be written with the article.'),
    ('pov', 'The highest status symbol in IT is never talking about it.', 'Dek to be written with the article.'),
    ('pov', 'Finger-pointing costs more than the outage ever did.', 'Dek to be written with the article.'),
    ('pov', 'A 24/7 line is worthless if the person answering can’t fix anything.', 'Dek to be written with the article.'),
]


def build_insights():
    catname = {k: n for k, n, _ in CATS}
    chips = '<button class="f-chip" type="button" aria-pressed="true" data-f="all">All</button>' + ''.join(
        f'<button class="f-chip" type="button" aria-pressed="false" data-f="{k}">{ic(i, 20)}<span>{esc(n)}</span></button>' for k, n, i in CATS)
    cat, title, dek = POSTS[0]
    feat = f'''<article class="feat" data-cat="{cat}" data-reveal>
      {ph('16:9', 'a person reading on a tablet in a quiet office', 'A person reading on a tablet in a quiet office')}
      <div class="feat-t"><span class="chip">{catname[cat]}</span><span class="chip soon">Coming soon</span><h2 class="h3">{esc(title)}</h2><p>{esc(dek)}</p><a class="link-arrow" href="template/">Read</a></div>
    </article>'''
    cs = ''
    for cat, title, dek in POSTS[1:]:
        cs += f'''<article class="post" data-cat="{cat}">
        {ph('3:2', 'an editorial scene to be photographed', 'Image placeholder for the article ' + title)}
        <div class="post-t"><div class="post-chips"><span class="chip">{catname[cat]}</span><span class="chip soon">Coming soon</span></div><h3 class="h4">{esc(title)}</h3><p>{esc(dek)}</p><a class="link-arrow" href="template/">Read</a></div>
      </article>'''
    body = f'''{hero('Insights', split_h1('Answers,', 'in writing.'), "28 years inside regulated environments. What we've learned about security, compliance and infrastructure, said plainly.")}

<section class="sec s-white" id="library">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filter by category" id="filters">{chips}</div>
    {feat}
    <div class="posts" id="posts" data-stagger>{cs}</div>
    <p class="f-empty" id="fEmpty" hidden>Nothing in this category yet.</p>
  </div>
</section>

{band('Want us to write the answer', 'to yours?', '', ('Send us your question', B + '#assessment?topic=question'))}'''
    return shell('insights', 'Insights | Trisian',
                 "28 years inside regulated environments. What we've learned about security, compliance and infrastructure, said plainly.",
                 body, 'insights', [breadcrumbs([('Home', BASE_URL), ('Insights', BASE_URL + 'insights/')])])


def build_article():
    """one reusable template, no articles. Every element the directive lists, with labelled placeholders."""
    b = '../../'
    body = f'''<article class="article">
  <header class="art-head">
    <div class="wrap">
      <span class="chip">Category</span>
      <h1 class="art-h1">Article title, set in the display face, centered, about eighteen characters a line</h1>
      <p class="sub-p">The dek sits here: one or two sentences that say what the reader will be able to do afterward.</p>
      <p class="byline" hidden>Author &middot; Date</p>
    </div>
  </header>
  <div class="wrap">
    {ph('16:9', 'an editorial scene to be photographed', 'Image placeholder for the article hero')}
    <div class="art-body">
      <p>Body copy runs in a 680px column, 18px on a 1.7 line height. It is written per article, with sources, before it ships.</p>
      <blockquote class="pull">A pull quote sits between two hairlines, in the display face, centered.</blockquote>
      <p>More body copy continues here.</p>
      <aside class="callout"><b>Callout.</b> A solid pale blue box for a fact or a definition worth keeping.</aside>
      <p>The closing paragraph sits here.</p>
    </div>
    <section class="related" aria-label="Related articles">
      <h2 class="h3">Related</h2>
      <div class="posts">{''.join(f'<article class="post">{ph("3:2", "related article image", "Related article image placeholder")}<div class="post-t"><span class="chip">Category</span><h3 class="h4">Related article title</h3><a class="link-arrow" href="{b}insights/">Read</a></div></article>' for _ in range(3))}</div>
    </section>
  </div>
</article>
{band('Want us to write the answer', 'to yours?', '', ('Send us your question', b + '#assessment?topic=question'))}'''
    html_ = shell('insights/template', 'Article template | Trisian', 'Reusable article template for the Insights library.', body, 'insights',
                  [breadcrumbs([('Home', BASE_URL), ('Insights', BASE_URL + 'insights/')])], base=b)
    html_ = html_.replace('<a class="btn" href="#assessment"', '<a class="btn" href="#assessment"')
    return html_


if __name__ == '__main__':
    write('coverage', build_coverage())
    write('services', build_services())
    write('insights', build_insights())
    write('insights/template', build_article())
    for s in ['coverage', 'services', 'insights', 'insights/template']:
        t = open(os.path.join(SITE, s, 'index.html'), encoding='utf-8').read()
        assert chr(0x2014) not in t and chr(0x2013) not in t, s
    print('wrote coverage, services, insights, insights/template')

# [CONFIRM] / [HOLD] items that render nothing:
OMITTED = [
    'Coverage FAQ, after hours: the 15-minute escalation target is [CONFIRM]; clause left out.',
    'Coverage: whether the nine frameworks apply on every level is [CONFIRM]; per-tier framework lists are not rendered. Every comparison row is [CONFIRM] against the contract.',
    'Insights: all articles are Coming soon. Do not launch with Coming soon cards. Hide the nav item if fewer than three articles are live.',
    'Insights: author and date line hidden until supplied.',
]
