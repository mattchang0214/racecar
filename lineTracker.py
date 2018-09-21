#! /usr/bin/env python3.6

from motorControl import motorControl
from picamera.array import PiRGBArray
from picamera import PiCamera
import time 
import cv2
import numpy as np

_BLACK_THRESH = 50
_DEBUG = True
_FRAMERATE = 5
_IMAGE_WIDTH = 640
_IMAGE_HEIGHT = 480
_KERNEL_SIZE = 10
_KERNEL = np.ones((_KERNEL_SIZE, _KERNEL_SIZE), np.uint8)
_LENGTH_THRESH = 120
_NUM_PX_AHEAD = 240


def getContours(image):
    # change colorspace to grayscale
    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # binarize the image with thresholds
    cv2.inRange(grey_img, 0, _BLACK_THRESH, grey_img)
    # close small holes in object
    cv2.morphologyEx(grey_img, cv2.MORPH_CLOSE, _KERNEL, grey_img)
    
    _, contours, _ = cv2.findContours(grey_img, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)

    return contours

def getVec(vx, vy, x, y):
    frame_center = np.asarray([_IMAGE_WIDTH / 2.0, _IMAGE_HEIGHT / 2.0]) # ctr of screen
    line_center = np.asarray([x, y]) # point on line
    slope = np.asarray([vx, vy]) # vector parallel to line
    slope = slope / np.linalg.norm(slope) # normalize
    closest = slope * np.dot(slope, frame_center - line_center) + line_center # point on line closest to center
    # to_line = closest - frame_center # shortest vector from ctr to line
    # line_dist = np.linalg.norm(to_line)  # dist from line to ctr

    # Extrapolate forwards to determine target
    if slope[1] > 0:
        slope *= -1
    print(slope)
    target = closest + slope * _NUM_PX_AHEAD
    to_target = target - frame_center
    to_target = [int(x) for x in to_target]

    print("[{}, {}]".format(to_target[0], to_target[1]))

    return to_target

if __name__ == '__main__':
    with PiCamera() as camera:
        camera.resolution = (_IMAGE_WIDTH, _IMAGE_HEIGHT)
        camera.framerate = _FRAMERATE
        rawCapture = PiRGBArray(camera, size=camera.resolution)
        time.sleep(0.1) # let camera warm up

        with motorControl([13, 19], [20, 16]) as motCon:
            # capture_continuous returns infinite iterator of images
            # use_video_port for rapid capture
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                contours = getContours(image)
                
                if len(contours) > 0:
                    maxc = max(contours, key=cv2.contourArea) # get biggest contour
                    rect = cv2.minAreaRect(maxc)
                    rectw, recth = rect[1]
                # check size of contour
                if rectw < _LENGTH_THRESH and recth < _LENGTH_THRESH:
                    rawCapture.truncate(0)
                    continue
                [vx,vy,x,y] = cv2.fitLine(maxc, distType=cv2.DIST_L2, param=0, reps=0.01, aeps=0.01)
                target = getVec(vx[0], vy[0], x[0], y[0])
                motCon.cmd_vel(target)
                
                if _DEBUG:
                    # overlay contours on original image
                    cv2.drawContours(image, contours, -1, (0, 255, 0), -1)
                    cv2.drawContours(image, [maxc], -1, (255, 0, 0), -1)
                    # xy = np.array([x[0],y[0]])
                    # v = np.array([vx[0], vy[0]])
                    # bv = (v * 50) + xy
                    # if x and y and bv[0] > 0 and bv[1] > 0:
                    #    cv2.line(img=image,pt1=(x, y),pt2=(bv[0], bv[1]),color=(255,0,255),thickness=1)
                    #    cv2.circle(img=image, center=(x, y), radius=2, color=(0, 255, 0), thickness=-1)
                    cv2.imshow("Final Image", image)
                
                key = cv2.waitKey(1) & 0xFF
                
                # clear current frame
                rawCapture.truncate(0)
                
                if key == ord("q"):
                   break
