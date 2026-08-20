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

Style feedback does not silently override exact title wording, platform geometry, the three-element text contract, safety, or another explicit delivery requirement. When improving a version, lock these invariants unless they are the cause of a hard failure:

- the exact three approved strings;
- the selected platform, aspect ratio, and canvas;
- the selected palette family, color complexity, active hues, area hierarchy, and topology;
- the pale-device state, detail roles, and alignment system;
- the typography direction;
- every region or relationship that already passes;
- any user-approved visual decision.

## Hard-compliance gate

Mark each item `PASS` or `FAIL` with one observable reason. A single failure prevents delivery.

1. **Semantic fidelity** — The approved `FINAL_TITLE` passes `references/content-fidelity.md`: it preserves `SOURCE_TITLE` meaning and every `MUST_RETAIN_ANCHOR`, and identifies the actual topic when seen alone.
2. **Text inventory** — Transcribe every visible fragment. The image contains exactly `FINAL_TITLE`, `CATEGORY_LABEL`, and `MICRO_SUBTITLE`, each once, with no misspelling, repetition, pseudo-text, watermark, logo, date, or number.
3. **Rendered-title fidelity** — The dominant rendered title exactly matches the approved `FINAL_TITLE` and remains the only dominant message.
4. **Canvas** — The file has the requested format, pixel dimensions, and aspect ratio. Run `scripts/verify_image.py` when a local file is available.
5. **Color contract** — The actual pixels use only the locked active hues and their derivatives, follow the selected color complexity, tonal regime, area hierarchy, saturation focus, coral role, and black-area limit, and do not activate every available palette color by habit.
6. **Typography contract** — The actual type direction, line count, weight, leading, footprint, contrast, and readability follow the selected typography and platform rules. For Chinese, verify that the rendered character visibly matches `CJK_NEO_GROTESK`, `CJK_SOFT_HUMANIST`, or `CJK_STRUCTURAL_SANS`, uses a medium-to-semibold 500–600-like weight, and breaks lines semantically. Reject every Song/Ming or serif-style Chinese title, generic heavy system Heiti, cute rounded type, narrow Gothic, faux-tech stencil, sliced glyph, and other prohibited fallback. For a 5–10-word X landscape title, verify that a balanced three-line option was considered and reject a caption-like block that uses less than roughly 40% of canvas height despite ample clear space.
7. **Recipe contract** — The actual gradient follows the locked topology; the primary form, optional pale device, panel text role, anchor/bridge/echo grammar, and alignment system are visibly present and compatible.
8. **Negative constraints** — No forbidden layout, literal scene, cliché combination, disconnected halo field, dense information design, floating UI card, inactive palette color, or competing ornament is present.

If semantic fidelity fails, return to title selection and replace `FINAL_TITLE` before generating again. If rendered text, ratio, composition, color, typography, or a forbidden visual element fails, discard the version and use `REGENERATE`. Do not ask an image edit to repair incorrect text. A file-format mismatch or exact-size-only mismatch may be normalized deterministically only when the aspect ratio and composition are already correct; reverify after normalization.

Run the deterministic check from the skill directory, substituting the selected preset:

```text
python3 scripts/verify_image.py <image> --width <W> --height <H> --ratio <W:H> --format PNG
```

Use `JPEG` only when the user explicitly requests JPEG output.

## Poster-integration gate

Run this gate only after hard compliance passes. Judge the cover as a designed whole rather than as separate ingredients.

1. **Unified composition** — The result reads as one poster, not typography placed over a generic gradient background.
2. **Title–form relationship** — The title and primary form share at least one legible structural relationship: edge, axis, baseline, tangent, overlap, counter-shape, or continuous color flow.
3. **Defined negative space** — Quiet space is shaped by color movement, cropping, alignment, or geometric tension. It does not read as an unfinished empty region.
4. **Visual balance** — The title, brightest transition, primary form, and small details create a deliberate center of gravity without dead corners or one-sided weight.
5. **Structural decoration** — The anchor establishes one quiet secondary focus, the optional bridge connects major regions, and the one or two echoes repeat the anchor language along a shared alignment. They do not float randomly.
6. **Thumbnail clarity** — At approximately 25%, the title is immediately readable, remains dominant, and does not merge with a bright edge or noisy texture.
7. **Template-resistance** — The cover avoids generic AI-poster shorthand such as a planet, orbit, sparkle, centered slogan, or three radial blooms assembled without a content-specific relationship.
8. **Background structure test** — Mentally hide the three text elements. The remaining color field and geometry must still show intentional direction, balance, and spatial structure. They need not work as standalone art, but they cannot collapse into unrelated light spots, a stock gradient, or an empty canvas.
9. **Reference-family fit** — The result shares the reference's seamless atmosphere, editorial restraint, grain character, and abstract futuristic fullness without copying one card literally.
10. **Recipe fidelity** — The actual palette family, active hue count, area hierarchy, gradient topology, primary form, title zone, type mode, pale-device state, and detail roles form the one selected recipe. The result differs from recent covers in coordinated composition, not only in hue.
11. **Pale-device quality** — When selected, the panel reads as an atmospheric editorial plane rather than a floating UI card, uses an active-hue tint, contains only its locked support-text role, and shapes negative space. When not selected, no accidental card appears.
12. **Color-count discipline** — `SINGLE_FAMILY` reads as one hue family with depth; `DUAL_FIELD` has a clear 70/30-like dominance; `SOFT_TRIAD` has clear 55/30/15-like hierarchy; `SPECTRAL_BLEND` reads as a continuous field rather than four separate blobs.

Treat items 1, 2, 6, 7, 8, 10, and 12 as critical. Any critical failure makes the aesthetic verdict `FAIL` regardless of other strengths. Do not use a vague total score or accept a result merely because most ingredients are present.

## Repair-mode decision

Name one highest-impact **root cause**, not a list of unrelated symptoms. One root cause may explain multiple visible effects; for example, “the composition lacks a shared diagonal structure” can explain both an undefined right side and a disconnected title.

Choose `EDIT` only when all of these are true:

- hard compliance passes;
- the composition's main hierarchy and geometry already work;
- the failure is local and spatially isolatable;
- the change can preserve the approved text and successful regions.

Typical `EDIT` cases include one floating accent, a locally coarse grain patch, one weak color transition, an underdefined corner, or a single overstrong line.

Choose `REGENERATE` when the title and primary form are disconnected, the center of gravity is wrong, the canvas feels split, the background structure test fails, the result looks like a generic AI template, the palette or typography contract fails, or a correction would require moving several major regions. Structural failure is not a patching task.

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
- rerun the deterministic file check;
- revisit every hard and aesthetic item;
- compare locked invariants against the preceding approved state;
- inspect full size and thumbnail size;
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
