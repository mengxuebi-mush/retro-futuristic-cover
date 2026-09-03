# Custom Composition Stress Findings

## Scope

One `CUSTOM_COMPOSED` toroidal ribbon commons object was tested across four editorial-poster Composition Contracts. Carrier, seven-string copy inventory, `SINGLE_OBJECT` assembly, function, object family, morphology, `PALETTE_ASSIMILATED` treatment, `INTEGRATED_HERO` scale role, `P01_POWDER_SIGNAL` active hues, `EDGE_BLOOM` topology, `SINGLE_SCALE_ANOMALY` focal event, `CJK_SOFT_HUMANIST` type mode, and `NOT_APPLICABLE` screen state were locked. Each case used one initial generation and zero retries.

## Observed evidence

- All four outputs are opaque RGB PNGs at `1080 × 1440` and `3:4`; all four corners and the full perimeter are covered by the continuous powder-sky/warm-ivory field.
- All four retain the same recognizable morphology: one continuous toroidal ribbon, large open center, suspended cabin, convex cabin window, docking bridges, and curved maintenance seam.
- All four preserve the exact seven designed strings once each. No extra readable poster copy or intrinsic screen text was observed.
- At full size and 25% thumbnails, `VIBE CODING WORKSHOP` is the first reading event in all four cases.
- All four keep the subject as one coherent mass and preserve one visibly quieter release zone.

## Contract-driven differences

| Contract | Repeatable spatial behavior |
|---|---|
| `ASYMMETRIC_COUNTERWEIGHT` | Large loop is biased to the upper-right and cropped at the top/right edges; title occupies the lower-left counter-space; the shared curved tangent makes the relationship structural. |
| `CENTERED_ANCHOR` | Loop is centered beneath the title and grounded on a horizontal baseline; the title remains larger, while the offset field and non-symmetric title block prevent a generic centered template. |
| `PERSPECTIVE_VECTOR` | A single lower-left → upper-right diagonal carries title, support rail, and subject; the loop crops into the vector and the open horizon becomes the release zone. |
| `TYPE_DOMINANT_FIELD` | Three-line title owns most of the left field; the loop is reduced to a lower-right counterweight while its open center and cabin remain identifiable. |

These differences are structural changes in title footprint, subject slot, crop/scale, relationship axis, support attachment, and release-zone position. They are not only coordinate translations: the same object is respectively cropped as a counterweight, centered as an anchored specimen, carried by a diagonal vector, and reduced to a typographic interruption.

## Generator variance

- Exact line wrapping and optical spacing vary slightly between outputs, while the seven strings remain legible and unique.
- Surface highlights, haze placement, cabin interior detail, and the apparent thickness of the loop vary between generations.
- The initial image service returned `1086 × 1448` RGB PNGs; each was resized proportionally to the required `1080 × 1440` delivery canvas. This is delivery normalization, not a composition failure.
- No hard-error retry was required, so there is no repeated failure class to report.

## Interpretation

The controlled comparison supports the claim that Composition Contract changes are visible and meaningful for this custom morphology. The contract determines the spatial logic while generator variance mainly affects surface and typographic micro-detail. `TYPE_DOMINANT_FIELD` communicates title priority most strongly but makes the functional object less central; `PERSPECTIVE_VECTOR` preserves a strong directional read at the cost of slightly quieter support copy at thumbnail scale. No grammar change is proposed from this single comparison.

## Validation

- `python3 scripts/validate_generation_brief.py --manifest ...`: four passes.
- `python3 scripts/validate_generation_brief.py --brief ...`: four passes.
- `python3 scripts/validate_visual_verdicts.py evals/visual/custom-composition-stress/verdicts`: four passes, zero artwork failures, zero invalid documents.
