'''
Samaritan Security Facial Recognition Script Functions:
    Functions for use in facial_recog.py

SDMay20-45
Dept. of Electrical and Computer Engineering
Iowa State University
Author(s): Devin Uner, Ryan Goluch, Ann Gould
'''

import pickle
import re
import face_recognition
import cv2
from random import seed
import random
import time
import os
import socket
import sys
import numpy as np
import struct
import json
import datetime

from facial_recog import small_frame


def get_camera_ip_from_file(filename: str):
    # Use a list of camera ips for ease of testing
    file = open(filename, "r")
    ip = file.readline()
    # video_feed = cv2.VideoCapture(0)
    video_feed = cv2.VideoCapture("http://" + str(ip) + "/video.mjpg")
    file.close()  # RYANN!! close your files!!
    return video_feed

def generate_json(name: str) -> json:
    data = {"name": name, "date": str(datetime.datetime.now())}
    print(data)
    return json.dumps(data)

def add_unknown_image():
    seed(time.time())
    image_counter = random.randrange(int(time.time()))
    directory = os.fsencode("images/unknown")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.find(str(image_counter)):
            image_counter = random.randrange(int(time.time()))
    cv2.imwrite('images/unknown/%d.jpeg' % image_counter, small_frame)


def scan_for_known_people(known_people_folder):
    names = []
    face_encodings = []

    for file in image_files_in_folder(known_people_folder):
        filename = os.path.splitext(os.path.basename(file))[0]
        print("DEBUG: Attempted to load image file from", file)
        image = face_recognition.load_image_file(file)

        if os.path.isfile(os.path.join(known_people_folder, "PreEncoded", filename) + ".npy"):
            #read from file, for performance reasons. useful for large batches of files
            encodedfile = np.load((os.path.join(known_people_folder, "PreEncoded", filename) + ".npy"))

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

                #write to file, for performance reasons, so as to not calculate all the faces each time
                encodedfile = np.save((os.path.join(known_people_folder, filename) + ".npy"), single_encoding[0])
                print("DEBUG: saved to document", filename)
                print("DEBUG: saved to document", encodedfile)

    return names, face_encodings


def image_files_in_folder(folder):
    #following code snippet from face_recognition
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]