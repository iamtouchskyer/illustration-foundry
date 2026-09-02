"""auth group: 5 subjects (mirrors clay auth/* templates)."""

from __future__ import annotations

from .. import motifs as M
from .. import svg as S


def sign_in(p):
    arch = S.path("M36 100 V52 A26 26 0 0 1 88 52 V100 H80 V54 A18 18 0 0 0 "
                  "44 54 V100 Z", fill=p["PRIMARY"])
    inner = S.path("M44 100 V54 A18 18 0 0 1 80 54 V100 Z",
                   fill=p["TERTIARY"])
    keyhole = S.circle(62, 70, 4.5, fill=p["PRIMARY"])
    return [
        M.shadow(rx=28), inner, arch, keyhole,
        *M.key(100, 42, s=0.9, color=p["SECONDARY"], rot_deg=135),
    ]


def sign_up(p):
    return [
        M.shadow(rx=26),
        S.rect(34, 38, 44, 58, rx=8, fill=p["PRIMARY"]),
        S.rect(40, 44, 32, 46, rx=5, fill=p["TERTIARY"]),
        S.circle(56, 58, 8, fill=p["PRIMARY"]),
        S.capsule(46, 78, 66, 78, 5, p["PRIMARY"]),
        S.path("M96 52 V74 M85 63 H107", stroke=p["SECONDARY"], width=8,
               cap="round"),
    ]


def two_factor(p):
    return [
        M.shadow(rx=24),
        M.shield(72, 50, w=40, h=48, color=p["SECONDARY"]),
        *M.padlock(54, 66, s=1.35, color=p["PRIMARY"],
                   keyhole=p["HIGHLIGHT"]),
    ]


def password_reset(p):
    return [
        M.shadow(rx=24),
        *M.key(60, 62, s=1.3, color=p["PRIMARY"], rot_deg=-45),
        S.path(S.arc_d(84, 40, 14, 300, 150), stroke=p["SECONDARY"],
               width=6),
        S.polygon([(72, 44), (70, 30), (84, 36)], fill=p["SECONDARY"]),
    ]


def magic_link(p):
    return [
        M.shadow(rx=26),
        *M.envelope(58, 62, w=50, h=36, color=p["PRIMARY"],
                    flap=p["HIGHLIGHT"]),
        S.rect(86, 24, 14, 24, rx=7, stroke=p["SECONDARY"], width=6),
        S.rect(94, 36, 14, 24, rx=7, stroke=p["SECONDARY"], width=6),
        M.sparkle(34, 30, s=6, color=p["SECONDARY"]),
    ]


ICONS = {
    "sign-in": sign_in,
    "sign-up": sign_up,
    "two-factor": two_factor,
    "password-reset": password_reset,
    "magic-link": magic_link,
}
