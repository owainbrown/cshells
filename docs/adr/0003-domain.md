# ADR-0003: cshellsbytheseashore.dev

Status: Accepted, 2026-09-26

## Context
cshells.com is parked for resale and cshells.io is registered. cshellsbytheseashore.dev and .com had no registry record on 26 September 2026.

## Decision
Register cshellsbytheseashore.dev at Cloudflare Registrar, which sells at cost (US$12.20 a year at the time of writing), and serve the site from the apex.

## Consequences
.dev is on the HSTS preload list, so the site only works over HTTPS. It will be unreachable until GitHub issues its certificate after DNS resolves. The long name reads as the pun; it's typed less than it's clicked.
