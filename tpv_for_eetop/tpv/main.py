# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   04-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 06-Mar-2018
# @License: Apache license vesion 2.0

import config
import os
import sys

from kivy.app import App
from controllers.tpv import Tpv
from kivy.config import Config
from kivy.clock import Clock
from kivy.lib import osc

Clock.max_iteration = 20

class TpvApp(App):

    def __init__(self, **kargs):
        super(TpvApp, self).__init__(**kargs)
        self.title = 'BTRES'
        path = os.path.abspath(__file__)
        self.icon = os.path.join(path, "img/logo.jpg")
        osc.init()


    def build(self):
        import os, threading
        threading.Thread(target=os.system, args=("python ./service/main.py",)).start()
        return Tpv()

    def on_pause(self):
        return True

    def on_stop(self):
        osc.sendMsg("/sync_service", ["finalizar"], port=config.PORT_SERVICE)


if __name__ == '__main__':
    from kivy.core.window import Window
    Window.clearcolor = (1, 1, 1, 1)
    TpvApp().run()
