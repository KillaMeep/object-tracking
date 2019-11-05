from __future__ import print_function

import sys
import cv2
from random import randint
import argparse
#import imutils
import time

trackerTypes = ['boosting', 'mil', 'kcf', 'tld', 'medianflow', 'goturn', 'mosse', 'csrt']
multiTracker = None

def createTrackerByName(trackerType):
    #Make a tracker by name
    if trackerType == trackerTypes[0]:
        tracker = cv2.TrackerBoosting_create()
    elif trackerType == trackerTypes[1]:
        tracker = cv2.TrackerMIL_create()
    elif trackerType == trackerTypes[2]:
        tracker = cv2.TrackerKCF_create()
    elif trackerType == trackerTypes[3]:
        tracker = cv2.TrackerTLD_create()
    elif trackerType == trackerTypes[4]:
        tracker = cv2.TrackerMedianFlow_create()
    elif trackerType == trackerTypes[5]:
        tracker = cv2.TrackerGOTURN_create()
    elif trackerType == trackerTypes[6]:
        tracker = cv2.TrackerMOSSE_create()
    elif trackerType == trackerTypes[7]:
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = None
        print('Incorrect tracker name!')
        print('Available trackers are:')
        for t in trackerTypes:
            print(t)

    return tracker

def selectROI(frame):
    while True:
        bbox = cv2.selectROI('MultiTracker', frame)
        bboxes.append(bbox)
        colors.append((randint(0,255), randint(0,255), randint(0,255)))
        print("Press q to quit selecting boxes and start tracking")
        print("Press any other key to select next object for tracking")
        k = cv2.waitKey(0) & 0xFF
        if (k == 113): # q is pressed
            break
    print("Selected bounding boxes {}".format(bboxes))
    multiTracker = cv2.MultiTracker_create()
    for bbox in bboxes:
        multiTracker.add(createTrackerByName(args["tracker"]), frame, bbox)
    return multiTracker

#Grab our command line args and parse them into args

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="Path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="csrt", help="OpenCV tracker type")
args = vars(ap.parse_args())

tracker=args["tracker"]

if not args.get("video", False):
    print("[INFO] Starting video stream...")
    cap = cv2.VideoCapture(0)
    fps = int(cap.get(5))
    print("FPS: {}".format(fps))
    time.sleep(1.0)

else:
    cap = cv2.VideoCapture(args["video"])
    fps = int(cap.get(5))
    print("FPS: {}".format(fps))

success, frame = cap.read()

if not success:
    print("Failed to read video")
    sys.exit(1)

bboxes = []
colors = []

while cap.isOpened():
    success, frame = cap.read()
    timer = cv2.getTickCount()
    if not success:
        break

    if multiTracker is not None:
        print("Tracking")
        success, boxes = multiTracker.update(frame)
        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
    calcfps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(frame, "FPS: " + str(int(calcfps)), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
    cv2.imshow('MultiTracker', frame)

    key = cv2.waitKey(int(1000/fps)) & 0xFF
    if key == ord("s"):
        multiTracker = selectROI(frame)
    elif key == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()





