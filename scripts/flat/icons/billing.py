"""billing group: 6 subjects (mirrors clay billing/* templates)."""

from __future__ import annotations

from .. import motifs as M
from .. import svg as S


def storage_full(p):
    return [
        M.shadow(rx=26),
        # sheets packed to the brim
        *M.sheet(52, 44, w=24, h=14, color=p["TERTIARY"]),
        *M.sheet(72, 40, w=24, h=14, color="#ffffff"),
        # hovering sheet with nowhere to fit
        S.group([*M.sheet(64, 22, w=26, h=14, color=p["TERTIARY"])]),
        *M.box(64, 74, w=56, h=36, color=p["PRIMARY"],
               flap=p["HIGHLIGHT"], open_=True),
        S.circle(100, 46, 6, fill=p["SECONDARY"]),
        S.capsule(100, 38, 100, 33, 4, p["SECONDARY"]),
    ]


def upload_limit(p):
    return [
        M.shadow(rx=26),
        *M.capsule_bar(60, 58, w=72, h=16, track=p["TERTIARY"],
                       fill_color=p["PRIMARY"], ratio=1.0,
                       knob=p["HIGHLIGHT"]),
        *M.cloud(98, 40, s=0.75, color=p["SECONDARY"]),
        *M.sheet(60, 86, w=26, h=14, color=p["TERTIARY"]),
    ]


def feature_locked(p):
    return [
        M.shadow(rx=24),
        S.circle(56, 58, 28, fill=p["TERTIARY"]),
        *M.gear(56, 58, r=13, color=p["SECONDARY"], hole="#ffffff"),
        S.group([*M.padlock(84, 76, s=1.3, color=p["PRIMARY"],
                            keyhole=p["HIGHLIGHT"])],
                transform=S.rot(-12, 84, 76)),
    ]


def upgrade(p):
    return [
        M.shadow(rx=24),
        *M.steps(70, 84, n=2, w=16, h_step=10, color=p["TERTIARY"]),
        *M.crown(52, 42, s=1.35, color=p["PRIMARY"],
                 gem_color=p["SECONDARY"]),
    ]


def trial_ended(p):
    return [
        M.shadow(rx=26),
        *M.ticket(60, 56, w=58, h=30, color=p["PRIMARY"], perf=None,
                  tear_gap=8, stub_tilt=10),
        *M.clock(98, 84, r=12, rim=p["SECONDARY"], face="#ffffff",
                 hands=p["SECONDARY"]),
    ]


def subscribed(p):
    return [
        M.shadow(rx=24),
        S.rect(38, 36, 46, 62, rx=8, fill=p["PRIMARY"]),
        S.rect(44, 42, 34, 50, rx=5, fill=p["HIGHLIGHT"], opacity=0.4),
        M.star(61, 58, r=11, color=p["SECONDARY"]),
        S.circle(86, 86, 13, fill=p["TERTIARY"]),
        M.check(86, 86, s=6, color=p["SECONDARY"], weight=4.5),
        M.sparkle(94, 32, s=5, color=p["SECONDARY"]),
    ]


ICONS = {
    "storage-full": storage_full,
    "upload-limit": upload_limit,
    "feature-locked": feature_locked,
    "upgrade": upgrade,
    "trial-ended": trial_ended,
    "subscribed": subscribed,
}
