# Figure style — nandan.me visual identity

Every figure in `writings/figures/` is published on nandan.me and must follow this spec. Values come
from the site's stylesheet (`assets/css/skins/purple.scss`) and from reference versions made in
Claude Design.

## Colour roles (use only these colours)

| Role | Value | Use |
|---|---|---|
| Canvas | `#ffffff` | full-size background rect; light mode only (the site has no dark mode) |
| Headline ink | `#000000` | headline 21–25px, weight 600–700; big code/result text |
| Body text | `#555555` | 14–15px |
| Muted / eyebrow | `#777777` | 11–12px; eyebrow labels in UPPERCASE with letter-spacing 1.6–2 |
| Accent | `#34374C` | the site's `$accent-color`, for the one thing the figure is about: the emphasis bar, the primary panel's left rule, stroke on key output boxes, key arrows. Text on an accent fill is `#ffffff`. |
| Accent tints | `#8a8c9e`, `#a7a9b7`, `#c9cad3` | the de-emphasised counterpart (for example the "imperative" panel's rule, secondary arrows and badges) |
| Panel fill | `#fafafa` | |
| Hairlines | `#e5e5e5` | dividers, panel borders |
| Box stroke | `#c8c8c8` | neutral value boxes |

Accent means importance: use it once per figure for the main idea, not for decoration.

## Type

- Sans, set on the root `<svg>`:
  `font-family="'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"`
- Mono (code, q/J expressions, values):
  `font-family="ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace"`
- Captions and asides in italic `#555555`.

## Shapes

Corner radius `rx=2` (3 at most); stroke-width 1, or 1.2–1.6 for emphasis; arrowheads as `<marker>`
paths filled with the arrow's own colour.

## Hard rules

- Real `<text>` elements, never text converted to outlines. `<title>` + `<desc>` with
  `aria-labelledby` on the root, and a `<desc>` full enough to replace the image.
- No external references: no `@import`, no webfont links, no `<image>`, no `href` to other files.
  (The site forbids external font dependencies, and an SVG in `<img>` can't load them anyway.)
- viewBox 900 wide (height to fit, about 470–500). Hand-written, readable SVG that diffs well in
  git: no embedded metadata/C2PA blocks, no editor cruft.
- LinkedIn/OG cards: 1200×627 PNG rendered from the same SVG source, same tokens.

## Accuracy

Figure text is checked against the articles and the lessons. Every number and code fragment in a
figure must come from verified output (a lesson file `make verify` runs, or committed eval data).
When restyling, extract every `<text>` string before and after and diff them: the only allowed
difference is line wrapping.
