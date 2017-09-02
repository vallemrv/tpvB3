# -*- coding: utf-8 -*
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.lang import Builder
from valle.component.botonimg import BotonImg

Builder.load_string('''
#:import BotonImg valle.component.botonimg.BotonImg
#:import LabelClicable valle.component.labelclicable.LabelClicable
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
        event: root.click_sug
        color: .9,.9,.9,1
        font_size: 16
        texto: "{0}  {1:.2f}".format(root.texto, root.total)
    BotonImg:
        size_hint: None, 1
        width: self.height
        on_press: root.sumar(root, root.tag)
        src: './img/plus.ico'
    BotonImg:
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
        self.btnPromo = BotonImg()
        self.btnPromo.size_hint = None, 1
        self.btnPromo.src = './img/promocion.jpeg'
        self.btnPromo.width = self.btnPromo.height
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

    def click_sug(self, btn):
        self.sugerencia(self, self.tag)