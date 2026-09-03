# Subject Assembly Stress Test

## Scope and method

This experiment tests whether the Toroidal Ribbon Commons can behave as a modular collaborative prototyping system across four `SUBJECT_ASSEMBLY` modes without becoming several competing hero objects. The content, speculative origin, object family, function, material language, `P03_PISTACHIO_FUTURE` palette, warm-ivory + pale-pistachio active hues, neutral-grotesk typography mode, and `DIAGONAL_DRIFT` topology are locked across all four cases.

`single-object-control`, `compound-set`, and `primary-satellites` are strict assembly-isolation cases under `ASYMMETRIC_COUNTERWEIGHT + INTEGRATED_HERO`. `repeated-family` is an assembly × required-layout compatibility test under `RHYTHMIC_FIELD + REPEATED_FIELD`; it is not a fully isolated layout comparison.

Each case was independently selected, compiled, generated, verified, and judged. Every case received one initial generation. A retry was used only after a hard failure and reused the same compiled brief. Rejected raw outputs remain outside the repository; the retained PNG is the final evidence for each case.

## Observed facts

### `single-object-control` — PASS

- One complete loop, suspended shared cavity, two soft bridges, and curved seam read as one coherent subject.
- `COLLECTIVE TOOLS LAB` is the first reading event at full size and 25%.
- The title zone, left support axis, bottom support anchors, and quiet counter-space remain available.
- The retry removed the initial off-palette coral/apricot field.

### `compound-set` — REGENERATE / visual collapse

- The retained proof has a coherent outer mass, but it visually resolves as one loop with one suspended cabin.
- Two or three related module cores are not independently traceable, so the assembly is not distinguishable from `SINGLE_OBJECT` at first glance or at 25%.
- The title, all seven text strings, support anchors, release zone, background coverage, material family, and hue contract pass.
- The same assembly collapse occurred in the initial generation and the single permitted retry. The retry fixed the off-palette field but not the assembly.

### `primary-satellites` — PASS

- One dominant toroidal apparatus and one much smaller toroidal satellite are immediately distinguishable.
- The satellite inherits the ring curve, suspended cavity, soft connector logic, and material language.
- The primary is comfortably more than twice the satellite's visual weight; a shared baseline and shadow bind them into one system.
- The retry corrected the initial satellite's generic pod-like morphology and removed the off-palette field.

### `repeated-family` — PASS

- Three same-family instances follow a clear lower-left to upper-right rhythm, with one large focal instance and two smaller echoes.
- The scale variation prevents equal hero weight and the open upper-left title zone remains intact.
- The result reads as a rhythmic family rather than a retail grid, wallpaper pattern, or parallel product lineup.
- No retry was needed.

## Generator variance

- Three initial generations introduced an independent coral/apricot/orange field even though only warm ivory and pale pistachio were active. Their allowed retries removed that field. This is generator variance because the compiled color contract was unchanged.
- The initial `primary-satellites` image reduced the satellite to a generic rounded pod. The unchanged-brief retry produced a true miniaturized toroidal cavity, showing that this instance was generator variance rather than a stable assembly failure.
- The generated source images were 1086×1448, an exact 3:4 ratio with no alpha. They were deterministically and proportionally resampled to 1080×1440 without cropping; this is delivery normalization, not a retry.

## Interpretation

- `SINGLE_OBJECT` is stable: the morphology produces a clear complete control subject without competing parts.
- `PRIMARY_SATELLITES` is stable after one allowed retry: explicit scale hierarchy plus a shared baseline/shadow preserves one `SUBJECT_MASS`.
- `REPEATED_FAMILY` is stable under its required `RHYTHMIC_FIELD`: repeated instances retain family identity, one focal scale, a coherent path, and an open title zone.
- `COMPOUND_SET` collapses: the generator satisfies unity by fusing the requested modules into a single-object silhouette, erasing the evidence needed to identify a compact compound assembly.
- No case produced multiple equal-weight hero objects. The failure mode is over-fusion, not competition.
- All four posters keep the title first, preserve the continuous full-bleed background, render the seven locked strings exactly once, and retain support/release structure.

## Grammar recommendation

The `COMPOUND_SET` collapse repeated in both its initial generation and unchanged-brief retry, so it meets the threshold for a grammar-change recommendation. A future grammar revision could require two or three independently traceable toroidal module cores inside the shared outer contour and add an explicit anti-collapse test: reject a result whose compound set can be described as one outer loop with one suspended cabin. This is a recommendation only; no grammar, reference, design-system, or script file was modified in this experiment.

## Verification record

- `python3 -B scripts/validate_catalog_v2.py` — PASS: 5 carriers, 8 layouts, 4 subject assemblies, 18 composition operators, 3 subject modes, 13 object families, 4 optional morphologies plus `CUSTOM_COMPOSED`, 4 screen states, and 6 focal events.
- `python3 -B scripts/validate_evals_v2.py` — PASS: 25 selector eval cases.
- `python3 -B evals/generation-brief/test_generation_brief.py` — PASS: 6 fixture groups.
- `python3 -B evals/visual/test_validate_visual_verdicts.py` — PASS: 9 tests.
- `python3 -B scripts/verify_examples.py` — PASS: 30 example and visual-proof images.
- Each verdict was also validated independently with `scripts/validate_visual_verdicts.py`: three passed artwork review; `compound-set` was correctly classified as one `ARTWORK_FAILURE`; all four were valid documents and none was `INVALID_INPUT`.
