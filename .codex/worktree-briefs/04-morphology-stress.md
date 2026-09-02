# Worktree Brief — Speculative Morphology Stress Test

## Identity

- Branch: `exp/morphology-stress`
- Suggested worktree: `/Users/mengxueb/Desktop/Mushroom_projects/retro-cover-worktrees/morphology-stress`
- Baseline: `next @ e6366d2`
- First read: `.codex/worktree-briefs/00-integration-contract.md`, then the worktree-local `SKILL.md`, `design-system/speculative-morphologies.json`, `design-system/objects.json`, and `references/visual-system.md`.

## Objective

Test whether the open morphology contract can produce several genuinely different, content-derived retro-future objects with understandable hypothetical functions—without forcing every idea into the four optional archetypes or collapsing into a contemporary EV, modern consumer device, cold minimal architecture, or a generic ceramic blob.

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
- Derive four distinct hypothetical functions from the event theme—for example collaborative prototyping, prompt exchange, rapid model review, or quiet pair-building—while keeping the event copy identical.
- Lock palette, topology, treatment, scale role, focal event, type mode, copy, and support placement.

Create four `CUSTOM_COMPOSED` morphology files conforming to `design-system/custom-morphology.schema.json`. Derive each morphology from its function before naming the visible object. The four silhouettes must remain clearly distinct at thumbnail size and at least two must not reduce to a bubble, teardrop/pod, joined biomorphic blob, or soft vertical monolith. Use 2–4 purpose-bearing parts and record them before generation.

Do not begin by assigning one of the four catalog archetypes. After generation, compare each result to those archetypes and record whether the image model collapsed the custom specification back into one of them.

## Visual questions

For every output, inspect:

- Can the morphology be identified from silhouette alone?
- Is one proportion visibly exaggerated?
- Is there an integrated rounded canopy or aperture?
- Do secondary parts follow the dominant curvature?
- Can the hypothetical function be inferred without labels?
- Does the object visibly follow its own declared shape ancestry instead of defaulting to the nearest catalog archetype?
- Are at least two custom silhouettes meaningfully outside the four optional archetype families?
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

1. Four selected PNG proofs, one per custom morphology.
2. One selector manifest JSON per proof.
3. One short subject specification per case: function, object family, morphology, exaggerated proportion, aperture, purpose-bearing parts, materials, and explicit modern cues rejected.
4. `results.json` compatible with the visual verdict schema when available. If that branch has not yet merged, preserve the same information in a clearly structured provisional format.
5. `findings.md` naming repeated failures, custom-morphology failures, and any archetype-collapse patterns without proposing exact grammar wording.

## Stop condition

Use one initial generation and at most one retry per morphology. Stop after four reviewed cases. Do not tune prompts until every image looks attractive; the goal is to test whether the open contract preserves imaginative shape diversity.

## Final prompt to the integration owner

Separate failures caused by custom morphology definitions from failures caused by the object family, generator variance, composition, or palette. Recommend a contract change only when the same failure class appears in at least two cases.
