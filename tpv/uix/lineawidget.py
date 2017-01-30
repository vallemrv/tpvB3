# -*- coding: utf-8 -*
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.lang import Builder

Builder.load_string('''
<LineaWidget>:
    canvas.before:
        Color:
            rgba: .3,.3,.3,1
        Rectangle:
            size: self.size
            pos: self.pos
    spacing: 5
    orientation: 'horizontal'
    Button:
        on_press: root.sugerencia(root, root.tag)
        AnchorLayout:
            anchor_y: 'center'
            anchor_x: 'left'
            size: self.parent.size
            pos: self.parent.pos
            padding: 5
            Label:
                color: .9,.9,.9,1
                font_size: 16
                text: "{0}  {1:.2f}".format(root.texto, root.total)
                text_size: self.size
                halign: 'left'
                valign: 'middle'
    Button:
        size_hint: None, 1
        width: self.height
        on_press: root.sumar(root, root.tag)
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'center'
            size: self.parent.size
            pos: self.parent.pos
            Image:
                source: './img/plus.ico'
                allow_stretch: True
                center: self.parent.center
                size: self.parent.width * .85, self.parent.height * .85
    Button:
        size_hint: None, 1
        width: self.height
        on_press: root.borrar(root, root.tag)
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'center'
            size: self.parent.size
            pos: self.parent.pos
            Image:
                source: './img/menos.png'
                allow_stretch: True
                center: self.parent.center
                size: self.parent.width * .85, self.parent.height * .85
''')

class LineaWidget(BoxLayout):
    tag = ObjectProperty(None, allownone=True)
    borrar = ObjectProperty(None, allownone=True)
    sumar = ObjectProperty(None, allownone=True)
    texto = StringProperty("")
    total = NumericProperty(0.0)
    sugerencia = ObjectProperty(None, allownone=True)
