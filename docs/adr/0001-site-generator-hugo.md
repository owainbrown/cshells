# ADR-0001: Hugo as the site generator

Status: Accepted, 2026-09-26

## Context
The blog is Markdown posts, one custom animated header and embedded demos. The long-term cost is keeping the build working, not building the site.

## Options
Hugo (one static binary), Eleventy (Node, small npm tree), Astro (Node, larger npm tree, components and MDX), or a hosted platform (Ghost, Hashnode).

## Decision
Hugo, pinned to 0.166.0 in the workflow and `hugo.toml`, with a small hand-written theme and no third-party theme.

## Consequences
No npm tree to patch. Go templates are terse, but the theme is small. Revisit in favour of Astro only if demos need shared components, TypeScript or bundled npm packages (see ADR-0009).
