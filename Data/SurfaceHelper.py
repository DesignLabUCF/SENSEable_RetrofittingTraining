import pyglet
from pyglet import app
from pyglet.window import Window
from pyglet.window import mouse

win = Window(width=640, height=480)

devices = pyglet.input.get_devices()
tablets = pyglet.input.get_tablets()

print("Tablets: ")
print(tablets)

print("All devices:")
i = 0
for d in devices:
	print(i, ": ", d)
	i = i + 1
print("==========================")

print("Devices with controls:")
i = 0
for d in devices:
	if(len(d.get_controls()) > 0):
		print(d)
print("==========================")

# Set up input for 1 key (WORKS)
keyboard = devices[1]
keyboard.open()
one_key = keyboard.get_controls()[1]
@one_key.event
def on_press():
	print("One key:", one_key.value)

# Set up input for mouse (WORKS)
"""
mouse = devices[0]
mouse.open()
left_click = mouse.get_controls()[3]
@left_click.event
def on_change(value):
	print("Left Click:", left_click.value)
"""

"""
# Set up Mouse X axis movement (WORKS)
mouse_x = mouse.get_controls()[0]
@mouse_x.event
def on_change(value):
	print("Mouse X:", value)
"""

# Set up input for pen (No input recieved... hmmm...)
pen = None
for d in devices:
	if(d.name == "Intel(R) Precise Touch Device" and len(d.get_controls()) != 0):
		pen = d
pen.open()
print(pen.get_controls())
pen_0 = pen.get_controls()[0]
@pen_0.event
def on_change(value):
	print("pen_0:", pen_0.value)
pen_1 = pen.get_controls()[1]
@pen_1.event
def on_change(value):
	print("pen_1:", pen_1.value)
pen_2 = pen.get_controls()[2]
@pen_2.event
def on_change(value):
	print("pen_2:", pen_2.x)
pen_3 = pen.get_controls()[3]
@pen_3.event
def on_change(value):
	print("pen_3:", pen_3.x)
pen_4 = pen.get_controls()[4]
@pen_4.event
def on_change(value):
	print("pen_4:", pen_4.x)
pen_5 = pen.get_controls()[5]
@pen_5.event
def on_change(value):
	print("pen_5:", pen_5.x)
pen_6 = pen.get_controls()[6]
@pen_6.event
def on_change(value):
	print("pen_6:", pen_6.x)
pen_7 = pen.get_controls()[7]
@pen_7.event
def on_change(value):
	print("pen_7:", pen_7.x)
pen_8 = pen.get_controls()[8]
@pen_8.event
def on_change(value):
	print("pen_8:", pen_8.x)
"""
# Pen controls (Must try each)
0 :  Button(raw_name=Tip Switch)
1 :  Button(raw_name=Button 1)
2 :  AbsoluteAxis(raw_name=Axis 6)
3 :  AbsoluteAxis(name=x, raw_name=X Axis)
4 :  AbsoluteAxis(name=y, raw_name=Y Axis)
5 :  AbsoluteAxis(raw_name=Axis 7)
6 :  AbsoluteAxis(raw_name=Axis 8)
7 :  AbsoluteAxis(raw_name=Axis 9)
8 :  AbsoluteAxis(raw_name=Axis 10)
"""

# Set up input for volume up (WORKS)
cpdcd_1 = devices[3]
"""
i = 0
for c in cpdcd_1.get_controls():
	print(i, ":", c)
	i = i + 1
print("==========================")
"""
cpdcd_1.open()
cpdcd_volumeInc = cpdcd_1.get_controls()[2]
@cpdcd_volumeInc.event
def on_change(value):
	print("cpdcd_volumeInc:", cpdcd_volumeInc.value)


hid = devices[6]
hid_controls = hid.get_controls()
i = 0
for c in hid_controls:
	print(i, c)
	i = i + 1


app.run()
