##################################
#    Retrofitting Log Parser     #
#     SENSEable Design Lab       #
##################################
# v1.0
# 8/04/2021
##################################
# To run, pass in .log file name (without extension) as first cmd argument
# EXP: 'python RetrofittingParser.py TestData_July202021'
##################################


import sys
import csv


class LogEvent:
	# Universal
	event_type = ""
	current_time = ""
	timestamp = ""
	# Task data
	task_name = ""
	task_number = ""
	# Head data
	head_position = ""
	head_rotation = ""
	facade_position = ""
	facade_rotation = ""
	gaze_valid = ""
	gaze_origin = ""
	gaze_direction = ""
	gaze_confidence = ""
	# Layer data
	wires = ""
	pipes = ""
	studs = ""
	# Menu pin data
	menu_name = ""
	menu_pinned = ""

	def reset(self):
		# Universal
		event_type = ""
		current_time = ""
		timestamp = ""
		# Task data
		task_name = ""
		task_number = ""
		# Head data
		head_position = ""
		head_rotation = ""
		facade_position = ""
		facade_rotation = ""
		gaze_valid = ""
		gaze_origin = ""
		gaze_direction = ""
		gaze_confidence = ""
		# Layer data
		wires = ""
		pipes = ""
		studs = ""
		# Menu pin data
		menu_name = ""
		menu_pinned = ""

	def __init__(self, event_type):
		self.event_type = event_type


#file_name = "TestData_July192021"


def main():
	event_parse_started = False
	read_event_name = False
	read_current = False
	read_timestamp = False
	read_task_name = False
	read_task_number = False
	read_head_position = False
	read_head_rotation = False
	read_facade_position = False
	read_facade_rotation = False
	read_gaze_valid = False
	read_gaze_origin = False
	read_gaze_direction = False
	read_gaze_confidence = False
	read_wires = False
	read_pipes = False
	read_studs = False
	read_menu_name = False
	read_menu_pinned = False

	event_list = []
	log_event = None

	try:
		#log = open(file_name + ".log")
		log = open(sys.argv[1] + ".log")
		for line in log:
			line = line.strip()
			# Read in data
			if read_event_name:
				read_event_name = False
				log_event = LogEvent(line)
			elif read_current:
				read_current = False
				log_event.current_time = line
			elif read_timestamp:
				read_timestamp = False
				log_event.timestamp = line
			elif read_task_name:
				read_task_name = False
				log_event.task_name = line
			elif read_task_number:
				read_task_number = False
				log_event.task_number = line
			elif read_head_position:
				read_head_position = False
				log_event.head_position = line
			elif read_head_rotation:
				read_head_rotation = False
				log_event.head_rotation = line
			elif read_facade_position:
				read_facade_position = False
				log_event.facade_position = line
			elif read_facade_rotation:
				read_facade_rotation = False
				log_event.facade_rotation = line
			elif read_gaze_valid:
				read_gaze_valid = False
				log_event.gaze_valid = line
			elif read_gaze_origin:
				read_gaze_origin = False
				log_event.gaze_origin = line
			elif read_gaze_direction:
				read_gaze_direction = False
				log_event.gaze_direction = line
			elif read_gaze_confidence:
				read_gaze_confidence = False
				log_event.gaze_confidence = line
			elif read_wires:
				read_wires = False
				log_event.wires = line
			elif read_pipes:
				read_pipes = False
				log_event.pipes = line
			elif read_studs:
				read_studs = False
				log_event.studs = line
			elif read_menu_name:
				read_menu_name = False
				log_event.menu_name = line
			elif read_menu_pinned:
				read_menu_pinned = False
				log_event.menu_pinned = line

			# Determine what type of data the next line is
			elif "====================" in line: # Start or end of event
				if not event_parse_started:
					#print("Start of event parse")
					event_parse_started = True
					read_event_name = True
				else:
					#print("End of event parse") #TODO set event data in array and reset all
					event_parse_started = False
					event_list.append(log_event)
					log_event.reset()
			elif "Current:" == line and event_parse_started:
				read_current = True
			elif "Timestamp:" == line and event_parse_started:
				read_timestamp = True
			elif "Task_Name:" == line and event_parse_started:
				read_task_name = True
			elif "Task_Number:" == line and event_parse_started:
				read_task_number = True
			elif "Head_Position:" == line and event_parse_started:
				read_head_position = True
			elif "Head_Rotation:" == line and event_parse_started:
				read_head_rotation = True
			elif "Facade_Position:" == line and event_parse_started:
				read_facade_position = True
			elif "Facade_Rotation:" == line and event_parse_started:
				read_facade_rotation = True
			elif "Gaze_Valid:" == line and event_parse_started:
				read_gaze_valid = True
			elif "Gaze_Origin:" == line and event_parse_started:
				read_gaze_origin = True
			elif "Gaze_Direction:" == line and event_parse_started:
				read_gaze_direction = True
			elif "Gaze_Confidence:" == line and event_parse_started:
				read_gaze_confidence = True
			elif "Wires:" == line and event_parse_started:
				read_wires = True
			elif "Pipes:" == line and event_parse_started:
				read_pipes = True
			elif "Studs:" == line and event_parse_started:
				read_studs = True
			elif "Menu_Name:" == line and event_parse_started:
				read_menu_name = True
			elif "Menu_Pinned:" == line and event_parse_started:
				read_menu_pinned = True
	except Exception as e:
			raise e

	with open(sys.argv[1] + ".csv", 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["Type", \
			"Current", \
			"Timestamp", \
			"Task_Name", \
			"Task_Number", \
			"Head_Position_X", \
			"Head_Position_Y", \
			"Head_Position_Z", \
			"Head_Rotation_X", \
			"Head_Rotation_Y", \
			"Head_Rotation_Z", \
			"Facade_Position_X", \
			"Facade_Position_Y", \
			"Facade_Position_Z", \
			"Facade_Rotation_X", \
			"Facade_Rotation_Y", \
			"Facade_Rotation_Z", \
			"Gaze_Valid", \
			"Gaze_Origin_X", \
			"Gaze_Origin_Y", \
			"Gaze_Origin_Z", \
			"Gaze_Direction_X", \
			"Gaze_Direction_Y", \
			"Gaze_Direction_Z", \
			"Gaze_Confidence", \
			"Wires", \
			"Pipes", \
			"Studs", \
			"Menu_Name", \
			"Menu_Pinned"])
		for i in range(0, len(event_list)):
			log_event = event_list[i]
			head_pos_x, head_pos_y, head_pos_z = parse_xyz_from_line(log_event.head_position)
			head_rot_x, head_rot_y, head_rot_z = parse_xyz_from_line(log_event.head_rotation)
			facade_pos_x, facade_pos_y, facade_pos_z = parse_xyz_from_line(log_event.facade_position)
			facade_rot_x, facade_rot_y, facade_rot_z = parse_xyz_from_line(log_event.facade_rotation)
			gaze_origin_rot_x, gaze_origin_rot_y, gaze_origin_rot_z = parse_xyz_from_line(log_event.gaze_origin)
			gaze_direction_rot_x, gaze_direction_rot_y, gaze_direction_rot_z = parse_xyz_from_line(log_event.gaze_direction)
			writer.writerow([log_event.event_type, \
				log_event.current_time, \
				log_event.timestamp, \
				log_event.task_name, \
				log_event.task_number, \
				head_pos_x, \
				head_pos_y, \
				head_pos_z, \
				head_rot_x, \
				head_rot_y, \
				head_rot_z, \
				facade_pos_x, \
				facade_pos_y, \
				facade_pos_z, \
				facade_rot_x, \
				facade_rot_y, \
				facade_rot_z, \
				log_event.gaze_valid, \
				gaze_origin_rot_x, \
				gaze_origin_rot_y, \
				gaze_origin_rot_z, \
				gaze_direction_rot_x, \
				gaze_direction_rot_y, \
				gaze_direction_rot_z, \
				log_event.gaze_confidence, \
				log_event.wires, \
				log_event.pipes, \
				log_event.studs, \
				log_event.menu_name, \
				log_event.menu_pinned])


#X=76.408 Y=319.696 Z=150.947
#P=-10.223447 Y=-113.999596 R=-1.140259
def parse_xyz_from_line(line):
	if line == "":
		return "", "", ""
	s = line.split("=")
	x = s[1][:-2] # remove " Y"
	y = s[2][:-2] # remove " Z"/" R"
	z = s[3].strip()
	return x, y, z

if __name__ == "__main__":
	main()