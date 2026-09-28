"""Generate the favicon set from one 16 x 16 pixel drawing.

    static/favicon.svg          modern browsers; follows light and dark mode
    static/favicon.ico          older browsers and the default /favicon.ico request (32px PNG inside)
    static/apple-touch-icon.png iOS home screen (180px)

Standard library only (see ADR-0004). Run `make favicon` after changing the drawing.
"""
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# The lighthouse on Seaham's North Pier, with the sea at its foot.
#   . sky   D tower dark   L tower light   Y lamp   g glow
#   b wave crest   w foam   f sea light   s sea   d deep
ART = [
    "................",
    ".......DD.......",
    "......DDDD......",
    ".....DDDDDD.....",
    "...g.DYYYYD.g...",
    ".....DYYYYD.....",
    "....DDDDDDDD....",
    "......LLLL......",
    "......LLLL......",
    "......DDDD......",
    "......DDDD......",
    ".....LLLLLL.....",
    "bb...DDDDDD...bb",
    "wfbbbbDDDDbbbbfw",
    "ffffwffffffwffff",
    "ssssssssssssssss",
]

# Token values from tools/design/tokens.json (light, dark).
COLOURS = {
    ".": ("#cdeefa", "#141b33"),   # sky
    "D": ("#1d2230", "#46506e"),   # tower-dark (lifted in dark mode so the tower reads against the night sky)
    "L": ("#f4f4f0", "#c9ccd6"),   # tower-light
    "Y": ("#ffd23f", "#fff1a8"),   # lamp
    "g": ("#ffe27a", "#fff1a8"),   # halo
    "b": ("#8ccbe0", "#2c4675"),   # back swell
    "w": ("#ffffff", "#cfe3ff"),   # foam
    "f": ("#3f8fc4", "#25427a"),   # front-light
    "s": ("#226fa6", "#182c56"),   # front
    "d": ("#174f7d", "#101f40"),   # deep
}


def svg():
    rects = []
    for key in COLOURS:
        if key == ".":
            continue
        d = []
        for y, row in enumerate(ART):
            x = 0
            while x < 16:
                if row[x] == key:
                    x0 = x
                    while x < 16 and row[x] == key:
                        x += 1
                    d.append(f"M{x0} {y}h{x - x0}v1h-{x - x0}z")
                else:
                    x += 1
        if d:
            rects.append(f'<path class="{key if key.isalpha() else "sky"}" d="{"".join(d)}"/>')
    light = "".join(f".{k}{{fill:{v[0]}}}" for k, v in COLOURS.items() if k.isalpha())
    dark = "".join(f".{k}{{fill:{v[1]}}}" for k, v in COLOURS.items() if k.isalpha())
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" shape-rendering="crispEdges">'
        f'<style>.sky{{fill:{COLOURS["."][0]}}}{light}'
        f'@media (prefers-color-scheme:dark){{.sky{{fill:{COLOURS["."][1]}}}{dark}}}</style>'
        '<rect class="sky" width="16" height="16"/>' + "".join(rects) + "</svg>\n"
    )


def rgb(hex_):
    return bytes.fromhex(hex_[1:])


def png(scale, pad=0):
    """Light-theme PNG: each art pixel becomes a scale x scale block."""
    size = 16 * scale + 2 * pad
    rows = []
    for y in range(size):
        row = bytearray(b"\x00")          # filter: none
        for x in range(size):
            # the padding repeats the edge pixels, so the sea runs to the edge
            ax = min(max((x - pad) // scale, 0), 15) if x >= pad else 0
            ay = min(max((y - pad) // scale, 0), 15) if y >= pad else 0
            row += rgb(COLOURS[ART[ay][ax]][0])
        rows.append(bytes(row))

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"".join(rows), 9))
            + chunk(b"IEND", b""))


def ico(png_bytes, size):
    # One PNG-compressed image inside an ICO container.
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(png_bytes), 6 + 16)
    return header + entry + png_bytes


def main():
    assert len(ART) == 16 and all(len(r) == 16 for r in ART)
    static = ROOT / "static"
    (static / "favicon.svg").write_text(svg())
    (static / "favicon.ico").write_bytes(ico(png(2), 32))
    (static / "apple-touch-icon.png").write_bytes(png(11, pad=2))   # 180px
    for name in ("favicon.svg", "favicon.ico", "apple-touch-icon.png"):
        print(f"wrote static/{name} ({(static / name).stat().st_size} bytes)")


if __name__ == "__main__":
    main()
