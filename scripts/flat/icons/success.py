"""success group: 6 subjects (mirrors clay success/* templates)."""

from __future__ import annotations

from .. import motifs as M
from .. import svg as S


def done(p):
    return [
        M.shadow(rx=24),
        M.check(60, 56, s=26, color=p["PRIMARY"], weight=14),
        M.sparkle(98, 30, s=7, color=p["SECONDARY"]),
        S.circle(36, 34, 3.5, fill=p["HIGHLIGHT"]),
    ]


def saved(p):
    return [
        M.shadow(rx=26),
        *M.sheet(58, 54, w=44, h=56, color=p["PRIMARY"], rx=6),
        *M.sheet_lines(58, 44, 26, p["HIGHLIGHT"], n=3, gap=9),
        M.shield(88, 78, w=26, h=32, color=p["SECONDARY"]),
        M.check(88, 77, s=6, color="#ffffff", weight=4),
    ]


def published(p):
    plane = S.group([
        S.polygon([(0, 0), (44, 12), (14, 22)], fill=p["PRIMARY"]),
        S.polygon([(14, 22), (44, 12), (20, 32)], fill=p["HIGHLIGHT"]),
    ], transform=f"{S.tr(30, 28)} {S.rot(-12)}")
    arc = S.path(S.arc_d(52, 78, 34, 200, 268), stroke=p["SECONDARY"],
                 width=5, cap="round")
    return [M.shadow(rx=24), arc, plane]


def milestone(p):
    return [
        M.shadow(rx=24),
        S.path("M28 96 Q64 66 100 96 Z", fill=p["TERTIARY"]),
        S.group(M.flag(58, 52, pole_h=46, color=p["PRIMARY"],
                       pole=p["HIGHLIGHT"])),
        S.circle(82, 28, 3.5, fill=p["SECONDARY"]),
    ]


def all_clear(p):
    return [
        M.shadow(rx=24),
        M.shield(64, 56, w=52, h=62, color=p["PRIMARY"]),
        M.shield(64, 58, w=40, h=48, color=p["HIGHLIGHT"]),
        M.check(64, 56, s=11, color="#ffffff", weight=7),
        M.sparkle(102, 30, s=6, color=p["SECONDARY"]),
        M.sparkle(26, 42, s=4.5, color=p["SECONDARY"]),
    ]


def streak(p):
    return [
        M.shadow(rx=24),
        *M.steps(74, 82, n=3, w=13, h_step=9, color=p["TERTIARY"]),
        *M.flame(52, 50, s=22, color=p["PRIMARY"], inner=p["HIGHLIGHT"]),
    ]


ICONS = {
    "done": done,
    "saved": saved,
    "published": published,
    "milestone": milestone,
    "all-clear": all_clear,
    "streak": streak,
}
