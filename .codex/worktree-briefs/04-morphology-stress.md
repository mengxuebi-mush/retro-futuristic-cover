# Worktree Brief — Speculative Morphology Stress Test

## Identity

- Branch: `exp/morphology-stress`
- Suggested worktree: `/Users/mengxueb/Desktop/Mushroom_projects/retro-cover-worktrees/morphology-stress`
- Baseline: `next @ e6366d2`
- First read: `.codex/worktree-briefs/00-integration-contract.md`, then the worktree-local `SKILL.md`, `design-system/speculative-morphologies.json`, `design-system/objects.json`, and `references/visual-system.md`.

## Objective

Test whether all four speculative morphology families reliably produce warm, rounded, exaggerated retro-future objects with an understandable hypothetical function—without collapsing into a contemporary EV, modern consumer device, cold minimal architecture, or a generic ceramic blob.

This is an evidence task. Do not change morphology rules or object catalogs.

## Controlled test

Use the same fictional event and composition for every case:

- Carrier: `EDITORIAL_POSTER`, 3:4, 1080 × 1440 PNG.
- Exact title: `VIBE CODING WORKSHOP`.
- Category: `BUILD`.
- Deck: `PROMPT. PROTOTYPE. SHIP.`
- Reuse the same four factual support elements from the composition-isolation brief.
- Layout: select one compatible layout and lock it across all four tests.
- Subject assembly: `SINGLE_OBJECT`.
- Subject origin: `SPECULATIVE_OBJECT`.
- Hypothetical function: a friendly mobile or airborne workspace for collaborative prototyping.
- Lock palette, topology, treatment, scale role, focal event, type mode, copy, and support placement.

Vary only `SPECULATIVE_MORPHOLOGY`:

1. `BUBBLE_CAPSULE`
2. `STREAMLINE_POD`
3. `BIOMORPHIC_APPARATUS`
4. `SOFT_VERTICAL_INFRASTRUCTURE`

Choose a compatible object family for each morphology. Preserve one shared function, but allow purpose-bearing parts to adapt to the morphology. Use 2–4 functional parts and record them before generation.

## Visual questions

For every output, inspect:

- Can the morphology be identified from silhouette alone?
- Is one proportion visibly exaggerated?
- Is there an integrated rounded canopy or aperture?
- Do secondary parts follow the dominant curvature?
- Can the hypothetical function be inferred without labels?
- Does the object feel designed from sphere, ovoid, teardrop, inflated spindle, biomorphic shell, or soft monolith ancestry?
- Does it avoid present-day automotive, appliance, phone, EV, supercar, and touchscreen-first cues?
- Does it avoid cold gray-white minimalism and generic matte ceramic form?
- Are warm material cues present: enamel, fiberglass, lacquer, resin, bubble glass, warm metal, or upholstery?
- Does the title remain the first reading event despite a large object?
- Is the background fully opaque and continuous across the canvas?

Record recognition, compliance, and preference separately.

## Owned files

- `evals/visual/morphology-stress/**`
- `examples/v3-tests/morphology-stress/**`

Keep raw and rejected generations outside the repository.

## Forbidden files

- `SKILL.md`
- `references/**`
- `design-system/**`
- `scripts/**`
- `evals/evals.json`

## Deliverables

1. Four selected PNG proofs, one per morphology.
2. One selector manifest JSON per proof.
3. One short subject specification per case: function, object family, morphology, exaggerated proportion, aperture, purpose-bearing parts, materials, and explicit modern cues rejected.
4. `results.json` compatible with the visual verdict schema when available. If that branch has not yet merged, preserve the same information in a clearly structured provisional format.
5. `findings.md` naming repeated failures and morphology-specific failures without proposing exact grammar wording.

## Stop condition

Use one initial generation and at most one retry per morphology. Stop after four reviewed cases. Do not tune prompts until every image looks attractive; the goal is to expose how much guidance each morphology needs.

## Final prompt to the integration owner

Separate failures caused by morphology definitions from failures caused by the object family, generator variance, composition, or palette. Recommend a catalog change only when the same failure class appears in at least two cases.
