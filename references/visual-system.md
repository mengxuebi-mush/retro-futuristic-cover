# Minimal retro-futuristic editorial cover system

Use this reference when composing the image-generation request. Inspect and attach `../assets/visual-reference.png` as the style reference. The controlled three-element text contract in `SKILL.md` is absolute; use the reference's hierarchy but do not copy its literal wording.

## Visual DNA

Build a calm, gradient-first retro-futuristic cover rather than a retro newspaper or cyberpunk poster.

- Build one continuous chromatic atmosphere across the entire canvas. Blend all colors into a single spatial field rather than placing separate halos.
- Form the field from two to four oversized, heavily overlapping gradient masses whose transitions cross broad areas of the canvas. Let some color centers sit beyond the canvas edge so no gradient reads as a self-contained circle.
- Add fine monochromatic grain or a subtle frosted texture without muddying the title.
- Keep colors luminous, airy, and softened by haze and grain. Do not make them muddy, gray, beige-only, or generically desaturated.
- Reserve a large uninterrupted quiet field before placing the title.
- Build the decoration from one primary form, zero to two hairline structures, and one micro-accent family with 1–3 instances. Choose the primary and hairline structures from an edge-cropped translucent orb, flowing blob, arch, portal, perspective grid, thin orbit curve, or hairline frame.
- Keep motifs abstract. Do not let them contain labels, numbers, glyphs, interface copy, or text-like marks.
- Let the elements share axes, overlap, or visually connect so the cover feels composed and futuristic rather than sparsely decorated.
- Favor generous margins, clean editorial geometry, one clear focal point, and enough visual structure that the cover feels full without becoming busy.

## Gradient continuity gate

The gradient must pass all of these checks:

- Read as one uninterrupted field when squinting or viewing the cover small.
- Show broad color-to-color transitions with intermediate mixed hues, not abrupt separation.
- Carry a subtle color undertone through nominally light or ivory areas so they do not become blank white gaps.
- Use asymmetrical, edge-crossing color movement rather than three evenly spaced radial spots.
- Avoid visible circular boundaries, repeated equal-size blooms, white-centered glow rings, spotlight dots, isolated halos, and donut-shaped gradients.
- Reject and regenerate if the colors can be counted as separate blobs or if removing the title makes the background feel like three disconnected lights.

## Typography

- Render exactly `FINAL_TITLE`, `CATEGORY_LABEL`, and `MICRO_SUBTITLE` once each and no other text.
- Use one clean grotesk, neo-grotesk, geometric sans, or restrained editorial serif.
- For Chinese, use a modern CJK sans or restrained Song/Ming-style editorial face with sturdy readable strokes.
- Use one family, one dominant scale, and no more than two weights.
- Keep line breaks natural. Avoid condensed poster type, novelty fonts, outlines, multiple text boxes, cramped tracking, stretched glyphs, and excessive italics.
- Keep `FINAL_TITLE` as the only obvious information layer.
- Set `CATEGORY_LABEL` in tiny uppercase sans, approximately 8–12% of the title cap height, near a top corner. It may sit inside one thin rounded pill or beside one short hairline.
- Set `MICRO_SUBTITLE` in tiny sans, approximately 8–14% of the title cap height, using one or two short lines at most. Place it below the title or near the lower margin.
- Keep both support elements legible but quiet; they must not compete with or visually enlarge the text footprint of the title.
- Use black/near-black text on light fields and warm-white text on indigo fields. Micro-accents follow the same contrast rule.

## Editorial detail recipe

Every cover must include:

1. One whitelisted top `CATEGORY_LABEL`.
2. One `MICRO_SUBTITLE` with no more than five English words or roughly eight Han characters.
3. One micro-accent family chosen from four-point stars, equilateral or right triangles, diamonds/rhombi, tiny dots, thin rings, or minimal corner brackets.
4. Between one and three instances of that micro-accent family, placed where the composition benefits rather than at a fixed corner.
5. One primary abstract form integrated into the gradient.
6. Zero to two hairline accents such as an orbit curve, short rule, corner crop, pill outline, perspective grid, or portal outline.

Keep each micro-accent no larger than roughly 3% of the short canvas edge and keep their combined footprint below roughly 1.5% of the canvas. Use flat fills or thin outlines only: no bevels, 3D depth, heavy shadows, or glow. A cluster of three should read as one quiet punctuation mark, not three competing focal points.

Distribute details around the perimeter and title rather than clustering every element together. They should make the cover feel authored and polished while preserving generous space. Randomize the accent family, count, placement, and orientation across outputs while keeping the visual DNA consistent.

## Composition families

Randomly choose one family and adapt it to the title. Do not announce the choice.

1. **Diffuse horizon** — continuous edge-to-edge gradient atmosphere, a low blended horizon, one large cropped arc, and one to three tiny geometric marks.
2. **Orbital calm** — one translucent edge-cropped orb integrated into the gradient, a thin orbit curve, and one quiet micro-accent family.
3. **Type and light** — dominant title over a broad diagonal color flow, grain, one soft geometric blob, and one to three tiny punctuation shapes.
4. **Quiet signal** — continuous gradient field, an extremely faint perspective grid or flowing signal line, one outlined portal, and a small marker.
5. **Soft portal** — a large blurred arch or portal grown from the gradient, one hairline curve, and one to three minimal accent marks.

Vary the chosen composition, approved palette family, title placement, and type category while preserving this restrained visual family.

## Locked palette system

The target color identity is warm ivory plus powdery cool tones and glowing coral warmth. Use exactly one family below. Hex values are perceptual anchors: stay close to their hue and lightness even when blending.

1. **Sky + coral** — warm ivory `#F4EBDD`, powder blue `#A8CAE5`, luminous coral `#F27462`.
2. **Blush + coral** — blush pink `#EBA6B6`, warm peach `#F3A172`, coral red `#F06F64`, a small amount of warm ivory `#F5EBDD`.
3. **Periwinkle + coral** — powder blue `#A7C8E5`, periwinkle `#8C89CB`, soft lavender `#B59BD2`, coral `#F07867`.
4. **Indigo glow** — diffused indigo `#414486`, violet `#805CAE`, coral `#F1745E`, amber glow `#F0A34E`, with warm white `#F7EFE2` for type. Use the indigo as a velvety color field, never as near-black.
5. **Ivory + apricot + pistachio** — warm ivory `#F4EAD7`, apricot `#F1B25F`, pale pistachio `#DCE2AA`, optional coral `#F07B66`.
6. **Sky + blush** — clear powder blue `#93C2E3`, blush pink `#ECA2C0`, coral `#F17A69`, warm ivory `#F4EBDD`.

Apply color by area:

- Let a light or mid-light base occupy roughly 50–70% of the canvas.
- Let the second gradient color occupy roughly 20–35%.
- Keep the warm coral, amber, or pink bloom to roughly 10–25% unless using the blush + coral family.
- In the indigo glow family only, a diffused indigo/violet field may occupy up to 65%; keep it visibly colorful rather than black.
- Use near-black `#17191B` only for the three approved text elements, micro-accents, or hairline motifs on light backgrounds. Keep black below roughly 3% of the image area.
- Use warm white `#F8F2E8` for headline type on indigo/violet fields.

Create transitions as broad airbrushed color flow, hazy diagonal fields, blurred horizon light, and large overlapping translucent shapes. Preserve recognizable hues while rendering many intermediate blends; do not collapse the field into gray or brown.

Never substitute black, charcoal backgrounds, sepia, tan, dark brown, olive, khaki, teal, corporate navy, primary red, acid green, or electric cyan. Avoid black-and-orange newsprint, rainbow gradients, neon-on-black, harsh complementary clashes, and any palette dominated by beige or gray.

## Platform composition

### Xiaohongshu 3:4

- Design for phone-feed scanning.
- Use 1–3 title lines in roughly the upper or middle half.
- Keep the title inside an approximate 8% perimeter safe margin.
- Let negative space occupy at least one third of the cover.

### X post landscape — 1200 × 675

- Use a clear left or right title zone.
- Use 1–2 title lines when possible.
- Keep the title inside an approximate 7% perimeter safe margin.
- Let the wider gradient field carry the atmosphere instead of adding more content.

### X post square — 1080 × 1080

- Recompose for a balanced square; never crop the landscape design.
- Use 1–3 title lines with a strong off-center block and an approximate 8% perimeter safe margin.
- Let the continuous gradient move diagonally or vertically so the square retains depth rather than becoming a centered badge.
- Balance one primary abstract form against the title. Distribute the category label, micro-subtitle, and small accents across distinct quiet zones.

### X banner — 1500 × 500

- Recompose for the shallow 3:1 field; never stretch or crop another preset.
- Prefer 1–2 short title lines in a compact left, center-left, or centered zone. Keep the title materially shorter and smaller than it would be on a post cover.
- Keep critical text inside an approximate 7% horizontal and 12% vertical safe margin; do not place words at the extreme edges.
- Let the seamless gradient sweep horizontally across the full width. Use a wide cropped form, long hairline curve, faint grid, or portal fragment to make the banner feel intentional.
- Preserve all three approved text elements, but keep the category label and micro-subtitle especially restrained so the low-height layout stays airy.

## Hard negative list

Never produce:

- a newspaper, newsprint page, zine, scrapbook, moodboard, or vintage editorial collage;
- a listicle, “takeaways” panel, numbered list, body-copy column, timeline, flowchart, annotation, or infographic;
- multiple headlines, pull quotes, badges, stickers, extra captions, dates, issue numbers, footers, UI panels, or fake data beyond the controlled top label and micro-subtitle;
- silhouetted people at computers, humanoid robots, magazine cutouts, or literal explanatory scenes unless the user explicitly asks for them;
- high-density layouts, hard black blocks, distressed poster type, or orange-and-black propaganda-poster styling.
- palettes outside the locked families, black/charcoal-dominant backgrounds, muddy brown transitions, gray corporate gradients, or neon cyberpunk color.
- three or more isolated radial halos, repeated spotlight dots, disconnected gradient circles, or a large white-centered color ring.
- a nearly empty background with only one orbit line and one micro-accent; include a primary abstract form and the full editorial detail recipe.

## Reject and regenerate when

- visible text does not equal exactly `FINAL_TITLE`, `CATEGORY_LABEL`, and `MICRO_SUBTITLE` once each;
- the title exceeds the title gate or is unreadable at thumbnail size;
- the design resembles a magazine page, explainer graphic, poster collage, or newsprint layout;
- ornaments or imagery compete with the title;
- saturation, contrast, or detail density feels aggressive rather than calm;
- the hues do not visibly match one approved palette family or the black-area limit is exceeded;
- the gradient reads as separate halos instead of one seamless field;
- the primary abstract form or the 1–3 instance micro-accent family is missing;
- micro-accents are oversized, visually dominant, three-dimensional, heavily shadowed, or exceed the allowed footprint;
- the composition ignores the requested platform ratio.
