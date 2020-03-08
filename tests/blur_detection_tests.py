import unittest
import cv2

from BlurDetection import *

class BlurDetectionTests(unittest.TestCase):
    def test_not_blurry(self):

        image = cv2.imread("tests/Ryan_Goluch.jpeg")
        print(variance_of_laplacian(image))

        self.assertEqual(detect_blurry_image(image, 150), False)

    def test_blurry(self):
        image = cv2.imread("tests/unknown.jpeg")
        print(variance_of_laplacian(image))

        self.assertEqual(detect_blurry_image(image, 150), True)

   

