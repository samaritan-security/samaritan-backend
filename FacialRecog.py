'''
Samaritan Security Facial Recognition Script Functions:
    Functions for use in RecogScript.py

SDMay20-45
Dept. of Electrical and Computer Engineering
Iowa State University
Author(s): Devin Uner, Ryan Goluch, Ann Gould
'''

import re
from typing import Tuple

import face_recognition
import cv2
import os
import numpy as np

from app import get_known_people, get_all_people
from app import add_known_person, add_unknown_person, get_known_people


def get_video_from_file(filename: str):
    return cv2.VideoCapture(filename)


def get_camera_ip_from_file(filename: str):
    file = open(filename, "r")
    ip = file.readline()
    video_feed = cv2.VideoCapture("http://" + str(ip).replace("\n", "") + "/video.mjpg")
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


'''
Helper function for image pre-processing
'''
def image_files_in_folder(folder):
    # following code snippet from face_recognition
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]


'''
Updates the known persons in the frame from the facial recog script
'''
def add_to_known_stream(name: str, encoded_image: str, encoded_encoding: str):
    data = {"name": name, "img": encoded_image, "npy": encoded_encoding}
    return add_known_person(data)


'''
Updates the unknown persons in the frame from facial recog script
'''
def add_to_unknown_stream(encoded_image: str):
    data = {"img": encoded_image}
    return add_unknown_person(data)


def get_all_people_information() -> Tuple[list, list]:
    all_encodings = []
    all_ids = []

    db_data = get_all_people("not_api_call")
    for i in db_data:
        npy = np.fromstring(i['npy'], count=128)
        all_encodings.append(npy)
        id = i['_id']
        all_ids.append(id)

    return all_ids, all_encodings
