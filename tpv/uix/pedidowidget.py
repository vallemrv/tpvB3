# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty, NumericProperty
from kivy.lang import Builder

from shared.botonera import Botonera
from shared.utils import json_to_list
from models.pedido import Pedido


Builder.load_file('./uix/pedidowidget.kv')

class PedidoWidget(BoxLayout):
    tpv = ObjectProperty(None, allownone=True)
    pedido = ObjectProperty(None, allownone=True)
    total = NumericProperty(0.0)

    def __init__(self, **kargs):
        super(PedidoWidget, self).__init__(**kargs)
        self.clase = None
        self.storage = None

    def onPress(self, btn):
        tipo = btn.tag.get('tipo')
        if tipo == 'clase':
            self.clase = btn.tag
            self.clase = clase
            self.show_botonera(self.clase.get('productos'))
        else:
            self.pedido.add_modificador(btn.tag)
            self.precio = self.pd.precio_total
            self.show_botonera(cod)

    def show_botonera(self, db):
        self.storage = JsonStore(db)
        if self.storage.exists('titulo'):
            self.ids._botonera.titulo = str(self.storage['titulo'].get('text'))
            self.ids._botonera.botones = []
            self.ids._botonera.botones = json_to_list(
                                        self.storage['db'].get('lista'))


    def nuevo_pedido(self, clase):
        self.clase = clase
        self.show_botonera(self.clase.get('productos'))
        self.pedido = Pedido(add_linea=self.add_linea,
                             clear_linea=self.clear_linea)



    def clear_linea(self, widget=None):
        if not widget:
            self.ids._contenido_pedido.clear_widgets()
        else:
            self.ids._contenido_pedido.remove_widget(widget)

    def add_linea(self, widget):
        self.ids._contenido_pedido.add_widget(widget)
        self.ids._scroll.scroll_y = 0


    def hacer_pedido(self):
        if self.tpv:
            self.tpv.hacer_pedido(None)
