"""error group: 12 subjects (mirrors clay error/* templates)."""

from __future__ import annotations

from .. import motifs as M
from .. import svg as S


def not_found_404(p):
    return [
        M.shadow(rx=26),
        *M.sheet(56, 60, w=42, h=52, color=p["PRIMARY"], rx=5),
        S.circle(56, 60, 12, fill="#ffffff"),
        *M.magnifier(92, 76, r=12, ring=p["SECONDARY"],
                     glass="#ffffff"),
    ]


def server_error_500(p):
    blocks = []
    for i, y in enumerate((86, 66)):
        blocks.append(S.rect(38, y - 9, 52, 18, rx=4, fill=p["PRIMARY"]))
        blocks.append(S.circle(46, y, 2.6, fill=p["HIGHLIGHT"]))
        blocks.append(S.circle(54, y, 2.6, fill=p["HIGHLIGHT"]))
    top = S.group(
        [S.rect(38, 37, 52, 18, rx=4, fill=p["PRIMARY"]),
         S.circle(46, 46, 2.6, fill=p["HIGHLIGHT"]),
         S.circle(54, 46, 2.6, fill=p["HIGHLIGHT"])],
        transform=S.rot(-16, 64, 46))
    warn = S.polygon([(100, 70), (112, 92), (88, 92)],
                     fill=p["SECONDARY"])
    warn_mark = S.capsule(100, 78, 100, 84, 3.5, "#ffffff")
    warn_dot = S.circle(100, 88, 2, fill="#ffffff")
    return [M.shadow(rx=28), *blocks, top, warn, warn_mark, warn_dot]


def offline(p):
    arcs = [
        S.path(S.arc_d(64, 78, 12, 225, 315), stroke=p["HIGHLIGHT"],
               width=6),
        S.path(S.arc_d(64, 78, 24, 225, 315), stroke=p["PRIMARY"],
               width=6),
    ]
    broken_l = S.path(S.arc_d(64, 78, 36, 225, 262), stroke=p["PRIMARY"],
                      width=6)
    broken_r = S.path(S.arc_d(64, 78, 36, 278, 315), stroke=p["PRIMARY"],
                      width=6)
    return [
        M.shadow(rx=24),
        *M.cloud(64, 82, s=1.0, color=p["PRIMARY"]),
        *arcs, broken_l, broken_r,
    ]


def no_permission(p):
    ring = S.circle(56, 54, 26, stroke=p["PRIMARY"], width=11)
    slash = S.capsule(38, 72, 74, 36, 11, p["HIGHLIGHT"])
    return [
        M.shadow(rx=28),
        ring, slash,
        *M.key(98, 84, s=0.8, color=p["SECONDARY"], rot_deg=-30),
    ]


def account_disabled(p):
    ring = S.path(S.arc_d(64, 56, 24, -60, 240), stroke=p["PRIMARY"],
                  width=10)
    bar = S.capsule(64, 26, 64, 44, 10, p["HIGHLIGHT"])
    return [
        M.shadow(rx=24),
        S.group([ring, bar], transform=S.rot(12, 64, 56)),
        M.moon(98, 84, r=10, color=p["SECONDARY"]),
    ]


def session_expired(p):
    return [
        M.shadow(rx=24),
        *M.hourglass(56, 58, s=1.2, frame=p["PRIMARY"],
                     glass=p["TERTIARY"], sand=p["HIGHLIGHT"]),
        S.circle(96, 82, 13, fill=p["SECONDARY"]),
        S.path("M96 75 V82 L101 85", stroke="#ffffff", width=3.5,
               cap="round"),
    ]


def region_locked(p):
    globe = S.circle(58, 52, 26, fill=p["PRIMARY"])
    band = S.path(S.arc_d(58, 52, 26, 8, 172), stroke=p["TERTIARY"],
                  width=6)
    meridian = S.ellipse(58, 52, 11, 26, stroke=p["TERTIARY"], width=4)
    return [
        M.shadow(rx=24),
        globe, band, meridian,
        *M.padlock(86, 78, s=1.05, color=p["SECONDARY"],
                   keyhole="#ffffff"),
    ]


def broken_link(p):
    l1 = S.rect(24, 48, 26, 22, rx=11, stroke=p["PRIMARY"], width=8)
    l2 = S.rect(58, 58, 26, 22, rx=11, stroke=p["HIGHLIGHT"], width=8,
                transform=S.rot(8, 71, 69))
    return [
        M.shadow(rx=24),
        l1, l2,
        S.polygon([(100, 46), (108, 50), (102, 56)], fill=p["TERTIARY"]),
    ]


def rate_limited(p):
    face = S.circle(56, 60, 27, fill=p["TERTIARY"], stroke=p["PRIMARY"],
                    width=6)
    needle = S.capsule(56, 60, 74, 42, 6, p["SECONDARY"])
    hub = S.circle(56, 60, 4.5, fill=p["PRIMARY"])
    bar1 = S.capsule(98, 60, 98, 78, 7, p["SECONDARY"])
    bar2 = S.capsule(110, 60, 110, 78, 7, p["SECONDARY"])
    return [M.shadow(rx=26), face, needle, hub, bar1, bar2]


def maintenance(p):
    wrench = S.group([
        S.capsule(0, 0, 34, 34, 8, p["PRIMARY"]),
        S.circle(-2, -2, 9, fill=p["PRIMARY"]),
        S.circle(-2, -2, 4, fill="#ffffff"),
    ], transform=f"{S.tr(36, 30)}")
    driver = S.group([
        S.capsule(0, 0, 30, -30, 6, p["HIGHLIGHT"]),
        S.rect(26, -38, 12, 10, rx=3, fill=p["PRIMARY"]),
    ], transform=f"{S.tr(36, 66)}")
    return [
        M.shadow(rx=26),
        *M.gear(72, 74, r=18, color=p["TERTIARY"], hole="#ffffff"),
        wrench, driver,
        S.polygon([(100, 62), (114, 92), (86, 92)], fill=p["SECONDARY"]),
        S.rect(94, 82, 12, 10, fill=p["SECONDARY"]),
    ]


def payment_failed(p):
    return [
        M.shadow(rx=26),
        S.group(M.card(58, 58, w=52, h=34, color=p["PRIMARY"],
                       stripe=p["HIGHLIGHT"]),
                transform=S.rot(-14, 58, 58)),
        S.circle(98, 82, 12, fill=p["SECONDARY"]),
        *M.cross(98, 82, s=5.5, color="#ffffff", weight=4),
    ]


def timeout(p):
    return [
        M.shadow(rx=24),
        *M.clock(54, 60, r=22, rim=p["PRIMARY"], face="#ffffff",
                 hands=p["HIGHLIGHT"]),
        S.group(M.hourglass(94, 84, s=0.62, frame=p["SECONDARY"],
                            glass=p["TERTIARY"], sand=p["HIGHLIGHT"]),
                transform=S.rot(90, 94, 84)),
    ]


ICONS = {
    "not-found-404": not_found_404,
    "server-error-500": server_error_500,
    "offline": offline,
    "no-permission": no_permission,
    "account-disabled": account_disabled,
    "session-expired": session_expired,
    "region-locked": region_locked,
    "broken-link": broken_link,
    "rate-limited": rate_limited,
    "maintenance": maintenance,
    "payment-failed": payment_failed,
    "timeout": timeout,
}
