"""Blender adapter for conceptual radial layouts. Run with Blender Python."""
import argparse
import json
import math
import sys
from pathlib import Path

def validate(data):
    if data.get("kind") != "conceptual_style" or data.get("units") != "m":
        raise ValueError("expected conceptual_style with meter units")
    geometry=data.get("geometry",{})
    points=geometry.get("ring_points_m")
    if not isinstance(points,list) or not 6 <= len(points) <= 128:
        raise ValueError("invalid ring points")
    for point in points:
        if len(point)!=3 or any(not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v) for v in point):
            raise ValueError("non-finite or invalid point")
    if geometry.get("ring_edges") != [[i,(i+1)%len(points)] for i in range(len(points))]:
        raise ValueError("unexpected ring edge topology")
    if geometry.get("radial_edges") != [[len(points),i] for i in range(len(points))]:
        raise ValueError("unexpected spoke topology")
    if geometry.get("center_point_m") != [0.0,0.0,0.0]:
        raise ValueError("unexpected origin")
    return points

def prism_geometry(points, height_m):
    """Closed radial prism; style metadata does not imply typology geometry."""
    if isinstance(height_m, bool) or not isinstance(height_m, (int, float)) or not math.isfinite(height_m) or not 0 < height_m <= 100:
        raise ValueError("height_m must be finite, >0..100")
    if any(p[2] != 0 for p in points):
        raise ValueError("prism requires a planar ring at z=0")
    n = len(points)
    vertices = [tuple(p) for p in points] + [(p[0], p[1], height_m) for p in points]
    faces = [tuple(reversed(range(n))), tuple(range(n, 2*n))]
    faces += [(i, (i+1)%n, (i+1)%n+n, i+n) for i in range(n)]
    return vertices, faces


def build(data, output, height_m=None, typology=False, roof_rise_m=2.0, courtyard_ratio=0.4):
    import bpy
    points=validate(data)
    # Isolated in a new Blender process: never clear or overwrite user-open scenes.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mesh=bpy.data.meshes.new("RadialPlan")
    model = None
    if typology:
        from lab.typology_geometry import generate_typology
        model = generate_typology(data['style']['id'], data['geometry']['radius_m'],
                                  height_m if height_m is not None else 3.0, len(points),
                                  roof_rise_m, courtyard_ratio)
        vertices, faces, edges = model['vertices'], model['faces'], []
    elif height_m is None:
        vertices = [tuple(p) for p in points] + [(0, 0, 0)]
        edges = data["geometry"]["ring_edges"] + data["geometry"]["radial_edges"]
        faces = []
    else:
        vertices, faces = prism_geometry(points, height_m)
        edges = []
    mesh.from_pydata(vertices, edges, faces)
    mesh.update()
    obj=bpy.data.objects.new("Conceptual_Radial_Plan",mesh)
    bpy.context.collection.objects.link(obj)
    obj["status"]="CONCEPT_ONLY_NOT_STRUCTURAL"
    obj["source_style"]=data["style"]["id"]
    obj["source_parameters_json"] = json.dumps(data, sort_keys=True)
    if height_m is not None:
        obj["height_m"] = height_m
    if model:
        obj["typology_parameters_json"] = json.dumps(model['parameters'], sort_keys=True)
        obj["typology"] = model['kind']
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0
    output=Path(output)
    if output.suffix.lower()!=".blend":
        raise ValueError("output must end in .blend")
    if output.exists():
        raise FileExistsError("refusing to overwrite an existing .blend file")
    output.parent.mkdir(parents=True,exist_ok=True)
    measured=[list(v.co) for v in obj.data.vertices]
    expected=[[float(v) for v in p] for p in vertices]
    if any(not math.isclose(actual, target, rel_tol=1e-7, abs_tol=1e-6)
           for point, source in zip(measured, expected) for actual, target in zip(point, source)):
        raise RuntimeError("Blender measured geometry differs from source")
    area = abs(sum(points[i][0]*points[(i+1)%len(points)][1] - points[(i+1)%len(points)][0]*points[i][1] for i in range(len(points)))) / 2
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(mesh)
    volume = abs(bm.calc_volume(signed=True)) if faces else None
    closed = all(e.is_manifold for e in bm.edges) if faces else False
    bm.free()
    expected_volume = model['expected_volume_m3'] if model else area*height_m if faces else None
    if faces and (not closed or not math.isclose(volume, expected_volume, rel_tol=1e-6)):
        raise RuntimeError("Blender volume/topology differs from expected mass")
    bpy.ops.wm.save_as_mainfile(filepath=str(output.resolve()))
    return {"typology": model['kind'] if model else 'radial_prism' if faces else 'radial_plan',
            "footprint_area_m2": model['footprint_area_m2'] if model else area, "volume_m3": volume, "closed_manifold": closed,
            "height_m": height_m, "faces": len(mesh.polygons), "source_style":data["style"]["id"],"vertices":len(measured),
            "edges":len(mesh.edges),"geometry_match":True,"build_ready":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--report",type=Path)
    p.add_argument("--typology", action="store_true", help="Generate the style's conceptual mass")
    p.add_argument("--roof-rise", type=float, default=2.0)
    p.add_argument("--courtyard-ratio", type=float, default=0.4)
    p.add_argument("--height", type=float, help="Optional closed radial prism height in meters")
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    if args.report and args.report.exists():
        raise FileExistsError("refusing to overwrite existing report")
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    result=build(json.loads(args.input.read_text(encoding="utf-8")),args.output, args.height, args.typology, args.roof_rise, args.courtyard_ratio)
    if args.report:
        if args.report.exists():
            raise FileExistsError("refusing to overwrite existing report")
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result))

if __name__=="__main__":
    main()
