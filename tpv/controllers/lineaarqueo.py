# -*- coding: utf-8 -*
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 04-Sep-2017
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
        color: .9,.9,.9, 1
        font_size: 16
        texto: str("  {0}  {1:.2f} €".format(root.texto, root.total)).decode("utf-8")
    ButtonImg:
        size_hint: None, 1
        width: self.height
        on_press: root.borrar(root)
        src: './img/menos.png'
        ''')

class LineaArqueo(BoxLayout):
    tag = ObjectProperty(None, allownone=True)
    borrar = ObjectProperty(None, allownone=True)
    texto = StringProperty("")
    total = NumericProperty(0.0)
