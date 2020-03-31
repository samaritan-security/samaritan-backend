import unittest
import json
import numpy as np
import base64
import face_recognition
import datetime

from app import app, add_new_alert, add_new_seen
from FacialRecog import *


class APITest(unittest.TestCase):
    def setUp(self):

        self.app = app.test_client()
        self.app.testing = True

        image = open("tests/Ryan_Goluch.jpeg", "rb")
        self.encoded_image = base64.b64encode(image.read())
        self.encoded_image = self.encoded_image.decode('utf-8')
        frame = cv2.resize(cv2.imread(
            "tests/Ryan_Goluch.jpeg"), (0, 0), fx=0.75, fy=0.75)
        self.encoded_encoding = get_face_encodings(frame)
        self.encoded_encoding = str(self.encoded_encoding[0])
        image.close()
        image = open("tests/test2.jpeg", "rb")
        self.encoded_image_2 = base64.b64encode(image.read())
        self.encoded_image_2 = self.encoded_image_2.decode('utf-8')
        frame = cv2.resize(cv2.imread("tests/test2.jpeg"),
                           (0, 0), fx=0.75, fy=0.75)
        self.encoded_encoding_2 = get_face_encodings(frame)
        self.encoded_encoding_2 = str(self.encoded_encoding_2[0])
        image.close()
        self.name = "Ryan Goluch"

    # all tests must start with "test"

    def test_index_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_get_known_people(self):
        result = self.app.get("/people/known")
        self.assertEqual(result.status_code, 200)

    def test_get_unknown_people(self):
        result = self.app.get("/people/unknown")
        self.assertEqual(result.status_code, 200)

    def test_add_known_person(self):
        data = {"img": self.encoded_image,
                "npy": self.encoded_encoding, "name": self.name}
        result = self.app.post(
            "/people/known", data=json.dumps(data), content_type="application/json")
        self.assertEqual(result.status_code, 200)

    def test_add_unknown_person(self):
        data = {"img": self.encoded_image_2, "npy": self.encoded_encoding_2}
        result = self.app.post(
            "/people/unknown", data=json.dumps(data), content_type="application/json")
        self.assertEqual(result.status_code, 200)

    def test_get_seen_time_intervale(self):
        route = "/seen/" + str(datetime.datetime.now()) + \
            "/" + str(datetime.datetime.now())
        result = self.app.get(route)
        self.assertEqual(result.status_code, 200)

    def test_add_new_seen(self):
        result = add_new_seen("5e545bcbd541d79f9ef5b0c7",
                              "5e795368354d37c78043626e")
        self.assertEqual(result.acknowledged, True)

    def test_get_all_seen(self):
        result = self.app.get("/seen")
        self.assertEqual(result.status_code, 200)

    def test_add_authorized(self):
        data = {"ref_id": "5e545bcbd541d79f9ef5b0c7"}
        result = self.app.post(
            "/authorized", data=json.dumps(data), content_type="application/json")
        self.assertEqual(result.status_code, 200)

    def test_get_all_authorized(self):
        result = self.app.get("/authorized")
        self.assertEqual(result.status_code, 200)

    def test_remove_from_authorized(self):
        route = "/authorized/5e545bcbd541d79f9ef5b0c7"
        result = self.app.delete(route)
        self.assertEqual(result.status_code, 200)

    def test_add_unauthorized(self):
        data = {"ref_id": "5e545bcbd541d79f9ef5b0c7"}
        result = self.app.post(
            "/unauthorized", data=json.dumps(data), content_type="application/json")
        self.assertEqual(result.status_code, 200)

    def test_get_all_unauthorized(self):
        result = self.app.get("/unauthorized")
        self.assertEqual(result.status_code, 200)

    def test_check_for_unauthorized(self):
        route = "/unauthorized/5e545bcbd541d79f9ef5b0c7"
        result = self.app.get(route)
        self.assertEqual(result.status_code, 200)

    def test_remove_from_unauthorized(self):
        route = "/unauthorized/5e545bcbd541d79f9ef5b0c7"
        result = self.app.delete(route)
        self.assertEqual(result.status_code, 200)

    def test_get_alerts_time_intervale(self):
        route = "/alerts/" + str(datetime.datetime.now()) + \
            "/" + str(datetime.datetime.now())
        result = self.app.get(route)
        self.assertEqual(result.status_code, 200)

    def test_add_new_alert(self):
        result = add_new_alert("5e545bcbd541d79f9ef5b0c7",
                               "5e795368354d37c78043626e")
        self.assertEqual(result.acknowledged, True)

    def test_get_all_alerts(self):
        result = self.app.get("/alerts")
        self.assertEqual(result.status_code, 200)

    def test_add_new_camera(self):
        data = {"ip": "192.168.1.107", "nickname": "home-camera"}
        result = self.app.post(
            "/camera", data=json.dumps(data), content_type="application/json")
        self.assertEqual(result.status_code, 200)

    def test_get_camera_by_id(self):
        route = "/camera/5e795368354d37c78043626e"
        result = self.app.get(route)
        self.assertEqual(result.status_code, 200)

    def test_get_all_cameras(self):
        route = "/camera"
        result = self.app.get(route)
        self.assertEquals(result.status_code, 200)

    def test_login(self):
        route = "/users/login"
        result = self.app.get(route)
        self.assertEquals(result.status_code, 200)

    def test_(self):
        route = "/users"
        result = self.app.get(route)
        self.assertEquals(result.status_code, 200)


if __name__ == '__main__':
    unittest.main()
