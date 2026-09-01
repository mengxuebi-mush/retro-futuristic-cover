# Self-critique, repair, and verification

Use this reference after every generated or edited cover. Inspect the actual pixels; never judge from the prompt, plan, or generator description. Keep all verdicts private unless the user asks to see them.

## Contents

- [Precedence and locked invariants](#precedence-and-locked-invariants)
- [Hard-compliance gate](#hard-compliance-gate)
- [Poster-integration gate](#poster-integration-gate)
- [Repair-mode decision](#repair-mode-decision)
- [Three-version state machine](#three-version-state-machine)
- [Full-image regression check](#full-image-regression-check)
- [Verdict format](#verdict-format)

## Precedence and locked invariants

Apply direction in this order:

1. The user's explicit feedback in the current request.
2. Visual preferences the user has confirmed in the current conversation.
3. The bundled visual reference and this skill's visual system.
4. Internal controlled variation.

Style feedback does not silently override exact title wording, platform geometry, the carrier-specific text contract, safety, or another explicit delivery requirement. When improving a version, lock these invariants unless they are the cause of a hard failure:

- every exact designed-copy string locked by the selected carrier contract;
- the selected platform, aspect ratio, and canvas;
- the selected Composition Contract, including attention hierarchy, title zone, object slot, collision, support zones, crop rule, release area, and thumbnail test;
- the selected palette family, color complexity, active hues, area hierarchy, and topology;
- the pale-device state, detail roles, and alignment system;
- the focal mode and, when selected, the hero ID, family, geometry, material, lighting, placement, scale, and title relationship;
- the typography direction;
- every region or relationship that already passes;
- any user-approved visual decision.

## Hard-compliance gate

Mark each item `PASS` or `FAIL` with one observable reason. A single failure prevents delivery.

1. **Semantic fidelity** — The approved `FINAL_TITLE` passes `references/content-fidelity.md`: it preserves `SOURCE_TITLE` meaning and every `MUST_RETAIN_ANCHOR`, and identifies the actual topic when seen alone.
2. **Text inventory** — Transcribe every visible fragment and classify it as designed copy or `INTRINSIC_ARTIFACT_TEXT`. Compact carriers contain exactly the three locked designed strings. `EDITORIAL_POSTER` contains exactly its locked 5–7 designed strings. Authentic source-borne artifact text may remain only when identity-bearing, subordinate, safe, and faithful. `SCREEN_CARRIER` copy remains designed copy, must exactly match one locked support element, and must not repeat externally. Reject invented labels, pseudo-text, repeated copy, watermarks, or logos.
3. **Rendered-title fidelity** — The dominant rendered title exactly matches the approved `FINAL_TITLE` and remains the only dominant message.
4. **Canvas and opacity** — The file has the requested format, pixel dimensions, and aspect ratio. The full perimeter and all four corners contain the intended continuous background; there are no transparent, checkerboard, cutout, unpainted, accidental black-void, or missing-background regions. Run `scripts/verify_image.py` when a local file is available and reject any alpha channel or PNG transparency chunk unless the user explicitly requested a transparent asset.
5. **Color contract** — The actual pixels use only the locked active hues and their derivatives, follow the selected color complexity, tonal regime, area hierarchy, saturation focus, coral role, and black-area limit, and do not activate every available palette color by habit. The gradient is a bottommost, full-bleed field covering 100% of the canvas behind type, subjects, and negative space.
6. **Typography contract** — The actual type direction, line count, weight, leading, footprint, contrast, and readability follow the selected typography and platform rules. For Chinese, verify that the rendered character visibly matches `CJK_NEO_GROTESK`, `CJK_SOFT_HUMANIST`, or `CJK_STRUCTURAL_SANS`, uses a medium-to-semibold 500–600-like weight, and breaks lines semantically. For English, verify a regular-to-medium 450–500-like starting weight unless contrast or resolution justifies semibold. Reject every Song/Ming or serif-style Chinese title, generic heavy system Heiti, cute rounded type, narrow Gothic, faux-tech stencil, sliced glyph, and other prohibited fallback. For a 5–10-word X landscape title, verify that a balanced three-line option was considered and reject a tight visible-glyph block below roughly 28% of canvas height despite ample clear space. Verify palette-derived text color and target at least 3:1 contrast for the large title and 4.5:1 for small support text where feasible.
7. **Recipe contract** — The selected Composition Contract is visibly present: title attention exceeds subject attention even when object footprint is larger; exactly one allowed subject assembly resolves every visible object into one subject mass; the returned primary relation, focal operation, support alignment, object slot, collision, crop rule, and release area are obeyed; no listed failure signal appears; and the actual gradient, subject origin, treatment, scale role, screen state when supported, optional pale device, and detail grammar remain compatible.
8. **Negative constraints** — No forbidden layout, literal scene, cliché combination, disconnected halo field, dense information design, floating UI card, inactive palette color, or competing ornament is present.
9. **Supplied-image transform integrity** — When a source asset is used, inspect the normalized rendered pixels rather than trusting file metadata or a planning preview. The source is upright, its 2–4 identity anchors remain aligned, and every mask, crop, landmark, or attached element uses the same coordinate transform. Reject a rotated subject, displaced overlay, or mismatched extraction before judging the visual treatment.

If semantic fidelity fails, return to title selection and replace `FINAL_TITLE` before generating again. If rendered text, ratio, composition, color, typography, or a forbidden visual element fails, discard the version and use `REGENERATE`. Do not ask an image edit to repair incorrect text. If opacity alone fails while the composition succeeds, use one targeted `EDIT` to continue the locked gradient behind every transparent or unpainted pixel, then inspect the entire image and rerun the deterministic check. Do not flatten onto a generic matte because that destroys the selected palette and gradient topology. A file-format mismatch or exact-size-only mismatch may be normalized deterministically only when the aspect ratio and composition are already correct; reverify after normalization.

Run the deterministic check from the skill directory, substituting the selected preset:

```text
python3 scripts/verify_image.py <image> --width <W> --height <H> --ratio <W:H> --format PNG
```

Use `JPEG` only when the user explicitly requests JPEG output.

## Poster-integration gate

Run this gate only after hard compliance passes. Judge the cover as a designed whole rather than as separate ingredients.

1. **Unified composition** — The result reads as one poster, not typography placed over a generic gradient background. A multi-object result reads first as one compact set, one primary with subordinate satellites, or one repeated family—not as several unrelated hero objects.
2. **Title–form relationship** — The title and primary form share at least one legible structural relationship: edge, axis, baseline, tangent, glyph-safe background overlap, counter-shape, or continuous color flow.
3. **Defined negative space** — Quiet space is shaped by color movement, cropping, alignment, or geometric tension. It does not read as an unfinished empty region.
4. **Visual balance** — The title, brightest transition, primary form, and small details create a deliberate center of gravity without dead corners or one-sided weight.
5. **Structural decoration** — The anchor establishes one quiet secondary focus, the optional bridge connects major regions, and the one or two echoes repeat the anchor language along a shared alignment. The anchor, echoes, label outlines, and decorative lines stay outside the primary form's core contour, highest-contrast region, and visual center; they may follow an outer edge, tangent, or extended axis but may not cut through the focal structure.
6. **Thumbnail clarity** — At approximately 25%, the title is immediately readable, remains dominant, and does not merge with a bright edge, hero silhouette, luminous core, or noisy texture.
7. **Template-resistance** — The cover avoids generic AI-poster shorthand such as a planet, orbit, sparkle, centered slogan, or three radial blooms assembled without a content-specific relationship.
8. **Background structure test** — Mentally hide all designed copy. The remaining color field and subject must still show intentional direction, balance, provenance or function, and spatial structure. They cannot collapse into unrelated light spots, a stock gradient, or an empty canvas.
9. **Reference-family fit** — The result shares the reference's seamless atmosphere, editorial restraint, grain character, and abstract futuristic fullness without copying one card literally.
10. **Recipe fidelity** — The actual palette family, active hue count, area hierarchy, gradient topology, primary form, title zone, type mode, pale-device state, and detail roles form the one selected recipe. The result differs from recent covers in coordinated composition, not only in hue.
11. **Pale-device quality** — When selected, the panel reads as an atmospheric editorial plane rather than a floating UI card, uses an active-hue tint, contains only its locked support-text role, and shapes negative space. When not selected, no accidental card appears.
12. **Color-count discipline** — `SINGLE_FAMILY` reads as one hue family with depth; `DUAL_FIELD` has a clear 70/30-like dominance; `SOFT_TRIAD` has clear 55/30/15-like hierarchy; `SPECTRAL_BLEND` reads as a continuous field rather than four separate blobs.
13. **Long-form crop resilience** — For a Xiaohongshu long-form cover, inspect the final 3:4 asset with an additional 4% inset preview. If using a 9:16 working master, also inspect its centered 3:4 crop. All three text elements must remain fully legible, the visible letterforms must retain generous left and right breathing room, and the title–form relationship must survive without feeling enlarged or clipped.
14. **Subject-mode integrity** — `ABSTRACT_FORM` remains non-referential and has no accidental product controls. `ARCHIVE_ARTIFACT` preserves historical proportions, material evidence, and 2–4 identity anchors without palette assimilation. `SPECULATIVE_OBJECT` communicates one plausible function through 2–4 purpose-bearing parts and visibly follows its selected morphology: one sphere/ovoid/teardrop/inflated-spindle/biomorphic-shell/soft-monolith ancestor, one exaggerated proportion, one integrated rounded canopy or aperture, and secondary parts following the dominant curvature. Reject it if hiding minor details leaves a recognizable present-day car, EV, appliance, device, or building with rounded corners; also reject black glass bands, full-width LED strips, faceted supercar surfaces, touchscreen-first controls, generic matte ceramic blobs, or cold gray-white minimalism. The selected scale role is visible: monumental fragments crop decisively, centerpieces remain coherent, specimen anchors are grounded, and repeated fields use one family only.
15. **Title-clear-zone integrity** — Inspect the actual visible glyph silhouettes, not one coarse title-block rectangle. The primary form's solid silhouette, luminous core, and highest-contrast edge stay outside the glyph envelope plus roughly 4% of canvas width. A centered form or one placed beside shorter title lines passes when this clearance is intact. Soft atmosphere may pass behind the title only when contrast and crispness remain unchanged.
16. **Role–scale integrity** — If the selected hero is `H09_RADIANT_FOUR_POINT_STAR`, exactly one principal star is unmistakable at thumbnail size and occupies 32–46% of the short edge. Any four-point star used as an anchor or echo remains at 3–8% or 1–3% respectively, stays flat, and does not steal the hero or glow budget. A large luminous star must never appear without the H09 hero role.
17. **Hero-halo integration** — When H09 is selected, the warm core and broad active-hue haze dissolve into one continuous gradient with no visible circular boundary, ring, donut, isolated bloom, or lens-flare streak. Decorative stars have no broad halo.
18. **Spatial-weight distribution** — Inspect the title, primary form, brightest transition, label, anchor, and decorative axis as weighted regions. If the title, primary form, and decoration all concentrate on one side while the opposite side has no clear role in color movement, cropping, tension, or support, mark `FAIL` and `REGENERATE`. Shared alignment may cross the canvas; it is not permission to co-locate every high-information element. Same-side title and form placement passes only when a clear portal opening, frame, counter-shape, or negative-space relationship makes the nesting meaningful and preserves both elements.
19. **Composition Contract fidelity** — Run the selected contract's `thumbnail_test`, then compare the image against its `failure_signals`. For `INFORMATION_AXIS`, verify that every support string is supplied or source-grounded and shares the primary rule; for every other contract, verify that support copy remains limited to its named anchors.
20. **Screen-state integrity** — When `SCREEN_STATE` is `DORMANT`, verify that no generated screen content appears. For `SIGNAL`, verify one sparse nonverbal low-resolution system, active-hue-derived local emission, and no readable text or pseudo-text. For `CARRIER`, verify one exact locked editorial support string, no surrounding UI, no external duplicate, and full-size legibility. For `REPEATED_FAMILY`, verify that only the primary screen is active. In every state, the title remains first at 25% and the screen does not become an extra focal event.

Treat items 1, 2, 5, 6, 7, 8, 10, 12, 14, 15, 16, 17, 18, 20, and—when applicable—13 as critical. Any critical failure makes the aesthetic verdict `FAIL` regardless of other strengths. Do not use a vague total score or accept a result merely because most ingredients are present.

## Repair-mode decision

Name one highest-impact **root cause**, not a list of unrelated symptoms. One root cause may explain multiple visible effects; for example, “the composition lacks a shared diagonal structure” can explain both an undefined right side and a disconnected title.

Choose `EDIT` only when all of these are true:

- hard compliance passes;
- the composition's main hierarchy and geometry already work;
- the failure is local and spatially isolatable;
- the change can preserve the approved text and successful regions.

Typical `EDIT` cases include one floating accent, a locally coarse grain patch, one weak color transition, an underdefined corner, a single overstrong line, or an otherwise successful hero that only needs one isolated translation or modest scale reduction to restore the title clear zone. Use `EDIT` for title clearance only when every glyph remains exact and fully readable and the rest of the composition already works; regenerate if the object has obscured or mutated rendered text.

Choose `REGENERATE` when the title and primary form are disconnected, the center of gravity is wrong, the title, form, and decorative axis all pile onto one side while the other side has no clear role, the canvas feels split, decoration crosses the primary form's core, the background structure test fails, the result looks like a generic AI template, the palette or typography contract fails, or a correction would require moving several major regions. Structural failure is not a patching task.

For `EDIT`, attach the preceding image as the edit target. State the single root cause to fix, the exact region affected, and every invariant to preserve. Do not request a general redesign.

For `REGENERATE`, keep the approved strings, platform, palette tuple, and other valid constraints, but select a materially different primary-form family or compositional axis. Do not recreate the failed arrangement with paraphrased prompting.

## Three-version state machine

Use at most three internal versions:

1. Generate `V1`.
2. Run the complete hard gate. On failure, regenerate `V2` except for safe deterministic file normalization.
3. Run the complete poster-integration gate. On failure, choose `EDIT` or `REGENERATE` and produce `V2`.
4. Inspect all of `V2`, not merely the repaired region. If it passes, deliver it.
5. If the original root cause persists, make `V3` a fresh composition. Do not patch the same failure twice.
6. If the original issue is resolved but one new, isolated regression appears, `V3` may be a targeted edit.
7. Inspect all of `V3`. Deliver only if both gates pass.

If no version passes after `V3`, do not present a known failing image as finished work. State concisely that the cover did not clear the quality gate and invite a fresh run. Do not expose failed drafts unless the user requests them.

## Full-image regression check

After every edit, regeneration, conversion, or resize:

- retranscribe all visible text;
- rerun the deterministic file check, including opaque delivery;
- inspect the full perimeter and all four corners for continuous background coverage;
- revisit every hard and aesthetic item;
- compare locked invariants against the preceding approved state;
- inspect full size and thumbnail size;
- for Xiaohongshu long-form, inspect the centered 3:4 crop and the additional 4% inset preview;
- verify the correction did not introduce a seam, text mutation, extra shape, new color, weaker hierarchy, or generic template cue elsewhere.

Never infer that an edit preserved the rest of the image. Verify it from the new pixels.

## Verdict format

Produce one concise internal record per version:

`VERSION` identifies the current attempt in this workflow; do not infer it from an existing filename such as `-v2` or `-v3`.

```text
VERSION: V1 | V2 | V3
HARD: PASS | FAIL — observable evidence
AESTHETIC: PASS | FAIL | NOT_RUN — observable evidence and the single highest-impact root cause
REPAIR_MODE: NONE | EDIT | REGENERATE
LOCK: approved strings; canvas; palette tuple; typography direction; successful regions
VERDICT: PASS — why the poster is complete | FAIL — what must change next
```

Acceptable examples:

```text
VERDICT: FAIL — The right side is undefined negative space because the title and primary form share no axis, tangent, or color flow.
```

```text
VERDICT: PASS — The title, curved surface, and chromatic transition form one continuous diagonal composition; thumbnail text is clear and no extra text is visible.
```

Never write only “looks good,” “mostly works,” or another conclusion without pixel-based evidence.
