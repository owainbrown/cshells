# C Shells

Source for [cshellsbytheseashore.dev](https://cshellsbytheseashore.dev): notes on building mobile apps and the tools around them.

Built with [Hugo](https://gohugo.io) 0.166.0 and deployed to GitHub Pages on every push to `main`. Decisions are recorded in [docs/adr](docs/adr).

## Writing

```sh
hugo new posts/my-post/index.md   # new post (draft: true by default)
make serve                        # preview with drafts at http://localhost:1313
```

Set `draft: false` and push to publish. Interactive demos start from `tools/demo/template.html`, live in `static/demos/<post folder>/` and are embedded with the `demo` shortcode (ADR-0009). Callouts: `{{< callout note >}}…{{< /callout >}}` (`note`, `warn`, `danger`).

## The header

The animated sea header is generated, not hand-written (ADR-0004):

```sh
make header            # regenerate from tools/sea/gen.py and template.html
make tokens            # regenerate colour tokens from tools/design/tokens.json
make check-generated   # fail if generated files are stale
```

## Licences

Fonts are under the SIL Open Font License; see `static/fonts/LICENSE-*.txt`.
