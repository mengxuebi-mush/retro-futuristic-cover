# Worktree Brief — Photo Treatment

## Identity

- Branch: `exp/photo-treatment`
- Suggested worktree: `/Users/mengxueb/Desktop/Mushroom_projects/retro-cover-worktrees/photo-treatment`
- Baseline: `next @ dc04661`
- Related evidence: `exp/composition-isolation @ d0394d1`

## Objective

Determine whether supplied real photographs can be transformed into retro-futurist poster material by extracting important subject elements, preserving identity anchors, and integrating typography with the image treatment rather than placing text over an untouched rectangular photo.

This is an evidence task. Do not change the shared skill, visual catalogs, or selector behavior during the experiment.

## Controlled fixture

Use the supplied Digital Media Gallery photo fixture, converted only for tool compatibility to `/private/tmp/digital-media-gallery-source.png`. The source contains a woman in a light floral dress surrounded by dense green palm foliage and lanterns.

Keep these content requirements fixed:

- Carrier: `PHOTO_COVER`, 3:4, `1080 × 1440` PNG.
- Exact title: `DIGITAL MEDIA GALLERY`.
- Exact supporting labels: `ARCHIVE / SIGNAL / IMAGE CULTURE` and `FIELD NOTE 03`.
- Preserve the woman's recognizable face, hair, pose, light floral dress, and selected green foliage as identity or scene anchors.
- Preserve the skill's continuous gradient field, warm retro palette, halftone/overprint vocabulary, and readable title hierarchy.
- Do not invent event facts or add visible copy beyond the three supplied strings.

## Controlled treatment comparisons

Test one initial proof for each direction, holding the fixture, copy, carrier, palette family, gradient, and composition contract constant:

1. `EXTRACTION_SCREENPRINT`: subject and foliage separated into halftone/duotone printed layers; no full rectangular photo field.
2. `SIGNAL_SCAN`: extracted subject receives restrained scanline, registration, or data-trace structure that follows the silhouette and surrounding foliage.
3. `COOL_STRUCTURAL_PLATE`: extracted subject remains editorial while a limited cyan/blue structural plate, grid, or optical registration system adds the future-facing layer.
4. `FUTURIST_GLASSES`: add one face-attached futuristic glasses treatment. Test transparent or translucent lenses first; use opaque/tinted lenses only as a clearly labeled variant when the instruction calls for obscured eyes. The glasses must read as part of the subject treatment, not a sticker or generic full-face visor.

Use the supplied glasses reference images only as visual references for shape/material language. Do not reproduce their helmets, extra UI, or unrelated facial styling.

## Evaluation questions

Inspect each image at full size and approximately 25% thumbnail size:

- Is the person still recognizable after extraction or treatment?
- Are the retained foliage elements intentional and materially integrated?
- Is the source photo no longer doing all the compositional work as a rectangular field?
- Does the title share a treatment relationship with the image through texture, color plate, contour, masking, or overprint rather than behaving as an overlay?
- Does the retro-futurist signal come from the image system and structure, not from a decorative sci-fi prop alone?
- Is the gradient still continuous across the full canvas and perimeter?
- Are the exact three strings readable and free of extra generated copy?
- Does the result survive thumbnail scale without sacrificing face identity or title priority?

Record observations separately from interpretation. A visually attractive result is not by itself a reliability claim.

## Owned files

- `evals/visual/photo-treatment/**`
- `examples/v3-tests/photo-treatment/**`

Keep raw or rejected generations outside the repository. The source photo and reference images remain external fixtures.

## Forbidden files

- `SKILL.md`
- `references/**`
- `design-system/**`
- `scripts/select_design_recipe.py`
- `evals/evals.json`

## Deliverables

1. One selected PNG proof per treatment direction, or an explicit recorded incompatibility.
2. One compact manifest JSON per selected proof.
3. `results.json` with fixed variables, changed treatment variable, pass/fail fields, and thumbnail verdicts.
4. `findings.md` separating observations, interpretations, generator variance, and reliability limits.

## Stop condition

Stop after the four initial treatment proofs and one review pass. Do not keep regenerating to obtain a preferred aesthetic. If one direction fails, record the failure and continue the comparison with the remaining directions.

## Follow-up boundary

Repeated evidence across at least two controlled source photos or two repeated generations is required before proposing centralized wording changes to `SKILL.md` or the visual catalogs. The integration owner decides those changes.
