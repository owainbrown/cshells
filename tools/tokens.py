"""Generate assets/css/tokens.css from tools/design/tokens.json.

tokens.json is exported from the C Shells design system. Run `make tokens`
after changing it; never edit tokens.css by hand.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
t = json.loads((ROOT / "tools" / "design" / "tokens.json").read_text())

light, dark = [], []
for c in t["color"]["tokens"]:
    light.append(f"  --{c['name']}: {c['value']['light']};")
    dark.append(f"  --{c['name']}: {c['value']['dark']};")
for s in t.get("shadow", {}).get("tokens", []):
    v = s["value"]
    light.append(f"  --{s['name']}: {v['light'] if isinstance(v, dict) else v};")
    dark.append(f"  --{s['name']}: {v['dark'] if isinstance(v, dict) else v};")

other = [f"  --{x['name']}: {x['value']};"
         for fam in ("spacing", "radius", "size") for x in t.get(fam, {}).get("tokens", [])]
other += [f"  --font-{k}: {v};" for k, v in t["type"]["families"].items()]

dk = "\n".join(dark)
css = (
    "/* GENERATED from tools/design/tokens.json (make tokens). Do not edit by hand. */\n"
    ":root {\n" + "\n".join(light + other) + "\n}\n"
    "@media (prefers-color-scheme: dark) {\n  :root:not([data-theme=\"light\"]) {\n    color-scheme: dark;\n"
    + "\n".join("  " + l for l in dark) + "\n  }\n}\n"
    ":root[data-theme=\"dark\"] {\n  color-scheme: dark;\n" + dk + "\n}\n"
)
out = ROOT / "assets" / "css" / "tokens.css"
out.write_text(css)
print(f"wrote {out.relative_to(ROOT)} ({len(css)} bytes)")
