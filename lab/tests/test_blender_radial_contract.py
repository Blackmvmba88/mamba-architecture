import unittest
from copy import deepcopy
from lab.styled_habitat import generate_style
from lab.blender_radial import validate, prism_geometry

class BlenderRadialContractTests(unittest.TestCase):
    def test_valid_contract(self):
        doc=generate_style("sacred_dome",5,12)
        self.assertEqual(len(validate(doc)),12)

    def test_closed_prism(self):
        points = validate(generate_style("sacred_dome", 5, 12))
        vertices, faces = prism_geometry(points, 3)
        self.assertEqual(len(vertices), 24)
        self.assertEqual(len(faces), 14)
        from collections import Counter
        edges = Counter(tuple(sorted((face[i], face[(i+1)%len(face)])))
                        for face in faces for i in range(len(face)))
        self.assertTrue(all(count == 2 for count in edges.values()))
        self.assertEqual(max(v[2] for v in vertices), 3)

    def test_invalid_height(self):
        points = validate(generate_style("sacred_dome"))
        for height in (0, -1, 101, True, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                prism_geometry(points, height)

    def test_wrong_units(self):
        doc=generate_style("sacred_dome")
        doc["units"]="cm"
        with self.assertRaises(ValueError):validate(doc)

    def test_broken_edges(self):
        doc=generate_style("biophilic_oasis")
        doc["geometry"]["ring_edges"][0]=[0,2]
        with self.assertRaises(ValueError):validate(doc)

    def test_nonfinite_vertex(self):
        doc=generate_style("stone_timber_rotunda")
        doc["geometry"]["ring_points_m"][0][0]=float("nan")
        with self.assertRaises(ValueError):validate(doc)

if __name__=="__main__":
    unittest.main()
