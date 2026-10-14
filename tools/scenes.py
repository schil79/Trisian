"""Original isometric compositions for the home page. Built with iso.py.

Each function returns an inline SVG string. Classes used for motion (rise, axis, beam, dk, ...) are
styled in site/css/styles.css. Every scene shows its final state without CSS animation.
"""
from iso import *

STEPS = [
    ('Logs from vendor A', 'server'),
    ('Legal on line two', 'phone'),
    ("Last year’s audit", 'file-check'),
    ('Who has the access list?', 'key'),
    ('“Unfortunately…”', 'clock'),
]

# timestamp, question lines (pre-split so the SVG needs no text measuring)
ROOMS = {
    'default': ('Day after · 9:00 AM', ['What did you know,', 'and when?']),
    'healthcare': ('Day after · 8:15 AM', ['Whose records were', 'reachable?']),
    'financial': ('Day after · 2:00 PM', ['What did you know,', 'and when did clients', 'hear it?']),
    'legal': ('Day after · 9:00 AM', ['Whose files, and', 'have the clients', 'heard it from you?']),
}


def hero(base, mobile=False):
    sc = Scene('hm' if mobile else 'hd', base)
    steps = STEPS[2:] if mobile else STEPS
    n = len(steps)
    if mobile:
        w, d, pitch, rise, fs, tx = 150, 38, 48, 28, 15, 12
        bw, bd, bfs, blh = 214, 150, 22, 28
    else:
        w, d, pitch, rise, fs, tx = 226, 40, 50, 26, 14, 14
        bw, bd, bfs, blh = 310, 148, 22, 28
    x0 = 0
    by = n * pitch + 14                      # the big slab sits just past the last step
    cy = by + bd / 2

    # grain light first, so it sits on the floor under everything
    sc.add(sc.group(sc.beam(x0 + bw / 2 - 20, by + bd * 0.8, 0, 250 if not mobile else 190, 128 if not mobile else 100), 'beamg'))
    # axis on the floor, nodes at each step and at the big slab
    cx = x0 + w / 2
    nodes = [(cx, i * pitch + d / 2) for i in range(n)] + [(cx, cy)]
    sc.add(sc.axis((cx, -12), (cx, by + bd + 24), nodes, z=0, name='ax'))

    for i, (txt, ic) in enumerate(steps):
        z = (n - 1 - i) * rise
        y = i * pitch
        inner = sc.drop(cx, y + d / 2, z) + sc.slab(x0, y, z, w, d, 12)
        inner += sc.ttop(x0, y, z + 12, tx, d / 2 + fs * .35, txt, 't-m', fs)
        inner += sc.icon(ic, x0, y, z + 12, w - 30, d / 2 - 9, 18)
        sc.add(sc.group(inner, 'rise', f'--d:{i * 90}ms'))

    # the big slab: Navy, white outline, bright extrusion, the question set bold
    h = 20
    bx = x0 - (bw - w) / 2
    big = sc.slab(bx, by, 0, bw, bd, h, top=NAVY, side=BRIGHT, line=WHITE, sw=2)
    for key, (stamp, lines) in ROOMS.items():
        g = sc.ttop(bx, by, h, 18, 30, stamp, 't-m', 13, fill=T2)
        g += sc.ttop(bx, by, h, 18, 64, lines, 't-b', bfs, lh=blh, fill=WHITE)
        big += f'<g class="room{" on" if key == "default" else ""}" data-room="{key}">{g}</g>'
    sc.add(sc.group(big, 'rise big', f'--d:{n * 90 + 60}ms'))
    return sc.svg('hero-iso' + (' is-m' if mobile else ''), pad=10, hidden=True)


# ------------------------------------------------------------------ answer 1: the empty room
def room(base):
    sc = Scene('rm', base)
    cols, rows, pw, pd = 4, 5, 46, 36
    gx, gy = 14, 10
    for r in range(rows):
        for c in range(cols):
            x, y = c * (pw + gx), r * (pd + gy)
            sc.add(sc.group(sc.slab(x, y, 0, pw, pd, 7, top=WHITE, side=CORN, line=WHITE, sw=1.5,
                                    face_cls=('dk-s', 'dk-s', 'dk-t')), 'dk', f'--r:{r}'))
    # the clock slab sits in front of the pool
    cx0, cy0 = 34, rows * (pd + gy) + 54
    cw, cd = 156, 64
    inner = sc.slab(cx0, cy0, 0, cw, cd, 12, top=NAVY, side=BRIGHT, line=WHITE, sw=2)
    inner += sc.icon('clock', cx0, cy0, 12, 14, 14, 26, color=WHITE)
    inner += sc.ttop(cx0, cy0, 12, 52, 28, '00:00', 't-b', 22, fill=WHITE)
    inner += sc.ttop(cx0, cy0, 12, 52, 48, 'Reset', 't-m', 14, fill=T2)
    sc.add(sc.group(inner, 'clk'))
    return sc.svg('room-iso', label='Twenty desktops, filled during the day and wiped row by row at midnight', pad=12)


# ------------------------------------------------------------------ answer 2: same lid
def bound(base):
    sc = Scene('bd', base)
    s, lid, gap = 70, 92, 230
    za = 220                                   # height of the measuring axis
    for (y, hh, key) in ((0, 44, 'small'), (gap, 150, 'tall')):
        body = sc.slab(0, y, 0, s, s, hh, top=WHITE, side=INK, line=INK, sw=2)
        lines, z = '', 22                      # floor lines on the two visible faces
        while z < hh:
            a, b = P(0, y + s, z), P(s, y + s, z)
            c, e = P(0, y, z), P(0, y + s, z)
            lines += (f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" stroke="#fff" stroke-width="1.2" opacity=".8"/>'
                      f'<line x1="{f(c[0])}" y1="{f(c[1])}" x2="{f(e[0])}" y2="{f(e[1])}" stroke="#fff" stroke-width="1.2" opacity=".8"/>')
            z += 22
        lo = (s - lid) / 2
        lidg = sc.slab(lo, y + lo, hh, lid, lid, 12, top=INDIGO, side=INK, line=INK, sw=2)
        lidg += sc.ttop(lo, y + lo, hh + 12, 14, lid / 2 + 8, 'HIPAA', 't-b', 22, fill=WHITE)
        lidg += sc.drop(s / 2, y + s / 2, za, hh + 12)
        sc.add(sc.group(body + lines + lidg, 'rise', f'--d:{0 if key == "small" else 140}ms'))
    # dashed axis between the lids, reading "Same lid"
    sc.add(sc.axis((s / 2, s / 2), (s / 2, gap + s / 2), [(s / 2, s / 2), (s / 2, gap + s / 2)], z=za, name='ax'))
    X, Y = P(s / 2, gap / 2 + s / 2, za)
    sc.grow((X - 50, Y - 34), (X + 50, Y + 8))
    sc.add(f'<text transform="matrix({f(C)} {f(S)} 0 1 {f(X)} {f(Y - 12)})" text-anchor="middle" class="t-m" font-size="16">Same lid</text>')
    return sc.svg('bound-iso', label='Two buildings, one small and one tall, each wearing the same HIPAA lid', pad=14)


# ------------------------------------------------------------------ answer 3: zero markup
def markup(base):
    sc = Scene('mk', base)
    w, d, h = 214, 124, 12
    items = ['Compute', 'Storage', 'Networking', 'Licensing']

    def invoice(x, y, z, title, delay):
        g = sc.slab(x, y, z, w, d, h, top=WHITE, side=INK, line=INK, sw=2)
        g += sc.ttop(x, y, z + h, 16, 26, title, 't-b', 16)
        rows = ''
        for i, it in enumerate(items):
            yy = 50 + i * 18
            rows += f'<text x="16" y="{yy}" class="t-r" font-size="12">{it}</text>'
            rows += f'<rect x="104" y="{yy - 9}" width="{[92, 62, 40, 70][i]}" height="8" rx="1" fill="{T2}" stroke="{INK}" stroke-width="1"/>'
        g += sc.flat(x, y, z + h, rows)
        return sc.group(g, 'rise', f'--d:{delay}ms')

    sc.add(invoice(0, 0, 96, 'Azure invoice', 0))
    sc.add(invoice(0, 150, 0, 'Your invoice', 140))
    # the hollow markup bar sits in front of the lower invoice
    bx, by = 14, 150 + d + 22
    bar = sc.slab(bx, by, 0, w - 28, 50, 8, top=WHITE, side=INK, line=INK, sw=2, cls='')
    bar += sc.flat(bx, by, 8, f'<rect x="10" y="10" width="{w - 48}" height="30" rx="3" fill="none" stroke="{INK}" stroke-width="1.5" stroke-dasharray="4 3"/>'
                                f'<text x="{(w - 28) / 2}" y="30" text-anchor="middle" class="t-b" font-size="14">Markup 0%</text>')
    sc.add(sc.group(bar, 'rise', '--d:280ms'))
    return sc.svg('markup-iso', label='An Azure invoice above Trisian\'s invoice with the same four lines, and a markup bar reading zero percent', pad=14)


# ------------------------------------------------------------------ one name: six vendors
VENDORS = ['Endpoint vendor', 'Identity vendor', 'Cloud reseller', 'Compliance consultant', 'The break/fix guy',
           'Whoever set up the firewall in 2014']


def vendors(base):
    sc = Scene('vd', base)
    offs = [0, 22, -14, 28, -6, 16]
    ws = [210, 210, 210, 230, 210, 290]
    for i, name in enumerate(VENDORS):
        z = i * 40
        x = offs[i]
        g = sc.slab(x, 0, z, ws[i], 36, 10, top=WHITE, side=CORN, line=NAVY, sw=1.5)
        g += sc.ttop(x, 0, z + 10, 14, 23, name, 't-m', 14)
        sc.add(sc.group(g, 'rise', f'--d:{i * 70}ms'))
    sc.ground(-20, 0, 0, 300, 40)
    return sc.svg('vendors-iso', label='Six separate vendors stacked in a leaning pile', pad=12)
