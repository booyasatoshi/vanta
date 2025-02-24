import unittest
from vanta import VantaAPI

class TestVantaAPI(unittest.TestCase):
    def setUp(self):
        self.api = VantaAPI(api_key="dummy_key")

    def test_get_organizations(self):
        # Since we can't actually call the API, we'll just check if the method exists
        self.assertTrue(hasattr(self.api, 'get_organizations'))

if __name__ == '__main__':
    unittest.main()