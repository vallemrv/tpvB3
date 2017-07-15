# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 14-Jul-2017
# @License: Apache license vesion 2.0


# -*- coding: utf-8 -*-
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (BooleanProperty, StringProperty,
                             ObjectProperty, NumericProperty, ListProperty)
from kivy.lang import Builder
from kivy.metrics import dp
from components.buttons import ButtonColor, ButtonIcon
from math import ceil
import resources as res

Builder.load_string('''
#:import res components.resources
#:import ButtonIcon components.buttons.ButtonIcon
<Botonera>:
    anchor_x: 'center'
    anchor_x: 'center'
    container: _contenedor
    content_titulo: _content_titulo
    size_hint: 1, 1
    spacing: 2
    GridLayout:
        size_hint: .9, .9
        cols: 1
        spacing: 20
        BoxLayout:
            orientation: 'horizontal'
            id: _content_titulo
            size_hint: 1, None
            height: dp(35)
            Label:
                color: 0, 0, 0, 1
                text: root.titulo
                font_size: '40dp'
                size_hint: 1, 1
        ScrollView:
            size_hint: 1, 1
            GridLayout:
                id: _contenedor
                cols: root.columnas
                spacing: root.spacing
                size_hint: root.content_size_hint

''')


class Botonera(AnchorLayout):
    font_size = ObjectProperty("30dp")
    columnas = NumericProperty(0)
    titulo = StringProperty("Titulo")
    botones = ObjectProperty(None)
    onPress = ObjectProperty(allownone=False)
    selectable = BooleanProperty(False)
    item_selected = ListProperty([])
    text_button_enter = StringProperty("sel 0")
    scrollable = BooleanProperty(False)
    content_size_hint = ListProperty([1, 1])
    spacing = NumericProperty()

    def __init__(self, **kargs):
        super(Botonera, self).__init__(**kargs)


    def on_scrollable(self, w, val):
        if self.scrollable and self.container and self.botones:
            self.content_size_hint = (1, None)
            self.container.height = dp(100) * ceil(len(self.botones) / float(self.container.cols))
        else:
            self.content_size_hint = (1, 1)


    def on_item_selected(self, w, val):
        if val != "" and len(self.content_titulo.children) == 1:
            self.add_button_enter()
        self.text_button_enter = "sel "+ str(len(self.item_selected))


    def on_selectable(self, w, val):
        if self.selectable and self.content_titulo and len(self.content_titulo.children) == 1:
            self.add_button_enter()
        elif not selectable and self.content_titulo and len(self.content_titulo.children) > 1:
            self.content_titulo(self.content_titulo.children[-1])

    def add_button_enter(self):
        btn = ButtonIcon(text=self.text_button_enter,size_hint=(.5, 1),
                    font_size='15dp', orientation='horizontal',icon=res.FA_ENTER)
        self.content_titulo.add_widget(btn)
        self.bind(text_button_enter=btn.setter('text'))
        btn.bind(on_release=self.on_button_enter_press)


    def on_botones(self, key, value):
        if self.scrollable:
            self.content_size_hint = (1, None)
            self.container.height = dp(100) * ceil(len(value) / float(self.container.cols))
        self.set_botones()

    def set_botones(self):
        self.container.clear_widgets()
        self.item_selected = []
        if self.botones:
            if self.columnas <= 0:
                self.container.cols = self.get_colums(len(self.botones))
            else:
                self.container.cols  = self.columnas
            for i in range(len(self.botones)):
                btn = self.botones[i]
                btnC = ButtonColor(text=btn.get('text'),
                                  bgColor=btn.get('color'),
                                  tag=btn, selectable=self.selectable)
                btnC.font_size = self.font_size
                btnC.bind(on_press=self.on_press)
                self.bind(selectable=btnC.setter('selectable'))
                self.container.add_widget(btnC)

    def get_colums(self, num):
        if num <= 5:
            return 1
        elif num > 5 and num < 10:
            return 3
        elif num >= 10:
            return 4

    def on_exit(self):
        self.onPress(self.item_selected)

    def on_button_enter_press(self, btn):
        if self.onPress:
            self.onPress(self.item_selected)

    def on_press(self, btn):
        if self.selectable:
            if not btn.selected:
                self.item_selected.append(btn)
            else:
                self.item_selected.remove(btn)
        elif self.onPress:
            self.onPress([btn])
