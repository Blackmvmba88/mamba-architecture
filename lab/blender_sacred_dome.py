"""Write Sacred Dome P2 roof mesh to a NEW .blend file; conceptual only."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

def canonical_hash(document):
    payload=json.dumps(document,sort_keys=True,ensure_ascii=False,separators=(",",":"),allow_nan=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def validate(document):
    if document.get("kind")!="sacred_dome_p2" or document.get("units")!="m":
        raise ValueError("Expected sacred_dome_p2 document in meters")
    p=document["parameters"]
    n,rings=p["segments"],p["roof_rings"]
    vertices=document["roof_mesh"]["vertices_m"]
    faces=document["roof_mesh"]["quad_faces"]
    if not isinstance(n,int) or isinstance(n,bool) or not 8<=n<=64 or not isinstance(rings,int) or not 2<=rings<=30:
        raise ValueError("Invalid tessellation")
    if len(vertices)!=(rings+1)*n or len(faces)!=rings*n:
        raise ValueError("Unexpected vertex/face count")
    if any(len(v)!=3 or any(isinstance(x,bool) or not isinstance(x,(float,int)) or not math.isfinite(x) for x in v) for v in vertices):
        raise ValueError("Invalid vertices")
    expected=[[j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i] for j in range(rings) for i in range(n)]
    if faces!=expected:
        raise ValueError("Invalid roof connectivity")
    radius=p["radius_m"]
    rise=p["roof_rise_m"]
    wall=p["wall_height_m"]
    ratio=p["oculus_ratio"]
    if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) for x in (radius,rise,wall,ratio)):
        raise ValueError("Invalid parameters")
    if not (2<=radius<=40 and 2<=wall<=12 and 0.5<=rise<=20 and 0.05<=ratio<=0.5):
        raise ValueError("Parameters out of bounds")
    for j in range(rings+1):
        r=radius*(1-(1-ratio)*j/rings)
        z=wall+rise*(1-(r/radius)**2)
        for i in range(n):
            t=2*math.pi*i/n
            actual=vertices[j*n+i]
            target=(round(r*math.cos(t),6),round(r*math.sin(t),6),round(z,6))
            if any(abs(a-b)>1e-6 for a,b in zip(actual,target)):
                raise ValueError("Roof vertex inconsistent with parameters")
    return vertices,faces

def export(document,output):
    import bpy
    vertices,faces=validate(document)
    output=Path(output).resolve()
    if output.suffix.lower()!=".blend" or output.exists():
        raise ValueError("Target must be an unused .blend path")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mesh=bpy.data.meshes.new("SacredDomeRoofOpenSurface")
    mesh.from_pydata(vertices,[],faces)
    mesh.update()
    obj=bpy.data.objects.new("SacredDome_P2_Roof",mesh)
    bpy.context.collection.objects.link(obj)
    obj["source_sha256"]=canonical_hash(document)
    obj["state"]="CONCEPT_OPEN_SURFACE_NOT_STRUCTURAL"
    bpy.context.scene.unit_settings.system="METRIC"
    bpy.context.scene.unit_settings.scale_length=1.0
    output.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(output))
    return {"file":str(output),"input_sha256":obj["source_sha256"],"vertices":len(vertices),"quads":len(faces),"build_ready":False}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:])
    document=json.loads(a.input.read_text(encoding="utf-8"))
    print(json.dumps(export(document,a.output),indent=2))

if __name__=="__main__":
    main()
