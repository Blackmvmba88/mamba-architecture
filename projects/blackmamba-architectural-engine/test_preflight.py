"""Regression checks for failure paths that would otherwise break scene generation."""
import copy,json,unittest
from pathlib import Path
from preflight import validate
class PreflightTests(unittest.TestCase):
 def setUp(self):self.p=json.loads(Path(__file__).with_name('parameters.json').read_text())
 def test_default(self):self.assertEqual(validate(self.p),[])
 def test_seed_bool(self):self.p['seed']=True;self.assertTrue(any('seed' in e for e in validate(self.p)))
 def test_dormer_outside_facade(self):self.p['dormer_axes']=[-20,20];self.assertTrue(any('dormer_axes' in e for e in validate(self.p)))
 def test_nan(self):self.p['depth']=float('nan');self.assertTrue(any('depth' in e for e in validate(self.p)))
 def test_coincident_camera(self):self.p['camera_target']=self.p['camera_location'][:];self.assertTrue(any('camera' in e for e in validate(self.p)))
 def test_fractional_samples(self):self.p['render_samples']=12.5;self.assertTrue(any('render_samples' in e for e in validate(self.p)))
if __name__=='__main__':unittest.main()
