"""
Samaritan Security Facial Recognition Script

SDMay20-45
Dept. of Electrical and Computer Engineering
Iowa State University
Author(s): Devin Uner, Ryan Goluch, Ann Gould
"""
import pickle
import re
import face_recognition
import cv2
from random import seed
import random
import time
import os
import socket
import numpy as np
import struct
import json

'''
gets ips from file 
'''


def get_camera_ip_from_file(filename: str):
    # Use a list of camera ips for ease of testing
    file = open(filename, "r")
    ip = file.readline()
    video_feed = cv2.VideoCapture("http://" + str(ip) + "/video.mjpg")
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


'''
loads facial recog image file, encodes and names known face
'''


def facial_recog_process(faces, temp):
    for face in faces:
        encodings = face_recognition.compare_faces(face, temp)
    # names = ["Ryan Goluch"]
    return encodings


'''
Function to add the file path of an image to database
'''


def add_facial_data():
    # TODO
    return True


'''
Function to add a face to temp_access directory
'''


def add_temp_data(name: str):
    directory = os.fsencode("images/temp_access")
    cv2.imwrite(dir+name, small_frame)

'''
Function to generate the JSON file for users' data
'''


def generate_json(name: str) -> json:
    data = {"name": name}
    print(data)
    return json.dumps(data)


'''
Function to add unknown images to the database of images
'''


def add_unknown_image():
    seed(time.time())
    image_counter = random.randrange(int(time.time()))
    directory = os.fsencode("images/unknown")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.find(str(image_counter)):
            image_counter = random.randrange(int(time.time()))
    cv2.imwrite('images/unknown/%d.jpeg' % image_counter, small_frame)


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

        if os.path.isfile(os.path.join(known_people_folder, "PreEncoded", filename) + ".npy"):
            # read from file, for performance reasons. useful for large batches of files
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

                # write to file, for performance reasons, so as to not calculate all the faces each time
                encodedfile = np.save((os.path.join(known_people_folder, filename) + ".npy"), single_encoding[0])
                print("DEBUG: saved to document", filename)
                print("DEBUG: saved to document", encodedfile)

    return names, face_encodings


'''
Helper function for image pre-processing
'''


def image_files_in_folder(folder):
    # following code snippet from face_recognition
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]


'''
Main script function
'''

video_capture = get_camera_ip_from_file("camera_ip.txt")
known_names, known_encodings = scan_for_known_people("images/employees")
encodings = []

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)

    # Convert the image from BGR color (which OpenCV uses) 
    # to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    cv2.imwrite('images/temp.jpeg', small_frame)
    temp = face_recognition.load_image_file("images/temp.jpeg")
    temp_encode = face_recognition.face_encodings(temp)
    if len(temp_encode) == 0:
        continue

    for face in known_encodings:
        r = face_recognition.compare_faces(temp_encode, face)
        encodings.append(r.pop())

    image_name = "Unknown"
    if True in encodings:
        first_match_index = encodings.index(True)
        image_name = known_names[first_match_index]
        generate_json(image_name)
    elif False in encodings:
        add_unknown_image()
        generate_json(image_name)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
