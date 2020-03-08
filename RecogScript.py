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

from FacialRecog import *

'''
Function to add unknown images to the database of images
Returns image path
'''


def add_unknown_image(img):
    seed(time.time())
    image_counter = rand.randrange(int(time.time()))
    directory = os.fsencode("images/unknown")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.find(str(image_counter)):
            image_counter = rand.randrange(int(time.time()))
    image_location = 'images/unknown/%d.jpeg' % image_counter
    cv2.imwrite(image_location, img)
    return image_location


# TODO add in temp access pics (idk if this needs a function)


# refactor images directory to be a list of directories probably?
def process_video_to_encode(video_feed, images_directory, temp_filename="images/temp.jpeg"):

    known_names, known_encodings = scan_for_known_people(images_directory)
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

    # ryan look hereee...
    if len(temp_encode) == 0:
        return None, known_names, small_frame

    encodings = []
    for face in known_encodings:
        if len(temp_encode) == 1:
            temp = [face_recognition.compare_faces(face, temp_encode)]
            encodings.append(temp)
        else:
            encodings.append(face_recognition.compare_faces(face, temp_encode))

    return encodings, known_names, small_frame


def check_encodings(encodings, known_names, small_frame, que):
    if encodings is not None:
        person_name = "unknown"
        for entry in encodings:
            if True in entry[:len(entry)]:
                match_index = encodings.index(entry)
                person_name = known_names[match_index]
                path = "images/employees/" + person_name.replace(" ", "_") + ".jpeg"
                image = open(path, "rb")
                image_encoded = base64.b64encode(image.read())
                image_encoded = image_encoded.decode('utf-8')
                add_to_known_stream(person_name, image_encoded)
                generate_json(person_name)
                image.close()
            else:
                if entry not in que:
                    path = add_unknown_image(small_frame)
                    unknown_image = open(path, "rb")
                    unknown = base64.b64encode(unknown_image.read())
                    unknown = unknown.decode('utf-8')
                    add_to_unknown_stream(unknown)
                    generate_json(person_name)
                else:
                    que.append(entry)
    return que

'''
Main script function
'''
def main():
    video_capture = get_camera_ip_from_file("camera_ip.txt")
    unknown_que = []

    while True:
        encodings, known_names, small_frame = process_video_to_encode(video_capture, "images/employees")
        unknown_que = check_encodings(encodings, known_names, small_frame, unknown_que)




if __name__== "__main__":
    main()
