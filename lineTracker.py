#! /usr/bin/env python3.6

from picamera.array import PiRGBArray
from picamera import PiCamera
import time 
import cv2

_IMAGE_WIDTH = 640
_IMAGE_HEIGHT = 480

# default framerate = 30fps
with PiCamera() as camera:
    camera.resolution = (_IMAGE_WIDTH, _IMAGE_HEIGHT)
    camera.framerate = 5
    rawCapture = PiRGBArray(camera, size=camera.resolution)

    time.sleep(0.1)

    # capture_continuous returns infinite iterator of images
    # use_video_port for rapid capture
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        
        # clear current frame
        rawCapture.truncate(0)
        
        if key == ord("q"):
            break
