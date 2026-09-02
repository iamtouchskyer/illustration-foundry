"""learning group: 6 subjects (mirrors clay learning/* templates)."""

from __future__ import annotations

from .. import motifs as M
from .. import svg as S


def lesson_complete(p):
    return [
        M.shadow(rx=28),
        *M.book_open(64, 70, w=56, h=38, cover=p["PRIMARY"],
                     page=p["TERTIARY"]),
        M.check(64, 42, s=12, color=p["SECONDARY"], weight=8),
        S.circle(92, 26, 3.5, fill=p["HIGHLIGHT"]),
        S.circle(36, 30, 3, fill=p["HIGHLIGHT"]),
    ]


def lesson_locked(p):
    return [
        M.shadow(rx=24),
        *M.book_closed(58, 56, w=40, h=48, cover=p["PRIMARY"],
                       page=p["TERTIARY"]),
        *M.padlock(84, 72, s=1.0, color=p["SECONDARY"],
                   keyhole="#ffffff"),
    ]


def wrong_answer(p):
    return [
        M.shadow(rx=24),
        S.group([*M.sheet(64, 66, w=40, h=46, color=p["TERTIARY"])],
                transform=S.rot(5, 64, 66)),
        *M.sheet(60, 56, w=42, h=48, color="#ffffff"),
        *M.sheet_lines(58, 46, 24, p["TERTIARY"], n=3, gap=8),
        *M.cross(92, 78, s=11, color=p["PRIMARY"], weight=8),
    ]


def flashcards(p):
    return [
        M.shadow(rx=26),
        S.group([*M.sheet(60, 66, w=44, h=32, color=p["TERTIARY"])],
                transform=S.rot(-7, 60, 66)),
        S.group([*M.sheet(62, 60, w=46, h=32, color="#ffffff")],
                transform=S.rot(4, 62, 60)),
        # upright front card
        S.rect(46, 34, 36, 44, rx=6, fill=p["TERTIARY"]),
        *M.sheet_lines(64, 48, 20, "#ffffff", n=3, gap=8),
        S.circle(98, 66, 4, fill=p["SECONDARY"]),
    ]


def certificate(p):
    return [
        M.shadow(rx=28),
        S.rect(26, 46, 76, 40, rx=8, fill=p["PRIMARY"]),
        S.rect(32, 52, 64, 28, rx=5, fill=p["HIGHLIGHT"]),
        *M.sheet_lines(58, 60, 30, p["TERTIARY"], n=2, gap=8),
        S.circle(86, 72, 9, fill=p["SECONDARY"]),
        S.polygon([(82, 78), (80, 96), (86, 90), (92, 96), (90, 78)],
                  fill=p["SECONDARY"]),
    ]


def study_review(p):
    return [
        M.shadow(rx=28),
        *M.book_open(64, 68, w=56, h=40, cover=p["PRIMARY"],
                     page=p["TERTIARY"]),
        S.polygon([(76, 44), (88, 44), (88, 92), (82, 84), (76, 92)],
                  fill=p["SECONDARY"], transform=S.rot(6, 82, 66)),
    ]


ICONS = {
    "lesson-complete": lesson_complete,
    "lesson-locked": lesson_locked,
    "wrong-answer": wrong_answer,
    "flashcards": flashcards,
    "certificate": certificate,
    "study-review": study_review,
}
