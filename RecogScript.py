"""
Samaritan Security Facial Recognition Script

SDMay20-45
Dept. of Electrical and Computer Engineering
Iowa State University
Author(s): Devin Uner, Ryan Goluch, Ann Gould
"""

import time
from random import seed
import random as rand
import base64
import numpy as np

from Alerts import check_for_alert
from FacialRecog import *
from app import add_unknown_person, add_new_seen


def process_video_to_encode(video_feed, images_directory, temp_filename="images/temp.jpeg"):

    all_ids, all_encodings = get_all_people_information()


    ret, frame = video_feed.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)

    # Convert the image from BGR color (which OpenCV uses)
    # to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    cv2.imwrite(temp_filename, small_frame)
    temp = face_recognition.load_image_file(temp_filename)
    temp_encode = face_recognition.face_encodings(temp)


    if len(temp_encode) == 0:
        return None, all_ids, small_frame 

    encodings = []
    for face in all_encodings: 
        if len(temp_encode) == 1:
            temp = [face_recognition.compare_faces(face, temp_encode)]
            encodings.append(temp)
        else:
            encodings.append(face_recognition.compare_faces(face, temp_encode))

    return encodings, all_ids, small_frame 


def check_encodings(all_encodings, all_ids, small_frame, temp_filename="images/temp.jpeg"):
    if all_encodings is not None:
        for entry in all_encodings:
            if True in entry[:len(entry)]:
                match_index = all_encodings.index(entry)
                add_new_seen(all_ids[match_index])
                check_for_alert(all_ids[match_index])

            else:
                cv2.imwrite(temp_filename, small_frame)
                image = cv2.imread(temp_filename)

                if(!detect_blurry_image(image)):
                    encoded_image = base64.b64encode(small_frame)
                    encoded_image = encoded_image.decode('utf-8')
                    temp = face_recognition.load_image_file(temp_filename)
                    encoding = face_recognition.face_encodings(temp)
                    encoding = str(encoding)
                    data = {"img": encoded_image, "npy": encoding}
                    add_unknown_person(data)

'''
Main script function
'''
def main():
    video_capture = get_camera_ip_from_file("camera_ip.txt")
    unknown_queue = []

    while True:
        encodings, all_ids, small_frame = process_video_to_encode(video_capture, "images/employees")
        check_encodings(encodings, all_ids, small_frame)


if __name__== "__main__":
    main()
