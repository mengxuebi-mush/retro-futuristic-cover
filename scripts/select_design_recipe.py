#!/usr/bin/env python3
"""Select a coordinated, variable-complexity retro-futuristic-cover design recipe."""

from __future__ import annotations

import argparse
import json
import os
import random
import secrets
import sys
import tempfile
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
DESIGN_SYSTEM_ROOT = SKILL_ROOT / "design-system"


def load_catalog(filename: str) -> dict[str, Any]:
    with (DESIGN_SYSTEM_ROOT / filename).open(encoding="utf-8") as handle:
        return json.load(handle)


try:
    CARRIER_CATALOG = load_catalog("carriers.json")
    LAYOUT_CATALOG = load_catalog("layouts.json")
    COMPOSITION_GRAMMAR_CATALOG = load_catalog("composition-grammar.json")
    OBJECT_CATALOG = load_catalog("objects.json")
    SPECULATIVE_MORPHOLOGY_CATALOG = load_catalog("speculative-morphologies.json")
    SUBJECT_CATALOG = load_catalog("subject-modes.json")
    SCREEN_STATE_CATALOG = load_catalog("screen-states.json")
    FOCAL_EVENT_CATALOG = load_catalog("focal-events.json")
except (FileNotFoundError, json.JSONDecodeError, OSError) as error:
    raise RuntimeError(f"V3 visual grammar catalogs are unavailable: {error}") from error


COMPLEXITY_WEIGHTS = {
    "SINGLE_FAMILY": 25,
    "DUAL_FIELD": 40,
    "SOFT_TRIAD": 25,
    "SPECTRAL_BLEND": 10,
}

FOCAL_MODE_WEIGHTS = {
    "HERO_OBJECT": 55,
    "ATMOSPHERIC_STRUCTURE": 45,
}

SUBJECT_ORIGIN_WEIGHTS = {
    "ABSTRACT_FORM": 34,
    "ARCHIVE_ARTIFACT": 33,
    "SPECULATIVE_OBJECT": 33,
}

SCALE_ROLE_BY_LAYOUT = {
    layout["id"]: layout["allowed_scale_roles"]
    for layout in LAYOUT_CATALOG["layouts"]
}
SUBJECT_ASSEMBLY_BY_ID = {
    assembly["id"]: assembly
    for assembly in COMPOSITION_GRAMMAR_CATALOG["subject_assemblies"]
}
OPERATOR_BY_ID = {
    operator["id"]: operator
    for operator in COMPOSITION_GRAMMAR_CATALOG["operators"]
}
SCREEN_STATE_BY_ID = {
    state["id"]: state
    for state in SCREEN_STATE_CATALOG["screen_states"]
}
SPECULATIVE_MORPHOLOGY_BY_ID = {
    morphology["id"]: morphology
    for morphology in SPECULATIVE_MORPHOLOGY_CATALOG["morphologies"]
}


PALETTES: list[dict[str, Any]] = [
    {
        "id": "P01_POWDER_SIGNAL",
        "name": "Powder Signal",
        "variants": {
            "SINGLE_FAMILY": [["powder sky"]],
            "DUAL_FIELD": [["powder sky", "coral"], ["powder sky", "warm ivory"]],
            "SOFT_TRIAD": [["powder sky", "warm ivory", "coral"]],
            "SPECTRAL_BLEND": [["powder sky", "warm ivory", "coral"]],
        },
    },
    {
        "id": "P02_INDIGO_INSIGHT",
        "name": "Indigo Insight",
        "variants": {
            "SINGLE_FAMILY": [["diffused indigo"]],
            "DUAL_FIELD": [["diffused indigo", "periwinkle"], ["diffused indigo", "apricot"]],
            "SOFT_TRIAD": [["diffused indigo", "periwinkle", "apricot"]],
            "SPECTRAL_BLEND": [["diffused indigo", "periwinkle", "apricot"]],
        },
    },
    {
        "id": "P03_PISTACHIO_FUTURE",
        "name": "Pistachio Future",
        "variants": {
            "SINGLE_FAMILY": [["pale pistachio"]],
            "DUAL_FIELD": [["pale pistachio", "apricot"], ["pale pistachio", "soft sage"]],
            "SOFT_TRIAD": [["warm ivory", "pale pistachio", "apricot"]],
            "SPECTRAL_BLEND": [["warm ivory", "pale pistachio", "soft sage", "apricot"]],
        },
    },
    {
        "id": "P04_LAVENDER_SYSTEM",
        "name": "Lavender System",
        "variants": {
            "SINGLE_FAMILY": [["soft lavender"]],
            "DUAL_FIELD": [["soft lavender", "mineral blue"], ["soft lavender", "blush"]],
            "SOFT_TRIAD": [["soft lavender", "mineral blue", "blush"]],
            "SPECTRAL_BLEND": [["mineral blue", "soft lavender", "blush"]],
        },
    },
    {
        "id": "P05_APRICOT_STRUCTURE",
        "name": "Apricot Structure",
        "variants": {
            "SINGLE_FAMILY": [["apricot"]],
            "DUAL_FIELD": [["warm ivory", "apricot"], ["apricot", "muted amber"]],
            "SOFT_TRIAD": [["warm ivory", "apricot", "muted amber"]],
            "SPECTRAL_BLEND": [["warm ivory", "apricot", "muted amber", "coral"]],
        },
    },
    {
        "id": "P06_BLUSH_FOCUS",
        "name": "Blush Focus",
        "variants": {
            "SINGLE_FAMILY": [["blush"]],
            "DUAL_FIELD": [["blush", "coral"], ["blush", "warm ivory"]],
            "SOFT_TRIAD": [["warm ivory", "blush", "coral"]],
            "SPECTRAL_BLEND": [["warm ivory", "blush", "coral"]],
        },
    },
    {
        "id": "P07_VELVET_ENERGY",
        "name": "Velvet Energy",
        "variants": {
            "SINGLE_FAMILY": [["soft violet"]],
            "DUAL_FIELD": [["diffused indigo", "soft violet"], ["diffused indigo", "coral"]],
            "SOFT_TRIAD": [["diffused indigo", "soft violet", "coral"]],
            "SPECTRAL_BLEND": [["diffused indigo", "soft violet", "coral", "muted amber"]],
        },
    },
    {
        "id": "P08_QUIET_SPECTRUM",
        "name": "Quiet Spectrum",
        "variants": {
            "SINGLE_FAMILY": [["mineral blue"]],
            "DUAL_FIELD": [["powder sky", "blush"], ["warm ivory", "soft sage"]],
            "SOFT_TRIAD": [["warm ivory", "powder sky", "blush"]],
            "SPECTRAL_BLEND": [["warm ivory", "powder sky", "blush", "soft sage"]],
        },
    },
]


COMPOSITIONS = [
    {
        "id": "C01_EDGE_BLOOM",
        "gradient_topology": "EDGE_BLOOM",
        "gradient_direction": "one oversized color field blooms inward from an off-canvas edge",
        "primary_forms": ["misted arch", "edge-cropped curved translucent surface"],
        "title_zones": ["upper-left", "middle-left", "lower-left"],
        "bridges": ["one tangent curve", "one short aligned rule"],
    },
    {
        "id": "C02_DIAGONAL_DRIFT",
        "gradient_topology": "DIAGONAL_DRIFT",
        "gradient_direction": "two broad fields cross diagonally through a long intermediate blend",
        "primary_forms": ["flowing chromatic ribbon", "curved translucent membrane"],
        "title_zones": ["upper-left", "lower-left", "center-right"],
        "bridges": ["one long tangent curve", "one partial frame aligned to the diagonal"],
    },
    {
        "id": "C03_HORIZON_HAZE",
        "gradient_topology": "HORIZON_HAZE",
        "gradient_direction": "diffuse light spreads along an asymmetric soft horizon",
        "primary_forms": ["faint perspective plane", "soft portal fragment"],
        "title_zones": ["upper-left", "lower-left", "upper-right"],
        "bridges": ["one faint perspective grid", "one horizon rule"],
    },
    {
        "id": "C04_CHROMATIC_CURTAIN",
        "gradient_topology": "CHROMATIC_CURTAIN",
        "gradient_direction": "a broad vertical or arcing translucent color curtain crosses an edge",
        "primary_forms": ["flowing chromatic shape", "curved translucent surface"],
        "title_zones": ["middle-left", "lower-left", "center-right"],
        "bridges": ["one contour line", "one narrow partial frame"],
    },
    {
        "id": "C05_CENTER_OF_GRAVITY",
        "gradient_topology": "CENTER_OF_GRAVITY",
        "gradient_direction": "one offset chromatic mass dissolves outward without a visible circular boundary",
        "primary_forms": ["flattened edge-cropped orb"],
        "title_zones": ["upper-left", "lower-left"],
        "bridges": ["one short aligned rule", "one minimal corner bracket"],
    },
    {
        "id": "C06_SPLIT_ATMOSPHERE",
        "gradient_topology": "SPLIT_ATMOSPHERE",
        "gradient_direction": "warm and cool atmospheric fields meet through a broad mixed transition",
        "primary_forms": ["offset soft portal", "faint folded plane"],
        "title_zones": ["middle-left", "upper-right", "lower-right"],
        "bridges": ["one shared-axis portal outline", "one faint folded-grid structure"],
    },
]


PALE_DEVICES = [
    "pale edge-cropped rectangle",
    "pale arched inset",
    "pale curved cutout",
    "pale translucent side plane",
]

ACCENTS = ["four-point stars", "triangles", "diamonds", "tiny dots", "thin rings", "corner brackets"]
HERO_OBJECTS: list[dict[str, Any]] = [
    {
        "id": "H01_SCULPTURAL_ORB",
        "family": "SCULPTURAL_VOLUME",
        "weight": 20,
        "geometry": "one complete or decisively edge-cropped atmospheric orb",
        "material": "matte frosted volume integrated into the active gradient hues",
        "lighting": "soft directional shading with broad tonal rolloff; no hard rim, specular planet highlight, or black space",
        "scale": "25–40% of the short edge",
        "placements": ["offset-center", "centered behind or beside the title", "edge-cropped along the title axis"],
        "title_relationships": ["shared tangent", "partial overlap", "counter-shape", "shared vertical axis"],
        "topologies": ["EDGE_BLOOM", "HORIZON_HAZE", "CENTER_OF_GRAVITY", "SPLIT_ATMOSPHERE"],
        "allowed_accents": ["triangles", "diamonds", "tiny dots", "corner brackets"],
        "forbidden_bridge_tokens": ["portal"],
    },
    {
        "id": "H02_TRANSLUCENT_POD",
        "family": "SCULPTURAL_VOLUME",
        "weight": 10,
        "geometry": "one rounded bubble, egg, or capsule-like pod",
        "material": "translucent acrylic-like shell with a pale internal color layer",
        "lighting": "diffuse interior light without glassmorphism, chrome, or product-render gloss",
        "scale": "24–38% of the short edge",
        "placements": ["offset-center", "edge-cropped", "floating on the title baseline"],
        "title_relationships": ["shared baseline", "partial overlap", "nested negative space"],
        "topologies": ["EDGE_BLOOM", "DIAGONAL_DRIFT", "CHROMATIC_CURTAIN", "SPLIT_ATMOSPHERE"],
        "allowed_accents": ["four-point stars", "triangles", "tiny dots", "corner brackets"],
        "forbidden_bridge_tokens": [],
    },
    {
        "id": "H03_TORUS_PORTAL",
        "family": "SCULPTURAL_VOLUME",
        "weight": 8,
        "geometry": "one soft torus or thick hollow ring functioning as a portal",
        "material": "powdery translucent volume with restrained depth",
        "lighting": "soft inner-to-outer tonal transition; no metallic donut or neon rim",
        "scale": "26–42% of the short edge",
        "placements": ["offset-center", "edge-cropped", "partly behind the title"],
        "title_relationships": ["title enters the opening", "shared tangent", "counter-shape"],
        "topologies": ["EDGE_BLOOM", "DIAGONAL_DRIFT", "CHROMATIC_CURTAIN", "SPLIT_ATMOSPHERE"],
        "allowed_accents": ["triangles", "diamonds", "tiny dots", "corner brackets"],
        "forbidden_bridge_tokens": ["portal"],
    },
    {
        "id": "H04_GEODESIC_GLOBE",
        "family": "EARLY_CG_GEOMETRY",
        "weight": 7,
        "geometry": "one translucent geodesic globe built from a restrained triangular mesh",
        "material": "hairline wireframe with a faint tinted atmospheric skin",
        "lighting": "subtle depth through line density and one soft shaded side; no chrome or literal Earth texture",
        "scale": "24–38% of the short edge",
        "placements": ["offset-center", "edge-cropped", "centered in a quiet field"],
        "title_relationships": ["shared axis", "title overlaps the outer mesh edge", "aligned tangent"],
        "topologies": ["HORIZON_HAZE", "CENTER_OF_GRAVITY", "SPLIT_ATMOSPHERE"],
        "allowed_accents": ["triangles", "diamonds", "tiny dots", "corner brackets"],
        "forbidden_bridge_tokens": ["grid", "folded"],
    },
    {
        "id": "H05_TRANSLUCENT_PRISM",
        "family": "EARLY_CG_GEOMETRY",
        "weight": 7,
        "geometry": "one transparent prism, cube, or quiet monolith",
        "material": "pale translucent planes derived only from active hues",
        "lighting": "soft refraction and overlapping planes without glossy product-render reflections",
        "scale": "22–36% of the short edge",
        "placements": ["offset-center", "edge-cropped", "anchored to a title corner"],
        "title_relationships": ["shared edge", "partial overlap", "aligned perspective axis"],
        "topologies": ["DIAGONAL_DRIFT", "CHROMATIC_CURTAIN", "SPLIT_ATMOSPHERE"],
        "allowed_accents": ["four-point stars", "diamonds", "tiny dots", "corner brackets"],
        "forbidden_bridge_tokens": ["frame"],
    },
    {
        "id": "H06_WIREFRAME_POLYHEDRON",
        "family": "EARLY_CG_GEOMETRY",
        "weight": 6,
        "geometry": "one early-computer-graphics wireframe polyhedron",
        "material": "thin low-contrast lines with a barely visible translucent surface skin",
        "lighting": "depth from perspective and restrained line overlap, not glow",
        "scale": "24–38% of the short edge",
        "placements": ["offset-center", "edge-cropped", "floating beside the title"],
        "title_relationships": ["shared perspective axis", "overlap", "aligned corner"],
        "topologies": ["HORIZON_HAZE", "CENTER_OF_GRAVITY", "SPLIT_ATMOSPHERE"],
        "allowed_accents": ["triangles", "diamonds", "tiny dots", "corner brackets"],
        "forbidden_bridge_tokens": ["grid", "folded"],
    },
    {
        "id": "H07_FOLDED_GRID_WELL",
        "family": "SPATIAL_STRUCTURE",
        "weight": 7,
        "geometry": "one folded perspective grid, curved grid well, or receding spatial plane",
        "material": "fine low-opacity hairlines emerging from the atmospheric field",
        "lighting": "depth from convergence and fading line density; no second complex line system",
        "scale": "30–55% of the short edge",
        "placements": ["lower-center", "edge-cropped", "receding behind the title"],
        "title_relationships": ["shared vanishing axis", "title sits on the fold", "grid emerges from a title-aligned anchor"],
        "topologies": ["DIAGONAL_DRIFT", "HORIZON_HAZE", "SPLIT_ATMOSPHERE"],
        "allowed_accents": ["four-point stars", "diamonds", "tiny dots", "corner brackets"],
        "forbidden_bridge_tokens": ["grid", "folded", "frame"],
    },
    {
        "id": "H08_NESTED_PORTAL",
        "family": "SPATIAL_STRUCTURE",
        "weight": 6,
        "geometry": "one nested arch, ellipse, or rectangular portal tunnel",
        "material": "thin translucent layers receding through active-hue tints",
        "lighting": "soft depth through overlap and atmospheric fading; no neon tunnel",
        "scale": "28–48% of the short edge",
        "placements": ["offset-center", "edge-cropped", "behind the title"],
        "title_relationships": ["title enters the portal opening", "shared centerline", "aligned edge"],
        "topologies": ["EDGE_BLOOM", "CHROMATIC_CURTAIN", "SPLIT_ATMOSPHERE"],
        "allowed_accents": ["four-point stars", "triangles", "tiny dots", "corner brackets"],
        "forbidden_bridge_tokens": ["portal", "frame"],
    },
    {
        "id": "H09_RADIANT_FOUR_POINT_STAR",
        "family": "RADIANT_SYMBOL",
        "weight": 15,
        "geometry": "one large four-point star used as the principal focal object",
        "material": "warm-white or active-hue-derived luminous core with clean tapered points",
        "lighting": "one broad feathered active-hue haze around the warm-white or active-hue-derived core; dissolve it seamlessly into the cross-canvas gradient with no circular boundary, ring, donut, isolated blob, lens-flare streak, or repeated sparkle field",
        "scale": "32–46% of the short edge; normally near 40%",
        "placements": ["centered in a quiet field", "offset-center", "aligned between title and spatial structure"],
        "title_relationships": [
            "shared axis with a clear gap from every title glyph",
            "star occupies reserved counter-space beside or below the title lines without crossing glyphs",
            "aligned tangent outside the glyph-based title clear zone",
        ],
        "topologies": ["EDGE_BLOOM", "HORIZON_HAZE", "CENTER_OF_GRAVITY", "SPLIT_ATMOSPHERE"],
        "allowed_accents": ["four-point stars", "triangles", "diamonds", "tiny dots", "corner brackets"],
        "forbidden_bridge_tokens": [],
    },
    {
        "id": "H10_ATOMIC_STARBURST",
        "family": "RADIANT_SYMBOL",
        "weight": 4,
        "geometry": "one restrained atomic starburst with a single center and sparse tapered rays or nodes",
        "material": "flat warm-white or near-black lines according to field contrast",
        "lighting": "a faint center bloom only; no firework, sunburst wallpaper, or repeated bursts",
        "scale": "14–24% of the short edge",
        "placements": ["offset-center", "edge-cropped", "aligned to the title baseline"],
        "title_relationships": ["shared centerline", "rays bridge toward the title", "baseline alignment"],
        "topologies": ["EDGE_BLOOM", "HORIZON_HAZE", "SPLIT_ATMOSPHERE"],
        "allowed_accents": ["diamonds", "tiny dots", "corner brackets"],
        "forbidden_bridge_tokens": [],
    },
    {
        "id": "H11_STREAMLINED_CAPSULE",
        "family": "STREAMLINE_BIOMORPHIC",
        "weight": 5,
        "geometry": "one tapered capsule, teardrop, or aerodynamic lozenge",
        "material": "soft opaque-to-translucent surface derived from active hues",
        "lighting": "broad directional shading that emphasizes motion without chrome",
        "scale": "24–40% of the short edge",
        "placements": ["diagonal center", "edge-cropped", "floating on a long title axis"],
        "title_relationships": ["shared motion axis", "partial overlap", "point directs attention to title"],
        "topologies": ["DIAGONAL_DRIFT", "CHROMATIC_CURTAIN", "SPLIT_ATMOSPHERE"],
        "allowed_accents": ["four-point stars", "triangles", "tiny dots", "corner brackets"],
        "forbidden_bridge_tokens": [],
    },
    {
        "id": "H12_BIOMORPHIC_CELL",
        "family": "STREAMLINE_BIOMORPHIC",
        "weight": 5,
        "geometry": "one abstract amoeba, cellular membrane, or vital organic form",
        "material": "powdery translucent membrane with one thicker chromatic edge",
        "lighting": "soft interior diffusion without cartoon outlines or liquid-metal gloss",
        "scale": "26–44% of the short edge",
        "placements": ["offset-center", "edge-cropped", "wrapped around the title zone"],
        "title_relationships": ["counter-shape", "partial overlap", "shared curvature"],
        "topologies": ["EDGE_BLOOM", "CHROMATIC_CURTAIN", "CENTER_OF_GRAVITY"],
        "allowed_accents": ["four-point stars", "diamonds", "tiny dots", "thin rings"],
        "forbidden_bridge_tokens": ["portal"],
    },
]
FONT_MODE_BASE_WEIGHTS = {
    "CJK_NEO_GROTESK": 60,
    "CJK_SOFT_HUMANIST": 25,
    "CJK_STRUCTURAL_SANS": 15,
}
LABEL_TREATMENTS = ["plain label with short rule", "thin outlined pill", "minimal corner alignment"]


def default_state_file() -> Path:
    override = os.environ.get("RETRO_COVER_STATE_FILE")
    if override:
        return Path(override).expanduser()
    return Path(tempfile.gettempdir()) / "retro-futuristic-cover-design-history.json"


def load_history(path: Path) -> list[dict[str, str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        records = data.get("recent_designs", [])
        return [record for record in records if isinstance(record, dict)]
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def save_history(path: Path, records: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"recent_designs": records[-3:]}
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary_path = Path(handle.name)
    os.replace(temporary_path, path)


def weighted_choice(rng: random.Random, values: dict[str, int]) -> str:
    return rng.choices(list(values), weights=list(values.values()), k=1)[0]


def choose_different(rng: random.Random, values: list[str], recent: set[str]) -> str:
    candidates = [value for value in values if value not in recent] or values
    return rng.choice(candidates)


def choose_carrier(
    rng: random.Random,
    history: list[dict[str, str]],
    excluded: set[str],
    requested: str,
) -> dict[str, Any]:
    carriers = CARRIER_CATALOG["carriers"]
    if requested != "AUTO":
        matches = [carrier for carrier in carriers if carrier["id"] == requested]
        if not matches:
            raise ValueError(f"Unknown carrier: {requested}")
        if requested in excluded:
            raise ValueError(f"Carrier excluded: {requested}")
        return matches[0]
    recent = {record.get("carrier_id", "") for record in history[-2:]}
    candidates = [carrier for carrier in carriers if carrier["id"] not in excluded and carrier["id"] not in recent]
    candidates = candidates or [carrier for carrier in carriers if carrier["id"] not in excluded]
    if not candidates:
        raise ValueError("No carriers remain after exclusions.")
    return rng.choice(candidates)


def choose_layout_family(
    rng: random.Random,
    carrier_id: str,
    history: list[dict[str, str]],
    excluded: set[str],
    requested: str,
    requested_subject_assembly: str,
) -> dict[str, Any]:
    layouts = [
        layout for layout in LAYOUT_CATALOG["layouts"]
        if carrier_id in layout["allowed_carriers"]
        and layout["id"] not in excluded
        and (
            requested_subject_assembly == "AUTO"
            or requested_subject_assembly in layout["allowed_subject_assemblies"]
        )
    ]
    if requested != "AUTO":
        matches = [layout for layout in layouts if layout["id"] == requested]
        if not matches:
            raise ValueError(f"Layout {requested} is not available for carrier {carrier_id} or was excluded.")
        return matches[0]
    recent = {record.get("layout_family", "") for record in history[-2:]}
    diverse = [layout for layout in layouts if layout["id"] not in recent]
    return rng.choice(diverse or layouts)


def choose_subject_assembly(
    layout: dict[str, Any],
    excluded: set[str],
    requested: str,
    requested_scale_role: str,
) -> dict[str, Any]:
    allowed_ids = [
        assembly_id for assembly_id in layout["allowed_subject_assemblies"]
        if assembly_id not in excluded
        and (
            requested_scale_role == "AUTO"
            or requested_scale_role in SUBJECT_ASSEMBLY_BY_ID[assembly_id]["allowed_scale_roles"]
        )
    ]
    if requested != "AUTO":
        if requested not in allowed_ids:
            raise ValueError(
                f"Subject assembly {requested} is incompatible with layout {layout['id']}, "
                f"scale role {requested_scale_role}, or was excluded."
            )
        return SUBJECT_ASSEMBLY_BY_ID[requested]
    default_id = layout["default_subject_assembly"]
    if default_id in allowed_ids:
        return SUBJECT_ASSEMBLY_BY_ID[default_id]
    if not allowed_ids:
        raise ValueError(f"No subject assemblies remain for layout {layout['id']} and scale role {requested_scale_role}.")
    return SUBJECT_ASSEMBLY_BY_ID[allowed_ids[0]]


def choose_focal_event(
    rng: random.Random,
    layout: dict[str, Any],
    history: list[dict[str, str]],
    excluded: set[str],
    requested: str,
) -> dict[str, Any]:
    event_by_id = {event["id"]: event for event in FOCAL_EVENT_CATALOG["focal_events"]}
    allowed_ids = [event_id for event_id in layout["focal_events"] if event_id not in excluded]
    if requested != "AUTO":
        if requested not in allowed_ids:
            raise ValueError(f"Focal event {requested} is not supported by layout {layout['id']} or was excluded.")
        return event_by_id[requested]
    recent = {record.get("focal_event", "") for record in history[-2:]}
    candidates = [event_by_id[event_id] for event_id in allowed_ids if event_id not in recent]
    candidates = candidates or [event_by_id[event_id] for event_id in allowed_ids]
    if not candidates:
        raise ValueError(f"No focal events remain for layout {layout['id']}.")
    return rng.choice(candidates)


def choose_object_family(
    rng: random.Random,
    carrier_id: str,
    layout: dict[str, Any],
    subject_origin_mode: str,
    history: list[dict[str, str]],
    excluded: set[str],
    requested: str,
) -> dict[str, Any] | None:
    objects = [
        item for item in OBJECT_CATALOG["object_families"]
        if carrier_id in item["compatible_carriers"]
        and layout["id"] in item["compatible_layouts"]
        and item["subject_origin_mode"] == subject_origin_mode
        and item["id"] not in excluded
    ]
    if requested == "NONE":
        return None
    if requested != "AUTO":
        matches = [item for item in objects if item["id"] == requested]
        if not matches:
            raise ValueError(f"Object family {requested} is not compatible with carrier {carrier_id} and layout {layout['id']}.")
        return matches[0]
    recent = {record.get("object_family", "") for record in history[-3:]}
    diverse = [item for item in objects if item["id"] not in recent]
    if not diverse and objects:
        diverse = objects
    return rng.choice(diverse) if diverse else None


def choose_speculative_morphology(
    rng: random.Random,
    subject_origin_mode: str,
    object_family: dict[str, Any] | None,
    history: list[dict[str, str]],
    excluded: set[str],
    requested: str,
) -> dict[str, Any] | None:
    if subject_origin_mode != "SPECULATIVE_OBJECT":
        if requested != "AUTO":
            raise ValueError("--speculative-morphology applies only to SPECULATIVE_OBJECT.")
        return None
    if object_family is None:
        raise ValueError("SPECULATIVE_OBJECT requires an object family before morphology can resolve.")
    allowed_ids = [
        morphology_id for morphology_id in object_family.get("compatible_morphologies", [])
        if morphology_id not in excluded
    ]
    if requested != "AUTO":
        if requested not in allowed_ids:
            raise ValueError(
                f"Speculative morphology {requested} is incompatible with object family {object_family['id']} or was excluded."
            )
        return SPECULATIVE_MORPHOLOGY_BY_ID[requested]
    recent = {record.get("speculative_morphology", "") for record in history[-2:]}
    candidates = [
        SPECULATIVE_MORPHOLOGY_BY_ID[morphology_id]
        for morphology_id in allowed_ids
        if morphology_id not in recent
    ]
    candidates = candidates or [
        SPECULATIVE_MORPHOLOGY_BY_ID[morphology_id]
        for morphology_id in allowed_ids
    ]
    if not candidates:
        raise ValueError(f"No speculative morphologies remain for object family {object_family['id']}.")
    return rng.choice(candidates)


def choose_screen_state(
    carrier_id: str,
    object_family: dict[str, Any] | None,
    subject_assembly_id: str,
    requested: str,
    screen_copy_element: str,
) -> tuple[dict[str, Any], str, str]:
    copy_element = screen_copy_element.strip()
    allowed_ids = (
        object_family.get("supported_screen_states", ["NOT_APPLICABLE"])
        if object_family else
        ["NOT_APPLICABLE"]
    )
    if requested == "AUTO":
        selected_id = (
            "CARRIER" if copy_element and "CARRIER" in allowed_ids else
            object_family.get("default_screen_state", "NOT_APPLICABLE") if object_family else
            "NOT_APPLICABLE"
        )
    else:
        selected_id = requested
    if selected_id not in allowed_ids:
        family_id = object_family["id"] if object_family else "NONE"
        raise ValueError(f"Screen state {selected_id} is not supported by object family {family_id}.")
    if selected_id == "CARRIER":
        if carrier_id != "EDITORIAL_POSTER":
            raise ValueError("SCREEN_CARRIER is supported only for EDITORIAL_POSTER.")
        if not copy_element:
            raise ValueError("SCREEN_CARRIER requires --screen-copy-element with one exact locked support string.")
        if len(copy_element) > 80:
            raise ValueError("SCREEN_CARRIER copy must remain one concise support element of 80 characters or fewer.")
    elif copy_element:
        raise ValueError("--screen-copy-element requires --screen-state CARRIER or AUTO on a carrier-capable screen object.")
    state = SCREEN_STATE_BY_ID[selected_id]
    instance_rule = (
        object_family.get("screen_instance_rule", "activate only the compositionally primary screen")
        if selected_id not in {"NOT_APPLICABLE", "DORMANT"} and object_family else
        "all visible screens remain dormant" if selected_id == "DORMANT" else
        "no generated screen behavior"
    )
    if subject_assembly_id == "REPEATED_FAMILY" and selected_id in {"SIGNAL", "CARRIER"}:
        instance_rule = "only the largest or compositionally primary instance is active; every subordinate screen remains DORMANT"
    return state, copy_element or "NONE", instance_rule


def choose_composition(
    rng: random.Random,
    layout: dict[str, Any],
    object_family: dict[str, Any] | None,
    history: list[dict[str, str]],
    excluded: set[str],
) -> dict[str, Any]:
    compatible_topologies = set(layout["compatible_topologies"])
    if object_family:
        compatible_topologies &= set(object_family["topologies"])
    candidates = [
        composition for composition in COMPOSITIONS
        if composition["id"] not in excluded
        and composition["gradient_topology"] not in excluded
        and composition["gradient_topology"] in compatible_topologies
    ]
    recent_topologies = {record.get("gradient_topology", "") for record in history[-2:]}
    diverse = [composition for composition in candidates if composition["gradient_topology"] not in recent_topologies]
    if diverse:
        candidates = diverse
    if not candidates:
        raise ValueError(f"No compositions remain for layout {layout['id']} and object family {object_family and object_family['id']}.")
    return rng.choice(candidates)


def complementary_side(title_zone: str) -> str:
    """Assign an atmospheric form to the side opposite the locked title zone."""
    return "right" if "left" in title_zone else "left"


def choose_focal_mode(rng: random.Random, history: list[dict[str, str]]) -> str:
    recent_modes = [record.get("focal_mode", "") for record in history[-2:]]
    if len(recent_modes) == 2 and all(mode == "HERO_OBJECT" for mode in recent_modes):
        return "ATMOSPHERIC_STRUCTURE"
    if len(recent_modes) == 2 and all(mode == "ATMOSPHERIC_STRUCTURE" for mode in recent_modes):
        return "HERO_OBJECT"
    return weighted_choice(rng, FOCAL_MODE_WEIGHTS)


def choose_subject_origin_mode(
    rng: random.Random,
    history: list[dict[str, str]],
    requested: str,
) -> str:
    if requested != "AUTO":
        return requested
    recent_modes = [record.get("subject_origin_mode", "") for record in history[-2:]]
    weights = SUBJECT_ORIGIN_WEIGHTS.copy()
    if len(recent_modes) == 2 and recent_modes[0] == recent_modes[1]:
        weights.pop(recent_modes[0], None)
    return weighted_choice(rng, weights)


def subject_mode_record(subject_origin_mode: str) -> dict[str, Any]:
    return next(mode for mode in SUBJECT_CATALOG["subject_origin_modes"] if mode["id"] == subject_origin_mode)


def choose_render_treatment(
    rng: random.Random,
    subject_origin_mode: str,
    history: list[dict[str, str]],
    requested: str,
) -> dict[str, Any]:
    mode = subject_mode_record(subject_origin_mode)
    allowed = mode["allowed_render_treatments"]
    if requested != "AUTO":
        if requested not in allowed:
            raise ValueError(f"Render treatment {requested} is incompatible with {subject_origin_mode}.")
        selected = requested
    else:
        recent = {record.get("render_treatment", "") for record in history[-2:]}
        selected = choose_different(rng, allowed, recent)
    return next(item for item in SUBJECT_CATALOG["render_treatments"] if item["id"] == selected)


def choose_scale_role(
    rng: random.Random,
    subject_origin_mode: str,
    layout_id: str,
    subject_assembly: dict[str, Any],
    history: list[dict[str, str]],
    requested: str,
) -> dict[str, Any]:
    mode = subject_mode_record(subject_origin_mode)
    candidates = [
        role for role in SCALE_ROLE_BY_LAYOUT[layout_id]
        if role in mode["allowed_scale_roles"]
        and role in subject_assembly["allowed_scale_roles"]
    ]
    if requested != "AUTO":
        if requested not in candidates:
            raise ValueError(f"Scale role {requested} is incompatible with {subject_origin_mode} and {layout_id}.")
        selected = requested
    else:
        recent = {record.get("scale_role", "") for record in history[-2:]}
        selected = choose_different(rng, candidates, recent)
    return next(item for item in SUBJECT_CATALOG["scale_roles"] if item["id"] == selected)


def choose_hero_object(
    rng: random.Random,
    topology: str,
    history: list[dict[str, str]],
    excluded: set[str],
) -> dict[str, Any]:
    compatible = [
        hero for hero in HERO_OBJECTS
        if topology in hero["topologies"]
        and hero["id"] not in excluded
        and hero["family"] not in excluded
        and hero["geometry"] not in excluded
    ]
    if not compatible:
        compatible = [hero for hero in HERO_OBJECTS if hero["id"] not in excluded and hero["family"] not in excluded]
    if not compatible:
        raise ValueError("No hero objects remain after exclusions.")

    recent_families = {record.get("hero_family", "") for record in history[-3:]}
    recent_ids = {record.get("hero_id", "") for record in history[-3:]}
    diverse = [hero for hero in compatible if hero["family"] not in recent_families and hero["id"] not in recent_ids]
    diverse = diverse or [hero for hero in compatible if hero["id"] not in recent_ids]
    diverse = diverse or compatible
    return rng.choices(diverse, weights=[hero["weight"] for hero in diverse], k=1)[0]


def choose_font_mode(
    rng: random.Random,
    recent: set[str],
    regime: str,
    primary_form: str,
    use_pale_panel: bool,
) -> str:
    weights = FONT_MODE_BASE_WEIGHTS.copy()
    if regime == "HIGH_KEY_AIRY" or use_pale_panel:
        weights["CJK_SOFT_HUMANIST"] += 15
    else:
        weights["CJK_SOFT_HUMANIST"] = 10
    if regime == "DEEP_VELVET" or any(token in primary_form for token in ["perspective", "folded", "portal"]):
        weights["CJK_STRUCTURAL_SANS"] += 20
    else:
        weights["CJK_STRUCTURAL_SANS"] = 10
    candidates = {mode: weight for mode, weight in weights.items() if mode not in recent} or weights
    return weighted_choice(rng, candidates)


def tonal_regime(palette_id: str, complexity: str, rng: random.Random) -> str:
    if palette_id in {"P02_INDIGO_INSIGHT", "P07_VELVET_ENERGY"}:
        return rng.choice(["MID_TONE_EDITORIAL", "DEEP_VELVET"])
    if complexity == "SPECTRAL_BLEND":
        return rng.choice(["HIGH_KEY_AIRY", "MID_TONE_EDITORIAL"])
    return rng.choices(["HIGH_KEY_AIRY", "MID_TONE_EDITORIAL"], weights=[70, 30], k=1)[0]


def harmony_mode(complexity: str, hues: list[str]) -> str:
    if complexity == "SINGLE_FAMILY":
        return "MONOCHROMATIC"
    if complexity == "DUAL_FIELD":
        return "WARM_COOL_DUOTONE" if any(h in hues for h in ["coral", "apricot", "pale apricot", "blush"]) else "ANALOGOUS"
    return "EDITORIAL_TRIAD"


def area_hierarchy(complexity: str) -> str:
    return {
        "SINGLE_FAMILY": "one hue family expressed as pale tint / mid tone / soft deep tone; no independent accent hue",
        "DUAL_FIELD": "dominant hue 70–80%; companion hue 20–30%; never 50/50",
        "SOFT_TRIAD": "dominant hue 50–60%; secondary 25–35%; accent 10–15%",
        "SPECTRAL_BLEND": "dominant hue 45–55%; secondary 20–30%; remaining anchors and derived transition 15–25% combined",
    }[complexity]


def coral_role(hues: list[str]) -> str:
    if "coral" not in hues:
        return "ABSENT"
    return "PRIMARY" if hues[0] == "coral" else "ACCENT"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-file", type=Path, default=default_state_file())
    parser.add_argument("--no-state", action="store_true", help="Do not read or update history")
    parser.add_argument("--exclude", action="append", default=[], help="Exclude a palette, carrier, layout, topology, object, speculative morphology, focal event, form, or signature ID")
    parser.add_argument("--carrier", default="SOCIAL_COVER", help="Carrier ID, or AUTO")
    parser.add_argument("--layout-family", default="AUTO", help="Layout family ID, or AUTO")
    parser.add_argument(
        "--subject-origin-mode",
        default="AUTO",
        choices=["AUTO", "ABSTRACT_FORM", "ARCHIVE_ARTIFACT", "SPECULATIVE_OBJECT"],
        help="Visual subject provenance; choose this before rendering treatment or scale role",
    )
    parser.add_argument(
        "--render-treatment",
        default="AUTO",
        choices=["AUTO", "FAITHFUL_RETAINED", "ENVIRONMENT_GRADED", "PALETTE_ASSIMILATED"],
        help="How strongly the selected subject retains local color and material",
    )
    parser.add_argument(
        "--scale-role",
        default="AUTO",
        choices=["AUTO", "FIELD_STRUCTURE", "MONUMENTAL_FRAGMENT", "INTEGRATED_HERO", "CENTERPIECE_ARTIFACT", "SPECIMEN_ANCHOR", "REPEATED_FIELD"],
        help="The subject's independent compositional scale role",
    )
    parser.add_argument(
        "--subject-assembly",
        default="AUTO",
        choices=["AUTO", "SINGLE_OBJECT", "COMPOUND_SET", "PRIMARY_SATELLITES", "REPEATED_FAMILY"],
        help="How one or more visible objects resolve into one perceptually unified subject mass",
    )
    parser.add_argument(
        "--source-asset-mode",
        default="NONE",
        choices=["NONE", "FAITHFUL_IMAGE", "ABSTRACT_SYMBOL"],
        help="Optional supplied-image override; this is an input source, not a fourth visual style",
    )
    parser.add_argument(
        "--subject-mode",
        choices=["ATMOSPHERIC_STRUCTURE", "CONCRETE_OBJECT", "ABSTRACT_SYMBOL", "FAITHFUL_IMAGE", "REPEATED_OBJECT"],
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--object-family", default="AUTO", help="Archive or speculative object family ID, NONE, or AUTO")
    parser.add_argument(
        "--speculative-morphology",
        default="AUTO",
        help="Retro-future morphology ID for SPECULATIVE_OBJECT, or AUTO",
    )
    parser.add_argument(
        "--screen-state",
        default="AUTO",
        choices=["AUTO", "NOT_APPLICABLE", "DORMANT", "SIGNAL", "CARRIER"],
        help="Generated screen behavior for a screen-capable object family",
    )
    parser.add_argument(
        "--screen-copy-element",
        default="",
        help="Exact locked editorial support string relocated into SCREEN_CARRIER",
    )
    parser.add_argument("--focal-event", default="AUTO", help="Focal event ID, or AUTO")
    parser.add_argument("--seed", type=int, help="Deterministic seed for testing")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rng = random.Random(args.seed) if args.seed is not None else random.Random(secrets.randbits(64))
    history = [] if args.no_state else load_history(args.state_file)
    excluded = set(args.exclude)
    legacy_subject_mode = args.subject_mode
    source_asset_mode = args.source_asset_mode
    requested_subject_origin = args.subject_origin_mode
    requested_subject_assembly = args.subject_assembly
    force_atmospheric = False
    force_repeated = False
    if legacy_subject_mode:
        if legacy_subject_mode == "ATMOSPHERIC_STRUCTURE":
            requested_subject_origin = "ABSTRACT_FORM"
            force_atmospheric = True
        elif legacy_subject_mode in {"CONCRETE_OBJECT", "REPEATED_OBJECT"}:
            requested_subject_origin = "SPECULATIVE_OBJECT"
            force_repeated = legacy_subject_mode == "REPEATED_OBJECT"
            if force_repeated:
                requested_subject_assembly = "REPEATED_FAMILY"
        else:
            source_asset_mode = legacy_subject_mode

    try:
        carrier = choose_carrier(rng, history, excluded, args.carrier)
        layout = choose_layout_family(
            rng,
            carrier["id"],
            history,
            excluded,
            args.layout_family,
            requested_subject_assembly,
        )
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    if source_asset_mode != "NONE":
        subject_origin_mode = "NOT_APPLICABLE_SUPPLIED_IMAGE"
        focal_mode = "HERO_OBJECT"
        render_treatment = next(
            item for item in SUBJECT_CATALOG["render_treatments"]
            if item["id"] == ("FAITHFUL_RETAINED" if source_asset_mode == "FAITHFUL_IMAGE" else "PALETTE_ASSIMILATED")
        )
    else:
        subject_origin_mode = choose_subject_origin_mode(rng, history, requested_subject_origin)
        focal_mode = (
            "ATMOSPHERIC_STRUCTURE" if force_atmospheric else
            choose_focal_mode(rng, history) if subject_origin_mode == "ABSTRACT_FORM" else
            "HERO_OBJECT"
        )
        try:
            render_treatment = choose_render_treatment(
                rng, subject_origin_mode, history, args.render_treatment
            )
        except ValueError as error:
            print(str(error), file=sys.stderr)
            return 2
    concrete_object_requested = subject_origin_mode in {"ARCHIVE_ARTIFACT", "SPECULATIVE_OBJECT"}
    supplied_image_requested = source_asset_mode != "NONE"
    try:
        subject_assembly = choose_subject_assembly(
            layout,
            excluded,
            requested_subject_assembly,
            args.scale_role,
        )
        object_family = choose_object_family(
            rng,
            carrier["id"],
            layout,
            subject_origin_mode,
            history,
            excluded,
            args.object_family if concrete_object_requested else "NONE",
        )
        speculative_morphology = choose_speculative_morphology(
            rng,
            subject_origin_mode,
            object_family,
            history,
            excluded,
            args.speculative_morphology,
        )
        composition = choose_composition(rng, layout, object_family, history, excluded)
        focal_event = choose_focal_event(rng, layout, history, excluded, args.focal_event)
        if supplied_image_requested:
            source_scale_candidates = [
                role for role in SCALE_ROLE_BY_LAYOUT[layout["id"]]
                if role in {"MONUMENTAL_FRAGMENT", "INTEGRATED_HERO", "CENTERPIECE_ARTIFACT", "SPECIMEN_ANCHOR", "REPEATED_FIELD"}
                and role in subject_assembly["allowed_scale_roles"]
            ]
            selected_scale = args.scale_role if args.scale_role != "AUTO" else rng.choice(source_scale_candidates)
            if selected_scale not in source_scale_candidates:
                raise ValueError(f"Scale role {selected_scale} is incompatible with supplied image layout {layout['id']}.")
            scale_role = next(item for item in SUBJECT_CATALOG["scale_roles"] if item["id"] == selected_scale)
        else:
            requested_scale_role = args.scale_role
            if (
                requested_scale_role == "AUTO"
                and subject_origin_mode == "ABSTRACT_FORM"
                and focal_mode == "ATMOSPHERIC_STRUCTURE"
                and layout["id"] != "RHYTHMIC_FIELD"
            ):
                requested_scale_role = "FIELD_STRUCTURE"
            elif (
                requested_scale_role == "AUTO"
                and subject_origin_mode == "ABSTRACT_FORM"
                and focal_mode == "HERO_OBJECT"
            ):
                abstract_hero_roles = [
                    role for role in SCALE_ROLE_BY_LAYOUT[layout["id"]]
                    if role in subject_mode_record(subject_origin_mode)["allowed_scale_roles"]
                    and role != "FIELD_STRUCTURE"
                ]
                requested_scale_role = rng.choice(abstract_hero_roles)
            elif requested_scale_role == "AUTO" and force_repeated:
                requested_scale_role = "REPEATED_FIELD"
            scale_role = choose_scale_role(
                rng,
                subject_origin_mode,
                layout["id"],
                subject_assembly,
                history,
                requested_scale_role,
            )
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    if concrete_object_requested and object_family is None:
        print(f"No concrete object families remain for carrier {carrier['id']} and layout {layout['id']}.", file=sys.stderr)
        return 2
    try:
        screen_state, screen_copy_element, screen_instance_rule = choose_screen_state(
            carrier["id"],
            object_family,
            subject_assembly["id"],
            args.screen_state,
            args.screen_copy_element,
        )
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2

    recent_palettes = {record.get("palette_id", "") for record in history[-3:]}
    palette_candidates = [p for p in PALETTES if p["id"] not in excluded and p["id"] not in recent_palettes]
    palette_candidates = palette_candidates or [p for p in PALETTES if p["id"] not in excluded]
    if not palette_candidates:
        print("No palette families remain after exclusions.", file=sys.stderr)
        return 2
    palette = rng.choice(palette_candidates)

    complexity = weighted_choice(rng, COMPLEXITY_WEIGHTS)
    active_hues = rng.choice(palette["variants"][complexity])

    hero: dict[str, Any] | None = None
    if focal_mode == "HERO_OBJECT" and not concrete_object_requested and not supplied_image_requested:
        try:
            hero = choose_hero_object(rng, composition["gradient_topology"], history, excluded)
        except ValueError as error:
            print(str(error), file=sys.stderr)
            return 2
        primary_form = hero["geometry"]
        primary_form_role = "HERO_OBJECT"
    elif object_family:
        primary_form = (
            f"{object_family['geometry']}; resolve the entire silhouette through "
            f"{speculative_morphology['silhouette']}"
            if speculative_morphology else
            object_family["geometry"]
        )
        primary_form_role = "HERO_OBJECT"
    elif supplied_image_requested:
        primary_form = "one supplied image field or cropped image fragment preserving the subject's identity anchors"
        primary_form_role = "IMAGE_FIELD"
    else:
        primary_form = rng.choice([form for form in composition["primary_forms"] if form not in excluded] or composition["primary_forms"])
        primary_form_role = "ATMOSPHERIC_STRUCTURE"

    use_pale_panel = rng.random() < (0.18 if focal_mode == "HERO_OBJECT" else 0.38)
    editorial_device = rng.choice(PALE_DEVICES) if use_pale_panel else "NONE"
    panel_text_role = rng.choice(["CATEGORY_LABEL", "MICRO_SUBTITLE"]) if use_pale_panel else "NONE"

    if hero:
        allowed_accents = hero["allowed_accents"]
    elif object_family:
        allowed_accents = object_family["allowed_accents"]
    else:
        allowed_accents = ACCENTS if "orb" not in primary_form else ["triangles", "diamonds", "tiny dots", "thin rings", "corner brackets"]
    recent_accents = {record.get("accent_family", "") for record in history[-2:]}
    accent_family = choose_different(rng, allowed_accents, recent_accents)
    bridge_options = composition["bridges"] + ["NONE"]
    forbidden_bridge_tokens: list[str] = []
    if hero:
        forbidden_bridge_tokens = hero["forbidden_bridge_tokens"]
    elif object_family:
        forbidden_bridge_tokens = object_family["forbidden_bridge_tokens"]
    if forbidden_bridge_tokens:
        bridge_options = [
            option for option in bridge_options
            if option == "NONE" or not any(token in option.lower() for token in forbidden_bridge_tokens)
        ]
    bridge = rng.choice(bridge_options or ["NONE"])
    anchor_count = 1
    echo_count = rng.choice([1, 1, 2])

    regime = tonal_regime(palette["id"], complexity, rng)
    recent_fonts = {record.get("font_mode", "") for record in history[-1:]}
    font_mode = choose_font_mode(rng, recent_fonts, regime, primary_form, use_pale_panel)
    label_choices = LABEL_TREATMENTS[:]
    if use_pale_panel:
        label_choices = [choice for choice in label_choices if choice != "thin outlined pill"]
    label_treatment = rng.choice(label_choices)
    title_zone = rng.choice(composition["title_zones"])
    if supplied_image_requested or focal_mode == "ATMOSPHERIC_STRUCTURE":
        subject_preservation_clause = (
            "preserve the supplied subject's 2–4 identity anchors"
            if supplied_image_requested else
            "keep the abstract field non-referential and do not add product-like controls or labels"
        )
        primary_form_placement = (
            f"authoritative layout object slot: {layout['object_slot']}; "
            f"use the side complementary to the {title_zone} title zone only when that heuristic remains compatible with the slot; "
            f"{subject_preservation_clause}; apply crop rule: {layout['crop_rule']}; "
            f"apply scale role {scale_role['id']}: {scale_role['behavior']}"
        )
        spatial_assignment = (
            f"obey the layout collision rule: {layout['collision_rule']} Place the title and supplied image field or atmospheric primary form in the returned relationship; "
            "same-side placement is allowed only for a clear portal opening, counter-shape, framing, or negative-space relationship that preserves both forms"
        )
    else:
        placement = rng.choice((hero or object_family)["placements"])
        relationship = rng.choice((hero or object_family)["title_relationships"])
        primary_form_placement = (
            f"authoritative layout object slot: {layout['object_slot']}; adapt the object's preferred placement cue ({placement}) inside that slot rather than replacing it; "
            f"use the locked title relationship: {relationship}; apply crop rule: {layout['crop_rule']}; "
            f"apply scale role {scale_role['id']}: {scale_role['behavior']}"
        )
        spatial_assignment = (
            f"obey the layout collision rule: {layout['collision_rule']} Distribute visual weight before establishing alignment; "
            "do not concentrate the title, hero, and decorative axis on one side unless the opposite region has a clear compositional role"
        )
    title_clear_zone = (
        "the union of visible title glyph silhouettes plus a calm buffer of about 4% of canvas width; "
        "the primary form's solid silhouette, luminous core, and highest-contrast edge must stay outside it; "
        "soft low-contrast atmosphere may pass behind only when glyph edges and thumbnail readability remain crisp"
    )
    assembly_clause = (
        f"resolve SUBJECT_ASSEMBLY {subject_assembly['id']}: {subject_assembly['mass_rule']}"
    )
    primary_form_placement = f"{primary_form_placement}; {assembly_clause}"

    focal_operator_id = COMPOSITION_GRAMMAR_CATALOG["focal_event_operator_map"][focal_event["id"]]
    composition_operator_ids = list(dict.fromkeys([*layout["required_operators"], focal_operator_id]))
    composition_operators = [
        {
            "id": operator_id,
            "category": OPERATOR_BY_ID[operator_id]["category"],
            "definition": OPERATOR_BY_ID[operator_id]["definition"],
        }
        for operator_id in composition_operator_ids
    ]
    primary_relation = next(
        operator["id"] for operator in composition_operators
        if operator["category"] == "PRIMARY_RELATION"
    )
    support_alignment = next(
        operator["id"] for operator in composition_operators
        if operator["category"] == "SUPPORT_ALIGNMENT"
    )
    composition_sentence = (
        f"TITLE_MASS + {subject_assembly['id']} + {primary_relation} + "
        f"{focal_operator_id} + RELEASE_ZONE + {support_alignment}"
    )

    hero_payload: dict[str, Any] | str = "NONE"
    if hero:
        hero_payload = {
            "id": hero["id"],
            "family": hero["family"],
            "geometry": hero["geometry"],
            "material": f"{hero['material']}; {render_treatment['material_rule']}",
            "lighting": hero["lighting"],
            "scale": scale_role["scale"],
            "placement": rng.choice(hero["placements"]),
            "title_relationship": rng.choice(hero["title_relationships"]),
            "role_scale_rule": f"{scale_role['behavior']} Identically shaped anchors and echoes remain decorative.",
            "subject_assembly": subject_assembly["id"],
            "subject_mass_rule": subject_assembly["mass_rule"],
        }
    elif object_family:
        hero_payload = {
            "id": object_family["id"],
            "family": subject_origin_mode,
            "geometry": object_family["geometry"],
            "material": f"{object_family['material']}; render treatment {render_treatment['id']}: {render_treatment['material_rule']}",
            "lighting": object_family["lighting"],
            "scale": scale_role["scale"],
            "placement": primary_form_placement,
            "title_relationship": "use the object's selected placement and keep its identity anchors outside the title clear zone",
            "identity_anchors": object_family["identity_anchors"],
            "visual_behavior": object_family["visual_behavior"],
            "function_requirement": object_family.get("function_requirement", "preserve the object's real historical function and provenance"),
            "speculative_morphology": speculative_morphology["id"] if speculative_morphology else "NOT_APPLICABLE",
            "morphology_idea": speculative_morphology["idea"] if speculative_morphology else "NOT_APPLICABLE",
            "morphology_silhouette": speculative_morphology["silhouette"] if speculative_morphology else "NOT_APPLICABLE",
            "morphology_exaggeration": speculative_morphology["exaggeration"] if speculative_morphology else "NOT_APPLICABLE",
            "morphology_aperture_rule": speculative_morphology["aperture_rule"] if speculative_morphology else "NOT_APPLICABLE",
            "morphology_construction_cues": speculative_morphology["construction_cues"] if speculative_morphology else "NOT_APPLICABLE",
            "morphology_material_direction": speculative_morphology["material_direction"] if speculative_morphology else "NOT_APPLICABLE",
            "screen_state": screen_state["id"],
            "screen_rendering_rule": screen_state["rendering_rule"],
            "screen_text_rule": screen_state["text_rule"],
            "screen_instance_rule": screen_instance_rule,
            "role_scale_rule": f"{scale_role['behavior']} The object owns the focal scale; supporting accents remain flat and subordinate.",
            "subject_assembly": subject_assembly["id"],
            "subject_mass_rule": subject_assembly["mass_rule"],
        }
    elif supplied_image_requested:
        hero_payload = {
            "id": "SUPPLIED_IMAGE_FIELD",
            "family": "SUPPLIED_IMAGE",
            "geometry": primary_form,
            "material": f"selected supplied-image treatment with exposed atmosphere and crisp title edges; {render_treatment['material_rule']}",
            "lighting": "preserve the supplied subject's defining light and expression; do not add a competing hero light",
            "scale": scale_role["scale"],
            "placement": primary_form_placement,
            "title_relationship": "title locks tightly to the image field while preserving 2–4 identity anchors",
            "identity_anchors": "preserve 2–4 subject-specific identity anchors from the supplied image",
            "role_scale_rule": f"{scale_role['behavior']} The supplied image owns the focal attention; do not add a discrete abstract hero.",
            "subject_assembly": subject_assembly["id"],
            "subject_mass_rule": subject_assembly["mass_rule"],
        }

    signature_form = hero["id"] if hero else object_family["id"] if object_family else primary_form.replace(" ", "_")
    morphology_id = speculative_morphology["id"] if speculative_morphology else "NOT_APPLICABLE"
    signature = ":".join([
        carrier["id"],
        layout["id"],
        subject_origin_mode,
        render_treatment["id"],
        scale_role["id"],
        subject_assembly["id"],
        signature_form,
        morphology_id,
        screen_state["id"],
        focal_event["id"],
        palette["id"],
        complexity,
        composition["id"],
        focal_mode,
    ])
    recipe = {
        "manifest_version": 4,
        "text_contract": carrier["text_contract"],
        "design_signature": signature,
        "carrier_id": carrier["id"],
        "carrier": carrier["name"],
        "carrier_signals": carrier["critical_signals"],
        "layout_family_id": layout["id"],
        "layout_family": layout["name"],
        "layout_select_when": layout["select_when"],
        "layout_dominant_mass": layout["dominant_mass"],
        "layout_attention_contract": layout["attention_contract"],
        "layout_allowed_subject_assemblies": layout["allowed_subject_assemblies"],
        "layout_allowed_scale_roles": layout["allowed_scale_roles"],
        "layout_required_operators": layout["required_operators"],
        "layout_optional_operators": layout["optional_operators"],
        "layout_forbidden_relationships": layout["forbidden_relationships"],
        "layout_subject_area_percent": layout["subject_area_percent"],
        "layout_release_area_percent": layout["release_area_percent"],
        "layout_title_zone": layout["title_zone"],
        "layout_object_slot": layout["object_slot"],
        "layout_collision_rule": layout["collision_rule"],
        "layout_support_zones": layout["support_zones"],
        "layout_crop_rule": layout["crop_rule"],
        "layout_required_structure": layout["required_structure"],
        "layout_failure_signals": layout["failure_signals"],
        "layout_thumbnail_test": layout["thumbnail_test"],
        "composition_primitives": [primitive["id"] for primitive in COMPOSITION_GRAMMAR_CATALOG["primitives"]],
        "subject_assembly": subject_assembly["id"],
        "subject_assembly_count": subject_assembly["count"],
        "subject_mass_rule": subject_assembly["mass_rule"],
        "composition_operators": composition_operators,
        "composition_sentence": composition_sentence,
        "subject_origin_mode": subject_origin_mode,
        "subject_origin_definition": (
            "supplied image source override" if supplied_image_requested else subject_mode_record(subject_origin_mode)["definition"]
        ),
        "subject_identity_contract": (
            "preserve 2–4 source-specific identity anchors" if supplied_image_requested else subject_mode_record(subject_origin_mode)["identity_contract"]
        ),
        "render_treatment": render_treatment["id"],
        "render_treatment_definition": render_treatment["definition"],
        "render_color_rule": render_treatment["color_rule"],
        "scale_role": scale_role["id"],
        "scale_role_scale": scale_role["scale"],
        "scale_role_behavior": scale_role["behavior"],
        "source_asset_mode": source_asset_mode,
        "image_role": (
            "HERO_PHOTOGRAPH" if source_asset_mode == "FAITHFUL_IMAGE" else
            "CROPPED_FRAGMENT" if source_asset_mode == "ABSTRACT_SYMBOL" else
            "REPEATED_SPECIMEN" if scale_role["id"] == "REPEATED_FIELD" else
            "NONE"
        ),
        "object_family_id": object_family["id"] if object_family else "NONE",
        "object_family": object_family["name"] if object_family else "NONE",
        "speculative_morphology": morphology_id,
        "speculative_morphology_definition": speculative_morphology["idea"] if speculative_morphology else "NOT_APPLICABLE",
        "speculative_morphology_silhouette": speculative_morphology["silhouette"] if speculative_morphology else "NOT_APPLICABLE",
        "speculative_morphology_exaggeration": speculative_morphology["exaggeration"] if speculative_morphology else "NOT_APPLICABLE",
        "speculative_morphology_aperture_rule": speculative_morphology["aperture_rule"] if speculative_morphology else "NOT_APPLICABLE",
        "speculative_morphology_construction_cues": speculative_morphology["construction_cues"] if speculative_morphology else "NOT_APPLICABLE",
        "speculative_morphology_material_direction": speculative_morphology["material_direction"] if speculative_morphology else "NOT_APPLICABLE",
        "speculative_global_form_ancestry": (
            SPECULATIVE_MORPHOLOGY_CATALOG["global_contract"]["form_ancestry"]
            if speculative_morphology else "NOT_APPLICABLE"
        ),
        "speculative_global_construction_order": (
            SPECULATIVE_MORPHOLOGY_CATALOG["global_contract"]["construction_order"]
            if speculative_morphology else "NOT_APPLICABLE"
        ),
        "speculative_global_required_character": (
            SPECULATIVE_MORPHOLOGY_CATALOG["global_contract"]["required_character"]
            if speculative_morphology else "NOT_APPLICABLE"
        ),
        "speculative_global_hard_failures": (
            SPECULATIVE_MORPHOLOGY_CATALOG["global_contract"]["hard_failures"]
            if speculative_morphology else "NOT_APPLICABLE"
        ),
        "screen_state": screen_state["id"],
        "screen_state_definition": screen_state["definition"],
        "screen_content_role": screen_state["content_role"],
        "screen_content_source": screen_state["content_source"],
        "screen_display_language": screen_state["display_language"],
        "screen_copy_element": screen_copy_element,
        "screen_rendering_rule": screen_state["rendering_rule"],
        "screen_text_rule": screen_state["text_rule"],
        "screen_attention_rule": screen_state["attention_rule"],
        "screen_instance_rule": screen_instance_rule,
        "intrinsic_artifact_text_policy": (
            SUBJECT_CATALOG["intrinsic_artifact_text"]["policy"]
            if subject_origin_mode == "ARCHIVE_ARTIFACT" or source_asset_mode == "FAITHFUL_IMAGE"
            else "NOT_APPLICABLE"
        ),
        "focal_event_id": focal_event["id"],
        "focal_event": focal_event["definition"],
        "release_zone": focal_event["release_zone"],
        "focal_event_thumbnail_test": focal_event["thumbnail_test"],
        "palette": palette["name"],
        "palette_id": palette["id"],
        "palette_family": palette["name"],
        "color_complexity": complexity,
        "active_hues": active_hues,
        "derived_tints": "derive pale, mid, and soft-deep tones only from the active hues",
        "area_hierarchy": area_hierarchy(complexity),
        "saturation_rule": "allow only one saturation focus; render all other hues as softened fields, haze, or translucent layers",
        "tonal_regime": regime,
        "harmony_mode": harmony_mode(complexity, active_hues),
        "coral_role": coral_role(active_hues),
        "composition_id": composition["id"],
        "focal_mode": focal_mode,
        "gradient_topology": composition["gradient_topology"],
        "gradient_direction": composition["gradient_direction"],
        "primary_form_role": primary_form_role,
        "primary_form": primary_form,
        "primary_form_placement": primary_form_placement,
        "hero_object": hero_payload,
        "title_zone": title_zone,
        "spatial_assignment": spatial_assignment,
        "title_clear_zone": title_clear_zone,
        "primary_form_clearance": (
            "CATEGORY_LABEL outlines, ANCHOR, ECHO, and decorative lines must not cross the primary form's core contour, highest-contrast region, or visual center; "
            "place them along an outer edge, tangent, or extended axis instead"
        ),
        "collision_resolution": (
            "preserve approved wording and readable title scale; use balanced reflow when suitable, otherwise translate or modestly scale the primary form; "
            "never preserve centered placement at the cost of glyph clearance"
        ),
        "editorial_device": editorial_device,
        "panel_text_role": panel_text_role,
        "detail_roles": {
            "anchor": f"{anchor_count} focal {accent_family} instance",
            "bridge": bridge,
            "echo": f"{echo_count} much smaller {accent_family} echo instance(s)",
        },
        "detail_limits": (
            "the hero owns the dimensional or glow budget; supporting accents stay flat, anchors remain 3–8% of the short edge, echoes remain 1–3%, and accents stay under 1% combined canvas area; at most one compatible bridge"
            if hero else
            "one accent language plus at most one hairline bridge; accents under 2% combined canvas area"
        ),
        "type_mode": font_mode,
        "detail_grammar": "one ANCHOR, zero or one BRIDGE, and one or two ECHO instances using one returned accent language",
        "font_mode": font_mode,
        "label_treatment": label_treatment,
        "alignment_system": (
            "first distribute visual weight across complementary regions, then align at least three of title, hero or atmospheric form, panel, label, bridge, and accents "
            "through a shared edge, axis, tangent, baseline, or curvature; the relationship may span the canvas and must not stack all high-information elements in one region"
        ),
    }

    if not args.no_state:
        record = {
            "design_signature": signature,
            "carrier_id": carrier["id"],
            "layout_family": layout["id"],
            "subject_origin_mode": subject_origin_mode,
            "render_treatment": render_treatment["id"],
            "scale_role": scale_role["id"],
            "subject_assembly": subject_assembly["id"],
            "object_family": object_family["id"] if object_family else "NONE",
            "speculative_morphology": morphology_id,
            "screen_state": screen_state["id"],
            "focal_event": focal_event["id"],
            "palette_id": palette["id"],
            "color_complexity": complexity,
            "gradient_topology": composition["gradient_topology"],
            "focal_mode": focal_mode,
            "primary_form": primary_form,
            "hero_id": hero["id"] if hero else "NONE",
            "hero_family": hero["family"] if hero else "NONE",
            "accent_family": accent_family,
            "font_mode": font_mode,
        }
        try:
            save_history(args.state_file, (history + [record])[-3:])
        except OSError as error:
            print(f"Warning: could not update design history: {error}", file=sys.stderr)

    print(json.dumps(recipe, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
