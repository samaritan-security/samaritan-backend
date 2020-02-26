import unittest
import json
import base64
import face_recognition
import datetime

from app import app


image = open("tests/temp1.jpeg", "rb")
image_b64 = base64.b64encode(image.read())
image_b64 = image_b64.decode('utf-8')
image_npy = face_recognition.load_image_file(image)
image_npy = face_recognition.face_encodings(image_npy)
image.close()

class APITest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

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
        data = {"img": image_b64, "npy": image_npy, "name": "Foo Bar"}
        result = self.app.post("/people/known", data=json.dumps(data), content_type="application/json")
        self.assertEqual(result.status_code, 200)

    def test_add_unknown_person(self):
        data = {"img": image_b64, "npy": image_npy, "name": "Foo Bar"}
        result = self.app.post("/people/unknown", data=json.dumps(data), content_type="application/json")
        self.assertEqual(result.status_code, 200)
    
    def test_get_seen_time_intervale(self):
        route = "/seen/" + str(datetime.datetime.now()) + "/" + str(datetime.datetime.now())
        result = self.app.get(route)
        self.assertEqual(result.status_code, 200)

    def test_add_new_seen(self):
        route = "/seen/5e545bcbd541d79f9ef5b0c7"
        result = self.app.put(route)
        self.assertEqual(result.status_code, 200)

    def test_get_all_seen(self):
        result = self.app.get("/seen")
        self.assertEqual(result.status_code, 200)

    def test_add_authorized(self):
        data = {"ref_id" : "5e545bcbd541d79f9ef5b0c7"}
        result = self.app.post("/authorized", data=json.dumps(data), content_type="application/json")
        self.assertEqual(result.status_code, 200)

    def test_get_all_authorized(self):
        result = self.app.get("/authorized")
        self.assertEqual(result.status_code, 200)

    def test_remove_from_authorized(self):
        route = "/authorized/5e545bcbd541d79f9ef5b0c7"
        result = self.app.delete(route)
        self.assertEqual(result.status_code, 200)

    def test_add_unauthorized(self):
        data = {"ref_id" : "5e545bcbd541d79f9ef5b0c7"}
        result = self.app.post("/unauthorized", data=json.dumps(data), content_type="application/json")
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
        route = "/alerts/" + str(datetime.datetime.now()) + "/" + str(datetime.datetime.now())
        result = self.app.get(route)
        self.assertEqual(result.status_code, 200)

    def test_add_new_alert(self):
        route = "/alerts/5e545bcbd541d79f9ef5b0c7"
        result = self.app.put(route)
        self.assertEqual(result.status_code, 200)

    def test_get_all_alerts(self):
        result = self.app.get("/alerts")
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()
