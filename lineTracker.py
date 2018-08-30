#! /usr/bin/env python3.6

from picamera.array import PiRGBArray
from picamera import PiCamera
import time 
import cv2
import numpy as np

_IMAGE_WIDTH = 640
_IMAGE_HEIGHT = 480
_KERNEL = np.ones((2, 2), np.uint8)

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
        grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        image = cv2.inRange(image, 0, 50)
        cv2.morphologyEx(image, cv2.MORPH_CLOSE, _KERNEL, image)
        
        _, contours, _ = cv2.findContours(image, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            maxc = max(contours, key=cv2.contourArea())
            
        cv2.drawContours(image, contours, -1, (0, 100, 100), -1)
        
        # cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        
        # clear current frame
        rawCapture.truncate(0)
        
        if key == ord("q"):
            break
