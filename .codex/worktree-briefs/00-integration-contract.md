# Parallel Worktree Integration Contract

Use this contract for every V2/V3 optimization worktree in this repository.

## Frozen baseline

- Repository: `/Users/mengxueb/Desktop/Mushroom_projects/retro-futuristic-cover`
- Integration branch: `next`
- Baseline commit: `e6366d2`
- Stable branch: `main` — do not modify or merge into it.
- Every worktree must use the `SKILL.md` inside that worktree. Do not edit through the installed symlink at `~/.agents/skills/retro-futuristic-cover`.

Before working, verify:

```bash
git branch --show-current
git rev-parse --short HEAD
git status --short
```

Stop if the branch name is wrong, the baseline is not descended from `e6366d2`, or the worktree contains unexplained changes.

## Shared operating rules

1. Work only inside the assigned worktree and its declared owned files.
2. Do not edit `SKILL.md`, `design-system/layouts.json`, `design-system/composition-grammar.json`, `design-system/objects.json`, `design-system/speculative-morphologies.json`, or `references/visual-system.md` unless the lane explicitly owns that file.
3. Evidence lanes diagnose behavior; they do not rewrite design rules. Record a finding even when the result is good.
4. Keep generated raw artifacts in an isolated temporary directory. Commit only selected proofs and compact machine-readable findings required by the brief.
5. Do not convert one attractive or failed image into a universal rule. A proposed grammar change needs the same failure class in at least two controlled comparisons.
6. Preserve user-supplied wording and event facts. Never invent facts solely to make an experiment look realistic.
7. Do not merge, rebase, push, or modify `next`. Finish with one or more focused commits on the assigned branch.
8. If the task reveals a necessary edit outside owned files, describe it in the handoff instead of making it.

## Required handoff

Every lane must finish with:

- branch name and final commit SHA;
- files changed;
- commands run and their results;
- observed evidence, separated from interpretation;
- proposed follow-up changes, if any;
- unresolved risks or decisions;
- a clean `git status --short`.

## Repository-wide validation

Run these when the lane touches a shared catalog, selector behavior, evals, or checked-in proof images:

```bash
python3 scripts/validate_catalog_v2.py
python3 scripts/validate_evals_v2.py
python3 scripts/verify_examples.py
```

New deterministic scripts require focused tests in addition to the repository-wide validation.

## Integration order

The integration owner reviews and merges branches into `next` in this order:

1. `feat/visual-verdicts`
2. `feat/generation-brief`
3. evidence from `exp/composition-isolation`
4. evidence from `exp/morphology-stress`
5. one centralized grammar update based on repeated evidence

The integration owner, not the evidence lanes, resolves final changes to `SKILL.md` and the visual catalogs.
