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
	wall_visible = ""
	wall_position = ""
	wall_rotation = ""
	gaze_status = ""
	gaze_valid = ""
	gaze_origin = ""
	gaze_direction = ""
	# Menu pin data
	menu_pinned = ""
	menu_position = ""
	menu_rotation = ""
	menu_scale = ""
	menu_visible = ""

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
		wall_visible = ""
		wall_position = ""
		wall_rotation = ""
		gaze_status = ""
		gaze_valid = ""
		gaze_origin = ""
		gaze_direction = ""
		# Menu pin data
		menu_pinned = ""
		menu_position = ""
		menu_rotation = ""
		menu_scale = ""
		menu_visible = ""

	def __init__(self, event_type):
		self.event_type = event_type


#file_name = "TestData_July192021"


def main():
	print("Opening file: " + sys.argv[1] + ".txt")

	event_parse_started = False
	read_event_name = False
	read_current = False
	read_timestamp = False
	read_task_name = False
	read_task_number = False
	read_head_position = False
	read_head_rotation = False
	read_wall_visible = False
	read_wall_position = False
	read_wall_rotation = False
	read_gaze_status = False
	read_gaze_valid = False
	read_gaze_origin = False
	read_gaze_direction = False
	read_menu_pinned = False
	read_menu_position = False
	read_menu_rotation = False
	read_menu_scale = False
	read_menu_visible = False

	event_list = []
	log_event = None

	try:
		#log = open(file_name + ".log")
		log = open(sys.argv[1] + ".txt")
		print("Parsing file...")

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
			elif read_wall_visible:
				read_wall_visible = False
				log_event.wall_visible = line
			elif read_wall_position:
				read_wall_position = False
				log_event.wall_position = line
			elif read_wall_rotation:
				read_wall_rotation = False
				log_event.wall_rotation = line
			elif read_gaze_status:
				read_gaze_status = False
				log_event.gaze_status = line
			elif read_gaze_valid:
				read_gaze_valid = False
				log_event.gaze_valid = line
			elif read_gaze_origin:
				read_gaze_origin = False
				log_event.gaze_origin = line
			elif read_gaze_direction:
				read_gaze_direction = False
				log_event.gaze_direction = line
			elif read_menu_pinned:
				read_menu_pinned = False
				log_event.menu_pinned = line
			elif read_menu_position:
				read_menu_position = False
				log_event.menu_position = line
			elif read_menu_rotation:
				read_menu_rotation = False
				log_event.menu_rotation = line
			elif read_menu_scale:
				read_menu_scale = False
				log_event.menu_scale = line
			elif read_menu_visible:
				read_menu_visible = False
				log_event.menu_visible = line

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
			elif "Wall_Visible:" == line and event_parse_started:
				read_wall_visible = True
			elif "Wall_Position:" == line and event_parse_started:
				read_wall_position = True
			elif "Wall_Rotation:" == line and event_parse_started:
				read_wall_rotation = True
			elif "Gaze_Status:" == line and event_parse_started:
				read_gaze_status = True
			elif "Gaze_Valid:" == line and event_parse_started:
				read_gaze_valid = True
			elif "Gaze_Origin:" == line and event_parse_started:
				read_gaze_origin = True
			elif "Gaze_Direction:" == line and event_parse_started:
				read_gaze_direction = True
			elif "Menu_Pinned:" == line and event_parse_started:
				read_menu_pinned = True
			elif "Menu_Position:" == line and event_parse_started:
				read_menu_position = True
			elif "Menu_Rotation:" == line and event_parse_started:
				read_menu_rotation = True
			elif "Menu_Scale:" == line and event_parse_started:
				read_menu_scale = True
			elif "Menu_Visible:" == line and event_parse_started:
				read_menu_visible = True
	except Exception as e:
			raise e

	print("Parsing complete.")
	print("Creating output file: " + sys.argv[1] + ".csv")

	with open(sys.argv[1] + ".csv", 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		print("Writing to file...")
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
			"Wall_Visible", \
			"Wall_Position_X", \
			"Wall_Position_Y", \
			"Wall_Position_Z", \
			"Wall_Rotation_X", \
			"Wall_Rotation_Y", \
			"Wall_Rotation_Z", \
			"Gaze_Status", \
			"Gaze_Valid", \
			"Gaze_Origin_X", \
			"Gaze_Origin_Y", \
			"Gaze_Origin_Z", \
			"Gaze_Direction_X", \
			"Gaze_Direction_Y", \
			"Gaze_Direction_Z", \
			"Menu_Position_X", \
			"Menu_Position_Y", \
			"Menu_Position_Z", \
			"Menu_Rotation_X", \
			"Menu_Rotation_Y", \
			"Menu_Rotation_Z", \
			"Menu_Scale_X", \
			"Menu_Scale_Y", \
			"Menu_Scale_Z", \
			"Menu_Visible"])
		for i in range(0, len(event_list)):
			log_event = event_list[i]
			head_pos_x, head_pos_y, head_pos_z = parse_xyz_from_line(log_event.head_position)
			head_rot_x, head_rot_y, head_rot_z = parse_xyz_from_line(log_event.head_rotation)
			wall_pos_x, wall_pos_y, wall_pos_z = parse_xyz_from_line(log_event.wall_position)
			wall_rot_x, wall_rot_y, wall_rot_z = parse_xyz_from_line(log_event.wall_rotation)
			gaze_origin_rot_x, gaze_origin_rot_y, gaze_origin_rot_z = parse_xyz_from_line(log_event.gaze_origin)
			gaze_direction_rot_x, gaze_direction_rot_y, gaze_direction_rot_z = parse_xyz_from_line(log_event.gaze_direction)
			menu_pos_x, menu_pos_y, menu_pos_z = parse_xyz_from_line(log_event.menu_position)
			menu_rot_x, menu_rot_y, menu_rot_z = parse_xyz_from_line(log_event.menu_rotation)
			menu_scale_x, menu_scale_y, menu_scale_z = parse_xyz_from_line(log_event.menu_scale)
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
				log_event.wall_visible, \
				wall_pos_x, \
				wall_pos_y, \
				wall_pos_z, \
				wall_rot_x, \
				wall_rot_y, \
				wall_rot_z, \
				log_event.gaze_status, \
				log_event.gaze_valid, \
				gaze_origin_rot_x, \
				gaze_origin_rot_y, \
				gaze_origin_rot_z, \
				gaze_direction_rot_x, \
				gaze_direction_rot_y, \
				gaze_direction_rot_z, \
				menu_pos_x, \
				menu_pos_y, \
				menu_pos_z, \
				menu_rot_x, \
				menu_rot_y, \
				menu_rot_z, \
				menu_scale_x, \
				menu_scale_y, \
				menu_scale_z, \
				log_event.menu_visible])
	print("Output file succesfully generated!")

#(0.053, -0.007, -0.030)
def parse_xyz_from_line(line):
	if line == "":
		return None, None, None
	s = line.split(",")
	x = s[0][1:].strip() # remove '('
	y = s[1].strip()
	z = s[2].strip()[:-1].strip() # remove ')' and any potential spaces
	return float(x), float(y), float(z)

if __name__ == "__main__":
	main()