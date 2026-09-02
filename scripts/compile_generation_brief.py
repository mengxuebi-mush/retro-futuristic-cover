#!/usr/bin/env python3
"""Compile locked content and a selector manifest into a generator-ready brief."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from validate_generation_brief import (
    BACKGROUND_REQUIREMENT,
    ValidationError,
    load_json,
    validate_brief,
    validate_content,
    validate_manifest,
)


ROOT = Path(__file__).resolve().parents[1]
DESIGN_SYSTEM = ROOT / "design-system"


def _load_catalog(filename: str, key: str) -> list[dict[str, Any]]:
    data = json.loads((DESIGN_SYSTEM / filename).read_text(encoding="utf-8"))
    return data[key]


def _carrier_id(manifest: dict[str, Any]) -> str:
    if manifest.get("carrier_id"):
        return manifest["carrier_id"]
    matches = [item["id"] for item in _load_catalog("carriers.json", "carriers") if item["name"] == manifest["carrier"]]
    if len(matches) != 1:
        raise ValidationError("manifest.carrier: cannot resolve carrier id")
    return matches[0]


def _carrier_contract(manifest: dict[str, Any]) -> dict[str, Any]:
    carrier_id = _carrier_id(manifest)
    catalog = next(item for item in _load_catalog("carriers.json", "carriers") if item["id"] == carrier_id)
    return {
        "id": carrier_id,
        "name": manifest.get("carrier", catalog["name"]),
        "text_contract": manifest["text_contract"],
        "critical_signals": manifest.get("carrier_signals", catalog["critical_signals"]),
        "forbidden_signals": catalog["forbidden_signals"],
        "safe_margin": catalog["safe_margin"],
        "title_priority": catalog["title_priority"],
        "object_scale": catalog["object_scale"],
        "crop_behavior": catalog["crop_behavior"],
    }


def _text_inventory(content: dict[str, Any], manifest: dict[str, Any]) -> list[dict[str, Any]]:
    inventory = [
        {"id": "FINAL_TITLE", "text": content["final_title"], "role": "dominant title", "placement": "TITLE_ZONE"},
        {"id": "CATEGORY_LABEL", "text": content["category_label"], "role": "top category label", "placement": "CATEGORY_ZONE"},
        {"id": "MICRO_SUBTITLE", "text": content["micro_subtitle"], "role": "quiet micro-subtitle", "placement": "MICRO_ZONE"},
    ]
    support_zones = manifest["layout_support_zones"]
    carrier_copy = content.get("screen_carrier_element")
    for index, element in enumerate(content["poster_support_elements"], start=1):
        text = element["text"]
        is_carrier = carrier_copy is not None and text == carrier_copy
        placement = "SCREEN_CARRIER" if is_carrier else (element.get("anchor") or support_zones[(index - 1) % len(support_zones)])
        inventory.append({
            "id": f"POSTER_SUPPORT_{index:02d}",
            "text": text,
            "role": element.get("role", "factual poster support"),
            "placement": placement,
            **({"source": element["source"]} if "source" in element else {}),
        })
    if manifest["screen_state"] == "CARRIER":
        if carrier_copy is None or manifest["screen_copy_element"] != carrier_copy:
            raise ValidationError("content.screen_carrier_element: must match manifest.screen_copy_element for CARRIER")
    elif carrier_copy is not None:
        raise ValidationError("content.screen_carrier_element: manifest does not resolve CARRIER")
    return inventory


def _composition(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "layout_family_id": manifest["layout_family_id"],
        "layout_family": manifest["layout_family"],
        "attention_contract": manifest["layout_attention_contract"],
        "composition_sentence": manifest["composition_sentence"],
        "subject_assembly": manifest["subject_assembly"],
        "subject_mass_rule": manifest["subject_mass_rule"],
        "operators": manifest["composition_operators"],
        "focal_event": {
            "id": manifest.get("focal_event_id", ""),
            "definition": manifest["focal_event"],
            "thumbnail_test": manifest.get("focal_event_thumbnail_test", ""),
        },
        "title_zone": manifest["title_zone"],
        "object_slot": manifest["layout_object_slot"],
        "support_zones": manifest["layout_support_zones"],
        "collision_rule": manifest["layout_collision_rule"],
        "crop_rule": manifest["layout_crop_rule"],
        "release_zone": manifest["release_zone"],
        "failure_signals": manifest["layout_failure_signals"],
        "thumbnail_test": manifest["layout_thumbnail_test"],
    }


def _hero_identity_anchors(manifest: dict[str, Any]) -> list[str]:
    hero = manifest.get("hero_object")
    if isinstance(hero, dict) and isinstance(hero.get("identity_anchors"), list):
        return hero["identity_anchors"]
    return []


def _subject(content: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    origin = manifest["subject_origin_mode"]
    anchors = content.get("archive_identity_anchors", _hero_identity_anchors(manifest)) if origin == "ARCHIVE_ARTIFACT" else []
    if origin == "ARCHIVE_ARTIFACT" and not 2 <= len(anchors) <= 4:
        raise ValidationError("subject.archive_identity_anchors: archive subjects require 2–4 identity anchors")
    if origin == "SPECULATIVE_OBJECT" and not content.get("speculative_function"):
        raise ValidationError("content.speculative_function: speculative subjects require one hypothetical function")
    subject = {
        "origin_mode": origin,
        "origin_definition": manifest.get("subject_origin_definition", ""),
        "assembly": manifest["subject_assembly"],
        "mass_rule": manifest["subject_mass_rule"],
        "render_treatment": manifest["render_treatment"],
        "render_definition": manifest.get("render_treatment_definition", ""),
        "color_rule": manifest.get("render_color_rule", ""),
        "scale_role": manifest["scale_role"],
        "scale": manifest.get("scale_role_scale", ""),
        "scale_behavior": manifest.get("scale_role_behavior", ""),
        "object_family_id": manifest.get("object_family_id", "NONE"),
        "object_family": manifest.get("object_family", "NONE"),
        "function": content.get("speculative_function", ""),
        "purpose_bearing_parts": content.get("purpose_bearing_parts", []),
        "archive_identity_anchors": anchors,
        "intrinsic_artifact_text_policy": content.get(
            "intrinsic_artifact_text_policy",
            manifest.get("intrinsic_artifact_text_policy", "NOT_APPLICABLE"),
        ),
        "morphology": {
            "id": manifest.get("speculative_morphology", "NOT_APPLICABLE"),
            "name": manifest.get("speculative_morphology_name", manifest.get("speculative_morphology", "NOT_APPLICABLE")),
            "source": manifest.get(
                "speculative_morphology_source",
                "ARCHETYPE_PRESET" if manifest.get("speculative_morphology") not in (None, "NOT_APPLICABLE") else "NOT_APPLICABLE",
            ),
            "shape_ancestry": manifest.get(
                "speculative_morphology_shape_ancestry",
                manifest.get("speculative_morphology_silhouette", "NOT_APPLICABLE"),
            ),
            "definition": manifest.get("speculative_morphology_definition", "NOT_APPLICABLE"),
            "silhouette": manifest.get("speculative_morphology_silhouette", "NOT_APPLICABLE"),
            "exaggeration": manifest.get("speculative_morphology_exaggeration", "NOT_APPLICABLE"),
            "aperture_rule": manifest.get("speculative_morphology_aperture_rule", "NOT_APPLICABLE"),
            "construction_cues": manifest.get("speculative_morphology_construction_cues", "NOT_APPLICABLE"),
            "material_direction": manifest.get("speculative_morphology_material_direction", "NOT_APPLICABLE"),
            "hard_failures": manifest.get("speculative_global_hard_failures", "NOT_APPLICABLE"),
        },
        "screen_state": manifest["screen_state"],
        "screen_content_role": manifest["screen_content_role"],
        "screen_content_source": manifest["screen_content_source"],
        "screen_display_language": manifest["screen_display_language"],
        "screen_copy_element": manifest["screen_copy_element"],
        "screen_rendering_rule": manifest.get("screen_rendering_rule", ""),
        "screen_text_rule": manifest.get("screen_text_rule", ""),
        "screen_instance_rule": manifest.get("screen_instance_rule", ""),
    }
    if origin == "SPECULATIVE_OBJECT" and manifest.get("speculative_morphology") in (None, "NOT_APPLICABLE"):
        raise ValidationError("manifest.speculative_morphology: speculative subjects require one morphology")
    if origin == "ARCHIVE_ARTIFACT" and manifest["render_treatment"] == "PALETTE_ASSIMILATED":
        raise ValidationError("manifest.render_treatment: archive artifacts cannot use PALETTE_ASSIMILATED")
    return subject


def _palette(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": manifest.get("palette_id", ""),
        "family": manifest.get("palette_family", manifest["palette"]),
        "color_complexity": manifest.get("color_complexity", ""),
        "active_hues": manifest.get("active_hues", []),
        "derived_tints": manifest.get("derived_tints", ""),
        "area_hierarchy": manifest.get("area_hierarchy", ""),
        "tonal_regime": manifest.get("tonal_regime", ""),
        "harmony_mode": manifest.get("harmony_mode", ""),
        "coral_role": manifest.get("coral_role", ""),
        "gradient_topology": manifest["gradient_topology"],
        "gradient_direction": manifest.get("gradient_direction", ""),
        "focal_mode": manifest.get("focal_mode", ""),
        "primary_form": manifest["primary_form"],
        "editorial_device": manifest.get("editorial_device", "NONE"),
        "detail_roles": manifest.get("detail_roles", {}),
        "type_mode": manifest["type_mode"],
        "alignment_system": manifest.get("alignment_system", ""),
    }


def _negative_constraints(manifest: dict[str, Any], subject: dict[str, Any], carrier: dict[str, Any]) -> list[str]:
    constraints = [
        *carrier["forbidden_signals"],
        *manifest["layout_failure_signals"],
        "No designed letters, words, numbers, logos, watermarks, pseudo-text, or copy outside the locked inventory.",
        "Keep the title first at thumbnail size and preserve the title glyph clear zone.",
        "Resolve all visible objects as one perceptually unified subject mass; do not create equal-weight hero objects.",
    ]
    if subject["origin_mode"] == "ABSTRACT_FORM":
        constraints.append("Keep the abstract form non-referential; no fake controls, interface, product seams, or invented labels.")
    if subject["origin_mode"] == "ARCHIVE_ARTIFACT":
        constraints.append("Preserve historical proportions, provenance, identity anchors, and material transitions; do not redesign the artifact.")
    if subject["origin_mode"] == "SPECULATIVE_OBJECT":
        constraints.extend([
            "Do not depict a present-day product with rounded corners, faceted contemporary vehicle surfaces, or cold minimal-product language.",
            "No black panoramic glass band, full-width LED strip, touchscreen-first controls, RGB light, or chrome-covered body.",
        ])
        failures = manifest.get("speculative_global_hard_failures")
        if isinstance(failures, list):
            constraints.extend(failures)
    if subject["screen_state"] == "SIGNAL":
        constraints.append(subject["screen_text_rule"] or "No readable screen content; use one nonverbal low-resolution signal only.")
    if subject["screen_state"] == "CARRIER":
        constraints.append("The screen carries exactly one locked support string and that string must not appear in any external location.")
    return list(dict.fromkeys(item for item in constraints if isinstance(item, str) and item.strip()))


def _quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _generator_instruction(brief: dict[str, Any]) -> str:
    content = brief["designed_text_inventory"]
    text_lines = [
        f'{item["id"]}={_quote(item["text"])} at {item["placement"]}'
        for item in content
    ]
    composition = brief["composition"]
    subject = brief["subject"]
    palette = brief["palette"]
    background = brief["background"]
    lines = [
        background["requirement"],
        f'Carrier {brief["carrier_contract"]["id"]}; canvas {brief["canvas"]["width"]}x{brief["canvas"]["height"]} ({brief["canvas"]["ratio"]}); text contract {brief["text_contract"]}.',
        "Render exactly these designed text elements once each: " + "; ".join(text_lines) + ". No other designed copy.",
        f'Composition: {composition["composition_sentence"]}; focal event {composition["focal_event"]["id"]}: {composition["focal_event"]["definition"]}; title zone {composition["title_zone"]}; object slot {composition["object_slot"]}; support zones {", ".join(composition["support_zones"])}; collision rule {composition["collision_rule"]}; crop rule {composition["crop_rule"]}; release zone {composition["release_zone"]}.',
        f'Subject: {subject["origin_mode"]}, assembly {subject["assembly"]}, object family {subject["object_family_id"]}, treatment {subject["render_treatment"]}, scale {subject["scale_role"]}; function {subject["function"] or "not applicable"}; archive anchors {", ".join(subject["archive_identity_anchors"]) or "not applicable"}; intrinsic artifact text policy {subject["intrinsic_artifact_text_policy"]}; morphology {json.dumps(subject["morphology"], ensure_ascii=False)}.',
        f'Screen: {subject["screen_state"]}; {subject["screen_rendering_rule"] or subject["screen_text_rule"] or "no generated screen behavior"}',
        f'Palette: {palette["family"]} / {palette["color_complexity"]}; active hues {", ".join(palette["active_hues"]) or "locked manifest hues"}; area hierarchy {palette["area_hierarchy"]}; topology {palette["gradient_topology"]}; type mode {palette["type_mode"]}; focal mode {palette["focal_mode"]}; details {json.dumps(palette["detail_roles"], ensure_ascii=False)}.',
    ]
    return "\n".join(lines)


def compile_brief(content_input: Any, manifest_input: Any) -> dict[str, Any]:
    content = validate_content(content_input)
    manifest = validate_manifest(manifest_input)
    if content["text_contract"] != manifest["text_contract"]:
        raise ValidationError("content.text_contract: does not match manifest.text_contract")
    if manifest["screen_state"] == "CARRIER" and manifest.get("carrier_id", "") != "EDITORIAL_POSTER":
        raise ValidationError("manifest.screen_state: CARRIER requires EDITORIAL_POSTER")
    if manifest["screen_state"] == "CARRIER" and "screen_carrier_element" not in content:
        raise ValidationError("content.screen_carrier_element: required for manifest CARRIER")

    carrier = _carrier_contract(manifest)
    inventory = _text_inventory(content, manifest)
    subject = _subject(content, manifest)
    brief: dict[str, Any] = {
        "brief_version": 1,
        "canvas": content["canvas"],
        "carrier_contract": carrier,
        "text_contract": content["text_contract"],
        "designed_text_inventory": inventory,
        "designed_text_count": len(inventory),
        "composition": _composition(manifest),
        "subject": subject,
        "palette": _palette(manifest),
        "background": {
            "id": "OPAQUE_BACKGROUND_BASE",
            "full_bleed_opaque": True,
            "requirement": BACKGROUND_REQUIREMENT,
            "coverage": "100% of the canvas behind every element and every cropped edge",
        },
        "negative_constraints": [],
        "opaque_full_bleed_background_requirement": BACKGROUND_REQUIREMENT,
    }
    brief["negative_constraints"] = _negative_constraints(manifest, subject, carrier)
    brief["generator_instruction"] = _generator_instruction(brief)
    return validate_brief(brief)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--content", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        brief = compile_brief(load_json(args.content), load_json(args.manifest))
    except (ValidationError, OSError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 2
    print(json.dumps(brief, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
