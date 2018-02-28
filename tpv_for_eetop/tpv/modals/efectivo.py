# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   13-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 15-Sep-2017
# @License: Apache license vesion 2.0


from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.properties import (ObjectProperty, StringProperty,
                             ListProperty)
from kivy.lang import Builder

Builder.load_string("""
<Efectivo>:
    botonera: _botonera
    background_color: 0,0,0,.6
    size_hint: .7, .7
    AnchorLayout:
        size_hint: .95, .95
        BoxLayout:
            orientation: 'horizontal'
            spacing: 10
            AnchorLayout:
                anchor_y: "top"
                canvas:
                    Color:
                        rgba: 1,1,1,1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                GridLayout:
                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    cols: 1
                    size_hint_y: None
                    height: "230dp"
                    LabelColor:
                        size_hint_y: .25
                        bgColor: "#000000"
                        color: "#ffffff"
                        text: "Introducir efectivo"
                    AnchorLayout:
                        anchor_x: "center"
                        GridLayout:
                            cols: 1
                            size_hint_x: .9
                            BoxLayout:
                                orientation: 'horizontal'
                                Label:
                                    font_size: "40dp"
                                    text: 'Total'
                                    color: 0,0,0,1
                                    text_size: self.size
                                    halign: "left"
                                Label:
                                    font_size: "40dp"
                                    text: root.text_total
                                    color: 0,0,0,1
                                    text_size: self.size
                                    halign: "right"
                            BoxLayout:
                                orientation: 'horizontal'
                                Label:
                                    font_size: "40dp"
                                    text: 'Efectivo'
                                    color: 0,0,0,1
                                    text_size: self.size
                                    halign: "left"
                                Label:
                                    font_size: "40dp"
                                    text: root.efectivo
                                    color: 0,0,0,1
                                    text_size: self.size
                                    halign: "right"
                            BoxLayout:
                                orientation: 'horizontal'
                                Label:
                                    font_size: "40dp"
                                    text: 'Cambio'
                                    color: 0,0,0,1
                                    text_size: self.size
                                    halign: "left"
                                Label:
                                    font_size: "40dp"
                                    text: root.cambio
                                    color: 0,0,0,1
                                    text_size: self.size
                                    halign: "right"

            GridButtons:
                cols: 3
                bgColor: "#010101"
                onPress: root.on_press
                id: _botonera

              """)

class Efectivo(ModalView):
    onExit = ObjectProperty(None, allownone=True)
    content = ObjectProperty(None, allownone=True)
    total = StringProperty("")
    cambio = StringProperty("0.00 €")
    text_efectivo = StringProperty("")
    text_total = StringProperty("")
    efectivo = StringProperty("0.00 €")
    botones = ListProperty([
        {'text': '1', "bgColor":'#999999', 'num': '1'},
        {'text': '2', "bgColor":'#999999', 'num': '2'},
        {'text': '3', "bgColor":'#999999', 'num': '3'},
        {'text': '4', "bgColor":'#999999', 'num': '4'},
        {'text': '5', "bgColor":'#999999', 'num': '5'},
        {'text': '6', "bgColor":'#999999', 'num': '6'},
        {'text': '7', "bgColor":'#999999', 'num': '7'},
        {'text': '8', "bgColor":'#999999', 'num': '8'},
        {'text': '9', "bgColor":'#999999', 'num': '9'},
        {'text': '0', "bgColor":'#999999', 'num': '0'},
        {'text': ',', "bgColor":'#999999', 'num': '.'},
        {'text': 'Ok', "bgColor":'#7bf67c', 'num': 'Ok'},
        {'text': 'C', "bgColor":'#f67b7b', 'num': 'C'},
        {'text': 'Exit', "bgColor":'#f67b7b', 'num': 'Exit'},
    ])

    def __init__(self, **kargs):
        super(Efectivo, self).__init__(**kargs)
        self.botonera.botones = self.botones


    def on_total(self, w, v):
        self.text_total = "{0:0.2f} €".format(float(v))

    def on_text_efectivo(self, w, v):
        total = float(self.total)
        efectivo = 0.0 if self.text_efectivo == "" else float(self.text_efectivo)
        cambio = efectivo - total
        cambio = 0.0 if cambio < 0 else cambio
        self.cambio = "{0:0.2f} €".format(cambio)
        self.efectivo = "{0:0.2f} €".format(efectivo)

    def borrar(self):
        self.text_efectivo = ""

    def on_press(self, btn):
        obj = btn[0].tag
        txt = obj.get("num")
        if txt not in ("Ok", "C", "Exit"):
            if txt == "." and not "." in self.text_efectivo:
                self.text_efectivo += txt
            elif txt != ".":
                self.text_efectivo += txt
        elif txt == "Exit":
            self.cancelar()
        elif txt == "Ok":
            self.aceptar()
        elif txt == "C":
            self.borrar()

    def aceptar(self):
        if self.onExit:
            self.onExit(cancelar=False)
            self.borrar()

    def cancelar(self):
        if self.onExit:
            self.onExit(cancelar=True)
            self.borrar()
