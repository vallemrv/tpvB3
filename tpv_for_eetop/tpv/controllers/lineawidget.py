# -*- coding: utf-8 -*
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 06-Mar-2018
# @License: Apache license vesion 2.0

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.lang import Builder
from components.buttons import ButtonImg

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
    LabelClicable:
        on_press: root.click_sug()
        bgColor: "#3b434d"
        font_size: "15dp"
        color: "#f1eaea"
        text: "{0}  {1:.2f}".format(root.texto, root.total)
    ButtonImg:
        size_hint: None, 1
        width: self.height
        on_press: root.sumar(root, root.tag)
        src: './img/plus.ico'
    ButtonImg:
        size_hint: None, 1
        width: self.height
        on_press: root.borrar(root, root.tag)
        src: './img/menos.png'
        ''')

class LineaWidget(BoxLayout):
    tag = ObjectProperty(None, allownone=True)
    borrar = ObjectProperty(None, allownone=True)
    sumar = ObjectProperty(None, allownone=True)
    texto = StringProperty("")
    total = NumericProperty(0.0)
    sugerencia = ObjectProperty(None, allownone=True)
    promocion = ObjectProperty(None)
    aplicar = ObjectProperty(None)

    def __init__(self, **kargs):
        super(LineaWidget, self).__init__(**kargs)
        self.btnPromo = ButtonImg()
        self.btnPromo.size_hint = None, 1
        self.btnPromo.src = './img/promocion.jpeg'
        self.btnPromo.width = "50dp"
        self.btnPromo.bind(on_press=self.aplicar_promo)


    def mostar_btnpromo(self, mostrar=True):
        if mostrar:
            self.add_widget(self.btnPromo)
        else:
            self.remove_widget(self.btnPromo)

    def aplicar_promo(self, obj):
        self.tag.promocion = self.promocion
        self.remove_widget(self.btnPromo)
        if self.aplicar:
            self.aplicar(self)

    def click_sug(self):
        self.sugerencia(self, self.tag)
