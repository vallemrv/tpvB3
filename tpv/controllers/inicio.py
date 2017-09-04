# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 04-Sep-2017
# @License: Apache license vesion 2.0

from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from components.gridbuttons import GridButtons
from kivy.lang import Builder

Builder.load_string('''
<Inicio>:
    tpv: None
    orientation: 'horizontal'
    content: _content
    size_hint: .95, .95
    spacing: 20
    GridButtons:
        cols: 4
        id: _content
        font_size_title: '35dp'
    AnchorLayout:
        size_hint_x: None
        width: 70
        anchor_x: 'center'
        anchor_y: 'top'
        GridLayout:
            cols: 1
            spacing: 5
            size_hint: 1, None
            height: len(self.children) * 70
            ButtonImg:
                border_size: 1
                bgColor: tpv_res.COLOR_BUTTONS
                src: 'img/llevar.png'
                on_release: root.tpv.mostrar_domicilio()
            ButtonImg:
                border_size: 1
                bgColor: tpv_res.COLOR_BUTTONS
                src: 'img/listapd.png'
                on_release: root.tpv.mostrar_pendientes()
            ButtonImg:
                bgColor: tpv_res.COLOR_BUTTONS
                src: 'img/lista.png'
                on_release: root.tpv.mostrar_pedidos()
            ButtonImg:
                border_size: 1
                bgColor: tpv_res.COLOR_BUTTONS
                src: 'img/arqueo.jpeg'
                on_release: root.tpv.mostrar_arqueo()
            ButtonImg:
                border_size: 1
                bgColor: tpv_res.COLOR_BUTTONS
                src: 'img/llave.png'
                on_release: root.tpv.abrir_cajon()
                    ''')


class Inicio(BoxLayout):

    def __init__(self, **kargs):
        super(Inicio, self).__init__(**kargs)
        self.tpv = kargs["tpv"]
        self.crear_inicio()


    def crear_inicio(self):
        src = JsonStore('../db/clases.json')
        self.content.botones = src['db'].get('lista')
        self.content.title = "Bienvenido"
