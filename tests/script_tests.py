import unittest

from FacialRecog import *
from RecogScript import process_video_to_encode


class ScriptTest(unittest.TestCase):
    def setUp(self):
        self.one = get_video_from_file("test_ann.mov")
        self.two = get_video_from_file("test1.jpeg")
        self.unknown = get_video_from_file("unknown.jpeg")
        self.employee_dir = "../images/employees"
        pass

    # all tests must start with "test"
    def test_headless_encoding_one(self):
        encodings = process_video_to_encode(self.one, self.employee_dir, "../images/temp.jpeg")
        # asserts true that the video was able to find Ann and ONLY ann
        same = [[[False]], [[False]], [[False]], [[True]]]
        self.assertEqual(same, encodings[0])

    def test_headless_encoding_two(self):
        encodings = process_video_to_encode(self.two, self.employee_dir, "../images/temp.jpeg")
        # asserts true that the video was able to find Ann and Ryan (via cool diy image)
        same = [[False, False], [False, False], [False, True], [True, False]]
        self.assertEqual(same, encodings[0])

    def test_encodings_unknown(self):
        encodings = process_video_to_encode(self.unknown, self.employee_dir , "../images/temp.jpeg")
        self.assertEquals(encodings[0], None)

    # will add tests for check_encodings... Those are our "integration tests" though
    # want to greenlight everything else before thought



if __name__ == '__main__':
    unittest.main()
