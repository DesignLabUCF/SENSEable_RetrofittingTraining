##################################
#   Retrofitting Undistorter     #
#     SENSEable Design Lab       #
##################################
# v1.0
# 2/11/2021
##################################
# To run, pass in 1 for full folder or 0 for single file and folder/file name w/ extension
# EXP: 'python Undistorter.py 1/0 Folder/File CameraCalibrationFilesDirectory'
##################################
# Authors: 
# Sermarini
# Kider
##################################

# TODO UPDATE TO TAKE THIRD ARGUMENT AS CALIBRATION FILES DIRECTORY

import sys
import os
import cv2
import numpy as np
import glob

def undistort(image_path, camera_calibration_dir):
    print("Undistorting  " + image_path + "...")
    # Import calibration data
    #mtx = np.load("Camera\\Calibration\\mtx.npy")
    #dist = np.load("Camera\\Calibration\\dist.npy")
    #revcs = np.load("Camera\\Calibration\\revcs.npy")
    #tvecs = np.load("Camera\\Calibration\\tvecs.npy")
    mtx = np.load(os.path.join(camera_calibration_dir, "mtx.npy"))
    dist = np.load(os.path.join(camera_calibration_dir, "dist.npy"))
    revcs = np.load(os.path.join(camera_calibration_dir, "revcs.npy"))
    tvecs = np.load(os.path.join(camera_calibration_dir, "tvecs.npy"))
    assert mtx.size != 0, "Error: mtx loaded empty. Maybe run CameraCalibration.py?"
    assert dist.size != 0, "Error: dist loaded empty. Maybe run CameraCalibration.py?"
    assert revcs.size != 0, "Error: revcs loaded empty. Maybe run CameraCalibration.py?"
    assert tvecs.size != 0, "Error: tvecs loaded empty. Maybe run CameraCalibration.py?"

    img = cv2.imread(image_path)
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
    # Save 
    #print("Creating " + image_name + "...")
    #undistorted_image = cv2.imwrite(image_name, dst)
    # Ouput
    image_path = image_path[:-4] + "_Undistorted.jpg"
    return dst, image_path


def save_undistort(dst, full_path):
    cv2.imwrite(full_path, dst)
    print(full_path, "saved!")

def main(argv):
    # Check inputs and initialize
    assert len(sys.argv) >= 3, "Error: Argument required for entire folder key (1 is yes, 0 is no), folder/file name, and camera calibration files directory"
    assert os.path.isdir(argv[2]), "Error: Folder " + argv[1] + " not found."
    # Full folder
    if argv[0] == "1":
        assert os.path.isdir(argv[1]), "Error: Folder " + argv[1] + " not found."
        #file_names = glob.glob(argv[1] + "\\*.jpg")
        file_names = glob.glob(os.path.join(argv[1], "*.jpg"))
        for file_name in file_names:
            if "_Undistorted" in file_name: # Don't undistort undistorted images. File explorer pain avoidance
                continue
            if "_Highlighted" in file_name: # Don't undistort highlighted images.
                continue
            #undistort(file_name, mtx, dist, revcs, tvecs)
            save_undistort(*undistort(file_name, argv[2]))
    # Individual file
    else:
        assert os.path.exists(argv[1]), "Error: File " + argv[1] + " not found."
        #undistort(argv[1], mtx, dist, revcs, tvecs)
        save_undistort(*undistort(argv[1], argv[2]))

if __name__=='__main__':
    main(sys.argv[1:])