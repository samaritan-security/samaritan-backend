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

    return encodings, all_ids, frame 


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

                    frame = cv2.resize(image, (0, 0), fx=0.75, fy=0.75)
                    unknown_encodings, unknown_images = get_images_and_encodings(frame)

                    i = 0
                    for encoding in unknown_encodings:
                        encoded_image = base64.b64encode(unknown_images[i]).decode('utf-8')
                        encoding_str = str(encoding[i])
                        data = {"img":encoded_image, "npy": encoding_str}
                        add_unknown_person(data)
                        i = i + 1


'''
Main script function
'''
def main():

    while True:
        # when we start storing cameras {ip, nickname} in db, then we can pull
        # info from there and then that information will be passed down
        # so we can tie who is seen by what camera
        video_feeds = get_multiple_camera_feeds_from_file("camera_ip.txt")
        for video_feed in video_feeds:
            encodings, all_ids, small_frame = process_video_to_encode(video_capture)
            check_encodings(encodings, all_ids, small_frame)


if __name__== "__main__":
    main()
