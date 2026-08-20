# Coordinated design recipes

Run `scripts/select_design_recipe.py` after title and platform selection. Treat its JSON as a locked visual recipe. Do not average several outputs, fill omitted palette colors, or let the image generator replace the recipe with a familiar blue-purple planet composition.

## Variable color complexity

A palette family defines compatible color relationships, not a checklist of colors that must all appear. `COLOR_COMPLEXITY` determines how many independently readable hue families activate in this cover:

- `SINGLE_FAMILY` — target 25%. Activate one hue family and create depth only with its pale tint, main mid-tone, and soft deep tone. Do not add an independent accent hue.
- `DUAL_FIELD` — target 40%. Activate a dominant hue at 70–80% and one companion at 20–30%. Never split the canvas 50/50.
- `SOFT_TRIAD` — target 25%. Activate three coordinated hues at approximately 55/30/15. Keep only one saturation focus.
- `SPECTRAL_BLEND` — target 10%. Activate three or four compatible anchors, but treat the least prominent color as a transition between fields rather than a separate blob. Keep one dominant hue at 45–55%.

Count perceptually independent hue families, not RGB values. A powder-blue field with pale blue-white, mineral mid-tones, and a velvety blue edge still counts as `SINGLE_FAMILY`.

## Palette families

The selector activates only a valid subset from one family:

| ID | Family | Available relationships |
|---|---|---|
| `P01_POWDER_SIGNAL` | Powder Signal | powder sky, warm ivory, coral |
| `P02_INDIGO_INSIGHT` | Indigo Insight | diffused indigo, periwinkle, apricot |
| `P03_PISTACHIO_FUTURE` | Pistachio Future | warm ivory, pale pistachio, soft sage, apricot |
| `P04_LAVENDER_SYSTEM` | Lavender System | mineral blue, soft lavender, blush |
| `P05_APRICOT_STRUCTURE` | Apricot Structure | warm ivory, apricot, muted amber, coral |
| `P06_BLUSH_FOCUS` | Blush Focus | warm ivory, blush, coral |
| `P07_VELVET_ENERGY` | Velvet Energy | diffused indigo, soft violet, coral, muted amber |
| `P08_QUIET_SPECTRUM` | Quiet Spectrum | warm ivory, powder sky, blush, soft sage |

Render only `ACTIVE_HUES`. An available but inactive hue must be absent as an independently visible field. A derived tinted near-neutral may appear only as a lightness variation of an active hue.

## Gradient topologies

Use the locked topology to define how color moves across the canvas:

- `EDGE_BLOOM` — one oversized field blooms inward from beyond an edge.
- `DIAGONAL_DRIFT` — two broad fields cross diagonally through a long intermediate blend.
- `HORIZON_HAZE` — diffuse light spreads along an asymmetric soft horizon.
- `CHROMATIC_CURTAIN` — one broad vertical or arcing translucent color curtain crosses an edge.
- `CENTER_OF_GRAVITY` — one offset chromatic mass dissolves outward without a circular halo boundary.
- `SPLIT_ATMOSPHERE` — warm and cool fields meet through a broad mixed transition rather than a hard division.

Do not replace topology with several separate radial spots. The background must retain visible direction when the text is hidden.

## Pale editorial device

When `EDITORIAL_DEVICE` is not `NONE`, create exactly one pale inset grown from the surrounding atmosphere:

- Occupy roughly 15–35% of the canvas.
- Use a tint derived from an active hue and make it approximately 8–18% lighter than the local field; never use pure white.
- Use the selected edge-cropped rectangle, arched inset, curved cutout, or translucent side plane.
- Use no drop shadow, glassmorphism, heavy border, dashboard styling, or floating-card depth.
- Place only the selected `PANEL_TEXT_ROLE` inside it: `CATEGORY_LABEL` or `MICRO_SUBTITLE`. Do not add text.
- Align the device with the title, primary form, bridge, or canvas edge so it shapes negative space instead of becoming a pasted-on card.
- Do not combine a pale device with an outlined category pill.

## Detail-role grammar

Use one accent family in three possible roles:

- `ANCHOR` — exactly one focal instance that establishes a small secondary point of attention.
- `BRIDGE` — zero or one hairline structure connecting the title, primary form, panel, or edge.
- `ECHO` — one or two much smaller instances of the anchor family placed along the same axis, tangent, curvature, or baseline.

Keep the anchor around 3–8% of the short edge, each echo around 1–3%, and all accent shapes below 2% of total canvas area. Keep hairlines approximately 0.08–0.18% of the short edge at 12–30% opacity. A perspective grid counts as one bridge system, not many separate ornaments.

Never scatter decoration. Use no more than one accent language plus one hairline bridge. If the primary form is a flattened orb, prohibit four-point stars and orbit lines. If a perspective grid is the bridge, add no second complex line system. When the title is long, reduce bridge and echo density before reducing title size.

## Typography modes

For Chinese, use exactly one:

- `CJK_EDITORIAL_SONG` — contemporary editorial Song/Ming with moderate contrast, sturdy medium or semibold strokes, open counters, and crisp terminals.
- `CJK_NEO_GROTESK` — contemporary neo-grotesk CJK sans with optically even strokes, open counters, calm squared terminals, and medium weight.

Avoid default system Heiti, extra-bold poster black, cute rounded type, faux-tech stencil type, calligraphic display, and delicate classical Song. For English, map `CJK_EDITORIAL_SONG` to restrained editorial serif and `CJK_NEO_GROTESK` to clean sans or neutral grotesk.

## Diversity gate

The selector persists the last three design records when runtime state is available. Reject a plan when it:

- repeats a recent palette family or either of the last two gradient topologies while alternatives exist;
- changes only hue while repeating title zone, primary form, topology, and details;
- fills every available palette hue instead of following `COLOR_COMPLEXITY`;
- uses the same accent or typography mode consecutively without need;
- mixes several recipes into a generic average;
- collapses into a glowing planet, orbit, and sparkle composition.

When a recipe conflicts with explicit user direction, rerun the selector with `--exclude ID`, where the ID may be a palette ID, composition ID, topology, or primary form. Preserve the user's direction rather than hand-editing unrelated axes.
