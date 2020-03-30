# USAGE
# python client.py --server-ip SERVER_IP

# import the necessary packages
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip")
ap.add_argument("-c", "--camera-ip")
args = vars(ap.parse_args())

# initialize the ImageSender object with the socket address of the
# server

sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(
	args["server_ip"]))

# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
rpiName = socket.gethostname()
feed = cv2.VideoCapture("http://" + str(args["camera_ip"]) + "/video.mjpg")
# ret, img = feed.read()
# vs = VideoStream(src="http://"+str(args["camera_ip"])+"/video.mjpg").start()
time.sleep(2.0)
i = 0
while True:
	# read the frame from the camera and send it to the server
	ret, frame = feed.read()
	print(i)
	i+=1
	sender.send_image(rpiName, frame)