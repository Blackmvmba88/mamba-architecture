import json
import math
import unittest
from lab.style_presets import STYLES,get_style
from lab.styled_habitat import generate_style

class StyleTests(unittest.TestCase):
    def test_all_styles(self):
        self.assertEqual(len(STYLES),7)
        for name,style in STYLES.items():
            with self.subTest(name=name):
                self.assertEqual(style.id,name)
                for v in (style.biophilia_level,style.glazing_ratio,style.ornament_density):
                    self.assertGreaterEqual(v,0)
                    self.assertLessEqual(v,1)
                doc=generate_style(name)
                n=len(doc["geometry"]["ring_points_m"])
                self.assertEqual(n,len(doc["geometry"]["ring_edges"]))
                self.assertEqual(n,len(doc["geometry"]["radial_edges"]))
                self.assertFalse(doc["validation"]["build_ready"])
                self.assertEqual(doc["units"],"m")

    def test_geometry_radius(self):
        d=generate_style("sacred_dome",4,12)
        for x,y,z in d["geometry"]["ring_points_m"]:
            self.assertAlmostEqual(math.hypot(x,y),4,places=5)
            self.assertEqual(z,0)

    def test_determinism(self):
        self.assertEqual(json.dumps(generate_style("biophilic_oasis"),sort_keys=True),
                         json.dumps(generate_style("biophilic_oasis"),sort_keys=True))

    def test_bad_inputs(self):
        for value in (0,-1,101,float("nan"),float("inf"),True):
            with self.assertRaises(ValueError): generate_style("sacred_dome",value)
        for value in (0,5,129,True,7.5):
            with self.assertRaises(ValueError): generate_style("sacred_dome",5,value)
        with self.assertRaises(ValueError): get_style("unknown")

if __name__=="__main__":
    unittest.main()
