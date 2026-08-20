# Minimal retro-futuristic editorial cover system

Inspect and attach `../assets/visual-reference.png` as a style-only reference. Use its atmosphere, hierarchy, grain, geometry, and restraint; never copy its words, numbers, or multi-card grid. Read `design-recipes.md` and execute the selector before composing the generation request.

## Contents

- [Visual DNA](#visual-dna)
- [Gradient and color gates](#gradient-and-color-gates)
- [Typography](#typography)
- [Title footprint](#title-footprint)
- [Composition layers](#composition-layers)
- [Pale editorial device](#pale-editorial-device)
- [Detail-role grammar](#detail-role-grammar)
- [Compatibility gate](#compatibility-gate)
- [Platform composition](#platform-composition)
- [Hard negatives](#hard-negatives)

## Visual DNA

Build a calm, gradient-first retro-futuristic editorial cover rather than a retro newspaper, cyberpunk poster, or generic gradient background.

- Create one continuous chromatic atmosphere with broad transitions and intermediate mixed hues.
- Keep color luminous, softened by diffuse light, pale veils, and fine frosted grain.
- Preserve generous negative space, but shape it through color movement, cropping, alignment, or geometric tension.
- Use one dominant title, one primary abstract form, one alignment system, an optional pale editorial device, and one restrained detail language.
- Make title, color field, geometry, and decoration behave as one poster. Removing the text must still reveal a directed and balanced background composition.
- Prefer asymmetry, edge cropping, shared tangents, long diagonals, partial frames, and quiet perspective over centered cosmic symbolism.

## Gradient and color gates

Use the selector's `PALETTE_FAMILY` as an allowed color relationship and `ACTIVE_HUES` as the actual inventory. Never fill every available palette color by default.

- Follow the locked `COLOR_COMPLEXITY`: one, two, three, or controlled spectral blend.
- Count independent hue families, not derived light and dark tones.
- Follow `AREA_HIERARCHY`; never distribute active hues evenly.
- Allow only one saturation focus. Render other hues as pale fields, haze, intermediate blends, or translucent layers.
- Derive near-white from an active hue rather than using pure white.
- Build the selected `GRADIENT_TOPOLOGY` across broad canvas regions. Let some centers sit beyond the canvas edge.
- Keep a subtle undertone through nominally pale regions so they do not become blank white holes.
- Add fine monochromatic grain without softening text edges.

Reject the gradient when:

- its color regions can be counted as separate circular blobs;
- it contains repeated equal-size blooms, white-centered glow rings, isolated halos, donut gradients, or spotlight dots;
- a `SINGLE_FAMILY` recipe introduces an unrelated accent hue;
- a `DUAL_FIELD` recipe becomes 50/50 or adds a third independent hue;
- a triad or spectral blend has no clear dominant color;
- transitions collapse into gray, brown, beige, or muddy neutral;
- the selected topology is not visible when the text is mentally hidden.

### Approved hue anchors

- Warm ivory `#F4EBDD`
- Powder sky `#A8CAE5`
- Mineral blue `#739AC7`
- Diffused indigo `#414486`
- Periwinkle `#8C89CB`
- Soft lavender `#B59BD2`
- Soft violet `#805CAE`
- Blush `#EBA6B6`
- Coral `#F27462`
- Apricot `#F1B25F`
- Muted amber `#D69A55`
- Pale pistachio `#DCE2AA`
- Soft sage `#B7C6A2`

Treat these as perceptual anchors. Reduce chroma near very high or low lightness so pale tones remain powdery and deep tones remain velvety. Use near-black `#17191B` only for text and small details on light fields, below 3% of image area. Use warm white `#F8F2E8` on deep fields.

## Typography

- Render exactly `FINAL_TITLE`, `CATEGORY_LABEL`, and `MICRO_SUBTITLE`, once each.
- Use the selector's type mode. For Chinese, use only `CJK_NEO_GROTESK`, `CJK_SOFT_HUMANIST`, or `CJK_STRUCTURAL_SANS`; never use Song/Ming or another serif-style Chinese title. For English, map these modes to clean/neutral grotesk, restrained humanist sans, or architectural display sans.
- Use one family and no more than two weights. For Chinese, keep title weight around 500–600 with open counters, sturdy strokes, natural tracking, and semantic line breaks.
- Use approximately `1.05–1.15` display leading for English and `1.08–1.18` for Chinese.
- Set the category label in tiny uppercase sans, approximately 8–12% of title cap height.
- Set the micro-subtitle in tiny sans, approximately 8–14% of title cap height and no more than two short lines.
- Use crisp text edges. Reject Chinese Song/Ming, thin fashion Didone, default heavy system Heiti, extra-black, condensed poster type, cute rounded type, faux-tech stencil, sliced glyphs, novelty fonts, outlines, stretched glyphs, or multiple unrelated text boxes.

## Title footprint

- Use 1–4 title lines on portrait and square covers, 1–3 on landscape posts, and 1–2 on a shallow banner.
- On landscape, let a 5–10-word title occupy roughly 45–54% of canvas height when three lines are appropriate. On portrait or square, target roughly 38–52%.
- Keep the title within roughly 55–62% of portrait width unless the form is absent from that zone.
- Preserve roughly 4% of canvas width between the title and the brightest or highest-contrast edge of the primary form.
- Preserve semantically approved wording before reducing type. Reflow first; reduce decoration second; reduce title size last.

## Composition layers

Build in this order:

1. Continuous atmospheric field following the selected topology.
2. One selected primary form integrated into that field.
3. Optional pale editorial device.
4. Title and two support-text elements on the locked alignment system.
5. One anchor/echo accent language and zero or one bridge.
6. Fine grain applied behind crisp text.

Align at least three of title, primary form, pale device, label, bridge, and accents to a shared edge, axis, tangent, baseline, or curvature. The title and primary form must have a legible structural relationship rather than merely occupying opposite sides.

## Pale editorial device

When selected, create exactly one pale inset as part of the atmosphere:

- Occupy 15–35% of the canvas.
- Make it 8–18% lighter than the surrounding field using a tint of an active hue; never use pure white.
- Use the locked edge-cropped rectangle, arched inset, curved cutout, or translucent side plane.
- Place only `PANEL_TEXT_ROLE` inside it and add no copy.
- Use no drop shadow, glassmorphism, heavy border, floating-card depth, or dashboard styling.
- Let it crop at an edge or align to the title, form, or bridge so it shapes negative space.
- Do not combine it with an outlined category pill.

## Detail-role grammar

Use the selected accent family consistently:

- `ANCHOR`: exactly one focal instance, about 3–8% of the short edge.
- `BRIDGE`: zero or one hairline curve, rule, frame, portal outline, or perspective system.
- `ECHO`: one or two instances of the anchor family at about 1–3% of the short edge.

Keep combined accents under 2% of the canvas. Keep hairlines around 0.08–0.18% of the short edge at 12–30% opacity. Use flat fills or thin outlines without bevel, 3D depth, shadow, or glow.

Place anchor and echoes along the same edge, axis, tangent, curvature, or baseline. A bridge must connect at least two major regions. A perspective grid counts as one bridge system. Do not use a fixed favorite corner.

## Compatibility gate

- Never pair a flattened orb with starbursts or orbit lines. Remove rim glow and specular highlights.
- Never pair a perspective grid with a second complex line system.
- Never pair a pale panel with an outlined category pill.
- When a large four-point star is the anchor, render its echoes much smaller and add no second star language.
- When the title is long, remove the bridge or one echo before reducing title size.
- Allow one visual surprise only: pale panel, perspective structure, large star, portal, or unusual chromatic surface. Keep other layers quiet.
- Reject oversized high-contrast serif + glowing planet + orbit + sparkle. Replace at least two decisions.
- Never use literal space imagery as shorthand for futurism.

## Platform composition

### Xiaohongshu 3:4

- Design for phone-feed scanning with an approximate 8% safe margin.
- Use the upper or middle half for the title and leave at least one third as shaped negative space.
- Let pale devices and primary forms crop decisively at edges rather than becoming centered cards.

### X post landscape 16:9

- Use a clear left or right title zone inside an approximate 7% safe margin.
- Let the topology carry atmosphere across the width; do not add more content to fill space.
- Ensure the far side contains a form, color direction, panel edge, or detail echo rather than an unfinished blank region.

### Square 1:1

- Recompose rather than crop. Use a strong off-center title block and approximate 8% safe margin.
- Move the gradient diagonally or vertically and balance one primary form against the title.

### Banner 3:1

- Recompose for the shallow field with 7% horizontal and 12% vertical safe margins.
- Sweep the topology horizontally and use only a wide cropped form or restrained bridge.
- Keep support text especially quiet.

## Hard negatives

Never produce:

- newspapers, zines, listicles, infographics, dashboards, moodboards, collages, or dense magazine pages;
- extra captions, dates, numbers, badges, stickers, logos, UI panels, fake data, or pseudo-text;
- silhouetted workers, robots, literal computers, or explanatory scenes unless explicitly requested;
- neon cyberpunk, black-dominant backgrounds, sepia, tan, dark brown, olive, khaki, teal, corporate navy, primary red, acid green, or electric cyan;
- disconnected radial halos, stock-gradient emptiness, glowing planets, specular spheres, or cosmic scenes;
- scattered ornaments without a structural relationship;
- a pale device that reads as a floating UI card;
- a background that becomes directionless or unfinished when the text is hidden.
