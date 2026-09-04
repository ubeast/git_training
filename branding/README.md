# Branding

Logo and mark for the training courses.

## The idea

The mark is a **branch-and-merge graph**: a base commit splits into two paths
and merges into a tip. It's the one picture common to all three courses (Git,
GitLab, Git in Databricks) — version control, drawn. The larger tip node reads
as "where you're headed."

## Files

| File | Use |
| --- | --- |
| `logo.svg` | Horizontal lockup (mark + wordmark) — light backgrounds |
| `logo-dark.svg` | Horizontal lockup — dark backgrounds |
| `logo-stacked.svg` | Mark above wordmark — slides, title pages |
| `mark.svg` / `mark-dark.svg` | Mark only — light / dark backgrounds |
| `mark-mono.svg` | Mark in a single colour (`currentColor`, defaults to ink) — one-colour print, embossing, watermarks |
| `favicon.svg` | Self-contained square icon with background — browser tabs, avatars |

All are SVG (scalable, diff-able, no binary blobs in the repo).

## Palette

| Role | Hex | Notes |
| --- | --- | --- |
| Accent (nodes) | `#F05032` | Git orange |
| Ink — light theme | `#1F2328` | near-black |
| Ink — dark theme | `#E6EDF3` | near-white |
| Favicon background | `#1F2328` | so the icon reads on any tab colour |

## Using it in the root README (theme-aware)

GitHub strips `<style>` from inline SVG, so switch files with `<picture>`:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="branding/logo-dark.svg">
  <img alt="Git Training" src="branding/logo.svg" width="360">
</picture>
```

## Clear space & minimum size

- Keep clear space around the logo equal to the diameter of one node.
- Don't render the horizontal lockup below ~120 px wide — use `mark.svg` instead.

## The wordmark font

The wordmark uses a system sans stack (`ui-sans-serif, -apple-system, "Segoe
UI", Roboto, …`) so the SVG is self-contained. For a fixed, portable wordmark
(print, or environments without those fonts), outline the text:

```bash
# with Inkscape 1.x
inkscape logo.svg --export-text-to-path --export-plain-svg=logo-outlined.svg
```

## Generating PNGs

No rasteriser is checked in. Any of these work:

```bash
# rsvg-convert (librsvg)
rsvg-convert -w 1024 branding/logo.svg -o logo@1024.png

# Inkscape
inkscape branding/logo.svg -w 1024 -o logo@1024.png

# cairosvg (pip install cairosvg)
cairosvg branding/logo.svg -o logo@1024.png --output-width 1024
```

Or open any of the SVGs in a browser and screenshot.
