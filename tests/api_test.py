import unittest
import json
from app import app


class APITest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # all tests must start with "test"
    def test_index_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_create_user(self):
        data = {"name": "ann123", "image": "foo"}
        result = self.app.post("/user", data=json.dumps(data), content_type="application/json")
        self.assertEqual(result.status_code, 200)



if __name__ == '__main__':
    unittest.main()
