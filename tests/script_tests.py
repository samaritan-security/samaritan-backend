import unittest

from FacialRecog import *
from RecogScript import process_video_to_encode


class ScriptTest(unittest.TestCase):
    def setUp(self):

        image = open("Ryan_Goluch.jpeg", "rb")
        self.encoded_encoding = face_recognition.load_image_file(image)
        self.encoded_encoding = face_recognition.face_encodings(self.encoded_encoding)
        image.close()

        self.one = get_video_from_file("test_ann.mov")
        self.two = get_video_from_file("test1.jpeg")
        self.employee_dir = "../images/employees"

    # all tests must start with "test"
    def test_headless_encoding_one(self):
        encodings = process_video_to_encode(self.one, self.employee_dir, "../images/temp.jpeg")
        # asserts true that the video was able to find Ann and ONLY ann
        # this looks a bit gross
        same = [[[False]], [[False]], [[False]], [[True]]]
        self.assertEqual(encodings[0], same)

    # this doesn't work yet
    def test_encodings_from_db(self):
        foo = scan_for_known_people_from_db(self.encoded_encoding)
        self.assertTrue(foo)

if __name__ == '__main__':
    unittest.main()
