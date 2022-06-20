import sys

from kivymd.uix.textfield import MDTextField

from main.Graphics.GraphicInterface import UserInterface

from kivy.core.window import Window

"""

Notes:
 -> beta_int Linear Regression with constraint (0,0)
 -> show calculated beta_int in plot
 -> vector length sync [...]
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
