"""Preflight independiente de Blender para parámetros de la escena invernal.

Uso: python3 preflight.py [parameters.json]
No modifica archivos, no renderiza y no requiere paquetes externos.
"""
import json
import math
import sys
from pathlib import Path


def validate(data):
    errors = []
    positive = (
        "width", "depth", "wall", "storey", "roof_rise",
        "window_width", "window_height", "camera_ortho_scale",
        "render_width", "render_height", "render_samples",
    )
    nonnegative = ("base", "overhang")
    for key in positive + nonnegative:
        value = data.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors.append(f"{key}: falta número válido")
        elif not math.isfinite(value) or (value <= 0 if key in positive else value < 0):
            errors.append(f"{key}: debe ser {'positivo' if key in positive else 'no negativo'} y finito")

    for key in ("render_width", "render_height", "render_samples"):
        value = data.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value):
            if not isinstance(value, int):
                errors.append(f"{key}: debe ser entero")

    for key in ("window_axes", "dormer_axes"):
        axes = data.get(key)
        if not isinstance(axes, list) or not axes:
            errors.append(f"{key}: lista no vacía requerida")
            continue
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in axes):
            errors.append(f"{key}: coordenadas numéricas finitas requeridas")
            continue
        if len(set(axes)) != len(axes):
            errors.append(f"{key}: ejes duplicados")
        if axes != sorted(axes):
            errors.append(f"{key}: ordenar ejes de izquierda a derecha")
        width = data.get("width")
        clearance = data.get("window_width") if key == "window_axes" else 1.65
        if isinstance(width, (int, float)) and not isinstance(width, bool) and isinstance(clearance, (int, float)):
            if width > 0 and clearance > 0 and any(abs(v) + clearance / 2 >= width / 2 for v in axes):
                errors.append(f"{key}: elemento fuera de la fachada (comprobación aproximada)")

    if isinstance(data.get("seed"), bool) or not isinstance(data.get("seed"), int):
        errors.append("seed: se requiere entero")

    for key in ("camera_location", "camera_target"):
        vec = data.get(key)
        if not isinstance(vec, list) or len(vec) != 3 or any(
            isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in vec
        ):
            errors.append(f"{key}: se requieren tres coordenadas finitas")
    if not errors:
        if data["wall"] * 2 >= min(data["width"], data["depth"]):
            errors.append("wall: espesor consume el interior")
        if data["window_height"] >= data["storey"]:
            errors.append("window_height: debe ser menor que storey")
        if data["camera_location"] == data["camera_target"]:
            errors.append("camera: posición y objetivo coinciden")
    return errors


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("parameters.json")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("se espera un objeto JSON")
    except (OSError, ValueError) as exc:
        print(f"FAIL: no se pudieron leer parámetros: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    for error in errors:
        print("FAIL:", error, file=sys.stderr)
    if errors:
        return 1
    print("PASS: preflight paramétrico (sin Blender)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
