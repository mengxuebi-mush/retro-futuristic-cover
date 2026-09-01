#!/usr/bin/env python3
"""Focused observable-contract tests for the generation brief compiler."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
SELECTOR = ROOT / "scripts" / "select_design_recipe.py"
COMPILER = ROOT / "scripts" / "compile_generation_brief.py"
VALIDATOR = ROOT / "scripts" / "validate_generation_brief.py"


def run(*command: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != expect:
        raise AssertionError(f"unexpected exit {result.returncode} for {command}:\n{result.stderr}\n{result.stdout}")
    return result


def select_manifest(*args: str) -> dict:
    result = run("python3", str(SELECTOR), "--no-state", "--seed", "17", *args)
    return json.loads(result.stdout)


def compile_fixture(name: str, manifest: dict) -> dict:
    with tempfile.TemporaryDirectory(prefix="generation-brief-") as directory:
        manifest_path = Path(directory) / "manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        result = run("python3", str(COMPILER), "--manifest", str(manifest_path), "--content", str(FIXTURES / name))
        return json.loads(result.stdout)


def test_three_element_abstract() -> None:
    manifest = select_manifest(
        "--carrier", "SOCIAL_COVER", "--layout-family", "TYPE_DOMINANT_FIELD",
        "--subject-origin-mode", "ABSTRACT_FORM", "--subject-assembly", "SINGLE_OBJECT",
        "--focal-event", "NEGATIVE_SPACE_CUT",
    )
    brief = compile_fixture("abstract-cover.json", manifest)
    assert brief["text_contract"] == "THREE_ELEMENT_COVER"
    assert brief["designed_text_count"] == 3
    assert brief["subject"]["origin_mode"] == "ABSTRACT_FORM"
    assert brief["subject"]["screen_state"] == "NOT_APPLICABLE"
    assert brief["background"]["full_bleed_opaque"] is True


def test_archive_signal() -> None:
    manifest = select_manifest(
        "--carrier", "EDITORIAL_POSTER", "--layout-family", "ASYMMETRIC_COUNTERWEIGHT",
        "--subject-origin-mode", "ARCHIVE_ARTIFACT", "--object-family", "ARCHIVE_COMPUTING_DEVICE",
        "--subject-assembly", "SINGLE_OBJECT", "--render-treatment", "ENVIRONMENT_GRADED",
        "--scale-role", "MONUMENTAL_FRAGMENT", "--screen-state", "SIGNAL",
        "--focal-event", "DECISIVE_EDGE_CROP",
    )
    brief = compile_fixture("archive-computer-signal.json", manifest)
    assert brief["designed_text_count"] == 5
    assert brief["subject"]["object_family_id"] == "ARCHIVE_COMPUTING_DEVICE"
    assert brief["subject"]["screen_state"] == "SIGNAL"
    assert brief["subject"]["screen_copy_element"] == "NONE"
    assert len(brief["subject"]["archive_identity_anchors"]) == 3
    assert "No readable" in " ".join(brief["negative_constraints"])


def test_archive_carrier_has_no_external_duplicate() -> None:
    manifest = select_manifest(
        "--carrier", "EDITORIAL_POSTER", "--layout-family", "INFORMATION_AXIS",
        "--subject-origin-mode", "ARCHIVE_ARTIFACT", "--object-family", "ARCHIVE_COMPUTING_DEVICE",
        "--subject-assembly", "SINGLE_OBJECT", "--render-treatment", "ENVIRONMENT_GRADED",
        "--scale-role", "CENTERPIECE_ARTIFACT", "--screen-state", "CARRIER",
        "--screen-copy-element", "RSVP · BUILDERS-SD.EXAMPLE",
        "--focal-event", "TITLE_CONTOUR_TENSION",
    )
    brief = compile_fixture("archive-computer-carrier.json", manifest)
    carrier_items = [item for item in brief["designed_text_inventory"] if item["text"] == "RSVP · BUILDERS-SD.EXAMPLE"]
    assert len(carrier_items) == 1
    assert carrier_items[0]["placement"] == "SCREEN_CARRIER"
    assert brief["subject"]["screen_copy_element"] == "RSVP · BUILDERS-SD.EXAMPLE"
    assert brief["designed_text_count"] == 5


def test_speculative_function_and_morphology() -> None:
    manifest = select_manifest(
        "--carrier", "SOCIAL_COVER", "--layout-family", "FRAME_THRESHOLD",
        "--subject-origin-mode", "SPECULATIVE_OBJECT", "--object-family", "FUTURE_MOBILITY_POD",
        "--speculative-morphology", "STREAMLINE_POD", "--subject-assembly", "SINGLE_OBJECT",
        "--render-treatment", "PALETTE_ASSIMILATED", "--scale-role", "INTEGRATED_HERO",
        "--screen-state", "NOT_APPLICABLE", "--focal-event", "PORTAL_ENTRY",
    )
    brief = compile_fixture("speculative-object.json", manifest)
    assert brief["subject"]["function"].startswith("A shared")
    assert brief["subject"]["morphology"]["id"] == "STREAMLINE_POD"
    assert len(brief["subject"]["purpose_bearing_parts"]) == 3


def test_invalid_inputs_are_rejected() -> None:
    carrier_manifest = select_manifest(
        "--carrier", "EDITORIAL_POSTER", "--layout-family", "INFORMATION_AXIS",
        "--subject-origin-mode", "ARCHIVE_ARTIFACT", "--object-family", "ARCHIVE_COMPUTING_DEVICE",
        "--subject-assembly", "SINGLE_OBJECT", "--render-treatment", "ENVIRONMENT_GRADED",
        "--scale-role", "CENTERPIECE_ARTIFACT", "--screen-state", "CARRIER",
        "--screen-copy-element", "RSVP · BUILDERS-SD.EXAMPLE",
        "--focal-event", "TITLE_CONTOUR_TENSION",
    )
    with tempfile.TemporaryDirectory(prefix="generation-brief-invalid-") as directory:
        directory_path = Path(directory)
        manifest_path = directory_path / "manifest.json"
        manifest_path.write_text(json.dumps(carrier_manifest), encoding="utf-8")

        duplicate = json.loads((FIXTURES / "archive-computer-carrier.json").read_text(encoding="utf-8"))
        duplicate["poster_support_elements"].append({"text": duplicate["screen_carrier_element"], "factual": True})
        duplicate_path = directory_path / "duplicate.json"
        duplicate_path.write_text(json.dumps(duplicate), encoding="utf-8")
        result = run("python3", str(COMPILER), "--manifest", str(manifest_path), "--content", str(duplicate_path), expect=2)
        assert "duplicate designed string" in result.stderr

        invalid_count = json.loads((FIXTURES / "archive-computer-carrier.json").read_text(encoding="utf-8"))
        invalid_count["poster_support_elements"] = invalid_count["poster_support_elements"][:1]
        invalid_count_path = directory_path / "invalid-count.json"
        invalid_count_path.write_text(json.dumps(invalid_count), encoding="utf-8")
        result = run("python3", str(COMPILER), "--manifest", str(manifest_path), "--content", str(invalid_count_path), expect=2)
        assert "requires 2–4" in result.stderr

        valid = compile_fixture("archive-computer-carrier.json", carrier_manifest)
        valid.pop("background")
        missing_background_path = directory_path / "missing-background.json"
        missing_background_path.write_text(json.dumps(valid), encoding="utf-8")
        result = run("python3", str(VALIDATOR), "--brief", str(missing_background_path), expect=2)
        assert "background" in result.stderr


def main() -> int:
    for test in (
        test_three_element_abstract,
        test_archive_signal,
        test_archive_carrier_has_no_external_duplicate,
        test_speculative_function_and_morphology,
        test_invalid_inputs_are_rejected,
    ):
        test()
    print("PASS: 5 generation-brief fixture groups")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
