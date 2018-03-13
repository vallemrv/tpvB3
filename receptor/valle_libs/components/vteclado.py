# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 11-Jul-2017
# @License: Apache license vesion 2.0


from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import (StringProperty, NumericProperty,
                             ObjectProperty)
from kivy.lang import Builder
from components.botoncolor import ButtonColor
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)



Builder.load_string('''
<VTeclado>:
    GridLayout:
        cols: 1
        spacing: 5
        id: _contenedor
                    ''')


class VTeclado(AnchorLayout):
    tipo = StringProperty('')
    font_size = NumericProperty(24)
    texto = StringProperty("")
    exit = ObjectProperty(None, allownone=True)
    onChange = ObjectProperty(None, allownone=True)

    def __init__(self, **kargs):
        super(VTeclado, self).__init__(**kargs)
        self.db = JsonStore(dname+'/teclados.json')
        self.bind(tipo=self.on_tipo)
        self.teclas = []


    def on_tipo(self, key, value):
        self.build_teclado()

    def build_teclado(self):
        self.listBtn = self.db[self.tipo].get('db')
        self.ids._contenedor.clear_widgets()
        self.teclas = []
        if len(self.listBtn) > 0:
            num_lineas = 11
            on_press = self.on_press_letras
            if self.tipo == 'numeros':
                num_lineas = 3
                on_press = self.on_press_num
            linea = 0
            box = BoxLayout(orientation='horizontal', spacing=5)
            self.ids._contenedor.add_widget(box)
            for i in range(len(self.listBtn)):
                btn = self.listBtn[i]
                if linea >= num_lineas:
                    linea = 0
                    box = BoxLayout(orientation='horizontal', spacing=5)
                    self.ids._contenedor.add_widget(box)
                btnC = ButtonColor(text=btn,
                                  bColor="#333333",
                                  tag=btn)
                btnC.font_size = self.font_size
                btnC.bind(on_press=on_press)
                self.teclas.append(btnC)
                box.add_widget(btnC)
                linea = linea + 1

    def on_press_letras(self, key):
        if key.text == 'mayus':
            for btn in self.teclas:
                btn.text = btn.text.upper()
        elif key.text == 'MAYUS':
            for btn in self.teclas:
                btn.text = btn.text.lower()
        elif key.text == '<--':
            self.texto = self.texto[:-1]
        elif key.text == "[ ]":
            self.texto = self.texto + " "
        elif key.text == "FIN" or key.text == "Fin" or key.text == "fin":
            if self.exit:
                self.exit()
        else:
            self.texto = self.texto + key.text

        if self.onChange:
            self.onChange(self.texto)
