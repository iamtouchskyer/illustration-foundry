#!/usr/bin/env python3
"""Build the flat-vector icon library (line 2 of the illustration library).

Same 93 subjects, same eight palettes, same four palette slots — but
drawn as flat SVG geometry instead of rendered clay. Palettes are
imported from generate_clay_library.py (single source of truth); the
build fails closed if the flat icon set drifts from the clay catalog.

Output:
    out/flat-svg/{palette}/{group}-{state}.svg    (512x512, viewBox 0 0 128 128)

Usage:
    python3 scripts/build_flat_library.py --list
    python3 scripts/build_flat_library.py --all
    python3 scripts/build_flat_library.py --all --palette ocean
    python3 scripts/build_flat_library.py --group billing
    python3 scripts/build_flat_library.py --subject billing/upgrade
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(ROOT))

from flat.icons import GROUPS  # noqa: E402
from flat.palettes import PALETTES, SUBJECTS  # noqa: E402
from flat.svg import svg_doc  # noqa: E402

OUT_FLAT = Path(__file__).resolve().parents[1] / "out" / "flat-svg"
SHIP_SIZE = 512


def parity_check() -> None:
    """Fail closed if flat coverage != clay catalog."""
    clay = {f"{g}/{s}" for g, subs in SUBJECTS.items() for s in subs}
    flat = {f"{g}/{s}" for g, icons in GROUPS.items() for s in icons}
    if clay != flat:
        missing = sorted(clay - flat)
        extra = sorted(flat - clay)
        raise SystemExit(
            "flat/clay catalog drift — refusing to build.\n"
            f"  missing from flat: {missing}\n"
            f"  extra in flat:     {extra}")
    if set(GROUPS) != set(SUBJECTS):
        raise SystemExit("group-name drift between flat and clay")


def all_keys() -> list[str]:
    return [f"{g}/{s}" for g, subs in SUBJECTS.items() for s in subs]


def build_one(group: str, state: str, palette: str) -> Path:
    els = GROUPS[group][state](PALETTES[palette])
    dest = OUT_FLAT / palette / f"{group}-{state}.svg"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(svg_doc(els, SHIP_SIZE), encoding="utf-8")
    return dest


def verify() -> int:
    """Rebuild every SVG in memory and diff against disk.

    Fails closed on missing files, stale/hand-edited output, or orphan
    files the catalog cannot account for. Pure read — never writes.
    """
    problems: list[str] = []
    expected: set[Path] = set()
    for palette in sorted(PALETTES):
        for key in all_keys():
            group, state = key.split("/")
            els = GROUPS[group][state](PALETTES[palette])
            want = svg_doc(els, SHIP_SIZE)
            dest = OUT_FLAT / palette / f"{group}-{state}.svg"
            expected.add(dest)
            rel = dest.relative_to(OUT_FLAT.parent.parent)
            if not dest.exists():
                problems.append(f"missing: {rel}")
            elif dest.read_text(encoding="utf-8") != want:
                problems.append(f"stale or hand-edited: {rel}")
    for extra in sorted(set(OUT_FLAT.glob("*/*.svg")) - expected):
        problems.append(
            f"orphan file outside catalog: "
            f"{extra.relative_to(OUT_FLAT.parent.parent)}")
    if problems:
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        raise SystemExit(
            f"flat library drift — {len(problems)} problem(s); "
            f"re-run with --all to regenerate")
    print(f"verified {len(expected)} flat SVGs against disk — no drift")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the flat-vector icon library.")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--verify", action="store_true",
                        help="diff a rebuild-in-memory against out/flat-svg")
    parser.add_argument("--group", help="one group name")
    parser.add_argument("--subject", help="one subject as group/state")
    parser.add_argument("--palette", choices=sorted(PALETTES))
    parser.add_argument("--all", action="store_true",
                        help="every subject for every palette")
    args = parser.parse_args()

    parity_check()

    if args.verify:
        return verify()

    palettes = [args.palette] if args.palette else sorted(PALETTES)

    if args.list:
        for group, subs in SUBJECTS.items():
            print(f"{group} ({len(subs)}): {', '.join(subs)}")
        print(f"\npalettes: {', '.join(palettes)}")
        print(f"total subjects: {len(all_keys())} "
              f"(x{len(palettes)} palettes = "
              f"{len(all_keys()) * len(palettes)} SVGs)")
        return 0

    if args.subject:
        if args.subject not in all_keys():
            print(f"unknown subject {args.subject}", file=sys.stderr)
            return 1
        keys = [args.subject]
    elif args.group:
        if args.group not in SUBJECTS:
            print(f"unknown group {args.group}", file=sys.stderr)
            return 1
        keys = [f"{args.group}/{s}" for s in SUBJECTS[args.group]]
    elif args.all:
        keys = all_keys()
    else:
        parser.print_help()
        return 1

    count = 0
    for palette in palettes:
        for key in keys:
            group, state = key.split("/")
            dest = build_one(group, state, palette)
            count += 1
        print(f"  {palette}: {len(keys)} subjects", flush=True)
    print(f"wrote {count} SVGs into {OUT_FLAT}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
