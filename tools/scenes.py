"""The two isometric graphics kept from the slab pass: the invoice (Answer 3) and the six vendors (One partner).
v2 palette: no black. White and pale tops, periwinkle sides, 1.5px indigo lines. Balanced, not high contrast.
Each slab group gets a class so CSS can lift it on hover and rise it on entry. No em dashes.
"""
from iso import *

LINE = INDIGO
SW = 1.5


def markup(base):
    sc = Scene('mk', base)
    w, d, h = 214, 124, 10
    items = ['Compute', 'Storage', 'Networking', 'Licensing']

    def invoice(x, y, z, title, delay):
        g = sc.slab(x, y, z, w, d, h, top=WHITE, side=T2, line=LINE, sw=SW)
        g += sc.ttop(x, y, z + h, 16, 26, title, 't-b', 16, fill='#191919')
        rows = ''
        for i, it in enumerate(items):
            yy = 50 + i * 18
            rows += f'<text x="16" y="{yy}" class="t-r" font-size="12" fill="#191919">{it}</text>'
            rows += f'<rect class="bar" style="--i:{i}" x="104" y="{yy - 9}" width="{[92, 62, 40, 70][i]}" height="8" rx="2" fill="{T2}" stroke="{LINE}" stroke-width="1"/>'
        g += sc.flat(x, y, z + h, rows)
        return sc.group(g, 'rise lift', f'--d:{delay}ms')

    sc.add(invoice(0, 0, 96, 'Azure invoice', 0))
    sc.add(invoice(0, 150, 0, 'Your invoice', 140))
    bx, by = 14, 150 + d + 22
    bar = sc.slab(bx, by, 0, w - 28, 50, 8, top=WHITE, side=T2, line=LINE, sw=SW)
    bar += sc.flat(bx, by, 8, f'<rect x="10" y="10" width="{w - 48}" height="30" rx="3" fill="none" stroke="{LINE}" stroke-width="1.5" stroke-dasharray="4 3"/>'
                              f'<text x="{(w - 28) / 2}" y="30" text-anchor="middle" class="t-b" font-size="14" fill="#1800AD">Markup 0%</text>')
    sc.add(sc.group(bar, 'rise lift', '--d:280ms'))
    return sc.svg('markup-iso', label="An Azure invoice above Trisian's invoice with the same four lines, and a markup bar reading zero percent", pad=14)


VENDORS = ['Endpoint vendor', 'Identity vendor', 'Cloud reseller', 'Compliance consultant', 'The break/fix guy',
           'Whoever set up the firewall in 2014']


def vendors(base):
    sc = Scene('vd', base)
    offs = [0, 22, -14, 28, -6, 16]
    ws = [210, 210, 210, 230, 210, 290]
    for i, name in enumerate(VENDORS):
        z = i * 40
        x = offs[i]
        g = sc.slab(x, 0, z, ws[i], 36, 10, top=T1 if i % 2 == 0 else WHITE, side=T2, line=LINE, sw=SW)
        g += sc.ttop(x, 0, z + 10, 14, 23, name, 't-m', 14, fill='#191919')
        sc.add(sc.group(g, 'rise lift', f'--d:{i * 70}ms'))
    sc.ground(-20, 0, 0, 300, 40)
    return sc.svg('vendors-iso', label='Six separate vendors stacked in a leaning pile', pad=12)
