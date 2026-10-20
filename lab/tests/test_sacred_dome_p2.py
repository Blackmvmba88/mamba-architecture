import json
import math
import unittest
from lab.sacred_dome_p2 import build

class SacredDomeP2Tests(unittest.TestCase):
    def test_topology(self):
        d=build()
        n=d["parameters"]["segments"]
        rings=d["parameters"]["roof_rings"]
        self.assertEqual(len(d["roof_mesh"]["vertices_m"]),n*(rings+1))
        self.assertEqual(len(d["roof_mesh"]["quad_faces"]),n*rings)
        self.assertFalse(d["validation"]["build_ready"])

    def test_oculus_ring(self):
        d=build()
        n=d["parameters"]["segments"]
        ring=d["roof_mesh"]["vertices_m"][-n:]
        radii=[math.hypot(p[0],p[1]) for p in ring]
        for r in radii:self.assertAlmostEqual(r,1.08,places=5)

    def test_determinism(self):
        self.assertEqual(json.dumps(build(),sort_keys=True),json.dumps(build(),sort_keys=True))

    def test_invalid_parameters(self):
        for value in (0,float("nan"),float("inf"),True):
            with self.assertRaises(ValueError):build(radius_m=value)
        for n in (7,65,2.5,True):
            with self.assertRaises(ValueError):build(segments=n)
        with self.assertRaises(ValueError):build(door_width_m=4)

if __name__=="__main__":unittest.main()
