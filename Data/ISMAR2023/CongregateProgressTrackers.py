##################################
#   Congregate Progress Tracker  #
#     SENSEable Design Lab       #
##################################
# v1.0
# 2/14/2023
##################################
# Pass in nothing
# EXP: 'python CongregateProgressTrackers.py'
##################################
# Authors: 
# Sermarini
##################################

import sys
import os
import re

directory_path = "..\\Subjects"

def main(argv):
	subject_dirs = os.listdir(directory_path)
	# Remove non subject folders
	for i in range(len(subject_dirs) - 1, 0, -1):
		if not os.path.isdir(os.path.join(directory_path, subject_dirs[i])):
			subject_dirs.pop(i)
	subject_dirs.remove("Mihir") # Pilot test
	subject_dirs.remove(".gitkeep") # Github management file
	# Print debug log to console
	print("Subjects Directories: ")
	print(subject_dirs)
	# Iterate through each subject file
	for subject_dir in subject_dirs:
		file_found = False
		subject_path = os.path.join(directory_path, subject_dir)
		for file in os.listdir(subject_path):
			if "ProgressTracker_MANUAL" in file:
				print(file)
				break


if __name__ == "__main__":
	main(sys.argv[1:])