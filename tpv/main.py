# -*- coding: utf-8 -*-
"""Programa tpv para la pizeria Btres

    Autor: Manuel Rodriguez
    Licencia: Apache v2.0

"""
from kivy.app import App
from uix.tpv import Tpv
from kivy.config import Config
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

Config.set("graphics", 'width', '1024')
Config.set("graphics", 'height', '600')


class TpvApp(App):

    """Aplicacion principal para el TPV"""

    def build(self):
        return Tpv()

    def on_pause(self):
        return True


if __name__ == '__main__':
    from kivy.core.window import Window
    Window.clearcolor = (1, 1, 1, 1)
    TpvApp().run()
