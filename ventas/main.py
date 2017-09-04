# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   13-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Filename: main.py
# @Last modified by:   valle
# @Last modified time: 13-Aug-2017
# @License: Apache license vesion 2.0

import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
abspath = os.path.abspath(__file__)
from random import shuffle

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivy.lang import Builder


from components.pagenavigations import MainPage
from components.pagenavigations import PageManager

Builder.load_string('''
#:import Botonera components.botonera.Botonera
#:import Page components.pagenavigations.Page
<Password>:
    botonera: _botonera
    textInput: _textInput
    AnchorLayout:
        anchor_x:'right'
        anchor_y:'bottom'
        canvas:
            Color:
                rgba: 0,0,0,1
            Rectangle:
                source: root.dname +'/sombra.png'
                size: root.width + dp(60), root.height + dp(60)
                pos: self.x, self.y - dp(60)
    AnchorLayout:
        canvas:
            Color:
                rgb: .4,.4,.4,.4
            Rectangle:
                size: self.size
                pos: self.pos
        BoxLayout:
            size_hint: .9, .9
            orientation: 'vertical'
            TextInput:
                multiline: False
                font_size: 30
                size_hint: 1, None
                height: 50
                password: True
                id: _textInput
            Botonera:
                id: _botonera
                scrollable: False
                selectable: False
                title: 'None'
                cols: 3
                onPress: root.on_press

<Ventas>:
    Menu:
        passw: _passw
        id: _menu
        title: "Ventas"
        AnchorLayout:
            id: _passw
            size_hint: 1, 1
            canvas:
                Color:
                    rgb: 0,1,1,1
                Rectangle:
                    size: self.size
                    pos: self.pos
            Password:
                size_hint: .5, .9
                onPress: _menu.on_pass_ok


                    ''')

class Password(AnchorLayout):
    dname = StringProperty(os.path.dirname(abspath)+"/img/")
    botonera = ObjectProperty(None)
    onPress = ObjectProperty(None)
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
    ])
    def __init__(self, **kargs):
        super(Password, self).__init__(**kargs)

    def add_botones(self):
        botonesOut = []
        shuffle(self.botones)
        for btn in self.botones:
            btn["text"] = btn['num']
            botonesOut.append(btn)

        botonesOut.append({'text': 'C', "bgColor":'#f09696', 'num': 'C'})
        botonesOut.append({'text': 'OK', "bgColor":'#c6e494', 'num': 'OK'})

        self.botonera.botones = []
        self.botonera.botones = botonesOut
        Clock.schedule_once(self.set_as, 5)

    def on_botonera(self, w, l):
        self.add_botones()

    def set_as(self, dt):
        botonesOut = []
        for btn in self.botones:
            btn['text']='*'
            botonesOut.append(btn)

        botonesOut.append({'text': 'C', "bgColor":'#f09696', 'num': 'C'})
        botonesOut.append({'text': 'OK', "bgColor":'#c6e494', 'num': 'OK'})

        self.botonera.botones = []
        self.botonera.botones = botonesOut

    def on_press(self, btn):
        obj = btn[0].tag
        text = obj.get("num")
        if text != 'C' and text != "OK":
            self.textInput.text = self.textInput.text + text
        elif text == 'C':
            self.add_botones()
        elif text == 'OK':
            self.on_press_ok()

    def on_press_ok(self):
        if self.onPress:
            self.onPress(self.textInput.text)

class Menu(MainPage):
    def on_pass_ok(self, passw):
        print passw
        if passw == '7484':
            self.clear_widgets()


class Ventas(PageManager):
    pass

class VentasApp(App):
    def build(self):
        return Ventas()

if __name__ == '__main__':
    VentasApp().run()
