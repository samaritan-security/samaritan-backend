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
Function to generate the JSON file for users' data
'''


def generate_json(name: str) -> json:
    data = {"name": name}
    print(data)
    return json.dumps(data)


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


'''
Function to pre-process the known images to help speed up facial recognition
'''


def scan_for_known_people(known_people_folder):
    names = []
    face_encodings = []

    for file in image_files_in_folder(known_people_folder):
        filename = os.path.splitext(os.path.basename(file))[0]
        print("DEBUG: Attempted to load image file from", file)
        image = face_recognition.load_image_file(file)

        if os.path.isfile(os.path.join(known_people_folder, "PreEncoded" + filename) + ".npy"):
            # read from file, for performance reasons. useful for large batches of files
            encodedfile = np.load((os.path.join(known_people_folder, "PreEncoded" + filename) + ".npy"))

            if encodedfile is not None:
                names.append(filename)
                print("DEBUG: appended from document", filename)
                face_encodings.append(encodedfile)
                print("DEBUG: appended from document", encodedfile)
        else:
            single_encoding = face_recognition.face_encodings(image)

            if len(single_encoding) > 1:
                print("WARNING: More than one face found in", file + ".", "Only using the first face.")

            if len(single_encoding) == 0:
                print("WARNING: No faces found in", file + ".", "Ignoring file.")
            else:
                names.append(filename)
                face_encodings.append(single_encoding[0])

                # write to file, for performance reasons, so as to not calculate all the faces each time
                encodedfile = np.save((os.path.join(known_people_folder, "PreEncoded" + filename) + ".npy"),
                                      single_encoding[0])
                print("DEBUG: saved to document", filename)
                print("DEBUG: saved to document", encodedfile)

    return names, face_encodings


"""
Gets data from a specified db and detects if facial encodings are the same
returns a dict of users + respective true/false if person was detected
"""


def scan_for_known_people_from_db(npy_known: str) -> dict:
    all_people, all_encodings = get_names_and_encodings_from_known()

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


"""
Gets names and encodings from KNOWN, puts in lists just like that one function (process video to encode)
"""


def get_names_and_encodings_from_known() -> Tuple[list, list]:
    all_encodings = []
    all_people = []

    db_get_data = get_known_people("not_api_call")
    for i in db_get_data:
        foo = i['npy'].strip('][').split(', ')
        for j in range(len(foo)):
            foo[j] = float(foo[j])
        all_encodings.append(foo)
        all_people.append(i['name'])

    # returns dictionary of people and their encodings
    return all_people, all_encodings
