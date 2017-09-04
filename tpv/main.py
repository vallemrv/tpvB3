# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   04-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 04-Sep-2017
# @License: Apache license vesion 2.0



import config
from kivy.app import App
from controllers.tpv import Tpv
from kivy.config import Config

class TpvApp(App):

    def __init__(self, **kargs):
        super(TpvApp, self).__init__(**kargs)
        self.title = 'BTRES'
        self.icon = "img/logo.jpg"

    def build(self):
        return Tpv()

    def on_pause(self):
        return True


if __name__ == '__main__':
    from kivy.core.window import Window
    Window.clearcolor = (1, 1, 1, 1)
    TpvApp().run()
