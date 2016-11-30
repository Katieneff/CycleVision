import numpy as np
import cv2
import glob
import argparse 
import imutils
from collections import deque

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the headlights
# in the HSV color space
maskLower = (0, 0, 255)
maskUpper = (255, 255, 255)

# load the video
camera = cv2.VideoCapture(args["video"])


while True:
	# grab the current frame
	(grabbed, orig) = camera.read()
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		print "Can't grab video"
		continue
		
 	# Resize for faster processing
	orig = imutils.resize(orig, width=600)

	# Convert to HSV color to find headlights
	hsv = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV)

	# Mask headlights. Ranges found with https://github.com/jrosebr1/imutils/blob/master/bin/range-detector
	mask = cv2.inRange(hsv, maskLower, maskUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)


	# find contours in the mask and initialize the current
	# (x, y) center of the contours
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	contours = orig.copy()
	cv2.drawContours(contours, cnts, -1, (0,255,0), 3)
	cv2.imshow("Contours", contours)

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		for i in range(0, len(cnts)):
			# find the minimum enclosing circle in the contour
			((x, y), radius) = cv2.minEnclosingCircle(cnts[i])
			
			# Find center coordinates
			M = cv2.moments(cnts[i])
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])

			# Used to ignore the sky (place on the lefthand side of the frame
			# because the sky is the same color as the headlights)
			if cX < 150:
				continue
				
			# If the headlight is on lefthand side, print left,
			# if right, print right
			if cX > 220:
				print "right"
			else:
				print "left"
			
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			
			# only proceed if the radius meets a minimum size
			if radius < 10:
				# draw the circle and centroid on the frame
				cv2.circle(orig, (int(x), int(y)), int(radius), (0, 255, 255), 2)
				cv2.circle(orig, center, 5, (0, 0, 255), -1)

		#show the frame to our screen
		cv2.imshow("Circles", orig)
 	
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()


