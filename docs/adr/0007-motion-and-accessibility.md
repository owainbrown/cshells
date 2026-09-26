# ADR-0007: CSS-only motion with a pause control

Status: Accepted, 2026-09-26

## Context
WCAG 2.2 SC 2.2.2 (Level A) requires a way to pause motion that starts automatically and lasts more than five seconds.

## Decision
All animation is CSS. `prefers-reduced-motion` shows a still frame. `static/js/motion.js` adds a "Pause waves" toggle that sets `data-motion="paused"` on `<html>`, remembers the choice where storage is allowed, and tells embedded demos. The `<h1>` keeps `aria-label="C Shells"` and the scene is `aria-hidden`.
