#!/usr/bin/env python3
"""Validate locked generation content, selector manifests, and compiled briefs."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DESIGN_SYSTEM = ROOT / "design-system"
BACKGROUND_REQUIREMENT = (
    "Render a finished, fully opaque full-bleed poster. The selected gradient is the bottommost "
    "background layer and covers 100% of the canvas behind the title, subject, negative space, "
    "and every cropped edge. No transparency or alpha anywhere."
)
CATEGORY_LABELS = {
    "FUTURE", "FOCUS", "INSIGHT", "IDEA", "PRINCIPLE", "MINDSET", "DESIGN",
    "GROWTH", "BUILD", "LEADERSHIP", "REMINDER",
}
TEXT_CONTRACTS = {"THREE_ELEMENT_COVER", "EDITORIAL_POSTER_5_TO_7"}
SUBJECT_ASSEMBLIES = {"SINGLE_OBJECT", "COMPOUND_SET", "PRIMARY_SATELLITES", "REPEATED_FAMILY"}
MULTI_OBJECT_ASSEMBLIES = SUBJECT_ASSEMBLIES - {"SINGLE_OBJECT"}
SUBJECT_ORIGINS = {"ABSTRACT_FORM", "ARCHIVE_ARTIFACT", "SPECULATIVE_OBJECT", "NOT_APPLICABLE_SUPPLIED_IMAGE"}
TREATMENTS = {"FAITHFUL_RETAINED", "ENVIRONMENT_GRADED", "PALETTE_ASSIMILATED"}
SCREEN_STATES = {"NOT_APPLICABLE", "DORMANT", "SIGNAL", "CARRIER"}
SUPPORTING_COPY_ROLES = {"MICRO_SUBTITLE", "SUPPORTING_DECK"}


class ValidationError(ValueError):
    """An input or output does not satisfy the generation-brief contract."""


def _fail(path: str, message: str) -> None:
    raise ValidationError(f"{path}: {message}")


def _require(data: dict[str, Any], key: str, path: str) -> Any:
    if key not in data:
        _fail(path, f"missing required field {key!r}")
    return data[key]


def _string(value: Any, path: str, *, allow_none: bool = False) -> str:
    if allow_none and value is None:
        return ""
    if not isinstance(value, str) or not value.strip():
        _fail(path, "must be a non-empty string")
    return value


def _list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        _fail(path, "must be an array")
    return value


def _normalized(value: str) -> str:
    return " ".join(value.split()).casefold()


def _assert_unique(values: list[str], path: str) -> None:
    seen: dict[str, int] = {}
    for index, value in enumerate(values):
        key = _normalized(value)
        if key in seen:
            _fail(path, f"duplicate designed string at indexes {seen[key]} and {index}: {value!r}")
        seen[key] = index


def _language_length(value: str) -> tuple[int, int]:
    english_words = re.findall(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*", value)
    han_characters = re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", value)
    return len(english_words), len(han_characters)


def _validate_supporting_copy(value: str, role: str, path: str) -> None:
    english_words, han_characters = _language_length(value)
    if english_words and not han_characters:
        lower, upper = (2, 5) if role == "MICRO_SUBTITLE" else (2, 14)
        if not lower <= english_words <= upper:
            destination = "deck" if role == "MICRO_SUBTITLE" and english_words > upper else role.lower()
            _fail(path, f"{role} requires {lower}–{upper} English words; use {destination} for this exact copy")
    elif han_characters and not english_words:
        lower, upper = (4, 8) if role == "MICRO_SUBTITLE" else (4, 24)
        if not lower <= han_characters <= upper:
            destination = "deck" if role == "MICRO_SUBTITLE" and han_characters > upper else role.lower()
            _fail(path, f"{role} requires {lower}–{upper} Han characters; use {destination} for this exact copy")


def _numeric_range(value: Any, path: str, *, minimum: float, maximum: float) -> list[float]:
    values = _list(value, path)
    if len(values) != 2:
        _fail(path, "must contain exactly two ordered numbers")
    if any(isinstance(item, bool) or not isinstance(item, (int, float)) for item in values):
        _fail(path, "must contain numbers")
    if not minimum <= values[0] <= values[1] <= maximum:
        _fail(path, f"must be ordered within {minimum}–{maximum}")
    return values


def _validate_canvas(canvas: Any, path: str = "canvas") -> dict[str, Any]:
    if not isinstance(canvas, dict):
        _fail(path, "must be an object")
    width = canvas.get("width")
    height = canvas.get("height")
    ratio = _string(canvas.get("ratio"), f"{path}.ratio")
    if isinstance(width, bool) or not isinstance(width, int) or width <= 0:
        _fail(f"{path}.width", "must be a positive integer")
    if isinstance(height, bool) or not isinstance(height, int) or height <= 0:
        _fail(f"{path}.height", "must be a positive integer")
    divisor = math.gcd(width, height)
    expected_ratio = f"{width // divisor}:{height // divisor}"
    if ratio != expected_ratio:
        _fail(f"{path}.ratio", f"must match canvas dimensions ({expected_ratio})")
    result = {"width": width, "height": height, "ratio": ratio}
    if "platform" in canvas:
        result["platform"] = _string(canvas["platform"], f"{path}.platform")
    return result


def _support_element(value: Any, path: str) -> dict[str, Any]:
    if isinstance(value, str):
        text = _string(value, path)
        return {"text": text}
    if not isinstance(value, dict):
        _fail(path, "must be a string or object")
    text = _string(value.get("text"), f"{path}.text")
    result = {"text": text}
    for key in ("role", "anchor", "source"):
        if key in value:
            result[key] = _string(value[key], f"{path}.{key}")
    if "factual" in value:
        if not isinstance(value["factual"], bool):
            _fail(f"{path}.factual", "must be a boolean")
        if not value["factual"]:
            _fail(f"{path}.factual", "must be true for poster support copy")
        result["factual"] = True
    return result


def _assembly_member(value: Any, path: str) -> dict[str, str]:
    if not isinstance(value, dict):
        _fail(path, "must be an object")
    result = {
        "role": _string(value.get("role"), f"{path}.role"),
        "form_cue": _string(value.get("form_cue"), f"{path}.form_cue"),
    }
    if "function" in value:
        result["function"] = _string(value["function"], f"{path}.function")
    return result


def validate_concept_contract(value: Any, path: str = "content.concept_contract") -> dict[str, Any]:
    """Validate message-to-image evidence without prescribing morphology."""
    if not isinstance(value, dict):
        _fail(path, "must be an object")
    evidence_values = _list(value.get("visible_evidence"), f"{path}.visible_evidence")
    if not 1 <= len(evidence_values) <= 3:
        _fail(f"{path}.visible_evidence", "must contain 1–3 observable cues")
    evidence = [_string(item, f"{path}.visible_evidence[{index}]") for index, item in enumerate(evidence_values)]
    _assert_unique(evidence, f"{path}.visible_evidence")
    forbidden_values = _list(value.get("must_not_imply"), f"{path}.must_not_imply")
    if not 1 <= len(forbidden_values) <= 4:
        _fail(f"{path}.must_not_imply", "must contain 1–4 contradictory or generic readings")
    forbidden = [_string(item, f"{path}.must_not_imply[{index}]") for index, item in enumerate(forbidden_values)]
    _assert_unique(forbidden, f"{path}.must_not_imply")
    if {_normalized(item) for item in evidence} & {_normalized(item) for item in forbidden}:
        _fail(path, "visible evidence cannot also be listed as a forbidden reading")
    return {
        "message_anchor": _string(value.get("message_anchor"), f"{path}.message_anchor"),
        "subject_behavior": _string(value.get("subject_behavior"), f"{path}.subject_behavior"),
        "visible_evidence": evidence,
        "semantic_direction": _string(value.get("semantic_direction"), f"{path}.semantic_direction"),
        "must_not_imply": forbidden,
    }


def validate_assembly_plan(value: Any, path: str = "content.assembly_plan") -> dict[str, Any]:
    """Validate a mode-aware plan without prescribing concrete object morphology."""
    if not isinstance(value, dict):
        _fail(path, "must be an object")
    mode = _string(value.get("mode"), f"{path}.mode")
    if mode not in MULTI_OBJECT_ASSEMBLIES:
        _fail(f"{path}.mode", f"must be one of {sorted(MULTI_OBJECT_ASSEMBLIES)}")
    result: dict[str, Any] = {
        "mode": mode,
        "shared_relation": _string(value.get("shared_relation"), f"{path}.shared_relation"),
        "observability_rule": _string(value.get("observability_rule"), f"{path}.observability_rule"),
    }
    if mode == "COMPOUND_SET":
        values = _list(value.get("members"), f"{path}.members")
        if not 2 <= len(values) <= 3:
            _fail(f"{path}.members", "COMPOUND_SET requires 2–3 complete members")
        members = [_assembly_member(item, f"{path}.members[{index}]") for index, item in enumerate(values)]
        _assert_unique([item["role"] for item in members], f"{path}.members")
        result["members"] = members
    elif mode == "PRIMARY_SATELLITES":
        primary = _assembly_member(value.get("primary"), f"{path}.primary")
        values = _list(value.get("satellites"), f"{path}.satellites")
        if not 1 <= len(values) <= 2:
            _fail(f"{path}.satellites", "PRIMARY_SATELLITES requires 1–2 satellites")
        satellites = [_assembly_member(item, f"{path}.satellites[{index}]") for index, item in enumerate(values)]
        _assert_unique([primary["role"], *[item["role"] for item in satellites]], f"{path}.roles")
        ratio = value.get("min_visual_weight_ratio")
        if isinstance(ratio, bool) or not isinstance(ratio, (int, float)) or ratio < 2:
            _fail(f"{path}.min_visual_weight_ratio", "must be a number greater than or equal to 2")
        result.update({"primary": primary, "satellites": satellites, "min_visual_weight_ratio": ratio})
    else:
        unit = _assembly_member(value.get("family_unit"), f"{path}.family_unit")
        count = value.get("instance_count")
        if isinstance(count, bool) or not isinstance(count, int) or not 2 <= count <= 5:
            _fail(f"{path}.instance_count", "REPEATED_FAMILY requires 2–5 instances")
        result.update({
            "family_unit": unit,
            "instance_count": count,
            "path": _string(value.get("path"), f"{path}.path"),
            "focal_instance_rule": _string(value.get("focal_instance_rule"), f"{path}.focal_instance_rule"),
        })
    return result


def validate_content(content: Any) -> dict[str, Any]:
    """Validate and normalize content.json without inventing any copy."""
    if not isinstance(content, dict):
        _fail("content", "must be an object")
    canvas = _validate_canvas(_require(content, "canvas", "content"))
    contract = _string(_require(content, "text_contract", "content"), "content.text_contract")
    if contract not in TEXT_CONTRACTS:
        _fail("content.text_contract", f"must be one of {sorted(TEXT_CONTRACTS)}")
    title = _string(_require(content, "final_title", "content"), "content.final_title")
    category = _string(_require(content, "category_label", "content"), "content.category_label")
    if category not in CATEGORY_LABELS:
        _fail("content.category_label", f"must be one of {sorted(CATEGORY_LABELS)}")
    if "micro_subtitle" in content and "deck" in content:
        _fail("content", "provide only one of micro_subtitle or deck")
    supporting_copy_role = "MICRO_SUBTITLE" if "micro_subtitle" in content else "SUPPORTING_DECK"
    subtitle = content.get("micro_subtitle", content.get("deck"))
    if subtitle is None:
        _fail("content", "requires micro_subtitle or deck")
    supporting_path = "content.micro_subtitle" if supporting_copy_role == "MICRO_SUBTITLE" else "content.deck"
    subtitle = _string(subtitle, supporting_path)
    _validate_supporting_copy(subtitle, supporting_copy_role, supporting_path)

    support_values = _list(content.get("poster_support_elements", []), "content.poster_support_elements")
    support = [_support_element(value, f"content.poster_support_elements[{index}]") for index, value in enumerate(support_values)]
    if contract == "THREE_ELEMENT_COVER" and support:
        _fail("content.poster_support_elements", "THREE_ELEMENT_COVER requires exactly 0 support elements")
    if contract == "EDITORIAL_POSTER_5_TO_7" and not 2 <= len(support) <= 4:
        _fail("content.poster_support_elements", "EDITORIAL_POSTER_5_TO_7 requires 2–4 factual support elements")

    all_strings = [title, category, subtitle, *[item["text"] for item in support]]
    _assert_unique(all_strings, "content")

    carrier_copy = content.get("screen_carrier_element")
    if carrier_copy is not None:
        carrier_copy = _string(carrier_copy, "content.screen_carrier_element")
        if contract != "EDITORIAL_POSTER_5_TO_7":
            _fail("content.screen_carrier_element", "is only valid for EDITORIAL_POSTER_5_TO_7")
        matches = [item for item in support if _normalized(item["text"]) == _normalized(carrier_copy)]
        if len(matches) != 1:
            _fail("content.screen_carrier_element", "must match exactly one support element already in the designed inventory")

    result: dict[str, Any] = {
        "canvas": canvas,
        "text_contract": contract,
        "final_title": title,
        "category_label": category,
        "concept_contract": validate_concept_contract(
            _require(content, "concept_contract", "content")
        ),
        "supporting_copy": subtitle,
        "supporting_copy_role": supporting_copy_role,
        "poster_support_elements": support,
    }
    for key in ("speculative_function", "intrinsic_artifact_text_policy"):
        if key in content:
            result[key] = _string(content[key], f"content.{key}")
    for key in ("purpose_bearing_parts", "archive_identity_anchors"):
        if key in content:
            values = _list(content[key], f"content.{key}")
            if not 2 <= len(values) <= 4:
                _fail(f"content.{key}", "must contain 2–4 strings")
            result[key] = [_string(value, f"content.{key}[{index}]") for index, value in enumerate(values)]
    if "assembly_plan" in content:
        result["assembly_plan"] = validate_assembly_plan(content["assembly_plan"])
    if "source_asset_paths" in content:
        values = _list(content["source_asset_paths"], "content.source_asset_paths")
        if not 1 <= len(values) <= 5:
            _fail("content.source_asset_paths", "must contain 1–5 paths")
        result["source_asset_paths"] = [
            _string(value, f"content.source_asset_paths[{index}]") for index, value in enumerate(values)
        ]
        for index, value in enumerate(result["source_asset_paths"]):
            if not Path(value).is_absolute():
                _fail(f"content.source_asset_paths[{index}]", "must be an absolute local path")
    if carrier_copy is not None:
        result["screen_carrier_element"] = carrier_copy
    return result


def _catalog_ids(filename: str, key: str) -> set[str]:
    data = json.loads((DESIGN_SYSTEM / filename).read_text(encoding="utf-8"))
    return {item["id"] for item in data[key]}


def validate_manifest(manifest: Any) -> dict[str, Any]:
    """Validate the selector manifest fields consumed by the compiler."""
    if not isinstance(manifest, dict):
        _fail("manifest", "must be an object")
    schema = json.loads((DESIGN_SYSTEM / "manifest.schema.json").read_text(encoding="utf-8"))
    for key in schema["required"]:
        if key not in manifest:
            _fail("manifest", f"missing required field {key!r}")

    required_consumed_fields = {"text_contract", "title_zone"}
    for key in required_consumed_fields:
        _require(manifest, key, "manifest")
    string_fields = {
        "carrier", "layout_family", "layout_family_id", "layout_title_zone", "layout_object_slot",
        "layout_collision_rule", "layout_crop_rule", "layout_thumbnail_test", "subject_assembly", "subject_assembly_count",
        "subject_mass_rule", "composition_sentence", "subject_origin_mode", "render_treatment",
        "scale_role", "screen_state", "screen_content_role", "screen_content_source",
        "screen_display_language", "screen_copy_element", "focal_event", "release_zone", "palette",
        "gradient_topology", "primary_form", "type_mode", "detail_grammar", "text_contract", "title_zone",
    }
    for key in string_fields:
        _string(manifest[key], f"manifest.{key}")
    if manifest["text_contract"] not in TEXT_CONTRACTS:
        _fail("manifest.text_contract", "has an unsupported text contract")
    if manifest["layout_family_id"] not in _catalog_ids("layouts.json", "layouts"):
        _fail("manifest.layout_family_id", "is not a known layout")
    if manifest["subject_assembly"] not in SUBJECT_ASSEMBLIES:
        _fail("manifest.subject_assembly", "is not a known subject assembly")
    if manifest["subject_origin_mode"] not in SUBJECT_ORIGINS:
        _fail("manifest.subject_origin_mode", "is not a known subject origin")
    if manifest["render_treatment"] not in TREATMENTS:
        _fail("manifest.render_treatment", "is not a known render treatment")
    if manifest["screen_state"] not in SCREEN_STATES:
        _fail("manifest.screen_state", "is not a known screen state")

    arrays = ("layout_allowed_subject_assemblies", "layout_required_operators", "layout_support_zones", "layout_failure_signals")
    for key in arrays:
        values = _list(manifest[key], f"manifest.{key}")
        if key in {"layout_support_zones", "layout_failure_signals"} and not values:
            _fail(f"manifest.{key}", "must not be empty")
        for index, value in enumerate(values):
            _string(value, f"manifest.{key}[{index}]")
    primitives = _list(manifest["composition_primitives"], "manifest.composition_primitives")
    if len(primitives) < 4:
        _fail("manifest.composition_primitives", "must include the four composition primitives")
    for index, primitive in enumerate(primitives):
        _string(primitive, f"manifest.composition_primitives[{index}]")
    operators = _list(manifest["composition_operators"], "manifest.composition_operators")
    categories: set[str] = set()
    for index, operator in enumerate(operators):
        if not isinstance(operator, dict):
            _fail(f"manifest.composition_operators[{index}]", "must be an object")
        for key in ("id", "category", "definition"):
            _string(operator.get(key), f"manifest.composition_operators[{index}].{key}")
        categories.add(operator["category"])
    if not {"PRIMARY_RELATION", "FOCAL_OPERATION", "SUPPORT_ALIGNMENT"}.issubset(categories):
        _fail("manifest.composition_operators", "must include primary relation, focal operation, and support alignment")

    carrier_id = manifest.get("carrier_id")
    if carrier_id is not None:
        _string(carrier_id, "manifest.carrier_id")
        if carrier_id not in _catalog_ids("carriers.json", "carriers"):
            _fail("manifest.carrier_id", "is not a known carrier")
    for key in ("layout_attention_contract",):
        if not isinstance(manifest[key], dict):
            _fail(f"manifest.{key}", "must be an object")
    if manifest["screen_state"] == "CARRIER" and manifest["screen_copy_element"] == "NONE":
        _fail("manifest.screen_copy_element", "must identify the locked support string for CARRIER")
    if manifest["screen_state"] != "CARRIER" and manifest["screen_copy_element"] != "NONE":
        _fail("manifest.screen_copy_element", "must be NONE unless screen_state is CARRIER")
    return manifest


def _brief_texts(brief: dict[str, Any]) -> list[dict[str, Any]]:
    inventory = brief.get("designed_text_inventory")
    if not isinstance(inventory, list):
        _fail("brief.designed_text_inventory", "must be an array")
    texts: list[dict[str, Any]] = []
    for index, item in enumerate(inventory):
        if not isinstance(item, dict):
            _fail(f"brief.designed_text_inventory[{index}]", "must be an object")
        _string(item.get("id"), f"brief.designed_text_inventory[{index}].id")
        texts.append(item)
        _string(item.get("text"), f"brief.designed_text_inventory[{index}].text")
    return texts


def validate_brief(brief: Any) -> dict[str, Any]:
    """Validate observable output invariants, including the opaque background gate."""
    if not isinstance(brief, dict):
        _fail("brief", "must be an object")
    required = json.loads((DESIGN_SYSTEM / "generation-brief.schema.json").read_text(encoding="utf-8"))["required"]
    for key in required:
        if key not in brief:
            _fail("brief", f"missing required field {key!r}")
    if brief["brief_version"] != 1:
        _fail("brief.brief_version", "must be 1")
    _validate_canvas(brief["canvas"], "brief.canvas")
    contract = brief["text_contract"]
    if contract not in TEXT_CONTRACTS:
        _fail("brief.text_contract", "is unsupported")
    inventory = _brief_texts(brief)
    count = brief["designed_text_count"]
    if count != len(inventory):
        _fail("brief.designed_text_count", "must equal designed_text_inventory length")
    if contract == "THREE_ELEMENT_COVER" and count != 3:
        _fail("brief.designed_text_inventory", "THREE_ELEMENT_COVER must contain exactly 3 designed strings")
    if contract == "EDITORIAL_POSTER_5_TO_7" and not 5 <= count <= 7:
        _fail("brief.designed_text_inventory", "EDITORIAL_POSTER_5_TO_7 must contain 5–7 designed strings")
    _assert_unique([item["text"] for item in inventory], "brief.designed_text_inventory")
    inventory_ids = {item["id"] for item in inventory}
    if not {"FINAL_TITLE", "CATEGORY_LABEL"}.issubset(inventory_ids):
        _fail("brief.designed_text_inventory", "requires FINAL_TITLE and CATEGORY_LABEL")
    support_roles = inventory_ids & SUPPORTING_COPY_ROLES
    if len(support_roles) != 1:
        _fail("brief.designed_text_inventory", "requires exactly one of MICRO_SUBTITLE or SUPPORTING_DECK")

    typography = brief["typography_contract"]
    if not isinstance(typography, dict):
        _fail("brief.typography_contract", "must be an object")
    for key in ("mode", "title", "category_label", "supporting_copy", "cluster", "thumbnail_rule"):
        _require(typography, key, "brief.typography_contract")
    if typography["mode"] not in {"SHORT_TITLE_EXPANDED", "STANDARD_TITLE_BLOCK", "LONG_TITLE_STACK"}:
        _fail("brief.typography_contract.mode", "is not a known title mode")
    for key in ("title", "category_label", "supporting_copy", "cluster"):
        if not isinstance(typography[key], dict):
            _fail(f"brief.typography_contract.{key}", "must be an object")
    title_contract = typography["title"]
    for key in ("visible_glyph_count", "zone", "type_mode", "attention_percent", "line_count", "width_percent", "height_percent", "weight", "tracking", "contrast_target", "rule"):
        _require(title_contract, key, "brief.typography_contract.title")
    title_item = next(item for item in inventory if item["id"] == "FINAL_TITLE")
    visible_glyph_count = len("".join(title_item["text"].split()))
    if title_contract["visible_glyph_count"] != visible_glyph_count:
        _fail("brief.typography_contract.title.visible_glyph_count", "must match FINAL_TITLE")
    expected_mode = "SHORT_TITLE_EXPANDED" if visible_glyph_count <= 8 else ("STANDARD_TITLE_BLOCK" if visible_glyph_count <= 24 else "LONG_TITLE_STACK")
    if typography["mode"] != expected_mode:
        _fail("brief.typography_contract.mode", f"must be {expected_mode} for this title length")
    _numeric_range(title_contract["attention_percent"], "brief.typography_contract.title.attention_percent", minimum=0, maximum=100)
    _numeric_range(title_contract["line_count"], "brief.typography_contract.title.line_count", minimum=1, maximum=5)
    _numeric_range(title_contract["width_percent"], "brief.typography_contract.title.width_percent", minimum=1, maximum=100)
    _numeric_range(title_contract["height_percent"], "brief.typography_contract.title.height_percent", minimum=1, maximum=100)
    for key in ("zone", "type_mode", "weight", "tracking", "contrast_target", "rule"):
        _string(title_contract[key], f"brief.typography_contract.title.{key}")
    if typography["supporting_copy"].get("role") not in support_roles:
        _fail("brief.typography_contract.supporting_copy.role", "must match the designed supporting-copy role")
    for key in ("line_count", "full_size_min_x_height_percent", "title_cap_height_ratio", "rule", "contrast_target"):
        _require(typography["supporting_copy"], key, "brief.typography_contract.supporting_copy")
    _numeric_range(typography["supporting_copy"]["line_count"], "brief.typography_contract.supporting_copy.line_count", minimum=1, maximum=2)
    _numeric_range(typography["supporting_copy"]["title_cap_height_ratio"], "brief.typography_contract.supporting_copy.title_cap_height_ratio", minimum=0, maximum=1)
    min_x_height = typography["supporting_copy"]["full_size_min_x_height_percent"]
    if isinstance(min_x_height, bool) or not isinstance(min_x_height, (int, float)) or min_x_height < 1:
        _fail("brief.typography_contract.supporting_copy.full_size_min_x_height_percent", "must be at least 1%")
    for key in ("line_count", "full_size_min_x_height_percent", "title_cap_height_ratio", "rule", "contrast_target"):
        _require(typography["category_label"], key, "brief.typography_contract.category_label")
    _numeric_range(typography["category_label"]["line_count"], "brief.typography_contract.category_label.line_count", minimum=1, maximum=1)
    _numeric_range(typography["category_label"]["title_cap_height_ratio"], "brief.typography_contract.category_label.title_cap_height_ratio", minimum=0, maximum=1)
    category_x_height = typography["category_label"]["full_size_min_x_height_percent"]
    if isinstance(category_x_height, bool) or not isinstance(category_x_height, (int, float)) or category_x_height < 1:
        _fail("brief.typography_contract.category_label.full_size_min_x_height_percent", "must be at least 1%")
    _string(typography["cluster"].get("rule"), "brief.typography_contract.cluster.rule")
    _string(typography["thumbnail_rule"], "brief.typography_contract.thumbnail_rule")

    normalized_concept = validate_concept_contract(
        brief["concept_contract"], "brief.concept_contract"
    )
    if normalized_concept != brief["concept_contract"]:
        _fail("brief.concept_contract", "must preserve the normalized locked concept contract")

    background = brief["background"]
    if not isinstance(background, dict):
        _fail("brief.background", "must be an object")
    if background.get("full_bleed_opaque") is not True:
        _fail("brief.background.full_bleed_opaque", "must be true")
    if background.get("requirement") != BACKGROUND_REQUIREMENT:
        _fail("brief.background.requirement", "must include the exact full-canvas opaque background requirement")
    if brief.get("opaque_full_bleed_background_requirement") != BACKGROUND_REQUIREMENT:
        _fail("brief.opaque_full_bleed_background_requirement", "must repeat the exact background requirement")

    carrier = brief["carrier_contract"]
    if not isinstance(carrier, dict):
        _fail("brief.carrier_contract", "must be an object")
    subject = brief["subject"]
    if not isinstance(subject, dict):
        _fail("brief.subject", "must be an object")
    screen_state = subject.get("screen_state")
    screen_copy = subject.get("screen_copy_element")
    placements = [item.get("placement") for item in inventory]
    if screen_state == "CARRIER":
        if placements.count("SCREEN_CARRIER") != 1:
            _fail("brief.designed_text_inventory", "CARRIER must have exactly one SCREEN_CARRIER placement")
        if screen_copy not in {item["text"] for item in inventory}:
            _fail("brief.subject.screen_copy_element", "must be present exactly once in the designed inventory")
        matching = [item for item in inventory if item["text"] == screen_copy]
        if len(matching) != 1 or matching[0].get("placement") != "SCREEN_CARRIER":
            _fail("brief.subject.screen_copy_element", "must not have an external duplicate")
    elif "SCREEN_CARRIER" in placements:
        _fail("brief.designed_text_inventory", "SCREEN_CARRIER placement requires subject screen_state CARRIER")
    if screen_state == "SIGNAL" and screen_copy != "NONE":
        _fail("brief.subject.screen_copy_element", "SIGNAL cannot carry readable copy")

    composition = brief["composition"]
    palette = brief["palette"]
    for key, value in (("composition", composition), ("subject", subject), ("palette", palette)):
        if not isinstance(value, dict):
            _fail(f"brief.{key}", "must be an object")
    assembly = subject.get("assembly")
    if assembly not in SUBJECT_ASSEMBLIES:
        _fail("brief.subject.assembly", "is not a known subject assembly")
    if composition.get("subject_assembly") != assembly:
        _fail("brief.composition.subject_assembly", "must match brief.subject.assembly")
    _string(composition.get("subject_assembly_count"), "brief.composition.subject_assembly_count")
    if composition.get("subject_mass_rule") != subject.get("mass_rule"):
        _fail("brief.composition.subject_mass_rule", "must match brief.subject.mass_rule")
    plan = subject.get("assembly_plan")
    if assembly == "SINGLE_OBJECT":
        if plan is not None:
            _fail("brief.subject.assembly_plan", "must be omitted for SINGLE_OBJECT")
    else:
        normalized_plan = validate_assembly_plan(plan, "brief.subject.assembly_plan")
        if normalized_plan["mode"] != assembly:
            _fail("brief.subject.assembly_plan.mode", "must match brief.subject.assembly")
    if subject.get("origin_mode") == "SPECULATIVE_OBJECT":
        if not isinstance(subject.get("function"), str) or not subject["function"].strip():
            _fail("brief.subject.function", "is required for SPECULATIVE_OBJECT")
        morphology = subject.get("morphology")
        if not isinstance(morphology, dict) or morphology.get("id") in (None, "", "NOT_APPLICABLE"):
            _fail("brief.subject.morphology", "is required for SPECULATIVE_OBJECT")
        for field in ("name", "source", "shape_ancestry", "definition", "silhouette", "exaggeration", "aperture_rule", "material_direction"):
            _string(morphology.get(field), f"brief.subject.morphology.{field}")
        if morphology["source"] not in {"ARCHETYPE_PRESET", "CUSTOM"}:
            _fail("brief.subject.morphology.source", "must be ARCHETYPE_PRESET or CUSTOM")
        cues = _list(morphology.get("construction_cues"), "brief.subject.morphology.construction_cues")
        if not 1 <= len(cues) <= 4:
            _fail("brief.subject.morphology.construction_cues", "must contain 1–4 strings")
        for index, cue in enumerate(cues):
            _string(cue, f"brief.subject.morphology.construction_cues[{index}]")
    if subject.get("origin_mode") == "ARCHIVE_ARTIFACT" and subject.get("render_treatment") == "PALETTE_ASSIMILATED":
        _fail("brief.subject.render_treatment", "archive artifacts cannot use PALETTE_ASSIMILATED")

    generation_call = brief["generation_call"]
    if not isinstance(generation_call, dict):
        _fail("brief.generation_call", "must be an object")
    style_reference = _string(generation_call.get("style_reference_path"), "brief.generation_call.style_reference_path")
    source_assets = _list(generation_call.get("source_asset_paths"), "brief.generation_call.source_asset_paths")
    referenced = _list(generation_call.get("referenced_image_paths"), "brief.generation_call.referenced_image_paths")
    for key, values in (("source_asset_paths", source_assets), ("referenced_image_paths", referenced)):
        for index, value in enumerate(values):
            _string(value, f"brief.generation_call.{key}[{index}]")
    if not referenced:
        _fail("brief.generation_call.referenced_image_paths", "must include the style reference")
    if style_reference not in referenced:
        _fail("brief.generation_call.referenced_image_paths", "must include the style reference")
    if referenced[0] != style_reference:
        _fail("brief.generation_call.referenced_image_paths", "must place the style reference first")
    if any(path not in referenced for path in source_assets):
        _fail("brief.generation_call.referenced_image_paths", "must include every source asset")
    expected_references = list(dict.fromkeys([style_reference, *source_assets]))
    if referenced != expected_references:
        _fail("brief.generation_call.referenced_image_paths", "must exactly equal style reference plus locked source assets")
    if subject.get("origin_mode") == "NOT_APPLICABLE_SUPPLIED_IMAGE" and not source_assets:
        _fail("brief.generation_call.source_asset_paths", "supplied-image mode requires at least one source asset")
    _string(generation_call.get("reference_instruction"), "brief.generation_call.reference_instruction")
    for key in ("composition_sentence", "title_zone", "object_slot", "support_zones", "collision_rule", "crop_rule", "release_zone"):
        if key == "support_zones":
            if not brief["composition"].get(key):
                _fail(f"brief.composition.{key}", "must not be empty")
        else:
            _string(brief["composition"].get(key), f"brief.composition.{key}")
    if not brief["negative_constraints"]:
        _fail("brief.negative_constraints", "must not be empty")
    _string(brief["generator_instruction"], "brief.generator_instruction")
    return brief


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError(f"{path}: cannot read JSON ({error})") from error


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content", type=Path, help="validate a generation content JSON file")
    parser.add_argument("--manifest", type=Path, help="validate a selector manifest JSON file")
    parser.add_argument("--brief", type=Path, help="validate a compiled generation brief JSON file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    targets = [value for value in (args.content, args.manifest, args.brief) if value]
    if len(targets) != 1:
        print("choose exactly one of --content, --manifest, or --brief", file=sys.stderr)
        return 2
    try:
        if args.content:
            validate_content(load_json(args.content))
            message = "content"
        elif args.manifest:
            validate_manifest(load_json(args.manifest))
            message = "manifest"
        else:
            validate_brief(load_json(args.brief))
            message = "brief"
    except ValidationError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 2
    print(f"PASS: valid generation {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
