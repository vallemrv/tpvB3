# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   28-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Filename: main.py
# @Last modified by:   valle
# @Last modified time: 29-Aug-2017
# @License: Apache license vesion 2.0

import config
from kivy.app import App
from kivy.config import Config

from views.tpv import Tpv


class TpvApp(App):

    """Aplicacion principal para el TPV"""
    def __init__(self, **kargs):
        super(TpvApp, self).__init__(**kargs)
        self.title = "Tpv para el BTRES"
        self.icon = "img/logo.jpg"

    def build(self):
        return Tpv()

    def on_pause(self):
        return True


if __name__ == '__main__':
    TpvApp().run()
