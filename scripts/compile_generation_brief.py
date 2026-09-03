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
STYLE_REFERENCE = ROOT / "assets" / "visual-reference.png"


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
    support_role = content["supporting_copy_role"]
    support_placement = "MICRO_ZONE" if support_role == "MICRO_SUBTITLE" else "DECK_ZONE"
    support_role_name = "quiet micro-subtitle" if support_role == "MICRO_SUBTITLE" else "readable supporting deck"
    inventory = [
        {"id": "FINAL_TITLE", "text": content["final_title"], "role": "dominant title", "placement": "TITLE_ZONE"},
        {"id": "CATEGORY_LABEL", "text": content["category_label"], "role": "top category label", "placement": "CATEGORY_ZONE"},
        {"id": support_role, "text": content["supporting_copy"], "role": support_role_name, "placement": support_placement},
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


def _typography_contract(content: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    catalog = json.loads((DESIGN_SYSTEM / "typography-contracts.json").read_text(encoding="utf-8"))
    glyph_count = len("".join(content["final_title"].split()))
    if glyph_count <= catalog["short_title_max_visible_glyphs"]:
        mode = "SHORT_TITLE_EXPANDED"
    elif glyph_count <= catalog["standard_title_max_visible_glyphs"]:
        mode = "STANDARD_TITLE_BLOCK"
    else:
        mode = "LONG_TITLE_STACK"
    title = dict(catalog["title_modes"][mode])
    if mode == "SHORT_TITLE_EXPANDED" and manifest["layout_family_id"] == "TYPE_DOMINANT_FIELD":
        title["width_percent"] = title.pop("type_dominant_width_percent")
    else:
        title.pop("type_dominant_width_percent", None)
    title.update({
        "visible_glyph_count": glyph_count,
        "zone": manifest["title_zone"],
        "type_mode": manifest["type_mode"],
        "attention_percent": manifest["layout_attention_contract"]["title_percent"],
        "contrast_target": catalog["global"]["title_contrast_target"],
    })
    supporting_copy = dict(catalog["support_modes"][content["supporting_copy_role"]])
    supporting_copy.update({
        "role": content["supporting_copy_role"],
        "text": content["supporting_copy"],
        "contrast_target": catalog["global"]["support_contrast_target"],
    })
    category = dict(catalog["category_label"])
    category.update({
        "text": content["category_label"],
        "contrast_target": catalog["global"]["support_contrast_target"],
    })
    return {
        "mode": mode,
        "title": title,
        "category_label": category,
        "supporting_copy": supporting_copy,
        "cluster": {
            "alignment_system": manifest.get("alignment_system", ""),
            "support_zones": manifest["layout_support_zones"],
            "rule": catalog["global"]["cluster_rule"],
        },
        "thumbnail_rule": catalog["global"]["thumbnail_rule"],
    }


def _generation_call(content: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    source_assets = content.get("source_asset_paths", [])
    if manifest.get("source_asset_mode", "NONE") != "NONE" and not source_assets:
        raise ValidationError("content.source_asset_paths: supplied-image mode requires at least one source asset path")
    paths = list(dict.fromkeys([str(STYLE_REFERENCE), *source_assets]))
    return {
        "style_reference_path": str(STYLE_REFERENCE),
        "source_asset_paths": source_assets,
        "referenced_image_paths": paths,
        "reference_instruction": (
            "Attach every referenced_image_path to the image-generation call. Treat visual-reference.png as style-only: "
            "use its hierarchy, spacing, atmosphere, grain, and geometric restraint, but never copy its literal text, numbers, or card grid. "
            "Treat source_asset_paths as content assets whose locked identity anchors must be preserved."
        ),
    }


def _composition(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "layout_family_id": manifest["layout_family_id"],
        "layout_family": manifest["layout_family"],
        "attention_contract": manifest["layout_attention_contract"],
        "composition_sentence": manifest["composition_sentence"],
        "subject_assembly": manifest["subject_assembly"],
        "subject_assembly_count": manifest["subject_assembly_count"],
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
        **({"assembly_plan": content["assembly_plan"]} if "assembly_plan" in content else {}),
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


def _concept_instruction(concept: dict[str, Any]) -> str:
    return (
        f'Concept contract: communicate {_quote(concept["message_anchor"])} through visible subject behavior '
        f'{_quote(concept["subject_behavior"])}. Required visible evidence: '
        f'{"; ".join(concept["visible_evidence"])}. Semantic direction: '
        f'{_quote(concept["semantic_direction"])}. This evidence must remain understandable from the subject and '
        'background without relying on the subtitle. Do not substitute a generic symbol whose only rationale is '
        'future, guidance, progress, or possibility.'
    )


def _negative_constraints(
    manifest: dict[str, Any],
    subject: dict[str, Any],
    carrier: dict[str, Any],
    concept: dict[str, Any],
) -> list[str]:
    constraints = [
        *carrier["forbidden_signals"],
        *manifest["layout_failure_signals"],
        "No designed letters, words, numbers, logos, watermarks, pseudo-text, or copy outside the locked inventory.",
        "Keep the title first at thumbnail size and preserve the title glyph clear zone.",
        "Unify visible objects through the planned spatial relation while preserving the required assembly count; do not create unrelated equal-weight hero objects.",
        *[f"Do not visually imply {reading}." for reading in concept["must_not_imply"]],
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
    if subject["assembly"] == "COMPOUND_SET":
        constraints.append("Do not fuse the listed complete members into one object; internal parts, openings, and attached components do not count as members.")
    if subject["assembly"] == "PRIMARY_SATELLITES":
        constraints.append("Do not lose the satellites inside the primary and do not promote a satellite into an equal-weight hero.")
    if subject["assembly"] == "REPEATED_FAMILY":
        constraints.append("Do not collapse the repeated family into one object or vary instances into unrelated object types.")
    return list(dict.fromkeys(item for item in constraints if isinstance(item, str) and item.strip()))


def _quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _assembly_instruction(subject: dict[str, Any], composition: dict[str, Any]) -> str:
    assembly = subject["assembly"]
    count = composition["subject_assembly_count"]
    mass_rule = subject["mass_rule"]
    if assembly == "SINGLE_OBJECT":
        return f"Assembly: SINGLE_OBJECT; expected count {count}; mass rule {mass_rule}."
    plan = subject["assembly_plan"]
    serialized = json.dumps(plan, ensure_ascii=False, separators=(",", ":"))
    if assembly == "COMPOUND_SET":
        observability = "Each listed member must remain a complete, independently countable object at full size and 25%; internal parts do not count."
    elif assembly == "PRIMARY_SATELLITES":
        observability = "The primary and every satellite must remain traceable at full size and 25%, while the primary preserves the specified weight ratio."
    else:
        observability = "Show the specified instance count of one recognizable family along the named path, with exactly one focal instance."
    return f"Assembly: {assembly}; expected count {count}; mass rule {mass_rule}; member plan {serialized}. {observability}"


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
    concept = brief["concept_contract"]
    typography = brief["typography_contract"]
    title = typography["title"]
    category = typography["category_label"]
    supporting = typography["supporting_copy"]
    cluster = typography["cluster"]
    lines = [
        background["requirement"],
        f'Carrier {brief["carrier_contract"]["id"]}; canvas {brief["canvas"]["width"]}x{brief["canvas"]["height"]} ({brief["canvas"]["ratio"]}); text contract {brief["text_contract"]}.',
        "Render exactly these designed text elements once each: " + "; ".join(text_lines) + ". No other designed copy.",
        _concept_instruction(concept),
        (
            f'Typography: {typography["mode"]}; FINAL_TITLE has {title["visible_glyph_count"]} visible glyphs and must form the first visual mass in {title["zone"]}; '
            f'target {title["width_percent"][0]}–{title["width_percent"][1]}% of canvas width and {title["height_percent"][0]}–{title["height_percent"][1]}% of canvas height across {title["line_count"][0]}–{title["line_count"][1]} line(s); '
            f'weight {title["weight"]}; tracking {title["tracking"]}; {title["contrast_target"]}; {title["rule"]} '
            f'CATEGORY_LABEL: full-size x-height at least {category["full_size_min_x_height_percent"]}% of canvas height and {category["title_cap_height_ratio"][0]}–{category["title_cap_height_ratio"][1]} of title cap height; {category["rule"]} '
            f'Supporting copy {supporting["role"]}: {supporting["rule"]} Use {supporting["line_count"][0]}–{supporting["line_count"][1]} line(s), '
            f'full-size x-height at least {supporting["full_size_min_x_height_percent"]}% of canvas height, and {supporting["title_cap_height_ratio"][0]}–{supporting["title_cap_height_ratio"][1]} of title cap height. '
            f'{cluster["rule"]} {typography["thumbnail_rule"]}'
        ),
        f'Composition: {composition["composition_sentence"]}; focal event {composition["focal_event"]["id"]}: {composition["focal_event"]["definition"]}; title zone {composition["title_zone"]}; object slot {composition["object_slot"]}; support zones {", ".join(composition["support_zones"])}; collision rule {composition["collision_rule"]}; crop rule {composition["crop_rule"]}; release zone {composition["release_zone"]}.',
        _assembly_instruction(subject, composition),
        f'Subject: {subject["origin_mode"]}, assembly {subject["assembly"]}, object family {subject["object_family_id"]}, treatment {subject["render_treatment"]}, scale {subject["scale_role"]}; function {subject["function"] or "not applicable"}; archive anchors {", ".join(subject["archive_identity_anchors"]) or "not applicable"}; intrinsic artifact text policy {subject["intrinsic_artifact_text_policy"]}; morphology {json.dumps(subject["morphology"], ensure_ascii=False)}.',
        f'Screen: {subject["screen_state"]}; {subject["screen_rendering_rule"] or subject["screen_text_rule"] or "no generated screen behavior"}',
        f'Palette: {palette["family"]} / {palette["color_complexity"]}; active hues {", ".join(palette["active_hues"]) or "locked manifest hues"}; area hierarchy {palette["area_hierarchy"]}; topology {palette["gradient_topology"]}; type mode {palette["type_mode"]}; focal mode {palette["focal_mode"]}; details {json.dumps(palette["detail_roles"], ensure_ascii=False)}.',
        brief["generation_call"]["reference_instruction"],
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
    assembly = manifest["subject_assembly"]
    plan = content.get("assembly_plan")
    if assembly == "SINGLE_OBJECT" and plan is not None:
        raise ValidationError("content.assembly_plan: must be omitted for SINGLE_OBJECT")
    if assembly != "SINGLE_OBJECT":
        if plan is None:
            raise ValidationError(f"content.assembly_plan: required for {assembly}")
        if plan["mode"] != assembly:
            raise ValidationError("content.assembly_plan.mode: must match manifest.subject_assembly")

    carrier = _carrier_contract(manifest)
    inventory = _text_inventory(content, manifest)
    subject = _subject(content, manifest)
    typography = _typography_contract(content, manifest)
    generation_call = _generation_call(content, manifest)
    concept = content["concept_contract"]
    brief: dict[str, Any] = {
        "brief_version": 1,
        "canvas": content["canvas"],
        "carrier_contract": carrier,
        "text_contract": content["text_contract"],
        "designed_text_inventory": inventory,
        "designed_text_count": len(inventory),
        "typography_contract": typography,
        "concept_contract": concept,
        "composition": _composition(manifest),
        "subject": subject,
        "palette": _palette(manifest),
        "background": {
            "id": "OPAQUE_BACKGROUND_BASE",
            "full_bleed_opaque": True,
            "requirement": BACKGROUND_REQUIREMENT,
            "coverage": "100% of the canvas behind every element and every cropped edge",
        },
        "generation_call": generation_call,
        "negative_constraints": [],
        "opaque_full_bleed_background_requirement": BACKGROUND_REQUIREMENT,
    }
    brief["negative_constraints"] = _negative_constraints(manifest, subject, carrier, concept)
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
