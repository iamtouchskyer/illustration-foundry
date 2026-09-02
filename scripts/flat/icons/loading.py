"""loading group: 6 subjects (mirrors clay loading/* templates)."""

from __future__ import annotations

from .. import motifs as M
from .. import svg as S


def loading(p):
    return [
        M.shadow(rx=24),
        *M.ring_progress(64, 56, r=24, color=p["PRIMARY"],
                         track=p["TERTIARY"], span=270,
                         spark=p["SECONDARY"]),
    ]


def processing(p):
    return [
        M.shadow(rx=26),
        *M.sheet(28, 76, w=22, h=28, color=p["TERTIARY"]),
        *M.gear(62, 50, r=17, color=p["PRIMARY"], hole="#ffffff"),
        *M.gear(92, 74, r=13, color=p["HIGHLIGHT"], hole="#ffffff"),
    ]


def uploading(p):
    return [
        M.shadow(rx=24),
        *M.cloud(64, 40, s=1.2, color=p["PRIMARY"]),
        S.path("M64 92 V62 M54 72 L64 61 L74 72", stroke=p["SECONDARY"],
               width=6.5, cap="round", join="round"),
        *M.sheet(64, 100, w=24, h=12, color=p["TERTIARY"]),
    ]


def syncing(p):
    top = S.path(S.arc_d(64, 58, 26, 200, 330), stroke=p["PRIMARY"],
                 width=8)
    top_head = S.polygon([(91, 62), (95, 46), (77, 48)], fill=p["PRIMARY"])
    bot = S.path(S.arc_d(64, 58, 26, 20, 150), stroke=p["HIGHLIGHT"],
                 width=8)
    bot_head = S.polygon([(37, 54), (33, 70), (51, 68)],
                         fill=p["HIGHLIGHT"])
    return [
        M.shadow(rx=24),
        top, top_head, bot, bot_head,
        *M.sheet(64, 58, w=18, h=22, color=p["TERTIARY"]),
    ]


def importing(p):
    return [
        M.shadow(rx=26),
        *M.sheet(64, 30, w=26, h=20, color=p["TERTIARY"]),
        *M.sheet(64, 42, w=30, h=18, color="#ffffff"),
        *M.box(64, 78, w=52, h=32, color=p["PRIMARY"],
               flap=p["HIGHLIGHT"], open_=True),
    ]


def deploying(p):
    body = S.path("M64 18 C76 34 76 58 64 72 C52 58 52 34 64 18 Z",
                  fill=p["PRIMARY"])
    window = S.circle(64, 42, 6, fill=p["TERTIARY"])
    fin_l = S.polygon([(54, 58), (42, 76), (56, 72)], fill=p["HIGHLIGHT"])
    fin_r = S.polygon([(74, 58), (86, 76), (72, 72)], fill=p["HIGHLIGHT"])
    pad = S.capsule(44, 96, 84, 96, 7, p["TERTIARY"])
    puff = S.circle(88, 88, 6, fill=p["SECONDARY"], opacity=0.6)
    return [M.shadow(rx=22), pad, body, fin_l, fin_r, window, puff]


ICONS = {
    "loading": loading,
    "processing": processing,
    "uploading": uploading,
    "syncing": syncing,
    "importing": importing,
    "deploying": deploying,
}
