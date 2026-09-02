"""community group: 8 subjects (mirrors clay community/* templates)."""

from __future__ import annotations

from .. import motifs as M
from .. import svg as S


def _stool(cx, cy, color, leg=None):
    leg = leg or color
    return [
        S.ellipse(cx, cy, 16, 7, fill=color),
        S.line(cx - 10, cy + 4, cx - 13, cy + 24, leg, 4.5),
        S.line(cx + 10, cy + 4, cx + 13, cy + 24, leg, 4.5),
    ]


def _cup(cx, cy, color):
    return [
        S.rect(cx - 7, cy - 6, 14, 12, rx=3, fill=color),
        S.path(S.arc_d(cx + 8, cy - 1, 4.5, -80, 80), stroke=color,
               width=3),
        S.path(f"M{S._n(cx - 3)} {S._n(cy - 10)} q2 -3 0 -6", stroke=color,
               width=2.5, cap="round"),
        S.path(f"M{S._n(cx + 3)} {S._n(cy - 10)} q2 -3 0 -6", stroke=color,
               width=2.5, cap="round"),
    ]


def empty_room(p):
    return [
        M.shadow(rx=32),
        *_stool(40, 68, p["PRIMARY"], leg=p["HIGHLIGHT"]),
        *_stool(88, 68, p["PRIMARY"], leg=p["HIGHLIGHT"]),
        *_cup(64, 86, p["SECONDARY"]),
    ]


def open_table(p):
    return [
        M.shadow(rx=30),
        *_stool(44, 62, p["PRIMARY"], leg=p["HIGHLIGHT"]),
        *_cup(44, 42, p["SECONDARY"]),
        *_stool(88, 68, p["TERTIARY"]),
    ]


def anon_mask(p):
    mask = S.group([
        S.path("M30 56 Q30 30 64 30 Q98 30 98 56 Q98 82 64 80 Q30 82 30 56 Z",
               fill=p["PRIMARY"]),
        S.ellipse(50, 52, 8, 5, fill="#ffffff"),
        S.ellipse(78, 52, 8, 5, fill="#ffffff"),
        S.path("M56 68 Q64 74 72 68", stroke=p["HIGHLIGHT"], width=4,
               cap="round"),
    ], transform=S.rot(-8, 64, 56))
    return [M.shadow(rx=30), mask]


def direct_message(p):
    return [
        M.shadow(rx=28),
        *M.bubble(44, 44, w=48, h=34, color=p["PRIMARY"], tail_side=-1),
        *M.bubble(84, 72, w=48, h=34, color=p["SECONDARY"], tail_side=1),
        M.sparkle(64, 58, s=5, color=p["HIGHLIGHT"]),
    ]


def waiting_reply(p):
    return [
        M.shadow(rx=26),
        *M.bubble(58, 52, w=60, h=42, color=p["PRIMARY"], tail_side=-1),
        S.circle(44, 52, 4, fill=p["SECONDARY"]),
        S.circle(58, 52, 4, fill=p["SECONDARY"]),
        S.circle(72, 52, 4, fill=p["SECONDARY"]),
        *M.clock(100, 82, r=14, rim=p["TERTIARY"], face="#ffffff",
                 hands=p["SECONDARY"]),
    ]


def reported(p):
    return [
        M.shadow(rx=24),
        *M.flag(52, 54, pole_h=56, color=p["PRIMARY"],
                pole=p["HIGHLIGHT"]),
        M.shield(90, 84, w=24, h=28, color=p["SECONDARY"]),
    ]


def blocked(p):
    return [
        M.shadow(rx=26),
        S.group([*M.bubble(64, 58, w=56, h=40, color=p["PRIMARY"]),
                 S.capsule(44, 76, 86, 42, 9, p["SECONDARY"])],
                transform=S.rot(-7, 64, 58)),
    ]


def content_removed(p):
    return [
        M.shadow(rx=24),
        *M.sheet(52, 62, w=38, h=46, color=p["TERTIARY"]),
        # dissolving pieces drifting off the top-right corner
        S.circle(80, 34, 4, fill=p["TERTIARY"]),
        S.circle(90, 26, 3, fill=p["TERTIARY"]),
        S.circle(98, 36, 2.5, fill=p["TERTIARY"]),
        S.rect(86, 80, 16, 20, rx=4, fill=p["PRIMARY"]),
        S.rect(82, 76, 24, 5, rx=2.5, fill=p["PRIMARY"]),
    ]


ICONS = {
    "empty-room": empty_room,
    "open-table": open_table,
    "anon-mask": anon_mask,
    "direct-message": direct_message,
    "waiting-reply": waiting_reply,
    "reported": reported,
    "blocked": blocked,
    "content-removed": content_removed,
}
