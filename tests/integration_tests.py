import unittest
import base64
from app import app


class APITest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_status_code(self):
        data = {"name": "ann123", "img": self.encoded_image}
        result = self.app.post('/unknown')
        self.assertEqual(result.status_code, 200)




if __name__ == '__main__':
    unittest.main()
