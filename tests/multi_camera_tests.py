import unittest

from RecogScript import *
from FacialRecog import *

class MultiCameraTests(unittest.TestCase):

    """
    Set up for running tests on multiple camera feeds. Multiple camera feeds
    represented by multiple video recordings being used.
    """
    def setup(self):
        image = open("tests/Ryan_Goluch.jpeg", "rb")
        self.encoded_image = face_recognition.load_image_file(image)
        self.encoded_image = face_recognition.face_encodings(self.encoded_image)
        image.close()

        self.video_one = get_video_from_file("tests/multi_camera_test_1.mov")
        self.video_two = get_video_from_file("tests/multi_camera_test_2.mov")
        self.employee_dir = "../images/employees"

    def test_get_frame(self):
        self.setup()
        video_feeds = []
        video_feeds.append(self.video_one)
        video_feeds.append(self.video_two)
        frames = get_frame(video_feeds)
        self.assertTrue(len(frames) > 0)

if __name__ == '__main__':
    unittest.main()