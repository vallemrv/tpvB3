# @Author: Manuel Rodriguez <valle>
# @Date:   15-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: main.py
# @Last modified by:   valle
# @Last modified time: 26-Jul-2017
# @License: Apache license vesion 2.0
# -*- coding: utf-8 -*-

import os
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(root, "valle_libs"))


from kivy.app import App
from views.gestion  import Gestion
from kivy.config import Config


Config.set("graphics", "width", "350")
Config.set("graphics", "height", "600")


class GestionApp(App):
    def __init__(self, **kargs):
        super(GestionApp, self).__init__(**kargs)

    def build(self):
        return Gestion()

    def on_pause(self):
        return True


if __name__ == '__main__':
    GestionApp().run()
