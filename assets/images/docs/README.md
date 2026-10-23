# Documentation figures

The `.txt` companions preserve the source diagrams' spatial layouts and connections.
Run `python3 scripts/generate-site-diagrams.py` after editing them to regenerate the
Jost/orange, theme-aware SVG versions. Keep text labels sharp; only connections use
slightly uneven strokes. The browser and wire process figures use explicit
rectangular nodes in `scripts/generate-architecture-figures.py`, called by the
shared generator; update those node layouts when their source text changes. The `site-figure` shortcode embeds the SVG and exposes its
text companion in a collapsed, copyable panel. Documentation Markdown exports retain
the text representation.

Wide figures scroll inside their container on mobile so branches and columns retain
their relationships. Blog SVGs have independently authored text companions and use
`blog-figure`; three-stage component figures use `component-flow` with HTML labels
and sketch outlines.
