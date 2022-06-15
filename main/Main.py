import sys

from main.Graphics.GraphicInterface import UserInterface

from kivy.core.window import Window

"""
    WELCOME!
    
    This is the main code of main:
        This is where all the magic happens. 
        The code written here (main_old.py) uses all other files as the following suggests:
        
            ->  tabs_old.py             The GUI in main uses Kivy & Kivymd, which are based on KV language. 
                                    "tabs_old.py" is a KV file that contains the design structure of main's GUI.
                                    
            ->  bancrofts_data.txt  Data file; is used in the dispersion correction calculation.
            
            ->  k_type.txt          Data file used for the calibration of a K type Thermocouple. 
                                    This is used only if thermal analysis is enabled.
                                    
            ->  defaults.txt        As the name implies, this is where all the settings & parameters of main   
                                    are saved.
     
    Have a blast!
    
    // Gregory Tzvi Gershanik, creator of main.
    
"""

"""

Notes:
 -> beta_int Linear Regression with constraint (0,0)
 -> show calculated beta_int in plot
 -> vector length sync 
 -> Symmetric axes
 
"""

Window.size = (900, 850)
Window.icon = "/2BarG_emblem.png"
Window.title = "2BarG"
Window.top = 100
Window.left = 500


def resize(*args):
    Window.top = Window.top
    Window.left = Window.left
    Window.size = (900, 850)
    return True


Window.bind(on_resize=resize)

#   The following will hide the CMD window when the program is running.
if sys.platform == "win32":
    import ctypes

    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

UserInterface().run()
