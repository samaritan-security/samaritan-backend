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

from FacialRecog import *

'''
loads facial recog image file, encodes and names known face
'''


def facial_recog_process(faces):
    for face in faces:
        encodings = face_recognition.compare_faces(face, temp)
    names = ["Ryan Goluch"]
    return encodings, names

'''
Function to add unknown images to the database of images
Returns image path
'''
def add_unknown_image():
    seed(time.time())
    image_counter = rand.randrange(int(time.time()))
    directory = os.fsencode("images/unknown")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.find(str(image_counter)):
            image_counter = rand.randrange(int(time.time()))
    image_location = 'images/unknown/%d.jpeg' % image_counter
    cv2.imwrite(image_location, small_frame)
    return image_location


# TODO add in temp access pics (idk if this needs a function)


'''
Main script function
'''

# TODO: this line should be changed for when @rgoluch adds video footage :)
video_capture = get_camera_ip_from_file("camera_ip.txt")
known_names, known_encodings = scan_for_known_people("images/employees")

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

    cv2.imwrite('images/temp.jpeg', small_frame)
    temp = face_recognition.load_image_file("images/temp.jpeg")
    temp_encode = face_recognition.face_encodings(temp)

    for face in known_encodings:
        encodings = face_recognition.compare_faces(temp_encode, face)

    known_face_names = ["Ryan Goluch"]
    person_name = "Unknown"
    data = None

    if True in encodings:
        first_match_index = encodings.index(True)
        person_name = known_face_names[first_match_index]
        add_facial_data(person_name, path)
        generate_json(person_name)
    elif False in encodings:
        path = add_unknown_image()
        add_facial_data(person_name, path)
        generate_json(person_name)
