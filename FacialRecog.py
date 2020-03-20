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

from app import add_known_person, add_unknown_person, get_all_people


def get_video_from_file(filename: str):
    cap = cv2.VideoCapture(filename)
    feed = []
    while True:
        ret, frame = cap.read()

        if frame is None:
            break
        feed.append(frame)
    return feed


def get_camera_ip_from_file(filename: str):
    ip = []
    video_feed = []
    with open(filename, "r") as file :
        ip += file.readline()
    for i in ip:
        video_feed += cv2.VideoCapture("http://" + str(i).replace("\n", "") + "/video.mjpg")
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
        formatted_npy_str = i['npy'].replace(r"\n", "")[2:-2] #get rid on newlines and "[]"
        iterable = formatted_npy_str.split() #make string values iterable
        npy = np.fromiter(iterable, float) #create npy by iterating over strings
        all_encodings.append(npy)
        id = i['_id']
        all_ids.append(id)

    return all_ids, all_encodings


"""
given a video feed, returns a frame
"""
def get_frame(video_feed):
    frame = []
    for f in video_feed:
        # TODO need to make sure this is ok for live streams, works for videos
        for x in f:
            small_frame = cv2.resize(x, (0, 0), fx=0.75, fy=0.75)
            frame.append(small_frame)
    return frame


"""
given a frame, returns a list of nparray face encodings, shape = (128,)
"""
def get_face_encodings(frame):
    # Convert the image from BGR color (which OpenCV uses)
    # to RGB color (which face_recognition uses)
    rgb_small_frame = []
    for f in frame:
        rgb_small_frame += f[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_encodings = []

    for r in rgb_small_frame:
        face_locations = face_recognition.face_locations(r)
        face_encodings += face_recognition.face_encodings(r, face_locations)

    return face_encodings


"""
for getting images and encodings of unknown people from an image
"""
def get_images_and_encodings(frame) -> Tuple[list, list]:
    rgb_small_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

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
system encdoings, returns a list of lists of boolean values
"""
def compare_encodings(frame_encodings, all_encodings):
    if len(frame_encodings) == 0:
        return None

    encodings = []
    for face in all_encodings:
        for entry in frame_encodings:
            encodings.append(face_recognition.compare_faces(face, entry))

    return encodings
