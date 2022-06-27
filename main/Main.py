import os
import sys

from kivy.resources import resource_add_path, resource_find

from main.Graphics.GraphicInterface import UserInterface

from kivy.core.window import Window

Window.size = (900, 850)
Window.icon = "2BarG_emblem.ico"
Window.title = "2BarG"
Window.top = 100
Window.left = 500


def resize(*args):
    Window.top = Window.top
    Window.left = Window.left
    Window.size = (900, 850)
    return True


Window.bind(on_resize=resize)


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    UserInterface().run()
