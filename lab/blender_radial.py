"""Blender adapter for conceptual radial layouts. Run with Blender Python."""
import argparse
import json
import math
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

def build(data, output):
    import bpy
    points=validate(data)
    # Isolated in a new Blender process: never clear or overwrite user-open scenes.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mesh=bpy.data.meshes.new("RadialPlan")
    mesh.from_pydata([tuple(p) for p in points]+[(0,0,0)],data["geometry"]["ring_edges"]+data["geometry"]["radial_edges"],[])
    mesh.update()
    obj=bpy.data.objects.new("Conceptual_Radial_Plan",mesh)
    bpy.context.collection.objects.link(obj)
    obj["status"]="CONCEPT_ONLY_NOT_STRUCTURAL"
    obj["source_style"]=data["style"]["id"]
    output=Path(output)
    if output.suffix.lower()!=".blend":
        raise ValueError("output must end in .blend")
    if output.exists():
        raise FileExistsError("refusing to overwrite an existing .blend file")
    output.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(output.resolve()))
    measured=[[round(v.co.x,6),round(v.co.y,6),round(v.co.z,6)] for v in obj.data.vertices]
    expected=[[round(float(v),6) for v in p] for p in points]+[[0.0,0.0,0.0]]
    if measured!=expected:
        raise RuntimeError("Blender measured geometry differs from source")
    return {"source_style":data["style"]["id"],"vertices":len(measured),
            "edges":len(mesh.edges),"geometry_match":True,"build_ready":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--report",type=Path)
    args=p.parse_args()
    result=build(json.loads(args.input.read_text(encoding="utf-8")),args.output)
    if args.report:
        if args.report.exists():
            raise FileExistsError("refusing to overwrite existing report")
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result))

if __name__=="__main__":
    main()
