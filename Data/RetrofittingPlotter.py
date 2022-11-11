##################################
#     Retrofitting Plotter       #
#     SENSEable Design Lab       #
##################################
# v1.0
# 8/04/2021
##################################
# To run, pass in .csv file name (without extension) as first cmd argument
# EXP: 'python RetrofittingPlotter.py TestData_July202021'
##################################

# Color palettes
# https://matplotlib.org/stable/tutorials/colors/colormaps.html

# Head Rotations:
# Straight down: x = -90.0
# Straight up:   x = 90.0
# Clockwise:     y = 0 to 179.9 then -179.9 to 0
# Tilt Left:     z = 0 to -90
# Tilt Right:    z = 0 to 90

# Eye Rotations:
#



import sys
import pandas as pd
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import math
#import numpy as np
from matplotlib.widgets import RangeSlider


#flip_x_axis = True
plot_head_positions = True
plot_head_positions_line = True
plot_arrows = True
plot_facade = True
plot_eyes = True
head_color = "red"
eye_color = "blue"
structure_color = "green"


def main():
	filename = sys.argv[1]
	try:
		# Read in all data from previously generated .csv
		df = pd.read_csv(filename + ".csv")
		""" ## ACTUALLY MAYBE NOT LOL ##
		# Swap column names because Unreal Y = Matplotlib Z
		df = swap_column_name(df, "Head_Position_Y", "Head_Position_Z")
		df = swap_column_name(df, "Head_Rotation_Y", "Head_Rotation_Z")
		df = swap_column_name(df, "Facade_Position_Y", "Facade_Position_Z")
		df = swap_column_name(df, "Facade_Rotation_Y", "Facade_Rotation_Z")
		"""
		# Get only head positional data
		head_data = df[df["Type"]=="Head"]
		head_data = head_data.iloc[1:] # Drop 1st row, is bum data
		# Add index column
		head_data["Index"] = np.arange(0, head_data.shape[0])

		fig = plt.figure()
		ax = plt.axes(projection="3d")
		# Facade
		if plot_facade:
			cube_x = head_data.iloc[head_data.shape[0] - 1]["Facade_Position_X"]
			cube_y = head_data.iloc[head_data.shape[0] - 1]["Facade_Position_Y"] 
			cube_z = head_data.iloc[head_data.shape[0] - 1]["Facade_Position_Z"]
			facade_rotation_angle = head_data.iloc[head_data.shape[0] - 1]["Facade_Rotation_Y"]
			# Conference room - Pos 1
			cube_dx = 152.4 # TODO VERIFY
			cube_dy = -10.0
			cube_dz = 118.3 # TODO VERIFY
			# TODO other position/room combos
			p_facade = plot_linear_cube(ax, cube_x, cube_y, cube_z, cube_dx, cube_dy, cube_dz, facade_rotation_angle)
		# Head position points
		if plot_head_positions:
			p_head_positions = plot_positions(ax, head_data)
		# Time line
		if plot_head_positions_line:
			p_time_line = plot_time_line(ax, head_data)
		# Head direction arrows - https://stackoverflow.com/questions/11140163/plotting-a-3d-cube-a-sphere-and-a-vector-in-matplotlib
		if plot_arrows:
			p_head_rotations = plot_head_rotations(ax, head_data)
		# Gaze
		if plot_eyes:
			p_eyes = plot_eyes(ax, head_data)

		# Axes
		# X axis
		x_axis_current = [min(head_data["Head_Position_X"]), max(head_data["Head_Position_X"])]
		x_axis_current[0] = x_axis_current[0] - 1.0 # Account for potential of no movement along this axis in desktop variant
		x_axis_current[1] = x_axis_current[1] + 1.0 # Account for potential of no movement along this axis in desktop variant
		x_axis_label = "X axis"
		# Y axis
		y_axis_current = [min(head_data["Head_Position_Y"]), max(head_data["Head_Position_Y"])]
		y_axis_current[0] = y_axis_current[0] - 1.0 # Account for potential of no movement along this axis in desktop variant
		y_axis_current[1] = y_axis_current[1] + 1.0 # Account for potential of no movement along this axis in desktop variant
		y_axis_label = "Y axis"
		# Z axis
		z_axis_current = [min(head_data["Head_Position_Z"]), max(head_data["Head_Position_Z"])]
		z_axis_current[0] = z_axis_current[0] - 1.0 # Account for potential of no movement along this axis in desktop variant
		z_axis_current[1] = z_axis_current[1] + 1.0 # Account for potential of no movement along this axis in desktop variant
		z_axis_label = "Z axis"
		# Labels
		ax.set_xlabel(x_axis_label)
		ax.set_ylabel(y_axis_label)
		ax.set_zlabel(z_axis_label)
		# Limits
		ax.set_xlim3d(x_axis_current[1], x_axis_current[0]) # FLIPPED
		ax.set_ylim3d(y_axis_current[0], y_axis_current[1])
		ax.set_zlim3d(z_axis_current[0], z_axis_current[1])

		# Add sliders
		slider_color = 'red'
		slider_height = 0.015
		slider_ax_x = plt.axes([0.20, 0.06, 0.60, slider_height]) #([left, bottom, width, height])
		x_slider = RangeSlider(
			slider_ax_x,
			"X Axis", 
			min(head_data["Head_Position_X"]), 
			max(head_data["Head_Position_X"]), 
			valinit = (x_axis_current[0], x_axis_current[1]),
			color = slider_color)
		slider_ax_y = plt.axes([0.20, 0.04, 0.60, slider_height])
		y_slider = RangeSlider(
			slider_ax_y, 
			"Y Axis", 
			min(head_data["Head_Position_Y"]), 
			max(head_data["Head_Position_Y"]), 
			valinit = (y_axis_current[0], y_axis_current[1]),
			color = slider_color)
		slider_ax_z = plt.axes([0.20, 0.02, 0.60, slider_height])
		z_slider = RangeSlider(
			slider_ax_z, 
			"Z Axis", 
			min(head_data["Head_Position_Z"]), 
			max(head_data["Head_Position_Z"]), 
			valinit = (z_axis_current[0], z_axis_current[1]),
			color = slider_color)
		slider_ax_points = plt.axes([0.20, 0.08, 0.60, slider_height])
		points_slider = RangeSlider(
			slider_ax_points, 
			"Points", 
			0, 
			len(head_data),
			valstep = 1.0, 
			valinit = (0, len(head_data)),
			color = slider_color)
		def update_x(val):
			x_axis_current[0] = val[0]
			x_axis_current[1] = val[1]
			x_axis_current[0] = x_axis_current[0] - 1.0 # Account for potential of no movement along this axis in desktop variant
			x_axis_current[1] = x_axis_current[1] + 1.0 # Account for potential of no movement along this axis in desktop variant
			ax.set_xlim3d(val[1], val[0]) # FLIPPED
			fig.canvas.draw_idle()
		x_slider.on_changed(update_x)
		def update_y(val):
			y_axis_current[0] = val[0]
			y_axis_current[1] = val[1]
			y_axis_current[0] = y_axis_current[0] - 1.0 # Account for potential of no movement along this axis in desktop variant
			y_axis_current[1] = y_axis_current[1] + 1.0 # Account for potential of no movement along this axis in desktop variant
			ax.set_ylim3d(val[0], val[1])
			fig.canvas.draw_idle()
		y_slider.on_changed(update_y)
		def update_z(val):
			z_axis_current[0] = val[0]
			z_axis_current[1] = val[1]
			z_axis_current[0] = z_axis_current[0] - 1.0 # Account for potential of no movement along this axis in desktop variant
			z_axis_current[1] = z_axis_current[1] + 1.0 # Account for potential of no movement along this axis in desktop variant
			ax.set_zlim3d(val[0], val[1])
			fig.canvas.draw_idle()
		z_slider.on_changed(update_z)
		def update_points(val):
			# Remove current plots
			ax.cla()
			# Get interesting points from data and plot
			selected_data = head_data[(head_data["Index"] >= val[0]) & (head_data["Index"] <= val[1])]
			if plot_facade:
				plot_linear_cube(ax, cube_x, cube_y, cube_z, cube_dx, cube_dy, cube_dz, facade_rotation_angle)
			if plot_head_positions:
				plot_positions(ax, selected_data)
			if plot_head_positions_line:
				plot_time_line(ax, selected_data)
			if plot_arrows:
				plot_head_rotations(ax, selected_data)
			if plot_eyes:
				plot_eyes(ax, selected_data)
			# Redraw axes and update
			ax.set_xlabel(x_axis_label)
			ax.set_ylabel(y_axis_label)
			ax.set_zlabel(z_axis_label)
			#ax.set_xlim3d(x_axis_current[0], x_axis_current[1])
			ax.set_xlim3d(x_axis_current[1], x_axis_current[0]) # FLIPPED
			ax.set_ylim3d(y_axis_current[0], y_axis_current[1])
			ax.set_zlim3d(z_axis_current[0], z_axis_current[1])
			fig.canvas.draw_idle()
		points_slider.on_changed(update_points)


		# Show plot/print debug info
		DEBUG_print_xyz(
			head_data.iloc[0]["Head_Position_X"],
			head_data.iloc[0]["Head_Position_Y"],
			head_data.iloc[0]["Head_Position_Z"],
			"Initial position")
		DEBUG_print_xyz(
			head_data.iloc[head_data.shape[0] - 1]["Head_Position_X"],
			head_data.iloc[head_data.shape[0] - 1]["Head_Position_Y"],
			head_data.iloc[head_data.shape[0] - 1]["Head_Position_Z"],
			"Final position")
		plt.show()

	except Exception as e:
			raise e


def plot_linear_cube(ax, facade_x, facade_y, facade_z, dx, dy, dz, angle):
	cube_vertices = [
	#[1.0, 1.0, 0],
	[1.0, 0, 0],
	[0, 0, 0],
	#[0, 1.0, 0],
	#[1.0, 1.0, 1.0],
	[1.0, 0, 1.0],
	[0, 0, 1.0],
	#[0, 1.0, 1.0]
	]

	for i in range(0, len(cube_vertices)):
		cube_vertices[i] = scale_coord(
			cube_vertices[i][0],
			cube_vertices[i][1],
			cube_vertices[i][2], 
			dx, 
			dy, 
			dz)
		cube_vertices[i] = rotate_coord_around_z(
			cube_vertices[i][0],
			cube_vertices[i][1],
			cube_vertices[i][2], 
			angle)
		cube_vertices[i] = translate_coord(
			cube_vertices[i][0],
			cube_vertices[i][1],
			cube_vertices[i][2],
			facade_x, 
			facade_y, 
			facade_z)

	x = []
	y = []
	z = []
	for i in range(0, len(cube_vertices)):
		x.append(cube_vertices[i][0])
		y.append(cube_vertices[i][1])
		z.append(cube_vertices[i][2])

	x, z = np.meshgrid(x, z)
	ax.plot_wireframe(
		x,
		y,
		z, 
		linewidth=2, 
		antialiased=True,
		color=structure_color)

	return ax


def plot_positions(ax, head_data):
	p = ax.scatter3D(
		head_data["Head_Position_X"],
		head_data["Head_Position_Y"],
		head_data["Head_Position_Z"],
		cmap = "Blues",
		c = head_data["Index"], 
		alpha = 1.0,
		s = 2.0)
	return p


def plot_time_line(ax, head_data):
	p = ax.plot3D(
		head_data["Head_Position_X"],
		head_data["Head_Position_Y"],
		head_data["Head_Position_Z"],
		c = "grey", 
		alpha = 0.5)
	return p


def plot_head_rotations(ax, head_data):
	# Convert up and down from [90 degrees, -90 degrees] to [0, 180] degrees in radians
	# Straight down: x = -90.0
	# Straight up:   x = 90.0
	alpha = head_data["Head_Rotation_X"].map(lambda x: 90.0 - x if x > 0.0 else abs(x) + 90.0)
	alpha = alpha.map(lambda x: math.radians(x))
	# Convert clockwise turning from [-180 degrees, 180 degrees] to [0, 180] degrees in radians
	# Clockwise:     y = 0 to 179.9 then -179.9 to 0
	theta = head_data["Head_Rotation_Y"].map(lambda x: (x + 360.0) % 360.0 if x < 0.0 else x)
	theta = theta.map(lambda x: math.radians(x))
	p = 1.0
	# Credit: https://mathinsight.org/spherical_coordinates
	arrow_x = p * np.sin(alpha) * np.cos(theta)
	arrow_y = p * np.sin(alpha) * np.sin(theta)
	arrow_z = p * np.cos(alpha)

	p = ax.quiver(
		head_data["Head_Position_X"], 
		head_data["Head_Position_Y"],
		head_data["Head_Position_Z"], 
		arrow_x,
		arrow_y,
		arrow_z,
		length = 10.0,
		pivot = "tail",
		normalize = True,
		arrow_length_ratio = 0.4,
		color = head_color)

	return p

# Gaze_Direction_X
def plot_eyes(ax, head_data):
	head_data = head_data[head_data.Gaze_Valid == True] # Remove invalid eye readings

	arrow_x = head_data["Gaze_Direction_X"]
	arrow_y = head_data["Gaze_Direction_Y"]
	arrow_z = head_data["Gaze_Direction_Z"]

	p = ax.quiver(
		head_data["Head_Position_X"], 
		head_data["Head_Position_Y"],
		head_data["Head_Position_Z"], 
		arrow_x,
		arrow_y,
		arrow_z,
		length = 10.0,
		pivot = "tail",
		normalize = True,
		arrow_length_ratio = 0.4,
		color = eye_color)

	return p


# Credit: https://www.cs.cornell.edu/courses/cs4620/2010fa/lectures/03transforms3d.pdf
def rotate_coord_around_z(x, y, z, angle):
	#numpy.matmul(x1, x2)
	rot = np.matmul(
		[
		[math.cos(math.radians(angle)), -math.sin(math.radians(angle)), 0, 0],
		[math.sin(math.radians(angle)), math.cos(math.radians(angle)), 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
		], 
		[x, y, z, 1])
	x1 = rot[0]
	y1 = rot[1]
	z1 = rot[2]
	return x1, y1, z1


def translate_coord(x, y, z, dx, dy, dz):
	trans = np.matmul(
		[
		[1, 0, 0, dx],
		[0, 1, 0, dy],
		[0, 0, 1, dz],
		[0, 0, 0, 1]
		], 
		[x, y, z, 1])
	x1 = trans[0]
	y1 = trans[1]
	z1 = trans[2]
	return x1, y1, z1


def scale_coord(x, y, z, dx, dy, dz):
	scale = np.matmul(
		[
		[dx, 0, 0, 0],
		[0, dy, 0, 0],
		[0, 0, dz, 0],
		[0, 0, 0, 1]
		], 
		[x, y, z, 1])
	x1 = scale[0]
	y1 = scale[1]
	z1 = scale[2]
	return x1, y1, z1


# Credit: https://stackoverflow.com/questions/11346283/renaming-column-names-in-pandas
def swap_column_name(df, a, b):
	df.columns = df.columns.str.replace(a, 'REPLACE_COL_NAME')
	df.columns = df.columns.str.replace(b, a)
	df.columns = df.columns.str.replace('REPLACE_COL_NAME', b)
	return df


def DEBUG_print_xyz(x, y, z, prefix = ""):
	print(prefix + ": " + str(x) + " ~ " +  str(y) + " ~ "  + str(z))


if __name__ == "__main__":
	main()