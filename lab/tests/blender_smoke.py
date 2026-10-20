"""Run: blender --background --python lab/tests/blender_smoke.py -- OUTPUT_DIR"""
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import bpy
from lab.blender_radial import build
from lab.style_presets import STYLES
from lab.styled_habitat import generate_style

output = Path(sys.argv[sys.argv.index('--') + 1])
output.mkdir(parents=True, exist_ok=True)
reports = []
for style in STYLES:
    data = generate_style(style, 6)
    target = output / f'{style}.blend'
    report = build(data, target, height_m=3)
    bpy.ops.wm.open_mainfile(filepath=str(target.resolve()))
    obj = bpy.data.objects['Conceptual_Radial_Plan']
    assert json.loads(obj['source_parameters_json']) == json.loads(json.dumps(data))
    assert math.isclose(max(v.co.z for v in obj.data.vertices), 3)
    assert len(obj.data.vertices) == report['vertices']
    assert len(obj.data.polygons) == report['faces']
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    assert all(edge.is_manifold for edge in bm.edges)
    assert math.isclose(abs(bm.calc_volume()), report['volume_m3'], rel_tol=1e-6)
    bm.free()
    report['reopened_verified'] = True
    reports.append(report)
(output / 'report.json').write_text(json.dumps(reports, indent=2) + '\n')
print(f'PASS: {len(reports)} styles saved, reopened and measured')
