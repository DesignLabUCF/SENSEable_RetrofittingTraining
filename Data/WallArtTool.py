##################################
#          WallArtTool           #
#     SENSEable Design Lab       #
##################################
# v1.0
# 1/28/2021
##################################
# To run, ~
# EXP: 'python WallArtTool.py'
##################################
# Authors: 
# Sermarini
# Kider
##################################

# NOTE: REVIEW https://groups.google.com/g/kivy-users/c/8cjmh_Ri4Jg/m/nez06cNHAQAJ


import os
import sys
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
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import tkinter as tk
from tkinter import messagebox

datafile = None
subject_name = ""
subject_dir = None
tkinter_font = 'Times 20'
datetime_format = '%Y-%m-%d_%H-%M-%S-%f'


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
        self.buttonIsdown=False
        Window.bind(mouse_pos=self.on_mouse_pos)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        Window.bind(on_request_close=self.on_request_close)
        # Window width must be divisible by 4 (https://github.com/kivy/kivy/issues/3847)
        #Window.size = (1200, 800) # Original
        Window.size = (800, 800) # Square
        #Window.size = (400, 300) # For debugging
        Window.top = 25
        Window.left = 5
        #Window.maximize()
        # SENSEable variables
        self.bIsDrawing = False
        self.strokeIndex = 0
        self.strokes = [] #
        self.previousLines = []
        self.lastStrokeStartDatetime = None
        self.lastUndoDatetime = None
        self.penDoubleTapCheck = 0.2 # Number of seconds between taps to check for pen double taps/touch calls
        # Write window dimensions to file for Redraw script
        datafile.write("WINDOW: " + str(Window.size[0]) + "," + str(Window.size[1]) + "$" + str(Window.top) + "$" + str(Window.left) + "\n")
        datafile.flush()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None


    def screen_shot(self):
            print("Saving Screenshot: " +datetime.now().strftime(datetime_format))
            Window.screenshot(name=subject_dir +'\\screenshot-'+datetime.now().strftime(datetime_format)+'.jpg')


    def on_request_close(self, *args):
        self.exit()
        return True


    def exit(self):
        self.screen_shot()
        datafile.close()
        quit()


    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 's':
            self.screen_shot()
        if keycode[1] == 'q':
            self.exit()
        if keycode[1] == 'e':
            self.undo()


    def on_mouse_pos(self, instance, pos):   #double check on info, granted repeative.
        # Not called by pen touching screen. Only mouse
        """
        if self.buttonIsdown and pos[1] > 60:
            datafile.write("POSTION: " +str(pos[0])+','+str(pos[1])+','+str(self.last_color)+','+datetime.now().strftime('%Y-%m-%d,%H-%M-%S.%f')[:-3]+"\n")
            datafile.flush()
        """
        pass


    '''
        When touched with mouse, calls once with class MouseMotionEvent
        When touched with finger, calls once with class WM_MotionEvent
        When touched with pen, calls twice. First with class WM_MotionEvent and then with class WM_Pen
        When using pen, WM_Motion DOES has positional data, but DOES NOT change button aesthetics
        When using pen, WM_Pen DOES NOT have position data, but DOES change button aesthetics
        So, apply WM_PEN call to only buttons and WM_MotionEvent call to only drawing canvas  
    '''
    def on_touch_down(self, touch):
        """
        if(self.pen_double_call(self.lastStrokeStartDatetime)): # Old method, prevents double call with pen but doesn't allow for button aesthetic changes for feedback to user
            return
        """
        #print(touch.__class__.__name__)


        # Touch is on canvas and not bottom buttons
        if touch.y > 60:
            if touch.__class__.__name__ != "WM_Pen": # Prevent pointless pen call from double logging
                #print(touch.profile)
                # Set stroke values
                self.bIsDrawing = True
                self.lastStrokeStartDatetime = datetime.now()
                #stroke_out =  "STROKE: " +str(touch.x)+','+str(touch.y)+','+str(self.last_color)+','+datetime.now().strftime('%Y-%m-%d,%H-%M-%S.%f')[:-3]+"\n"
                stroke_out =  "STROKE-START: " +str(touch.x)+','+str(touch.y)+'$'+str(self.last_color)+'$'+str(self.line_width)+'$'+datetime.now().strftime(datetime_format)+"\n"
                # Write to output file
                datafile.write(stroke_out)
                datafile.flush()
                # Draw to canvas
                with self.canvas:
                    self.previousLines.append(Line(points=(touch.x,touch.y),width=self.line_width))
                    touch.ud['current_line']=self.previousLines[len(self.previousLines) - 1]
            else:
                return # Prevent rest of button operations since this call was never desired here anyway
        # Touch is on bottom buttons and not canvas
        else:
            if touch.__class__.__name__ != "WM_MotionEvent": # Will eliminate ability to change buttons with finger, but I'm not crying about it :)
                pass # Continue on, nothing to see here
            else:
                return # Prevent rest of button operations since this call was never desired here anyway
        self.buttonIsdown=True
        if Widget.on_touch_down(self,touch):
            return


    def on_touch_move(self, touch):
        #Connection line
        if touch.y > 60 and len(touch.profile) > 0: # Touch happens above the buttons and is not the pen held above the screen
            #datafile.write("POINT: " +str(touch.x)+','+str(touch.y)+','+str(self.last_color)+','+datetime.now().strftime('%Y-%m-%d,%H-%M-%S.%f')[:-3]+"\n")
            datafile.write("POINT: " +str(touch.x)+','+str(touch.y)+'$'+str(self.last_color)+'$'+str(self.line_width)+'$'+datetime.now().strftime(datetime_format)+"\n")
            datafile.flush()
            if 'current_line' in touch.ud:
                touch.ud['current_line'].points+=(touch.x,touch.y)
                self.previousLines[len(self.previousLines) - 1].points+=(touch.x,touch.y)
            #self.print_touch_profile(touch)


    def on_touch_up(self, touch):
        if(self.bIsDrawing == True):
            self.strokeIndex = self.strokeIndex + 1
            print("Stroke count: ", self.strokeIndex)
            # Write to output file
            stroke_out =  "STROKE-END: "+ datetime.now().strftime(datetime_format)+"\n"
            datafile.write(stroke_out)
            datafile.flush()
        self.buttonIsdown=False
        self.bIsDrawing = False


    def change_color(self,new_color):
        #Pull color selection brush color
        self.last_color=new_color
        self.canvas.add(Color(*new_color))


    def change_line_width(self,line_width='generally'):
        #Select the line width
        self.line_width={'Finer':1,'generally':2.5,'Coarse':5.5}[line_width]
        print(self.line_width)
        #if 'pressure' in touch.profile:
        #    ud['pressure'] = touch.pressure
        #    pointsize = (touch.pressure * 100000) ** 2


    def clear_canvas(self):
        #Empty
        saved=self.children[:]
        self.clear_widgets()
        self.canvas.clear()
        for widget in saved:
            self.add_widget(widget)
        self.change_color(self.last_color)

    # Erase previous line
    def undo(self):
        if(self.pen_double_call(self.lastUndoDatetime)):
            return
        if(len(self.previousLines) != 0):
            #undoOut = "UNDO:" + datetime.now().strftime('%Y-%m-%d,%H-%M-%S.%f')[:-3]+"\n"
            undoOut = "UNDO: " + datetime.now().strftime(datetime_format)+"\n"
            self.lastUndoDatetime = datetime.now()
            datafile.write(undoOut)
            datafile.flush()
            self.canvas.remove(self.previousLines[len(self.previousLines) - 1])
            self.previousLines.pop()

    #def Pressbtn(self, instance):
    #    print(instance.state)


    def print_touch_profile(self, touch):
        """
        for i in range(0, len(touch.profile)):
            print(touch.profile[i] + ": ")
            print(type(touch.profile))
            print("==================")
        """
        print(touch.profile)
        print(touch.is_touch)
        if 'angle' in touch.profile:
            print('Angle: ', touch.a)
        if 'button' in touch.profile:
            print('Button: ', touch.button)
        if 'pos' in touch.profile:
            print('Position: ', touch.pos)
        if 'pressure' in touch.profile:
            print('Pressure: ', touch.pressure)
        if 'shape' in touch.profile:
            print('Shape: ', touch.shape)
        if 'size' in touch.profile:
            print('Size: ', touch.size)


    # True if double call caused by the pen double calling function twice
    def pen_double_call(self, previousTime):
        if(previousTime == None):
            return False
        currentTime = datetime.now()
        difference = currentTime - previousTime
        if(difference.total_seconds() >= self.penDoubleTapCheck):
            return False
        else:
            return True

class WallArtToolApp(App):  #Inherited App Class
    #Implement the build () method of the APP class (inherited from the APP class)
    def build(self):
        self.canvas_widget=DrawCanvasWidget()
        return self.canvas_widget         #Return root control

def get_topleft_of_screen(window):
    width = int(window.winfo_screenwidth() / 4.0)
    height = int(window.winfo_screenheight() / 2.0)
    #return "+" + str(width) + "+0"
    return "+0+0"

def get_id_window():
    # Init
    window = tk.Tk()
    # Configure GUI
    window.title("Wall Cutout Estimator")
    window.resizable(width=False, height=False)
    window.configure(background="white")
    window.wm_iconbitmap("icon.ico") # Icon (For classy reason, duh)
    window.wm_geometry(get_topleft_of_screen(window)) # Put window on center of screen
    # Create GUI frame
    frame = tk.Frame(window)
    id_label = tk.Label(window, text="Please enter your ID number:", font=tkinter_font)
    id_label.pack(fill=tk.BOTH)
    id_text = tk.Text(window, height=1, width=10, font=tkinter_font)
    id_text.pack(fill=tk.BOTH)
    continue_button = tk.Button(window, text="Continue", font=tkinter_font, command=lambda : finish_get_id(id_text.get("1.0","end-1c").strip(), window))
    continue_button.pack(fill=tk.BOTH)
    # Run GUI
    window.mainloop()

def finish_get_id(subject_id_textbox_value, root_window):
    global subject_name
    global subject_dir
    # Ensure input is valud
    if subject_id_textbox_value == "":
        tk.messagebox.showinfo("Error", "Error: Invalid Subject ID entered.")
        return
    # Assign filename values from textbox input
    subject_name = subject_id_textbox_value
    subject_dir = "Subjects//" + subject_name
    # Create directories for subject if needed
    #assert not os.path.isfile(file_name), "Error: File '" + file_name + "' already exists. Please delete it or double check subject name argument before restarting."
    if not os.path.isdir(subject_dir):
        print("Subject directory not found. " + subject_dir + " created.")
        os.makedirs(subject_dir)
    root_window.destroy()

if __name__=='__main__':
    """
    # Assign subject ID from argument
    if len(sys.argv) > 1:
        subjectID = sys.argv[1]
    else:
        subjectID = "NoID"
    # Create data directory if does not exists
    subjectDir = "Subjects\\" + str(subjectID)
    if not os.path.isdir(subjectDir):
        os.makedirs(subjectDir)
    """
    # TKinter for instructions and text input
    while(subject_name == ""):
        get_id_window()
    # Open textfile to write to
    datafile = open(subject_dir + "\\" + subject_name + "_" + datetime.now().strftime(datetime_format)+".txt", "w")
    #datafile.write("START: " + datetime.now().strftime('%Y-%m-%d,%H-%M-%S.%f')[:-3]+"\n")
    datafile.write("START: " + datetime.now().strftime(datetime_format)+"\n")
    datafile.flush()
    # Start drawing app
    WallArtToolApp().run()