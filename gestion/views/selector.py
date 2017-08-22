# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   25-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: selector.py
# @Last modified by:   valle
# @Last modified time: 11-Aug-2017
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty
from components.mens import FloatMen
from kivy.lang import Builder

Builder.load_string('''
#:import FloatButton  components.buttons.FloatButton
#:import Botonera components.botonera
#:import Spin components.spin
<Selector>:
    spin: _spin
    content: _content_men
    botonera: _botonera
    selectable: False
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        Botonera:
            id: _botonera
            scrollable: True
            cols: 2
            font_size: '20dp'
            size_hint: .9, 1
            title: 'None'
            selectable: root.selectable
            onPress: root.on_press

    AnchorLayout:
        id: _content_men
    Spin:
        id: _spin

                    ''')

class Selector(AnchorLayout):
    page_manager = ObjectProperty(None)
    controller = ObjectProperty(None)


    def __init__(self, **kargs):
        super(Selector, self).__init__(**kargs)
        self.mensaje = FloatMen(men="")

    def on_press(self, btns):
        if self.controller and not self.selectable:
            self.controller.on_press(btns[0].tag)

    def show_mensaje(self, men):
        reg = self.botonera.botones
        if len(reg) <= 0 and not self.mensaje in self.content.children:
            self.mensaje.men = men
            self.content.add_widget(self.mensaje)
        elif len(reg) > 0 and self.mensaje in self.content.children:
            self.content.remove_widget(self.mensaje)


    def show_spin(self):
        self.spin.show()

    def hide_spin(self):
        self.spin.hide()


    def append_buttons(self, btns):
        self.botonera.botones.extend(btns)

    def set_botones(self, btns):
        self.botonera.botones = btns

    def on_show(self, page_manager):
        self.page_manager = page_manager
        if self.controller:
            self.controller.on_show(selector=True)

    def back_page(self):
        self.page_manager.back_page()
