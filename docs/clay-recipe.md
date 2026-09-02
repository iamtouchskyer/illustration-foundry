# Clay illustration recipe (locked, r8-2 grounded-tray)

Recipe archive for line 1 of the library (see README "Product lines"). Mirrors
`docs/ui-playbook/clay-illustration-prompts.md` in Reviso — the script
`scripts/generate_clay_library.py` is the executable source of truth; this
doc is the human-readable record of *why* every clause exists.

## Base structure (never parametrized)

- Soft 3D matte clay render, miniature product-illustration style, isometric
  three-quarter view, centered composition.
- Pure seamless white background; key light from upper left; soft ambient fill.
- **Grounded tray**: a medium-rounded off-white (`#f9f9f9`) panel debossed
  into the background like a shallow open tray. The subject stands on the
  recessed floor and casts one pronounced elliptical contact shadow. Soft
  shading only on the top and left inner walls.
- High-key, airy, slightly translucent surfaces; smooth rounded geometry,
  chunky but delicate; no gloss.

## Palette slots (the only parametrized part)

Every subject template takes `{PRIMARY}`, `{HIGHLIGHT}`, `{SECONDARY}`,
`{TERTIARY}`. Palettes are measured color facts, extracted by a VL model from
the three Reviso originals — not adjectives:

- terracotta: `#ff6b35` / `#ffa55c` / `#a984ff` / `#e6e6f5`
- ocean: `#2f7cf6` / `#6cc4f0` / `#ff8f6b` / `#e8f1fa`
- forest: `#3ba55d` / `#7fd8a4` / `#e8a94f` / `#eaf4ec`
- sunset: `#f4647c` / `#ffb38a` / `#8d7bf0` / `#fceef0`
- gold: `#f2a516` / `#ffd166` / `#4f8a8b` / `#fbf3e0`
- coffee: `#6f4e37` / `#c8a97e` / `#8fa37a` / `#f5efe6`
- minecraft: `#5aab47` / `#8fd662` / `#4ed3c8` / `#eef0e8`
- blackpink: `#ff4d8d` / `#ff9ec2` / `#55556b` / `#fdeff5`

Adding a palette: append to `PALETTES` in the script, regenerate that folder.
Do not describe a palette in words — measure or pick hex values.

## Negative list (AVOID, appended to every prompt)

No photorealistic people, no hands/fingers unless the subject demands a tiny
stylized figure; no text, letters, numbers, logos, or watermarks on the
subject; no harsh gloss or plastic sheen; no dark or colored backgrounds; no
cast shadows beyond the single contact ellipse; no gradients on the background.

## Hard rules

- **Do NOT recolor or hue-shift these PNGs.**
- Regeneration is one command through the script; hand-editing images is
  forbidden.
- Transparent variant = rembg cutout of the white variant. One generation per
  subject per palette — never generate the transparent version separately.
- Theme adaptation = container (dark card base), never asset re-render.

## Provenance

- Structure locked in Reviso on 2026-08-30 as `r8-2-grounded-tray`, chosen by
  human adjudication over a 5-group × 3-shot candidate matrix against the
  three measured originals (404 / 500 / region-lock).
- Endpoint: `wan2.7-image-pro` requires the async DashScope route; the
  image-x skill's legacy routing is a known trap (see README "Constraints").
- Cross-project generalization (this library) built 2026-09-01 after pilot
  verification confirmed rembg preserves the `#f9f9f9` tray.
- Catalog expansion 2026-09-02: `gamification` / `learning` / `community` /
  `wellness` groups (30 subjects) added after studying Duolingo-style
  gamified learning, anoncafe.life-style anonymous community spaces, and
  suri.world-style AI companion surfaces; `empty` and `error` each gained
  two community/payment subjects. Structure, tray, and palettes untouched.
- Online-exam expansion 2026-09-02: `assessment` group (5 subjects:
  blank-exam-paper, results-sealed, proctor-camera, device-check,
  integrity-shield) added for online exam systems. Exam states that map to
  existing subjects (timeout, practice-again, certificate, reported,
  leaderboard-podium) are NOT duplicated. Score digits and countdown numbers
  stay abstracted (sealed envelope, hand-less clock) because the AVOID list
  bans text/numbers on the subject. Structure, tray, and palettes untouched.
- Billing + palette expansion 2026-09-02: `billing` group (6 subjects:
  storage-full, upload-limit, feature-locked, upgrade, trial-ended,
  subscribed) added for quota / subscription / paywall states — the broadest
  remaining gap after the app-type audit. All subjects stay digit-free per
  the AVOID list: upgrade is a crown, trial-ended is a torn perforated
  ticket, subscribed is a membership card with star + check badge. Same day,
  three palettes added on user request: `coffee` (espresso/latte/matcha),
  `minecraft` (grass green/diamond cyan), `blackpink` (hot pink/graphite).
  Palette descriptions stay anchored to hex values, not vibes. Structure,
  tray, and existing palettes untouched.
- Flat-vector sibling 2026-09-02: the same catalog drawn as flat SVG geometry
  (`scripts/build_flat_library.py`, output `out/flat-svg/`, contract in
  `docs/flat-recipe.md`). Shares this recipe's palette slots verbatim — hexes
  are parsed from this script's `PALETTES`, never re-declared — and fails
  closed if its subject catalog drifts from `SUBJECTS`.
