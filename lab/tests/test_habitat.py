import json
import unittest

from lab.habitat import PRESETS, generate


class HabitatTests(unittest.TestCase):
    def test_all_presets(self):
        for preset in PRESETS:
            with self.subTest(preset=preset):
                output = generate(preset)
                self.assertEqual(len(output["modules"]), output["levels"])
                self.assertFalse(output["validation"]["build_ready"])
                for module in output["modules"]:
                    self.assertTrue(all(x > 0 for x in module["size_m"]))

    def test_deterministic(self):
        self.assertEqual(json.dumps(generate("habitat_arctic"), sort_keys=True),
                         json.dumps(generate("habitat_arctic"), sort_keys=True))

    def test_level_override(self):
        self.assertEqual(generate("capsule_living", 2)["levels"], 2)

    def test_invalid(self):
        for value in (0, 13, True, 2.5):
            with self.assertRaises(ValueError):
                generate("bioshell", value)
        with self.assertRaises(ValueError):
            generate("no_such_preset")


if __name__ == "__main__":
    unittest.main()
