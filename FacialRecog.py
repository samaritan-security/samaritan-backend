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
import json
import base64

from app import get_known_people, get_all_people

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
