# ADR-0008: Deterministic frame captures, run locally

Status: Accepted, 2026-09-26

## Decision
Header changes are reviewed from frame captures: pause every animation with `document.getAnimations()`, seek to fixed times and screenshot at 1100, 390 and 320px in light and dark, in Chromium and WebKit. Run by hand when the header changes; not part of CI.
