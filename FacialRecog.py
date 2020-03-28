'''
Samaritan Security Facial Recognition Script Functions:
    Functions for use in RecogScript.py

SDMay20-45
Dept. of Electrical and Computer Engineering
Iowa State University
Author(s): Devin Uner, Ryan Goluch, Ann Gould
'''

from typing import Tuple
import face_recognition
import cv2
import numpy as np
import base64
from datetime import datetime
import imagezmq
from app import add_known_person, add_unknown_person, get_all_people, get_all_cameras
from BlurDetection import detect_blurry_image
from Alerts import check_for_alert
from app import add_unknown_person, add_new_seen


def get_video_from_file(filename: str):
    cap = cv2.VideoCapture(filename)
    feed = []
    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        feed.append(frame)
    return frame


def get_camera_ip_from_file(filename: str):
    video_feed = []
    with open(filename, "r") as file:
        ip = file.readline()
        video_feed.append(cv2.VideoCapture(
            "http://" + str(ip).replace("\n", "") + "/video.mjpg"))
    file.close()
    return video_feed


'''
Function to add a new camera to the text file of camera IPs
'''


def add_camera_ip(ip: str):
    with open("camera_ip.txt", "a") as file:
        num = file.write("\n" + ip)
    file.close()
    if num > 0:
        return True
    return False


"""
gets all encoding/id pairs from people db
"""


def scan_for_known_people_from_db(npy_known: str) -> dict:
    all_people, all_encodings = get_all_people_information()
    all_encodings = np.array(all_encodings)
    npy_array = np.array(npy_known)
    detected_faces = face_recognition.compare_faces(all_encodings, npy_array)

    people_found = dict(zip(all_people, detected_faces))

    return detected_faces


"""
returns list of ids and encodings
"""


def get_all_people_information() -> Tuple[list, list]:
    all_encodings = []
    all_ids = []

    db_data = get_all_people("not_api_call")
    for i in db_data:
        formatted_npy_str = i['npy'].replace(
            r"\n", "")[2:-2]  # get rid on newlines and "[]"
        iterable = formatted_npy_str.split()  # make string values iterable
        # create npy by iterating over strings
        npy = np.fromiter(iterable, float)
        all_encodings.append(npy)
        id = i['_id']
        all_ids.append(id)

    return all_ids, all_encodings


"""
given a video feed, returns a frame
"""


def get_frame(video_feed):
    ret, frame = video_feed.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
    return small_frame


"""
given a frame, returns a list of nparray face encodings, shape = (128,)
"""


def get_face_encodings(frame):
    # Convert the image from BGR color (which OpenCV uses)
    # to RGB color (which face_recognition uses)
    rgb_small_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(
        rgb_small_frame, face_locations)

    return face_encodings


"""
for getting images and encodings of unknown people from an image
"""


def get_images_and_encodings(frame) -> Tuple[list, list]:
    rgb_small_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(
        rgb_small_frame, face_locations)

    face_images = []
    for location in face_locations:
        y_s = location[0]
        x_f = location[1]
        y_f = location[2]
        x_s = location[3]
        crop_frame = frame[y_s:y_f, x_s:x_f]
        face_images.append(crop_frame)

    return face_encodings, face_images


"""
given a list of encodings from frame and a list of all
system encodings, returns a list of lists of boolean values
"""


def compare_encodings(frame_encodings, all_encodings):
    if len(frame_encodings) == 0:
        return None

    encodings = []
    for face in all_encodings:
        encodings.append(face_recognition.compare_faces(face, frame_encodings))

    return encodings


"""
returns a list of all cameras in db
"""


def all_cameras():
    cameras = get_all_cameras("not_api_call")
    return cameras


"""
given a camera from db, returns a frame
from that camera
"""


def get_frame_from_camera():
    # Camera Streaming code:
    image_hub = imagezmq.ImageHub()

    # initialize the dictionary which will contain  information regarding
    # when a device was last active, then store the last time the check
    # was made was now
    last_active = {}
    last_active_check = datetime.now()

    camera_name, img = image_hub.recv_image()
    image_hub.send_reply(b'OK')

    last_active[camera_name] = datetime.now()

    # print("Frame received")
    # print(img)

    # if current time *minus* last time when the active device check was made is
    # greater than the threshold set then do a check
    if (datetime.now() - last_active_check).seconds > 10:
        # loop over all previously active devices
        for (rpi_name, ts) in list(last_active.items()):
            # remove the RPi from the last active and frame dictionaries if the
            # device hasn't been active recently
            if (datetime.now() - ts).seconds > 10:
                print("[INFO] lost connection to {}".format(rpi_name))
                last_active.pop(rpi_name)

        # set the last active check time as current time
        last_active_check = datetime.now()

    # feed = cv2.VideoCapture("http://" + str(camera['ip']) + "/video.mjpg")
    # ret, img = feed.read()
    frame = cv2.resize(img, (0, 0), fx=0.75, fy=0.75)
    return camera_name, frame


"""
given a frame and a list of encodings,
returns a list of comparisons between faces
in the frame and the list of encodings
"""


def compare_frame_and_encodings(frame, encodings):
    frame_encodings = get_face_encodings(frame)
    comparison_results = compare_encodings(frame_encodings, encodings)
    return comparison_results


"""
given a list of comparisons, list of ids, camera, frame,
processes comparisons
"""


def process_comparisons(comparisons, ids, camera, frame):
    if comparisons is not None:
        print(comparisons)
        face_recognized = [False] * len(comparisons[0])
        for comparison in comparisons:
            if True in comparison[:len(comparison)]:
                face_recognized[comparison.index(True)] = True
                id = ids[comparisons.index(comparison)]
                add_new_seen(id, str(camera['_id']))
                check_for_alert(id, str(camera['_id']))

        unknown_encodings, unknown_images = get_images_and_encodings(frame)
        i = 0
        print(face_recognized)
        for recognized in face_recognized:
            if recognized is False:
                encoded_image = base64.b64encode(
                    np.array(unknown_images[i])).decode('utf-8')
                npy_encoding = str(unknown_encodings[i])
                data = {"img": encoded_image, "npy": npy_encoding}
                add_unknown_person(data)
            i = i + 1
