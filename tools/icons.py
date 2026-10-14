"""Inline line icons with a hover reaction each. Lucide (https://lucide.dev, ISC licence) shapes where one exists,
redrawn by hand where an animated part needs its own element. 1.5px stroke, 24px box.

The reactions live in site/css/styles.css under `.ic-<name>`. Under prefers-reduced-motion they become a colour change only.
No em dashes in this file.
"""
import iso

_A = 'width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'

CUSTOM = {
    # desktop: powers on, the inner lines draw
    'desktop': '<rect x="2" y="3" width="20" height="14" rx="3"/><path d="M8 21h8M12 17v4"/><path class="ln l1" d="M6 8h8"/><path class="ln l2" d="M6 11h11"/><path class="ln l3" d="M6 14h5"/>',
    # radar: the sweep rotates
    'radar': '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/><path class="sweep" d="M12 12 19.5 4.5"/>',
    # growth: the arrow rises
    'growth': '<path d="M3 3v18h18"/><g class="arr"><path d="m7 15 4-4 3 3 6-7"/><path d="M15 7h5v5"/></g>',
    # file-check: the check draws
    'filecheck': '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path class="ck" d="m9 15 2 2 4-4"/>',
    # reset: rotates back
    'reset': '<g class="rot"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></g>',
    # percent badge: one scale pulse
    'percent': '<g class="pct"><line x1="19" x2="5" y1="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></g>',
    # activity: the line pulses along its length
    'activity': '<path class="act" d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    # calendar: patch day, the check draws and the page tips
    'calendar': '<g class="rot"><rect x="3" y="4" width="18" height="18" rx="3"/><path d="M16 2v4M8 2v4M3 10h18"/></g><path class="ck" d="m9 16 2 2 4-4"/>',
    # backup: the arrow lifts
    'backup': '<ellipse cx="11" cy="5" rx="8" ry="3"/><path d="M3 5v6c0 1.7 3.6 3 8 3M19 5v4"/><path d="M3 11v6c0 1.7 3.6 3 8 3"/><g class="arr"><path d="M18 21v-7M15 17l3-3 3 3"/></g>',
    # Microsoft mark: four squares pop with a stagger. Colours are the one deliberate palette exception.
    'msft': '<rect class="q q1" x="3" y="3" width="8.5" height="8.5" fill="#F25022" stroke="none"/><rect class="q q2" x="12.5" y="3" width="8.5" height="8.5" fill="#7FBA00" stroke="none"/><rect class="q q3" x="3" y="12.5" width="8.5" height="8.5" fill="#00A4EF" stroke="none"/><rect class="q q4" x="12.5" y="12.5" width="8.5" height="8.5" fill="#FFB900" stroke="none"/>',
    'target': '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    'gauge': '<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
    'check-circle': '<circle cx="12" cy="12" r="10"/><path class="ck" d="m9 12 2 2 4-4"/>',
}


def ic(name, size=24, extra=''):
    """animated or static inline icon. Unknown names fall back to the shared Lucide set in iso.ICONS."""
    body = CUSTOM.get(name) or iso.ICONS[name]
    return f'<svg class="ic ic-{name} {extra}" {_A.format(s=size)}>{body}</svg>'


def tile_icon(name, size=28):
    return ic(name, size)
