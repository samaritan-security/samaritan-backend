import unittest

from FacialRecog import *
from RecogScript import process_video_to_encode


class ScriptTest(unittest.TestCase):
    def setUp(self):
        pass

    # all tests must start with "test"
    def test_headless_encoding(self):
        foo = get_video_from_file("test_ann.mov")
        # employee_dir = "/home/runner/work/samaritan-backend/samaritan-backend/images/employees"
        employee_dir = "../images/employees"
        encodings = process_video_to_encode(foo, employee_dir, "temp.jpeg")
        # asserts true that the video was able to find Ann :)
        self.assertTrue(encodings[1])


if __name__ == '__main__':
    unittest.main()
