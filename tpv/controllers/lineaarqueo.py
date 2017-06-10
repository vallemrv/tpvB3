# -*- coding: utf-8 -*
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.lang import Builder

Builder.load_string('''
#:import BotonImg valle.component.botonimg.BotonImg
#:import LabelClicable valle.component.labelclicable.LabelClicable
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
    BotonImg:
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
