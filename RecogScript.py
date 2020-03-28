"""
Samaritan Security Facial Recognition Script

SDMay20-45
Dept. of Electrical and Computer Engineering
Iowa State University
Author(s): Devin Uner, Ryan Goluch, Ann Gould
"""

from FacialRecog import all_cameras, get_all_people_information, get_frame_from_camera, compare_frame_and_encodings, process_comparisons

'''
Main script function
'''


def main():
    # cameras = all_cameras()
    # all_ids, all_encodings = get_all_people_information()

    while True:
        # for camera in cameras:
            camera, frame = get_frame_from_camera()
            print(frame)
            # comparison_results = compare_frame_and_encodings(
            #     frame, all_encodings)
            # process_comparisons(comparison_results, all_ids, camera, frame)


if __name__ == "__main__":
    main()
