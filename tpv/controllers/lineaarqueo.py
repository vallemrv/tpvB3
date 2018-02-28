# -*- coding: utf-8 -*
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 21-Feb-2018
# @License: Apache license vesion 2.0


from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.lang import Builder

Builder.load_string('''
<LineaArqueo>:
    canvas.before:
        Color:
            rgba: .3,.3,.3,1
        Rectangle:
            size: self.size
            pos: self.pos
    spacing: 5
    orientation: 'horizontal'
    LabelClicable:
        bg_color: "#2f2f2f"
        color: "#999999"
        font_size: '16dp'
        text: "{0}  {1:.2f} €".format(root.text, root.total)
    ButtonImg:
        size_hint: None, 1
        width: self.height
        on_press: root.borrar(root)
        src: './img/menos.png'
        ''')

class LineaArqueo(BoxLayout):
    tag = ObjectProperty(None, allownone=True)
    borrar = ObjectProperty(None, allownone=True)
    text = StringProperty("")
    total = NumericProperty(0.0)
