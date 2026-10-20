"""Deterministic conceptual masses in meters; no construction assemblies."""
import math
from lab.style_presets import get_style


def generate_typology(style_id, radius_m=5.0, height_m=3.0, segments=24, roof_rise_m=2.0, courtyard_ratio=0.4):
    style = get_style(style_id)
    for name, value, low, high in (("radius", radius_m, 1, 100), ("height", height_m, 0.1, 100),
                                    ("roof rise", roof_rise_m, 0.1, 100), ("courtyard ratio", courtyard_ratio, 0.1, 0.8)):
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or not low <= value <= high:
            raise ValueError(f"invalid {name}")
    if isinstance(segments, bool) or not isinstance(segments, int) or not 6 <= segments <= 128:
        raise ValueError("segments must be integer 6..128")
    r, h, rise, n = radius_m, height_m, roof_rise_m, segments
    vertices, faces = [], []
    factor = n * math.sin(2*math.pi/n) / 2

    def ring(radius, z):
        start = len(vertices)
        vertices.extend((radius*math.cos(2*math.pi*i/n), radius*math.sin(2*math.pi*i/n), z) for i in range(n))
        return list(range(start, start+n))

    def bridge(a, b):
        faces.extend((a[i], a[(i+1)%n], b[(i+1)%n], b[i]) for i in range(n))

    if style.geometry == 'courtyard':
        # Continuous annular mass with a genuine central void, open to sky.
        a, b, c, d = ring(r, 0), ring(r, h), ring(r*courtyard_ratio, h), ring(r*courtyard_ratio, 0)
        for first, second in ((a,b), (b,c), (c,d), (d,a)):
            bridge(first, second)
        area = factor*r*r*(1-courtyard_ratio**2)
        volume = area*h
        kind = 'annular_courtyard'
    elif style.geometry == 'rectilinear':
        vertices = [(-r,-r,0),(r,-r,0),(r,r,0),(-r,r,0),
                    (-r,-r,h),(r,-r,h),(r,r,h),(-r,r,h), (0,-r,h+rise),(0,r,h+rise)]
        faces = [(3,2,1,0),(0,1,5,8,4),(1,2,6,5),(2,3,7,9,6),(3,0,4,7),
                 (4,8,9,7),(8,5,6,9)]
        area = 4*r*r
        volume = area*(h+rise/2)
        kind = 'gable_villa'
    else:
        base = ring(r, 0)
        faces.append(tuple(reversed(base)))
        previous = ring(r, h)
        bridge(base, previous)
        volume = factor*r*r*h
        # Polygonal ellipsoid cap sampled at deterministic latitude rings.
        last_r, last_z = r, h
        for step in range(1, 6):
            theta = math.pi/2*step/6
            next_r, next_z = r*math.cos(theta), h+rise*math.sin(theta)
            current = ring(next_r, next_z)
            bridge(previous, current)
            volume += factor*(next_z-last_z)*(last_r**2+last_r*next_r+next_r**2)/3
            previous, last_r, last_z = current, next_r, next_z
        apex = len(vertices)
        vertices.append((0,0,h+rise))
        faces.extend((previous[i], previous[(i+1)%n], apex) for i in range(n))
        volume += factor*(h+rise-last_z)*last_r**2/3
        area = factor*r*r
        kind = 'faceted_dome' if style.geometry == 'geodesic_shell' else 'radial_dome'
        # Faceted suite uses triangular panels; this is not an icosphere geodesic.
        if kind == 'faceted_dome':
            faces = [tri for face in faces for tri in ([face] if len(face)!=4 else
                     [(face[0],face[1],face[2]),(face[0],face[2],face[3])])]
    return dict(vertices=vertices, faces=faces, kind=kind, footprint_area_m2=area,
                expected_volume_m3=volume,
                parameters=dict(style_id=style_id, radius_m=r, height_m=h, segments=n,
                                roof_rise_m=rise, courtyard_ratio=courtyard_ratio))
