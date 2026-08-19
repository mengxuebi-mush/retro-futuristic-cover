# Minimal retro-futuristic editorial cover system

Use this reference when composing the image-generation request. Inspect and attach `../assets/visual-reference.png` as the style reference. The controlled three-element text contract in `SKILL.md` is absolute; use the reference's hierarchy but do not copy its literal wording.

## Visual DNA

Build a calm, gradient-first retro-futuristic cover rather than a retro newspaper or cyberpunk poster.

- Build one continuous chromatic atmosphere across the entire canvas. Blend all colors into a single spatial field rather than placing separate halos.
- Form the field from two to four oversized, heavily overlapping gradient masses whose transitions cross broad areas of the canvas. Let some color centers sit beyond the canvas edge so no gradient reads as a self-contained circle.
- Add fine monochromatic grain or a subtle frosted texture without muddying the title.
- Keep colors luminous, airy, and softened by haze and grain. Do not make them muddy, gray, beige-only, or generically desaturated.
- Reserve a large uninterrupted quiet field before placing the title.
- Build the decoration from one primary form, one editorial alignment system, zero to two total hairline structures, and one micro-accent family with 1–3 instances. Choose the primary form from a misted arch, soft portal, flowing chromatic shape, curved translucent surface, faint perspective plane, or flattened edge-cropped orb.
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
- Select exactly one direction: **restrained editorial serif**, **clean sans**, or **neutral grotesk**. Rotate the direction across recent outputs rather than defaulting to a serif.
- A restrained editorial serif uses moderate contrast and sturdy strokes. Never use an oversized ultra-high-contrast Didone that makes the cover resemble a fashion or fragrance advertisement.
- A clean sans uses open proportions and quiet geometry. A neutral grotesk uses practical, slightly compact proportions without becoming condensed poster type.
- For Chinese, use a modern CJK sans or restrained Song/Ming-style editorial face with sturdy readable strokes.
- Use one family, one dominant scale, and no more than two weights.
- Keep line breaks natural. Avoid condensed poster type, novelty fonts, outlines, multiple text boxes, cramped tracking, stretched glyphs, and excessive italics.
- Keep `FINAL_TITLE` as the only obvious information layer.
- Set `CATEGORY_LABEL` in tiny uppercase sans, approximately 8–12% of the title cap height, near a top corner. It may sit inside one thin rounded pill or beside one short hairline.
- Set `MICRO_SUBTITLE` in tiny sans, approximately 8–14% of the title cap height, using one or two short lines at most. Place it below the title or near the lower margin.
- Keep both support elements legible but quiet; they must not compete with or visually enlarge the text footprint of the title.
- Use black/near-black text on light fields and warm-white text on indigo fields. Micro-accents follow the same contrast rule.

## Title footprint gate

- Use 1–3 title lines on portrait and square covers; use 1–2 on X landscape and banner covers.
- Aim for a title block occupying roughly 25–35% of the canvas rather than half or more of the page.
- Keep the title block within roughly 55–62% of the canvas width on portrait covers unless the primary form is deliberately absent from that zone.
- Preserve a calm buffer of roughly 4% of the canvas width between the title and the brightest or highest-contrast edge of the primary form.
- Reject a title that becomes a near-full-page fashion billboard, collides with the primary form, or loses contrast over a bright edge.

## Editorial detail recipe

Every cover must include:

1. One whitelisted top `CATEGORY_LABEL`.
2. One `MICRO_SUBTITLE` with no more than five English words or roughly eight Han characters.
3. One micro-accent family chosen from four-point stars, equilateral or right triangles, diamonds/rhombi, tiny dots, thin rings, or minimal corner brackets.
4. Between one and three instances of that micro-accent family, placed where the composition benefits rather than at a fixed corner.
5. One primary abstract form integrated into the gradient.
6. One category-label treatment chosen from a plain aligned label with a short rule, a thin outlined pill, or a minimal corner alignment.
7. Zero to two total hairline structures such as a curve, short rule, corner crop, pill outline, perspective grid, portal outline, or partial frame. Count the category rule or pill outline toward this limit.

Keep each micro-accent no larger than roughly 3% of the short canvas edge and keep their combined footprint below roughly 1.5% of the canvas. Use flat fills or thin outlines only: no bevels, 3D depth, heavy shadows, or glow. A cluster of three should read as one quiet punctuation mark, not three competing focal points.

Create a visible editorial relationship rather than scattering decorations. Align at least two of the category label, title block, primary form, structural line, and micro-accents to a shared edge, axis, tangent, or baseline. Distribute the remaining details around the perimeter and title. Randomize the label treatment, accent family, count, placement, and orientation across outputs while keeping the visual DNA consistent.

## Primary-form and composition families

Randomly choose one family and adapt it to the title. Do not announce the choice.

1. **Misted arch** — a large blurred arch grown from the gradient, one quiet structural line, and a small geometric punctuation family.
2. **Soft portal** — an offset portal fragment with no hard glow, a shared tangent or baseline, and sparse flat accents.
3. **Flowing chromatic shape** — one broad asymmetric color ribbon or blob crossing an edge, paired with a short rule or partial frame.
4. **Perspective plane** — an extremely faint perspective grid or folded plane used as the primary structure, balanced by one small marker family.
5. **Curved translucent surface** — one edge-cropped abstract membrane or arc with low-contrast depth, aligned to the title without resembling a planet.
6. **Flattened orb** — a translucent, heavily cropped orb integrated into the gradient with no rim glow or specular highlight. Pair it with brackets, dots, rings, triangles, or rhombi; never pair it with orbit lines or starbursts.

Vary the primary form, approved palette family, title placement, typography direction, label treatment, and accent family. When recent output is visible, do not repeat both its primary-form family and typography direction.

## Anti-cliché combination gate

Reject the complete combination of oversized high-contrast Didone, glowing 3D planet, orbit line, and sparkle. It reads as a generic AI space poster rather than an editorial system. If two or more of those traits appear, replace enough decisions that the composition no longer reads as a cosmic-poster template.

Do not use literal space imagery as shorthand for “future.” Futurism must come from proportion, alignment, cropped geometry, color flow, and restrained structural detail.

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
- a glowing 3D planet, luminous rim, specular sphere, or literal cosmic scene;
- oversized high-contrast fashion Didone paired with space imagery;
- decorative shapes scattered without a shared alignment, tangent, baseline, or structural relationship;

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
- the title uses too many lines, occupies roughly half the page, collides with the primary form, or crosses its brightest edge;
- the primary form, typography direction, and micro-accent family repeat the most recent visible output without reason;
- the layout triggers the anti-cliché combination gate or lacks a coherent editorial alignment system;
- the grain reads as a coarse uniform filter or softens text edges at thumbnail size;
- the composition ignores the requested platform ratio.
