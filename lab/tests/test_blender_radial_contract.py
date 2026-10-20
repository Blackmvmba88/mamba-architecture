import unittest
from copy import deepcopy
from lab.styled_habitat import generate_style
from lab.blender_radial import validate

class BlenderRadialContractTests(unittest.TestCase):
    def test_valid_contract(self):
        doc=generate_style("sacred_dome",5,12)
        self.assertEqual(len(validate(doc)),12)

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
