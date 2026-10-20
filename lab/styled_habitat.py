"""Conceptual parametric style generator. Geometry intent only; never build-ready."""
import argparse
from dataclasses import asdict
import json
import math
from pathlib import Path
from lab.style_presets import STYLES, get_style

def generate_style(style_id: str, radius_m: float = 5.0, segments: int | None = None) -> dict:
    style = get_style(style_id)
    if isinstance(radius_m, bool) or not isinstance(radius_m,(int,float)) or not math.isfinite(radius_m) or not (1.0 <= radius_m <= 100):
        raise ValueError("radius_m must be finite, 1..100")
    if segments is None:
        segments = max(8, style.radial_pattern_complexity)
    if isinstance(segments,bool) or not isinstance(segments,int) or not 6 <= segments <= 128:
        raise ValueError("segments must be integer, 6..128")
    # Ring points and radial edges are conceptual spatial axes; not physical beams.
    points = [[round(radius_m * math.cos(2*math.pi*i/segments),6),
               round(radius_m * math.sin(2*math.pi*i/segments),6),0.0] for i in range(segments)]
    edges = [[i,(i+1)%segments] for i in range(segments)]
    radial = [[segments,i] for i in range(segments)]
    return {
        "schema_version":"0.2.0","kind":"conceptual_style",
        "style":asdict(style),"units":"m",
        "geometry":{"origin_m":[0.0,0.0,0.0],"radius_m":radius_m,"ring_points_m":points,
                    "center_point_m":[0.0,0.0,0.0],"ring_edges":edges,"radial_edges":radial},
        "validation":{"topology":"ring_plus_spokes","structure":"not_assessed",
                      "building_regulation":"not_assessed","build_ready":False},
        "assumptions":["Planar schematic; not a dome mesh or structural framing.",
                       "Materials, oculus and water are metadata, not implemented components."]
    }

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--style",required=True,choices=sorted(STYLES))
    parser.add_argument("--radius",type=float,default=5.0)
    parser.add_argument("--segments",type=int)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    data=json.dumps(generate_style(args.style,args.radius,args.segments),indent=2,ensure_ascii=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(data,encoding="utf-8")
    else:
        print(data,end="")

if __name__=="__main__":
    main()
