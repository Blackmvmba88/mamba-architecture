import unittest
from copy import deepcopy
from lab.sacred_dome_p2 import build
from lab.blender_sacred_dome import validate,canonical_hash

class SacredDomeContractTests(unittest.TestCase):
    def test_valid(self):
        doc=build()
        vertices,faces=validate(doc)
        self.assertEqual((len(vertices),len(faces)),(84,72))
    def test_tampered_vertex(self):
        doc=build()
        doc["roof_mesh"]["vertices_m"][0][0]+=0.2
        with self.assertRaises(ValueError):validate(doc)
    def test_tampered_face(self):
        doc=build()
        doc["roof_mesh"]["quad_faces"][0]=[0,1,2,3]
        with self.assertRaises(ValueError):validate(doc)
    def test_hash_is_deterministic(self):
        self.assertEqual(canonical_hash(build()),canonical_hash(deepcopy(build())))

if __name__=="__main__":unittest.main()
