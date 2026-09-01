#!/usr/bin/env python3
"""Verify that checked-in visual regression proofs use the canonical canvas."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "scripts" / "verify_image.py"


def main() -> int:
    images = sorted((ROOT / "examples").rglob("*.png"))
    images.extend(sorted((ROOT / "evals" / "visual").glob("*/proofs/*.png")))
    if not images:
        print("FAIL: no example PNGs found")
        return 1

    failures: list[str] = []
    for image in images:
        result = subprocess.run(
            [
                "python3",
                "-B",
                str(VERIFY),
                str(image),
                "--width",
                "1080",
                "--height",
                "1440",
                "--ratio",
                "3:4",
                "--format",
                "PNG",
            ],
            text=True,
            capture_output=True,
        )
        if result.returncode:
            failures.append(f"{image.name}: {result.stdout.strip() or result.stderr.strip()}")

    if failures:
        print("FAIL: example image verification")
        print("\n".join(failures))
        return 1
    print(f"PASS: {len(images)} example and visual-proof images at 1080x1440 PNG")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
