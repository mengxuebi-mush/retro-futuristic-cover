#!/usr/bin/env python3
"""Run selector regression cases for the V3 visual grammar layer."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals" / "evals.json"
MANIFEST_SCHEMA = ROOT / "design-system" / "manifest.schema.json"
SELECTOR = ROOT / "scripts" / "select_design_recipe.py"
if not SELECTOR.exists():
    SELECTOR = ROOT / "selector-work" / "select_design_recipe.py"


def main() -> int:
    payload = json.loads(EVALS.read_text(encoding="utf-8"))
    manifest_schema = json.loads(MANIFEST_SCHEMA.read_text(encoding="utf-8"))
    required_manifest_fields = set(manifest_schema["required"])
    failures: list[str] = []
    for index, case in enumerate(payload["evals"], start=1):
        command = ["python3", "-B", str(SELECTOR), "--no-state", "--seed", str(index * 17), *case["args"]]
        result = subprocess.run(command, text=True, capture_output=True)
        if case.get("expect_failure"):
            if result.returncode == 0:
                failures.append(f"{case['id']}: selector unexpectedly accepted an incompatible combination")
            continue
        if result.returncode != 0:
            failures.append(f"{case['id']}: selector failed: {result.stderr.strip()}")
            continue
        recipe = json.loads(result.stdout)
        missing_manifest_fields = sorted(required_manifest_fields - set(recipe))
        if missing_manifest_fields:
            failures.append(f"{case['id']}: selector omitted required manifest fields {missing_manifest_fields}")
        expected = case["expected"]
        for key, value in expected.items():
            if key == "hero_object_id":
                actual = recipe.get("hero_object", {})
                actual = actual.get("id") if isinstance(actual, dict) else actual
                if actual != value:
                    failures.append(f"{case['id']}: hero_object.id expected {value!r}, got {actual!r}")
                continue
            if key.endswith("_not"):
                actual_key = key.removesuffix("_not")
                if recipe.get(actual_key) == value:
                    failures.append(f"{case['id']}: {actual_key} unexpectedly equals {value}")
            elif recipe.get(key) != value:
                failures.append(f"{case['id']}: {key} expected {value!r}, got {recipe.get(key)!r}")
        for key, fragment in case.get("expected_contains", {}).items():
            actual = recipe.get(key, "")
            if fragment not in actual:
                failures.append(f"{case['id']}: {key} does not contain {fragment!r}")

    if failures:
        print("FAIL: selector evals")
        print("\n".join(failures))
        return 1
    print(f"PASS: {len(payload['evals'])} selector eval cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
