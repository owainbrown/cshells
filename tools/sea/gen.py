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
import math
import re, random

W = 48          # tile width (art px)
HF = 16         # layer frame height
N = 48          # frames per cycle
CYCLE = 7.0     # seconds
SHEET = 997     # front sheet width; right-anchored at the pier face
XW = (SHEET - 1) % W   # tile column that sits against the wall (36)
SW_L, SW_R = 24, 26    # shore overlay: columns left of the wall, columns over the pier
SW = SW_L + SW_R
SH = 40                # shore frame height, bottom aligned with the front window
LIFT = SH - HF         # overlay extends this far above the front window
PIER_H = 11            # pier top, in rows above the front window's bottom
SURGE = 17             # how far the break climbs the wall at its peak

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
    """The break against the pier, drawn over the front layer, the wall and
    the lighthouse.

    Columns 0..SW_L-1 are the last stretch of sea before the wall: at the
    left edge they equal the tiled sea exactly, so there's no seam. Columns
    SW_L.. sit over the pier. Per cycle:
      build     the crest shoals and steepens into the wall
      impact    it piles up the face and bursts into a white plume that
                climbs past the lighthouse
      overtop   green water spills over the coping and runs across the pier,
                and the plume rains down onto it
      runback   the pier drains back towards the edge and pours off the wall
                into the sea, leaving foam on the backwash
    Everything is simulated frame by frame from the impact and has drained
    before the cycle wraps, so the loop has no seam.
    """
    rnd = random.Random(11)
    impact = N // 2 - 1            # crest reaches the wall at phi = 0.5
    G = 1.05                       # gravity, rows per frame squared
    TOP = SH - 1

    # Plume particles: launch frame offset, x velocity (+ is over the pier),
    # y velocity (up). Most go up and inland; a few fall back seaward.
    parts = []
    for _ in range(145):
        lo = min(int(rnd.expovariate(0.55)), 6)
        vy = rnd.uniform(2.4, 7.75) * (1 - 0.08 * lo)   # apex about 29 rows
        vx = rnd.gauss(0.87, 0.46)
        x0 = SW_L - 1 + rnd.uniform(-1.5, 1.0)
        parts.append((lo, x0, vx, vy))

    # Pre-simulate the plume and the water on the pier, frame by frame.
    plume = {}                     # frame -> list of (x, y, streak)
    sheet = {}                     # frame -> list of depths per pier column
    pour = {}                      # frame -> amount pouring off the edge
    depth = [0.0] * SW_R
    for k in range(0, N - impact):
        i = impact + k
        pts = []
        for lo, x0, vx, vy in parts:
            ft = k - lo
            if ft < 0:
                continue
            # Integrate analytically to the landing point, if any.
            land = None
            for f in range(ft + 1):
                x = x0 + vx * f
                y = PIER_H + 1 + vy * f - 0.5 * G * f * f
                ground = PIER_H if x >= SW_L else PIER_H - 5
                if f > 0 and y <= ground:
                    land = (f, x)
                    break
            if land:
                f, x = land
                if f == ft and x >= SW_L:
                    c = int(x) - SW_L
                    if c < SW_R:
                        depth[c] += 0.12
                continue
            x = x0 + vx * ft
            y = PIER_H + 1 + vy * ft - 0.5 * G * ft * ft
            speed_up = vy - G * ft
            pts.append((x, y, speed_up > 2.5))
        plume[i] = pts

        # Green water over the coping, early in the impact.
        if 1 <= k <= 5:
            spill = [4.0, 5.0, 4.5, 3.5, 2.0][k - 1]
            reach = 4 + 5 * k
            for c in range(min(reach, SW_R)):
                depth[c] = max(depth[c], spill * (1 - c / reach) ** 0.6)
        # Momentum carries the first rush inland; after that the pier drains
        # back to the edge, which pours into the sea.
        new = depth[:]
        if k <= 6:
            for c in range(SW_R - 1, 0, -1):
                m = new[c - 1] * 0.25
                new[c - 1] -= m
                new[c] += m
        else:
            for c in range(SW_R):
                m = new[c] * 0.4
                new[c] -= m
                if c > 0:
                    new[c - 1] += m
                else:
                    pour[i] = pour.get(i, 0) + m
        decay = 0.93 if k <= 6 else 0.84
        depth = [d * decay if d > 0.1 else 0.0 for d in new]
        sheet[i] = depth[:]

    light, water, foam = [], [], []

    def px(c, y, bottom, lst=foam):
        # y is height above the frame bottom
        if 0 <= c < SW_L + SW_R and 0 < y <= TOP:
            lst.append(f"M{c} {bottom - y}h1v1h-1z")

    for i in range(N):
        phi = i / N
        s = smooth(phi)
        bottom = (i + 1) * SH
        t = (i - impact) / 12.0
        surge = SURGE * 0.75 * math.sin(math.pi * t) ** 0.8 if 0 <= t <= 1 else 0
        bt = (i - impact - 8) / 18.0

        # --- sea side of the wall ---
        hs, fs = [], []
        for c in range(SW_L):
            x = (XW - (SW_L - 1) + c) % W
            h, dist, level, wx = column(x, phi, p)
            b = (c / (SW_L - 1)) ** 2
            h += b * 0.6 * max(0, h - level)                  # shoaling
            wall = math.exp(-(SW_L - 1 - c) / (5 + 6 * max(t, 0)))
            h += surge * wall
            # Solid water stops just above the coping; the rest is plume.
            h = min(h, PIER_H + 2)
            f = foam_at(dist, phi, s, wx)
            if surge * wall > 1.5:
                f = 2 if surge * wall > 5 else max(f, 1)
            if 0 <= bt <= 1 and c >= SW_L - 1 - (4 + 18 * bt):
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

        # --- the face: white water hugging the wall as the crest hits ---
        k = i - impact
        if 0 <= k <= 4:
            jet = [PIER_H + 4, PIER_H + 10, PIER_H + 14, PIER_H + 12, PIER_H + 7][k]
            for y in range(hs[-1] - 2, jet):
                for dc in (-2, -1, 0, 1):
                    c = SW_L - 1 + dc
                    lean = (y - PIER_H) / 6          # leans inland as it rises
                    cc = int(c + max(0, lean) * (0.6 if dc >= 0 else 0.3))
                    if hashv(cc * 5 + y, i) < 0.85 - 0.15 * abs(dc + 0.5) - 0.02 * (y - PIER_H):
                        px(cc, y, bottom)

        # --- plume: up past the lighthouse and raining down ---
        for x, y, streak in plume.get(i, []):
            xi, yi = int(x), int(round(y))
            gi = hs[xi] if 0 <= xi < SW_L else PIER_H
            if yi <= gi:
                continue
            px(xi, yi, bottom)
            if streak:
                px(xi, yi - 1, bottom)

        # --- water on the pier, running back to the edge ---
        d = sheet.get(i)
        fade = min(1.0, (N - 1 - i) / 5)       # nothing left when the loop wraps
        if d:
            d = [x * fade for x in d]
            for c, dep in enumerate(d):
                col = SW_L + c
                if dep >= 0.9:
                    # dark body with a broken white top, so it reads against
                    # the waves behind
                    n = int(round(min(dep, 4)))
                    water.append(f"M{col} {bottom - PIER_H - n}h1v{n}h-1z")
                    if hashv(col, i) < 0.85:
                        px(col, PIER_H + n, bottom)
                    if n >= 3 and hashv(col * 7, i) < 0.35:
                        px(col, PIER_H + 1 + int(hashv(col, i * 3) * (n - 1)), bottom)
                elif dep >= 0.3 and hashv(col * 3, i) < dep:
                    px(col, PIER_H + 1, bottom)

        # --- pouring off the edge back into the sea ---
        amt = pour.get(i, 0) * fade
        if amt > 0.05:
            for y in range(hs[-1] + 1, PIER_H + 1):
                for c in (SW_L - 1, SW_L - 2):
                    if hashv(c * 7 + y, i) < min(0.9, amt * 1.2):
                        px(c, y, bottom)
            # and churn where it lands
            for c in range(SW_L - 5, SW_L):
                if hashv(c * 13, i) < min(0.8, amt):
                    px(c, hs[c] + 1, bottom)

    total = N * SH
    width = SW_L + SW_R
    return f'''<svg viewBox="0 0 {width} {total}" shape-rendering="crispEdges">
            <path style="fill:var(--front-light)" d="{''.join(light)}"/>
            <path style="fill:var(--front)" d="{''.join(water)}"/>
            <path style="fill:var(--foam)" d="{''.join(foam)}"/>
          </svg>'''

params = {
    "back":  dict(f=3, f2=6, drift=16, amin=1.0, amax=3.0, base=4.0, rise=1.0, r=0.4),
    "mid":   dict(f=2, f2=4, drift=24, amin=1.5, amax=4.5, base=4.0, rise=1.5, r=0.5),
    "front": dict(f=1, f2=3, drift=48, amin=2.0, amax=5.5, base=3.5, rise=2.0, r=0.8),
}


# ---------- Sky: clouds ----------
def pixels(rows, ch):
    """ASCII art -> SVG path of 1x1 runs for character ch."""
    d = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            if row[x] == ch:
                x0 = x
                while x < len(row) and row[x] == ch:
                    x += 1
                d.append(f"M{x0} {y}h{x - x0}v1h-{x - x0}z")
            else:
                x += 1
    return "".join(d)

CLOUDS = {
    "a": ["      #####           ",
          "   ########## ####    ",
          "  #################   ",
          " #####################",
          "######################",
          " ++++++++++++++++++++ "],
    "b": ["    #####     ",
          "  ########### ",
          "##############",
          " ++++++++++++ "],
    "c": ["     ####  ###    ",
          "  ############### ",
          "##################",
          " #################",
          "  ++++++++++++++  "],
}

def cloud(rows):
    w, h = len(rows[0]), len(rows)
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" shape-rendering="crispEdges">'
            f'<path style="fill:var(--cloud)" d="{pixels(rows, "#")}"/>'
            f'<path style="fill:var(--cloud-shade)" d="{pixels(rows, "+")}"/></svg>')

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
    for k, rows in CLOUDS.items():
        html = html.replace("{{cloud_" + k + "}}", cloud(rows))
        html = html.replace("{{CW_" + k + "}}", str(len(rows[0]))).replace("{{CH_" + k + "}}", str(len(rows)))
    for n, p in params.items():
        svg = layer(n, p)
        vbw = SHEET if n == "front" else 1000
        svg = svg.replace("{VBW}", str(vbw)).replace("{PX0}", "0")
        html = html.replace("{{" + n + "}}", svg)
    for k, v in dict(N=N, HF=HF, CYCLE=CYCLE, LOOP=LOOP, SW=SW, SWL=SW_L, SH=SH, LIFT=LIFT, SHEET=SHEET).items():
        html = html.replace("{{" + k + "}}", f"{v:g}")
    open(out, "w").write(html)
    print("bytes", len(html), "wall column", XW)
