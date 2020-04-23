"""
Samaritan Security Facial Recognition Script

SDMay20-45
Dept. of Electrical and Computer Engineering
Iowa State University
Author(s): Devin Uner, Ryan Goluch, Ann Gould
"""


from FacialRecog import all_cameras, get_all_people_information, get_frame_from_camera, compare_frame_and_encodings, process_comparisons
import imagezmq
from timeoutqueue import TimeoutQueue


def main():
    """
    Main script function
    """
    cameras = all_cameras()
    all_ids, all_encodings = get_all_people_information()
    image_hub = imagezmq.ImageHub()
    timeout_queue = TimeoutQueue(4)

    while True:
        for camera in cameras:
            frame = get_frame_from_camera(image_hub, camera)
            comparison_results = compare_frame_and_encodings(
                frame, all_encodings)
            if comparison_results is not None:
                if len(timeout_queue.get()) != 0:
                    # print("hitting timeoutqueue")
                    if comparison_results not in timeout_queue.get():
                        timeout_queue.append(comparison_results)
                        process_comparisons(comparison_results, all_ids, camera, frame)
                else:
                    # print("now being added")
                    timeout_queue.append(comparison_results)


if __name__ == "__main__":
    main()
