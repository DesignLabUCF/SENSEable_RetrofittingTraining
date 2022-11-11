##################################
#         RedrawWallArt          #
#     SENSEable Design Lab       #
##################################
# v1.0
# 2/13/2021
##################################
# To run, pass in directory and file without extensions
# EXP: 'python RedrawWallArt.py SubjectFolder DrawingTextFile'
##################################
# Authors: 
# Sermarini
# Kider
##################################

import sys
import os
import re
import threading
import time
from datetime import datetime
from kivy.app import App
from kivy.graphics import Line,Color   #Introduce drawing
from kivy.uix.widget import Widget     #Control
from kivy.utils import get_color_from_hex   #Compatible with hex colors
from kivy.uix.behaviors import ToggleButtonBehavior  #Introduction button switch behavior
from kivy.uix.togglebutton import ToggleButton   #Introduction switch button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.input.providers.mouse import MouseMotionEvent


# Datafile info
datafile = None
subjectID = "NoID"
subjectDir = "Subjects\\" + str(subjectID)
# Imported from data file
start_time = None
strokes = []
points = []
commands = []
imported_window_size = (-1,-1)
imported_window_top = -1
imported_window_left = -1
# Parameters
update_frequency = 1.0/60.0
#datetime_format = '%Y-%m-%d_%H-%M-%S-%f'
datetime_format = '%H:%M:%S.%f'
previous_time_DEBUG = None


class Point():
    def __init__(self, x, y, rgb, stroke_width, time, stroke):
        self.x = x
        self.y = y
        self.rgb = rgb
        self.stroke_width = stroke_width
        self.time = time
        self.stroke = stroke # Stroke it's part of


class Stroke_Start():
    def __init__(self, x, y, rgb, stroke_width, time):
        self.x = x
        self.y = y
        self.rgb = rgb
        self.stroke_width = stroke_width
        self.time = time
        self.points = []    

    def add_point(self, point):
        self.points.append(point)

    def print_debug(self):
        print("==========")
        print("(" + str(self.x) + ", " + str(self.y) + ")")  
        print(self.rgb)  
        print(self.stroke_width)  
        print(self.time)
        print(str(len(self.points)) + " points")  

class Stroke_End():
    def __init__(self, stroke, time):
        self.stroke = stroke
        self.time = time

class Undo():
    def __init__(self, stroke, time):
        self.stroke = stroke
        self.time = time


class FrameToggleButton(ToggleButton):
    #Current button to add a border
    def do_press(self):
        if self.state=='generally':
            ToggleButtonBehavior.do_press(self)


class DrawCanvasWidget(Widget):    #Layout
    def __init__(self,**kwargs):
        super(DrawCanvasWidget, self).__init__(**kwargs)
        # Kivy variables
        self.change_color(get_color_from_hex('#9A6324'))
        self.line_width=5.5
        Window.bind(mouse_pos=self.on_mouse_pos)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        Window.bind(on_request_close=self.on_request_close)
        # Set window size from imported file
        global imported_window_size
        global imported_window_top
        global imported_window_left
        Window.size = (imported_window_size[0], imported_window_size[1])
        Window.top = imported_window_top
        Window.left = imported_window_left
        #Window.maximize()
        # Play button
        self.button_play = Button(
            text="Play", 
            size=(Window.size[0]/4, 60),
            pos=(0,0))
        self.button_play.bind(on_press=self.play_button_pressed)
        self.add_widget(self.button_play)
        # Timeline label
        self.timeline_label = Label(
            text='---',
            font_size='20sp',
            color=(0,0,0,1),
            bold=True,
            halign="center",
            size = (Window.size, 60),
            pos=(Window.size[0]/2, Window.size[1]-60))
        self.timeline_label.texture_update()
        self.add_widget(self.timeline_label)
        # Timeline
        # Timeline min: time of first point
        # Timeline max: time of last point
        # Timeline step: 1/60 of second
        # Update: Go thru commands up to this given time and draw all up to that point
        timeline_min = strokes[0].time
        timeline_max = points[len(points) - 1].time
        self.timeline = Slider(
            value_track=True,
            orientation="horizontal",
            size=((3.0*Window.size[0])/4.0, 60),
            pos=(Window.size[0]/4, 0),
            #range=(1,get_number_of_points()),
            range=(timeline_min.timestamp()*1000.0, timeline_max.timestamp()*1000.0),
            #step=1)
            step=update_frequency)
        self.timeline.bind(value=self.timeline_clicked)
        self.add_widget(self.timeline)
        # Application variables
        self.kill_inc = False
        self.drawn_lines = []
        

    #def callback(self, instance):
    #    print('The button %s state is <%s>' % (instance, instance.state))

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def on_request_close(self, *args):
        self.exit()
        return True

    def exit(self):
        #self.screen_shot()
        self.kill_inc = True
        datafile.close()
        quit()

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'a':
            print_commands()
            pass
        if keycode[1] == 'q':
            #self.exit()
            pass
        if keycode[1] == 'e':
            #self.undo()
            pass

    def on_mouse_pos(self, instance, pos):
        pass

    def on_touch_down(self, touch):
        if Widget.on_touch_down(self, touch):
            return

    def on_touch_move(self, touch):
        pass

    def on_touch_up(self, touch):
        pass

    def change_color(self, new_color):
        #Pull color selection brush color
        self.last_color = new_color
        self.canvas.add(Color(*new_color))

    def change_line_width(self, line_width):
        #self.line_width={'Finer':1,'generally':2.5,'Coarse':5.5}[line_width]
        self.line_width = line_width

    # Used for init
    def clear_canvas(self):
        #Empty
        saved=self.children[:]
        self.clear_widgets()
        self.canvas.clear()
        for widget in saved:
            self.add_widget(widget)

    def clear(self):
        pass

    def draw_stroke(self, stroke, termination_timestamp=None):
        # Simulate pen - https://stackoverflow.com/questions/60720602/how-can-i-generate-an-event-in-kivy-like-an-on-touch-down-or-on-touch-up-event
        touch = MouseMotionEvent(None, 123, (123, 456))  # args are device, id, spos
        touch.button = 'left'
        # Simulate pen down
        with self.canvas:
            Color(stroke.rgb[0], stroke.rgb[1], stroke.rgb[2], stroke.rgb[3])
            touch.ud['current_line'] = Line(points=(stroke.x, stroke.y), width=stroke.stroke_width)
        # Simulate hand movement with pen
        for point in stroke.points:
            # if this points time is past the termination time, exit because we've drawn all we need to
            if termination_timestamp != None and point.time.timestamp()*1000.0 > termination_timestamp:
                break
            Color(point.rgb[0], point.rgb[1], point.rgb[2], point.rgb[3])
            touch.ud['current_line'].points += (point.x, point.y)
        self.drawn_lines.append(touch.ud['current_line'])

    def play_button_pressed(self, button):
        if button.text == "Play":
            button.text = "Pause"
            self.kill_inc = False
            inc_thread = threading.Thread(target=self.inc_timeline).start()
            # Start inc
        else:
            button.text = "Play"
            self.kill_inc = True
            # Kill inc

    def inc_timeline(self):
        while not self.kill_inc: # Only exit when thread is terminated
            previous_time = self.timeline.value
            next_time = self.timeline.value + self.timeline.step
            if next_time < self.timeline.max:
                # Update timeline slider on GUI
                self.timeline.value = self.timeline.value + (self.timeline.step * 1000.0)
                # Update canvas
                self.increment_drawing(previous_time, next_time)
                # Wait for next canvas update so it can be done in real-time
                previous_time_DEBUG = datetime.now()
                time.sleep(update_frequency)
                #print((datetime.now() - previous_time_DEBUG).total_seconds())
            else:
                self.button_play.text = "Play"
                self.kill_inc = True
    
    def timeline_clicked(self, instance, value):
        value = self.timeline.value
        # Update time header text
        time = datetime.fromtimestamp(value/1000.0).strftime(datetime_format)[:-3] # Turn microseconds to milliseconds
        self.timeline_label.text = time
        # Update drawing canvas
        self.set_drawing_to_time(value)    

    # Use to create drawing from scratch. Used when clicking on timeline
    def set_drawing_to_time(self, timestamp):
        #print("Timeline:", datetime.fromtimestamp(timestamp/1000.0).strftime(datetime_format))
        # Reset canvas
        self.clear_canvas()
        self.drawn_lines.clear()
        # Find final command
        final_index = 0
        for i in range(0, len(commands)):
            command = commands[i]
            command_time_microseconds = command.time.timestamp()*1000.0
            if command_time_microseconds > timestamp:
                break
            else:
                final_index = i
        # Draw the strokes
        last_stroke = None
        for i in range(0, final_index + 1, 1):
            command = commands[i]            
            if isinstance(command, Stroke_Start):
                last_stroke = command
            elif isinstance(command, Stroke_End): # Draw full stroke
                self.draw_stroke(last_stroke)
            elif isinstance(command, Point):  
                if i == final_index: # If last stroke was not finished, draw up to this point
                    self.draw_stroke(last_stroke, commands[final_index].time.timestamp()*1000.0)
            elif isinstance(command, Undo): # Delete the last full stroke
                self.canvas.remove(self.drawn_lines[len(self.drawn_lines) - 1])
                self.drawn_lines.pop()

    # Used to increment drawing for seperate thread calls. Redrawing entire image from scratch is timely with longer drawings
    # On the first update frame in which a command is found, execute it
    def increment_drawing(self, previous_time, current_time):
        # Find next command
        next_index = 0
        for i in range(0, len(commands)):
            command = commands[i]
            command_time_microseconds = command.time.timestamp()*1000.0
            if command_time_microseconds > current_time:
                break
            else:
                next_index = i
        next_command = commands[next_index]
        # Fine previously executed command
        previous_index = 0
        for i in range(0, len(commands)):
            command = commands[i]
            command_time_microseconds = command.time.timestamp()*1000.0
            if command_time_microseconds > previous_time:
                break
            else:
                previous_index = i
        previous_command = commands[previous_index] # Don't need to execute a command if it's already been done
        # Execute command if needed
        if next_command != previous_command:
            if isinstance(next_command, Stroke_Start): # Don't need to do anything, drawing doesn't start untill point
                pass
            elif isinstance(next_command, Stroke_End): # Don't need to do anything, stroke would've already been drawn by last final point
                pass
            elif isinstance(next_command, Point):
                # If the previous command was a point, we have a partially drawn line, so delete it for replacement
                if isinstance(previous_command, Point):
                    self.canvas.remove(self.drawn_lines[len(self.drawn_lines) - 1])
                    self.drawn_lines.pop()
                # Draw this point's stroke up to this point
                stroke = command.stroke
                self.draw_stroke(stroke, next_command.time.timestamp()*1000.0)               
                pass
            elif isinstance(next_command, Undo): # Remove previous stroke entirely
                self.canvas.remove(self.drawn_lines[len(self.drawn_lines) - 1])
                self.drawn_lines.pop()

class RedrawWallArtApp(App):  #Inherited App Class
    #Implement the build () method of the APP class (inherited from the APP class)
    def build(self):
        self.canvas_widget=DrawCanvasWidget()
        return self.canvas_widget         #Return root control

def parse_input(datafile):
    # First line will be start time
    start_time = time_ripper(datafile.readline().split(": ")[1])
    # Second line will be window size
    global imported_window_size
    global imported_window_top
    global imported_window_left
    window_info = datafile.readline().split(": ")[1].split("$")
    imported_window_size = (int(window_info[0].split(",")[0]), int(window_info[0].split(",")[1]))
    imported_window_top = int(window_info[1])
    imported_window_left = int(window_info[2])
    # Parse rest of input file
    lines = datafile.readlines()
    current_stroke = None
    for line in lines:
        data_type = line.split(": ")[0]
        if "STROKE-START" in data_type:
            x, y, rgb, stroke_width, time = parse_position_line(line)
            stroke = Stroke_Start(int(x), int(y), get_rgb_from_string(rgb), float(stroke_width), time)
            # Add to mega lists
            strokes.append(stroke)
            commands.append(stroke)
            current_stroke = stroke
            pass
        elif "STROKE-END" in data_type:
            stroke_start = strokes[len(strokes) - 1]
            time = time_ripper(line.split(": ")[1])
            stroke_end = Stroke_End(stroke_start, time)
            # Add to mega list
            commands.append(stroke_end)
            pass
        elif "POINT" in data_type:
            x, y, rgb, stroke_width, time = parse_position_line(line)
            point = Point(int(x), int(y), get_rgb_from_string(rgb), float(stroke_width), time, current_stroke)
            # Add point to latest stroke
            strokes[len(strokes) - 1].add_point(point)
            # Add to mega list
            points.append(point)
            commands.append(point)
            pass
        elif "UNDO" in data_type:
            stroke = strokes[len(strokes) - 1]
            time = time_ripper(line.split(": ")[1])
            undo = Undo(stroke, time)
            # Add to mega list
            commands.append(undo)
            pass

def parse_position_line(line):
    # Get data, ignore line header
    data = line.split(": ")[1]
    # Get position
    pos = data.split("$")[0]
    x = float(pos.split(",")[0].strip())
    y = float(pos.split(",")[1].strip())
    # Get color value
    rgb = data.split("$")[1] #Color(*new_color)
    # Get line width
    stroke_width = data.split("$")[2]
    # Get time of drawing
    time = time_ripper(data.split("$")[3])
    return x, y, rgb, stroke_width, time

# Get line from a section of line (Gave it a cool name because hell yeah)
def time_ripper(data):
    data = data.strip()
    # Date
    date = data.split("_")[0]
    year = date.split("-")[0]
    month = date.split("-")[1]
    day = date.split("-")[2]
    # Time
    time = data.split("_")[1]
    hour = time.split("-")[0]
    minute = time.split("-")[1]
    second = time.split("-")[2]
    microsecond = time.split("-")[3].strip()
    return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second), int(microsecond))

# TODO replace with len(points)
def get_number_of_points():
    num = 0
    for stroke in strokes:
        num = num + len(stroke.points)
    return num

def get_rgb_from_string(rgb_string):
    rgb_string = rgb_string.strip()[1:-1]
    rgb_string = rgb_string.split(", ")
    r = float(rgb_string[0])
    g = float(rgb_string[1])
    b = float(rgb_string[2])
    a = float(rgb_string[3])
    return (r, g, b, a)

def print_commands():
    i = 0
    for c in commands:
        i = i + 1
        print(i, ": " + str(type(c)))

if __name__=='__main__':
    # Check inputs and initialize
    assert len(sys.argv) >= 3, "Error: Arguments required for Subject directory and data text file."
    subject_directory = os.path.join("Subjects", sys.argv[1])
    assert os.path.isdir(subject_directory), "Error: Valid directory for " + sys.argv[1] + " not found."
    subject_datafile = os.path.join(subject_directory, sys.argv[2] + ".txt")
    assert os.path.exists(subject_datafile), "Error file " + sys.argv[2] + ".txt" + " not found in directory " + subject_directory 
    # Open file and parse it
    datafile = open(subject_datafile, "r")
    parse_input(datafile)
    datafile.close()
    # Start GUI
    RedrawWallArtApp().run()

# self.canvas.remove(self.previousLines[len(self.previousLines) - 1])
# touch.ud['current_line']=self.previousLines[len(self.previousLines) - 1]
# touch.ud['current_line'].points+=(touch.x,touch.y)