#!/usr/bin/env python3
"""Wrap every shipped clay PNG in an SVG container.

Clay renders are lighting/shadow raster art — they cannot be truly vectorized
without destroying the locked r8-2 style (see docs/clay-recipe.md). This
script is the honest middle path: each PNG is embedded byte-identical into a
minimal .svg so consumers that require the .svg file format get a drop-in
file with zero visual drift.

    out/clay-png/{palette}/{name}.png  ->  out/clay-svg/{palette}/{name}.svg

The wrapper is deterministic and idempotent: re-running scans
out/clay-png/ and overwrites out/clay-svg/. Run it after any regeneration
of the PNGs.

Usage:
    python3 scripts/make_svg_wrappers.py            # wrap everything
    python3 scripts/make_svg_wrappers.py --palette coffee
    python3 scripts/make_svg_wrappers.py --check    # verify, never write
"""

import argparse
import base64
import re
import sys
from pathlib import Path

from PIL import Image

_B64 = re.compile(r"base64,([A-Za-z0-9+/=]+)")

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "out" / "clay-png"
SVG_DIR = ROOT / "out" / "clay-svg"

SVG_TEMPLATE = (
    '<svg xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink" '
    'width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
    '<image width="{w}" height="{h}" '
    'xlink:href="data:image/png;base64,{b64}" '
    'href="data:image/png;base64,{b64}"/>'
    "</svg>\n"
)


def _wrap_bytes(png_path: Path) -> str:
    with Image.open(png_path) as im:
        w, h = im.size
    b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")
    return SVG_TEMPLATE.format(w=w, h=h, b64=b64)


def wrap_one(png_path: Path, svg_path: Path) -> None:
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(_wrap_bytes(png_path), encoding="utf-8")


def check(roots: list[Path]) -> int:
    """Verify every wrapper embeds its PNG byte-identical; never writes.

    Fails closed on: wrapper missing for a PNG, orphan wrapper with no PNG,
    or base64 payload that no longer matches the source PNG.
    """
    problems: list[str] = []
    count = 0
    for palette_dir in sorted(roots):
        wrap_dir = SVG_DIR / palette_dir.name
        # orphan wrappers whose source PNG is gone
        svgs = sorted(wrap_dir.glob("*.svg")) if wrap_dir.is_dir() else []
        for svg in svgs:
            if not (palette_dir / (svg.stem + ".png")).exists():
                problems.append(
                    f"orphan wrapper, no PNG: "
                    f"{palette_dir.name}/{svg.name}")
        for png in sorted(palette_dir.glob("*.png")):
            svg = wrap_dir / (png.stem + ".svg")
            rel = f"{palette_dir.name}/{png.stem}.svg"
            if not svg.exists():
                problems.append(f"missing wrapper: {rel}")
                continue
            m = _B64.search(svg.read_text(encoding="utf-8"))
            if m is None:
                problems.append(f"no embedded payload: {rel}")
            elif base64.b64decode(m.group(1)) != png.read_bytes():
                problems.append(f"payload drift: {rel}")
            else:
                count += 1
    if problems:
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        raise SystemExit(
            f"wrapper check failed — {len(problems)} problem(s); "
            f"re-run without --check to rewrite")
    print(f"verified {count} wrappers byte-identical to their PNGs")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--palette", help="wrap only one palette folder")
    parser.add_argument("--check", action="store_true",
                        help="verify byte-identity of wrappers; never write")
    args = parser.parse_args()

    if not OUT_DIR.is_dir():
        print(f"no {OUT_DIR} — generate PNGs first", file=sys.stderr)
        return 1

    roots = [OUT_DIR / args.palette] if args.palette else sorted(
        p for p in OUT_DIR.iterdir() if p.is_dir()
    )

    if args.check:
        for palette_dir in roots:
            if not palette_dir.is_dir():
                print(f"no such palette dir: {palette_dir}", file=sys.stderr)
                return 1
        return check(roots)

    count = 0
    for palette_dir in roots:
        if not palette_dir.is_dir():
            print(f"no such palette dir: {palette_dir}", file=sys.stderr)
            return 1
        for png in sorted(palette_dir.glob("*.png")):
            wrap_one(png, SVG_DIR / palette_dir.name / (png.stem + ".svg"))
            count += 1
    print(f"wrapped {count} PNGs into {SVG_DIR}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
