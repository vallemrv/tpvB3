# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   13-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 23-Feb-2018
# @License: Apache license vesion 2.0


from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.properties import (ObjectProperty, StringProperty,
                             ListProperty)
from kivy.lang import Builder

Builder.load_string("""
<Aceptar>:
    background_color: 0,0,0,.6
    size_hint: .7, .7
    AnchorLayout:
        size_hint: .95, .95
        BoxLayout:
            orientation: 'vertical'
            spacing: 10
            LabelColor:
                bg_color: "#ff5793"
                text: "Atención!"
                size_hint_y: None
                height: "70dp"
                color: '#ffffff'
                border_size: 0
            LabelColor:
                bg_color: "#99ace6"
                text: root.text_men
                size_hint_y: .6
                color: '#ffffff'
                border_size: 0
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: .2
                ButtonColor:
                    bg_color: "#989898"
                    text: "Aceptar"
                    on_release: root.on_press()


              """)

class Aceptar(ModalView):
    onExit = ObjectProperty(None, allownone=True)
    text_men = StringProperty("No puede hacer el arqueo de caja porque hay pedidos sin cobrar....")

    def __init__(self, **kargs):
        super(Aceptar, self).__init__(**kargs)
        self.auto_dismiss=False


    def on_press(self):
        if self.onExit != None:
            self.onExit()
