# Worktree Brief — Composition Isolation

## Identity

- Branch: `exp/composition-isolation`
- Suggested worktree: `/Users/mengxueb/Desktop/Mushroom_projects/retro-cover-worktrees/composition-isolation`
- Baseline: `next @ e6366d2`
- First read: `.codex/worktree-briefs/00-integration-contract.md`, then the worktree-local `SKILL.md`.

## Objective

Determine whether the current Composition Contracts create meaningfully different, reusable poster structures when content, object, palette, typography direction, carrier, and copy are held constant.

This is an evidence task. Do not improve the grammar during the experiment.

## Controlled test

Use one fictional editorial event consistently across all outputs:

- Carrier: `EDITORIAL_POSTER`, 3:4, 1080 × 1440 PNG.
- Exact title: `VIBE CODING WORKSHOP`.
- Category: `BUILD`.
- Deck: `PROMPT. PROTOTYPE. SHIP.`
- Support elements:
  - `SAT • OCT 24 • 10 AM–1 PM`
  - `SIGNAL GARAGE • BARRIO LOGAN`
  - `HANDS-ON • LAPTOP REQUIRED`
  - `FREE • RSVP REQUIRED`
- Subject origin: `SPECULATIVE_OBJECT`.
- Hypothetical function: a friendly airborne workspace carrier for small-group prototyping.
- Object family and speculative morphology: lock one compatible pair for every test.
- Subject assembly: `SINGLE_OBJECT`.
- Render treatment, scale role, focal event, palette, gradient topology, and type mode: lock once and reuse.

Vary only the Composition Contract. Test four compatible layouts representing distinct spatial logic:

1. `ASYMMETRIC_COUNTERWEIGHT`
2. `CENTERED_ANCHOR`
3. `PERSPECTIVE_VECTOR`
4. `TYPE_DOMINANT_FIELD`

Use `python3 scripts/select_design_recipe.py --no-state` with explicit overrides. Save the selector output for every case. If one layout is incompatible with the locked assembly or subject, record the incompatibility and substitute the nearest compatible layout without editing the catalogs.

## Evaluation questions

Inspect each image at full size and approximately 25% size:

- Is the title unquestionably the first reading event?
- Is the object slot visibly different across layouts, rather than the same poster with shifted coordinates?
- Does the subject adapt to the layout without shrinking the title?
- Is one release zone clearly quieter than the rest?
- Do support elements attach to actual structure?
- Does the layout survive thumbnail scale?
- Does the full-bleed background cover all corners and the complete perimeter?
- Which failure signal, if any, from the selected layout is visible?

Do not score aesthetic preference as grammar correctness. Record both separately.

## Owned files

- `evals/visual/composition-isolation/**`
- `examples/v3-tests/composition-isolation/**`

You may create these directories. Keep raw or rejected generations outside the repository.

## Forbidden files

- `SKILL.md`
- `references/**`
- `design-system/**`
- `scripts/select_design_recipe.py`
- `evals/evals.json`

## Deliverables

1. Four selected PNG proofs, one per tested layout.
2. One selector manifest JSON per proof.
3. `results.json` containing fixed variables, changed variable, pass/fail fields, observed failure classes, and thumbnail verdict.
4. `findings.md` with:
   - observations shared by two or more tests;
   - layout-specific behavior;
   - suspected grammar gaps clearly labeled as hypotheses;
   - no proposed wording changes to `SKILL.md`.

## Stop condition

Stop after four controlled outputs and one review pass. Do not keep regenerating to obtain a preferred aesthetic. One initial generation plus at most one retry per case is enough to reveal whether the contract is legible.

## Final prompt to the integration owner

Report which differences were caused by the Composition Contract, which were generator variance, and which failure classes repeated in at least two cases.
