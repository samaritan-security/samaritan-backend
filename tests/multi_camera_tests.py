import unittest

from RecogScript import *
from FacialRecog import *

class MultiCameraTests(unittest.TestCase):

    """
    Set up for running tests on multiple camera feeds. Multiple camera feeds
    represented by multiple video recordings being used.
    """
    def setUp(self):
        image = open("tests/Ryan_Goluch.jpeg", "rb")
        self.encoded_image = face_recognition.load_image_file(image)
        self.encoded_image = face_recognition.face_encodings(self.encoded_image)
        image.close()

        video_one = get_video_from_file("/Users/RyanGoluch/Desktop/test_mov.mov")
        video_two = get_video_from_file("/Users/RyanGoluch/Desktop/test_mov.mov")
        self.employee_dir = "../images/employees"
        self.video_feeds = []
        self.video_feeds.append(video_one)
        self.video_feeds.append(video_two)

    """
    Tests the get_frame method in FacialRecog.py to make sure it works with the supplied
    videos from the setup function
    """
    def test_get_frame(self):
        frames = get_frame(self.video_feeds)
        self.assertTrue(len(frames) > 0)
        # self.assertEqual(len(frames[1]), len(self.video_feeds[1]))

    """
    Tests the get_face_encodings method in FacialRecog.py to make sure it works with the
    supplied videos from the setUp function
    """
    def test_get_face_encodings(self):
        frames = get_frame(self.video_feeds)
        encodings = get_face_encodings(frames)
        print("encodings: "+str(len(encodings)))
        self.assertEqual(len(encodings), 1)


if __name__ == '__main__':
    unittest.main()