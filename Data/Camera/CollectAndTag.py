##################################
#    Collect and Tag Photos      #
#     SENSEable Design Lab       #
##################################
# v1.0
# 2/27/2023
##################################
# To run, navigate to Camera directory and pass in arugments
# arg1: 1 for copy-paste all subjects photos to the directory here, 0 for no copy-paste'ing needed
# arg2: "all" for running size calculation on every subject's last image, any subject number for individuals, or range seperated by an '-'
# EXP: 'python CollectAndTag.py 0/1 all/subject_number/start-end'
##################################
# Authors: 
# Sermarini
##################################

'''
	Collect all undistorted subject folders into one space for quick analysis.
	Run area calculations and stud locators.
'''

import sys
import os
import glob
import shutil
import PerspectiveCorrection
import pandas as pd

directory_path = os.path.join("..", "Subjects")
output_file = os.path.join(directory_path, "CutoutAreas.csv")


def run_calc_for_subject(subject):
	print("Running perspective corrected area calculation for subject", subject)
	# Ensure subject's photos are availble to use
	subject_dir = os.path.join(directory_path, subject, "Photos", "Processed")
	if not os.path.isdir(subject_dir):
		print("Unable to continue.", subject_dir, "does not exist. Ensure correct subject ID is passed in.")
		return
	subject_photos = glob.glob(os.path.join(subject_dir, "*_Undistorted.jpg"))
	if len(subject_photos) == 0:
		print("Processed photos for subject", subject, "unable to be located. Ensure 'ConvertAllRawPhotos.py' has been run.")
		return
	# Run area calculation for the last subject photo, as it is the their final results.
	cutout_area_photo = subject_photos[len(subject_photos) - 1]
	areas = PerspectiveCorrection.calculate_area(cutout_area_photo)
	#areas = 200, 340 # DEBUG Test values
	update_csv(subject, areas[0], areas[1])


def update_csv(subject, area_pixels, area_inches):
	print("Updating", output_file, "for subject", subject, "with the following values:")
	print(area_pixels, "pixels")
	print(area_inches, "inches")
	# Create CSV if it doesn't exist
	if not os.path.isfile(output_file):
		print(output_file, "does not exist. Creating file...")
		data = {
			"Participant_ID" : [str(subject)], 
			"Cutout_Area_Pixels" : [str(area_pixels)],
			"Cutout_Area_Inches" : [str(area_inches)]
			}
		dataframe = pd.DataFrame(data)
		dataframe.to_csv(output_file, index=False)
		return
	# Update/Add new row
	dataframe = pd.read_csv(output_file)
	if int(subject) in dataframe["Participant_ID"].values:
		print("Subject", subject, "already in CSV. Updating stored values...")
		dataframe.loc[dataframe['Participant_ID'] == int(subject), "Cutout_Area_Pixels"] = area_pixels
		dataframe.loc[dataframe['Participant_ID'] == int(subject), "Cutout_Area_Inches"] = area_inches
	else:
		print("Adding new row to CSV file for subject", subject)
		dataframe.loc["Participant_ID"] = [subject, area_pixels, area_inches]
	# Save updates
	dataframe.to_csv(output_file, index=False)


def main(argv):
	# Check inputs
	assert len(argv) >= 2, "Error: Must pass in two arguments. See script header for details."
	assert argv[0] == "0" or argv[0] == "1", "Error: Argument One must be either '0' or '1'"
	should_copy = True if argv[0] == "1" else False
	run_all = True if argv[1].upper() == "ALL" else False

	subjects = os.listdir(directory_path)
	# Remove non subject folders
	for i in range(len(subjects) - 1, 0, -1):
		if not os.path.isdir(os.path.join(directory_path, subjects[i])):
			subjects.pop(i)
	if "PILOTS" in subjects: # Pilot test
		subjects.remove("PILOTS")
	if ".gitkeep" in subjects: # Github management file
		subjects.remove(".gitkeep")
	print("Subjects:")
	print(subjects)
	# Copy-paste all photos into centralized directory (if desired)
	if should_copy:
		for subject in subjects:
			subject_photos_path = os.path.join(directory_path, subject, "Photos", "Processed") # Subject photos path
			photo_paths = glob.glob(os.path.join(subject_photos_path, "*_Undistorted.jpg")) # Raw photos
			#print(subject)
			#print(subject_photos_path)
			#print(photo_paths)
			for photo_path in photo_paths:
				#print(photo_path)
				photo_filename = subject + "_" + photo_path.split(os.sep)[len(photo_path.split(os.sep)) - 1]
				#print(photo_filename)
				dst = os.path.join("CollectedSubjectPhotos", photo_filename)
				print("Copying", photo_path, "to", "CollectedSubjectPhotos")
				shutil.copy2(photo_path, dst)
	if run_all:
		for subject in subjects:
			run_calc_for_subject(subject)
	else:
		# Range
		if "-" in argv[1]:
			start_subject = argv[1].split("-")[0]
			end_subject = argv[1].split("-")[1]
			print(start_subject)
			print(end_subject)
			for subject in range(int(start_subject), (int(end_subject) + 1)):
				subject = str(subject)
				if len(subject) == 1:
					subject = "0" + subject
				run_calc_for_subject(subject)
		# Single subject
		else:
			subject = argv[1]
			if len(subject) == 1:
				subject = "0" + subject
			run_calc_for_subject(subject)

if __name__=='__main__':
    main(sys.argv[1:])