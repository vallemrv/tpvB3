# @Author: Manuel Rodriguez <valle>
# @Date:   15-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Filename: password.py
# @Last modified by:   valle
# @Last modified time: 15-Aug-2017
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from random import shuffle
Builder.load_string('''
#:import Botonera components.botonera.Botonera
#:import res components.resources
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
                source: res.IMG_SHADOW_REC
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
                    ''')

class Password(AnchorLayout):
    botonera = ObjectProperty(None)
    onPress = ObjectProperty(None)
    timerout = NumericProperty(5)
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

    def random_botones(self):
        botonesOut = []
        shuffle(self.botones)
        for btn in self.botones:
            btn["text"] = btn['num']
            botonesOut.append(btn)

        botonesOut.append({'text': 'C', "bgColor":'#f09696', 'num': 'C'})
        botonesOut.append({'text': 'OK', "bgColor":'#c6e494', 'num': 'OK'})

        self.botonera.botones = []
        self.botonera.botones = botonesOut
        Clock.schedule_once(self.set_as, self.timerout)

    def on_botonera(self, w, l):
        self.random_botones()

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
            self.textInput.text = ""
            self.random_botones()
        elif text == 'OK':
            self.on_press_ok()

    def on_press_ok(self):
        if self.onPress:
            self.onPress(self.textInput.text)
