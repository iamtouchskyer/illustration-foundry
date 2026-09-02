"""assessment group: 5 subjects (mirrors clay assessment/* templates)."""

from __future__ import annotations

from .. import motifs as M
from .. import svg as S


def blank_exam_paper(p):
    return [
        M.shadow(rx=24),
        *M.sheet(64, 56, w=46, h=58, color=p["TERTIARY"], rx=5),
        # pristine blank lines (no digits/text — AVOID list)
        *M.sheet_lines(64, 44, 28, "#ffffff", n=3, gap=9),
        S.circle(64, 74, 8, fill=p["SECONDARY"]),
        M.star(64, 74, r=3.5, color="#ffffff"),
        S.capsule(48, 88, 80, 88, 3.5, p["PRIMARY"]),
    ]


def results_sealed(p):
    return [
        M.shadow(rx=26),
        *M.envelope(64, 60, w=58, h=42, color=p["PRIMARY"],
                    flap=p["HIGHLIGHT"]),
        S.rect(44, 66, 40, 18, rx=4, fill=p["TERTIARY"]),
        S.circle(64, 76, 11, fill=p["SECONDARY"]),
        M.star(64, 76, r=5, color="#ffffff"),
    ]


def proctor_camera(p):
    return [
        M.shadow(rx=26),
        *M.camera(58, 58, color=p["PRIMARY"], lens=p["TERTIARY"]),
        M.shield(98, 78, w=24, h=28, color=p["SECONDARY"]),
    ]


def device_check(p):
    return [
        M.shadow(rx=26),
        *M.laptop(54, 56, color=p["PRIMARY"], screen=p["TERTIARY"]),
        M.shield(94, 72, w=26, h=32, color=p["SECONDARY"]),
        M.check(94, 71, s=5.5, color="#ffffff", weight=4),
    ]


def integrity_shield(p):
    return [
        M.shadow(rx=24),
        S.rect(48, 94, 32, 10, rx=4, fill=p["TERTIARY"]),
        M.shield(64, 52, w=52, h=62, color=p["PRIMARY"]),
        M.shield(64, 54, w=40, h=48, color=p["HIGHLIGHT"]),
        M.check(64, 52, s=10, color=p["SECONDARY"], weight=7),
    ]


ICONS = {
    "blank-exam-paper": blank_exam_paper,
    "results-sealed": results_sealed,
    "proctor-camera": proctor_camera,
    "device-check": device_check,
    "integrity-shield": integrity_shield,
}
