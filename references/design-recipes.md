# Coordinated design recipes

Run `scripts/select_design_recipe.py` after title and platform selection. Treat its JSON as a locked visual recipe. Do not average several outputs, fill omitted palette colors, or let the image generator replace the recipe with a familiar blue-purple planet composition.

## V4 manifest axes

The selector now resolves the visual grammar before the atmospheric recipe. Read the catalog files in `../design-system/` and preserve these independent axes in the returned manifest:

`CARRIER → INFORMATION_STRUCTURE → COMPOSITION_CONTRACT → SUBJECT_ASSEMBLY / COMPOSITION_OPERATORS → FOCAL_EVENT / RELEASE_ZONE → SUBJECT_RESOLUTION → SPECULATIVE_MORPHOLOGY WHEN APPLICABLE → RENDER_TREATMENT / SCALE_ROLE → SCREEN_STATE WHEN SUPPORTED → PALETTE / TOPOLOGY → TYPE / MATERIAL / DETAILS`

`CARRIER` describes output context and information density. `LAYOUT_FAMILY` identifies one content-driven Composition Contract that locks title hierarchy, object slot, collision, support anchors, crop, release area, failure signals, and thumbnail behavior before subject selection. `SUBJECT_ASSEMBLY` then resolves the visible subjects as `SINGLE_OBJECT`, `COMPOUND_SET`, `PRIMARY_SATELLITES`, or `REPEATED_FAMILY`; every mode must read as one `SUBJECT_MASS`. `COMPOSITION_OPERATORS` state the primary spatial relation, focal operation, and support alignment. `SUBJECT_ORIGIN_MODE` then states whether the replaceable payload is non-referential, historically real, or speculatively invented. `SPECULATIVE_MORPHOLOGY` resolves shape ancestry only for an invented object. `RENDER_TREATMENT` controls color and material assimilation; `SCALE_ROLE` controls size independently; `SCREEN_STATE` is resolved only for a family with explicit display support; `FOCAL_EVENT` describes the memorable disruption; and `RELEASE_ZONE` remains deliberately quiet. `GRADIENT_TOPOLOGY` is atmospheric and must not stand in for composition.

Object footprint and perceptual attention are independent. A monumental fragment may occupy more literal canvas area than the title, but the title must remain the first reading event. For multiple objects, pass `--subject-assembly COMPOUND_SET`, `PRIMARY_SATELLITES`, or `REPEATED_FAMILY` only when the content requires that relationship; otherwise keep the default `SINGLE_OBJECT`. Do not invent extra objects merely for visual variety.

Use exactly one visual subject origin: `ABSTRACT_FORM`, `ARCHIVE_ARTIFACT`, or `SPECULATIVE_OBJECT`. Abstract forms lock shape and spatial behavior but never fake product controls. Archive artifacts preserve real historical proportions, materials, and 2–4 identity anchors, using only `FAITHFUL_RETAINED` or `ENVIRONMENT_GRADED`. Speculative objects state one hypothetical function, resolve one complete preset or custom morphology from the open contract in `speculative-morphologies.json`, preserve 2–4 purpose-bearing parts, and use `PALETTE_ASSIMILATED` or `ENVIRONMENT_GRADED`. A supplied image is a source override, not a fourth visual style.

### Speculative morphology

Use `--speculative-morphology AUTO` when one of these optional archetypes fits:

- `BUBBLE_CAPSULE`: sphere or ovoid with a generous convex canopy or rounded portal.
- `STREAMLINE_POD`: swelling nose and tapered teardrop/torpedo tail, with running gear or propulsion absorbed into the body.
- `BIOMORPHIC_APPARATUS`: inflated or joined-lobe device with one enlarged aperture, core, grip, or contained function.
- `SOFT_VERTICAL_INFRASTRUCTURE`: elongated rounded fins, arches, and pod thresholds rather than glass-box architecture.

These four entries are not the allowed universe. If the function or source implies another form, create one JSON object conforming to `custom-morphology.schema.json` and run:

`--speculative-morphology CUSTOM_COMPOSED --custom-morphology-file <path>`

Define `shape_ancestry`, one memorable `silhouette`, one `exaggeration`, an integrated `aperture_rule` or function-bearing negative space, 1–4 `construction_cues`, and `material_direction`. Custom forms may use loops, suspended cavities, nested shells, membranes, branching chambers, or other coherent rounded structures. Do not describe them as a current product category plus futuristic styling.

The selector returns exact silhouette, exaggeration, aperture, construction, material, and hard-failure fields. Include them in generation. Start with the chosen volume and integrate function into it; do not start with a present-day object and soften the corners. Restrained warm chrome trim and retro lacquer gloss are allowed. Full mirror-chrome bodies, contemporary concept-car light, black glass bands, full-width LED strips, and cold gray-white minimalism remain failures.

### Screen states

Use `--screen-state` only when the resolved object family declares support:

- `DORMANT` keeps the display materially present but generates no content.
- `SIGNAL` is the default active state and adds one nonverbal low-resolution phosphor system without changing the copy inventory.
- `CARRIER` requires `EDITORIAL_POSTER` plus `--screen-copy-element "EXACT LOCKED SUPPORT STRING"`. The returned string remains designed copy, appears exactly once inside the screen, and must be removed from its external anchor.

For every other object family, the selector returns `NOT_APPLICABLE`. In repeated families, only the primary instance may be active.

### Render treatments and scale roles

- `FAITHFUL_RETAINED`: keep local color and material evidence; the palette surrounds the object.
- `ENVIRONMENT_GRADED`: apply one global cast, grain, and print surface while preserving identity and material transitions.
- `PALETTE_ASSIMILATED`: derive body, light, shadow, haze, and gradient from active hues; use only for abstract or speculative subjects.

Scale is independent from provenance:

- `FIELD_STRUCTURE`: full or near-full-canvas abstract atmosphere.
- `MONUMENTAL_FRAGMENT`: 55–120% of the short edge with decisive architectural crop.
- `INTEGRATED_HERO`: 28–55%, sharing primary attention with the title.
- `CENTERPIECE_ARTIFACT`: 32–62%, complete or nearly complete and framed by title/support copy.
- `SPECIMEN_ANCHOR`: 12–26%, intact and visibly grounded by baseline, horizon, tangent, or contact shadow.
- `REPEATED_FIELD`: 2–5 same-family instances with one focal scale and one quiet release zone.

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

## Abstract-form focal mode and hero deck

Only `ABSTRACT_FORM` branches between these focal modes:

- `HERO_OBJECT` — base probability 55%. Render one discrete retro-futuristic focal object with locked geometry, material, lighting, scale, placement, and title relationship.
- `ATMOSPHERIC_STRUCTURE` — base probability 45%. Render no discrete hero. The gradient topology, primary atmospheric form, spatial bridge, pale device, and alignment system must still create a complete focal structure.

Use history-aware balance inside the abstract branch. `ARCHIVE_ARTIFACT` and `SPECULATIVE_OBJECT` always use one selected object family; their variation comes from treatment, scale role, layout, and focal event. Never interpret atmospheric mode as permission to place text on an unfinished gradient.

The hero deck contains five rotating families:

| Family | Approved hero objects |
|---|---|
| `SCULPTURAL_VOLUME` | matte atmospheric orb, translucent bubble/pod, restrained torus portal |
| `EARLY_CG_GEOMETRY` | geodesic globe, translucent prism/monolith, wireframe polyhedron |
| `SPATIAL_STRUCTURE` | folded perspective grid or grid well, nested portal tunnel |
| `RADIANT_SYMBOL` | luminous four-point star, restrained atomic starburst |
| `STREAMLINE_BIOMORPHIC` | tapered capsule/teardrop, amoeba or cellular membrane |

Do not repeat a recent hero family or exact hero ID within the last three records when another compatible choice exists. The selector's individual weights make the atmospheric orb and luminous four-point star recurring possibilities without making either a default.

Treat each hero as a complete recipe, not a noun. Follow its returned `geometry`, `material`, `lighting`, `scale`, `placement`, and `title_relationship`. The hero owns the cover's dimensional or glow budget. Keep supporting accents flat, quieter, and below 1% combined canvas area; use no more than one compatible bridge. A controlled luminous halo is allowed only when the selected hero explicitly permits it.

Treat the selector's `primary_form_placement`, `spatial_assignment`, `title_clear_zone`, `primary_form_clearance`, and `collision_resolution` as part of every recipe. In atmospheric mode, a side-weighted form uses the side complementary to the locked title zone by default. Same-side placement requires a visible portal opening, frame, counter-shape, or negative-space relationship; shared alignment alone is insufficient. Centered placement is allowed, including a four-point star near the canvas center, when its solid silhouette, luminous core, and highest-contrast edge stay outside the visible title glyphs plus the specified buffer and the remaining canvas has a defined role. The form may occupy unused negative space beside shorter title lines; do not confuse the overall title-block rectangle with the actual glyph envelope. Keep label outlines and decoration outside the primary form's core contour, highest-contrast region, and visual center. If a collision is predicted, preserve title wording and readable scale, then reflow, translate, or modestly scale the form in that order as appropriate.

### Role-aware four-point stars

Scale and lighting follow role rather than shape name:

- When `H09_RADIANT_FOUR_POINT_STAR` is the `HERO_OBJECT`, use exactly one principal star at 32–46% of the short edge, with roughly 40% as the normal center of the range. Give it a warm-white or active-hue-derived core and one broad, feathered active-hue haze. Blend the haze into the cross-canvas gradient without a visible circle, ring, donut, isolated blob, or lens flare. The hero owns the glow budget.
- When a four-point star is an `ANCHOR`, keep it at 3–8% of the short edge. When it is an `ECHO`, keep it at 1–3%. Decorative stars use a flat fill or thin outline with no broad halo, dimensional glow, or ownership of the center of gravity.
- A four-point-star hero may permit one or two tiny flat four-point-star echoes only when they remain within the echo scale and combined accent-area limits. They are subordinate repetitions, not a second radiant system.

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

Never scatter decoration. Use no more than one accent language plus one hairline bridge. In atmospheric mode, if the primary form is a flattened orb, prohibit four-point stars and orbit lines. In hero mode, use only the returned compatible accents and bridge. If a selected hero already contains a grid, portal, star, or other complex language, do not repeat that language as a bridge or accent, except that `H09_RADIANT_FOUR_POINT_STAR` may use its explicitly allowed tiny flat star echoes. When the title is long, reduce bridge and echo density before reducing title size.

## Typography modes

For Chinese, use exactly one sans-serif direction:

- `CJK_NEO_GROTESK` — default, target roughly 60%. Use optically even strokes, open counters, calm squared terminals, and medium or semibold weight. Prefer it for long titles and whenever another mode would reduce readability.
- `CJK_SOFT_HUMANIST` — target roughly 25%. Use subtly softened turns, open counters, and restrained humanist modulation without becoming rounded, cute, handwritten, or lifestyle-script-like. Favor high-key, warm, blush, apricot, pistachio, and pale-device compositions.
- `CJK_STRUCTURAL_SANS` — target roughly 15%. Use slightly compact but uncondensed proportions, crisp horizontal/vertical construction, and a quiet architectural or wayfinding character. Favor perspective planes, folded structures, portals, mid-tone fields, and deep-velvet compositions. Do not use it consecutively when another valid mode exists.

Use weight 500–600, natural tracking, and approximately `1.08–1.18` leading for multi-line Chinese. For English, default to a regular-to-medium optical weight around 450–500 and increase toward semibold only when contrast or resolution requires it. Break lines semantically, not by fixed character count. Create futurism through scale, spacing, alignment, color, and geometry rather than altered glyphs.

Avoid every Song/Ming or serif-style Chinese title, default system Heiti, extra-bold poster black, cute rounded type, faux-tech stencil type, calligraphic display, narrow Gothic type, and deliberately sliced or distorted glyphs. For English, map neo-grotesk to clean sans or neutral grotesk, soft humanist to restrained humanist sans, and structural sans to an architectural display sans with readable open forms.

## Diversity gate

The selector persists the last three design records when runtime state is available. Reject a plan when it:

- repeats a recent palette family or either of the last two gradient topologies while alternatives exist;
- ignores the focal-mode streak rule or repeats a recent hero family/ID while compatible alternatives exist;
- changes only hue while repeating title zone, primary form, topology, and details;
- fills every available palette hue instead of following `COLOR_COMPLEXITY`;
- uses the same accent or typography mode consecutively without need;
- mixes several recipes into a generic average;
- collapses into a glowing planet, orbit, and sparkle composition.

When a recipe conflicts with explicit user direction, rerun the selector with `--exclude ID`, where the ID may be a palette ID, composition ID, topology, or primary form. Preserve the user's direction rather than hand-editing unrelated axes.
