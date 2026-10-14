# Site upgrade report

Staged at https://schil79.github.io/Trisian/next/ (noindex). The live root is untouched until you say promote.
Branch: `claude/nifty-ptolemy-ixxiyv`. Build: `python3 tools/gen_home.py` and `python3 tools/gen_industry_pages.py`.

## Where I followed your message over the directive
- Font is Graphik everywhere (Light 300 to Bold 700). Headlines pair Bold with Light. Archivo Condensed Black is used for one word: "advance".
- H1 is `Answered in` (Graphik Regular) and `advance` (Archivo Condensed Black, indigo). The purple underline sits under "Answered".
- Sign-offs, numerals and the big-slab question are Graphik Bold, not Archivo Black.
- Content sits in the middle 75% (12.5% sides at 1100px and up), not the directive's 1200px cap.
- Labels render as typed. No text-transform.
- Commits are grouped, not one per phase, and I did not stop after phase 1.

## Other deviations
- Slabs are inline SVG, not CSS 3D. Text stays vector-sharp in every browser, at the cost of not being selectable. Each scene carries an aria-label. Only Chromium was tested.
- The grain beam is a pre-dithered WebP (`tools/make_stipple.py`) used as an SVG mask over solid #1453FF, rather than a gradient times a stipple tile.
- "Answered" label in the progress widget is ink, not purple, because purple text under 24px fails contrast.
- Hero room tabs start with nothing selected, showing the default "What did you know, and when?". Autoplay selects Healthcare after 6s.

## Purple search (9B4DFF / 155, 77, 255)
Only `site/css/styles.css` and `site/css/industry.css` define or use it, in the four budget uses: H1 underline, widget final dot, "Already written" check dots (also the "Trisian answers first" dots on industry pages), and the framework-chip dot on hover match. No hits in any HTML. The old purple cards, buttons, numerals and blur bands are gone.

## Checks
- axe-core: 0 violations on home (375, 1280) and all four industry pages and the hub, after one hub contrast fix.
- H1 stays on one line at 375, 768, 1024, 1280 and 1920. No horizontal scroll at those widths.
- Tabs: arrow keys, Home/End, hover pause, no autoplay under reduced motion, final-state rendering under reduced motion: checked.
- Weight (HTML, CSS, JS, fonts, beam; images excluded): 235 KB before, 319 KB after. The home HTML is 104 KB because of inline SVG. Motion library removed.
- No em dashes, banned words, emoji, Montserrat or Open Sans found.

## Not verified
Safari and Firefox rendering, Lighthouse, a screen reader pass, real touch devices, 768px visual review of every section.

## [CONFIRM] and [HOLD] items left out
- After-hours "aim to be on it in 15 minutes": omitted from the FAQ and the One name card.
- All response times (1 hour, 30 minutes) are shown as already live but need checking against the contract.
- Per-tier framework lists from the old architecture: not rendered.
- Phone number: none. Legal entity wording, Privacy Policy, Terms: not rendered. Footer says `© 2026 Trisian`.
- "See all services" link: held until /services/ exists.
- Legal page: client matter segregation omitted. Healthcare: BAA line held.
- Testimonials: placeholder removed, nothing rendered.
