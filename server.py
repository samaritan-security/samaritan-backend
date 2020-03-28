# USAGE
# python server.py --prototxt MobileNetSSD_deploy.prototxt --model MobileNetSSD_deploy.caffemodel --montageW 2 --montageH 2

from datetime import datetime
import imagezmq


def main():
    # initialize the ImageHub object
    image_hub = imagezmq.ImageHub()

    # initialize the dictionary which will contain  information regarding
    # when a device was last active, then store the last time the check
    # was made was now
    last_active = {}
    last_active_check = datetime.now()

    # start looping over all the frames
    while True:
        rpi_name, frame = image_hub.recv_image()
        image_hub.send_reply(b'OK')

        # if a device is not in the last active dictionary then it means that its a newly connected device
        if rpi_name not in last_active.keys():
            print("[INFO] receiving data from {}...".format(rpi_name))

        # record the last active time for the device from which we just received a frame
        last_active[rpi_name] = datetime.now()

        print("Frame received")
        print(frame)

        # if current time *minus* last time when the active device check was made is
        # greater than the threshold set then do a check
        if (datetime.now() - last_active_check).seconds > 10:
            # loop over all previously active devices
            for (rpi_name, ts) in list(last_active.items()):
                # remove the RPi from the last active and frame dictionaries if the
                # device hasn't been active recently
                if (datetime.now() - ts).seconds > 10:
                    print("[INFO] lost connection to {}".format(rpi_name))
                    last_active.pop(rpi_name)

            # set the last active check time as current time
            last_active_check = datetime.now()


if __name__ == "__main__":
    main()
