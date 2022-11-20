

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import math

LEN_LINE = 3
minDelta = 10
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

def countAngle(delta_x, delta_y):
    if (abs(delta_x)<minDelta):
        if (abs(delta_y)<minDelta):
            return None
        else:
            if delta_y > 0:
                return 90
            else:
                return 270
    if (abs(delta_y)<minDelta):
        if delta_x > 0:
            return 0
        else:
            return 180
    return (math.atan(delta_y/delta_x)*180/math.pi)

# define the lower and upper boundaries of the "yellow object"
# (or "ball") in the HSV color space, then initialize the
# list of tracked points
colorLower = (95, 100, 100)
colorUpper = (115, 255, 255)
pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(-3)
 
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])
cnt = 0
# keep looping

x0 = 0
y0 = 0
y1 = 0
x1 = 0
delta_x = 0
delta_y = 0
while True:
    cnt += 1
    # grab the current frame
    (grabbed, frame) = camera.read()
 
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break
 
    # resize the frame, inverted ("vertical flip" w/ 180degrees),
    # blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=600)
    #frame = imutils.rotate(frame, angle=180)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
 
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            #cv2.circle(frame, center, 5, (0, 0, 255), -1)
            #print(int(x), int(y), radius)
            x1 = int(x)
            y1 = int(y)
            print("x = ", x1, "y = ", y1, "angle=", countAngle(delta_x, delta_y))

            if(cnt % 5 == 0):
                #print(abs(x_old - int(x)),abs(y_old - int(y)) )
                    
                if( (abs(x0 - x1) > LEN_LINE) and (abs(y0 - y1) > LEN_LINE) ):
                    #print("line")

                    delta_x = (x1-x0)
                    delta_y = (y1-y0)
                    x0 = x1
                    y0 = y1
                print("dx = ", delta_x, "dy = ", delta_y)
            #cv2.line(frame, (x1, y1), (x0+delta_x*2, y0 + delta_y*2), (255,255 , 0), 10)
            cv2.line(frame, (x1, y1), (x1 + delta_x*2, y1 + delta_y*2), (255,255 , 0), 10)
 
    # update the points queue
    #pts.appendleft(center)
    
        # loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue
 
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        #cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
 
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()