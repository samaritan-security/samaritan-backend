import unittest
import json
import numpy as np
from FacialRecog import *


class ScriptTest(unittest.TestCase):

    """
    tests that all get_all_people_information returns values
    """

    def test_get_all_people_information(self):
        all_ids, all_encodings = get_all_people_information()
        self.assertEqual(len(all_ids) > 0 and len(all_encodings) > 0, True)

    """
    """

    def test_get_frame(self):
        # TODO figure out how to implement test
        self.assertEqual(True, True)

    """
    tests that for an image with 1 person, 1 encoding is returned
    """

    def test_get_face_encodings_1(self):
        image = cv2.imread("tests/Ryan_Goluch.jpeg")
        frame = cv2.resize(image, (0, 0), fx=0.75, fy=0.75)
        frame_encodings = get_face_encodings(frame)
        self.assertEqual(len(frame_encodings), 1)

    """
    tests that for an image with 2 people, 2 encodings are returned
    """

    def test_get_face_encodings_2(self):
        image = cv2.imread("tests/test1.jpeg")
        frame = cv2.resize(image, (0, 0), fx=0.75, fy=0.75)
        frame_encodings = get_face_encodings(frame)
        self.assertEqual(len(frame_encodings), 2)

    """
    tests that when ryan is in db and we compare encodings from db
    with an encoding of ryan, a true is found
    """

    def test_compare_face_encodings_1(self):
        image = cv2.imread("tests/Ryan_Goluch.jpeg")
        frame = cv2.resize(image, (0, 0), fx=0.75, fy=0.75)
        frame_encodings = get_face_encodings(frame)

        all_ids, all_encodings = get_all_people_information()
        encoding_comparisons = compare_encodings(
            frame_encodings, all_encodings)

        ryan = encoding_comparisons[0]
        self.assertEqual(True in ryan[:len(ryan)], True)

    """
    tests that when ryan is in db and we compare encodings from db 
    with encodings of ryan and ann, a true is found for ryan
    """

    def test_compare_face_encodings_2(self):
        image = cv2.imread("tests/test1.jpeg")
        frame = cv2.resize(image, (0, 0), fx=0.75, fy=0.75)
        frame_encodings = get_face_encodings(frame)

        all_ids, all_encodings = get_all_people_information()
        encoding_comparisons = compare_encodings(
            frame_encodings, all_encodings)

        ryan = encoding_comparisons[0]
        self.assertEqual(True in ryan[:len(ryan)], True)

    """
    tests that it works for image with 1 person
    """

    def test_get_images_and_encodings_1(self):
        image = cv2.imread("tests/Ryan_Goluch.jpeg")
        frame = cv2.resize(image, (0, 0), fx=0.75, fy=0.75)
        frame_encodings, frame_images = get_images_and_encodings(frame)

        i = 0
        for frame in frame_images:
            img = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
            cv2.imwrite("tests/im_{}.jpeg".format(i), img)
            i = i + 1

        self.assertEqual(i == 1, True)

    """
    tests that it works for image with 2 people
    """

    def test_get_images_and_encodings_2(self):
        image = cv2.imread("tests/test1.jpeg")
        frame = cv2.resize(image, (0, 0), fx=0.75, fy=0.75)
        frame_encodings, frame_images = get_images_and_encodings(frame)

        i = 0
        for frame in frame_images:
            img = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
            cv2.imwrite("tests/im_{}.jpeg".format(i), img)
            i = i + 1

        self.assertEqual(i == 2, True)

    """
    tests that function returns list of cameras with ip & nickname
    """

    def test_all_cameras(self):
        cameras = all_cameras()
        self.assertEqual(len(cameras) > 0 and len(
            cameras[0]['ip']) > 0 and len(cameras[0]['nickname']) > 0, True)

    """
    tests that a frame is returned
    --only passes if camera 192.168.1.107 is running--
    """

    def test_get_frame_from_camera(self):
        camera = {
            "_id": "5e795368354d37c78043626e",
            "ip": "192.168.1.107",
            "nickname": "home-camera"
        }

        frame = get_frame_from_camera(camera)
        self.assertEqual(len(frame) > 0, True)

    """
    tests that when ryan's encoding is in the db and we pass an image 
    of him to compare_frame_and_encodings, it returns true
    """

    def test_compare_frame_and_encodings(self):
        image = cv2.imread("tests/Ryan_Goluch.jpeg")
        frame = cv2.resize(image, (0, 0), fx=0.75, fy=0.75)
        all_ids, all_encodings = get_all_people_information()
        comparisons = compare_frame_and_encodings(frame, all_encodings)
        comparison = comparisons[0]
        self.assertEqual(True in comparison[:len(comparison)], True)


if __name__ == '__main__':
    unittest.main()
