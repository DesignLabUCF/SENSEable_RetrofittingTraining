##################################
#   Experiment Progress Tracker  #
#     SENSEable Design Lab       #
##################################
# v1.0
# 2/11/2021
##################################
# Pass in AR if AR, nothing or anything else if not AR
# EXP: 'python ProgressTracker.py AR'
##################################
# Authors: 
# Sermarini
##################################

import sys
import os
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import csv

# Global vars
is_ar = None
save_text = None
# Scripts params
TIME_FORMAT = "%m_%d_%Y-%H_%M_%S_%f"
DEFAULT_DATETIME = None
# Tasks
camera_after_these_tasks = ["4b", "6", "8", "11"]
tasks = [ \
["0a", "Headset is on", DEFAULT_DATETIME], \
["0b", "GUI training complete", DEFAULT_DATETIME], \
["1a", "Electric drill", DEFAULT_DATETIME], \
["1b", "Jab saw", DEFAULT_DATETIME], \
["1c", "Handheld screwdriver", DEFAULT_DATETIME], \
#["1d", "Pencil", DEFAULT_DATETIME], \
#["1e", "Ruler", DEFAULT_DATETIME], \
["1d", "Blue tape", DEFAULT_DATETIME], \
#["1e", "Hard hat", DEFAULT_DATETIME], \
["1e", "Gloves", DEFAULT_DATETIME], \
#["1g", "Glasses", DEFAULT_DATETIME], \
["1f", "Stud finder", DEFAULT_DATETIME], \
["2a", "Outlet and junction box", DEFAULT_DATETIME], \
["2b", "Mounting screws", DEFAULT_DATETIME], \
["2c", "Service panel", DEFAULT_DATETIME], \
["3", "Turn off power", DEFAULT_DATETIME], \
["4a", "Mark stud vertically", DEFAULT_DATETIME], \
["4b", "Mark the level", DEFAULT_DATETIME], \
["5", "Identify the corners", DEFAULT_DATETIME], \
["6", "Draw lines", DEFAULT_DATETIME], \
["7", "Drill guide holes", DEFAULT_DATETIME], \
["8", "Cut wall", DEFAULT_DATETIME], \
["9", "Identify the wire", DEFAULT_DATETIME], \
#["10", "Feed the wire", DEFAULT_DATETIME], \
["10", "Mark on stud side", DEFAULT_DATETIME], \
["11", "Drill fits", DEFAULT_DATETIME]]


def get_datetime(task):
	now = datetime.now()
	#now_formatted = now.strftime("%d/%m/%Y %H:%M:%S.%f")
	task[2] = now
	task[3].config(text = task[2])
	print(task[0] + " - " + task[1] + " - " + task[2].strftime("%m/%d/%Y %H:%M:%S.%f"))
	save_task_log(save_text.get("1.0","end-1c"), False)

def reset_task(task):
	task[2] = DEFAULT_DATETIME
	task[3].config(text = "")
	print("Resetting " + task[0] + " - " + task[1])
	save_task_log(save_text.get("1.0","end-1c"), False)

def save_task_log(subject_id, is_manual_save):
	# Get save type from input
	save_type = "MANUAL" if is_manual_save else "AUTO"
	print("Initiating " + save_type + " save.")
	# Check text box input of subject ID
	if subject_id == None or subject_id == "":
		messagebox.showerror('Error', 'Error: No subject ID inputted to top text box. Please enter an ID before saving. Save not complete.')
		print("ERROR: No subject ID inputted to top text box. Please enter an ID before saving. Save not complete.")
		return
	# Get directory and datetime info
	now = datetime.now()
	file_directory = "Subjects\\" + subject_id + "\\"
	#file_name = "ProgressTracker_" + now.strftime("%d_%m_%Y-%H_%M_%S_%f")
	file_name = "ProgressTracker_" + save_type + "_" + now.strftime(TIME_FORMAT)
	full_file = file_directory + file_name + ".csv"
	# If needed, create subject directory
	if not os.path.isdir(file_directory):
		print("Subject directory not found. " + file_directory + " created.")
		os.makedirs(file_directory)	
	# Create CSV
	print("Creating " + full_file + "...")
	with open(full_file, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		# Comments (Subject ID, condition, time of creation)
		writer.writerow([ \
			"Subject ID:",
			subject_id, 
			"Is AR:",
			str(is_ar),
			"Time of creation:",
			now.strftime(TIME_FORMAT)])
		# Headers
		writer.writerow([ \
			"Task_ID", \
			"Task_Name", \
			"Completion_Hour",
			"Completion_Minute",
			"Completion_Second",
			"Completion_Microsecond"])
		for i in range(0, len(tasks)):
			task_id = tasks[i][0]
			task_name = tasks[i][1]
			task_time = tasks[i][2]
			if task_time != None:
				task_hour = task_time.strftime("%H")
				task_minute = task_time.strftime("%M")
				task_second = task_time.strftime("%S")
				task_micro = task_time.strftime("%f")
			else:
				task_hour = ""
				task_minute = ""
				task_second = ""
				task_micro = ""
			writer.writerow([ \
				task_id, \
				task_name, \
				task_hour, \
				task_minute, \
				task_second, \
				task_micro])
	print(full_file + " generated!")

def main(argv):
	# Get global variables
	global save_text
	global is_ar
	# Check if AR component
	if len(argv) > 0 and "AR" in argv[0].upper():
		is_ar = True
		condition_label_text = "AR"
		print("Launching for condition: AR")
	else:
		is_ar = False
		condition_label_text = "Paper"
		print("Launching for condition: Paper")
	## Init
	window = Tk()
	## Configure GUI
	window.title("Experiment Progress Tracker")
	#window.geometry("1200x800")
	window.resizable(width=False, height=False)
	window.configure(background="white")
	window.wm_iconbitmap("icon.ico") # Icon (For classy reason, duh)
	# Create GUI frame
	frame = Frame(window)
	# Create GUI header row/save button
	save_label = Label(window, text="Subject ID: ")
	save_label.config(bg= "gold")
	save_label.grid(column=0, row=0, sticky=W)
	save_text = Text(window, height=1, width=10)
	save_text.config(bg= "gold")
	save_text.grid(column=1, row=0, sticky=W)
	save_button = Button(window, text="SAVE PROGRESS", command=lambda : save_task_log(save_text.get("1.0","end-1c"), True)) # x=task from https://stackoverflow.com/questions/4236182/generate-tkinter-buttons-dynamically
	save_button.grid(column=2, row=0, sticky=W)
	condition_label = Label(window, text=condition_label_text)
	condition_label.grid(column=3, row=0, sticky=W)
	# Create task grid buttons
	grid_inc = 1
	for task in tasks:
		# Skip non-relevant tasks
		if is_ar:
			if task[0] == "1f": # Stud finder
				continue
		else:
			if task[0] == "0a" or task[0] == "0b": # Headset on and GUI test
				continue
		# Text labels
		label_id = Label(window, text=task[0])
		label_id.grid(column=0, row=grid_inc, sticky=W)
		label_name = Label(window, text=task[1])
		label_name.grid(column=1, row=grid_inc, sticky=W)
		label_time = Label(window, text=task[2])
		label_time.grid(column=2, row=grid_inc, sticky=W)
		task.append(label_time)
		# Buttons for logging time
		datetime_button = Button(window, text="Log Time", command=lambda x=task : get_datetime(x)).grid(column=3, row=grid_inc, sticky=W) # x=task from https://stackoverflow.com/questions/4236182/generate-tkinter-buttons-dynamically
		reset_button = Button(window, text="Reset", command=lambda x=task : reset_task(x)).grid(column=4, row=grid_inc, sticky=W) # x=task from https://stackoverflow.com/questions/4236182/generate-tkinter-buttons-dynamically
		# Inc loop value
		grid_inc = grid_inc + 1
		# Add camera indicator
		if(task[0] in camera_after_these_tasks):
			label_photo = Label(window, text="Stop here for picture")
			label_photo.config(bg= "coral1")
			label_photo.grid(column=0, row=grid_inc, columnspan=5, sticky='ew')
			grid_inc = grid_inc + 1
	# Run GUI
	window.mainloop()

if __name__ == "__main__":
	main(sys.argv[1:])
