from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from shared.botonera import Botonera
from shared.utils import json_to_list
from kivy.clock import Clock


Builder.load_file('./uix/pedido.kv')

class ListaTeclados():
    pass

class LineaPedido(BoxLayout):
    pass

class Pedido(BoxLayout):
    tpv = ObjectProperty(None, allownone=True)
    pd = ObjectProperty(None, allownone=True)

    def __init__(self, **kargs):
        super(Pedido, self).__init__(**kargs)
        self.teclados = ListaTeclados()
        Clock.schedule_once(self.crear_botoneras, 0.5)


    def onPress(self, btn):
        self.ids._contenido_pedido.add_widget(LineaPedido())

    def show_botonera(self, code):
        self.pd = None
        self.ids._contenido_pedido.clear_widgets()
        self.ids._botoneras.clear_widgets()
        if code == 'pizzas':
            self.ids._botoneras.add_widget(self.teclados.pizzas)
        if code == 'burger':
            self.ids._botoneras.add_widget(self.teclados.burger)
        if code == 'seccion':
            self.ids._botoneras.add_widget(self.teclados.secciones)
    def hacer_pedido(self):
        if self.tpv:
            self.tpv.hacer_pedido(self.pd)

    def crear_botoneras(self, tr):
        src = json_to_list(JsonStore('db/pizzas.json'))
        self.teclados.pizzas = self.teclado(False, src, "Pizzas", 20)
        src = json_to_list(JsonStore('db/burger.json'))
        self.teclados.burger = self.teclado(False, src, "Burger", 20)
        src = json_to_list(JsonStore('db/secciones.json'))
        self.teclados.secciones = self.teclado(False, src, "Secciones", 20)


    def teclado(self, comp, src, titulo, font_size):
        btns = Botonera(onPress=self.onPress, font_size=20)
        btns.completo = False
        btns.botones = src
        btns.titulo = 'Pizzas'
        return btns
