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
import pandas as pd
from datetime import datetime
from datetime import timedelta
import csv

directory_path = "Subjects"
output_filename = "CongregatedProgressTrackers.csv"

def pull_metadata(metadata_str):
	data = metadata_str.strip()
	# Data
	date = data.split("-")[0]
	month = int(date.split("_")[0])
	day = int(date.split("_")[1])
	year = int(date.split("_")[2])
	return month, day, year	


def main(argv):
	subject_dirs = os.listdir(directory_path)
	# Remove non subject folders
	for i in range(len(subject_dirs) - 1, 0, -1):
		if not os.path.isdir(os.path.join(directory_path, subject_dirs[i])):
			subject_dirs.pop(i)
	if "53" in subject_dirs: # TEMPORARY - MUST FIX DATA
		subject_dirs.remove("53")
	if "Mihir" in subject_dirs: # Pilot test
		subject_dirs.remove("Mihir")
	if ".gitkeep" in subject_dirs: # Github management file
		subject_dirs.remove(".gitkeep") 
	if "PILOTS" in subject_dirs:
		subject_dirs.remove("PILOTS") # More pilot tests
	# Print debug log to console
	print("Subjects Directories: ")
	print(subject_dirs)
	# Iterate through each subject file
	subject_data = []
	for subject_dir in subject_dirs:
		file_found = False
		subject_path = os.path.join(directory_path, subject_dir)
		for file in os.listdir(subject_path):
			if "ProgressTracker_MANUAL" in file:
				# Build filename
				print(subject_dir, "-", file)
				pt_filename = os.path.join(subject_path, file)
				# Read metadata
				with open(pt_filename) as csvfile:
					reader = csv.reader(csvfile, delimiter=",")
					line = next(reader)
					metadata_timestamp = line[5]
					is_ar = (line[3] == "True")
					print(line[3])
				month, day, year = pull_metadata(metadata_timestamp) # read metadata
				print(is_ar)
				# Create timestamps of tasks
				df = pd.read_csv(pt_filename, skiprows=1)
				df['Completion'] = -1
				for index, row in df.iterrows():
					if not pd.isna(row['Completion_Hour']):
						hour = int(row['Completion_Hour'])
						minute = int(row['Completion_Minute'])
						second = int(row['Completion_Second'])
						microsecond = int(row['Completion_Microsecond'])
						df.at[index, 'Completion'] = datetime(year, month, day, hour, minute, second, microsecond)
				# Determine duration of tasks (timestamps)
				df['Duration'] = -1
				for index, row in df.iterrows():
					if index == 0:
						continue
					if row['Completion'] == -1:
						continue
					if df['Completion'].iloc[index - 1] == -1:
						df.at[index, 'Duration'] = row['Completion'] - df['Completion'].iloc[index - 2]
					else:
						df.at[index, 'Duration'] = row['Completion'] - df['Completion'].iloc[index - 1]
				# Determine duration of tasks (seconds)
				df['Duration_Seconds'] = -1.0
				for index, row in df.iterrows():
					if df['Duration'].iloc[index] != -1:
						seconds = int(df['Duration'].iloc[index].seconds)
						microseconds = int(df['Duration'].iloc[index].microseconds) / 1000000.0
						duration_seconds = seconds + microseconds
						df.at[index, 'Duration_Seconds'] = duration_seconds
				# Melt and reform
				df_melted = pd.melt(df, id_vars=["Task_Name", "Task_ID"], value_vars="Duration_Seconds")
				df_melted = df_melted.rename(columns={"value" : "Duration"})
				df_melted = df_melted.drop('variable', axis=1)
				df_melted["Subject_ID"] = subject_dir
				df_melted["AR_Condition"] = is_ar
				# Add to mega list
				subject_data.append(df_melted)				
				break
	# Merge and output to .csv
	df_full = pd.concat(subject_data)
	output_path = os.path.join(directory_path, output_filename)#"Outputs\\" + output_filename
	print("Creating " + output_path + "...")
	df_full.to_csv(output_path)
	print(output_path + " succesfully created!")


if __name__ == "__main__":
	main(sys.argv[1:])