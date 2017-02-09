# -*- coding: utf-8 -*-
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (BooleanProperty, StringProperty,
                             ObjectProperty, NumericProperty)
from kivy.lang import Builder
from valle.component.botoncolor import BotonColor

Builder.load_string('''
<Botonera>:
    anchor_x: 'center'
    anchor_x: 'center'
    GridLayout:
        size_hint: .9, .9
        cols: 1
        spacing: 20
        Label:
            id: _titulo
            color: 0, 0, 0, 1
            text: root.titulo
            font_size: 45
            size_hint: 1, None
            height: 35
        GridLayout:
            id: _contenedor
            cols: 1
            spacing: 5

''')


class Botonera(AnchorLayout):
    completo = BooleanProperty(True)
    font_size = NumericProperty(30)
    columnas = NumericProperty(0)
    titulo = StringProperty("Titulo")
    botones = ObjectProperty(None, allownone=True)
    onPress = ObjectProperty(allownone=False)
    selectable = BooleanProperty(False)

    def __init__(self, **kargs):
        super(Botonera, self).__init__(**kargs)

    def on_completo(self, key,  value):
        self.set_botones()

    def on_botones(self, key, value):
        self.set_botones()

    def set_botones(self):
        self.listBtn = []
        self.ids._contenedor.clear_widgets()
        if self.botones:
            if self.selectable:
                self.botones.append({"text": "Finalizar",
                                     "tipo": "exit",
                                     "color": "#BDBDBD"})
            if self.columnas <= 0:
                num_lineas = self.get_max_lienas(len(self.botones))
            else:
                num_lineas = self.columnas
            linea = 0
            box = BoxLayout(orientation='horizontal', spacing=5)
            self.ids._contenedor.add_widget(box)
            for i in range(len(self.botones)):
                btn = self.botones[i]
                if linea >= num_lineas:
                    linea = 0
                    box = BoxLayout(orientation='horizontal', spacing=5)
                    self.ids._contenedor.add_widget(box)
                btnC = BotonColor(text=btn.get('text'),
                                  bColor=btn.get('color'),
                                  tag=btn)
                btnC.font_size = self.font_size
                btnC.bind(on_press=self.on_press)
                box.add_widget(btnC)
                linea = linea + 1

    def get_max_lienas(self, num):
        if num <= 5 and not self.completo:
            return 1
        elif num > 5 and not self.completo:
            return 3
        else:
            return 4

    def on_press(self, btn):
        if self.selectable:
            tipo = btn.tag.get('tipo')
            if tipo != 'exit':
                if btn in self.listBtn:
                    self.listBtn.remove(btn)
                    btn.color = 1, 1, 1, 1
                else:
                    self.listBtn.append(btn)
                    btn.color = 1, 0, 0, 1
            else:
                self.onPress(self.listBtn)
        else:
            self.onPress([btn])
