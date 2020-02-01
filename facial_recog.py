'''
Samaritan Security Facial Recognition Script

SDMay20-45
Dept. of Electrical and Computer Engineering
Iowa State University 
Author(s): Devin Uner, Ryan Goluch, Ann Gould
'''

import face_recognition
import cv2
from random import seed
from random import random
import time
import os
import json
import datetime

'''
gets ips from file 
'''


def get_camera_ip_from_file(filename: str):
    # Use a list of camera ips for ease of testing
    file = open(filename, "r")
    ip = file.readline()
    # video_feed = cv2.VideoCapture(0)
    video_feed = cv2.VideoCapture("http://" + str(ip) + "/video.mjpg")
    file.close()
    return video_feed


# can return multiple different things in python (peep return statement)
'''
loads facial recog image file, encodes and names known face
'''


def facial_recog_process(image_name: str):
    user_image = face_recognition.load_image_file(image_name)
    user_face_encoding = face_recognition.face_encodings(user_image)[0]
    encodings_list = [user_face_encoding]
    names = ["Ryan Goluch"]
    return encodings_list, names


# writes the facial data to DB
def add_facial_data():
    # TODO
    return True


def generate_json(name: str) -> json:
    data = {"name": name, "date": datetime.datetime.now()}
    print(data)
    return json.dumps(data)


video_capture = get_camera_ip_from_file("camera_ip.txt")
known_face_encodings, known_face_names = facial_recog_process("images/Goluch_Ryan.jpeg")

seed(time.time())
image_counter = random()
directory = os.fsencode("images")
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.find(str(image_counter)):
        image_counter = random()

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) 
    # to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        image_name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            image_name = known_face_names[first_match_index]
            generate_json(image_name)
        elif False in matches:
            cv2.imwrite('images/%d.jpeg' %image_counter, small_frame)
            # video_capture.release()
            # cv2.destroyAllWindows()

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, image_name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
