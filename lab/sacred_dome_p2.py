"""P2 Sacred Dome: decorative roof grid and aperture schedule; no structural sizing."""
import argparse
import json
import math
from pathlib import Path

def finite_positive(name, value, low, high):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"{name} must be finite in [{low}, {high}]")
    return float(value)

def build(radius_m=6.0, wall_height_m=3.0, roof_rise_m=2.0,
          segments=12, roof_rings=6, oculus_ratio=0.18, door_width_m=1.2):
    radius_m=finite_positive("radius_m", radius_m, 2, 40)
    wall_height_m=finite_positive("wall_height_m",wall_height_m,2,12)
    roof_rise_m=finite_positive("roof_rise_m",roof_rise_m,0.5,20)
    oculus_ratio=finite_positive("oculus_ratio",oculus_ratio,0.05,0.5)
    door_width_m=finite_positive("door_width_m",door_width_m,0.7,3)
    for name,n,lo,hi in (("segments",segments,8,64),("roof_rings",roof_rings,2,30)):
        if isinstance(n,bool) or not isinstance(n,int) or not lo <= n <= hi:
            raise ValueError(f"{name} must be integer in [{lo}, {hi}]")
    if door_width_m >= 2*radius_m*math.sin(math.pi/segments):
        raise ValueError("door exceeds width of a single conceptual wall bay")
    # Circular paraboloid surface of revolution: z = wall + rise*(1-(r/R)^2).
    # Top ring defines a central open oculus; no roofing inside this ring.
    vertices=[]
    for j in range(roof_rings+1):
        r=radius_m*(1-(1-oculus_ratio)*j/roof_rings)
        z=wall_height_m+roof_rise_m*(1-(r/radius_m)**2)
        for i in range(segments):
            t=2*math.pi*i/segments
            vertices.append([round(r*math.cos(t),6),round(r*math.sin(t),6),round(z,6)])
    faces=[]
    for j in range(roof_rings):
        for i in range(segments):
            k=j*segments+i
            nxt=j*segments+(i+1)%segments
            faces.append([k,nxt,nxt+segments,k+segments])
    # Door remains metadata until an opening is actually cut from wall meshes.
    return {
        "schema_version":"0.3.0","kind":"sacred_dome_p2","units":"m",
        "parameters":{"radius_m":radius_m,"wall_height_m":wall_height_m,
           "roof_rise_m":roof_rise_m,"segments":segments,"roof_rings":roof_rings,
           "oculus_ratio":oculus_ratio,"door_width_m":door_width_m},
        "roof_mesh":{"vertices_m":vertices,"quad_faces":faces},
        "design_intent":{"oculus_radius_m":round(radius_m*oculus_ratio,6),
           "radial_rib_lines":segments,"door":{"bay":0,"width_m":door_width_m,
           "geometry_status":"unmodeled"},
           "materials":["timber (suggested)","glazing (suggested)"]},
        "validation":{"roof_boundary":"open_around_oculus_and_eaves",
          "structural":"not_assessed","connections":"not_assessed",
          "acoustics":"not_simulated","build_ready":False},
        "limitations":["Quad surface is a schematic paraboloid, not structural ribs.",
           "Door is scheduled but not cut from a wall.",
           "No thickness, wall opening, glazing, fasteners, loads, egress or code check."]
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--radius",type=float,default=6)
    parser.add_argument("--wall-height",type=float,default=3)
    parser.add_argument("--roof-rise",type=float,default=2)
    parser.add_argument("--segments",type=int,default=12)
    parser.add_argument("--roof-rings",type=int,default=6)
    parser.add_argument("--oculus-ratio",type=float,default=0.18)
    parser.add_argument("--door-width",type=float,default=1.2)
    parser.add_argument("--output",type=Path)
    a=parser.parse_args()
    data=json.dumps(build(a.radius,a.wall_height,a.roof_rise,a.segments,a.roof_rings,a.oculus_ratio,a.door_width),indent=2)+"\n"
    if a.output:
        if a.output.exists():
            raise FileExistsError(f"refusing overwrite: {a.output}")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(data,encoding="utf-8")
    else:
        print(data,end="")

if __name__=="__main__":
    main()
