import unittest
import base64
from app import app


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True





if __name__ == '__main__':
    unittest.main()
