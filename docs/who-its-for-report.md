# Who it's for: build report

Built from Trisian_Who_Its_For_Spec.md. Pages: /who-its-for/, /healthcare/, /financial-services/, /legal/, /growing-businesses/.
Copy lives in tools/gen_industry_pages.py (run it to regenerate; the site itself needs no build step).

## Not rendered, tagged [HOLD] in the spec
- Healthcare: business associate agreement row; SOC 2 and ISO 27001 due-diligence row; proof slot.
- Financial services: notification-window line; attestation-status line; proof slot.
- Legal: client security questionnaires and outside counsel guidelines row; proof slot.
- Growing businesses: proof slot.
No [CONFIRM] tags appear in the spec.

## Where the spec conflicted with itself or with later instructions
1. Type. Spec: Google Sans body, uppercase labels. Instruction in this project: Archivo SemiCondensed body, no caps. Followed the instruction. Labels the spec already typed in capitals (kickers, timestamps, PHOTO PENDING) render as typed; nothing is transformed to caps.
2. Surfaces. Spec: navy and black heroes, black footer. Earlier instruction: white main, color as pops. Kept the spec's navy/black bands (hero, rules, proof) on pages that are otherwise white and grey. Footer stays the existing light grey.
3. Purple never on indigo. The CTA band is indigo, so the purple button rule cannot apply there. The button sits inside the white form card (indigo fill, white label). The hub CTA button is white with a dark label.
4. Hub cards. Spec says "white industry cards" in one place and "dark card" in the component and design notes. Built dark.
5. Legal chips. Copy lists five chips; the design note says "four, not five". Copy is locked, so five render.
6. Home "#seats" link line. Spec asks for a line linking to the hub but gives no copy. Used "Pick your room." (from the hub hero).
7. Hub has a visually hidden H2 "Industries" so the heading outline is valid.

## Worth a look before launch
- Financial services shows a chip row "Frameworks Trisian covers" with SOC 2 and ISO 27001. The spec's fact register says never claim attestations until confirmed. The row says "covers", not "certified", but the client or counsel should confirm it.
- HIPAA 60-day wording is sourced from a secondary site; confirm against HHS. Everything under "stated from knowledge" in the spec's section 10 still needs counsel.
- Photos: the four client-supplied images are in (one per industry page, 3:2). Alt text describes what each photo actually shows, not the imagery brief. See the note below about two of them.
- Forms still send nowhere. No og:image is set because none exists.

## Checked
- Loaded all five pages and the home page at 375, 768 and 1280 px: no horizontal scroll, one H1 each.
- axe-core (WCAG 2.0/2.1 A and AA): 0 violations on all six pages. This also caught and fixed two contrast problems and one ARIA role on the home page.
- Day-after panel: plays once, 1.89 s end to end; reduced motion shows the final state with no tilt.
- Dropdown works by mouse, keyboard (Enter, Escape) and on mobile. FAQ is native details. Industry pre-select works from ?industry= and from each page.

## Could not verify here
- Screen reader behavior, real phones, Windows high contrast mode.
- JSON-LD was generated from the visible FAQ items but not run through Google's validator (no outside network).
