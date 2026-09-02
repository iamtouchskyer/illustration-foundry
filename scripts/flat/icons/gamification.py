"""gamification group: 10 subjects (mirrors clay gamification/*)."""

from __future__ import annotations

from .. import motifs as M
from .. import svg as S


def streak_freeze(p):
    return [
        M.shadow(rx=22),
        S.rect(40, 30, 48, 52, rx=10, fill=p["TERTIARY"]),
        S.rect(46, 36, 36, 40, rx=7, fill="#ffffff", opacity=0.45),
        *M.flame(64, 58, s=15, color=p["PRIMARY"], inner=p["HIGHLIGHT"]),
        # snowflake: three crossed strokes
        S.group([
            S.line(0, -8, 0, 8, p["SECONDARY"], 3.5),
            S.line(-7, -4, 7, 4, p["SECONDARY"], 3.5),
            S.line(-7, 4, 7, -4, p["SECONDARY"], 3.5),
        ], transform=S.tr(96, 34)),
    ]


def leaderboard_podium(p):
    podium = [
        S.rect(24, 66, 26, 30, rx=4, fill=p["PRIMARY"]),
        S.rect(51, 50, 26, 46, rx=4, fill=p["PRIMARY"]),
        S.rect(78, 72, 26, 24, rx=4, fill=p["PRIMARY"]),
        S.rect(51, 50, 26, 8, rx=4, fill=p["HIGHLIGHT"]),
        S.rect(24, 66, 26, 6, rx=3, fill=p["HIGHLIGHT"]),
        S.rect(78, 72, 26, 6, rx=3, fill=p["HIGHLIGHT"]),
    ]
    return [
        M.shadow(rx=34),
        *podium,
        *M.trophy(64, 32, s=0.8, color=p["SECONDARY"], accent=p["HIGHLIGHT"]),
    ]


def level_up(p):
    return [
        M.shadow(rx=26),
        *M.steps(56, 84, n=3, w=15, h_step=10, color=p["TERTIARY"]),
        S.path("M36 74 Q64 30 96 34", stroke=p["PRIMARY"], width=8,
               cap="round"),
        S.polygon([(90, 22), (104, 32), (88, 42)], fill=p["PRIMARY"]),
        M.sparkle(96, 18, s=6, color=p["SECONDARY"]),
    ]


def achievement_badge(p):
    return [
        M.shadow(rx=20),
        *M.medal(64, 62, r=22, color=p["PRIMARY"], ribbon=p["TERTIARY"],
                 emblem=None),
        M.star(64, 62, r=10, color=p["SECONDARY"]),
        M.sparkle(98, 36, s=5, color=p["HIGHLIGHT"]),
    ]


def quest(p):
    scroll = [
        S.rect(30, 38, 68, 48, rx=6, fill=p["PRIMARY"]),
        S.rect(36, 44, 56, 36, rx=4, fill=p["HIGHLIGHT"]),
        S.circle(30, 62, 8, fill=p["PRIMARY"]),
        S.circle(98, 62, 8, fill=p["PRIMARY"]),
    ]
    trail = S.path("M44 72 Q58 58 66 66 T88 54", stroke=p["TERTIARY"],
                   width=5, cap="round",
                   transform=None)
    return [
        M.shadow(rx=30),
        *scroll, trail,
        *M.flag(88, 46, pole_h=22, color=p["SECONDARY"]),
    ]


def treasure_chest(p):
    return [
        M.shadow(rx=28),
        # open lid tilted back
        S.group([S.rect(34, 26, 60, 18, rx=7, fill=p["HIGHLIGHT"])],
                transform=S.rot(-14, 64, 34)),
        # glow tokens peeking out
        M.star(50, 46, r=6, color=p["SECONDARY"]),
        *M.coin(68, 48, r=6, color=p["SECONDARY"], inner="#ffffff"),
        *M.coin(82, 46, r=5, color=p["SECONDARY"], inner="#ffffff"),
        # chest body
        S.rect(34, 54, 60, 34, rx=7, fill=p["PRIMARY"]),
        S.rect(58, 54, 12, 34, fill=p["HIGHLIGHT"]),
        S.rect(56, 60, 16, 12, rx=4, fill=p["HIGHLIGHT"]),
    ]


def energy_hearts(p):
    return [
        M.shadow(rx=26),
        M.heart(34, 56, s=13, color=p["PRIMARY"]),
        M.heart(64, 56, s=13, color=p["PRIMARY"]),
        # chipped heart: whole heart minus a corner wedge
        S.group([M.heart(94, 56, s=13, color=p["HIGHLIGHT"]),
                 S.polygon([(99, 44), (109, 46), (104, 54)],
                           fill="#ffffff")]),
        S.polygon([(104, 52), (108, 56), (103, 58)], fill=p["HIGHLIGHT"]),
    ]


def gem_currency(p):
    return [
        M.shadow(rx=28),
        *M.gem(50, 52, s=1.4, color=p["PRIMARY"], facet=p["HIGHLIGHT"]),
        *M.coin(88, 72, r=9, color=p["SECONDARY"], inner="#ffffff"),
        *M.coin(88, 58, r=9, color=p["SECONDARY"], inner="#ffffff"),
        *M.coin(88, 44, r=9, color=p["SECONDARY"], inner="#ffffff"),
    ]


def daily_goal(p):
    return [
        M.shadow(rx=24),
        *M.target(60, 58, r=26, outer=p["PRIMARY"], mid="#ffffff",
                  inner=p["TERTIARY"]),
        M.check(60, 58, s=8, color=p["SECONDARY"], weight=5.5),
        M.sparkle(98, 32, s=5, color=p["HIGHLIGHT"]),
    ]


def practice_again(p):
    return [
        M.shadow(rx=24),
        *M.arrow_loop(64, 58, r=26, color=p["PRIMARY"], gap=80),
        M.star(64, 58, r=9, color=p["SECONDARY"]),
    ]


ICONS = {
    "streak-freeze": streak_freeze,
    "leaderboard-podium": leaderboard_podium,
    "level-up": level_up,
    "achievement-badge": achievement_badge,
    "quest": quest,
    "treasure-chest": treasure_chest,
    "energy-hearts": energy_hearts,
    "gem-currency": gem_currency,
    "daily-goal": daily_goal,
    "practice-again": practice_again,
}
