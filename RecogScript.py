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

    # known_names, known_encodings = scan_for_known_people(images_directory)
    #known_names, known_encodings = get_names_and_encodings_from_known()
    all_ids, all_encodings = get_all_people_information()

    ret, frame = video_feed.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)

    # Convert the image from BGR color (which OpenCV uses)
    # to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    #why do we write this?
    #can't we do :
    #temp_encode = face_recognition.face_encodings(small_frame)
    cv2.imwrite(temp_filename, small_frame)
    temp = face_recognition.load_image_file(temp_filename)
    temp_encode = face_recognition.face_encodings(temp)

    # ryan look hereee...
    if len(temp_encode) == 0:
        return None, all_ids, small_frame #changed known_names -> all_ids

    encodings = []
    for face in all_encodings: #changed known_encodings -> all_encodings
        if len(temp_encode) == 1:
            temp = [face_recognition.compare_faces(face, temp_encode)]
            encodings.append(temp)
        else:
            encodings.append(face_recognition.compare_faces(face, temp_encode))

    return encodings, all_ids, small_frame #changed known_names -> all_ids


def check_encodings(encodings, all_ids, small_frame): #changed known_names -> all_ids
    if encodings is not None:
        person_name = "unknown"
        for entry in encodings:
            # if we know who this is
            if True in entry[:len(entry)]:
                match_index = encodings.index(entry)

                #person_name = known_names[match_index]
                add_new_seen(all_ids[match_index])
                check_for_alert(all_ids[match_index])
                
                # don't think we will need this anymore
                # path = "images/employees/" + person_name.replace(" ", "_") + ".jpeg"
                # image = open(path, "rb")
                # image_encoded = base64.b64encode(image.read())
                # image_encoded = image_encoded.decode('utf-8')
                # add_to_known_stream(person_name, image_encoded)
                # generate_json(person_name)
                # image.close()

            # if we don't know who this is, add unknown
            else:
                encoded_image = base64.b64encode(small_frame)
                encoded_image = encoded_image.decode('utf-8')
                encoded_encoding = face_recognition.load_image_file(small_frame)
                encoded_encoding = face_recognition.face_encodings(encoded_encoding)
                encoded_encoding = str(encoded_encoding)
                data = {"img": encoded_image, "npy": encoded_encoding}
                add_unknown_person(data)

                #don't think we need anymore
                # path = add_unknown_image(small_frame)
                # unknown_image = open(path, "rb")
                # unknown = base64.b64encode(unknown_image.read())
                # unknown = unknown.decode('utf-8')
                # add_to_unknown_stream(unknown)
                # generate_json(person_name)

'''
Main script function
'''
def main():
    video_capture = get_camera_ip_from_file("camera_ip.txt")

    while True:
        encodings, known_names, small_frame = process_video_to_encode(video_capture, "images/employees")
        check_encodings(encodings, known_names, small_frame)




if __name__== "__main__":
    main()
