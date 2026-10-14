# How the three reference sites are built

Source: the saved pages in Clutch.zip, Jitter.zip and Joi_Planner.zip. Where the saved files don't contain the answer (the animation code lives in server-side bundles), this says so.

## Clutch (clutch.security): Next.js + Tailwind + Framer Motion + Rive

| What you see | How it's built |
|---|---|
| Hairline "blueprint" frame | Tailwind `border-x-[0.5px] border-t-[0.5px] border-gray-600` on every section container. Connector "steps" between cards are a 0.5px line with a pill (`rounded-[80px] border-[0.5px]`) sitting on it. Pure CSS. |
| Hero: coins lift onto a figure, shield appears | A **state machine of Framer Motion variants**. `useAnimation` controllers per piece (`lift`, `land`, `bounce`, `compress`, `activate`, `deactivate`), sequenced with `Promise.all` and chained `setTimeout`s. The bounce is a spring: `stiffness: 300, damping: 15`. Icons are flat SVGs laid on tilted discs with CSS 3D: `perspective(600px) rotateX(50deg) rotate(-33deg)`, black discs skewed, drop shadows are blurred divs. Hover inverts the icon (`group-hover:invert`). |
| Small floating/spinning bits | Plain CSS keyframes: `flying` (4-5s, translateY 5px), `rotations` (40s linear), `scaner-rotations` (radar sweep), `drawLine` (SVG `stroke-dashoffset` 125 to 0). |
| Section reveals | One `FadeIn` wrapper: `motion.div` with hidden/visible variants (opacity + offset, `easeOut`), triggered once by `react-intersection-observer` (`threshold` 0.1, `triggerOnce`). |
| Headline greys, last words go black | `<span>`s with `transition-colors duration-300`, class toggled when in view. |
| Feature product animations | **Rive** (`@rive-app/canvas` 2.27.1, WASM). `.riv` files (e.g. `/rive/zero-trust-screen.riv`) drawn into a `<canvas>` at 2x pixel ratio, inside an `aspect-[468/322]` wrapper with `pointer-events-none`. Authored in the Rive editor, driven by state machines. |
| Identity Lineage diagram | Not canvas. HTML boxes, tiny SVG arrows and SVG icons, laid out with flex. The "custom graphic" is careful composition, not a heavy runtime. |

## Jitter (jitter.video): React (Vite, CSS modules) + Lottie + video

| What you see | How it's built |
|---|---|
| Stacked cards that slide over each other | `<li>` cards with inline `position: sticky` and staggered `top` values (150.5px, 175.5px, 200.5px), `height: 700px`, `margin-bottom` 50/25/0. Each card sticks slightly lower than the last, so the next one covers it. No animation library needed. |
| Card visuals | Looping screen recordings: `<video autoplay loop playsinline aria-hidden>` (28 on the page, hosted on their CDN). Cards are `border-radius: 4rem`, one flat brand color each (`#01b2fd` blue, purple), with a layered soft shadow. The "5x" card is just big text in a translucent pill. |
| Hero backdrop | A Lottie animation on a `<canvas>` (`lottie-web` is bundled in `app.js`, animation data loaded through a web worker). |
| Logo row pops in | Logos start at `transform: scale(0, 0)` and animate up in a stagger. Inline `translate: none; rotate: none; scale: none` is the signature of GSAP or Motion, and the saved files don't show which. |
| Pill tags, section headers, buttons | Plain CSS. `html { font-size: 62.5% }` so `1rem = 10px`; headlines are weight 800, line-height 95%, letter-spacing about -0.024em. |

## Joi (joi.software): Framer site (React, Framer Motion under the hood)

| What you see | How it's built |
|---|---|
| Big statements rise and fade in as you scroll | Framer scroll effect: each statement starts at `opacity: 0; transform: translateY(300px)` with `will-change: transform`, and is driven by scroll position. Statements sit in sticky containers so they overlap and cross-fade. |
| Soft blur at the edges of the page | **Progressive blur**: five stacked layers, each `backdrop-filter: blur(...)` from 0.78px up to 100px, each masked with a `linear-gradient` band (`mask-image`), so blur ramps up smoothly. |
| Inline icon chips between headline words | SVGs (`<use href="#svg-...">`) sitting inline in a flex row of text blocks. |
| Floating nav | `position: sticky; top: 20px` container. |
| Feel | Almost no color, one CTA, huge type (96px / 78px, weight 599, letter-spacing -0.01em), lots of empty space. |

## Common thread

All three lean on the same family of tools: Motion / Framer Motion for reveals, springs and scroll-linked values, plus CSS sticky and CSS 3D transforms. The heavy custom illustration is either a pre-authored asset (Rive, Lottie, video) or careful HTML/SVG composition.

## What Trisian uses (site/js/main.js, site/css/styles.css)

- Motion (vanilla, bundled to 63 KB) for hero orchestration, reveals, scroll-linked values.
- Hero graph: state machine with the same spring (300/15), a packet traveling along an SVG path, connector lines redrawn from real layout.
- Three proofs as Jitter-style stacked sticky cards; the card underneath scales back as the next one covers it.
- Progressive blur under the nav (Joi). The scroll-linked statements were cut: the meeting is now one short full-bleed purple band.
- Also: hairline frame and step-pill connector (Clutch), isometric framework tiles with CSS 3D (Clutch), pill tags, marquee and big centered quote (Jitter).
- Not used: Rive, Lottie, video. They need assets authored elsewhere. If wanted later, real product or scene footage can drop into the cards as `<video>` with no code change beyond the markup.
