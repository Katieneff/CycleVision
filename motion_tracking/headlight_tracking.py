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
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (0, 0, 255)
greenUpper = (255, 255, 255)
pts = deque(maxlen=args["buffer"])

# load the image and convert it to grayscale
camera = cv2.VideoCapture(args["video"])


while True:
	# grab the current frame
	(grabbed, orig) = camera.read()
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		print "Can't grab video"
		continue
 
	orig = imutils.resize(orig, width=600)

	hsv = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV)

	#cv2.imshow("HSV", hsv)


	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)


	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	contours = orig.copy()
	cv2.drawContours(contours, cnts, -1, (0,255,0), 3)
	cv2.imshow("Contours", contours)
	
	i = 0

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		for i in range(0, len(cnts)):
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
		#	c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(cnts[i])
			
			M = cv2.moments(cnts[i])
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])

			if cX < 150:
				continue
			if cX > 220:
				print "right"
			else:
				print "left"
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			i+=1
			# only proceed if the radius meets a minimum size
			if radius < 10:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(orig, (int(x), int(y)), int(radius), (0, 255, 255), 2)
				cv2.circle(orig, center, 5, (0, 0, 255), -1)


		#pts.appendleft(center)
			# loop over the set of tracked points
		#for i in xrange(1, len(pts)):
			# if either of the tracked points are None, ignore
			# them
		#	if pts[i - 1] is None or pts[i] is None:
		#		continue

			# otherwise, compute the thickness of the line and
			# draw the connecting lines
	#		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
	#		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	#	 show the frame to our screen
		cv2.imshow("Circles", orig)
 	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()


