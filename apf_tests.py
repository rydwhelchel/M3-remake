import unittest
from utilities import api_funcs as apf


class AddFavTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                "KEY_INPUT": "2QoU3awHVdcHS8LrZEKvSM",
                "KEY_EXPECTED": "Wilco",
            },
            {"KEY_INPUT": "4Z8W4fKeB5YxbusRsdQVPb", "KEY_EXPECTED": "Radiohead"},
            {"KEY_INPUT": "0k17h0D3J5VfsdmQ1iZtE9", "KEY_EXPECTED": "Pink Floyd"},
        ]

    def test_add_success(self):
        for test in self.success_test_params:
            actual_result = apf.get_artist_name(test["KEY_INPUT"])
            expected_result = test["KEY_EXPECTED"]

            self.assertEqual(len(actual_result), len(expected_result))
            self.assertEqual(actual_result, expected_result)


if __name__ == "__main__":
    unittest.main()
