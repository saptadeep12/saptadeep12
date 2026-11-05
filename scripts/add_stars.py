import random
import re
import sys

path = sys.argv[1]
svg = open(path, encoding="utf-8").read()

m = re.search(r'viewBox="0\s+0\s+([\d.]+)\s+([\d.]+)"', svg)
if m:
    w, h = float(m.group(1)), float(m.group(2))
else:
    w = float(re.search(r'width="([\d.]+)"', svg).group(1))
    h = float(re.search(r'height="([\d.]+)"', svg).group(1))

random.seed(7)
stars = []
for _ in range(70):
    x, y = random.uniform(0, w), random.uniform(0, h)
    r = random.choice([0.8, 1, 1.2, 1.6])
    color = random.choice(["#ffffff", "#ffd6da", "#ff9aa5"])
    dur = random.uniform(2, 5)
    begin = random.uniform(0, 4)
    stars.append(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" opacity="0.8">'
        f'<animate attributeName="opacity" values="0.15;1;0.15" '
        f'dur="{dur:.1f}s" begin="-{begin:.1f}s" repeatCount="indefinite"/></circle>'
    )
layer = '<g id="stars">' + "".join(stars) + "</g>"

if 'id="stars"' not in svg:
    rect = re.search(r"<rect\b[^>]*>", svg)
    if rect:
        end = rect.end()
        if not rect.group(0).endswith("/>"):
            close = svg.find("</rect>", end)
            if close != -1:
                end = close + len("</rect>")
        svg = svg[:end] + layer + svg[end:]
    else:
        svg = re.sub(r"(<svg\b[^>]*>)", lambda mo: mo.group(1) + layer, svg, count=1)

open(path, "w", encoding="utf-8").write(svg)