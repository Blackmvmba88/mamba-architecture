"""Independent second-process audit of saved Sacred Dome Blender geometry."""
import argparse
import json
import math
from pathlib import Path
import sys

def audit(source,blend,tolerance=2e-5):
    import bpy
    from lab.blender_sacred_dome import canonical_hash,validate
    vertices,faces=validate(source)
    blend=Path(blend).resolve()
    if not blend.is_file():
        raise FileNotFoundError(blend)
    bpy.ops.wm.open_mainfile(filepath=str(blend))
    obj=bpy.data.objects.get("SacredDome_P2_Roof")
    if obj is None or obj.type!="MESH":
        raise ValueError("Roof mesh missing")
    mesh=obj.data
    if obj.get("source_sha256")!=canonical_hash(source):
        raise ValueError("Input hash differs")
    if len(mesh.vertices)!=len(vertices) or len(mesh.polygons)!=len(faces):
        raise ValueError("Topology count differs")
    if any(len(poly.vertices)!=4 or list(poly.vertices)!=expected for poly,expected in zip(mesh.polygons,faces)):
        raise ValueError("Face connectivity differs")
    if any(abs(float(got)-float(want))>tolerance for v,expected in zip(mesh.vertices,vertices) for got,want in zip(v.co,expected)):
        raise ValueError("Coordinates differ from input")
    if any(abs(float(c)-t)>tolerance for c,t in zip(obj.matrix_world,( (1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1) )) for _ in []):
        raise ValueError("Transform differs")
    if not all(abs(obj.matrix_world[i][j]-(1 if i==j else 0))<1e-7 for i in range(4) for j in range(4)):
        raise ValueError("Unexpected object transform")
    return {"verified":True,"file":str(blend),"input_sha256":canonical_hash(source),
            "vertices":len(vertices),"quads":len(faces),"max_tolerance_m":tolerance,
            "open_surface":True,"build_ready":False}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",type=Path,required=True)
    ap.add_argument("--blend",type=Path,required=True)
    ap.add_argument("--report",type=Path)
    args=ap.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:])
    source=json.loads(args.input.read_text(encoding="utf-8"))
    result=audit(source,args.blend)
    if args.report:
        if args.report.exists():
            raise FileExistsError("Report exists")
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
    main()
