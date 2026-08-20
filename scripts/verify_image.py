#!/usr/bin/env python3
"""Verify a cover image's readable format, exact dimensions, and aspect ratio."""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path


def png_size(data: bytes) -> tuple[int, int] | None:
    if len(data) >= 24 and data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR":
        return struct.unpack(">II", data[16:24])
    return None


def jpeg_size(data: bytes) -> tuple[int, int] | None:
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        return None

    offset = 2
    sof_markers = {
        0xC0,
        0xC1,
        0xC2,
        0xC3,
        0xC5,
        0xC6,
        0xC7,
        0xC9,
        0xCA,
        0xCB,
        0xCD,
        0xCE,
        0xCF,
    }

    while offset + 1 < len(data):
        if data[offset] != 0xFF:
            offset += 1
            continue
        while offset < len(data) and data[offset] == 0xFF:
            offset += 1
        if offset >= len(data):
            break
        marker = data[offset]
        offset += 1
        if marker in {0xD8, 0xD9}:
            continue
        if marker == 0xDA:
            break
        if offset + 2 > len(data):
            break
        segment_length = struct.unpack(">H", data[offset : offset + 2])[0]
        if segment_length < 2 or offset + segment_length > len(data):
            break
        if marker in sof_markers and segment_length >= 7:
            height, width = struct.unpack(">HH", data[offset + 3 : offset + 7])
            return width, height
        offset += segment_length
    return None


def inspect_image(path: Path) -> tuple[str, int, int]:
    data = path.read_bytes()
    dimensions = png_size(data)
    if dimensions:
        return "PNG", dimensions[0], dimensions[1]
    dimensions = jpeg_size(data)
    if dimensions:
        return "JPEG", dimensions[0], dimensions[1]
    raise ValueError("unsupported or unreadable image; expected PNG or JPEG")


def parse_ratio(value: str) -> tuple[int, int]:
    parts = value.split(":", 1)
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("ratio must use W:H form, for example 3:4")
    try:
        width, height = (int(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("ratio values must be integers") from exc
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("ratio values must be positive")
    return width, height


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--ratio", type=parse_ratio)
    parser.add_argument(
        "--format",
        dest="expected_format",
        choices=("PNG", "JPEG"),
        default="PNG",
        help="expected output format (default: PNG)",
    )
    args = parser.parse_args()

    errors: list[str] = []
    result: dict[str, object] = {
        "path": str(args.image),
        "expected": {
            "format": args.expected_format,
            "width": args.width,
            "height": args.height,
        },
    }

    if args.width <= 0 or args.height <= 0:
        errors.append("expected width and height must be positive")

    try:
        detected_format, width, height = inspect_image(args.image)
        result["actual"] = {
            "format": detected_format,
            "width": width,
            "height": height,
            "ratio": f"{width}:{height}",
        }
        if detected_format != args.expected_format:
            errors.append(
                f"format mismatch: expected {args.expected_format}, got {detected_format}"
            )
        if width != args.width or height != args.height:
            errors.append(
                f"dimension mismatch: expected {args.width}x{args.height}, got {width}x{height}"
            )

        ratio_width, ratio_height = args.ratio or (args.width, args.height)
        if width * ratio_height != height * ratio_width:
            errors.append(
                f"ratio mismatch: expected {ratio_width}:{ratio_height}, got {width}:{height}"
            )
        result["expected"]["ratio"] = f"{ratio_width}:{ratio_height}"
    except (OSError, ValueError) as exc:
        errors.append(str(exc))

    result["passed"] = not errors
    result["errors"] = errors
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
