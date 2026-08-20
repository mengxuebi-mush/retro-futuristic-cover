#!/usr/bin/env python3
"""Select a coordinated, variable-complexity editorial-cover design recipe."""

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
FONT_MODES = ["CJK_EDITORIAL_SONG", "CJK_NEO_GROTESK"]
LABEL_TREATMENTS = ["plain label with short rule", "thin outlined pill", "minimal corner alignment"]


def default_state_file() -> Path:
    override = os.environ.get("RETRO_COVER_STATE_FILE")
    if override:
        return Path(override).expanduser()
    return Path(tempfile.gettempdir()) / "retro-editorial-cover-design-history.json"


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
    primary_form = rng.choice([form for form in composition["primary_forms"] if form not in excluded] or composition["primary_forms"])

    use_pale_panel = rng.random() < 0.38
    editorial_device = rng.choice(PALE_DEVICES) if use_pale_panel else "NONE"
    panel_text_role = rng.choice(["CATEGORY_LABEL", "MICRO_SUBTITLE"]) if use_pale_panel else "NONE"

    allowed_accents = ACCENTS if "orb" not in primary_form else ["triangles", "diamonds", "tiny dots", "thin rings", "corner brackets"]
    recent_accents = {record.get("accent_family", "") for record in history[-2:]}
    accent_family = choose_different(rng, allowed_accents, recent_accents)
    bridge = rng.choice(composition["bridges"] + ["NONE"])
    anchor_count = 1
    echo_count = rng.choice([1, 1, 2])

    recent_fonts = {record.get("font_mode", "") for record in history[-1:]}
    font_mode = choose_different(rng, FONT_MODES, recent_fonts)
    label_choices = LABEL_TREATMENTS[:]
    if use_pale_panel:
        label_choices = [choice for choice in label_choices if choice != "thin outlined pill"]
    label_treatment = rng.choice(label_choices)
    title_zone = rng.choice(composition["title_zones"])

    regime = tonal_regime(palette["id"], complexity, rng)
    signature = ":".join([palette["id"], complexity, composition["id"], primary_form.replace(" ", "_")])
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
        "gradient_topology": composition["gradient_topology"],
        "gradient_direction": composition["gradient_direction"],
        "primary_form": primary_form,
        "title_zone": title_zone,
        "editorial_device": editorial_device,
        "panel_text_role": panel_text_role,
        "detail_roles": {
            "anchor": f"{anchor_count} focal {accent_family} instance",
            "bridge": bridge,
            "echo": f"{echo_count} much smaller {accent_family} echo instance(s)",
        },
        "detail_limits": "one accent language plus at most one hairline bridge; accents under 2% combined canvas area",
        "font_mode": font_mode,
        "label_treatment": label_treatment,
        "alignment_system": "align at least three of title, panel or primary form, label, bridge, and accents to a shared edge, axis, tangent, baseline, or curvature",
    }

    if not args.no_state:
        record = {
            "design_signature": signature,
            "palette_id": palette["id"],
            "color_complexity": complexity,
            "gradient_topology": composition["gradient_topology"],
            "primary_form": primary_form,
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
