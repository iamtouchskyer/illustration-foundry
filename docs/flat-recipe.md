# Flat-vector icon recipe (locked)

Line 2 of the library (see README "Product lines"): same 93 subjects, same eight palettes,
same four palette slots — drawn as flat SVG geometry instead of rendered
clay. Infinite scaling, CSS-free recolor at build time, tiny files
(~0.5–2.3 KB each). The script `scripts/build_flat_library.py` is the
executable source of truth; this doc is the human-readable record of *why*
every clause exists.

## Why a separate product, not a conversion

Clay renders are lighting/shadow raster art; vectorizing them destroys the
locked style. The flat library is a **parallel product** that shares the
catalog and palette contract but owns its own geometry. One subject = one
geometry definition parametrized by the four palette slots, emitted once per
palette with hex values baked in.

## Style contract (locked)

- Canvas: `viewBox="0 0 128 128"`, shipped at **512×512** (`width`/`height`).
- **Transparent background** — flat SVGs are inherently transparent, so there
  is no white/transparent variant split (unlike clay's ×2). 93 × 8 = 744 files.
- Subject centered, occupying the vertical band **~y=18..96**.
- One neutral contact-shadow ellipse at **y=104** (`#2b2b3a` at opacity 0.08)
  — inherits the clay r8-2 "grounded" idea so both families sit the same way.
- Flat fills only: no gradients, no strokes unless a motif defines one, no
  filters, no text/digits (same AVOID spirit as clay).
- Allowed colors: the palette's four hex slots + `#ffffff` + the fixed shadow
  color. Nothing else.

## Palette slots (identical semantics to clay)

- `PRIMARY` — main subject body.
- `HIGHLIGHT` — brighter accent on the subject.
- `SECONDARY` — accent object / secondary prop.
- `TERTIARY` — pale surfaces, paper, backing shapes.

Hex values are **parsed out of `generate_clay_library.py`'s `PALETTES`** by
`scripts/flat/palettes.py` (regex on the `"name #hex"` strings) — never
re-declared. Adding a palette to the clay script automatically makes it
available to the flat build. Zero drift by construction.

## Fail-closed parity

`build_flat_library.py` refuses to run if the flat icon catalog drifts from
the clay `SUBJECTS` catalog (missing subjects, extra subjects, or group-name
drift). New subject = one line in clay `SUBJECTS` + one clay template + one
flat icon function; the parity check is the gate that keeps all three in
lockstep.

## Geometry vocabulary (`scripts/flat/motifs.py`)

Shared motif builders (sheet, envelope, check, cross, star, sparkle, heart,
leaf, box, folder, book-open/closed, bell, clock, cloud, bubble, magnifier,
padlock, key, shield, gear, person, target, flag, trophy, medal, coin, gem,
crown, capsule-bar, steps, arrow-loop, hourglass, moon, ticket, card,
ring-progress, camera, laptop, trash-bin, flame). Icon modules compose motifs
into subjects and mirror the clay template's semantics — e.g.
`billing/upgrade` = crown + steps, `billing/trial-ended` = torn ticket +
clock, `wellness/session-complete` = ripple + lotus petals + sparkle.

Prefer composing existing motifs over inventing one-off geometry; the motif
vocabulary is what keeps 93 subjects feeling like one family.

## Usage

```bash
python3 scripts/build_flat_library.py --list
python3 scripts/build_flat_library.py --all
python3 scripts/build_flat_library.py --all --palette ocean
python3 scripts/build_flat_library.py --group billing
python3 scripts/build_flat_library.py --subject billing/upgrade
```

```
out/flat-svg/{palette}/{group}-{state}.svg
```

Pure stdlib — no API key, no dependencies, deterministic output. Rebuilds are
idempotent; the generated SVGs ARE the shipped product of this line, so they
are committed to the repo and `--verify` is the drift gate.

## Hard rules

- **Do NOT hand-edit generated SVGs.** Change the icon function, rebuild.
- **Do NOT add colors** outside the four palette slots + white + shadow.
- New subjects must land in BOTH catalogs (clay template + flat icon); the
  parity check fails closed otherwise.
- Clay PNGs and flat SVGs may coexist in one product; they are siblings, not
  substitutes — clay carries warmth/texture, flat carries scale/flexibility.

## Provenance

- Built 2026-09-02 as option 3 of the SVG follow-up (after option 1, the
  byte-identical PNG→SVG wrappers in `out/clay-svg/`). 744 SVGs generated
  across all 8 palettes; XML validity and visual grid verification passed.
