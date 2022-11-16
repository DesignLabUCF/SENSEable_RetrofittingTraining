##################################
#    Experiment Wall Estimator   #
#      SENSEable Design Lab      #
##################################
# v1.0
# 4/5/21
##################################
# EXP: 'python WallEstimator.py'
##################################
# Authors: 
# Sermarini
##################################

import sys
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Button as PltButton
from matplotlib.backend_bases import MouseButton
from math import sqrt
import csv
from tkinter import *
#from tkinter import messagebox


# Params
outlet_dimensions = (2.76, 4.5) # width (inch), height (inch)
outlet_pixel_positions = ((670, 742), (732, 840)) # top-left corner, bottom-right corner
wall_file = "wall.png"
tkinter_font = 'Times 20'
instructions_text = "Suppose you wish to install an electrical outlet on a wall within your home. You plan install the\noutlet at the position shown in the following image. How much of the wall would you need to cut into during the process? Click and drag the mouse on the image to draw a rectangle of the estimated cutout area.\n\nSelect the continue button below when you are ready to begin."
# Script variables
points = [] # [[x, y], [x, y], ....]
img = None
click_down = False
mouse_start = None # (x, y)
subject_name = ""
subject_dir = None
file_name = None
previous_rect = None
window_name = "Wall Cutout Estimator"
figure_ax = None
# Outputs
x1 = None
x2 = None
y1 = None
y2 = None
area_pix = None
area_inch = None
outlet_topleft_x = None
outlet_topleft_y = None
outlet_bottomright_x = None
outlet_bottomright_y = None
justification = ""


def get_rect(start, end):
	min_x = 10000000.0
	max_x = -1.0
	min_y = 10000000.0
	max_y = -1.0
	points = [start, end]
	for p in points:
		x = p[0]
		y = p[1]
		min_x = min(min_x, x)
		max_x = max(max_x, x)
		min_y = min(min_y, y)
		max_y = max(max_y, y)
	rectangle_origin = (min_x, max_y)
	height = min_y - max_y
	width = max_x - min_x
	return rectangle_origin, height, width

def draw_rect(mouse_start, mouse_end):
	global previous_rect
	if previous_rect != None:
		previous_rect.remove()
	# Plot rectange
	rect_origin, rect_height, rect_width = get_rect(mouse_start, mouse_end)
	rectangle = plt.Rectangle(
		rect_origin,
		rect_width, 
		rect_height, 
		fc='red',
		ec="red",
		alpha=0.25)
	previous_rect = rectangle
	figure_ax.add_patch(rectangle)
	# Show
	plt.show()	

def pixels_per_inch():
	# Area in pixels
	outlet_width_pix = outlet_pixel_positions[1][0] - outlet_pixel_positions[0][0]
	outlet_height_pix = outlet_pixel_positions[1][1] - outlet_pixel_positions[0][1]
	outlet_area_pix = outlet_width_pix * outlet_height_pix
	# Area in inches
	outlet_width_inch = outlet_dimensions[0]
	outlet_height_inch = outlet_dimensions[1]
	outlet_area_inch = outlet_width_inch * outlet_height_inch
	# Convert
	conv = outlet_area_pix / outlet_area_inch
	return conv

def log(mouse_start, mouse_end):
	global x1
	global x2
	global y1
	global y2
	global area_pix
	global area_inch
	global outlet_topleft_x
	global outlet_topleft_y
	global outlet_bottomright_x
	global outlet_bottomright_y
	# Get area in pixels
	rect_origin, rect_height, rect_width = get_rect(mouse_start, mouse_end)
	area_pix = abs(rect_width * rect_height)
	#print("Area (Pixels):", area_pix)
	# Get area in inches
	area_inch = area_pix / pixels_per_inch()
	#print("Area (Inch):", area_inch)
	#print("===========================")
	# Set variables for later output writing
	x1 = mouse_start[0]
	y1 = mouse_start[1]
	x2 = mouse_end[0]
	y2 = mouse_end[1]
	#area_pix =
	#area_inch = 
	outlet_topleft_x = outlet_pixel_positions[0][0]
	outlet_topleft_y = outlet_pixel_positions[0][1]
	outlet_bottomright_x = outlet_pixel_positions[1][0]
	outlet_bottomright_y = outlet_pixel_positions[1][1]

def on_click(event):
	#print("Click")
	global click_down
	global mouse_start
	x, y = event.xdata, event.ydata
	if x == None or y == None:
		return
	if not event.button is MouseButton.LEFT:
		return
	if x >= 1.0 and y >= 1.0: # Not on button (NOTE: re-do if button changes size)
		click_down = True
		mouse_start = (x, y)

def on_drag(event):
	#print("Drag")
	global click_down
	global mouse_start
	x, y = event.xdata, event.ydata	
	if click_down == False:
		return
	if x == None or y == None:
		click_down = False
		return
	if x >= 1.0 and y >= 1.0: # Not on button (NOTE: re-do if button changes size)
		mouse_end = (x, y)
		log(mouse_start, mouse_end)
		draw_rect(mouse_start, mouse_end)	

def on_release(event):
	#print("Release")
	global click_down
	global mouse_start
	x, y = event.xdata, event.ydata	
	if click_down == False:
		return
	if not event.button is MouseButton.LEFT:
		return
	#if mouse_start == (x, y):
	#	return
	if x >= 1.0 and y >= 1.0: # Not on button (NOTE: re-do if button changes size)
		click_down = False
		mouse_end = (x, y)
		if (x, y) != mouse_start: # Ensures the mouse was actually dragged
			log(mouse_start, mouse_end)
			draw_rect(mouse_start, mouse_end)

def get_topleft_of_screen(window):
	width = int(window.winfo_screenwidth() / 4.0)
	height = int(window.winfo_screenheight() / 2.0)
	#return "+" + str(width) + "+0"
	return "+0+0"

def get_id_window():
	# Init
	window = Tk()
	# Configure GUI
	window.title(window_name)
	window.resizable(width=False, height=False)
	window.configure(background="white")
	window.wm_iconbitmap("icon.ico") # Icon (For classy reason, duh)
	window.wm_geometry(get_topleft_of_screen(window)) # Put window on center of screen
	# Create GUI frame
	frame = Frame(window)
	id_label = Label(window, text="Please enter your ID number:", font=tkinter_font)
	id_label.pack(fill=BOTH)
	id_text = Text(window, height=1, width=10, font=tkinter_font)
	id_text.pack(fill=BOTH)
	id_text.focus()
	continue_button = Button(window, text="Continue", font=tkinter_font, command=lambda : finish_get_id(id_text.get("1.0","end-1c").strip(), window))
	continue_button.pack(fill=BOTH)
	# Run GUI
	window.mainloop()

def finish_get_id(subject_id_textbox_value, root_window):
	global subject_name
	global subject_dir
	global file_name
	# Ensure input is valud
	if subject_id_textbox_value == "":
		messagebox.showinfo("Error", "Error: Invalid Subject ID entered.")
		return
	# Assign filename values from textbox input
	subject_name = subject_id_textbox_value
	subject_dir = "Subjects//" + subject_name
	file_name = subject_dir + "//" + "SizeEstimation" + "_" + subject_name + "_" + ".csv"
	# Create directories for subject if needed
	#assert not os.path.isfile(file_name), "Error: File '" + file_name + "' already exists. Please delete it or double check subject name argument before restarting."
	if not os.path.isdir(subject_dir):
		print("Subject directory not found. " + subject_dir + " created.")
		os.makedirs(subject_dir)
	root_window.destroy()

def get_instructions_window():
	# Init
	window = Tk()
	# Configure GUI
	window.title(window_name)
	window.resizable(width=False, height=False)
	window.configure(background="white")
	window.wm_iconbitmap("icon.ico") # Icon (For classy reason, duh)
	window.wm_geometry(get_topleft_of_screen(window)) # Put window on center of screen
	# Create GUI frame
	frame = Frame(window)
	#label = Label(window, text="TEXT/nTEXT/nTEXT/nTEXT/nTEXT/n", font=tkinter_font)
	#label.pack(fill=BOTH)
	text = Text(window, font=tkinter_font)
	text.pack(fill=BOTH)
	text.insert("1.0", instructions_text)
	text['state'] = 'disabled'
	continue_button = Button(window, text="Continue", font=tkinter_font, command=lambda : window.destroy())
	continue_button.pack(fill=BOTH)
	# Run GUI
	window.mainloop()

def finish_drawing(event):
	plt.close()

def get_drawing_window():
	global figure_ax
	# Configure window
	mpl.rcParams['toolbar'] = 'None' # Remove toolbar at bottom
	fig = plt.figure(num=window_name, figsize=(10, 10))
	plt.get_current_fig_manager().window.wm_iconbitmap("icon.ico") # Icon
	plt.get_current_fig_manager().window.wm_geometry(get_topleft_of_screen(plt.get_current_fig_manager().window)) # Put window on center of screen
	fig.canvas.mpl_connect('button_press_event', on_click) # Add on-click event
	fig.canvas.mpl_connect('motion_notify_event', on_drag) # Add drag event
	fig.canvas.mpl_connect('button_release_event', on_release) # Add on-release event
	# Show image
	img_plot = plt.imshow(img)
	figure_ax = plt.gca() # Set axis for later drawing on
	# Continue button
	continue_button_pos = plt.axes([0.25, 0.02, 0.5, 0.05]) # https://stackoverflow.com/questions/47489873/button-positioning-in-axes-matplotlib
	continue_button = PltButton(continue_button_pos, "Continue")
	continue_button.on_clicked(finish_drawing)
	# Show PLT
	plt.show()

def get_justification_window():
	# Init
	window = Tk()
	# Configure GUI
	window.title(window_name)
	window.resizable(width=False, height=False)
	window.configure(background="white")
	window.wm_iconbitmap("icon.ico") # Icon (For classy reason, duh)
	window.wm_geometry(get_topleft_of_screen(window)) # Put window on center of screen
	# Create GUI frame
	frame = Frame(window)
	just_label = Label(window, text="Please explain your reasoning.", font=tkinter_font)
	just_label.pack(fill=BOTH)
	just_text = Text(window, font=tkinter_font)
	just_text.pack(fill=BOTH)
	just_text.focus()
	continue_button = Button(window, text="Continue", font=tkinter_font, command=lambda : finish_justification(just_text.get("1.0","end-1c").strip(), window))
	continue_button.pack(fill=BOTH)
	# Run GUI
	window.mainloop()

def finish_justification(justification_textbox_value, root_window):
	global justification
	# Ensure input is valud
	if justification_textbox_value == "":
		messagebox.showinfo("Error", "Error: Invalid text entered.")
		return
	justification = justification_textbox_value
	root_window.destroy()

def main(argv):
	global img
	global justification
	# Open image
	assert os.path.exists(wall_file), "Error: " + wall_file + " not found in Data directory."
	img = mpimg.imread(wall_file)
	### TKinter for instructions and text input
	while(subject_name == ""):
		get_id_window()
	print("Subject identified as:", subject_name)
	get_instructions_window()
	print("Instructions completed.")
	### Matplotlib for drawing
	while(x1 == None): # Loop if window closed prematurely
		get_drawing_window()
	print("Valid drawing dimensions recieved.")
	### TKinter for "why" text input
	while(justification == ""): # Loop if window closed prematurely
		get_justification_window()
	print("Valid justification recieved.")
	### Write output file
	justification = justification.replace("\n", " ") # Get rid of the newlines for csv
	justification = justification.strip()
	with open(file_name, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["SelectionCorner1_X", "SelectionCorner1_Y", "SelectionCorner2_X", "SelectionCorner2_Y", "Area_Pix", "Area_Inch", "OutletTopLeft_X", "OutletTopLeft_Y", "OutletBottomRight_X", "OutletBottomRight_Y", "Justification"])
		writer.writerow([x1, y1, x2, y2, str(area_pix), str(area_inch), outlet_topleft_x, outlet_topleft_y, outlet_bottomright_x, outlet_bottomright_y, justification])
		print(file_name + " created and populated.")

if __name__=='__main__':
	main(sys.argv[1:])
