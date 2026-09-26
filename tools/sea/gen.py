"""Builds c-shells-header.html from template4.html.

One wave model drives everything: the tiled sea layers, the crest foam and
the break against the pier are all computed from the same function per
frame, so they can't drift out of step with each other.

Cycle (phi 0..1, peak at 0.5):
  trough  low, rounded, barely moving, no foam
  build   rises, sharpens, accelerates; a foam cap forms at the tip and widens
  peak    front crest reaches the pier face and surges up it, throwing spray
  fall    foam slides down the back of each wave and thins out; backwash
          slides off the wall on the real surface
"""
import math, random

W = 48          # tile width (art px)
HF = 16         # layer frame height
N = 48          # frames per cycle
CYCLE = 7.0     # seconds
SHEET = 997     # front sheet width; right-anchored at the pier face
XW = (SHEET - 1) % W   # tile column that sits against the wall (36)
SW, SH = 24, 36        # shore overlay: columns left of the wall, frame height
LIFT = SH - HF         # overlay extends this far above the front window

def smooth(phi):
    return ((1 - math.cos(2 * math.pi * phi)) / 2) ** 1.6

def drift(phi, p):
    k = 0.75
    return p["drift"] * (phi - k * math.sin(2 * math.pi * phi) / (2 * math.pi))

def column(x, phi, p):
    """Height and signed distance to nearest crest (px, + = ahead) at tile x."""
    s = smooth(phi)
    d = drift(phi, p)
    amp = p["amin"] + (p["amax"] - p["amin"]) * s
    sharp = 1.2 + 2.3 * s
    level = p["base"] + p["rise"] * s
    th = 2 * math.pi * p["f"] * (x - d) / W
    crest = ((1 + math.sin(th)) / 2) ** sharp
    ripple = math.sin(2 * math.pi * p["f2"] * (x - d * 0.6) / W + 1.3)
    h = level + amp * crest + p["r"] * ripple
    u = ((th - math.pi / 2) / (2 * math.pi)) % 1
    delta = u if u < 0.5 else u - 1
    dist = delta * W / p["f"]
    return h, dist, level, (x - d)   # last: position in the water's own frame

def hashv(a, b):
    return ((int(a) * 73856093) ^ (int(b) * 19349663)) % 1000 / 1000

def foam_at(dist, phi, s, water_x):
    """0 none, 1 surface foam, 2 surface + cap pixel above. Continuous in phi."""
    if phi <= 0.5:
        if s < 0.12:
            return 0
        capw = 0.3 + 3.2 * s
        if abs(dist) > capw:
            return 0
        return 2 if (s > 0.55 and abs(dist) < capw * 0.45) else 1
    # Falling: the cap stays on the crest briefly, then foam is left behind
    # on the back of the wave and thins, textured in the water's own frame so
    # it travels with the wave rather than twinkling.
    fall = (phi - 0.5) / 0.45                   # 0 at peak, 1 near trough
    if fall >= 1:
        return 0
    front = 3.2 * (1 - fall)                     # cap retreats
    back = -(3 + 14 * fall)                      # trail lengthens behind
    if not (back <= dist <= front):
        return 0
    density = (1 - fall) ** 1.3 * (1 - 0.5 * abs(dist) / (abs(back) + 1))
    if hashv(round(water_x) % W, 7) > density:
        return 0
    return 2 if (fall < 0.25 and abs(dist) < 1.5) else 1

def draw_columns(heights, foams, y_top_of, bottom):
    """Rect runs for light row, water and foam."""
    light, water, foam = [], [], []
    for c, (h, f) in enumerate(zip(heights, foams)):
        top = bottom - h
        light.append(f"M{c} {top}h1v1h-1z")
        water.append(f"M{c} {top + 1}h1v{h - 1}h-1z")
        if f:
            foam.append(f"M{c} {top}h1v1h-1z")
        if f == 2:
            foam.append(f"M{c} {top - 1}h1v1h-1z")
    return light, water, foam

def stair(tops, x0, bottom):
    out = [f"M{x0} {bottom}V{tops[0]}"]
    cur = tops[0]
    for i in range(1, len(tops)):
        if tops[i] != cur:
            out.append(f"H{x0 + i}V{tops[i]}")
            cur = tops[i]
    out.append(f"H{x0 + len(tops)}V{bottom}Z")
    return "".join(out)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def layer(name, p):
    light, water, foam = [], [], []
    for i in range(N):
        phi = i / N
        s = smooth(phi)
        bottom = (i + 1) * HF
        hs, fs = [], []
        for x in range(W):
            h, dist, _, wx = column(x, phi, p)
            hs.append(clamp(int(round(h)), 2, HF - 2))
            fs.append(foam_at(dist, phi, s, wx))
        tops = [bottom - h for h in hs]
        light.append(stair(tops, 0, bottom))
        water.append(stair([t + 1 for t in tops], 0, bottom))
        for x, f in enumerate(fs):
            if f:
                foam.append(f"M{x} {tops[x]}h1v1h-1z")
            if f == 2:
                foam.append(f"M{x} {tops[x] - 1}h1v1h-1z")
    total = N * HF
    return f'''<svg viewBox="0 0 {{VBW}} {total}" preserveAspectRatio="none" shape-rendering="crispEdges">
            <defs>
              <pattern id="tile-{name}" width="{W}" height="{total}" patternUnits="userSpaceOnUse" x="{{PX0}}">
                <path style="fill:var(--{name}-light)" d="{''.join(light)}"/>
                <path style="fill:var(--{name})" d="{''.join(water)}"/>
                <path style="fill:var(--foam)" d="{''.join(foam)}"/>
              </pattern>
            </defs>
            <rect width="{{VBW}}" height="{total}" fill="url(#tile-{name})"/>
          </svg>'''

def shore(p):
    """Front layer's last SW columns before the wall, redrawn with shoaling,
    surge, spray and backwash. At its left edge it equals the tiled sea
    exactly, so it blends in without a seam."""
    rnd = random.Random(7)
    impact = N // 2 - 1            # crest reaches the wall at phi = 0.5
    parts = [(rnd.randint(0, 3), -rnd.uniform(0.2, 1.1), rnd.uniform(1.5, 3.2)) for _ in range(16)]
    light, water, foam = [], [], []
    for i in range(N):
        phi = i / N
        s = smooth(phi)
        bottom = (i + 1) * SH
        t = (i - impact) / 12.0
        surge = 12 * math.sin(math.pi * t) ** 0.8 if 0 <= t <= 1 else 0
        bt = (i - impact - 8) / 18.0
        hs, fs = [], []
        for c in range(SW):
            x = (XW - (SW - 1) + c) % W
            h, dist, level, wx = column(x, phi, p)
            b = (c / (SW - 1)) ** 2
            h += b * 0.6 * max(0, h - level)                  # shoaling
            wall = math.exp(-(SW - 1 - c) / (3.5 + 4 * max(t, 0)))
            h += surge * wall
            f = foam_at(dist, phi, s, wx)
            if surge * wall > 1.5:
                f = 2 if surge * wall > 5 else max(f, 1)
            if 0 <= bt <= 1 and c >= SW - 1 - (4 + 18 * bt):
                if hashv(c + int(bt * 20), i) < (1 - bt) * 0.9:
                    f = max(f, 1)
            hs.append(clamp(int(round(h)), 2, SH - 2))
            fs.append(f)
        tops = [bottom - h for h in hs]
        light.append(stair(tops, 0, bottom))
        water.append(stair([t_ + 1 for t_ in tops], 0, bottom))
        for c, f in enumerate(fs):
            if f:
                foam.append(f"M{c} {tops[c]}h1v1h-1z")
            if f == 2:
                foam.append(f"M{c} {tops[c] - 1}h1v1h-1z")
        # Spray: launched from the top of the surge, arcing back over the sea
        wall_top = hs[-1]
        for lo, vx, vy in parts:
            ft = i - impact - 2 - lo
            if ft < 0:
                continue
            x = SW - 1 + vx * ft
            y = 13 + vy * ft - 0.22 * ft * ft
            if x < 0 or y < 4 or y <= (hs[int(x)] if 0 <= int(x) < SW else 0):
                continue
            foam.append(f"M{int(x)} {bottom - int(y)}h1v1h-1z")
    total = N * SH
    return f'''<svg viewBox="0 0 {SW} {total}" shape-rendering="crispEdges">
            <path style="fill:var(--front-light)" d="{''.join(light)}"/>
            <path style="fill:var(--front)" d="{''.join(water)}"/>
            <path style="fill:var(--foam)" d="{''.join(foam)}"/>
          </svg>'''

params = {
    "back":  dict(f=3, f2=6, drift=16, amin=1.0, amax=3.0, base=4.0, rise=1.0, r=0.4),
    "mid":   dict(f=2, f2=4, drift=24, amin=1.5, amax=4.5, base=4.0, rise=1.5, r=0.5),
    "front": dict(f=1, f2=3, drift=48, amin=2.0, amax=5.5, base=3.5, rise=2.0, r=0.8),
}

# ---------- Title loop: a terminal edit, c -> sea -> c ----------
LOOP = 14.0
events = [
    (0.0,   1, 0, 0, 1),
    (3.0,   1, 0, 1, 0),
    (3.6,   0, 0, 1, 0),
    (4.0,   0, 1, 1, 0),
    (4.2,   1, 1, 1, 0),
    (4.38,  2, 1, 1, 0),
    (4.56,  3, 1, 1, 0),
    (5.2,   3, 1, 0, 1),
    (10.0,  3, 1, 1, 0),
    (10.5,  2, 1, 1, 0),
    (10.62, 1, 1, 1, 0),
    (10.74, 0, 1, 1, 0),
    (11.1,  0, 0, 1, 0),
    (11.3,  1, 0, 1, 0),
    (11.9,  1, 0, 0, 1),
]

def kf(name, idx, fmt):
    lines, last = [], None
    for ev in events:
        v = ev[idx]
        if v != last:
            lines.append(f"    {ev[0] / LOOP * 100:.2f}% {{ {fmt(v)} }}")
            last = v
    lines.append(f"    100% {{ {fmt(events[0][idx])} }}")
    return f"  @keyframes {name} {{\n" + "\n".join(lines) + "\n  }"

title_kf = "\n".join([
    kf("edit-width", 1, lambda v: f"width: {v}ch;"),
    kf("edit-row", 2, lambda v: f"transform: translateY({-1.2 * v:g}em);"),
    kf("edit-cursor", 3, lambda v: f"visibility: {'visible' if v else 'hidden'};"),
    kf("end-cursor", 4, lambda v: f"visibility: {'visible' if v else 'hidden'};"),
])

if __name__ == "__main__":
    import sys
    tpl = sys.argv[1] if len(sys.argv) > 1 else "template4.html"
    out = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/c-shells-header.html"
    html = open(tpl).read()
    html = html.replace("/*{{title_kf}}*/", title_kf)
    html = html.replace("{{shore}}", shore(params["front"]))
    for n, p in params.items():
        svg = layer(n, p)
        vbw = SHEET if n == "front" else 1000
        svg = svg.replace("{VBW}", str(vbw)).replace("{PX0}", "0")
        html = html.replace("{{" + n + "}}", svg)
    for k, v in dict(N=N, HF=HF, CYCLE=CYCLE, LOOP=LOOP, SW=SW, SH=SH, LIFT=LIFT, SHEET=SHEET).items():
        html = html.replace("{{" + k + "}}", f"{v:g}")
    open(out, "w").write(html)
    print("bytes", len(html), "wall column", XW)
