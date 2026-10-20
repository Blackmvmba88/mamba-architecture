# Radial concept → Blender v0.1

This bridge converts planar conceptual layout edges to a native editable Blender mesh. It **does not** generate actual domes, beams, supports, glass panels or load-bearing construction. No rendering or engineering validation is claimed.

## Usage
From repository root:

```bash
python3 -m lab.styled_habitat --style sacred_dome --radius 6 --segments 12 --output out/sacred_dome.json
blender --background --python lab/blender_radial.py -- --input out/sacred_dome.json --output out/sacred_dome.blend --report out/sacred_dome_report.json
python3 -m unittest discover -s lab/tests -v
```

The adapter initializes a **new empty Blender process scene** using `read_factory_settings`; do not run inside an active personal Blender GUI session. It rejects existing target `.blend` files, avoiding overwrite. The source JSON has meter units, Z up. Edges are radial layout strokes, not verified structural members.

The report compares generated vertices against source coordinates in the same process. It is **not** independent reimport verification. Next gate: separate Blender invocation reopening the file, checking coordinates/tolerances, and exporting an interoperability format.
