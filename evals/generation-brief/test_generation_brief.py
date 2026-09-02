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


def compile_content(content: dict, manifest: dict, *, expect: int = 0) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory(prefix="generation-brief-content-") as directory:
        directory_path = Path(directory)
        manifest_path = directory_path / "manifest.json"
        content_path = directory_path / "content.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        content_path.write_text(json.dumps(content), encoding="utf-8")
        return run("python3", str(COMPILER), "--manifest", str(manifest_path), "--content", str(content_path), expect=expect)


def speculative_content() -> dict:
    return json.loads((FIXTURES / "speculative-object.json").read_text(encoding="utf-8"))


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


def test_custom_composed_morphology() -> None:
    manifest = select_manifest(
        "--carrier", "SOCIAL_COVER", "--layout-family", "ASYMMETRIC_COUNTERWEIGHT",
        "--subject-origin-mode", "SPECULATIVE_OBJECT", "--object-family", "FUTURE_HABITAT_CAPSULE",
        "--speculative-morphology", "CUSTOM_COMPOSED",
        "--custom-morphology-file", str(ROOT / "evals" / "fixtures" / "custom-composed-morphology.json"),
        "--subject-assembly", "SINGLE_OBJECT", "--render-treatment", "PALETTE_ASSIMILATED",
        "--scale-role", "INTEGRATED_HERO", "--screen-state", "NOT_APPLICABLE",
    )
    brief = compile_fixture("speculative-object.json", manifest)
    morphology = brief["subject"]["morphology"]
    assert morphology["id"] == "CUSTOM_COMPOSED"
    assert morphology["source"] == "CUSTOM"
    assert "toroidal ribbon" in morphology["shape_ancestry"]
    assert len(morphology["construction_cues"]) == 3
    assert "Orbit ribbon commons" in brief["generator_instruction"]


def test_compound_set_plan_reaches_prompt() -> None:
    manifest = select_manifest(
        "--carrier", "SOCIAL_COVER", "--layout-family", "ASYMMETRIC_COUNTERWEIGHT",
        "--subject-origin-mode", "SPECULATIVE_OBJECT", "--object-family", "FUTURE_MOBILITY_POD",
        "--speculative-morphology", "STREAMLINE_POD", "--subject-assembly", "COMPOUND_SET",
        "--render-treatment", "PALETTE_ASSIMILATED", "--scale-role", "INTEGRATED_HERO",
        "--screen-state", "NOT_APPLICABLE",
    )
    content = speculative_content()
    content["assembly_plan"] = {
        "mode": "COMPOUND_SET",
        "members": [
            {"role": "arrival chamber", "form_cue": "complete inflated chamber with a broad aperture"},
            {"role": "signal tender", "form_cue": "complete hovering vessel with a forked tail"},
        ],
        "shared_relation": "both objects share one rising tangent and overlap shadows",
        "observability_rule": "two complete silhouettes remain countable at thumbnail size",
    }
    result = compile_content(content, manifest)
    brief = json.loads(result.stdout)
    instruction = brief["generator_instruction"]
    assert brief["composition"]["subject_assembly_count"] == manifest["subject_assembly_count"]
    assert brief["subject"]["assembly_plan"]["members"][1]["role"] == "signal tender"
    assert "arrival chamber" in instruction
    assert "signal tender" in instruction
    assert manifest["subject_mass_rule"] in instruction
    assert "internal parts do not count" in instruction
    assert any("Do not fuse" in item for item in brief["negative_constraints"])


def test_other_multi_object_plans_reach_prompt() -> None:
    cases = [
        (
            "PRIMARY_SATELLITES", "PERSPECTIVE_VECTOR",
            {
                "mode": "PRIMARY_SATELLITES",
                "primary": {"role": "navigation carrier", "form_cue": "complete winged oval carrier"},
                "satellites": [{"role": "route beacon", "form_cue": "complete luminous seed vessel"}],
                "shared_relation": "the beacon sits on the carrier's projected route",
                "min_visual_weight_ratio": 2,
                "observability_rule": "primary and beacon remain separately traceable at thumbnail size",
            },
            "navigation carrier",
        ),
        (
            "REPEATED_FAMILY", "RHYTHMIC_FIELD",
            {
                "mode": "REPEATED_FAMILY",
                "family_unit": {"role": "listening pod", "form_cue": "complete pear-shaped pod with one side opening"},
                "instance_count": 3,
                "path": "descending diagonal rhythm",
                "focal_instance_rule": "the lower-left pod is largest and active",
                "shared_relation": "all pods follow the same curvature and spacing interval",
                "observability_rule": "three pods remain countable at thumbnail size",
            },
            "listening pod",
        ),
    ]
    for assembly, layout, plan, marker in cases:
        scale_role = "REPEATED_FIELD" if assembly == "REPEATED_FAMILY" else "INTEGRATED_HERO"
        manifest = select_manifest(
            "--carrier", "SOCIAL_COVER", "--layout-family", layout,
            "--subject-origin-mode", "SPECULATIVE_OBJECT", "--object-family", "FUTURE_MOBILITY_POD",
            "--speculative-morphology", "STREAMLINE_POD", "--subject-assembly", assembly,
            "--render-treatment", "PALETTE_ASSIMILATED", "--scale-role", scale_role,
            "--screen-state", "NOT_APPLICABLE",
        )
        content = speculative_content()
        content["assembly_plan"] = plan
        brief = json.loads(compile_content(content, manifest).stdout)
        assert marker in brief["generator_instruction"]
        assert brief["subject"]["assembly_plan"]["mode"] == assembly


def test_assembly_plan_contract_rejects_ambiguous_inputs() -> None:
    manifest = select_manifest(
        "--carrier", "SOCIAL_COVER", "--layout-family", "ASYMMETRIC_COUNTERWEIGHT",
        "--subject-origin-mode", "SPECULATIVE_OBJECT", "--object-family", "FUTURE_MOBILITY_POD",
        "--speculative-morphology", "STREAMLINE_POD", "--subject-assembly", "COMPOUND_SET",
        "--render-treatment", "PALETTE_ASSIMILATED", "--scale-role", "INTEGRATED_HERO",
        "--screen-state", "NOT_APPLICABLE",
    )
    result = compile_content(speculative_content(), manifest, expect=2)
    assert "assembly_plan: required" in result.stderr

    content = speculative_content()
    content["assembly_plan"] = {
        "mode": "COMPOUND_SET",
        "members": [
            {"role": "pod", "form_cue": "complete oval vessel"},
            {"role": "POD", "form_cue": "complete folded vessel"},
        ],
        "shared_relation": "shared diagonal",
        "observability_rule": "both remain countable",
    }
    result = compile_content(content, manifest, expect=2)
    assert "duplicate designed string" in result.stderr

    single_manifest = select_manifest(
        "--carrier", "SOCIAL_COVER", "--layout-family", "ASYMMETRIC_COUNTERWEIGHT",
        "--subject-origin-mode", "SPECULATIVE_OBJECT", "--object-family", "FUTURE_MOBILITY_POD",
        "--speculative-morphology", "STREAMLINE_POD", "--subject-assembly", "SINGLE_OBJECT",
        "--render-treatment", "PALETTE_ASSIMILATED", "--scale-role", "INTEGRATED_HERO",
        "--screen-state", "NOT_APPLICABLE",
    )
    content["assembly_plan"]["members"][1]["role"] = "companion pod"
    result = compile_content(content, single_manifest, expect=2)
    assert "must be omitted for SINGLE_OBJECT" in result.stderr


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
        test_custom_composed_morphology,
        test_compound_set_plan_reaches_prompt,
        test_other_multi_object_plans_reach_prompt,
        test_assembly_plan_contract_rejects_ambiguous_inputs,
        test_invalid_inputs_are_rejected,
    ):
        test()
    print("PASS: 9 generation-brief fixture groups")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
