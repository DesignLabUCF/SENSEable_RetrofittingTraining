##################################
#    Convert All Raw Pictures    #
#     SENSEable Design Lab       #
##################################
# v1.0
# 2/27/2023
##################################
# To run, navigate to Camera directory in cmd and run :)
# EXP: 'python ConvertAllRawPhotos.py'
##################################
# Authors: 
# Sermarini
##################################

import sys
import os
import glob
from NEFToJPG import convert_NEF, save_NEF
from Undistorter import undistort, save_undistort

directory_path = os.path.join("..", "Subjects")

def main(argv):
	subjects = os.listdir(directory_path)
	# Remove non subject folders
	for i in range(len(subjects) - 1, 0, -1):
		if not os.path.isdir(os.path.join(directory_path, subjects[i])):
			subjects.pop(i)
	if "PILOTS" in subjects: # Pilot test
		subjects.remove("PILOTS")
	if ".gitkeep" in subjects: # Github management file
		subjects.remove(".gitkeep")
	# Convert all photos
	for subject in subjects:
		subject_photos_path = os.path.join(directory_path, subject, "Photos") # Subject photos path
		raw_paths = glob.glob(os.path.join(subject_photos_path, "*.NEF")) # Raw photos
		# Create processed photo directories (if needed)
		processed_directory_path = os.path.join(subject_photos_path, "Processed")
		if not os.path.exists(processed_directory_path):
			print(processed_directory_path, "does not exist. Creating directory...")
			os.mkdir(processed_directory_path)
		# Convert photos and undistort
		for raw_path in raw_paths:
			# Convert to JPG and save
			rgb, processed_photo_path = convert_NEF(raw_path)
			processed_path_split = processed_photo_path.split(os.sep)
			processed_photo_filename = processed_path_split[len(processed_path_split) - 1] # Photo file name
			processed_photo_path = os.path.join(processed_directory_path, processed_photo_filename)
			save_NEF(rgb, processed_photo_path)
			# Undistort the JPG and save
			save_undistort(*undistort(processed_photo_path, "Calibration"))

if __name__=='__main__':
    main(sys.argv[1:])