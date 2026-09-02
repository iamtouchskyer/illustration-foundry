"""onboarding group: 6 subjects (mirrors clay onboarding/* templates)."""

from __future__ import annotations

from .. import motifs as M
from .. import svg as S


def welcome(p):
    arch = S.path("M40 96 V54 A24 24 0 0 1 88 54 V96 H78 V56 A14 14 0 0 0 "
                  "50 56 V96 Z", fill=p["PRIMARY"])
    inner = S.path("M50 96 V56 A14 14 0 0 1 78 56 V96 Z",
                   fill=p["TERTIARY"])
    mat = S.rect(48, 98, 32, 9, rx=4, fill=p["SECONDARY"])
    return [M.shadow(rx=28), inner, arch, mat]


def get_started(p):
    base = S.rect(46, 92, 36, 12, rx=5, fill=p["TERTIARY"])
    arrow = S.group([
        S.capsule(0, 30, 0, 6, 12, p["PRIMARY"]),
        S.polygon([(-14, 10), (14, 10), (0, -16)], fill=p["PRIMARY"]),
        S.polygon([(-6, 4), (6, 4), (0, -8)], fill=p["HIGHLIGHT"]),
    ], transform=f"{S.tr(64, 46)} {S.rot(18)}")
    return [M.shadow(rx=22), base, arrow]


def setup(p):
    return [
        M.shadow(rx=26),
        *M.gear(50, 48, r=20, color=p["PRIMARY"], hole="#ffffff"),
        S.capsule(36, 92, 100, 92, 8, p["TERTIARY"]),
        S.circle(82, 92, 9, fill=p["SECONDARY"]),
        S.circle(82, 92, 3.5, fill="#ffffff"),
    ]


def tutorial(p):
    return [
        M.shadow(rx=28),
        *M.book_open(64, 72, w=56, h=38, cover=p["PRIMARY"],
                     page=p["TERTIARY"]),
        S.path("M64 26 V14 M56 22 L64 13 L72 22", stroke=p["SECONDARY"],
               width=5.5, cap="round", join="round"),
    ]


def invite_team(p):
    return [
        M.shadow(rx=26),
        *M.person(46, 36, s=0.95, color=p["SECONDARY"]),
        *M.person(64, 30, s=1.05, color=p["TERTIARY"]),
        *M.person(82, 36, s=0.95, color=p["SECONDARY"]),
        *M.envelope(64, 68, w=52, h=34, color=p["PRIMARY"],
                    flap=p["HIGHLIGHT"]),
    ]


def create_first(p):
    return [
        M.shadow(rx=24),
        S.rect(46, 92, 36, 12, rx=5, fill=p["TERTIARY"]),
        S.path("M50 60 V92 M78 60 V92", stroke=p["TERTIARY"], width=7),
        S.rect(56, 30, 16, 44, rx=8, fill=p["PRIMARY"]),
        S.rect(42, 44, 44, 16, rx=8, fill=p["PRIMARY"]),
        S.rect(60, 34, 8, 36, rx=4, fill=p["HIGHLIGHT"]),
    ]


ICONS = {
    "welcome": welcome,
    "get-started": get_started,
    "setup": setup,
    "tutorial": tutorial,
    "invite-team": invite_team,
    "create-first": create_first,
}
