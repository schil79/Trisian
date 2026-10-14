#!/usr/bin/env python3
"""Generates site/index.html (the home page).

Not part of the site build. The site is plain static files; this exists so the locked copy from
Trisian_Site_Upgrade_Directive.md lives in one place. Edit here, run, commit the output:

    python3 tools/gen_home.py [outdir]      (default: site/)

Items the directive tags [CONFIRM] or [HOLD] are listed at the bottom of this file in OMITTED.
No em dashes anywhere in this file or its output.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import *
import iso, scenes

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'site')
BASE = ''                       # home page lives at the site root
LD = iso.ICONS


def ico(name, size=24):
    return iso.icon_svg(name, size)


def h2(bold, light=None, cls='', light_first=False):
    a = f'<span class="bd">{esc(bold)}</span>'
    if light is None:
        return f'<h2 class="h2 {cls}">{a}</h2>'
    b = f'<span class="lt">{esc(light)}</span>'
    return f'<h2 class="h2 {cls}">{b + a if light_first else a + b}</h2>'


def pill(text, cls=''):
    return f'<span class="pill {cls}">{esc(text)}</span>'


def sign(text):
    return f'<p class="signoff">{esc(text)}</p>'


# ------------------------------------------------------------------ hero
ROOMS = [
    ('healthcare', 'Healthcare', ['HIPAA', 'HITECH'], 'healthcare/'),
    ('financial', 'Financial services', ['SOX', 'GLBA', 'PCI-DSS', 'DORA'], 'financial-services/'),
    ('legal', 'Legal', ['SOC 2', 'GDPR'], 'legal/'),
]
ROOM_DATA = {k: {'stamp': scenes.ROOMS[k][0], 'q': ' '.join(scenes.ROOMS[k][1]), 'chips': c, 'href': BASE + href}
             for k, _, c, href in ROOMS}
ROOM_DATA['default'] = {'stamp': scenes.ROOMS['default'][0], 'q': ' '.join(scenes.ROOMS['default'][1]), 'chips': [], 'href': ''}


def widget(cls='', ident='', done=False):
    label = 'Answered' if done else 'Answers on file'
    n = 3 if done else 1
    return f'''<div class="pw {cls}{' done' if done else ''}"{ident} aria-hidden="true" data-pw style="--p:{n * 100 / 3:.1f}%">
        <span class="pw-label" data-pw-label>{label}</span>
        <span class="pw-bar"><i></i></span>
        <span class="pw-row"><span class="pw-dots"><i class="on"></i><i{' class="on"' if n > 1 else ''}></i><i{' class="on"' if n > 2 else ''}></i></span><b class="pw-n"><span data-pw-n>{n}</span> / 3</b></span>
      </div>'''


def hero():
    tabs = ''.join(
        f'<button class="rt-tab" role="tab" id="tab-{k}" type="button" aria-selected="false" aria-controls="roomPanel" '
        f'data-room="{k}" tabindex="{0 if i == 0 else -1}">{esc(label)}</button>'
        for i, (k, label, _, _) in enumerate(ROOMS))
    return f'''<section class="hero" id="top-hero">
  <div class="wrap">
    <a class="banner" href="#proof"><span>Managed IT for regulated industries</span><span class="banner-go">See how{ico('arrow-right', 16)}</span></a>
    <h1 class="h1"><span class="u">Answered</span> in <span class="adv">advance</span></h1>
    <div class="hero-grid">
      <div class="hero-copy">
        <p class="sub"><span>One bad day from a very specific meeting.</span><span>Not the day of the breach. The day after.</span><span>What you knew, and when. Trisian writes that answer before you need it.</span></p>
        <div class="cta-row">
          <a href="#assessment" class="btn">Book an assessment</a>
          <a href="#proof" class="btn btn-o">Read the three answers</a>
        </div>
      </div>
      <div class="stage anim" id="stage">
        {widget('pw-hero', ' id="heroPw"', True)}
        <p class="sr-only">Answers on file: 3 of 3. Answered.</p>
        <div class="stage-svg">{scenes.hero(BASE)}{scenes.hero(BASE, True)}</div>
        <div class="rt-bar">
          <span class="rt-label" id="rtLabel">Pick your room</span>
          <div class="rt-tabs" role="tablist" aria-labelledby="rtLabel" id="roomTabs">{tabs}</div>
        </div>
        <script type="application/json" id="roomData">{json.dumps(ROOM_DATA)}</script>
        <div class="rt-panel" id="roomPanel" role="tabpanel" aria-live="polite" hidden>
          <p class="sr-only" id="roomSr"></p>
          <ul class="chips" id="roomChips"></ul>
          <a class="link-arrow" id="roomLink" href="#">See this room</a>
        </div>
      </div>
    </div>
  </div>
</section>'''


FRAMEWORKS = [  # name, industries it matches on hover
    ('HIPAA', 'healthcare'), ('SOC 2', 'legal growing'), ('PCI-DSS', 'financial'), ('GDPR', 'legal growing'),
    ('SOX', 'financial'), ('DORA', 'financial'), ('CMMC', ''), ('GLBA', 'financial'), ('ISO 27001', 'growing'),
]
CHIP_MAP = {'HITECH': 'healthcare'}


def receipts():
    chips = ''.join(f'<li class="chip" data-ind="{ind}"><i></i>{esc(n)}</li>' for n, ind in FRAMEWORKS)
    return f'''<section class="receipts" id="receipts">
  <div class="wrap">
    <p class="rc-kicker">Hours, not adjectives.</p>
    <ul class="rc-grid anim" id="rcGrid">
      <li><b class="num"><span data-count="28">28</span></b><span>years in healthcare, finance and law. Since 1998.</span></li>
      <li><b class="num"><span data-count="9">9</span></b><span>frameworks, named, mapped, on file.</span></li>
      <li><b class="num">24/7</b><span>monitoring on every plan.</span></li>
      <li><b class="num"><span data-count="30">30</span><small> min</small></b><span>critical response on Enterprise.</span></li>
    </ul>
    <div class="strip">
      <p>Nine frameworks. One answer for each.</p>
      <div class="marquee" aria-label="Frameworks covered">
        <ul class="mq-track">{chips}</ul>
        <ul class="mq-track mq-dup" aria-hidden="true">{chips}</ul>
      </div>
    </div>
  </div>
</section>'''


# ------------------------------------------------------------------ the meeting
def meeting():
    scr = ['Logs from vendor A', 'Call vendor B', 'Who had access?', 'What was patched?', 'Legal on line two', '“Unfortunately…”']
    rot = [-4, 3, -2, 5, -5, 3]
    chips = ''.join(f'<li style="--r:{r}deg">{esc(s)}</li>' for s, r in zip(scr, rot))
    ready = ['Every desktop wiped at midnight', 'Exposure mapped to your regulation', 'Azure billed at cost, line by line']
    rows = ''.join(f'<li><i class="dot"></i>{esc(r)}</li>' for r in ready)
    return f'''<section class="sec s-grey" id="meeting">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      {pill('The meeting')}
      {h2('Not why it happened.', 'What you knew, and when.')}
      <p class="sub-p">Most companies spend that morning building the answer from scratch. Gathering logs. Calling vendors. Learning the word &ldquo;unfortunately.&rdquo; <b>Trisian answers it first.</b></p>
    </header>
    <div class="versus" data-reveal>
      <div class="vs vs-scratch">
        <span class="vs-tag">Built the day after</span>
        <ul class="scatter" aria-label="What the morning after looks like">{chips}</ul>
        <p class="vs-foot">Written by people who are already losing.</p>
      </div>
      <div class="vs-mid" aria-hidden="true"><span class="step-pill">Trisian answers first {ico('arrow-right', 16)}</span></div>
      <div class="vs vs-ready">
        <span class="vs-tag">Already written</span>
        <ul class="ready">{rows}</ul>
        <p class="vs-foot">Ready before anyone asks.</p>
      </div>
    </div>
    {sign('Answer it first.')}
  </div>
</section>'''


# ------------------------------------------------------------------ the three answers
def answers():
    return f'''<section class="sec s-white answers" id="proof">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      {pill('The three answers')}
      {h2('Written before', 'the question.')}
      <p class="sub-p">Three proofs, not three promises. Each one is something you can check.</p>
    </header>
    <div class="ans-list" id="ansList">
      <div class="pw-rail"><div class="pw-sticky">{widget('pw-side', ' id="sidePw"')}</div></div>

      <article class="ans a-navy" id="answer-1" data-ans="1">
        <div class="ans-copy">
          <span class="ans-label">Answer 1 of 3</span>
          <h3 class="h3">The Empty Room</h3>
          <p class="lead">A hacker gets in at midnight. At 6am there's nothing to find.</p>
          <p>Every Trisian desktop wipes itself clean every night. Think of a hotel room: checked in, used, checked out, reset for the next guest. Nothing lingers. Files and profiles are stored apart from the session, so nobody loses a day of work and nobody finds a trace of it.</p>
          <p class="stat">What was on that machine? <b>Nothing.</b></p>
        </div>
        <figure class="ans-viz anim" data-viz="room">
          {scenes.room(BASE)}
          <div class="rs-bar"><span class="rs-time" data-rs-time>00:00</span><span class="rs-track"><i data-rs-fill></i></span><span class="rs-pct" data-rs-pct>Reset 100%</span></div>
        </figure>
      </article>

      <article class="ans a-tint" id="answer-2" data-ans="2">
        <div class="ans-copy">
          <span class="ans-label">Answer 2 of 3</span>
          <h3 class="h3">Industry-Bound, Not Size-Bound</h3>
          <p class="lead">The regulator doesn't grade on a curve.</p>
          <p>A 50-person practice carries the same HIPAA exposure as a 5,000-person hospital. The small firm needs the big firm's infrastructure and can't afford the big firm's IT department. Trisian builds to the rule, not the headcount.</p>
          <p class="stat">Same exposure. <b>Same answer.</b></p>
        </div>
        <figure class="ans-viz anim" data-viz="bound">
          {scenes.bound(BASE)}
          <div class="bd-dots">
            <div><span class="dots" data-dots="1" aria-hidden="true"></span><b>50-person practice</b></div>
            <div><span class="dots" data-dots="100" aria-hidden="true"></span><b>5,000-person hospital</b></div>
          </div>
          <figcaption class="bd-key"><i></i> 1 dot = 50 people</figcaption>
        </figure>
      </article>

      <article class="ans a-white" id="answer-3" data-ans="3">
        <div class="ans-copy">
          <span class="ans-label">Answer 3 of 3</span>
          <h3 class="h3">Zero Markup</h3>
          <p class="lead">Azure billed at cost. We make nothing on it.</p>
          <p>Straight pass-through. Every dollar visible. Trisian optimizes the spend and takes no margin on it. Ask your current provider to say that sentence out loud.</p>
          <p class="stat">Trisian's cut of your Azure bill: <b>0%.</b></p>
        </div>
        <figure class="ans-viz anim" data-viz="markup">
          {scenes.markup(BASE)}
        </figure>
      </article>
    </div>
    {sign('Not protection. Proof.')}
  </div>
</section>'''


# ------------------------------------------------------------------ one name on the line
def onename():
    rows = ['Every issue has an owner, an SLA and a resolution path.',
            'Critical response in 1 hour on Core and Advanced. 30 minutes on Enterprise.',
            'After hours, every plan has emergency escalation through your named contacts.']
    li = ''.join(f'<li>{ico("check", 20)}<span>{esc(r)}</span></li>' for r in rows)
    return f'''<section class="sec s-navy" id="onename">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      {pill('One partner', 'on-dark')}
      {h2('One contract.', 'One team. One name.')}
      <p class="sub-p">The day something breaks isn't the failure. It's the day Trisian shows up.</p>
    </header>
    <div class="one-grid">
      <figure class="one-l anim" data-viz="vendors">
        {scenes.vendors(BASE)}
        <figcaption>Six vendors. Six answers. One word: &ldquo;unfortunately.&rdquo;</figcaption>
      </figure>
      <div class="one-r" data-reveal>
        <div class="trisian-slab">
          <p class="ts-name">Trisian</p>
          <ul>{li}</ul>
        </div>
      </div>
    </div>
    {sign('One partner. One answer.')}
  </div>
</section>'''


# ------------------------------------------------------------------ safe workspace
def product():
    tiles = [
        ('server', 'The desktop', 'Windows desktops in the cloud, on Azure or Citrix. Sessions reset after each use. Profiles and files stay put.'),
        ('key', 'The defense', 'MFA and Conditional Access from day one. Hardened images and behavioral detection as the plan climbs. Encrypted at rest and in transit.'),
        ('layers', 'The headroom', 'Auto-scaling follows real demand. Off-hours cost drops on schedule. Ten users or unlimited, with no redesign.'),
        ('file-check', 'The paper trail', 'Evidence collected automatically. Audit trails that can’t be edited. Controls mapped to nine frameworks.'),
    ]
    tl = ''.join(f'''<article class="slab-card">
        <div class="tile-wrap">{iso.tile(ic, "light", f"pt{i}")}</div>
        <h3 class="h4">{esc(t_)}</h3>
        <p>{esc(b)}</p>
      </article>''' for i, (ic, t_, b) in enumerate(tiles))

    bento = [
        ('b-a navy', 'moon', 'dark', 'Nightly reset', 'Every desktop wipes clean. Files and profiles stay put.', '00:00'),
        ('b-b tint', 'percent', 'tint', 'Azure at cost', 'Straight pass-through. Full visibility.', '0%'),
        ('b-c', 'activity', 'light', '24/7 monitoring', 'Platform monitoring runs around the clock.', None),
        ('b-d', 'grid', 'light', 'Microsoft 365, included', 'Licensing sits inside the platform fee. One less vendor.', None),
        ('b-e', 'refresh', 'light', 'Patching on schedule', 'OS and Microsoft 365 updates land without a ticket.', None),
        ('b-f', 'layers', 'light', 'One golden image', 'One managed desktop image, backed up weekly and kept for four weeks.', None),
    ]
    bt = ''
    for i, (c, ic, kind, t_, b, big) in enumerate(bento):
        mark = f'<span class="bignum">{big}</span>' if big else f'<div class="tile-wrap">{iso.tile(ic, kind, f"bt{i}")}</div>'
        bt += f'''<article class="b {c}">
        {mark}
        <div><h3 class="h4">{esc(t_)}</h3><p>{esc(b)}</p></div>
      </article>'''
    return f'''<section class="sec s-white" id="product">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      {pill('The product')}
      {h2('Safe Workspace.')}
      <p class="sub-p lead-p">Your whole digital environment, run by one partner.</p>
      <p class="sub-p">A cloud desktop on Azure Virtual Desktop or Citrix Cloud, with security, licensing, monitoring, compliance and support built in. Your people log in. Everything else is our job.</p>
    </header>
    <div class="tiles4" data-stagger>{tl}</div>

    <header class="sec-head sec-head--sub" id="included" data-reveal>
      {h2('Every plan starts with', 'the same six things.', cls='h2-s')}
      <p class="sub-p">One managed platform, one accountable team, nothing bolted on afterward.</p>
    </header>
    <div class="bento" data-stagger>{bt}</div>
  </div>
</section>'''


# ------------------------------------------------------------------ billing
def billing():
    rows = [
        ('layers', 'Platform fee', 'Per user, per month. Everything that runs on its own is in it: monitoring, patching, security updates, Microsoft 365 licensing.'),
        ('clock', 'Support hours', 'A contracted minimum for the work people do. Every hour logged, categorized and reported monthly.'),
        ('compass', 'Projects', 'Migrations, security builds, compliance programs. Scoped up front, quoted separately.'),
        ('cloud', 'Azure', 'At cost. Not a line we profit from.'),
    ]
    li = ''.join(f'''<li class="inv-row">
        <div class="tile-wrap">{iso.tile(ic, "light", f"bl{i}")}</div>
        <h3 class="h4">{esc(a)}</h3>
        <p>{esc(b)}</p>
      </li>''' for i, (ic, a, b) in enumerate(rows))
    return f'''<section class="sec s-grey" id="billing">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      {pill('Transparent by design')}
      {h2('Three lines on the invoice.', 'Nothing hiding.')}
      <p class="sub-p">You always know what you're paying for, what's included and what's billable before any work begins.</p>
    </header>
    <ol class="invoice" data-stagger>{li}</ol>
    {sign('Hours, not adjectives.')}
  </div>
</section>'''


# ------------------------------------------------------------------ find your room
def rooms():
    return f'''<section class="sec s-black" id="rooms">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      {pill("Who it's for", 'on-dark')}
      {h2('Find your room.')}
    </header>
    <div class="ind-grid" data-stagger>
      {cards(BASE)}
    </div>
  </div>
</section>'''


# ------------------------------------------------------------------ one table
def seats():
    return f'''<section class="sec s-white" id="seats">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      {pill("Who it's for")}
      {h2('One table.', 'Every seat covered.')}
      <p class="sub-p">Seven to twelve people touch this decision. Each one is afraid of something different.</p>
      <a class="link-arrow" href="{BASE}who-its-for/">Pick your room.</a>
    </header>
    <div class="seats-grid" data-stagger>
      <figure class="s-photo s-table"><img src="assets/img/table.webp" alt="Four colleagues working and talking around a long table" width="1600" height="1066" loading="lazy"></figure>
      <article class="seat"><h3 class="h4">The CTO</h3><p class="q">You already know what's broken.</p><p>You filed the ticket eighteen months ago. We work co-managed: we augment your team, we don't replace it.</p></article>
      <article class="seat"><h3 class="h4">The IT manager</h3><p class="q">The 2am call. And the 9am question.</p><p>Off your plate, not out of the room. We make you look good to leadership, with receipts.</p></article>
      <article class="seat"><h3 class="h4">The owner</h3><p class="q">You want to stop thinking about it.</p><p>Plain language. Predictable pricing. Peers in your industry who already made the call.</p></article>
      <figure class="s-photo s-close"><img src="assets/img/closeup.webp" alt="A woman at her desk listening closely" width="1600" height="1066" loading="lazy"><figcaption>The 9am question is coming. Have the answer.</figcaption></figure>
    </div>
  </div>
</section>'''


# ------------------------------------------------------------------ plans
# rows from section 6 of Trisian_Website_Architecture.html. A dash in the source renders as "Not included".
Y = '✓'
NO = 'none'
CMP = [
    ('Workspace and infrastructure', [
        ('Microsoft 365 License', 'Business Premium', 'E3', 'E5'),
        ('CIS-Hardened Images', NO, Y, Y),
        ('Customized Industry Images', NO, NO, Y),
        ('Multi-Region Infrastructure', NO, NO, Y)]),
    ('Security', [
        ('Endpoint Protection', 'Standard AV', 'Behavioral (P1)', 'Full EDR + Hunting (P2)'),
        ('Email Security', 'Anti-spam', 'Advanced anti-phishing', 'Attack simulation'),
        ('Identity Protection', 'MFA + CA', 'Risk-based sign-in', 'PIM + P2'),
        ('Data Loss Prevention', 'Basic', 'Enhanced', 'Advanced + auto-label'),
        ('SIEM/SOAR + Zero Trust', NO, NO, Y)]),
    ('Monitoring', [
        ('24×7 Platform Monitoring', Y, Y, Y),
        ('User Experience Monitoring', NO, Y, Y)]),
    ('Compliance', [
        ('Audit Log Retention', '180 days', '180 days', '1 year'),
        ('eDiscovery', 'Standard', 'Standard', 'Premium'),
        ('Automated Compliance Suite', NO, NO, Y)]),
    ('Support and SLA', [
        ('Support Window', 'Business Hours', '24/7/365', '24/7/365'),
        ('P1 Critical Response', '1 hour', '1 hour', '30 minutes'),
        ('P2 High Response', '4 hours', '4 hours', '2 hours'),
        ('Dedicated Team + TAM', NO, NO, Y)]),
]


def cell(v):
    if v == Y:
        return f'<span class="yes">{ico("check", 18)}<span class="sr-only">Included</span></span>'
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
    return f'''<details class="compare">
      <summary><span>Compare every line</span>{ico("arrow-right", 20)}</summary>
      <div class="cmp-body">
        <p class="legend"><span><span class="yes">{ico("check", 16)}</span> Included</span><span><span class="no">Not included</span> Not part of the plan</span></p>
        {table}
        <div class="cmp-cards">{cards_}</div>
      </div>
    </details>'''


def plans():
    return f'''<section class="sec s-grey" id="plans">
  <!-- Tier names are placeholders pending the Core/Advanced/Enterprise vs Standard/Premium/Financial Secure Suite decision. -->
  <div class="wrap">
    <header class="sec-head" data-reveal>
      {pill('Plans')}
      {h2('Three plans.', 'The same nightly reset.')}
      <p class="sub-p">Every plan includes the empty room, Azure at cost, Microsoft 365 licensing and 24/7 platform monitoring. Each one adds to the last.</p>
    </header>
    <div class="tiers" data-stagger>
      <article class="tier">
        <h3 class="h4">Core</h3><p class="one">The nightly reset, MFA and patching, for up to 300 people.</p><p class="who">For smaller regulated teams</p>
        <dl><div><dt>Users</dt><dd>Up to 300</dd></div><div><dt>Support</dt><dd>Business hours</dd></div><div><dt>Critical response</dt><dd>1 hour</dd></div></dl>
        <ul><li>Microsoft 365 Business Premium</li><li>Non-persistent desktops</li><li>MFA and Conditional Access</li><li>Automated patching</li></ul>
      </article>
      <article class="tier feat">
        <span class="badge">Most selected</span>
        <h3 class="h4">Advanced</h3><p class="one">Everything in Core, with the lights on 24/7.</p><p class="who">For teams that can't go dark</p>
        <dl><div><dt>Users</dt><dd>Unlimited</dd></div><div><dt>Support</dt><dd>24/7/365</dd></div><div><dt>Critical response</dt><dd>1 hour</dd></div></dl>
        <ul><li>Everything in Core</li><li>Microsoft 365 E3</li><li>CIS-hardened images</li><li>Behavioral threat detection</li></ul>
      </article>
      <article class="tier">
        <h3 class="h4">Enterprise</h3><p class="one">The full stack: SIEM, Zero Trust and a named person.</p><p class="who">For the most exposed environments</p>
        <dl><div><dt>Users</dt><dd>Unlimited</dd></div><div><dt>Support</dt><dd>24/7 priority</dd></div><div><dt>Critical response</dt><dd>30 minutes</dd></div></dl>
        <ul><li>Everything in Advanced</li><li>Microsoft 365 E5</li><li>SIEM/SOAR and Zero Trust</li><li>Dedicated team and named technical account manager</li></ul>
      </article>
    </div>
    {compare()}
    <div class="addons">
      <h3 class="h4">Add what you need, keep your plan</h3>
      <p>Compliance log archival up to 7+ years. Advanced user experience monitoring. SIEM/SOAR. Email threat protection. Emergency readiness retainers.</p>
    </div>
    <div class="center"><a href="#assessment" class="btn">Find your plan: book an assessment</a></div>
  </div>
</section>'''


# ------------------------------------------------------------------ day 1 to day 90
def process():
    steps = [
        ('Assess', 'We map your security, performance and compliance against the rules you answer to. You get the gaps in writing.'),
        ('Design', 'We build the Safe Workspace around your applications, your regulators and your growth plan.'),
        ('Deploy', 'Pilot group first. Then everyone, with training and a check at each stage.'),
        ('Operate', 'We run it. Monitoring, patching, security, tuning. Your team doesn’t file tickets for any of it.'),
        ('Review', 'Every quarter: what changed in your rules, what changed in your business, what we adjust.'),
    ]
    li = ''.join(f'''<li class="step" style="--i:{i}">
        <span class="node" aria-hidden="true"></span>
        <p class="numeral" aria-hidden="true">{i + 1}</p>
        <article class="slab-card"><h3 class="h4"><span class="sr-only">{i + 1}. </span>{esc(a)}</h3><p>{esc(b)}</p></article>
      </li>''' for i, (a, b) in enumerate(steps))
    return f'''<section class="sec s-white" id="process">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      {pill('What happens after you call')}
      {h2('From first call', 'to steady state.')}
    </header>
    <ol class="steps anim" id="steps">{li}</ol>
    <div class="phases" data-reveal>
      <p><b>Days 1 to 30:</b> platform and pilot</p>
      <p><b>Days 31 to 60:</b> full migration and training</p>
      <p><b>Days 61 to 90:</b> optimization, compliance validation, steady state</p>
    </div>
    <p class="phase-cap">Timeline scales with the size of the environment.</p>
  </div>
</section>'''


def services():
    items = ['Citrix to Azure Virtual Desktop', 'VMware Horizon to Azure Virtual Desktop', 'On-prem VDI to the cloud', 'Tenant and email migrations for M&amp;A']
    li = ''.join(f'<li class="slab-card o">{ico("arrow-right", 20)}<span>{s}</span></li>' for s in items)
    return f'''<section class="sec s-tint" id="services">
  <!-- "See all services" link is held until /services/ exists -->
  <div class="wrap">
    <header class="sec-head" data-reveal>
      {h2('part of the job.', 'Getting here is', light_first=True)}
      <p class="sub-p">Migrations, security builds and compliance programs, scoped and quoted separately.</p>
    </header>
    <ul class="svc4" data-stagger>{li}</ul>
  </div>
</section>'''


# ------------------------------------------------------------------ faq
FAQ = [
    ('What exactly is Safe Workspace?',
     "A cloud desktop environment built on Azure Virtual Desktop or Citrix Cloud. It bundles Microsoft 365, endpoint security, monitoring, compliance and support into one platform, run entirely by Trisian. Your team logs in. We handle everything underneath."),
    ('If desktops wipe every night, what happens to our files?',
     "They stay. Profiles and files live in separate, managed storage, so people sign in to a fresh desktop with their work exactly where they left it. Only the machine resets."),
    ('Which regulations do you cover?',
     "HIPAA, SOC 2, PCI-DSS, GDPR, SOX, DORA, CMMC, GLBA and ISO 27001. The assessment maps them to your business, so you see which ones actually apply to you."),
    ('How does pricing work?',
     "Three lines. A per-user monthly platform fee that covers everything automated, including Microsoft 365 licensing. Contracted support hours for the human work, every hour logged. And projects, scoped and quoted separately. Azure is billed at cost, with no markup."),
    ('Do you replace our IT team?',
     "No. Trisian works co-managed and augments the people you already have. Your team keeps the context. We take the load and the 2am calls."),
    ('How do we know which plan fits?',
     "The assessment decides. We score your security, performance and compliance against your user count, your industry and your regulators, then recommend a plan and show our reasoning."),
    ('What happens outside business hours?',
     "Advanced and Enterprise include 24/7/365 support at the same rate. Every plan has emergency escalation through your named contacts."),
    ('How long does it take to go live?',
     "A typical rollout runs 90 days. Days 1 to 30: platform and pilot group. Days 31 to 60: full migration and training. Days 61 to 90: optimization, compliance validation and steady state. Bigger environments take longer."),
    ('Can you move us off Citrix or VMware?',
     "Yes. We migrate from Citrix and VMware Horizon to Azure Virtual Desktop, keeping profiles and settings. Migrations are scoped and quoted as projects."),
    ('What happens in an assessment?',
     "We review your current environment against the rules you answer to, then tell you where the day-after meeting would go badly today and which plan closes the gap."),
    ('What does Azure actually cost us?',
     "What Azure charges. It's billed as a straight pass-through with full visibility, and Trisian adds no markup. We optimize the spend and profit nothing on it."),
]


def faq():
    ds = '\n      '.join(f'<details><summary><span>{esc(q)}</span>{ico("plus", 22)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)
    return f'''<section class="sec s-white" id="faq">
  <div class="wrap faq-in">
    <header class="sec-head" data-reveal>
      {pill('Questions')}
      {h2('What people ask', 'before they call.')}
    </header>
    <div class="faq-list">
      {ds}
    </div>
  </div>
</section>'''


def form():
    return f'''<section class="sec s-indigo" id="assessment">
  <div class="wrap">
    <div class="cta">
      <div class="cta-copy">
        <h2 class="h2 on-dark"><span class="bd">Have the answer</span><span class="lt">before the meeting.</span></h2>
        <p class="sub-p">We review your environment against the rules you answer to. Then we tell you where the day-after meeting would go badly today.</p>
      </div>
      <div class="form-card">
        <form class="form" id="form" novalidate>
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


# ------------------------------------------------------------------ page
def build():
    title = 'Trisian | Answered in Advance'
    desc = 'Managed IT for healthcare, financial services and legal. Trisian answers the day-after question before anyone asks it.'
    org = {'@context': 'https://schema.org', '@type': 'Organization', 'name': 'Trisian', 'url': BASE_URL,
           'email': 'contact@trisian.com', 'description': desc}
    head = head_common(BASE, title, desc, '', [org, faqld(FAQ)], home=True)
    head = head.replace('<meta name="theme-color"', '<meta name="theme-color"')
    body = f'''<body>
<a class="skip" href="#top">Skip to content</a>
{header(BASE)}
<main id="top">
{hero()}
{receipts()}
{meeting()}
{answers()}
{onename()}
{product()}
{billing()}
{rooms()}
{seats()}
{plans()}
{process()}
{services()}
{faq()}
{form()}
</main>
{footer(BASE)}
<script src="js/common.js"></script>
<script src="js/main.js"></script>
</body>
</html>
'''
    path = os.path.join(OUT, 'index.html')
    open(path, 'w').write(head + '\n' + body)
    print('wrote', path, len(head + body), 'bytes')


# [CONFIRM] / [HOLD] items from the directive that render nothing (also listed in docs/upgrade-report.md):
OMITTED = [
    'FAQ "What happens outside business hours?": the 15-minute engagement target is [CONFIRM]; the clause is left out.',
    'One name on the line, row 3: "We aim to be on it in 15 minutes." left out for the same reason.',
    'One name on the line: all response times are [CONFIRM] against the contract; 1 hour and 30 minutes are as already live on the plans.',
    'Plans: framework lists per tier from the old architecture are not rendered.',
    'Form: phone line not rendered until the client supplies one.',
    'Footer: legal entity wording, Privacy Policy and Terms of Service not rendered.',
    'Services: "See all services" link held until /services/ exists.',
    'Industry pages: client matter segregation [CONFIRM], BAA line [HOLD].',
]

if __name__ == '__main__':
    build()
