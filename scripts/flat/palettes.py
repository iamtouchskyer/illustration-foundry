"""Palette bridge: hex-only palette table derived from the clay script.

The clay generator is the single source of truth for palette colors.
Its values carry color names ("vivid orange #ff6b35"); flat SVG needs
bare hex, so we parse them out here — never re-declare a hex value.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from generate_clay_library import PALETTES as CLAY_PALETTES  # noqa: E402
from generate_clay_library import SUBJECTS as CLAY_SUBJECTS  # noqa: E402

_HEX = re.compile(r"#[0-9a-fA-F]{6}")


def _hex(value: str) -> str:
    m = _HEX.search(value)
    if not m:
        raise ValueError(f"palette slot has no hex: {value!r}")
    return m.group(0).lower()


PALETTES: dict[str, dict[str, str]] = {
    name: {slot: _hex(v) for slot, v in slots.items()}
    for name, slots in CLAY_PALETTES.items()
}

# Re-exported so the build script can parity-check against the clay
# catalog without importing the generator twice.
SUBJECTS = CLAY_SUBJECTS
