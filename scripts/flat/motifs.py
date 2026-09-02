"""Reusable flat-vector motifs shared across icon groups.

Style lock (see docs/flat-recipe.md): viewBox 0 0 128 128, transparent
background, subject centered in the vertical band ~18..96, one neutral
contact-shadow ellipse at y=104 grounding every subject (inherited from
the clay r8-2 grounded-tray recipe). Palette slots keep clay semantics:
PRIMARY main subject, HIGHLIGHT brighter accent on it, SECONDARY accent
object, TERTIARY pale surfaces/paper. Only palette hexes + white + the
neutral shadow color may appear in output.
"""

from __future__ import annotations

from . import svg as S

SHADOW_COLOR = "#2b2b3a"
SHADOW_OPACITY = 0.08


def shadow(rx: float = 30, cx: float = 64, cy: float = 104) -> S.El:
    return S.ellipse(cx, cy, rx, 5, fill=SHADOW_COLOR, opacity=SHADOW_OPACITY)


# -- paper / documents -----------------------------------------------------

def sheet(cx, cy, w=34, h=42, color=None, rx=4, fold=None):
    """Blank sheet; optional folded top-right corner in `fold` color."""
    els = [S.rect(cx - w / 2, cy - h / 2, w, h, rx=rx, fill=color)]
    if fold:
        f = w * 0.3
        x1, y1 = cx + w / 2 - f, cy - h / 2
        els.append(S.polygon([(x1, y1), (cx + w / 2, y1 + f), (x1, y1 + f)],
                             fill=fold))
    return els


def sheet_lines(cx, cy, w, color, n=2, gap=6, y0=0, weight=2.5):
    els = []
    for i in range(n):
        y = y0 + i * gap
        els.append(S.capsule(cx - w / 2, cy + y, cx + w / 2, cy + y,
                             weight, color))
    return els


def envelope(cx, cy, w=44, h=32, color=None, flap=None):
    flap = flap or color
    body = S.rect(cx - w / 2, cy - h / 2, w, h, rx=5, fill=color)
    tri = S.polygon([(cx - w / 2 + 2, cy - h / 2 + 2),
                     (cx + w / 2 - 2, cy - h / 2 + 2),
                     (cx, cy + 2)], fill=flap)
    return [body, tri]


# -- badges / marks --------------------------------------------------------

def check(cx, cy, s=10, color=None, weight=None):
    w = weight or s * 0.55
    return S.path(f"M{S._n(cx - s)} {S._n(cy)} L{S._n(cx - s * 0.2)} "
                  f"{S._n(cy + s * 0.8)} L{S._n(cx + s)} {S._n(cy - s * 0.7)}",
                  stroke=color, width=w, cap="round", join="round")


def cross(cx, cy, s=9, color=None, weight=None):
    w = weight or s * 0.6
    return [S.line(cx - s, cy - s, cx + s, cy + s, color, w),
            S.line(cx + s, cy - s, cx - s, cy + s, color, w)]


def star(cx, cy, r=10, color=None, r_in=None):
    return S.polygon(S.star_points(cx, cy, r, r_in or r * 0.45), fill=color)


def sparkle(cx, cy, s=6, color=None):
    k = s * 0.22
    pts = [(cx, cy - s), (cx + k, cy - k), (cx + s, cy), (cx + k, cy + k),
           (cx, cy + s), (cx - k, cy + k), (cx - s, cy), (cx - k, cy - k)]
    return S.polygon(pts, fill=color)


def heart(cx, cy, s=10, color=None):
    return S.path(
        f"M{S._n(cx)} {S._n(cy + s * 0.8)} "
        f"C{S._n(cx - s * 0.95)} {S._n(cy + s * 0.15)} "
        f"{S._n(cx - s * 1.05)} {S._n(cy - s * 0.6)} "
        f"{S._n(cx - s * 0.5)} {S._n(cy - s * 0.65)} "
        f"C{S._n(cx - s * 0.15)} {S._n(cy - s * 0.7)} "
        f"{S._n(cx)} {S._n(cy - s * 0.35)} {S._n(cx)} {S._n(cy - s * 0.15)} "
        f"C{S._n(cx)} {S._n(cy - s * 0.35)} "
        f"{S._n(cx + s * 0.15)} {S._n(cy - s * 0.7)} "
        f"{S._n(cx + s * 0.5)} {S._n(cy - s * 0.65)} "
        f"C{S._n(cx + s * 1.05)} {S._n(cy - s * 0.6)} "
        f"{S._n(cx + s * 0.95)} {S._n(cy + s * 0.15)} "
        f"{S._n(cx)} {S._n(cy + s * 0.8)} Z",
        fill=color)


def flame(cx, cy, s=14, color=None, inner=None):
    outer = S.path(
        f"M{S._n(cx)} {S._n(cy - s)} "
        f"C{S._n(cx + s * 0.85)} {S._n(cy - s * 0.15)} "
        f"{S._n(cx + s * 0.7)} {S._n(cy + s * 0.7)} {S._n(cx)} {S._n(cy + s)} "
        f"C{S._n(cx - s * 0.7)} {S._n(cy + s * 0.7)} "
        f"{S._n(cx - s * 0.85)} {S._n(cy - s * 0.15)} "
        f"{S._n(cx)} {S._n(cy - s)} Z", fill=color)
    els = [outer]
    if inner:
        els.append(S.path(
            f"M{S._n(cx)} {S._n(cy - s * 0.3)} "
            f"C{S._n(cx + s * 0.4)} {S._n(cy + s * 0.1)} "
            f"{S._n(cx + s * 0.32)} {S._n(cy + s * 0.55)} "
            f"{S._n(cx)} {S._n(cy + s * 0.68)} "
            f"C{S._n(cx - s * 0.32)} {S._n(cy + s * 0.55)} "
            f"{S._n(cx - s * 0.4)} {S._n(cy + s * 0.1)} "
            f"{S._n(cx)} {S._n(cy - s * 0.3)} Z", fill=inner))
    return els


def leaf(cx, cy, s=10, color=None, tilt=0):
    el = S.path(f"M{S._n(cx)} {S._n(cy - s)} "
                f"Q{S._n(cx + s * 0.9)} {S._n(cy)} {S._n(cx)} {S._n(cy + s)} "
                f"Q{S._n(cx - s * 0.9)} {S._n(cy)} {S._n(cx)} {S._n(cy - s)} Z",
                fill=color)
    if tilt:
        return S.group([el], transform=S.rot(tilt, cx, cy))
    return el


# -- containers ------------------------------------------------------------

def box(cx, cy, w=40, h=26, color=None, flap=None, open_=False):
    els = []
    if open_ and flap:
        els += [S.polygon([(cx - w / 2, cy - h / 2),
                           (cx - w / 2 - 7, cy - h / 2 - 10),
                           (cx - w / 2 + 6, cy - h / 2)], fill=flap),
                S.polygon([(cx + w / 2, cy - h / 2),
                           (cx + w / 2 + 7, cy - h / 2 - 10),
                           (cx + w / 2 - 6, cy - h / 2)], fill=flap)]
    els.append(S.rect(cx - w / 2, cy - h / 2, w, h, rx=5, fill=color))
    return els


def trash_bin(cx, cy, color=None, lid=None, w=30, h=34):
    lid = lid or color
    body = S.polygon([(cx - w / 2 + 2, cy - h / 2 + 6),
                      (cx + w / 2 - 2, cy - h / 2 + 6),
                      (cx + w / 2 - 5, cy + h / 2),
                      (cx - w / 2 + 5, cy + h / 2)], fill=color)
    lip = S.capsule(cx - w / 2 - 2, cy - h / 2 + 4, cx + w / 2 + 2,
                    cy - h / 2 + 4, 6, lid)
    handle = S.capsule(cx - 5, cy - h / 2 - 2, cx + 5, cy - h / 2 - 2, 4, lid)
    return [body, lip, handle]


def folder(cx, cy, w=44, h=32, color=None, tab=None, front=None):
    tab = tab or color
    back = S.rect(cx - w / 2, cy - h / 2, w, h, rx=5, fill=color)
    t = S.path(f"M{S._n(cx - w / 2)} {S._n(cy - h / 2)} "
               f"V{S._n(cy - h / 2 - 7)} Q{S._n(cx - w / 2)} "
               f"{S._n(cy - h / 2 - 11)} {S._n(cx - w / 2 + 4)} "
               f"{S._n(cy - h / 2 - 11)} H{S._n(cx - w / 2 + 16)} "
               f"L{S._n(cx - w / 2 + 22)} {S._n(cy - h / 2)} Z", fill=tab)
    els = [t, back]
    if front:
        els.append(S.rect(cx - w / 2, cy - h / 2 + 9, w, h - 9, rx=5,
                          fill=front))
    return els


def book_open(cx, cy, w=48, h=34, cover=None, page=None):
    pages = []
    for side in (-1, 1):
        pages.append(S.path(
            f"M{S._n(cx)} {S._n(cy - h / 2 + 3)} "
            f"Q{S._n(cx + side * w * 0.28)} {S._n(cy - h / 2 - 2)} "
            f"{S._n(cx + side * w / 2)} {S._n(cy - h / 2 + 4)} "
            f"L{S._n(cx + side * w / 2)} {S._n(cy + h / 2 - 2)} "
            f"Q{S._n(cx + side * w * 0.28)} {S._n(cy + h / 2 - 7)} "
            f"{S._n(cx)} {S._n(cy + h / 2 - 3)} Z", fill=page))
    spine = S.capsule(cx, cy - h / 2 + 3, cx, cy + h / 2 - 3, 2.5, cover)
    base = S.rect(cx - w / 2 - 3, cy - h / 2, w + 6, h + 4, rx=5, fill=cover)
    return [base] + pages + [spine]


def book_closed(cx, cy, w=34, h=42, cover=None, page=None, strap=None):
    els = [S.rect(cx - w / 2, cy - h / 2, w, h, rx=5, fill=cover)]
    if page:
        els.append(S.rect(cx - w / 2 + 5, cy - h / 2 + 4, w - 9, h - 8,
                          rx=3, fill=page))
        els.append(S.capsule(cx - w / 2 + 2.5, cy - h / 2 + 3,
                             cx - w / 2 + 2.5, cy + h / 2 - 3, 2, page))
    if strap:
        els.append(S.rect(cx - w / 2, cy - 3, w, 6, fill=strap))
    return els


# -- devices / interface ---------------------------------------------------

def bell(cx, cy, r=15, color=None, clapper=None):
    dome = S.path(S.arc_d(cx, cy - 2, r, 180, 360)
                  + f" L{S._n(cx + r + 4)} {S._n(cy + 8)} "
                    f"L{S._n(cx - r - 4)} {S._n(cy + 8)} Z", fill=color)
    lip = S.capsule(cx - r - 6, cy + 9, cx + r + 6, cy + 9, 5, color)
    tongue = S.circle(cx, cy + 16, 3.5, fill=clapper or color)
    knob = S.circle(cx, cy - r - 4, 2.5, fill=clapper or color)
    return [knob, dome, lip, tongue]


def clock(cx, cy, r=18, rim=None, face=None, hands=None):
    els = [S.circle(cx, cy, r, fill=rim),
           S.circle(cx, cy, r - 4.5, fill=face)]
    els.append(S.line(cx, cy, cx, cy - r * 0.55, hands, 3.5, cap="round"))
    els.append(S.line(cx, cy, cx + r * 0.45, cy + r * 0.15, hands, 3.5,
                      cap="round"))
    els.append(S.circle(cx, cy, 2.2, fill=hands))
    return els


def cloud(cx, cy, s=1.0, color=None):
    g = [S.circle(cx - 14 * s, cy + 3 * s, 11 * s, fill=color),
         S.circle(cx, cy - 5 * s, 15 * s, fill=color),
         S.circle(cx + 14 * s, cy + 3 * s, 10 * s, fill=color),
         S.rect(cx - 25 * s, cy + 3 * s - 11 * s, 50 * s, 14 * s,
                rx=7 * s, fill=color)]
    return g


def bubble(cx, cy, w=40, h=30, color=None, tail=True, tail_side=-1):
    els = [S.rect(cx - w / 2, cy - h / 2, w, h, rx=h / 3, fill=color)]
    if tail:
        x = cx + tail_side * w * 0.2
        els.append(S.polygon([(x - 6, cy + h / 2 - 2),
                              (x + 6, cy + h / 2 - 2),
                              (x + tail_side * 4, cy + h / 2 + 9)],
                             fill=color))
    return els


def magnifier(cx, cy, r=14, ring=None, glass=None, handle=None):
    els = []
    if glass is not None:
        els.append(S.circle(cx, cy, r - 3, fill=glass))
    els.append(S.circle(cx, cy, r, stroke=ring, width=6))
    hx, hy = S.polar(cx, cy, r + 3, 45)
    els.append(S.capsule(hx, hy, hx + 12, hy + 12, 8, handle or ring))
    return els


def padlock(cx, cy, s=1.0, color=None, keyhole=None):
    shackle = S.path(S.arc_d(cx, cy - 8 * s, 10 * s, 180, 360),
                     stroke=color, width=6 * s)
    body = S.rect(cx - 15 * s, cy - 8 * s, 30 * s, 24 * s, rx=6 * s,
                  fill=color)
    els = [shackle, body]
    if keyhole:
        els.append(S.circle(cx, cy + 1 * s, 3.2 * s, fill=keyhole))
        els.append(S.rect(cx - 1.6 * s, cy + 2 * s, 3.2 * s, 7 * s,
                          rx=1.6 * s, fill=keyhole))
    return els


def key(cx, cy, s=1.0, color=None, rot_deg=-45):
    ring = S.circle(cx - 12 * s, cy, 7.5 * s, stroke=color, width=5.5 * s)
    shaft = S.capsule(cx - 4 * s, cy, cx + 16 * s, cy, 5 * s, color)
    t1 = S.capsule(cx + 9 * s, cy, cx + 9 * s, cy + 6 * s, 4.5 * s, color)
    t2 = S.capsule(cx + 16 * s, cy, cx + 16 * s, cy + 7 * s, 4.5 * s, color)
    return [S.group([ring, shaft, t1, t2],
                    transform=S.rot(rot_deg, cx, cy))]


def shield(cx, cy, w=36, h=44, color=None):
    return S.path(
        f"M{S._n(cx - w / 2)} {S._n(cy - h * 0.34)} "
        f"Q{S._n(cx)} {S._n(cy - h * 0.5)} {S._n(cx + w / 2)} "
        f"{S._n(cy - h * 0.34)} "
        f"L{S._n(cx + w / 2)} {S._n(cy + h * 0.08)} "
        f"Q{S._n(cx + w / 2)} {S._n(cy + h * 0.42)} {S._n(cx)} "
        f"{S._n(cy + h * 0.62)} "
        f"Q{S._n(cx - w / 2)} {S._n(cy + h * 0.42)} {S._n(cx - w / 2)} "
        f"{S._n(cy + h * 0.08)} Z", fill=color)


def gear(cx, cy, r=16, color=None, hole=None, teeth=8):
    els = []
    for i in range(teeth):
        ang = i * 360 / teeth
        x1, y1 = S.polar(cx, cy, r - 2, ang)
        x2, y2 = S.polar(cx, cy, r + 6, ang)
        els.append(S.capsule(x1, y1, x2, y2, 9, color))
    els.append(S.circle(cx, cy, r, fill=color))
    if hole:
        els.append(S.circle(cx, cy, r * 0.42, fill=hole))
    return els


def person(cx, cy, s=1.0, color=None):
    return [S.circle(cx, cy - 7 * s, 6.5 * s, fill=color),
            S.path(f"M{S._n(cx - 9 * s)} {S._n(cy + 11 * s)} "
                   f"C{S._n(cx - 9 * s)} {S._n(cy - 1 * s)} "
                   f"{S._n(cx + 9 * s)} {S._n(cy - 1 * s)} "
                   f"{S._n(cx + 9 * s)} {S._n(cy + 11 * s)} Z", fill=color)]


def target(cx, cy, r=20, outer=None, mid=None, inner=None):
    els = [S.circle(cx, cy, r, fill=outer)]
    if mid:
        els.append(S.circle(cx, cy, r * 0.66, fill=mid))
    if inner:
        els.append(S.circle(cx, cy, r * 0.33, fill=inner))
    return els


def flag(cx, cy, pole_h=44, color=None, pole=None):
    pole = pole or color
    p = S.capsule(cx, cy - pole_h / 2, cx, cy + pole_h / 2, 4, pole)
    banner = S.polygon([(cx + 2, cy - pole_h / 2 + 2),
                        (cx + 26, cy - pole_h / 2 + 9),
                        (cx + 2, cy - pole_h / 2 + 16)], fill=color)
    return [p, banner]


def trophy(cx, cy, s=1.0, color=None, accent=None):
    cup = S.path(f"M{S._n(cx - 11 * s)} {S._n(cy - 14 * s)} "
                 f"H{S._n(cx + 11 * s)} V{S._n(cy - 4 * s)} "
                 f"Q{S._n(cx + 11 * s)} {S._n(cy + 6 * s)} {S._n(cx)} "
                 f"{S._n(cy + 6 * s)} "
                 f"Q{S._n(cx - 11 * s)} {S._n(cy + 6 * s)} "
                 f"{S._n(cx - 11 * s)} {S._n(cy - 4 * s)} Z", fill=color)
    stem = S.rect(cx - 3 * s, cy + 5 * s, 6 * s, 7 * s, fill=color)
    base = S.capsule(cx - 9 * s, cy + 14 * s, cx + 9 * s, cy + 14 * s,
                     5 * s, accent or color)
    h1 = S.path(S.arc_d(cx - 13 * s, cy - 8 * s, 6 * s, 90, 270),
                stroke=color, width=3.5 * s)
    h2 = S.path(S.arc_d(cx + 13 * s, cy - 8 * s, 6 * s, 270, 90),
                stroke=color, width=3.5 * s)
    return [h1, h2, cup, stem, base]


def medal(cx, cy, r=13, color=None, ribbon=None, emblem=None):
    els = []
    if ribbon:
        els.append(S.polygon([(cx - 8, cy - r - 2), (cx - 2, cy - r - 2),
                              (cx - 8, cy - r - 16), (cx - 14, cy - r - 16)],
                             fill=ribbon))
        els.append(S.polygon([(cx + 2, cy - r - 2), (cx + 8, cy - r - 2),
                              (cx + 14, cy - r - 16), (cx + 8, cy - r - 16)],
                             fill=ribbon))
    els.append(S.circle(cx, cy, r, fill=color))
    if emblem:
        els.append(star(cx, cy, r * 0.52, color=emblem))
    return els


def coin(cx, cy, r=9, color=None, inner=None):
    els = [S.circle(cx, cy, r, fill=color)]
    if inner:
        els.append(S.circle(cx, cy, r * 0.62, fill=inner))
    return els


def gem(cx, cy, s=1.0, color=None, facet=None):
    pts = [(cx - 14 * s, cy - 5 * s), (cx - 7 * s, cy - 12 * s),
           (cx + 7 * s, cy - 12 * s), (cx + 14 * s, cy - 5 * s),
           (cx, cy + 12 * s)]
    els = [S.polygon(pts, fill=color)]
    if facet:
        els.append(S.polygon([(cx - 14 * s, cy - 5 * s),
                              (cx + 14 * s, cy - 5 * s), (cx, cy + 12 * s)],
                             fill=facet, opacity=0.55))
    return els


def crown(cx, cy, s=1.0, color=None, gem_color=None):
    pts = [(cx - 19 * s, cy + 11 * s), (cx - 19 * s, cy - 7 * s),
           (cx - 9 * s, cy + 1 * s), (cx, cy - 12 * s),
           (cx + 9 * s, cy + 1 * s), (cx + 19 * s, cy - 7 * s),
           (cx + 19 * s, cy + 11 * s)]
    els = [S.polygon(pts, fill=color)]
    if gem_color:
        els.append(S.circle(cx, cy + 2 * s, 3.4 * s, fill=gem_color))
    return els


def capsule_bar(cx, cy, w, h, track=None, fill_color=None, ratio=1.0,
                knob=None):
    els = [S.rect(cx - w / 2, cy - h / 2, w, h, rx=h / 2, fill=track)]
    fw = max(h, w * ratio)
    els.append(S.rect(cx - w / 2, cy - h / 2, fw, h, rx=h / 2,
                      fill=fill_color))
    if knob:
        els.append(S.circle(cx - w / 2 + fw, cy, h * 0.85, fill=knob))
    return els


def steps(cx, cy, n=3, w=12, h_step=8, color=None):
    els = []
    total = n * w
    for i in range(n):
        h = (i + 1) * h_step
        x = cx - total / 2 + i * w
        els.append(S.rect(x + 1, cy + 14 - h, w - 2, h, rx=3, fill=color))
    return els


def arrow_loop(cx, cy, r=17, color=None, head=None, gap=70):
    head = head or color
    a0, a1 = -90 + gap / 2, -90 + 360 - gap / 2
    arc = S.path(S.arc_d(cx, cy, r, a0, a1), stroke=color, width=7)
    hx, hy = S.polar(cx, cy, r, a1)
    tri = S.polygon([(hx + 9, hy - 7), (hx + 11, hy + 8), (hx - 7, hy + 1)],
                    fill=head)
    return [arc, tri]


def hourglass(cx, cy, s=1.0, frame=None, glass=None, sand=None):
    top = S.capsule(cx - 13 * s, cy - 18 * s, cx + 13 * s, cy - 18 * s,
                    5 * s, frame)
    bot = S.capsule(cx - 13 * s, cy + 18 * s, cx + 13 * s, cy + 18 * s,
                    5 * s, frame)
    g1 = S.polygon([(cx - 9 * s, cy - 15 * s), (cx + 9 * s, cy - 15 * s),
                    (cx, cy)], fill=glass)
    g2 = S.polygon([(cx - 9 * s, cy + 15 * s), (cx + 9 * s, cy + 15 * s),
                    (cx, cy)], fill=glass)
    els = [g1, g2]
    if sand:
        els.append(S.polygon([(cx - 6 * s, cy + 15 * s),
                              (cx + 6 * s, cy + 15 * s), (cx, cy + 5 * s)],
                             fill=sand))
    els += [top, bot]
    return els


def moon(cx, cy, r=12, color=None):
    return S.path(f"M{S._n(cx + r * 0.35)} {S._n(cy - r)} "
                  f"A{S._n(r)} {S._n(r)} 0 1 0 {S._n(cx + r * 0.35)} "
                  f"{S._n(cy + r)} "
                  f"A{S._n(r * 0.78)} {S._n(r * 0.78)} 0 1 1 "
                  f"{S._n(cx + r * 0.35)} {S._n(cy - r)} Z", fill=color)


def ticket(cx, cy, w=46, h=26, color=None, perf=None, tear_gap=0,
           stub_tilt=0):
    if tear_gap:
        half = (w - tear_gap) / 2
        left = S.rect(cx - w / 2, cy - h / 2, half, h, rx=5, fill=color)
        right = S.rect(cx - w / 2 + half + tear_gap, cy - h / 2, half, h,
                       rx=5, fill=color)
        if stub_tilt:
            right = S.group([right], transform=S.rot(stub_tilt,
                            cx + w / 4, cy))
        return [left, right]
    els = [S.rect(cx - w / 2, cy - h / 2, w, h, rx=5, fill=color)]
    if perf:
        for i in range(4):
            y = cy - h / 2 + 4 + i * (h - 8) / 3
            els.append(S.circle(cx, y, 1.6, fill=perf))
    return els


def card(cx, cy, w=42, h=28, color=None, stripe=None):
    els = [S.rect(cx - w / 2, cy - h / 2, w, h, rx=6, fill=color)]
    if stripe:
        els.append(S.rect(cx - w / 2, cy - h / 2 + 6, w, 5, fill=stripe))
    return els


def ring_progress(cx, cy, r=20, color=None, track=None, span=270,
                  spark=None):
    els = []
    if track:
        els.append(S.circle(cx, cy, r, stroke=track, width=8))
    els.append(S.path(S.arc_d(cx, cy, r, -90, -90 + span), stroke=color,
                      width=8))
    if spark:
        sx, sy = S.polar(cx, cy, r, -90 + span)
        els.append(S.circle(sx, sy, 5.5, fill=spark))
    return els


def camera(cx, cy, color=None, lens=None):
    body = S.rect(cx - 22, cy - 13, 44, 30, rx=7, fill=color)
    bump = S.rect(cx - 8, cy - 19, 16, 8, rx=3, fill=color)
    lens_o = S.circle(cx, cy + 2, 10, fill=lens)
    lens_i = S.circle(cx + 3, cy - 1, 2.4, fill="#ffffff", opacity=0.85)
    return [bump, body, lens_o, lens_i]


def laptop(cx, cy, color=None, screen=None):
    lid = S.rect(cx - 19, cy - 18, 38, 26, rx=4, fill=color)
    inner = S.rect(cx - 15, cy - 14, 30, 18, rx=2, fill=screen)
    base = S.polygon([(cx - 26, cy + 14), (cx + 26, cy + 14),
                      (cx + 21, cy + 8), (cx - 21, cy + 8)], fill=color)
    return [lid, inner, base]
