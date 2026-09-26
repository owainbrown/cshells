# ADR-0009: Demos are self-contained HTML in sandboxed iframes

Status: Accepted, 2026-09-26

## Decision
Each demo is one HTML file in `static/demos/<post folder>/`, started from `tools/demo/template.html`, and embedded with `{{< demo src="name.html" caption="..." >}}`.

- The iframe uses `sandbox="allow-scripts"` only. Never add `allow-same-origin`: with `allow-scripts` on same-origin content it lets a demo remove its own sandbox.
- The template's CSP blocks all network access (`connect-src 'none'`). A demo that needs a library adds one pinned CDN with Subresource Integrity, or vendors the file.
- `demo-kit.js` (inlined in the template) reports the demo's height. `static/js/demo-host.js` accepts messages only from the demo's own window, only as a number, clamped to 120 to 2000px.
- Demos follow `prefers-color-scheme`, `prefers-reduced-motion` and the page's pause control, and don't use storage.
- Review each demo's code before publishing.

## Consequences
Demos drop in without conversion and can't break the build, the page or each other.

Demos live under `static/` rather than in the post folder because Hugo treats `.html` files in a post folder as content pages.
