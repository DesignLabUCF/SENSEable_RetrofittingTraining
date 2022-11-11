##################################
#   Retrofitting Undistorter     #
#     SENSEable Design Lab       #
##################################
# v1.0
# 2/11/2021
##################################
# To run, pass in 1 for full folder or 0 for single file and folder/file name w/ extension
# EXP: 'python Undistorter.py 1/0 Folder/File'
##################################
# Authors: 
# Sermarini
# Kider
##################################


import sys
import os
import cv2
import numpy as np
import glob


def undistort(image_name):
    # Import calibration data
    mtx = np.load("Camera\\Calibration\\mtx.npy")
    dist = np.load("Camera\\Calibration\\dist.npy")
    revcs = np.load("Camera\\Calibration\\revcs.npy")
    tvecs = np.load("Camera\\Calibration\\tvecs.npy")
    assert mtx.size != 0, "Error: mtx loaded empty. Maybe run CameraCalibration.py?"
    assert dist.size != 0, "Error: dist loaded empty. Maybe run CameraCalibration.py?"
    assert revcs.size != 0, "Error: revcs loaded empty. Maybe run CameraCalibration.py?"
    assert tvecs.size != 0, "Error: tvecs loaded empty. Maybe run CameraCalibration.py?"

    img = cv2.imread(image_name)
    h, w = img.shape[:2]
    # Refining the camera matrix using parameters obtained by calibration
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    # Method 1 to undistort the image
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    # Method 2 to undistort the image
    #mapx,mapy=cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
    #dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)
    # Crop image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    # Save image
    image_name = image_name[:-4] + "_Undistorted.jpg"
    print("Creating " + image_name + "...")
    undistorted_image = cv2.imwrite(image_name, dst)

def main(argv):
    # Check inputs and initialize
    assert len(sys.argv) >= 2, "Error: Argument required for entire folder key (1 is yes, 0 is no) and folder/file name"
    # Full folder
    if argv[0] == "1":
        assert os.path.isdir(argv[1]), "Error: Folder " + argv[1] + " not found."
        file_names = glob.glob(argv[1] + "\\*.jpg")
        for file_name in file_names:
            if "_Undistorted" in file_name: # Don't undistort undistorted images. File explorer pain avoidance
                continue
            if "_Highlighted" in file_name: # Don't undistort highlighted images.
                continue
            #undistort(file_name, mtx, dist, revcs, tvecs)
            undistort(file_name)
    # Individual file
    else:
        assert os.path.exists(argv[1]), "Error: File " + argv[1] + " not found."
        #undistort(argv[1], mtx, dist, revcs, tvecs)
        undistort(argv[1])

if __name__=='__main__':
    main(sys.argv[1:])