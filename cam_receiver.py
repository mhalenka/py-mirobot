#!/usr/bin/python3

import imagezmq
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
args = vars(ap.parse_args())

# initialize the ImageHub object
imageHub = imagezmq.ImageHub(open_port="tcp://mirobot", REQ_REP=False)

# start looping over all the frames
while True:
    # receive RPi name and frame from the RPi and acknowledge
    # the receipt
    (rpiName, frame) = imageHub.recv_image()

    cv2.imshow("frame", frame)
    cv2.waitKey(1)
