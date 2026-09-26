# ADR-0002: GitHub Pages, deployed by GitHub Actions

Status: Accepted, 2026-09-26

## Context
The repo lives on GitHub, the site is static, and deploys should happen on push with no manual step.

## Options
GitHub Pages with Actions (one vendor, no previews), Cloudflare Workers static assets (previews, custom headers, a second vendor), Netlify or Vercel.

## Decision
GitHub Pages, deployed by `.github/workflows/hugo.yaml`. Dependabot keeps the actions current.

## Consequences
One account and one place to look. No preview URLs; `make serve` shows drafts locally. GitHub Pages can't set response headers, so there's no `frame-ancestors` protection; that's acceptable for a site with no logged-in actions. Cloudflare Workers is the fallback if previews or headers become important.
