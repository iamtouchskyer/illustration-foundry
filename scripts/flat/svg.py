"""Minimal SVG element builders for the flat icon library.

Everything is a plain dataclass tree rendered to a string at the end —
no XML library, no dependencies. Coordinates live in a 128x128 viewBox;
the shipped file scales to 512 (parity with the clay PNG ship size).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


def _n(v: float) -> str:
    """Compact number formatting: no trailing zeros, no negative zero."""
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "-0.0", "") else s


@dataclass
class El:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def render(self, indent: int = 0) -> str:
        pad = "  " * indent
        parts = []
        for k, v in self.attrs.items():
            if v is None:
                continue
            parts.append(f'{k}="{_n(v) if isinstance(v, (int, float)) else v}"')
        head = f"{pad}<{self.tag} " + " ".join(parts)
        if not self.children:
            return head + "/>"
        body = "\n".join(c.render(indent + 1) for c in self.children)
        return f"{head}>\n{body}\n{pad}</{self.tag}>"


def _common(fill=None, opacity=None, stroke=None, width=None,
            cap=None, join=None, transform=None, rule=None):
    a = {}
    if fill is not None:
        a["fill"] = fill
    if opacity is not None:
        a["opacity"] = opacity
    if stroke is not None:
        a["stroke"] = stroke
        a["fill"] = a.get("fill", "none")
    if width is not None:
        a["stroke-width"] = width
    if cap is not None:
        a["stroke-linecap"] = cap
    if join is not None:
        a["stroke-linejoin"] = join
    if transform is not None:
        a["transform"] = transform
    if rule is not None:
        a["fill-rule"] = rule
    return a


def circle(cx, cy, r, fill=None, **kw) -> El:
    return El("circle", {"cx": cx, "cy": cy, "r": r} | _common(fill=fill, **kw))


def ellipse(cx, cy, rx, ry, fill=None, **kw) -> El:
    return El("ellipse", {"cx": cx, "cy": cy, "rx": rx, "ry": ry}
              | _common(fill=fill, **kw))


def rect(x, y, w, h, rx=0, fill=None, **kw) -> El:
    a = {"x": x, "y": y, "width": w, "height": h}
    if rx:
        a["rx"] = rx
    return El("rect", a | _common(fill=fill, **kw))


def path(d, fill=None, **kw) -> El:
    return El("path", {"d": d} | _common(fill=fill, **kw))


def polygon(points, fill=None, **kw) -> El:
    pts = " ".join(f"{_n(x)},{_n(y)}" for x, y in points)
    return El("polygon", {"points": pts} | _common(fill=fill, **kw))


def line(x1, y1, x2, y2, stroke, width, cap="round", **kw) -> El:
    return El("line", {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
              | _common(stroke=stroke, width=width, cap=cap, **kw))


def group(children, transform=None) -> El:
    a = {"transform": transform} if transform else {}
    return El("g", a, list(children))


# -- transform snippets ---------------------------------------------------

def tr(x, y) -> str:
    return f"translate({_n(x)} {_n(y)})"


def rot(deg, cx=0, cy=0) -> str:
    return f"rotate({_n(deg)} {_n(cx)} {_n(cy)})"


def scl(s, cx=0, cy=0) -> str:
    return f"scale({_n(s)})" if (cx == 0 and cy == 0) else \
        f"translate({_n(cx)} {_n(cy)}) scale({_n(s)}) translate({_n(-cx)} {_n(-cy)})"


# -- geometry helpers -----------------------------------------------------

def polar(cx, cy, r, deg):
    rad = math.radians(deg)
    return cx + r * math.cos(rad), cy + r * math.sin(rad)


def star_points(cx, cy, r_out, r_in, n=5, rot_deg=-90):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        pts.append(polar(cx, cy, r, rot_deg + i * 180 / n))
    return pts


def arc_d(cx, cy, r, a0, a1) -> str:
    """Open arc path from angle a0 to a1 (degrees, y-down screen space)."""
    x0, y0 = polar(cx, cy, r, a0)
    x1, y1 = polar(cx, cy, r, a1)
    sweep = 1 if (a1 - a0) % 360 > 0 else 0
    large = 1 if abs((a1 - a0) % 360) > 180 else 0
    return f"M{_n(x0)} {_n(y0)} A{_n(r)} {_n(r)} 0 {large} {sweep} {_n(x1)} {_n(y1)}"


def capsule(x1, y1, x2, y2, w, fill) -> El:
    """Rounded bar between two points (stroked line with round caps)."""
    return line(x1, y1, x2, y2, stroke=fill, width=w)


def svg_doc(children, ship_size: int = 512) -> str:
    body = "\n".join(c.render(1) for c in children)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{ship_size}" height="{ship_size}" '
        'viewBox="0 0 128 128">\n'
        f"{body}\n</svg>\n"
    )
