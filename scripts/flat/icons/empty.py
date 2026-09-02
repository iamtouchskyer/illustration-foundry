"""empty group: 12 subjects (mirrors clay empty/* templates)."""

from __future__ import annotations

from .. import motifs as M
from .. import svg as S


def empty_list(p):
    return [
        M.shadow(rx=26),
        *M.sheet(64, 30, w=22, h=26, color="#ffffff",
                 fold=p["TERTIARY"]),
        *M.folder(64, 66, w=48, h=34, color=p["PRIMARY"],
                  tab=p["HIGHLIGHT"], front=p["HIGHLIGHT"]),
    ]


def no_search_results(p):
    return [
        M.shadow(rx=26),
        *M.sheet(52, 60, w=38, h=46, color=p["TERTIARY"], fold=None),
        *M.sheet_lines(52, 52, 22, "#ffffff", n=3, gap=7),
        *M.magnifier(84, 44, r=17, ring=p["SECONDARY"],
                     glass="#ffffff", handle=p["SECONDARY"]),
    ]


def no_favorites(p):
    return [
        M.shadow(rx=24),
        *M.sheet(64, 78, w=40, h=14, color=p["TERTIARY"]),
        *M.sheet(64, 70, w=44, h=16, color="#ffffff"),
        M.star(64, 46, r=18, color=p["PRIMARY"], r_in=7.5),
        M.sparkle(94, 30, s=5, color=p["SECONDARY"]),
    ]


def empty_recycle(p):
    return [
        M.shadow(rx=24),
        *M.trash_bin(64, 66, color=p["PRIMARY"], lid=p["HIGHLIGHT"]),
        # lid propped half-open beside the bin
        S.group([S.capsule(0, 0, 26, -6, 5, p["HIGHLIGHT"])],
                transform=f"{S.tr(86, 40)} {S.rot(-24)}"),
        S.circle(38, 92, 6, fill="#ffffff", stroke=p["SECONDARY"],
                 width=2.5),
    ]


def empty_inbox(p):
    return [
        M.shadow(rx=26),
        S.rect(38, 70, 52, 8, rx=4, fill=p["HIGHLIGHT"]),
        S.polygon([(38, 74), (44, 52), (84, 52), (90, 74)],
                  fill=p["PRIMARY"]),
        *M.envelope(64, 30, w=34, h=24, color=p["SECONDARY"],
                    flap="#ffffff"),
    ]


def no_notifications(p):
    return [
        M.shadow(rx=22),
        *M.bell(58, 60, r=17, color=p["PRIMARY"],
                clapper=p["HIGHLIGHT"]),
        M.moon(94, 78, r=11, color=p["SECONDARY"]),
    ]


def no_team(p):
    return [
        M.shadow(rx=26),
        *M.folder(64, 58, w=50, h=36, color=p["PRIMARY"],
                  tab=p["HIGHLIGHT"]),
        *M.person(48, 82, s=1.15, color=p["SECONDARY"]),
        *M.person(80, 84, s=1.0, color=p["TERTIARY"]),
    ]


def no_projects(p):
    return [
        M.shadow(rx=26),
        S.rect(40, 48, 48, 34, rx=6, fill=p["PRIMARY"]),
        S.rect(36, 44, 56, 10, rx=5, fill=p["HIGHLIGHT"]),
        S.capsule(54, 40, 74, 40, 5, p["HIGHLIGHT"]),
        S.rect(58, 66, 16, 10, rx=3, fill=p["TERTIARY"]),
        M.leaf(96, 88, s=8, color=p["SECONDARY"], tilt=18),
    ]


def no_history(p):
    return [
        M.shadow(rx=24),
        *M.clock(54, 62, r=21, rim=p["PRIMARY"], face="#ffffff",
                 hands=p["HIGHLIGHT"]),
        *M.sheet(92, 44, w=20, h=26, color=p["TERTIARY"]),
    ]


def no_uploads(p):
    return [
        M.shadow(rx=24),
        *M.cloud(64, 46, s=1.25, color=p["PRIMARY"]),
        S.path("M64 74 V56 M55 64 L64 55 L73 64", stroke=p["HIGHLIGHT"],
               width=6, cap="round", join="round"),
        *M.sheet(64, 92, w=26, h=16, color=p["TERTIARY"]),
    ]


def empty_chat(p):
    return [
        M.shadow(rx=26),
        *M.bubble(60, 56, w=56, h=40, color=p["PRIMARY"], tail_side=-1),
        S.rect(46, 44, 28, 6, rx=3, fill=p["TERTIARY"]),
        S.rect(46, 56, 20, 6, rx=3, fill=p["TERTIARY"]),
        S.path("M98 38 V54 M90 46 H106", stroke=p["SECONDARY"], width=6,
               cap="round"),
    ]


def no_bookmarks(p):
    return [
        M.shadow(rx=24),
        *M.sheet(58, 58, w=40, h=52, color=p["TERTIARY"]),
        *M.sheet_lines(54, 48, 22, "#ffffff", n=3, gap=8),
        S.polygon([(78, 30), (90, 30), (90, 78), (84, 70), (78, 78)],
                  fill=p["PRIMARY"],
                  transform=S.rot(14, 84, 30)),
        M.star(30, 84, r=7, color=p["SECONDARY"]),
    ]


ICONS = {
    "empty-list": empty_list,
    "no-search-results": no_search_results,
    "no-favorites": no_favorites,
    "empty-recycle": empty_recycle,
    "empty-inbox": empty_inbox,
    "no-notifications": no_notifications,
    "no-team": no_team,
    "no-projects": no_projects,
    "no-history": no_history,
    "no-uploads": no_uploads,
    "empty-chat": empty_chat,
    "no-bookmarks": no_bookmarks,
}
