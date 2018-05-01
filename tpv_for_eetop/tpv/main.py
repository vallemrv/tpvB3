# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   04-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 17-Apr-2018
# @License: Apache license vesion 2.0

import sys
import os
try:
    reload(sys)
    sys.setdefaultencoding('UTF8')
except:
    from importlib import reload
    reload(sys)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
os.chdir(BASE_DIR)
sys.path.append(ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "valle_libs"))

import os
import sys
import valle_libs.config
from kivy.app import App
from controllers.tpv import Tpv
from kivy.config import Config
from kivy.clock import Clock

Clock.max_iteration = 20

class TpvApp(App):

    def __init__(self, **kargs):
        super(TpvApp, self).__init__(**kargs)
        self.title = 'BTRES'
        path = os.path.abspath(__file__)
        self.icon = os.path.join(path, "img/logo.jpg")


    def build(self):
        return Tpv()

    def on_pause(self):
        return True

    def on_stop(self):
        pass


if __name__ == '__main__':
    from kivy.core.window import Window
    Window.clearcolor = (1, 1, 1, 1)
    TpvApp().run()
