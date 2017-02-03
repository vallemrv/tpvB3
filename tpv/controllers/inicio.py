# -*- coding: utf-8 -*-
from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from valle.component.botonera import Botonera
from valle.utils import json_to_list


class Inicio(AnchorLayout):

    def __init__(self, **kargs):
        super(Inicio, self).__init__(**kargs)
        self.botonera = Botonera(onPress=kargs["controller"])
        self.crear_inicio()
        self.add_widget(self.botonera)


    def crear_inicio(self):
        self.botonera.completo = True
        src = JsonStore('db/clases.json')
        src = json_to_list(src['db'].get('lista'))
        src.append({"text": "Abrir cajón", "tipo": "abrir_cajon",
                    "color": "#BDBDBD"})
        self.botonera.botones = src
        self.botonera.titulo = "Bienvenido"
