#!/usr/bin/env python3
"""Generates site/index.html (the home page) per Trisian_Site_Directive_v2.

Not part of the site build. The site is plain static files. Edit copy here, run, commit the output:

    python3 tools/gen_home.py [outdir]      (default: site/)

Items the directive tags [CONFIRM] or [HOLD] are listed at the bottom in OMITTED.
No em dashes anywhere in this file or its output.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import *
import icons, scenes
from icons import ic
from data import FAQ

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'site')
BASE = ''


def pill(text, cls=''):
    return f'<span class="pill {cls}">{esc(text)}</span>'


def sign(text, cls=''):
    return f'<p class="signoff {cls}" data-reveal>{esc(text)}</p>'


def hl(s):
    """*phrase* becomes a highlight span. The asterisks never render."""
    import re
    return re.sub(r'\*(.+?)\*', r'<span class="hl">\1</span>', esc(s))


# ------------------------------------------------------------------ hero
def pool_tiles(n, cls='pt'):
    mon = ('<svg viewBox="0 0 40 34" aria-hidden="true"><rect class="scr" x="2" y="2" width="36" height="22" rx="4"/>'
           '<path class="stand" d="M20 24v5M12 30h16"/><path class="wl w1" d="M8 9h14"/><path class="wl w2" d="M8 14h20"/>'
           '<path class="wl w3" d="M8 19h10"/><rect class="cur" x="27" y="16" width="2" height="5"/></svg>')
    return ''.join(f'<div class="{cls}" style="--i:{i}">{mon}</div>' for i in range(n))


def hero():
    return f'''<section class="hero" id="top-hero">
  <div class="hero-grid-bg" id="heroBg" aria-hidden="true"></div>
  <div class="wrap hero-in">
    <a class="banner" href="#answers" data-reveal><span>Managed IT for regulated industries</span><span class="banner-go">See how{ic('arrow-right', 16)}</span></a>
    <h1 class="h1"><span class="u">Answered</span> in <span class="adv">advance</span></h1>
    <p class="hero-sub" data-reveal>Every regulated business is one bad day from a very specific meeting. Not the day of the breach. The day after. What you knew, and when you knew it. <b>Trisian writes that answer</b> before you need it.</p>
    <div class="cta-row" data-reveal>
      <a href="#assessment" class="btn" data-magnet>Book an assessment</a>
      <a href="#answers" class="btn btn-o" data-magnet>Read the 3 answers</a>
    </div>
    <div class="hpanel anim" id="hpanel" data-reveal="scale">
      <span class="scr-chip c1" aria-hidden="true">Logs from vendor A</span>
      <span class="scr-chip c2" aria-hidden="true">Legal on line two</span>
      <span class="scr-chip c3" aria-hidden="true">Who has the access list?</span>
      <span class="scr-chip c4" aria-hidden="true">&ldquo;Unfortunately&hellip;&rdquo;</span>
      <div class="hp-card" data-depth="8">
        <div class="hp-q">
          <p class="hp-tag">The day after &middot; 9:00 AM</p>
          <p class="hp-ask">What did you know, and when?</p>
          <p class="hp-status"><i></i><span class="s-a">Building the answer</span><span class="s-b">Answered</span></p>
        </div>
        <ul class="hp-rows">
          <li style="--i:0"><span class="ck">{ic('check', 16)}</span><div><b>Nothing to Find</b><span>Every desktop wiped at midnight.</span></div>
            <div class="mini mini-pool" aria-hidden="true">{pool_tiles(6, 'mp')}</div></li>
          <li style="--i:1"><span class="ck">{ic('check', 16)}</span><div><b>Industry-Bound</b><span>Built to the regulation, not your headcount.</span></div>
            <div class="mini mini-dots" aria-hidden="true"><i class="one"></i><span><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span></div></li>
          <li style="--i:2"><span class="ck">{ic('check', 16)}</span><div><b>Zero Markup</b><span>Azure billed at cost. Line by line.</span></div>
            <div class="mini mini-bar" aria-hidden="true"><i></i><em>0%</em></div></li>
        </ul>
      </div>
    </div>
  </div>
</section>'''


FRAMEWORKS = [
    ('HIPAA', 'healthcare'), ('SOC 2', 'legal growing'), ('PCI-DSS', 'financial'), ('GDPR', 'legal growing'),
    ('SOX', 'financial'), ('DORA', 'financial'), ('CMMC', ''), ('GLBA', 'financial'), ('ISO 27001', 'growing'),
]


def receipts():
    chips = ''.join(f'<li class="chip">{esc(n)}</li>' for n, ind in FRAMEWORKS)
    return f'''<section class="receipts" id="receipts">
  <div class="wrap">
    <p class="rc-kicker" data-reveal>Hours, not adjectives.</p>
    <ul class="rc-grid" id="rcGrid" data-stagger>
      <li><b class="num"><span data-count="28">28</span></b><span>years in business. Since 1998, in healthcare, finance and law.</span></li>
      <li><b class="num"><span data-count="9">9</span></b><span>frameworks, named, mapped, on file.</span></li>
      <li><b class="num">24/7</b><span>monitoring, for every client.</span></li>
      <li><b class="num"><span data-count="30">30</span><small> min</small></b><span>critical response, top coverage level.</span></li>
    </ul>
    <div class="strip" data-reveal>
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
    chips = ''.join(f'<li style="--r:{r}deg;--i:{i}">{esc(s)}</li>' for i, (s, r) in enumerate(zip(scr, rot)))
    ready = ['Every desktop reset at midnight', 'Exposure mapped to your regulation', 'Azure billed at cost, line by line']
    rows = ''.join(f'<li style="--i:{i}"><span class="ck">{ic("check", 16)}</span>{esc(r)}</li>' for i, r in enumerate(ready))
    return f'''<section class="sec s-white" id="meeting">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      {pill('The meeting')}
      <h2 class="h2"><span class="line"><span class="bd">Not why</span> <span class="lt">it happened.</span></span><span class="line"><span class="lt">What you knew, and when.</span></span></h2>
      <p class="sub-p">Most companies spend that morning building the answer from scratch. Gathering logs. Calling vendors. Learning the word &ldquo;unfortunately.&rdquo; Trisian answers it first.</p>
    </header>
    <div class="versus" id="versus">
      <div class="vs vs-scratch" data-reveal="left">
        <span class="vs-tag">Built the day after</span>
        <ul class="scatter" aria-label="What the morning after looks like">{chips}</ul>
        <p class="vs-foot">Written by people who are already losing.</p>
      </div>
      <div class="vs-mid" aria-hidden="true"><i class="cl"></i><span class="vs-label">Trisian answers first</span><i class="cr"></i></div>
      <div class="vs vs-ready" data-reveal="right">
        <span class="vs-tag">Already written</span>
        <ul class="ready">{rows}</ul>
        <p class="vs-foot">Ready before anyone asks.</p>
      </div>
    </div>
    {sign('Answer it first.')}
    {cta_end("Tell us what they'd ask you first.", 'Send us the question', 'mailto:contact@trisian.com?subject=The%20question%20I%27d%20be%20asked%20first')}
  </div>
</section>'''


# ------------------------------------------------------------------ the 3 answers
def answers():
    pool = f'''<div class="pool" id="pool" data-phase="reset">
            <div class="pool-top"><span>Desktop pool</span><span class="clock" id="poolClock">00:00</span></div>
            <div class="pool-grid" id="poolGrid"><i class="sweep" aria-hidden="true"></i>{pool_tiles(24)}</div>
            <ol class="pool-steps" id="poolSteps"><li data-s="in">Check in</li><li data-s="use">Use</li><li data-s="out">Check out</li><li data-s="rs" class="on">Reset</li></ol>
            <p class="pool-status" id="poolStatus" aria-live="off">Reset 100%</p>
          </div>'''
    return f'''<a id="proof" aria-hidden="true"></a>
<section class="answers s-white" id="answers">
  <div class="ans-intro" id="ansIntro">
    <div class="ans-intro-in">
      {pill('The 3 answers')}
      <h2 class="mega" data-split>Written before the question.</h2>
      <p class="sub-p">3 proofs, not 3 promises. Each one is something you can check.</p>
      <a class="scroll-cue" href="#answer-1" aria-label="Scroll to the first answer">{ic('arrow-right', 22)}</a>
    </div>
  </div>
  <div class="wrap">
    <div class="ans-list">
      <article class="ans a-indigo" id="answer-1" data-ans>
        <div class="ans-copy">
          <span class="ans-label">Answer 1 of 3</span>
          <h3 class="h3">Nothing to Find</h3>
          <p class="lead">{hl("A hacker gets in at midnight. At 6am there's *nothing to find.*")}</p>
          <p>{hl("Every Trisian desktop is *wiped clean every night.* Checked in, used, checked out, reset. Files and profiles are stored apart from the session, so nobody loses a day of work and nobody finds a trace of it.")}</p>
          <p class="stat">{hl("What was on that machine? *Nothing.*")}</p>
        </div>
        <figure class="ans-viz" data-viz="pool" aria-label="Diagram: a pool of desktops fills during the day and is wiped at midnight">
          {pool}
        </figure>
      </article>

      <article class="ans a-peri" id="answer-2" data-ans>
        <div class="ans-copy">
          <span class="ans-label">Answer 2 of 3</span>
          <h3 class="h3">Industry-Bound, Not Size-Bound</h3>
          <p class="lead">The regulator doesn't grade on a curve.</p>
          <p>A 50-person practice carries the same HIPAA exposure as a 5,000-person hospital. The small firm needs the big firm's infrastructure and can't afford the big firm's IT department. Trisian builds to the rule, not the headcount.</p>
          <p class="stat">Same exposure. <b>Same answer.</b></p>
        </div>
        <figure class="ans-viz" data-viz="dots" aria-label="Diagram: one dot is 50 people. One dot for the 50-person practice, one hundred dots for the 5,000-person hospital">
          <div class="bd-dots">
            <div><span class="dots d1" data-dots="1" aria-hidden="true"></span><b>50-person practice</b></div>
            <div><span class="dots d100" data-dots="100" aria-hidden="true"></span><b>5,000-person hospital</b></div>
          </div>
          <p class="bd-verdict">Same rules. Same audit. Same exposure.</p>
          <p class="bd-key"><i></i> 1 dot = 50 people</p>
        </figure>
      </article>

      <article class="ans a-pale" id="answer-3" data-ans>
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
    <p class="mega-sign" data-reveal="scale">Not protection. Proof.</p>
    {cta_end('Check our work.', 'Ask for a live walkthrough', '#assessment?topic=walkthrough')}
  </div>
</section>'''


# ------------------------------------------------------------------ who it's for (one table)
def seats():
    return f'''<section class="sec s-grey" id="seats">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      {pill("Who it's for")}
      <h2 class="h2"><span class="bd">One table.</span><span class="lt">Every seat covered.</span></h2>
      <p class="sub-p">Seven to twelve people touch this decision. Each one is afraid of something different.</p>
      <a class="link-arrow" href="{BASE}who-its-for/">Your industry</a>
    </header>
    <div class="seats-grid" data-stagger>
      <figure class="s-photo s-table"><img src="assets/img/table.webp" alt="Four colleagues working and talking around a long table" width="1600" height="1066" loading="lazy" data-parallax-img></figure>
      <article class="seat"><h3 class="h4">The CTO</h3><p class="q">You already know what's broken.</p><p>You filed the ticket eighteen months ago. We work co-managed: we augment your team, we don't replace it.</p></article>
      <article class="seat"><h3 class="h4">The IT manager</h3><p class="q">The 2am call. And the 9am question.</p><p>Off your plate, not out of the room. We make you look good to leadership, with receipts.</p></article>
      <article class="seat"><h3 class="h4">The owner</h3><p class="q">You want to stop thinking about it.</p><p>Plain language. Predictable pricing. Peers in your industry who already made the call.</p></article>
      <figure class="s-photo s-close"><img src="assets/img/closeup.webp" alt="A woman at her desk listening closely" width="1600" height="1066" loading="lazy" data-parallax-img><figcaption>The 9am question is coming. Have the answer.</figcaption></figure>
    </div>
    {cta_end('Bring everyone who gets a vote.', 'Set up a team call', '#assessment?topic=team-call')}
  </div>
</section>'''


# ------------------------------------------------------------------ one partner
def partner():
    rows = ['Every issue has an owner, an SLA and a resolution path.',
            'Critical response in 1 hour on Core and Advanced. 30 minutes on Enterprise.',
            'After hours, every level has emergency escalation through your named contacts.']
    li = ''.join(f'<li style="--i:{i}"><span class="ck">{ic("check", 18)}</span><span>{esc(r)}</span></li>' for i, r in enumerate(rows))
    return f'''<section class="sec s-white" id="partner">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      {pill('One partner')}
      <h2 class="h2"><span class="lt">One contract. One team. One name.</span></h2>
      <p class="sub-p">The day something breaks isn't the failure. It's the day Trisian shows up.</p>
    </header>
    <div class="one-grid">
      <figure class="one-l anim" data-viz="vendors">
        {scenes.vendors(BASE)}
        <figcaption>Six vendors. Six answers. One word: &ldquo;unfortunately.&rdquo;</figcaption>
      </figure>
      <div class="one-r" data-reveal="right">
        <div class="trisian-box">
          <p class="tb-name">Trisian</p>
          <ul>{li}</ul>
        </div>
      </div>
    </div>
    {sign('One partner. One answer.')}
    {cta_end('Find out who picks up at 2am.', 'Hear from a real person', '#assessment?topic=intro')}
  </div>
</section>'''


# ------------------------------------------------------------------ what we offer
def offer():
    tiles = [
        ('desktop', 'The desktop', 'Windows desktops in the cloud, on Azure or Citrix. Sessions reset after each use. Profiles and files stay put.'),
        ('radar', 'The defense', 'MFA and Conditional Access from day one. Hardened images and behavioral detection as coverage climbs. Encrypted at rest and in transit.'),
        ('growth', 'The headroom', 'Auto-scaling follows real demand. Off-hours cost drops on schedule. Ten users or unlimited, with no redesign.'),
        ('filecheck', 'The paper trail', 'Evidence collected automatically. Audit trails that can’t be edited. Controls mapped to nine frameworks.'),
    ]
    tl = ''.join(f'''<article class="box" tabindex="-1">
        <span class="box-ico">{ic(n, 30)}</span>
        <h3 class="h4">{esc(t_)}</h3>
        <p>{esc(b)}</p>
      </article>''' for n, t_, b in tiles)
    return f'''<section class="sec s-pale" id="offer">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      {pill('The product')}
      <h2 class="h2"><span class="bd">What we offer.</span></h2>
      <p class="sub-p lead-p">Safe Workspace: your whole digital environment, run by one partner.</p>
      <p class="sub-p">A cloud desktop on Azure Virtual Desktop or Citrix Cloud, with security, licensing, monitoring, compliance and support built in. Your people log in. Everything else is our job.</p>
    </header>
    <div class="boxes4" data-stagger>{tl}</div>
  </div>
</section>'''


def six():
    # name, icon, fill class, title, copy
    t = [
        ('t-indigo', 'reset', 'Nightly reset', 'Every desktop wipes clean. Files and profiles stay put.', True),
        ('t-peri', 'percent', 'Azure at cost', 'Straight pass-through. Full visibility.', False),
        ('t-pale', 'activity', '24/7 monitoring', 'Platform monitoring runs around the clock.', False),
        ('t-pale', 'msft', 'Microsoft 365, included', 'Licensing sits inside the platform fee. One less vendor.', False),
        ('t-indigo', 'calendar', 'Patching on schedule', 'OS and Microsoft 365 updates land without a ticket.', False),
        ('t-peri', 'backup', 'One golden image', 'One managed desktop image, backed up weekly and kept for four weeks.', False),
    ]
    out = ''
    for cls, icon, title, body, pool in t:
        mini = f'<div class="mini-pool3" aria-hidden="true" id="miniPool"><i class="sweep"></i>{pool_tiles(9, "mt")}</div>' if pool else ''
        out += f'''<article class="tile {cls}">
        {mini}
        <span class="box-ico">{ic(icon, 30)}</span>
        <div><h3 class="h4">{esc(title)}</h3><p>{esc(body)}</p></div>
      </article>'''
    return f'''<section class="sec s-white" id="six">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      <h2 class="h2"><span class="bd">Every client starts with</span><span class="lt">the same six things.</span></h2>
      <p class="sub-p">One managed platform, one accountable team, nothing bolted on afterward.</p>
    </header>
    <div class="tiles6" data-stagger>{out}</div>
    {cta_end("Not sure how much you'd need?", 'See how coverage works', BASE + 'coverage/')}
  </div>
</section>'''


# ------------------------------------------------------------------ the handoff
def handoff():
    steps = [
        ('Assess', 'We map your security, performance and compliance against the rules you answer to. You get the gaps in writing.'),
        ('Design', 'We build the Safe Workspace around your applications, your regulators and your growth plan.'),
        ('Deploy', 'Pilot group first. Then everyone, with training and a check at each stage.'),
        ('Operate', 'We run it. Monitoring, patching, security, tuning. Your team doesn’t file tickets for any of it.'),
        ('Review', 'Every quarter: what changed in your rules, what changed in your business, what we adjust.'),
    ]
    li = ''.join(f'''<li class="step" style="--i:{i}">
        <span class="badge-n" aria-hidden="true">{i + 1}</span>
        <div class="step-box"><h3 class="h4"><span class="sr-only">{i + 1}. </span>{esc(a)}</h3><p>{esc(b)}</p></div>
      </li>''' for i, (a, b) in enumerate(steps))
    return f'''<section class="sec s-grey" id="handoff">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      <h2 class="h2"><span class="bd">The handoff.</span></h2>
      <p class="sub-p">Five steps from first call to a workspace that runs without you.</p>
    </header>
    <div class="handoff-grid">
      {ph('4:5', 'an office at the end of the day, desks cleared, lights low', 'A quiet office at the end of the day, desks cleared', 'ph-tall')}
      <ol class="steps" id="steps">{li}</ol>
    </div>
    {cta_end('The first step is a conversation.', 'Start the handoff', '#assessment?topic=start')}
  </div>
</section>'''


def services():
    return f'''<section class="svc-band" id="services-band">
  <div class="svc-bg" data-parallax="0.12" aria-hidden="true"><span>PHOTO PENDING &middot; 21:9 &middot; an IT lead and an engineer at a whiteboard, mapping a migration</span></div>
  <div class="wrap svc-in">
    <h2 class="svc-h" data-split>Still on Citrix, VMware or a server closet? We'll move you.</h2>
    <p class="sub-p" data-reveal>Migrations, security builds and compliance programs, scoped and quoted as projects.</p>
    <a class="btn btn-w" href="{BASE}services/" data-magnet data-reveal>See the services</a>
  </div>
</section>'''


# ------------------------------------------------------------------ faq and form
def faq():
    ds = '\n      '.join(f'<details><summary><span>{esc(q)}</span>{ic("plus", 22)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)
    return f'''<section class="sec s-white" id="faq">
  <div class="wrap faq-in">
    <header class="sec-head" data-reveal>
      {pill('Questions')}
      <h2 class="h2"><span class="bd">What people ask</span><span class="lt">before they call.</span></h2>
    </header>
    <div class="faq-list" data-stagger>
      {ds}
    </div>
    {cta_end('Still stuck on one?', 'Put it to us', '#assessment?topic=question')}
  </div>
</section>'''


def form():
    return f'''<section class="sec s-indigo" id="assessment">
  <div class="wrap">
    <div class="cta">
      <div class="cta-copy" data-reveal="left">
        <h2 class="h2 on-dark"><span class="bd">Have the answer</span><span class="lt">before the meeting.</span></h2>
        <p class="sub-p">We review your environment against the rules you answer to. Then we tell you where the day-after meeting would go badly today.</p>
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


# ------------------------------------------------------------------ page
def build():
    title = 'Trisian | Answered in Advance'
    desc = 'Managed IT for healthcare, financial services and legal. Trisian answers the day-after question before anyone asks it.'
    org = {'@context': 'https://schema.org', '@type': 'Organization', 'name': 'Trisian', 'url': BASE_URL,
           'email': 'contact@trisian.com', 'description': desc}
    head = head_common(BASE, title, desc, '', [org, faqld(FAQ)], home=True)
    body = f'''<body class="home">
<a class="skip" href="#top">Skip to content</a>
{header(BASE)}
<main id="top">
{hero()}
{receipts()}
{meeting()}
{answers()}
{seats()}
{partner()}
{offer()}
{six()}
{handoff()}
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


# [CONFIRM] / [HOLD] items that render nothing (also listed in docs/upgrade-report.md):
OMITTED = [
    'One partner row 3 and the home FAQ (after hours): the 15-minute engagement target is [CONFIRM]; the clause is left out.',
    'One partner: all response times are [CONFIRM] against the contract; 1 hour and 30 minutes are as already live.',
    'Microsoft 365 four-colour mark: rendered on staging, [CONFIRM] partner status permits it.',
    'Footer: legal entity wording, Privacy Policy and Terms not rendered. Phone line not rendered.',
]

if __name__ == '__main__':
    build()
