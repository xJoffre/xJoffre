import base64
import random
import textwrap
from pathlib import Path

FONTS = Path(__file__).resolve().parent / "fonts"
FONT = "font-family:'Receipt Mono','Courier New',monospace"
WIDTH, LEFT, RIGHT = 520, 34, 486
SIZES = {"title": 24, "body": 15, "small": 14, "note": 13, "total": 18, "caption": 13, "thesis": 18, "legend": 12, "month": 10}
THEMES = {
    "light": {"paper": "#FFFFFF", "ink": "#1A1A1A", "note": "#666666", "edge": "none", "shadow": ".18", "text": "#222222", "muted": "#6B6B6B"},
    "dark": {"paper": "#1C2128", "ink": "#E6EDF3", "note": "#8B949E", "edge": "#30363D", "shadow": "0", "text": "#E6EDF3", "muted": "#9198A1"},
}


def encode(path):
    return base64.b64encode(path.read_bytes()).decode()


FONT_FACE = "".join(
    f"@font-face{{font-family:'Receipt Mono';font-weight:{weight};"
    f"src:url(data:font/woff2;base64,{encode(FONTS / f'ibm-plex-mono-{weight}.woff2')}) format('woff2')}}"
    for weight in (400, 700)
)


def wrapped(x, y, text, width, leading):
    return "".join(f'<tspan x="{x}" y="{y + i * leading}">{row}</tspan>' for i, row in enumerate(textwrap.wrap(text, width)))


def svg(width, height, label, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
            f'role="img" aria-label="{label}"><style>{FONT_FACE}</style>{body}</svg>')


class Receipt:
    def __init__(self, colors):
        self.colors = colors
        self.rows = []
        self.y = 70

    def _text(self, x, text, size, weight, color=None, anchor="start"):
        return (f'<text x="{x}" y="{self.y}" text-anchor="{anchor}" style="{FONT};font-size:{size}px;font-weight:{weight}" '
                f'fill="{color or self.colors["ink"]}">{text}</text>')

    def center(self, text, size=SIZES["body"], weight=400, gap=24):
        self.rows.append(self._text(WIDTH / 2, text, size, weight, anchor="middle"))
        self.y += gap

    def pair(self, left, right="", size=SIZES["body"], weight=400):
        self.rows.append(self._text(LEFT, left, size, weight) + self._text(RIGHT, right, size, weight, anchor="end"))
        self.y += 24

    def note(self, text, width=52, leading=17):
        rows = textwrap.wrap(text, width)
        self.rows.append(f'<text style="{FONT};font-size:{SIZES["note"]}px" fill="{self.colors["note"]}">{wrapped(LEFT + 18, self.y - 4, text, width, leading)}</text>')
        self.y += leading * len(rows)

    def draw(self, markup, height):
        self.rows.append(markup)
        self.y += height

    def rule(self):
        self.rows.append(f'<line x1="{LEFT}" y1="{self.y - 8}" x2="{RIGHT}" y2="{self.y - 8}" stroke="{self.colors["ink"]}" stroke-dasharray="5 4"/>')
        self.y += 18

    def barcode(self, seed, height=54):
        rnd, x, bars = random.Random(seed), 130.0, ""
        while x < 390:
            width = rnd.choice((1.5, 2, 3, 4))
            bars += f'<rect x="{x:.1f}" y="{self.y}" width="{width}" height="{height}" fill="{self.colors["ink"]}"/>'
            x += width + rnd.choice((1.5, 2, 3))
        self.rows.append(bars)
        self.y += height + 20

    def render(self, label):
        height = self.y + 10
        top = [(i * 10, 10 - (8 if i % 2 else 0)) for i in range(WIDTH // 10 + 1)]
        bottom = [(WIDTH - i * 10, height + (8 if i % 2 else 0)) for i in range(WIDTH // 10 + 1)]
        outline = " ".join(f"{x},{y}" for x, y in top + bottom)
        colors = self.colors
        body = (f'<defs><clipPath id="print"><rect x="0" y="0" width="{WIDTH}" height="0">'
                f'<animate attributeName="height" from="0" to="{height + 20}" dur="2.4s" begin=".2s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".3 0 .7 1"/></rect></clipPath>'
                f'<filter id="shadow"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-opacity="{colors["shadow"]}"/></filter></defs>'
                f'<g clip-path="url(#print)"><polygon points="{outline}" fill="{colors["paper"]}" stroke="{colors["edge"]}" filter="url(#shadow)"/>{"".join(self.rows)}</g>')
        return svg(WIDTH, height + 20, label, body)
