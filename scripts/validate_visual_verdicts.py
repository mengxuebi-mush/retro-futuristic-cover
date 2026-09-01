#!/usr/bin/env python3
"""Validate structured visual verdicts without judging aesthetic quality."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_image import inspect_image  # noqa: E402


EXIT_OK = 0
EXIT_ARTWORK_FAILURE = 1
EXIT_INVALID_DOCUMENT = 2

STATUS_VALUES = {"PASS", "FAIL", "NOT_APPLICABLE"}
VERDICT_VALUES = {"PASS", "EDIT", "REGENERATE", "INVALID_INPUT"}
CORE_ROLES = {"FINAL_TITLE", "CATEGORY_LABEL", "MICRO_SUBTITLE"}


def _is_dict(value: Any) -> bool:
    return isinstance(value, dict)


def _required(data: dict[str, Any], keys: tuple[str, ...], where: str, errors: list[str]) -> None:
    for key in keys:
        if key not in data:
            errors.append(f"{where}: missing required field '{key}'")


def _status(value: Any, where: str, errors: list[str]) -> None:
    if value not in STATUS_VALUES:
        errors.append(f"{where}: expected PASS, FAIL, or NOT_APPLICABLE")


def _evidence(item: Any, where: str, errors: list[str]) -> None:
    if not _is_dict(item):
        errors.append(f"{where}: expected an object")
    elif not isinstance(item.get("evidence"), str) or not item["evidence"].strip():
        errors.append(f"{where}.evidence: expected a non-empty observation note")


def _ratio(value: Any) -> tuple[int, int] | None:
    if not isinstance(value, str) or value.count(":") != 1:
        return None
    left, right = value.split(":")
    if not left.isdigit() or not right.isdigit() or int(left) <= 0 or int(right) <= 0:
        return None
    return int(left), int(right)


def _ratio_matches(expected: Any, width: int, height: int) -> bool:
    parsed = _ratio(expected)
    return bool(parsed and width * parsed[1] == height * parsed[0])


def _machine_checks(
    document: dict[str, Any], source: Path, errors: list[str], hard_failures: list[str]
) -> None:
    checks = document.get("machine_checks")
    proof = document.get("proof", {})
    if not _is_dict(checks):
        errors.append("machine_checks: expected an object")
        return
    _required(checks, ("file_exists", "format", "dimensions", "ratio", "opacity"), "machine_checks", errors)
    if errors and not all(key in checks for key in ("file_exists", "format", "dimensions", "ratio", "opacity")):
        return
    if not isinstance(checks.get("file_exists"), bool):
        errors.append("machine_checks.file_exists: expected a boolean")

    proof_path = proof.get("path") if _is_dict(proof) else None
    actual_path = None
    if isinstance(proof_path, str) and proof_path:
        candidate = Path(proof_path)
        actual_path = candidate if candidate.is_absolute() else ROOT / candidate
    actual_exists = bool(actual_path and actual_path.is_file())
    if checks["file_exists"] is not actual_exists:
        errors.append(f"machine_checks.file_exists: declared {checks['file_exists']}, observed {actual_exists}")
    if not actual_exists:
        hard_failures.append("machine delivery: proof file does not exist")
        for key in ("format", "dimensions", "ratio"):
            value = checks.get(key, {})
            if _is_dict(value) and value.get("actual") is not None:
                errors.append(f"machine_checks.{key}.actual: must be null when proof file is missing")
            if _is_dict(value) and value.get("pass") is not False:
                errors.append(f"machine_checks.{key}.pass: must be false when proof file is missing")
        opacity = checks.get("opacity", {})
        if _is_dict(opacity) and opacity.get("pass") is not False:
            errors.append("machine_checks.opacity.pass: must be false when proof file is missing")
        return

    try:
        detected_format, width, height, has_alpha = inspect_image(actual_path)
    except (OSError, ValueError) as exc:
        errors.append(f"machine delivery: cannot inspect proof file: {exc}")
        return
    detected_ratio = f"{width}:{height}"
    actuals = {
        "format": detected_format,
        "dimensions": {"width": width, "height": height},
        "ratio": detected_ratio,
        "has_alpha": has_alpha,
    }
    fmt = checks.get("format", {})
    if not _is_dict(fmt):
        errors.append("machine_checks.format: expected an object")
    else:
        if fmt.get("actual") != detected_format:
            errors.append(f"machine_checks.format.actual: declared {fmt.get('actual')!r}, observed {detected_format!r}")
        if fmt.get("pass") != (fmt.get("expected") == detected_format):
            errors.append("machine_checks.format.pass: inconsistent with expected and actual format")
    dimensions = checks.get("dimensions", {})
    if not _is_dict(dimensions):
        errors.append("machine_checks.dimensions: expected an object")
    else:
        actual_dimensions = dimensions.get("actual")
        if actual_dimensions != actuals["dimensions"]:
            errors.append("machine_checks.dimensions.actual: inconsistent with proof pixels")
        expected_dimensions = dimensions.get("expected")
        expected_pass = expected_dimensions == actual_dimensions
        if dimensions.get("pass") != expected_pass:
            errors.append("machine_checks.dimensions.pass: inconsistent with expected and actual dimensions")
    ratio = checks.get("ratio", {})
    if not _is_dict(ratio):
        errors.append("machine_checks.ratio: expected an object")
    else:
        if ratio.get("actual") != detected_ratio:
            errors.append(f"machine_checks.ratio.actual: declared {ratio.get('actual')!r}, observed {detected_ratio!r}")
        if ratio.get("pass") != _ratio_matches(ratio.get("expected"), width, height):
            errors.append("machine_checks.ratio.pass: inconsistent with expected and actual ratio")
    opacity = checks.get("opacity", {})
    if not _is_dict(opacity):
        errors.append("machine_checks.opacity: expected an object")
    else:
        if opacity.get("has_alpha") != has_alpha:
            errors.append("machine_checks.opacity.has_alpha: inconsistent with proof pixels")
        expected_opaque = not has_alpha
        if opacity.get("opaque") != expected_opaque or opacity.get("pass") != expected_opaque:
            errors.append("machine_checks.opacity: opaque/pass must reflect the observed alpha channel")

    for key in ("format", "dimensions", "ratio", "opacity"):
        value = checks.get(key, {})
        if _is_dict(value) and value.get("pass") is False:
            hard_failures.append(f"machine delivery: {key} check failed")


def _copy_checks(document: dict[str, Any], errors: list[str], hard_failures: list[str]) -> None:
    copy = document.get("copy")
    if not _is_dict(copy):
        errors.append("copy: expected an object")
        return
    _required(copy, ("contract", "locked", "observed", "intrinsic_artifact_text", "duplicates", "extra"), "copy", errors)
    locked = copy.get("locked")
    observed = copy.get("observed")
    if copy.get("contract") not in {"THREE_ELEMENT_COVER", "EDITORIAL_POSTER_5_TO_7"}:
        errors.append("copy.contract: invalid controlled value")
    if not isinstance(locked, list) or not isinstance(observed, list):
        return
    locked_texts: list[str] = []
    locked_roles: list[str] = []
    locked_locations: dict[str, str] = {}
    for index, item in enumerate(locked, start=1):
        if not _is_dict(item):
            errors.append(f"copy.locked[{index}]: expected an object")
            continue
        _required(item, ("role", "text", "location"), f"copy.locked[{index}]", errors)
        text = item.get("text")
        role = item.get("role")
        location = item.get("location")
        if isinstance(text, str):
            locked_texts.append(text)
            locked_locations[text] = location
        if isinstance(role, str):
            locked_roles.append(role)
    if len(locked_texts) != len(set(locked_texts)):
        errors.append("copy.locked: text strings must be unique")
    if copy.get("contract") == "THREE_ELEMENT_COVER":
        if not CORE_ROLES.issubset(set(locked_roles)) or len(locked) != 3:
            errors.append("copy.locked: THREE_ELEMENT_COVER requires exactly the three core roles")
    elif copy.get("contract") == "EDITORIAL_POSTER_5_TO_7" and not 5 <= len(locked) <= 7:
        errors.append("copy.locked: EDITORIAL_POSTER_5_TO_7 requires 5–7 locked strings")
    if copy.get("contract") == "EDITORIAL_POSTER_5_TO_7" and not CORE_ROLES.issubset(set(locked_roles)):
        errors.append("copy.locked: EDITORIAL_POSTER_5_TO_7 also requires the three core roles")
    screen_locked = {text for text, location in locked_locations.items() if location == "screen"}
    if document.get("screen_state") == "CARRIER" and not screen_locked:
        errors.append("copy.locked: CARRIER requires one locked string at the screen location")
    if document.get("screen_state") != "CARRIER" and screen_locked:
        errors.append("copy.locked: only CARRIER may place designed copy at the screen location")

    observed_by_text: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(observed, start=1):
        if not _is_dict(item):
            errors.append(f"copy.observed[{index}]: expected an object")
            continue
        _required(item, ("text", "role", "count", "locations"), f"copy.observed[{index}]", errors)
        text = item.get("text")
        locations = item.get("locations")
        count = item.get("count")
        if not isinstance(text, str) or not isinstance(locations, list) or not isinstance(count, int):
            continue
        if text in observed_by_text:
            errors.append(f"copy.observed: duplicate record for {text!r}")
        observed_by_text[text] = item
        if count != len(locations):
            errors.append(f"copy.observed[{index}]: count must equal locations length")

    observed_texts = set(observed_by_text)
    locked_set = set(locked_texts)
    derived_extra = sorted(observed_texts - locked_set)
    derived_duplicates = sorted(
        text for text, item in observed_by_text.items() if item.get("count", 0) > 1
    )
    if copy.get("extra") != derived_extra:
        errors.append(f"copy.extra: expected {derived_extra!r} from the observed inventory")
    if copy.get("duplicates") != derived_duplicates:
        errors.append(f"copy.duplicates: expected {derived_duplicates!r} from observed counts")
    if derived_extra:
        hard_failures.append("text inventory: extra designed text observed")
    if derived_duplicates:
        hard_failures.append("text inventory: duplicate designed text observed")
    if observed_texts != locked_set:
        hard_failures.append("text inventory: observed strings do not exactly match locked strings")
    for text, location in locked_locations.items():
        item = observed_by_text.get(text)
        if not item:
            continue
        locations = item.get("locations", [])
        if location not in locations:
            hard_failures.append(f"text inventory: {text!r} not observed at its locked {location} location")
        if document.get("screen_state") == "CARRIER" and location == "screen" and "external" in locations:
            hard_failures.append("screen state: CARRIER support copy duplicated externally")


def _visual_checks(document: dict[str, Any], errors: list[str], hard_failures: list[str]) -> None:
    review = document.get("visual_review")
    if not _is_dict(review):
        errors.append("visual_review: expected an object")
        return
    required = (
        "full_size", "thumbnail_25_percent", "background_coverage", "first_reading_event",
        "hierarchy", "subject_origin_recognition", "subject_mass_unity", "release_zone_visibility",
        "support_copy_structural_attachment", "screen_state_compliance", "layout_failure_signals",
    )
    _required(review, required, "visual_review", errors)
    for key in ("full_size", "thumbnail_25_percent", "subject_origin_recognition", "subject_mass_unity", "release_zone_visibility", "support_copy_structural_attachment"):
        item = review.get(key)
        _evidence(item, f"visual_review.{key}", errors)
        if _is_dict(item) and item.get("status") not in STATUS_VALUES:
            errors.append(f"visual_review.{key}.status: invalid status")
        elif _is_dict(item) and item.get("status") != "PASS":
            if key != "subject_mass_unity" or document.get("subject_assembly") != "SINGLE_OBJECT":
                suffix = "failed" if item.get("status") == "FAIL" else "was not reviewed"
                hard_failures.append(f"visual review: {key} {suffix}")

    background = review.get("background_coverage")
    if not _is_dict(background):
        errors.append("visual_review.background_coverage: expected an object")
    else:
        if background.get("status") not in STATUS_VALUES:
            errors.append("visual_review.background_coverage.status: invalid status")
        corners = background.get("corners")
        if not _is_dict(corners):
            errors.append("visual_review.background_coverage.corners: expected an object")
        else:
            for corner in ("top_left", "top_right", "bottom_left", "bottom_right"):
                _status(corners.get(corner), f"visual_review.background_coverage.corners.{corner}", errors)
                if corners.get(corner) == "FAIL":
                    hard_failures.append(f"background coverage: {corner} failed")
        _status(background.get("perimeter"), "visual_review.background_coverage.perimeter", errors)
        if background.get("status") != "PASS" or background.get("perimeter") != "PASS":
            hard_failures.append("background coverage: full perimeter is not continuous")
        if _is_dict(corners) and any(corners.get(corner) != "PASS" for corner in ("top_left", "top_right", "bottom_left", "bottom_right")):
            hard_failures.append("background coverage: every corner must be covered")

    first = review.get("first_reading_event")
    if not _is_dict(first):
        errors.append("visual_review.first_reading_event: expected an object")
    else:
        if not isinstance(first.get("evidence"), str) or not first["evidence"].strip():
            errors.append("visual_review.first_reading_event.evidence: expected a non-empty observation note")
        if first.get("value") not in {"TITLE", "SUBJECT", "SUPPORT", "OTHER"}:
            errors.append("visual_review.first_reading_event.value: invalid controlled value")
        elif first.get("value") != "TITLE":
            hard_failures.append("reading order: title is not the first reading event")

    hierarchy = review.get("hierarchy")
    if not _is_dict(hierarchy):
        errors.append("visual_review.hierarchy: expected an object")
    else:
        if not isinstance(hierarchy.get("evidence"), str) or not hierarchy["evidence"].strip():
            errors.append("visual_review.hierarchy.evidence: expected a non-empty observation note")
        for key in ("title", "subject", "support"):
            _status(hierarchy.get(key), f"visual_review.hierarchy.{key}", errors)
            if hierarchy.get(key) != "PASS":
                suffix = "failed" if hierarchy.get(key) == "FAIL" else "was not reviewed"
                hard_failures.append(f"hierarchy: {key} role {suffix}")

    screen = review.get("screen_state_compliance")
    if not _is_dict(screen):
        errors.append("visual_review.screen_state_compliance: expected an object")
    else:
        if not isinstance(screen.get("evidence"), str) or not screen["evidence"].strip():
            errors.append("visual_review.screen_state_compliance.evidence: expected a non-empty observation note")
        if screen.get("state") not in {"NOT_APPLICABLE", "DORMANT", "SIGNAL", "CARRIER"}:
            errors.append("visual_review.screen_state_compliance.state: invalid controlled value")
        _status(screen.get("status"), "visual_review.screen_state_compliance.status", errors)
        if screen.get("state") != document.get("screen_state"):
            errors.append("visual_review.screen_state_compliance.state: must match top-level screen_state")
        expected_screen_status = "NOT_APPLICABLE" if document.get("screen_state") == "NOT_APPLICABLE" else "PASS"
        if screen.get("status") != expected_screen_status:
            hard_failures.append("screen state: compliance check failed or was not reviewed")

    signals = review.get("layout_failure_signals")
    if not _is_dict(signals):
        errors.append("visual_review.layout_failure_signals: expected an object")
    else:
        observed = signals.get("observed")
        if not isinstance(signals.get("evidence"), str) or not signals["evidence"].strip():
            errors.append("visual_review.layout_failure_signals.evidence: expected a non-empty observation note")
        if not isinstance(observed, list):
            errors.append("visual_review.layout_failure_signals.observed: expected an array")
        elif observed:
            hard_failures.append("layout: failure signals were observed")


def validate_document(document: Any, source: Path) -> tuple[str, list[str]]:
    """Return (PASS, ARTWORK_FAILURE, or INVALID_DOCUMENT) and actionable messages."""
    errors: list[str] = []
    hard_failures: list[str] = []
    if not _is_dict(document):
        return "INVALID_DOCUMENT", ["document: top-level JSON value must be an object"]
    _required(
        document,
        ("schema_version", "version", "proof", "subject_assembly", "screen_state", "machine_checks", "copy", "visual_review", "hard_verdict", "repair_mode", "verdict", "root_cause_class", "aesthetic_preference"),
        "document",
        errors,
    )
    if document.get("schema_version") != 1:
        errors.append("schema_version: expected integer 1")
    if document.get("version") not in {"V1", "V2", "V3"}:
        errors.append("version: expected V1, V2, or V3")
    proof = document.get("proof")
    if not _is_dict(proof):
        errors.append("proof: expected an object")
    else:
        _required(proof, ("path", "manifest_path", "carrier", "canvas", "layout_family"), "proof", errors)
        canvas = proof.get("canvas")
        if not _is_dict(canvas):
            errors.append("proof.canvas: expected an object")
        else:
            _required(canvas, ("width", "height", "ratio"), "proof.canvas", errors)
            if not isinstance(canvas.get("width"), int) or not isinstance(canvas.get("height"), int):
                errors.append("proof.canvas: width and height must be positive integers")
            parsed = _ratio(canvas.get("ratio"))
            if parsed and isinstance(canvas.get("width"), int) and isinstance(canvas.get("height"), int):
                if canvas["width"] * parsed[1] != canvas["height"] * parsed[0]:
                    errors.append("proof.canvas.ratio: does not match canvas dimensions")
    if document.get("subject_assembly") not in {"SINGLE_OBJECT", "COMPOUND_SET", "PRIMARY_SATELLITES", "REPEATED_FAMILY"}:
        errors.append("subject_assembly: invalid controlled value")
    if document.get("screen_state") not in {"NOT_APPLICABLE", "DORMANT", "SIGNAL", "CARRIER"}:
        errors.append("screen_state: invalid controlled value")
    if document.get("screen_state") == "CARRIER":
        if _is_dict(proof) and proof.get("carrier") != "EDITORIAL_POSTER":
            errors.append("screen_state: CARRIER is only valid for EDITORIAL_POSTER")
        copy = document.get("copy")
        if _is_dict(copy) and copy.get("contract") != "EDITORIAL_POSTER_5_TO_7":
            errors.append("screen_state: CARRIER requires EDITORIAL_POSTER_5_TO_7 copy")
    if document.get("hard_verdict") not in {"PASS", "FAIL"}:
        errors.append("hard_verdict: expected PASS or FAIL")
    if document.get("repair_mode") not in {"NONE", "EDIT", "REGENERATE"}:
        errors.append("repair_mode: invalid controlled value")
    if document.get("verdict") not in VERDICT_VALUES:
        errors.append("verdict: invalid controlled value")
    if document.get("root_cause_class") not in {"NONE", "DELIVERY", "BACKGROUND_COVERAGE", "TEXT_INVENTORY", "TITLE_HIERARCHY", "SCREEN_DUPLICATION", "SUBJECT_MASS", "LAYOUT", "SUBJECT_ORIGIN", "SUPPORT_ATTACHMENT", "OTHER"}:
        errors.append("root_cause_class: invalid controlled value")

    _machine_checks(document, source, errors, hard_failures)
    _copy_checks(document, errors, hard_failures)
    _visual_checks(document, errors, hard_failures)

    preference = document.get("aesthetic_preference")
    if not _is_dict(preference):
        errors.append("aesthetic_preference: expected an object")
    else:
        if preference.get("rating") not in {"PREFERRED", "ACCEPTABLE", "NOT_PREFERRED"}:
            errors.append("aesthetic_preference.rating: invalid controlled value")
        if not isinstance(preference.get("evidence"), str) or not preference["evidence"].strip():
            errors.append("aesthetic_preference.evidence: expected a non-empty preference note")

    if document.get("hard_verdict") == "PASS" and hard_failures:
        errors.append("hard_verdict: cannot be PASS while hard checks fail")
    if document.get("hard_verdict") == "FAIL" and not hard_failures:
        errors.append("hard_verdict: FAIL requires at least one hard check failure")
    expected_verdict = "PASS" if not hard_failures else None
    if expected_verdict == "PASS" and document.get("verdict") != "PASS":
        errors.append("verdict: must be PASS when all hard checks pass")
    if hard_failures and document.get("verdict") == "PASS":
        errors.append("verdict: cannot be PASS when hard checks fail")
    if not hard_failures and document.get("repair_mode") != "NONE":
        errors.append("repair_mode: must be NONE for a passing verdict")
    if hard_failures and document.get("verdict") == "INVALID_INPUT":
        if document.get("repair_mode") != "NONE":
            errors.append("repair_mode: INVALID_INPUT must use NONE")
    elif hard_failures and document.get("repair_mode") == "NONE":
        errors.append("repair_mode: choose EDIT or REGENERATE for a failed artwork")
    elif document.get("verdict") in {"EDIT", "REGENERATE"} and document.get("repair_mode") != document.get("verdict"):
        errors.append("repair_mode: must match the EDIT or REGENERATE verdict")
    if not hard_failures and document.get("root_cause_class") != "NONE":
        errors.append("root_cause_class: must be NONE for a passing verdict")
    if hard_failures and document.get("root_cause_class") == "NONE":
        errors.append("root_cause_class: name one highest-impact root cause for a failed artwork")

    if errors:
        return "INVALID_DOCUMENT", errors
    if hard_failures:
        return "ARTWORK_FAILURE", hard_failures
    return "PASS", []


def _inputs(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(candidate for candidate in path.rglob("*.json") if candidate.name != "schema.json")
    return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="one verdict JSON file or a directory of verdict JSON files")
    args = parser.parse_args(argv)
    files = _inputs(args.path)
    if not files:
        print(f"INVALID_DOCUMENT: no verdict JSON files found at {args.path}")
        return EXIT_INVALID_DOCUMENT

    counts = {"PASS": 0, "ARTWORK_FAILURE": 0, "INVALID_DOCUMENT": 0}
    for path in files:
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            counts["INVALID_DOCUMENT"] += 1
            print(f"INVALID_DOCUMENT: {path}: cannot parse JSON ({exc})")
            continue
        result, messages = validate_document(document, path)
        counts[result] += 1
        if result == "PASS":
            print(f"PASS: {path}")
        else:
            print(f"{result}: {path}")
            for message in messages:
                print(f"  - {message}")

    print(
        f"Summary: {counts['PASS']} pass, {counts['ARTWORK_FAILURE']} artwork failure, "
        f"{counts['INVALID_DOCUMENT']} invalid document"
    )
    if counts["INVALID_DOCUMENT"]:
        return EXIT_INVALID_DOCUMENT
    if counts["ARTWORK_FAILURE"]:
        return EXIT_ARTWORK_FAILURE
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
