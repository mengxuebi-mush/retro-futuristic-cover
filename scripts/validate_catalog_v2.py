#!/usr/bin/env python3
"""Validate the V3 visual grammar catalog references and basic invariants."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "design-system"


def load(name: str) -> dict:
    with (ROOT / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def ids(records: list[dict], key: str = "id") -> set[str]:
    values = {record[key] for record in records}
    assert len(values) == len(records), f"duplicate {key} values"
    return values


def main() -> int:
    carriers = load("carriers.json")
    layouts = load("layouts.json")
    grammar = load("composition-grammar.json")
    objects = load("objects.json")
    morphologies = load("speculative-morphologies.json")
    custom_morphology_schema = load("custom-morphology.schema.json")
    subjects = load("subject-modes.json")
    screen_states = load("screen-states.json")
    focal_events = load("focal-events.json")
    compatibility = load("compatibility.json")
    manifest_schema = load("manifest.schema.json")

    carrier_ids = ids(carriers["carriers"])
    layout_ids = ids(layouts["layouts"])
    object_ids = ids(objects["object_families"])
    morphology_ids = ids(morphologies["morphologies"])
    subject_ids = ids(subjects["subject_origin_modes"])
    treatment_ids = ids(subjects["render_treatments"])
    scale_role_ids = ids(subjects["scale_roles"])
    screen_state_ids = ids(screen_states["screen_states"])
    focal_ids = ids(focal_events["focal_events"])
    primitive_ids = ids(grammar["primitives"])
    assembly_ids = ids(grammar["subject_assemblies"])
    operator_ids = ids(grammar["operators"])

    assert carriers["default_carrier"] in carrier_ids
    assert carriers["text_policy"] == "CARRIER_SPECIFIC"
    assert subject_ids == {"ABSTRACT_FORM", "ARCHIVE_ARTIFACT", "SPECULATIVE_OBJECT"}
    assert treatment_ids == {"FAITHFUL_RETAINED", "ENVIRONMENT_GRADED", "PALETTE_ASSIMILATED"}
    assert scale_role_ids == {"FIELD_STRUCTURE", "MONUMENTAL_FRAGMENT", "INTEGRATED_HERO", "CENTERPIECE_ARTIFACT", "SPECIMEN_ANCHOR", "REPEATED_FIELD"}
    assert screen_state_ids == {"NOT_APPLICABLE", "DORMANT", "SIGNAL", "CARRIER"}
    assert primitive_ids == {"TITLE_MASS", "SUBJECT_MASS", "SUPPORT_SYSTEM", "RELEASE_ZONE"}
    assert assembly_ids == {"SINGLE_OBJECT", "COMPOUND_SET", "PRIMARY_SATELLITES", "REPEATED_FAMILY"}
    assert layout_ids == {
        "ASYMMETRIC_COUNTERWEIGHT",
        "CENTERED_ANCHOR",
        "FRAME_THRESHOLD",
        "PERSPECTIVE_VECTOR",
        "RHYTHMIC_FIELD",
        "TYPE_DOMINANT_FIELD",
        "IMAGE_MASK_FIELD",
        "INFORMATION_AXIS",
    }
    assert morphologies["system_mode"] == "OPEN_COMPOSABLE"
    assert morphologies["custom_contract"]["id"] == "CUSTOM_COMPOSED"
    required_custom_fields = set(morphologies["custom_contract"]["required_fields"])
    assert required_custom_fields == set(custom_morphology_schema["required"])
    assert required_custom_fields == {
        "name", "idea", "shape_ancestry", "silhouette", "exaggeration",
        "aperture_rule", "construction_cues", "material_direction",
    }
    for morphology in morphologies["morphologies"]:
        assert morphology["role"] == "OPTIONAL_ARCHETYPE", morphology["id"]
        assert set(morphology["compatible_object_families"]).issubset(object_ids), morphology["id"]
        for field in ("idea", "silhouette", "exaggeration", "aperture_rule", "material_direction"):
            assert morphology[field], (morphology["id"], field)
        assert 1 <= len(morphology["construction_cues"]) <= 4, morphology["id"]

    for carrier in carriers["carriers"]:
        assert carrier["text_contract"] in {"THREE_ELEMENT_COVER", "EDITORIAL_POSTER_5_TO_7"}, carrier["id"]

    for layout in layouts["layouts"]:
        assert set(layout["allowed_carriers"]).issubset(carrier_ids), layout["id"]
        assert set(layout["focal_events"]).issubset(focal_ids), layout["id"]
        assert layout["compatible_topologies"], layout["id"]
        assert layout["required_structure"] and layout["release_zone"], layout["id"]
        assert layout["select_when"] and layout["object_slot"] and layout["collision_rule"], layout["id"]
        assert layout["support_zones"] and layout["crop_rule"], layout["id"]
        assert layout["failure_signals"] and layout["thumbnail_test"], layout["id"]
        assert set(layout["allowed_subject_assemblies"]).issubset(assembly_ids), layout["id"]
        assert layout["default_subject_assembly"] in layout["allowed_subject_assemblies"], layout["id"]
        assert set(layout["allowed_scale_roles"]).issubset(scale_role_ids), layout["id"]
        assert set(layout["required_operators"]).issubset(operator_ids), layout["id"]
        assert set(layout["optional_operators"]).issubset(operator_ids), layout["id"]
        assert not set(layout["required_operators"]) & set(layout["optional_operators"]), layout["id"]
        assert layout["forbidden_relationships"], layout["id"]
        attention = layout["attention_contract"]
        for role in ("title_percent", "subject_percent", "support_percent"):
            low, high = attention[role]
            assert 0 <= low <= high <= 100, (layout["id"], role)
        assert attention["title_percent"][0] > attention["subject_percent"][1], layout["id"]
        for field in ("subject_area_percent", "release_area_percent"):
            low, high = layout[field]
            assert 0 <= low <= high <= 100, (layout["id"], field)

    assert next(item for item in layouts["layouts"] if item["id"] == "RHYTHMIC_FIELD")["allowed_subject_assemblies"] == ["REPEATED_FAMILY"]
    assert next(item for item in layouts["layouts"] if item["id"] == "TYPE_DOMINANT_FIELD")["allowed_subject_assemblies"] == ["SINGLE_OBJECT"]
    assert "MONUMENTAL_FRAGMENT" in next(item for item in layouts["layouts"] if item["id"] == "CENTERED_ANCHOR")["allowed_scale_roles"]

    operator_category_by_id = {operator["id"]: operator["category"] for operator in grammar["operators"]}
    assert {operator["category"] for operator in grammar["operators"]} == {"PRIMARY_RELATION", "FOCAL_OPERATION", "SUPPORT_ALIGNMENT"}
    event_operator_map = grammar["focal_event_operator_map"]
    assert set(event_operator_map) == focal_ids
    assert set(event_operator_map.values()).issubset(operator_ids)
    for event_id, operator_id in event_operator_map.items():
        assert operator_category_by_id[operator_id] == "FOCAL_OPERATION", (event_id, operator_id)
    for layout in layouts["layouts"]:
        supported_operators = set(layout["required_operators"]) | set(layout["optional_operators"])
        assert any(operator_category_by_id[item] == "PRIMARY_RELATION" for item in layout["required_operators"]), layout["id"]
        assert any(operator_category_by_id[item] == "SUPPORT_ALIGNMENT" for item in layout["required_operators"]), layout["id"]
        for event_id in layout["focal_events"]:
            assert event_operator_map[event_id] in supported_operators, (layout["id"], event_id)

    for assembly in grammar["subject_assemblies"]:
        assert set(assembly["allowed_scale_roles"]).issubset(scale_role_ids), assembly["id"]
        assert assembly["mass_rule"] and assembly["selection_signal"], assembly["id"]

    assert {
        "subject_assembly", "composition_operators", "composition_sentence",
        "screen_state", "screen_content_role", "screen_content_source",
        "screen_display_language", "screen_copy_element", "screen_instance_rule",
    }.issubset(set(manifest_schema["required"]))

    for object_family in objects["object_families"]:
        assert object_family["subject_origin_mode"] in {"ARCHIVE_ARTIFACT", "SPECULATIVE_OBJECT"}, object_family["id"]
        assert set(object_family["compatible_layouts"]) == layout_ids, object_family["id"]
        assert set(object_family["compatible_carriers"]).issubset(carrier_ids), object_family["id"]
        assert object_family["topologies"] and object_family["placements"], object_family["id"]
        assert object_family["title_relationships"] and object_family["allowed_accents"], object_family["id"]
        assert 2 <= len(object_family["identity_anchors"]) <= 4, object_family["id"]
        if object_family["subject_origin_mode"] == "SPECULATIVE_OBJECT":
            assert object_family["function_requirement"], object_family["id"]
            assert set(object_family["compatible_morphologies"]).issubset(morphology_ids), object_family["id"]
        supported_screen_states = set(object_family.get("supported_screen_states", []))
        assert supported_screen_states.issubset(screen_state_ids - {"NOT_APPLICABLE"}), object_family["id"]
        if supported_screen_states:
            assert object_family["default_screen_state"] in supported_screen_states, object_family["id"]
            assert object_family["screen_instance_rule"], object_family["id"]

    archive_computer = next(item for item in objects["object_families"] if item["id"] == "ARCHIVE_COMPUTING_DEVICE")
    assert set(archive_computer["supported_screen_states"]) == {"DORMANT", "SIGNAL", "CARRIER"}
    assert archive_computer["default_screen_state"] == "SIGNAL"

    role_by_screen_state = {state["id"]: state["content_role"] for state in screen_states["screen_states"]}
    assert role_by_screen_state == {
        "NOT_APPLICABLE": "NONE",
        "DORMANT": "NONE",
        "SIGNAL": "NONVERBAL_SIGNAL",
        "CARRIER": "SUPPORT_ELEMENT",
    }
    for state in screen_states["screen_states"]:
        assert state["rendering_rule"] and state["text_rule"] and state["attention_rule"], state["id"]

    for mode in subjects["subject_origin_modes"]:
        assert set(mode["allowed_render_treatments"]).issubset(treatment_ids), mode["id"]
        assert set(mode["allowed_scale_roles"]).issubset(scale_role_ids), mode["id"]
        assert mode["identity_contract"] and mode["recognition_test"], mode["id"]

    compatibility_treatments = compatibility["allowed_render_treatments"]
    compatibility_scales = compatibility["allowed_scale_roles"]
    for mode in subjects["subject_origin_modes"]:
        assert set(compatibility_treatments[mode["id"]]) == set(mode["allowed_render_treatments"]), mode["id"]
        assert set(compatibility_scales[mode["id"]]) == set(mode["allowed_scale_roles"]), mode["id"]

    for event in focal_events["focal_events"]:
        assert event["release_zone"], event["id"]
        assert event["thumbnail_test"], event["id"]

    for carrier, requirements in compatibility["carrier_requirements"].items():
        assert carrier in carrier_ids, carrier
        assert requirements, carrier

    for pair in compatibility["forbidden_pairs"]:
        assert pair["left"] and pair["right"] and pair["reason"]
    assert set(compatibility["screen_state_requirements"]) == screen_state_ids

    print(
        f"PASS: {len(carrier_ids)} carriers, {len(layout_ids)} layouts, "
        f"{len(assembly_ids)} subject assemblies, {len(operator_ids)} composition operators, "
        f"{len(subject_ids)} subject modes, {len(object_ids)} object families, "
        f"{len(morphology_ids)} optional morphology archetypes + CUSTOM_COMPOSED, "
        f"{len(screen_state_ids)} screen states, {len(focal_ids)} focal events"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
