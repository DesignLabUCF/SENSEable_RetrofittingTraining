##################################
#  Retrofitting Cam. Calibration #
#     SENSEable Design Lab       #
##################################
# v1.0
# 2/11/2021
##################################
# EXP: 'python Undistorter.py'
##################################
# Authors: 
# Sermarini
# Kider
##################################

# SET 2
# error 0.447196

# Latest Set 
# error ~0.23 :)

import cv2
import numpy as np
import glob




# TODO UPDATE SCRIPT TO ALLOW FOR CUSTOM OUTPUT LOCATION INSTEAD OF HARDCODED




# Defining the dimensions of checkerboard
CHECKERBOARD = (6,9)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Creating vector to store vectors of 3D points for each checkerboard image
objpoints = []
# Creating vector to store vectors of 2D points for each checkerboard image
imgpoints = [] 

# Defining the world coordinates for 3D points
objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

# Extracting path of individual image stored in a given directory
#images = glob.glob('./images/*.jpg')
images = glob.glob('Camera/Calibration/JPG/*.jpg')
for fname in images:
    if "_Highlighted" in fname or "_Undistorted" in fname: # Only need the OG camera pics
        continue
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    # If desired number of corners are found in the image then ret = true
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+
    	cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
    """
    If desired number of corner are detected,
    we refine the pixel coordinates and display 
    them on the images of checker board
    """
    if ret == True:
        print("Found CHECKERBOARD on " + fname)
        objpoints.append(objp)
        # refining pixel coordinates for given 2d points.
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)
        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2,ret) 
    # Show results in window
    """
    cv2.imshow('img',img)
    cv2.waitKey(0)
    """
    # Write checkerboard highlighted image to file
    name_split = fname.split("\\")
    image_name = "Camera\\Calibration\\JPG\\" + name_split[1][:-4] + "_Highlighted.png"
    print("Creating " + image_name + "...")
    cv2.imwrite(image_name, img)

cv2.destroyAllWindows()

h,w = img.shape[:2]

"""
Performing camera calibration by 
passing the value of known 3D points (objpoints)
and corresponding pixel coordinates of the 
detected corners (imgpoints)
"""
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
#print("Camera matrix : \n")
#print(mtx)
#print("dist : \n")
#print(dist)
#print("rvecs : \n")
#print(rvecs)
#print("tvecs : \n")
#print(tvecs)

# Save camera calibration data to external file for re-use
np.save("Camera\\Calibration\\mtx", mtx)
np.save("Camera\\Calibration\\dist", dist)
np.save("Camera\\Calibration\\revcs", rvecs)
np.save("Camera\\Calibration\\tvecs", tvecs)

# Print mean error to console (Closer to zero is better)
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error
print( "total error: {}".format(mean_error/len(objpoints)) )

"""
## Undistort all images as a test
# Using the derived camera parameters to undistort the image
image_names = glob.glob('Camera\\JPG\\*.jpg')
for image_name in image_names:
    img = cv2.imread(image_name)
    # Refining the camera matrix using parameters obtained by calibration
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    # Method 1 to undistort the image
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    # Method 2 to undistort the image
    mapx,mapy=cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
    dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)
    # Crop image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    # Save image
    image_name = image_name[:-4] + "_Undistorted.jpg"
    print("Creating " + image_name + "...")
    cv2.imwrite(image_name, dst)
"""