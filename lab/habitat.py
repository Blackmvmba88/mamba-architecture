"""Generador conceptual determinista de módulos de hábitat (sin cálculo estructural)."""
import argparse
import json
from pathlib import Path

PRESETS = {
    "habitat_arctic": (5.5, 7.0, 3.1, 4),
    "capsule_living": (5.0, 7.0, 2.9, 3),
    "bioshell": (6.0, 6.0, 3.0, 2),
    "forest_tower": (6.5, 6.5, 3.2, 4),
    "stone_water": (7.0, 8.0, 3.0, 3),
    "canal_district": (4.0, 9.0, 3.0, 3),
    "sacred_pavilion": (8.0, 8.0, 3.6, 1),
}

def generate(preset: str, levels: int | None = None) -> dict:
    if preset not in PRESETS:
        raise ValueError(f"Unknown preset: {preset}")
    width, depth, height, default_levels = PRESETS[preset]
    levels = default_levels if levels is None else levels
    if isinstance(levels, bool) or not isinstance(levels, int) or not 1 <= levels <= 12:
        raise ValueError("levels must be an integer from 1 to 12")
    modules = []
    for index in range(levels):
        # Offset is a stylistic concept, not a checked cantilever.
        offset = round((index % 2) * width * 0.12, 4)
        modules.append({
            "id": f"M{index + 1:02d}",
            "center_m": [offset, 0.0, round(height * (index + 0.5), 4)],
            "size_m": [width, depth, height],
        })
    return {
        "schema_version": "0.1.0",
        "preset": preset,
        "units": "m",
        "levels": levels,
        "modules": modules,
        "assumptions": [
            "Conceptual geometric volumes only",
            "No loads, foundations, support members or stability calculations",
            "No code compliance, fire safety or accessibility verified",
        ],
        "validation": {"digital_geometry": "unverified", "structural": "not_assessed", "build_ready": False},
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=sorted(PRESETS), default="habitat_arctic")
    parser.add_argument("--levels", type=int)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = json.dumps(generate(args.preset, args.levels), indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")

if __name__ == "__main__":
    main()
