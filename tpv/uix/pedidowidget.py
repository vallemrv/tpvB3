# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty, NumericProperty
from kivy.lang import Builder
from shared.lineawidget import LineaWidget
from shared.utils import json_to_list
from models.pedido import Pedido

Builder.load_file('./uix/pedidowidget.kv')

class PedidoWidget(BoxLayout):
    tpv = ObjectProperty(None, allownone=True)
    pedido = ObjectProperty(None, allownone=True)
    precio = NumericProperty(0.0)

    def __init__(self, **kargs):
        super(PedidoWidget, self).__init__(**kargs)
        self.clase = None
        self.puntero = 0
        self.linea_editable = None
        self.tipo_cobro = "Efectivo"

    def onPress(self, btn):
        tipo = btn.tag.get('tipo')
        if tipo == 'cobros':
            self.pedido.modo_pago = btn.tag.get("text")
            self.tpv.abrir_cajon()
            self.show_botonera("db/privado/num_avisador.json")
        elif tipo == 'num':
            self.pedido.num_avisador = btn.tag.get("text")
            self.pedido.guardar_pedido()
            self.tpv.mostrar_inicio()
        elif tipo == 'clase':
            self.clase = btn.tag
            self.puntero = 0
            self.show_botonera(self.clase.get('productos'))
        else:
            db = self.pedido.add_modificador(btn.tag)
            self.precio = self.pedido.total

            if not self.linea_editable:
                self.add_linea()

            self.refresh_linea()
            num = len(self.clase.get('preguntas'))
            if db:
                self.show_botonera(db)
            elif not db and self.puntero < num:
                db = self.clase.get('preguntas')[self.puntero]
                self.puntero = self.puntero + 1
                self.show_botonera(db)
            elif self.puntero >= num:
                self.pedido.add_linea()
                self.show_botonera("db/clases.json")
                self.linea_nueva()

    def linea_nueva(self):
        self.clase = None
        self.puntero = 0
        self.linea_editable = None
        self.ids._btnPedido.disabled = False

    def add_linea(self):
        self.ids._btnPedido.disabled = True
        if self.pedido.linea:
            self.linea_editable = LineaWidget(tag=self.pedido.linea,
                                              borrar=self.borrar)
            self.ids._contenido_pedido.add_widget(self.linea_editable)
            self.ids._scroll.scroll_y = 0

    def refresh_linea(self):
        if self.pedido.linea:
            self.linea_editable.texto = self.pedido.linea.getTexto()
            self.linea_editable.total = self.pedido.linea.getTotal()


    def borrar(self, widget, tag):
        self.show_botonera("db/clases.json")
        self.linea_nueva()
        self.pedido.borrar(tag)
        self.ids._contenido_pedido.remove_widget(widget)

    def show_botonera(self, db):
        self.storage = JsonStore(db)
        if self.storage.exists('titulo'):
            self.ids._botonera.titulo = str(self.storage['titulo'].get('text'))
            self.ids._botonera.botones = []
            self.ids._botonera.botones = json_to_list(
                                        self.storage['db'].get('lista'))


    def nuevo_pedido(self, clase):
        self.clase = clase
        self.puntero = 0
        self.linea_editable = None
        self.show_botonera(self.clase.get('productos'))
        self.ids._contenido_pedido.clear_widgets()
        self.pedido = Pedido()
        self.ids._btnPedido.disabled = True

    def cancelar_pedido(self):
        self.tpv.mostrar_inicio()

    def hacer_pedido(self):
        self.ids._btnPedido.disabled = True
        self.show_botonera('db/privado/cobrar.json')
