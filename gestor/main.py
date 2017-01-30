# -*- coding: utf-8 -*-
"""Programa Gestion para el TPV del Btres

    Autor: Manuel Rodriguez
    Licencia: Apache v2.0

"""
import init
from kivy.app import App
from uix.gestor import Gestor
from kivy.config import Config


try: # this is only for pygame window if pygame is avaliable
    import pygame
    pygame.display.init()
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    Config.set('graphics', 'width', str(int(width * .95)))
    Config.set('graphics', 'height', str(int(height * .95)))
except:
    pass


class GestorApp(App):

    """Aplicacion principal para el TPV"""

    def build(self):
        return Gestor()

    def on_pause(self):
        return True


if __name__ == '__main__':
    from kivy.core.window import Window
    Window.clearcolor = (1, 1, 1, 1)
    GestorApp().run()
