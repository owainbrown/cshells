# ADR-0004: The sea header is generated locally and committed

Status: Accepted, 2026-09-26

## Context
The header's waves, foam and wall break are about 150 pre-rendered sprite frames from a Python wave model. Adding Python to every deploy adds a second toolchain.

## Decision
`tools/sea/gen.py` and `tools/sea/split.py` (standard library only) write `layouts/partials/sea-header.html` and `assets/css/sea-header.css`. Both carry a "generated" banner. Run `make header` after changing the model or template; `make check-generated` fails if the committed files are stale.

## Consequences
Deploys need Hugo alone. The header changes rarely, so the manual step costs little.
