# -*- coding: utf-8 -*-
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder


Builder.load_string('''
<Menu>:
    size_hint: .8, .8
    cols: 1
    spacing: 5
    Label:
        size_hint_y: .2
        color: 0,0,0,1
        text: "Utilidades de gestión"
        font_size: 30
    GridLayout:
        cols: 3
        spacing: 5
        Button:
            text: 'Familias'
            on_press: root.edit_clases()
        Button:
            text: 'Productos'
            on_press: root.edit_productos()
        Button:
            text: 'No implenetado'
        Button:
            text: 'No implenetado'
        Button:
            text: 'No implenetado'
        Button:
            text: 'No implenetado'

''')

class Menu(GridLayout):
    edit_clases = ObjectProperty(None, allownone=True)
    edit_productos = ObjectProperty(None, allownone=True)
    def __init__(self, **kargs):
        super(Menu, self).__init__(**kargs)
