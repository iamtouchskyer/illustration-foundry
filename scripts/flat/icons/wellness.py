"""wellness group: 6 subjects (mirrors clay wellness/* templates)."""

from __future__ import annotations

from .. import motifs as M
from .. import svg as S


def journal(p):
    return [
        M.shadow(rx=24),
        *M.book_closed(62, 60, w=42, h=50, cover=p["PRIMARY"],
                       strap=p["SECONDARY"]),
        # feather resting on top
        S.path("M84 22 Q92 30 88 42 Q80 40 78 30 Q80 24 84 22 Z",
               fill=p["HIGHLIGHT"]),
        S.capsule(84, 24, 82, 44, 2.5, p["HIGHLIGHT"]),
    ]


def mood_checkin(p):
    def coin(cx, fill, mouth):
        els = [S.circle(cx, 56, 16, fill=fill),
               S.circle(cx - 5, 51, 2.2, fill="#ffffff"),
               S.circle(cx + 5, 51, 2.2, fill="#ffffff")]
        if mouth == "smile":
            els.append(S.path(S.arc_d(cx, 58, 7, 20, 160), stroke="#ffffff",
                              width=3))
        elif mouth == "flat":
            els.append(S.capsule(cx - 5, 63, cx + 5, 63, 3, "#ffffff"))
        else:  # frown
            els.append(S.path(S.arc_d(cx, 70, 7, 200, 340), stroke="#ffffff",
                              width=3))
        return els

    return [
        M.shadow(rx=30),
        *coin(34, p["PRIMARY"], "smile"),
        *coin(64, p["SECONDARY"], "flat"),
        *coin(94, p["PRIMARY"], "frown"),
        S.circle(64, 84, 4.5, fill=p["HIGHLIGHT"]),
    ]


def calm_breathing(p):
    return [
        M.shadow(rx=24),
        S.circle(62, 62, 26, fill=p["PRIMARY"]),
        S.circle(62, 62, 19, fill=p["HIGHLIGHT"], opacity=0.5),
        S.circle(62, 62, 12, fill=p["HIGHLIGHT"], opacity=0.6),
        M.leaf(98, 28, s=8, color=p["SECONDARY"], tilt=24),
    ]


def reflection(p):
    return [
        M.shadow(rx=22),
        S.circle(60, 52, 26, fill=p["PRIMARY"]),
        S.circle(60, 52, 20, fill=p["TERTIARY"]),
        S.capsule(72, 72, 82, 92, 7, p["PRIMARY"]),
        M.sparkle(52, 42, s=5, color=p["SECONDARY"]),
    ]


def safe_space(p):
    return [
        M.shadow(rx=28),
        # house body + roof
        S.rect(38, 56, 52, 36, rx=4, fill=p["PRIMARY"]),
        S.polygon([(32, 58), (64, 28), (96, 58)], fill=p["HIGHLIGHT"]),
        # round door
        S.circle(64, 78, 11, fill=p["TERTIARY"]),
        M.heart(64, 98, s=7, color=p["SECONDARY"]),
    ]


def session_complete(p):
    return [
        M.shadow(rx=26),
        # ripple
        S.ellipse(64, 88, 32, 8, fill=p["TERTIARY"]),
        # lotus petals
        M.leaf(64, 62, s=18, color=p["PRIMARY"]),
        M.leaf(48, 66, s=15, color=p["HIGHLIGHT"], tilt=-32),
        M.leaf(80, 66, s=15, color=p["HIGHLIGHT"], tilt=32),
        M.sparkle(96, 34, s=5, color=p["SECONDARY"]),
    ]


ICONS = {
    "journal": journal,
    "mood-checkin": mood_checkin,
    "calm-breathing": calm_breathing,
    "reflection": reflection,
    "safe-space": safe_space,
    "session-complete": session_complete,
}
