# ADR-0006: Self-hosted fonts

Status: Accepted, 2026-09-26

## Decision
Latin woff2 subsets of Press Start 2P (masthead only), Bricolage Grotesque (headings), Atkinson Hyperlegible Next (body) and Atkinson Hyperlegible Mono (code and labels) are served from `/fonts`, about 130 KB in total, with their OFL licences alongside. No Google Fonts requests.

## Consequences
No third-party requests and no consent banner for fonts. Titles render briefly in a fallback on a cold load (`font-display: swap`).
