"""Isometric SVG toolkit for the Trisian slab system.

Projection: X = C*(x+y), Y = S*(y-x) - z, with C=cos30 and S=sin30.
  x axis runs right and up at 30 degrees (the long edge of a slab), y axis runs right and down, z is up.
  The viewer sits at -x, +y, +z, so the faces we can see are the top, the x=x0 face and the y=y1 face.

Why SVG and not CSS 3D: text on a CSS-3D plane goes soft in some browsers. Here every glyph is vector
geometry, so it stays sharp at any zoom. Text sits on a face with an affine matrix.

Icons are Lucide (https://lucide.dev, ISC licence), inlined as SVG. 1.5px stroke.
No em dashes in this file or in any output.
"""
C = 0.8660254
S = 0.5

INK, NAVY, INDIGO, COBALT = '#000000', '#010441', '#1800AD', '#0031A8'
BRIGHT, CORN, T1, T2, T3, WHITE = '#1453FF', '#576FF6', '#ECEFFE', '#C7CBFA', '#FAF7FF', '#FFFFFF'


def P(x, y, z=0.0):
    return (C * (x + y), S * (y - x) - z)


def f(n):
    s = '%.1f' % n
    return s[:-2] if s.endswith('.0') else s


def pts(*ps):
    return ' '.join(f'{f(a)},{f(b)}' for a, b in ps)


ICONS = {
    'user': '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    'key': '<path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"/><path d="m21 2-9.6 9.6"/><circle cx="7.5" cy="15.5" r="5.5"/>',
    'layers': '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    'server': '<rect width="20" height="8" x="2" y="2" rx="2" ry="2"/><rect width="20" height="8" x="2" y="14" rx="2" ry="2"/><line x1="6" x2="6.01" y1="6" y2="6"/><line x1="6" x2="6.01" y1="18" y2="18"/>',
    'file-check': '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="m9 15 2 2 4-4"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    'receipt': '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 17.5v-11"/>',
    'monitor': '<rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/>',
    'trending-up': '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    'activity': '<path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/>',
    'grid': '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>',
    'refresh': '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
    'percent': '<line x1="19" x2="5" y1="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    'moon': '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    'file-text': '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    'phone': '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    'dots': '<circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>',
    'database': '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>',
    'compass': '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
    'cloud': '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>',
    'building': '<rect width="16" height="20" x="4" y="2" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/>',
    'mail': '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    'arrow-right': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    'check': '<path d="M20 6 9 17l-5-5"/>',
    'plus': '<path d="M5 12h14"/><path d="M12 5v14"/>',
}


def icon_svg(name, size=24, cls='ico-svg'):
    """flat inline icon for HTML use"""
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


class Scene:
    def __init__(self, uid, base=''):
        self.uid, self.base = uid, base
        self.parts, self.defs = [], []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    # ---- bookkeeping
    def grow(self, *ps):
        for x, y in ps:
            self.x0, self.x1 = min(self.x0, x), max(self.x1, x)
            self.y0, self.y1 = min(self.y0, y), max(self.y1, y)

    def add(self, s):
        self.parts.append(s)
        return s

    def group(self, inner, cls='', style='', extra=''):
        a = f' class="{cls}"' if cls else ''
        b = f' style="{style}"' if style else ''
        return f'<g{a}{b}{extra}>{inner}</g>'

    # ---- solids
    def slab(self, x, y, z, w, d, h, top=WHITE, side=INK, line=INK, sw=2, cls='', face_cls=('', '', '')):
        """box with bottom at z, top at z+h. Returns SVG; also grows the bounds."""
        zt = z + h
        x1, y1 = x + w, y + d
        topp = [P(x, y, zt), P(x1, y, zt), P(x1, y1, zt), P(x, y1, zt)]
        left = [P(x, y, zt), P(x, y1, zt), P(x, y1, z), P(x, y, z)]
        right = [P(x, y1, zt), P(x1, y1, zt), P(x1, y1, z), P(x, y1, z)]
        self.grow(*topp, *left, *right)
        lc, rc, tc = face_cls
        a = f' class="{cls}"' if cls else ''
        st = f'stroke="{line}" stroke-width="{sw}" stroke-linejoin="round"'
        return (f'<g{a}>'
                f'<polygon class="{lc}" points="{pts(*left)}" fill="{side}" {st}/>'
                f'<polygon class="{rc}" points="{pts(*right)}" fill="{side}" {st}/>'
                f'<polygon class="{tc}" points="{pts(*topp)}" fill="{top}" {st}/></g>')

    def ground(self, x, y, z, w, d):
        zt = z
        self.grow(P(x, y, zt), P(x + w, y, zt), P(x + w, y + d, zt), P(x, y + d, zt))

    # ---- text and icons laid on faces
    def _m_top(self, x, y, z):
        X, Y = P(x, y, z)
        return f'matrix({f(C)} {f(-S)} {f(C)} {f(S)} {f(X)} {f(Y)})'

    def ttop(self, x, y, z, lx, ly, lines, cls, size, lh=None, fill=None, anchor=None):
        """text on the top face of a slab whose top is at height z and whose back corner is (x,y)."""
        if isinstance(lines, str):
            lines = [lines]
        lh = lh or size * 1.2
        fa = f' fill="{fill}"' if fill else ''
        an = f' text-anchor="{anchor}"' if anchor else ''
        tsp = ''.join(f'<tspan x="{f(lx)}" y="{f(ly + i * lh)}">{l}</tspan>' for i, l in enumerate(lines))
        return f'<text transform="{self._m_top(x, y, z)}" class="{cls}" font-size="{size}"{fa}{an}>{tsp}</text>'

    def tfront(self, x, y1, zt, lx, ly, text, cls, size, fill=None):
        """text on the y=y1 face (the right-front face), reading up and to the right."""
        X, Y = P(x, y1, zt)
        fa = f' fill="{fill}"' if fill else ''
        return (f'<text transform="matrix({f(C)} {f(-S)} 0 1 {f(X)} {f(Y)})" x="{f(lx)}" y="{f(ly)}" '
                f'class="{cls}" font-size="{size}"{fa}>{text}</text>')

    def flat(self, x, y, z, inner):
        """arbitrary 2D shapes in top-face coordinates (rects, lines), laid on the face."""
        return f'<g transform="{self._m_top(x, y, z)}">{inner}</g>'

    def icon(self, name, x, y, z, lx, ly, size, color=INK):
        X, Y = P(x, y, z)
        s = size / 24
        return (f'<g class="ico" transform="matrix({f(C)} {f(-S)} {f(C)} {f(S)} {f(X)} {f(Y)}) translate({f(lx)} {f(ly)}) scale({f(s)})" '
                f'fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')

    # ---- axis, beam
    def axis(self, a, b, nodes=(), z=0, color=INK, name='ax', r=4, draw=True):
        """dashed measuring line from world point a to b (x,y) at height z, with round nodes.
        The draw-on is a mask whose solid stroke is revealed with stroke-dashoffset."""
        (x1, y1), (x2, y2) = P(a[0], a[1], z), P(b[0], b[1], z)
        self.grow((x1, y1), (x2, y2))
        mid = f'{self.uid}-{name}'
        d = f'M{f(x1)} {f(y1)}L{f(x2)} {f(y2)}'
        dots = ''.join(f'<circle cx="{f(P(n[0], n[1], z)[0])}" cy="{f(P(n[0], n[1], z)[1])}" r="{r}" fill="{color}"/>' for n in nodes)
        for n in nodes:
            self.grow(P(n[0] - r, n[1], z), P(n[0] + r, n[1], z))
        self.defs.append(f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="4000" height="4000">'
                         f'<path class="axm" d="{d}" pathLength="1" fill="none" stroke="#fff" stroke-width="12"/></mask>')
        return (f'<g class="axis"><path d="{d}" fill="none" stroke="{color}" stroke-width="1.5" stroke-dasharray="6 6" mask="url(#{mid})"/>'
                f'<g class="axn">{dots}</g></g>')

    def drop(self, x, y, z_from, z_to=0, color=INK):
        a, b = P(x, y, z_from), P(x, y, z_to)
        self.grow(a, b)
        return (f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" stroke="{color}" stroke-width="1.5" '
                f'stroke-dasharray="3 5" opacity=".55"/>')

    def beam(self, cx, cy, z, rw, rh, color=BRIGHT, name='bm'):
        """a pool of stippled light on the floor, centred on world (cx,cy,z). rw, rh are screen half-sizes."""
        X, Y = P(cx, cy, z)
        self.grow((X - rw, Y - rh), (X + rw, Y + rh))
        mid = f'{self.uid}-{name}'
        self.defs.append(f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="{f(X - rw)}" y="{f(Y - rh)}" width="{f(2 * rw)}" height="{f(2 * rh)}">'
                         f'<image href="{self.base}assets/img/beam.webp" x="{f(X - rw)}" y="{f(Y - rh)}" width="{f(2 * rw)}" height="{f(2 * rh)}" preserveAspectRatio="none"/></mask>')
        return (f'<rect class="beam" x="{f(X - rw)}" y="{f(Y - rh)}" width="{f(2 * rw)}" height="{f(2 * rh)}" fill="{color}" mask="url(#{mid})"/>')

    # ---- output
    def svg(self, cls='', label=None, pad=14, extra_style='', hidden=False):
        w, h = self.x1 - self.x0 + 2 * pad, self.y1 - self.y0 + 2 * pad
        vb = f'{f(self.x0 - pad)} {f(self.y0 - pad)} {f(w)} {f(h)}'
        if hidden or not label:
            a11y = 'aria-hidden="true"'
        else:
            a11y = f'role="img" aria-label="{label}"'
        defs = f'<defs>{"".join(self.defs)}</defs>' if self.defs else ''
        return (f'<svg class="iso {cls}" viewBox="{vb}" width="{f(w)}" height="{f(h)}" {a11y} xmlns="http://www.w3.org/2000/svg">'
                f'{defs}{"".join(self.parts)}</svg>')


def tile(name, kind='light', uid='t'):
    """small iso slab with a line icon on its top face: the icon tile used on cards and rows."""
    sc = Scene(uid)
    if kind == 'dark':
        top, side, line = NAVY, BRIGHT, WHITE
        col = WHITE
    elif kind == 'blue':
        top, side, line = INDIGO, INK, INK
        col = WHITE
    elif kind == 'tint':
        top, side, line = T1, INK, INK
        col = INK
    else:
        top, side, line = WHITE, INK, INK
        col = INK
    sc.add(sc.slab(0, 0, 0, 60, 60, 10, top=top, side=side, line=line, sw=2))
    sc.add(sc.icon(name, 0, 0, 10, 14, 14, 32, color=col))
    return sc.svg('tile', pad=4)
