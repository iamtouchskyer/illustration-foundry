"""notifications group: 5 subjects (mirrors clay notifications/*)."""

from __future__ import annotations

from .. import motifs as M
from .. import svg as S


def new_message(p):
    return [
        M.shadow(rx=26),
        *M.envelope(58, 62, w=52, h=38, color=p["PRIMARY"],
                    flap=p["HIGHLIGHT"]),
        S.circle(92, 42, 11, fill=p["SECONDARY"]),
        S.circle(92, 42, 4, fill="#ffffff"),
    ]


def alert_warning(p):
    tri = S.polygon([(60, 22), (96, 86), (24, 86)], fill=p["PRIMARY"])
    inner = S.polygon([(60, 34), (88, 82), (32, 82)], fill=p["HIGHLIGHT"],
                      opacity=0.5)
    mark = S.capsule(60, 48, 60, 66, 7, "#ffffff")
    dot = S.circle(60, 76, 3.6, fill="#ffffff")
    bolt = S.polygon([(104, 30), (96, 48), (103, 48), (95, 66), (110, 44),
                      (103, 44)], fill=p["SECONDARY"])
    return [M.shadow(rx=28), tri, inner, mark, dot, bolt]


def reminder(p):
    return [
        M.shadow(rx=22),
        *M.bell(54, 54, r=18, color=p["PRIMARY"],
                clapper=p["HIGHLIGHT"]),
        S.circle(94, 78, 15, fill=p["SECONDARY"]),
        S.circle(94, 78, 11, fill="#ffffff"),
        S.path("M94 72 V78 L99 82", stroke=p["SECONDARY"], width=3.5,
               cap="round"),
    ]


def digest(p):
    return [
        M.shadow(rx=24),
        *M.sheet(64, 50, w=44, h=18, color=p["TERTIARY"]),
        *M.sheet(64, 62, w=48, h=18, color="#ffffff"),
        *M.sheet(64, 74, w=52, h=18, color=p["TERTIARY"]),
        S.rect(58, 40, 12, 52, rx=5, fill=p["PRIMARY"]),
        S.capsule(56, 44, 72, 44, 4, p["HIGHLIGHT"]),
    ]


def announcement(p):
    horn = S.group([
        S.polygon([(0, 10), (26, -6), (26, 30), (0, 14)], fill=p["PRIMARY"]),
        S.rect(-14, 8, 16, 8, rx=3, fill=p["HIGHLIGHT"]),
    ], transform=f"{S.tr(36, 46)} {S.rot(-12)}")
    waves = [
        S.path(S.arc_d(78, 52, 12, -50, 50), stroke=p["SECONDARY"],
               width=5),
        S.path(S.arc_d(82, 52, 20, -50, 50), stroke=p["SECONDARY"],
               width=5),
    ]
    return [M.shadow(rx=24), horn, *waves]


ICONS = {
    "new-message": new_message,
    "alert-warning": alert_warning,
    "reminder": reminder,
    "digest": digest,
    "announcement": announcement,
}
