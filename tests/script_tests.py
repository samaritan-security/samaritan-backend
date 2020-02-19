import unittest
import os

from FacialRecog import *
from RecogScript import process_video_to_encode


class ScriptTest(unittest.TestCase):
    def setUp(self):
        pass

    # all tests must start with "test"
    def test_headless_encoding(self):
        foo = get_video_from_file("test_ann.mov")
        # employee_dir = "images/employees"
        # encodings = process_video_to_encode(foo, employee_dir, "../images/temp.jpeg")
        # asserts true that the video was able to find Ann :)
        # self.assertTrue(encodings[1])
        self.assertEquals(os.getcwd(), "foo")


if __name__ == '__main__':
    unittest.main()
