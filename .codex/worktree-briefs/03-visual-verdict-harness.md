# Worktree Brief — Visual Verdict Harness

## Identity

- Branch: `feat/visual-verdicts`
- Suggested worktree: `/Users/mengxueb/Desktop/Mushroom_projects/retro-cover-worktrees/visual-verdicts`
- Baseline: `next @ e6366d2`
- First read: `.codex/worktree-briefs/00-integration-contract.md`, then the worktree-local `SKILL.md`, `references/self-critique.md`, and `scripts/verify_image.py`.

## Objective

Create a structured verdict format and deterministic validation harness for visual proofs. Separate machine-verifiable delivery checks, observed visual facts, and subjective preference so future experiments can be compared consistently.

Do not attempt to automate aesthetic judgment with pixel heuristics. The harness validates the completeness and consistency of a human or vision-agent verdict.

## Verdict model

Each verdict must record:

- proof path, manifest path, carrier, canvas, and layout family;
- machine checks: file exists, PNG, dimensions, ratio, opacity;
- full-size review and 25% thumbnail review;
- background coverage across four corners and complete perimeter;
- exact designed-text inventory and duplicate/extra-text observation;
- first reading event;
- title, subject, and support hierarchy;
- subject-origin recognition;
- subject-mass unity for multi-object assemblies;
- release-zone visibility;
- support-copy structural attachment;
- screen-state compliance when applicable;
- layout failure signals observed;
- hard verdict: `PASS`, `EDIT`, `REGENERATE`, or `INVALID_INPUT`;
- one highest-impact root-cause class;
- aesthetic preference recorded separately from compliance.

Use controlled enums where useful, but allow concise evidence notes. A verdict cannot be `PASS` when a hard check fails.

## Owned files

- `evals/visual/schema.json`
- `evals/visual/fixtures/**`
- `scripts/validate_visual_verdicts.py`
- focused tests for the validator

The composition and morphology evidence branches will add their own subdirectories under `evals/visual/`; avoid filenames that collide with them.

## Forbidden files

- `SKILL.md`
- `references/self-critique.md`
- `design-system/**`
- `scripts/select_design_recipe.py`
- `evals/evals.json`

## Required fixtures

Create compact fixtures covering:

1. valid passing verdict;
2. transparent or missing-background failure;
3. correct machine delivery but title loses thumbnail hierarchy;
4. extra designed text;
5. `CARRIER` screen copy duplicated externally;
6. multi-object assembly that fails subject-mass unity;
7. invalid `PASS` despite a hard failure — validator must reject it.

Use placeholder image metadata or tiny local fixtures when possible. Do not generate visual art for this branch.

## Validation behavior

The validator should:

- accept one file or a directory of verdict JSON files;
- produce concise actionable failures;
- return nonzero when schema or logical consistency fails;
- distinguish a failed artwork verdict from an invalid verdict document;
- avoid judging whether an artwork is beautiful.

Run the focused tests plus:

```bash
python3 scripts/validate_catalog_v2.py
python3 scripts/validate_evals_v2.py
python3 scripts/verify_examples.py
```

## Stop condition

Stop when valid fixtures pass, invalid fixtures fail for the intended reason, and the output is usable by both composition and morphology evidence lanes. Do not add the new validator to CI in this branch; integration will do so after the evidence lanes adopt the schema.

## Final prompt to the integration owner

Identify which verdict fields are hard compliance, which require visual inspection, and which remain aesthetic preference. Flag any field that evidence workers could interpret inconsistently.
