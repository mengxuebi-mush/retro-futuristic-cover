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
    parser.add_argument("--exclude", action="append", default=[], help="Exclude a palette, composition, topology, form, or signature ID")
    parser.add_argument("--seed", type=int, help="Deterministic seed for testing")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rng = random.Random(args.seed) if args.seed is not None else random.Random(secrets.randbits(64))
    history = [] if args.no_state else load_history(args.state_file)
    excluded = set(args.exclude)
    focal_mode = choose_focal_mode(rng, history)

    recent_palettes = {record.get("palette_id", "") for record in history[-3:]}
    palette_candidates = [p for p in PALETTES if p["id"] not in excluded and p["id"] not in recent_palettes]
    palette_candidates = palette_candidates or [p for p in PALETTES if p["id"] not in excluded]
    if not palette_candidates:
        print("No palette families remain after exclusions.", file=sys.stderr)
        return 2
    palette = rng.choice(palette_candidates)

    complexity = weighted_choice(rng, COMPLEXITY_WEIGHTS)
    active_hues = rng.choice(palette["variants"][complexity])

    recent_topologies = {record.get("gradient_topology", "") for record in history[-2:]}
    composition_candidates = [
        c for c in COMPOSITIONS
        if c["id"] not in excluded
        and c["gradient_topology"] not in excluded
        and c["gradient_topology"] not in recent_topologies
    ]
    composition_candidates = composition_candidates or [c for c in COMPOSITIONS if c["id"] not in excluded]
    if not composition_candidates:
        print("No composition families remain after exclusions.", file=sys.stderr)
        return 2
    composition = rng.choice(composition_candidates)
    hero: dict[str, Any] | None = None
    if focal_mode == "HERO_OBJECT":
        try:
            hero = choose_hero_object(rng, composition["gradient_topology"], history, excluded)
        except ValueError as error:
            print(str(error), file=sys.stderr)
            return 2
        primary_form = hero["geometry"]
        primary_form_role = "HERO_OBJECT"
    else:
        primary_form = rng.choice([form for form in composition["primary_forms"] if form not in excluded] or composition["primary_forms"])
        primary_form_role = "ATMOSPHERIC_STRUCTURE"

    use_pale_panel = rng.random() < (0.18 if focal_mode == "HERO_OBJECT" else 0.38)
    editorial_device = rng.choice(PALE_DEVICES) if use_pale_panel else "NONE"
    panel_text_role = rng.choice(["CATEGORY_LABEL", "MICRO_SUBTITLE"]) if use_pale_panel else "NONE"

    if hero:
        allowed_accents = hero["allowed_accents"]
    else:
        allowed_accents = ACCENTS if "orb" not in primary_form else ["triangles", "diamonds", "tiny dots", "thin rings", "corner brackets"]
    recent_accents = {record.get("accent_family", "") for record in history[-2:]}
    accent_family = choose_different(rng, allowed_accents, recent_accents)
    bridge_options = composition["bridges"] + ["NONE"]
    if hero:
        bridge_options = [
            option for option in bridge_options
            if option == "NONE" or not any(token in option for token in hero["forbidden_bridge_tokens"])
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
    if focal_mode == "ATMOSPHERIC_STRUCTURE":
        primary_form_placement = (
            f"{complementary_side(title_zone)} side, offset or edge-cropped as needed; "
            f"use the space complementary to the {title_zone} title zone"
        )
        spatial_assignment = (
            "place the title and atmospheric primary form in complementary regions; same-side placement is allowed only for a clear portal opening, "
            "counter-shape, framing, or negative-space relationship that preserves both forms; distribute visual weight before establishing alignment"
        )
    else:
        primary_form_placement = "follow HERO_OBJECT.placement and its locked title relationship"
        spatial_assignment = (
            "distribute visual weight before establishing alignment; do not concentrate the title, hero, and decorative axis on one side unless the opposite region has a clear compositional role"
        )
    title_clear_zone = (
        "the union of visible title glyph silhouettes plus a calm buffer of about 4% of canvas width; "
        "the primary form's solid silhouette, luminous core, and highest-contrast edge must stay outside it; "
        "soft low-contrast atmosphere may pass behind only when glyph edges and thumbnail readability remain crisp"
    )

    hero_payload: dict[str, Any] | str = "NONE"
    if hero:
        hero_payload = {
            "id": hero["id"],
            "family": hero["family"],
            "geometry": hero["geometry"],
            "material": hero["material"],
            "lighting": hero["lighting"],
            "scale": hero["scale"],
            "placement": rng.choice(hero["placements"]),
            "title_relationship": rng.choice(hero["title_relationships"]),
            "role_scale_rule": "hero scale and lighting apply only to this HERO_OBJECT; identically shaped anchors and echoes remain decorative",
        }

    signature_form = hero["id"] if hero else primary_form.replace(" ", "_")
    signature = ":".join([palette["id"], complexity, composition["id"], focal_mode, signature_form])
    recipe = {
        "design_signature": signature,
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
