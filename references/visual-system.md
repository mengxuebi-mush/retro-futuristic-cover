# Minimal retro-futuristic editorial cover system

Inspect and attach `../assets/visual-reference.png` as a style-only reference. Use its atmosphere, hierarchy, grain, geometry, and restraint; never copy its words, numbers, or multi-card grid. Read `design-recipes.md` and execute the selector before composing the generation request.

## Contents

- [Visual DNA](#visual-dna)
- [V3 visual grammar](#v3-visual-grammar)
- [Gradient and color gates](#gradient-and-color-gates)
- [Typography](#typography)
- [Title footprint](#title-footprint)
- [Composition layers](#composition-layers)
- [Optional hero-object system](#optional-hero-object-system)
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
- Use one dominant title, the selected focal mode, one alignment system, an optional pale editorial device, and one restrained detail language.
- Make title, color field, geometry, and decoration behave as one poster. Removing the text must still reveal a directed and balanced background composition.
- Prefer asymmetry, edge cropping, shared tangents, long diagonals, partial frames, and quiet perspective over centered cosmic symbolism.

## V3 visual grammar

Read the machine-readable catalogs in `../design-system/` before composing. They are the source of truth for reusable visual structure; this document describes how to apply them.

### Decision order

Resolve one manifest in this order:

`carrier → information structure → Composition Contract → subject assembly + composition operators → focal event + release zone → subject resolution → render treatment + scale role → palette/topology → type/material/details`

Do not use gradient topology as a proxy for composition. `EDGE_BLOOM` or `DIAGONAL_DRIFT` describes atmospheric color movement; `ASYMMETRIC_COUNTERWEIGHT` or `FRAME_THRESHOLD` describes spatial construction. They are independent axes.

### Carrier signals

The carrier changes what counts as a finished composition:

- `SOCIAL_COVER`: screen-native crop, immediate title tier, thumbnail-first hierarchy.
- `EDITORIAL_POSTER`: flat front-facing page, asymmetric wall-poster logic, decisive edge crop.
- `PHOTO_COVER`: recognizable subject, faithful or abstract image treatment, 2–4 identity anchors.
- `PACKAGING_FACE`: seam, fold, label boundary, or die-cut implication; no invented product facts.
- `RECORD_SLEEVE`: square sleeve geometry, one strong image or typographic event, quiet support text.

Carrier signals are structural cues, not extra decoration. Never add a phone frame, mockup, fake label panel, artist credit, nutrition facts, QR code, barcode, or platform UI merely to signal a carrier.

Words such as “cover” do not override visible information needs. Event details, a request for more small copy, or a richer metadata system are `EDITORIAL_POSTER` density signals unless a platform constraint explicitly requires a compact three-element carrier.

### Composition Contracts

Select one content-driven Composition Contract before resolving the subject or background atmosphere. Walk the `selection_flow` in `layouts.json` from top to bottom and use the first compatible match unless the user has explicitly requested a composition. `AUTO` is only a fallback when no content signal distinguishes a contract.

The eight contracts are `ASYMMETRIC_COUNTERWEIGHT`, `CENTERED_ANCHOR`, `FRAME_THRESHOLD`, `PERSPECTIVE_VECTOR`, `RHYTHMIC_FIELD`, `TYPE_DOMINANT_FIELD`, `IMAGE_MASK_FIELD`, and `INFORMATION_AXIS`. Each contract owns:

- title-first perceptual attention ranges;
- a named title zone and replaceable object slot;
- one collision rule and explicit crop behavior;
- structural anchors for support copy;
- subject-area and release-area ranges;
- allowed focal events, failure signals, and one thumbnail test.

Treat the subject as payload inside the slot. Crop, scale, orient, repeat, or fragment it to satisfy the contract while preserving identity anchors. Never shrink the title, abandon the release zone, or switch composition merely to show a complete object. `INFORMATION_AXIS` is reserved for `EDITORIAL_POSTER` when truthful 5–7-element copy needs a ruled information skeleton.

### Composition grammar

Read `composition-grammar.json` after selecting the Composition Contract. The eight contracts are finite spatial families, not fixed templates. Resolve each cover as one sentence:

`TITLE_MASS + SUBJECT_ASSEMBLY + PRIMARY_RELATION + FOCAL_OPERATION + RELEASE_ZONE + SUPPORT_ALIGNMENT`

Choose exactly one subject assembly:

- `SINGLE_OBJECT`: one coherent object, image, or abstract field.
- `COMPOUND_SET`: two or three related objects overlapping, aligning, or tightly spacing into one outer silhouette.
- `PRIMARY_SATELLITES`: one primary object with one or two companions attached to its baseline, axis, tangent, cable, shadow, or directional path; the primary keeps at least twice each satellite's visual weight.
- `REPEATED_FAMILY`: two to five instances of one family following one path, with one focal instance and one open title zone.

Multiple objects are allowed only when they resolve into one perceptually unified `SUBJECT_MASS`. Do not create several unrelated hero objects or assign equal visual weight to a primary and its satellites. Object footprint is not perceptual attention: a `MONUMENTAL_FRAGMENT` may occupy more literal canvas area than the title while the title remains the first reading event at thumbnail size.

For every multi-object assembly, write a content-derived `assembly_plan` before generation. A member is a complete, independently countable object—not an opening, cabin, appendage, control, or other internal part. Name each member with a semantic role and visible form cue; then state the relation that binds the members and the rule by which they remain observable at full size and 25%. `COMPOUND_SET` plans 2–3 distinct members. `PRIMARY_SATELLITES` plans one primary plus 1–2 satellites and keeps the primary at least twice each satellite's visual weight. `REPEATED_FAMILY` plans one family unit repeated 2–5 times along one named path with one focal instance. These are assembly constraints, not morphology presets: derive the actual forms from content, function, provenance, or explicit user direction.

The two opposite assembly failures are equally invalid: **competition**, where several objects become unrelated heroes, and **over-fusion**, where planned complete members collapse into one object whose internal parts merely imply multiplicity. The compiled generator instruction must carry the assembly ID, expected count, mass rule, complete member plan, shared relation, and observability rule.

Use the contract's required operators plus the one focal operator mapped from `FOCAL_EVENT`. Support copy must attach to the returned edge, axis, tangent, perimeter, title band, vector, mask, rhythm path, or information rule. Do not improvise a second spatial system.

### Subject-origin rule

Choose exactly one visual origin before appearance:

- `ABSTRACT_FORM`: a non-referential shape or field. Lock one silhouette or field behavior and one spatial action. Do not add fake screens, buttons, handles, seams, or labels.
- `ARCHIVE_ARTIFACT`: a real object from the technological past. Preserve historical proportions, local material distinctions, and 2–4 identity anchors. Use `FAITHFUL_RETAINED` or `ENVIRONMENT_GRADED`; never `PALETTE_ASSIMILATED`.
- `SPECULATIVE_OBJECT`: an invented but apparently functional future device. State one hypothetical function and lock 2–4 purpose-bearing parts. Use `PALETTE_ASSIMILATED` or `ENVIRONMENT_GRADED`; reject a generic rounded blob with decorative controls.

Then choose an independent scale role. A real computer may be a `MONUMENTAL_FRAGMENT`, `CENTERPIECE_ARTIFACT`, `SPECIMEN_ANCHOR`, or `REPEATED_FIELD`; provenance does not determine size. A supplied image is an input-source override, not a fourth visual style.

### Supplied-image preflight

Before cropping, masking, extracting, recoloring, or adding a face- or object-attached element, normalize the source's orientation metadata into its actual pixel matrix and save or use that normalized asset consistently. Inspect those pixels upright before defining 2–4 identity anchors.

Every later mask, crop, landmark, overlay, accessory, and preview must use the same normalized coordinate system. Run a simple registration check before applying the visual treatment: confirm that face or object landmarks, silhouette boundaries, pose, and the locked identity anchors still align in the actual renderer. If they do not, stop and repair the transform before judging treatment quality. A recognizable but rotated person, displaced accessory, or mismatched mask is a source-transform failure, not evidence for or against a treatment direction.

Extraction, halftone, scan structure, localized color plates, and attached optical elements remain optional treatment candidates rather than universal defaults. Choose them only when they integrate the supplied subject with the selected Composition Contract while preserving identity and title priority.

### Focal event and release zone

Select exactly one `focal_event` from the layout's allowed events. The event is the one thing a viewer should remember at thumbnail size: a decisive crop, title/contour tension, scale anomaly, repeated rhythm, portal entry, or negative-space cut. Every other element either supports that event or creates the `release_zone`; it must not become a second focal point.

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

- On `SOCIAL_COVER`, `PHOTO_COVER`, `PACKAGING_FACE`, and `RECORD_SLEEVE`, render exactly `FINAL_TITLE`, `CATEGORY_LABEL`, and one supporting-copy role—`MICRO_SUBTITLE` or `SUPPORTING_DECK`—once each. On `EDITORIAL_POSTER`, render the three locked core elements plus 2–4 exact factual support strings, for 5–7 designed elements total.
- Read the compiled `typography_contract` rather than inferring scale from the words “dominant” or “quiet.” It owns the title mode, physical footprint envelope, line range, minimum visual weight, support-copy role, legibility floor, and cluster relationship.
- Use the selector's type mode. For Chinese, use only `CJK_NEO_GROTESK`, `CJK_SOFT_HUMANIST`, or `CJK_STRUCTURAL_SANS`; never use Song/Ming or another serif-style Chinese title. For English, map these modes to clean/neutral grotesk, restrained humanist sans, or architectural display sans.
- Use one family and no more than two weights. For Chinese, keep title weight around 500–600 with open counters, sturdy strokes, natural tracking, and semantic line breaks. For English, default to a regular-to-medium optical weight around 450–500; move toward semibold only when local contrast, resolution, or the chosen face requires it.
- Derive text color from an active hue, normally one or two tonal steps deeper than the local field. Avoid an unrelated navy or near-black that breaks harmony. Target at least 3:1 contrast for the large title and 4.5:1 for the category and supporting copy where feasible; when readability is marginal, combine same-hue deepening with a modest weight increase.
- Use approximately `1.05–1.15` display leading for English and `1.08–1.18` for Chinese.
- Set the category label according to its compiled ratio and full-size legibility floor. “Tiny” means subordinate, never unreadable.
- Keep `MICRO_SUBTITLE` to one short line. Set `SUPPORTING_DECK` as a readable one- or two-line deck according to the compiled ratio and legibility floor; never shrink exact long wording into micro-text.
- Use crisp text edges. Reject Chinese Song/Ming, thin fashion Didone, default heavy system Heiti, extra-black, condensed poster type, cute rounded type, faux-tech stencil, sliced glyphs, novelty fonts, outlines, stretched glyphs, or multiple unrelated text boxes.
- Treat authentic labels, key legends, screen UI, dial marks, clothing text, and other source-borne markings as `INTRINSIC_ARTIFACT_TEXT`, not designed poster copy. Preserve them when identity-bearing and safe; keep them subordinate and never invent replacements. Generated `SCREEN_CARRIER` text is explicitly excluded and remains budgeted designed copy.

## Screen-state system

Resolve `SCREEN_STATE` only after the object family and subject assembly. A screen is a conditional object capability, not a new composition layer and not permission to add fake UI.

- `DORMANT`: render curved deep active-hue glass, subdued reflection, and readable casing/screen material separation. Add no generated content.
- `SIGNAL`: render one sparse low-resolution nonverbal system—such as a waveform with one block cursor, a vector trace, or a simple geometric scope—using phosphor derived from `ACTIVE_HUES`. Add no readable letters, words, numbers, code, menu, icon set, dashboard, or pseudo-text.
- `CARRIER`: use only on `EDITORIAL_POSTER`. Relocate exactly one already locked factual support string into the screen, render it once in compact low-resolution monospace over one or two lines, and remove it from every external support zone. The string remains part of the 5–7 designed-element budget and is never `INTRINSIC_ARTIFACT_TEXT`.

Keep emission local to the glass and preserve the selected palette hierarchy. At 25%, the title must remain the first reading event; screen content stays in the support tier. For `REPEATED_FAMILY`, activate only the largest or compositionally primary screen and keep every subordinate screen `DORMANT`.

## Title footprint

- Select the compiled mode from `design-system/typography-contracts.json`. A title with no more than eight visible non-space glyphs uses `SHORT_TITLE_EXPANDED`: enlarge, strengthen, stack, or create a controlled edge interaction so the title becomes a deliberate graphic mass rather than a floating label.
- Use 1–4 title lines on portrait and square covers, 1–3 on landscape posts, and 1–2 on a shallow banner.
- On landscape, let a 5–10-word title use a balanced three-line stack whose tight visible-glyph block occupies roughly 28–34% of canvas height; treat 28% as a floor when ample clear space exists. On portrait or square, target roughly 38–52%.
- Keep the title within roughly 55–62% of portrait width unless the form is absent from that zone.
- Build `TITLE_CLEAR_ZONE` from the union of the visible glyph silhouettes on each title line plus a calm buffer of roughly 4% of canvas width. Do not approximate it as one large rectangle: unused space beside a shorter line may hold a form when the buffered glyph shapes remain clear.
- Keep the primary form's solid silhouette, luminous core, and brightest or highest-contrast edge outside `TITLE_CLEAR_ZONE`. Allow only soft low-contrast atmosphere behind the title, and only when glyph edges and thumbnail readability stay crisp.
- Preserve semantically approved wording before reducing type. Reflow first; reduce decoration second; reduce title size last.

## Composition layers

Build in this order:

0. Lock `CARRIER`, the content-driven `LAYOUT_FAMILY`, and its attention contract, title zone, object slot, collision rule, support zones, crop rule, failure signals, and thumbnail test.
1. Resolve one allowed `SUBJECT_ASSEMBLY`; lock the returned `COMPOSITION_OPERATORS` and `COMPOSITION_SENTENCE` so every object becomes one subject mass.
2. Continuous atmospheric field following the selected topology.
3. Lock one focal event and one release zone allowed by the Composition Contract.
4. Resolve the subject assembly into the locked object slot. Follow the selected provenance, treatment, scale role, mass rule, and crop rule.
5. Resolve one supported `SCREEN_STATE` without adding a second focal event; if `CARRIER`, relocate one locked support element.
6. Optional pale editorial device, only when it supports the release zone and the carrier.
7. Locked designed copy on the support-alignment operator: three elements for compact carriers or 5–7 for an editorial poster, including any screen-carried element. The three core roles form one typographic cluster; do not scatter category, title, and supporting copy into unrelated corners.
8. One anchor/echo accent language and zero or one bridge.
9. Fine grain applied behind crisp text.

First distribute visual weight, then establish alignment. When an atmospheric form clearly occupies one side, place the title in the complementary side by default. Allow same-side placement only when a portal opening, frame, counter-shape, or negative-space relationship is visibly intentional and preserves both title and form. Align at least three of title, hero or atmospheric form, pale device, label, bridge, and accents through a shared edge, axis, tangent, baseline, or curvature that may span the canvas; do not stack them in the same region merely to satisfy the alignment count.

The Composition Contract is the structural owner. The carrier supplies context and information density; the subject fills the replaceable object slot; the focal event supplies one memorable disruption; the release zone supplies silence. Do not let a carrier signal become decorative UI, and do not combine multiple contracts in one cover.

## Subject rendering system

`ABSTRACT_FORM` may use an abstract `HERO_OBJECT` or `ATMOSPHERIC_STRUCTURE`. `ARCHIVE_ARTIFACT` and `SPECULATIVE_OBJECT` use one selected object family. `SOURCE_ASSET_MODE` replaces generated subject construction while preserving identity anchors.

When rendering a discrete subject:

- Render exactly one returned abstract recipe, archive object family, speculative object family, or supplied image field. Follow its geometry, material, lighting, scale role, placement, title relationship, identity contract, accents, and bridge constraints.
- For `ARCHIVE_ARTIFACT`, preserve provenance, real material distinctions, authentic proportions, and source-borne text when safe. Environmental tint and grain may unify the object, but cannot redesign it.
- For a screen-capable archive computer, follow the returned screen state, display language, copy role, text rule, attention rule, and instance rule. Do not improvise a second screen behavior.
- For `SPECULATIVE_OBJECT`, state the hypothetical function before rendering and expose the locked purpose-bearing parts. Palette assimilation may soften boundaries but cannot erase the functional silhouette.
- For supplied images, preserve 2–4 source-specific identity anchors rather than replacing the subject with a catalog object.
- Allow centered, offset-center, counter-space-adjacent, background-layer-overlapping, or decisively edge-cropped placement when returned. Centered placement is valid only when the title clear zone remains intact; do not force every hero to the same side.
- Give the hero one structural relationship with the title: shared tangent, glyph-safe background overlap, counter-shape, baseline, axis, portal opening, vanishing direction, or aligned corner. Never pass a solid silhouette, luminous core, or high-contrast edge across a letterform.
- Resolve a predicted collision by preserving the approved wording and readable title scale, trying a balanced narrower reflow when suitable, then translating or modestly scaling the hero. Never keep a centered hero by shrinking the title into a caption.
- Let the hero own all conspicuous depth, refraction, wireframe complexity, or glow. Keep other layers flat and quiet.
- Follow `RENDER_TREATMENT`: archive local colors may survive under faithful or environmental grading; palette-assimilated abstract and speculative subjects derive their body, light, shadow, and haze from active hues.
- For `H09_RADIANT_FOUR_POINT_STAR`, render exactly one hero star at 32–46% of the short edge, normally near 40%. Use a warm-white or active-hue-derived core plus a broad violet/periwinkle-or-other-active-hue haze that dissolves seamlessly into the full gradient field. Reject a visible circular boundary, ring, donut, isolated glow blob, or lens flare. Only this hero role receives the large scale and conspicuous glow.

When `FOCAL_MODE` is `ATMOSPHERIC_STRUCTURE`:

- Render no discrete central object merely to fill space.
- Make the selected gradient topology, atmospheric primary form, optional pale device, bridge, and title alignment establish the center of gravity.
- Reject a background that becomes a stock gradient, disconnected blobs, or an unfinished empty half when the text is hidden.

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

Keep combined accents under 2% of the canvas in atmospheric mode and under 1% in hero mode. Keep hairlines around 0.08–0.18% of the short edge at 12–30% opacity. Use flat fills or thin outlines without bevel, 3D depth, shadow, or glow. A four-point star selected as an anchor or echo remains within these decorative scales and never inherits the H09 hero halo. A hero's explicitly allowed lighting does not turn its glow into an accent effect.

Place anchor and echoes along the same edge, axis, tangent, curvature, or baseline. Keep the anchor, echoes, label outlines, and decorative lines outside the primary form's core contour, highest-contrast region, and visual center; place them along an outer edge, tangent, or extended axis instead. A bridge must connect at least two major regions. A perspective grid counts as one bridge system. Do not use a fixed favorite corner.

## Compatibility gate

- In atmospheric mode, never pair a flattened orb with starbursts or orbit lines. In hero mode, follow the returned compatibility rules; a sculptural orb still prohibits the planet + orbit + sparkle cliché.
- Never pair a perspective grid with a second complex line system.
- Never pair a pale panel with an outlined category pill.
- When a four-point star is the anchor, keep it at 3–8% of the short edge, render its echoes at 1–3%, and add no second star language. A star may exceed this range only when it is the explicit H09 hero.
- When the title is long, remove the bridge or one echo before reducing title size.
- Allow one visual surprise only. A selected hero consumes that budget; reduce pale-panel probability and keep other layers quiet.
- Reject oversized high-contrast serif + glowing planet + orbit + sparkle. Replace at least two decisions.
- Never use literal space imagery as shorthand for futurism.

## Platform composition

### Xiaohongshu 3:4

- Design for phone-feed scanning with an approximate 8% safe margin.
- Use the upper or middle half for the title and leave at least one third as shaped negative space.
- Let pale devices and primary forms crop decisively at edges rather than becoming centered cards.

### Xiaohongshu long-form 3:4

- Deliver exact 3:4 at 1080 x 1440 px, but do not reuse the ordinary image-note title footprint.
- Use a deep-safe horizontal margin of approximately 10–12% and keep the title block to roughly 72–76% of canvas width. Judge the gap from the visible outermost letterform, not only from the text-box boundary.
- Prefer a slightly smaller title with more deliberate line breaks over a wide title that merely fits the raw canvas. Preserve the selected type mode, weight, and leading; create safety through scale, line breaks, and placement rather than condensed type.
- Treat the long-form UI as a potentially inset or lightly recropped container. Keep `FINAL_TITLE`, `CATEGORY_LABEL`, the selected supporting-copy role, the anchor, and the title-facing part of the bridge inside the deep-safe region. Decorative forms may bleed beyond it.
- Preferred workflow: design a 9:16 master at 1080 x 1920 px, lock all critical elements inside its centered 3:4 window from y=240 to y=1680, inspect that crop, and export the centered crop as the final 1080 x 1440 cover.
- If composing directly at 3:4, simulate the same result by previewing a version with an additional 4% inset on every side. Reject any title that becomes cramped, visually touches the container, or loses balance under that preview.

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
- disconnected radial halos, stock-gradient emptiness, literal planets, hard-rim specular spheres, or cosmic scenes; a selected matte orb or controlled radiant hero is allowed only under its recipe;
- scattered ornaments without a structural relationship;
- a pale device that reads as a floating UI card;
- a background that becomes directionless or unfinished when the text is hidden.
