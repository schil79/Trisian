# Site rebuild report (Directive v2)

Staged at https://schil79.github.io/Trisian/next/ (noindex). The live root is untouched until you say promote.
Build: `python3 tools/gen_home.py`, `python3 tools/gen_pages.py`, `python3 tools/gen_industry_pages.py`.

## Decisions you made that override the directive
- Fonts hold as built: Graphik throughout, Bold against Light. H1 is `Answered in` (Graphik Regular) and `advance` (Archivo Condensed Black, indigo), with the blue underline under "Answered". The directive's Archivo and Google Sans pairing is not used.
- The 75% middle column stays (12.5% each side from 1100px up).
- Kept graphics (invoice, six vendors) have no black sides or outlines: white and pale tops, periwinkle sides, 1.5px indigo lines.
- Labels render as typed. No text-transform.

## What changed
- Slab, hard-shadow, grain and iso-stair system removed. Flat solid fills, 24px panels, 16px cards, no shadows.
- Home order: hero, receipts and frameworks, meeting, the 3 answers, One table, One partner, What we offer, six things, handoff, services band, questions, form.
- Plans, billing and Find your room are off the home page. Coverage, Services and Insights (plus an article template) are new pages. Hub and sector pages restyled with the Industries header and the language fix.
- Motion: hero panel sequence, pointer-reactive dot grid and panel, magnetic buttons, word-by-word headline reveals, scroll-linked panel scaling, scroll progress bar, handoff line that fills as you scroll, parallax on photos, counters, desktop pool loop, dot wave, hover reactions on every icon, lift on every card. Reduced motion shows final states.

## Purple
No purple anywhere. Search for 9B4DFF, #9b4dff, 155, 77, 255 and `--purple` finds nothing in site or tools.

## Language fix ("room")
Replaced everywhere per the table. Two uncovered matches, left as written, for you to decide: `Off your plate, not out of the room.` (The IT manager card, home and hub) and none else.

## Checks
axe-core: 0 violations on home, coverage, services, insights, article template, hub and four sector pages at 1280 and 375.
No horizontal scroll at 375, 768, 1280, 1920. H1 stays on one line.
Keyboard: services tablist arrows and deep links, insights filter, topic hash sets the hidden interest field.
No em dashes, banned words or emoji.

## Not verified
Safari, Firefox, Lighthouse, a screen-reader pass, touch devices, 768px visual review of every section.

## Judgment calls
- Industries header sits directly under the nav on the hub and sectors as written, so the hub H2 comes before its H1.
- Services band button on the Services page, "Scope the way out", is my label. The directive gave none.
- Services and Insights band copy follows the directive. "Read" links on Insights point to the article template.
- Microsoft four-colour mark rendered on staging.

## [CONFIRM] and [HOLD] left out
- The 15-minute after-hours target: omitted in One partner, the home FAQ and the Coverage FAQ.
- Response times, comparison-table rows, nine frameworks on every level: shown as written, need checking against the contract.
- Microsoft partner status for the four-square mark.
- Footer entity wording, phone, Privacy Policy, Terms. Client matter segregation (Legal), BAA line (Healthcare).
- Insights: every card is Coming soon. Do not launch like this. Hide the nav item if fewer than three articles are live.
- Photo placeholders everywhere the directive lists them (handoff, services band, coverage, services, insights).
