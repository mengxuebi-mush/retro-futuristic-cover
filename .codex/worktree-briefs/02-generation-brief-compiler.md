# Worktree Brief — Generation Brief Compiler

## Identity

- Branch: `feat/generation-brief`
- Suggested worktree: `/Users/mengxueb/Desktop/Mushroom_projects/retro-cover-worktrees/generation-brief`
- Baseline: `next @ e6366d2`
- First read: `.codex/worktree-briefs/00-integration-contract.md`, then the worktree-local `SKILL.md`, `design-system/manifest.schema.json`, and `scripts/select_design_recipe.py --help`.

## Objective

Build a deterministic compiler that converts locked content plus an existing selector manifest into a complete, reviewable image-generation brief. It should reduce omitted requirements and contradictory prompt instructions without making aesthetic decisions that belong to the selector or the agent.

The compiler consumes resolved decisions; it does not choose a layout, palette, object, morphology, or title.

## Proposed interface

Implement:

```text
scripts/compile_generation_brief.py
```

Suggested usage:

```bash
python3 scripts/compile_generation_brief.py \
  --manifest /path/to/manifest.json \
  --content /path/to/content.json
```

Output one JSON object to stdout. It should include at minimum:

- canvas and carrier contract;
- exact designed-text inventory and count;
- composition sentence, title zone, object slot, support zones, collision rule, crop rule, and release zone;
- subject origin, assembly, function or archive anchors, treatment, scale, object family, morphology, and screen state when applicable;
- palette, active hues, area hierarchy, topology, type mode, focal event, and details;
- the opaque full-bleed background requirement;
- explicit negative constraints relevant to the resolved combination;
- a concise generator-ready instruction assembled only from the structured fields.

Do not include unused catalog options, rejected candidates, internal chain-of-thought, or a full article.

## Input contract

Create a small schema or validator for `content.json`. It must distinguish:

- `THREE_ELEMENT_COVER` from `EDITORIAL_POSTER_5_TO_7`;
- exact title, category, deck or micro-subtitle;
- 0 or 2–4 factual poster support elements;
- optional speculative function and purpose-bearing parts;
- optional archive identity anchors and intrinsic-text policy;
- optional exact screen carrier element already present in the designed-text inventory.

Reject, rather than silently repair:

- text counts outside the carrier contract;
- duplicate designed strings;
- a `CARRIER` screen element repeated externally;
- speculative objects without a function;
- archive artifacts paired with `PALETTE_ASSIMILATED`;
- manifests missing required fields;
- any brief that omits the full-canvas opaque background requirement.

## Owned files

- `scripts/compile_generation_brief.py`
- `scripts/validate_generation_brief.py` if a separate validator is useful
- `design-system/generation-content.schema.json`
- `design-system/generation-brief.schema.json`
- `evals/generation-brief/**`

Do not add files that are not needed by the implementation.

## Forbidden files

- `SKILL.md`
- `references/**`
- existing visual catalogs
- `scripts/select_design_recipe.py`
- `evals/evals.json`

## Required tests

Include focused fixtures for:

1. three-element abstract cover;
2. editorial archive computer with `SIGNAL` screen;
3. editorial archive computer with `CARRIER` screen and no external duplicate;
4. speculative object with function and morphology;
5. missing background clause — must fail;
6. duplicate screen copy — must fail;
7. invalid poster text count — must fail.

Tests should validate observable fields and invariants, not exact prose formatting.

Also run:

```bash
python3 scripts/validate_catalog_v2.py
python3 scripts/validate_evals_v2.py
python3 scripts/verify_examples.py
```

## Stop condition

Stop when the compiler and focused tests pass for the defined fixtures. Do not update `SKILL.md` to invoke the compiler in this branch; integration will decide how and where to route to it.

## Final prompt to the integration owner

Explain which omissions the compiler prevents, which decisions intentionally remain with the selector or agent, and the smallest `SKILL.md` change needed to route future generations through it.
