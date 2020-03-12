"""
Samaritan Security Facial Recognition Script

SDMay20-45
Dept. of Electrical and Computer Engineering
Iowa State University
Author(s): Devin Uner, Ryan Goluch, Ann Gould
"""

import base64

from Alerts import check_for_alert
from BlurDetection import detect_blurry_image
from FacialRecog import *
from app import add_unknown_person, add_new_seen


def process_video_to_encode(video_feed):

    all_ids, all_encodings = get_all_people_information()

    frame = get_frame(video_feed)

    frame_encodings = get_face_encodings(frame)

    encodings = compare_encodings(frame_encodings, all_encodings)

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

                if not detect_blurry_image(image):
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

    while True:
        encodings, all_ids, small_frame = process_video_to_encode(video_capture)
        check_encodings(encodings, all_ids, small_frame)


if __name__== "__main__":
    main()
