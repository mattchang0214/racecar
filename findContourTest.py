#! /usr/bin/env python3.6

from picamera.array import PiRGBArray
from picamera import PiCamera
import time 
import cv2
import numpy as np

_IMAGE_WIDTH = 640
_IMAGE_HEIGHT = 480
_KERNEL_SIZE = 2
_KERNEL = np.ones((_KERNEL_SIZE, _KERNEL_SIZE), np.uint8)

# default framerate = 30fps
with PiCamera() as camera:
    camera.resolution = (_IMAGE_WIDTH, _IMAGE_HEIGHT)
    camera.framerate = 5
    rawCapture = PiRGBArray(camera, size=camera.resolution)

    time.sleep(0.1)

    # capture_continuous returns infinite iterator of images
    # use_video_port for rapid capture
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    
    # show original image
    cv2.imshow("Colored Image", image)
    cv2.waitKey(0)
	
    # change colorspace to grayscale
    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Grey Image", grey_img)
    cv2.waitKey(0)
    print(grey_img)
    
    # binarize the image with thresholds
    cv2.inRange(grey_img, 0, 50, grey_img)
    cv2.imshow("Threshold Image", grey_img)
    cv2.waitKey(0)
    print(grey_img)
	
    # close small holes in object
    cv2.morphologyEx(grey_img, cv2.MORPH_CLOSE, _KERNEL, grey_img)
    cv2.imshow("Transformed Image", grey_img)
    cv2.waitKey(0)
	
    _, contours, _ = cv2.findContours(grey_img, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
	
    # if len(contours) > 0:
        # maxc = max(contours, key=cv2.contourArea())
		
    # overlay contours on original image
    cv2.drawContours(image, contours, -1, (0, 255, 0), -1)
    cv2.imshow("Final Image", image)
    cv2.waitKey(0)
    
    time.sleep(0.5)
    cv2.destroyAllWindows()
