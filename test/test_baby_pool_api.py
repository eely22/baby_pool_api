import unittest
import sys
sys.path.append("..")
import baby_pool_api
import json

class APITestCase(unittest.TestCase):
    """
    Test cases for the API and helper functions
    """

    def setUp(self):
        baby_pool_api.app.config['TABLE_NAME'] = 'baby_pool_test'
        self.app = baby_pool_api.app.test_client()

    def test_get(self):
        rv = json.loads(self.app.get("/baby_pool").data)
        self.assertEqual(len(rv), 0)

        data = {"email": "test@test.com", "weight": "7lb 7oz", "date": "5-22-2017", "sex": "M", "comment": "comment"}
        rv = self.app.post("/baby_pool", data=data)
        self.assertEqual(rv.status_code, 200)

        data = {"email": "test2@test.com", "weight": "9lb 7oz", "date": "6-22-2017", "sex": "F", "comment": "comment22"}
        rv = self.app.post("/baby_pool", data=data)
        self.assertEqual(rv.status_code, 200)

        rv = json.loads(self.app.get("/baby_pool").data)
        self.assertEqual(len(rv), 2)

# Enable this script to be executed.
if __name__ == '__main__':
    unittest.main()