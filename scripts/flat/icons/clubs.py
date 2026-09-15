"""clubs group: 5 subjects (school club scenes).

Added for products that illustrate *school clubs* rather than UI states.
Each scene leads with the same single contact shadow and keeps the subject
inside the band ~y=18..96, like every other group.
"""

from __future__ import annotations

from .. import motifs as M
from .. import svg as S


def art_club(p):
    return [
        M.shadow(rx=28),
        *M.palette(58, 62, w=50, h=40, color=p["PRIMARY"],
                   holes=p["HIGHLIGHT"]),
        S.path("M84 40 L104 20", stroke=p["TERTIARY"], width=7, cap="round"),
        S.polygon([(104, 20), (99, 33), (91, 25)], fill=p["SECONDARY"]),
    ]


def coffee_club(p):
    return [
        M.shadow(rx=26),
        *M.coffee(64, 58, w=36, h=34, color=p["PRIMARY"],
                  lid=p["SECONDARY"], steam=p["TERTIARY"]),
        S.ellipse(64, 84, 30, 6, fill=p["HIGHLIGHT"]),
    ]


def science_club(p):
    return [
        M.shadow(rx=26),
        *M.flask(64, 60, w=42, h=46, color=p["HIGHLIGHT"],
                 liquid=p["PRIMARY"]),
        S.circle(84, 34, 5, fill=p["SECONDARY"]),
        S.circle(94, 46, 3.4, fill=p["SECONDARY"]),
    ]


def chess_club(p):
    return [
        M.shadow(rx=26),
        S.rect(38, 60, 52, 26, rx=4, fill=p["HIGHLIGHT"]),
        *M.chess(64, 56, s=1.3, color=p["PRIMARY"], base=p["TERTIARY"]),
    ]


def culture_club(p):
    return [
        M.shadow(rx=26),
        *M.globe(64, 60, r=22, color=p["HIGHLIGHT"],
                 line=p["SECONDARY"], stand=p["TERTIARY"]),
        S.path("M96 30 L96 58", stroke=p["TERTIARY"], width=3, cap="round"),
        S.path("M96 30 L112 36 L96 43 Z", fill=p["PRIMARY"]),
    ]


ICONS = {
    "art-club": art_club,
    "coffee-club": coffee_club,
    "science-club": science_club,
    "chess-club": chess_club,
    "culture-club": culture_club,
}
