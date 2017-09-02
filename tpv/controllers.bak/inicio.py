# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   28-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Filename: inicio.py
# @Last modified by:   valle
# @Last modified time: 29-Aug-2017
# @License: Apache license vesion 2.0

from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from components.gridbuttons import GridButtons
from valle.utils import json_to_list
from kivy.lang import Builder

Builder.load_string('''
#:import BotonImg components.botonimg.BotonImg
<Inicio>:
    tpv: None
    orientation: 'horizontal'
    inicio: _inicio
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        id: _inicio
    AnchorLayout:
        size_hint_x: None
        width: 100
        anchor_x: 'center'
        anchor_y: 'top'
        GridLayout:
            cols: 1
            spacing: 5
            padding: 30
            size_hint: 1, None
            height: len(self.children) * 70
            BotonImg:
                src: 'img/llevar.png'
                on_press: root.tpv.mostrar_domicilio()
            BotonImg:
                src: 'img/listapd.png'
                on_press: root.tpv.mostrar_pendientes()
            BotonImg:
                src: 'img/lista.png'
                on_press: root.tpv.mostrar_pedidos()
            BotonImg:
                src: 'img/arqueo.jpeg'
                on_press: root.tpv.mostrar_arqueo()
            BotonImg:
                src: 'img/llave.png'
                on_press: root.tpv.abrir_cajon()
                    ''')


class Inicio(BoxLayout):

    def __init__(self, **kargs):
        super(Inicio, self).__init__(**kargs)
        self.tpv = kargs["tpv"]
        self.botonera = GridButtons(onPress=self.tpv.onPress_seccion)
        self.crear_inicio()
        self.inicio.add_widget(self.botonera)


    def crear_inicio(self):
        self.botonera.completo = False
        src = JsonStore('db/clases.json')
        src = src['db'].get('lista')
        self.botonera.botones = src
        self.botonera.titulo = "Bienvenido"