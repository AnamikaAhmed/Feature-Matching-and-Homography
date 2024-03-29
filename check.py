import numpy as np
import cv2
from matplotlib import pyplot as pl
import itertools
import math

MIN_MATCH_COUNT = 10

img1 = cv2.imread('rotated_image.PNG',0)  # queryImage
img2 = cv2.imread('normal_image.PNG',0) # trainImage

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()
#descriptor = cv2.DescriptorExtractor_create("SIFT")
# find the keypoints and descriptors with SIFT
#kp1 = sift.detect(img1)
#kp1, des1 = descriptor.compute(img1, kp1)

#kp2 = sift.detect(img2)
#kp2, des2 = descriptor.compute(img2, kp2)


kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1,des2,k=2)

# store all the good matches as per Lowe's ratio test.
good = []
for m, n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)
if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)

    if np.shape(M) == ():
        print( "No transformation possible" )
        # derive rotation angle from homography
    else:
        theta = - math.atan2(M[0,1], M[0,0]) * 180 /math.pi
        print("The angle is: ")
        print(theta)
