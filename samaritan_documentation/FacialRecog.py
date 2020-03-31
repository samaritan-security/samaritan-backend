'''
Samaritan Security Facial Recognition Script Functions:
    Functions for use in RecogScript.py

SDMay20-45
Dept. of Electrical and Computer Engineering
Iowa State University
Author(s): Devin Uner, Ryan Goluch, Ann Gould, Kate Brune
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
    """ Function that allows you to read in a video feed from a file. Used for testing purposes.

    Parameters
    ----------
    filename: str
        Name of the video file that you want to read in to test with
    Returns
    -------
    type: dict
        The "camera feed" that is read in from the video file
    """


def get_camera_ip_from_file(filename: str):
    """ Function that allows you to get all open video feeds from the camera IPs that are listed in the given filename

    Parameters
    ----------
    filename: str
        Name of the file that contains the list of camera IPs on the local network
    Returns
    -------
    type: dict
        A dictionary of camera feed objects that allow you to capture the feed from each of
        the connected cameras
    """


def add_camera_ip(ip: str):
    """ Function to add a new camera to the text file of camera IPs

    Parameters
    ----------
    ip: str
        IP address of the camera that you are wanting to add to the camera.txt file
    Returns
    -------
    type: bool
        True/False based on whether or not the IP was written to the file
    """


def scan_for_known_people_from_db(npy_known: str) -> dict:
    """ Gets all encoding/id pairs from people db

    Parameters
    ----------
    npy_known: str
        NumPy array that is passed in as a string to use in DB query
    Returns
    -------
    type: dict
        A dictionary of any faces that were detected in the passed in string
    """


def get_all_people_information() -> Tuple[list, list]:
    """
    Queries the database for IDs and encodings of all the people in the database. All people
    in the database consists of both known and unknown people.

    Returns
    -------
    type: tuple
        Returns a list of IDs and image encodings

    """


def get_frame(video_feed):
    """
    Takes in a camera video feed, reads a single frame from that feed. Then resizes the frame appropriately and returns that frame.

    Parameters
    ----------
    video_feed
        Camera video feed that you want to get a frame from for analysis
    Returns
    -------
    A single, resized frame from the given video feed
    """


"""
given a frame, returns a list of nparray face encodings, shape = (128,)
"""


def get_face_encodings(frame):
    """


    Parameters
    ----------
    frame

    Returns
    -------

    """
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
    """


    Parameters
    ----------
    frame

    Returns
    -------

    """
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
    """


    Parameters
    ----------
    frame_encodings
    all_encodings

    Returns
    -------

    """
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
    """


    Returns
    -------

    """
    cameras = get_all_cameras("not_api_call")
    return cameras


"""
given a camera from db, returns a frame
from that camera
"""


def get_frame_from_camera(image_hub, camera):
    """


    Parameters
    ----------
    image_hub
    camera

    Returns
    -------

    """
    camera_name, img = image_hub.recv_image()
    image_hub.send_reply(b'OK')
    while str(camera_name) not in str(camera['ip']):
        camera_name, img = image_hub.recv_image()
        image_hub.send_reply(b'OK')

    frame = cv2.resize(img, (0, 0), fx=0.75, fy=0.75)
    return frame


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