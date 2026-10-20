import math
import unittest
from collections import Counter
from lab.style_presets import STYLES
from lab.typology_geometry import generate_typology


def signed_volume(vertices, faces):
    total = 0
    for face in faces:
        a = vertices[face[0]]
        for i in range(1, len(face)-1):
            b, c = vertices[face[i]], vertices[face[i+1]]
            total += (a[0]*(b[1]*c[2]-b[2]*c[1]) + a[1]*(b[2]*c[0]-b[0]*c[2]) + a[2]*(b[0]*c[1]-b[1]*c[0]))/6
    return total


class TypologyTests(unittest.TestCase):
    def test_closed_oriented_volume(self):
        for style in STYLES:
            for n in (6, 24, 128):
                with self.subTest(style=style, segments=n):
                    model = generate_typology(style, 6, 3, n)
                    vertices, faces = model['vertices'], model['faces']
                    directed = Counter((face[i], face[(i+1)%len(face)]) for face in faces for i in range(len(face)))
                    self.assertTrue(all(count == 1 and directed[(b,a)] == 1 for (a,b), count in directed.items()))
                    self.assertAlmostEqual(signed_volume(vertices, faces), model['expected_volume_m3'], places=6)
                    self.assertEqual(model, generate_typology(style, 6, 3, n))

    def test_courtyard_void(self):
        model = generate_typology('biophilic_oasis', 6, 3, 24, courtyard_ratio=0.5)
        self.assertTrue(all(math.hypot(x,y) >= 3-1e-9 for x,y,z in model['vertices']))
        self.assertAlmostEqual(model['footprint_area_m2'], 24*math.sin(2*math.pi/24)/2*36*0.75)

    def test_invalid_inputs(self):
        for key in ('radius_m', 'height_m', 'roof_rise_m', 'courtyard_ratio', 'segments'):
            for bad in (True, float('nan'), float('inf'), -1, 0):
                with self.subTest(key=key, bad=bad), self.assertRaises(ValueError):
                    generate_typology('sacred_dome', **{key: bad})
