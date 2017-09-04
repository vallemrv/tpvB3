# @Author: Manuel Rodriguez <valle>
# @Date:   04-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 04-Sep-2017
# @License: Apache license vesion 2.0


# -*- coding: utf-8 -*-
"""Programa tpv para la pizeria Btres

    Autor: Manuel Rodriguez
    Licencia: Apache v2.0
"""
import init
from kivy.app import App
from controllers.tpv import Tpv
from kivy.config import Config

try: # this is only for pygame window if pygame is avaliable
    import pygame
    pygame.display.init()
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    Config.set('graphics', 'width', str(int(width * .96)))
    Config.set('graphics', 'height', str(int(height * .98)))
except:
    pass

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
