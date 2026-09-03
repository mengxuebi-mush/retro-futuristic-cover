# Photo treatment findings

## Scope and stop condition

The lane rendered exactly one initial proof for each controlled treatment and completed one review pass at full size and 25% thumbnail size. It then stopped without regeneration. The source fixture and all working derivatives remained outside the repository.

## Observations

- All four checked-in proofs are opaque RGB PNG files at exactly `1080 × 1440` and pass the repository image verifier.
- All four proofs render the exact three supplied strings and no additional designed copy. `DIGITAL MEDIA GALLERY` is the dominant title at full size and 25%.
- The continuous warm-ivory/blush/coral gradient fills every edge and corner. No proof uses a full rectangular photo field.
- Face, dark hair, light floral dress, and green palm foliage remain visible in each proof. The title and image share a diagonal mask, a common left axis, and treatment-specific overprint, scanline, or plate structure.
- A shared hard failure appears in every proof: the browser rasterized the source 90 degrees away from the SVG mask coordinate system. The face remains visible, but the hands-on-hips pose is not preserved as an upright portrait.
- `EXTRACTION_SCREENPRINT` visibly shares halftone and coral overprint language between title and image. Its coarse polygon extraction also retains unrelated source regions, so the foliage selection is only partial.
- `SIGNAL_SCAN` adds restrained registration offsets, horizontal scanlines, and one trace that follows the combined subject mass. At 25%, the scan vocabulary remains subordinate to the title.
- `COOL_STRUCTURAL_PLATE` introduces a limited cyan plate and grid that connect the title edge to the portrait mass. The cool layer remains localized rather than recoloring the whole poster.
- `FUTURIST_GLASSES` uses two transparent cyan-tinted lenses rather than an opaque visor. Because the face and overlay coordinates diverge after rotation, the glasses float over foliage and are not face-attached.

## Interpretation

- Portrait orientation and coordinate-system validation are upstream identity gates. If they fail, later judgments about face preservation, pose preservation, silhouette extraction, and face-attached accessories are invalid even when the person is still visually detectable.
- The shared title mask demonstrates a useful structural relationship: the title is not simply placed over an untouched photograph. Halftone, scanline, and cyan-plate treatments can extend through both type and image while maintaining title priority.
- Preserving source-local green foliage and the light dress against a warm poster palette is compatible with a continuous gradient when the photograph is extracted into selected fields rather than used as a rectangle.
- Transparent glasses are the correct first material direction, but face attachment requires landmark-derived coordinates or a validated normalized portrait transform. A manually positioned overlay is not reliable enough.

## Generator variance

- No generative model was used. The four proofs were produced by deterministic local SVG/CSS composition, so prompt or sampling variance is not applicable.
- The observed variance is renderer/asset-handling variance: the normalized PNG appeared upright in local inspection but entered the browser SVG rasterization with a conflicting orientation relative to the authored mask coordinates.
- Because every direction inherited the same renderer mismatch, differences among the four treatments should not be interpreted as treatment-ranking evidence.

## Reliability limits

- This is one source photo with one initial proof per direction and no repeated generations.
- The source orientation mismatch is a shared confounder and invalidates any claim that one treatment preserves portrait identity better than another.
- The extraction masks were hand-authored polygons, not semantic person/foliage masks; hair edges, arm contours, and leaf selection are therefore only approximate.
- No local glasses reference fixtures were available in this worktree or `/private/tmp`. The glasses proof tests only the brief's transparent-lens-first requirement, not fidelity to a supplied reference shape.
- Support copy is readable at full size but becomes marginal at 25%; the title hierarchy remains clear.

## Follow-up boundary

No shared skill, catalog, selector, or design-system change is proposed from this evidence. A future experimental budget should first assert upright pixel orientation, render a coordinate-registration test, and validate face/eye landmarks before applying any treatment. Only after that preflight passes should the same four controlled directions be repeated. Central wording changes still require repeated evidence across at least two controlled photos or two repeated generations.
