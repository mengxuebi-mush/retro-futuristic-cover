#!/usr/bin/env python3
"""Focused tests for the visual verdict harness."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "evals" / "visual" / "fixtures"
VALIDATOR = ROOT / "scripts" / "validate_visual_verdicts.py"
sys.path.insert(0, str(ROOT / "scripts"))
from validate_visual_verdicts import validate_document  # noqa: E402


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def typography_v2_document() -> dict:
    document = copy.deepcopy(load_fixture("valid-pass.json"))
    document["schema_version"] = 2
    document["visual_review"].update({
        "title_footprint": {"status": "PASS", "evidence": "The short title occupies the locked canvas envelope."},
        "title_weight_contrast": {"status": "PASS", "evidence": "The title uses robust strokes and remains first against every crossing field."},
        "support_legibility": {"status": "PASS", "evidence": "The complete supporting phrase is legible at full size."},
        "text_cluster_cohesion": {"status": "PASS", "evidence": "Title, category, and support share one left alignment axis."},
    })
    return document


class VisualVerdictHarnessTests(unittest.TestCase):
    def test_passing_fixture_is_accepted(self) -> None:
        result, messages = validate_document(load_fixture("valid-pass.json"), FIXTURES / "valid-pass.json")
        self.assertEqual(result, "PASS")
        self.assertEqual(messages, [])

    def test_directory_reports_artwork_failures_and_invalid_documents_separately(self) -> None:
        process = subprocess.run(
            [sys.executable, "-B", str(VALIDATOR), str(FIXTURES)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(process.returncode, 2)
        self.assertIn("ARTWORK_FAILURE:", process.stdout)
        self.assertIn("INVALID_DOCUMENT:", process.stdout)
        self.assertIn("Summary: 1 pass, 5 artwork failure, 1 invalid document", process.stdout)

    def test_background_failure_is_a_failed_artwork_not_a_bad_document(self) -> None:
        result, messages = validate_document(load_fixture("missing-background-failure.json"), FIXTURES / "missing-background-failure.json")
        self.assertEqual(result, "ARTWORK_FAILURE")
        self.assertTrue(any("background coverage" in message for message in messages))

    def test_extra_text_is_actionable(self) -> None:
        result, messages = validate_document(load_fixture("extra-designed-text-failure.json"), FIXTURES / "extra-designed-text-failure.json")
        self.assertEqual(result, "ARTWORK_FAILURE")
        self.assertIn("text inventory: extra designed text observed", messages)

    def test_carrier_copy_must_not_repeat_externally(self) -> None:
        result, messages = validate_document(load_fixture("carrier-screen-duplicate-failure.json"), FIXTURES / "carrier-screen-duplicate-failure.json")
        self.assertEqual(result, "ARTWORK_FAILURE")
        self.assertIn("screen state: CARRIER support copy duplicated externally", messages)

    def test_subject_mass_failure_is_actionable(self) -> None:
        result, messages = validate_document(load_fixture("subject-mass-unity-failure.json"), FIXTURES / "subject-mass-unity-failure.json")
        self.assertEqual(result, "ARTWORK_FAILURE")
        self.assertIn("visual review: subject_mass_unity failed", messages)

    def test_pass_cannot_hide_thumbnail_failure(self) -> None:
        document = load_fixture("thumbnail-title-hierarchy-failure.json")
        document["verdict"] = "PASS"
        result, messages = validate_document(document, FIXTURES / "mutated.json")
        self.assertEqual(result, "INVALID_DOCUMENT")
        self.assertIn("verdict: cannot be PASS when hard checks fail", messages)

    def test_aesthetic_preference_does_not_change_compliance(self) -> None:
        document = copy.deepcopy(load_fixture("valid-pass.json"))
        document["aesthetic_preference"] = {"rating": "NOT_PREFERRED", "evidence": "The reviewer prefers another direction."}
        result, messages = validate_document(document, FIXTURES / "preference-only.json")
        self.assertEqual(result, "PASS")
        self.assertEqual(messages, [])

    def test_schema_v2_requires_and_accepts_typography_observations(self) -> None:
        document = typography_v2_document()
        result, messages = validate_document(document, FIXTURES / "typography-pass.json")
        self.assertEqual(result, "PASS")
        self.assertEqual(messages, [])

        document["visual_review"].pop("title_footprint")
        result, messages = validate_document(document, FIXTURES / "typography-missing.json")
        self.assertEqual(result, "INVALID_DOCUMENT")
        self.assertTrue(any("title_footprint" in message for message in messages))

    def test_schema_v2_typography_failure_forces_regeneration(self) -> None:
        document = typography_v2_document()
        document["visual_review"]["support_legibility"] = {
            "status": "FAIL",
            "evidence": "The seven-word deck is too small to read at full size.",
        }
        document["hard_verdict"] = "FAIL"
        document["repair_mode"] = "REGENERATE"
        document["verdict"] = "REGENERATE"
        document["root_cause_class"] = "TYPOGRAPHY"
        result, messages = validate_document(document, FIXTURES / "typography-failure.json")
        self.assertEqual(result, "ARTWORK_FAILURE")
        self.assertIn("typography: support_legibility failed", messages)

    def test_unavailable_proof_can_be_recorded_as_invalid_input(self) -> None:
        document = copy.deepcopy(load_fixture("valid-pass.json"))
        document["proof"]["path"] = "evals/visual/fixtures/does-not-exist.png"
        document["machine_checks"]["file_exists"] = False
        for key in ("format", "dimensions", "ratio"):
            document["machine_checks"][key]["actual"] = None
            document["machine_checks"][key]["pass"] = False
        document["machine_checks"]["opacity"]["opaque"] = False
        document["machine_checks"]["opacity"]["has_alpha"] = False
        document["machine_checks"]["opacity"]["pass"] = False
        document["hard_verdict"] = "FAIL"
        document["repair_mode"] = "NONE"
        document["verdict"] = "INVALID_INPUT"
        document["root_cause_class"] = "DELIVERY"
        result, messages = validate_document(document, FIXTURES / "missing-proof.json")
        self.assertEqual(result, "ARTWORK_FAILURE")
        self.assertIn("machine delivery: proof file does not exist", messages)


if __name__ == "__main__":
    unittest.main()
