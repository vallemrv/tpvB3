# -*- coding: utf-8 -*-
from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty
from shared.botonera import Botonera
from shared.utils import json_to_list
from uix.pedidowidget import PedidoWidget
from kivy.clock import Clock
from shared.impresora import DocPrint
from glob import glob
from os import rename



class Inicio(AnchorLayout):
    onPress = ObjectProperty(None, allownone=True)

    def __init__(self, **kargs):
        super(Inicio, self).__init__(**kargs)
        self.botonera = Botonera(onPress=self.onPress)
        self.crear_inicio()
        self.add_widget(self.botonera)


    def crear_inicio(self):
        self.botonera.completo = True
        src = JsonStore('db/clases.json')
        src = json_to_list(src['db'].get('lista'))
        src.append({"text": "Abrir cajón", "tipo": "abrir_cajon",
                    "color": "#BDBDBD"})
        self.botonera.botones = src
        self.botonera.titulo = "Bienvenido"


class Tpv(AnchorLayout):

    def __init__(self, **kargs):
        super(Tpv, self).__init__(**kargs)
        self.inicio = Inicio(onPress=self.onPress_seccion)
        self.pedido = PedidoWidget(tpv=self)
        self.add_widget(self.inicio)
        self.docPrint = DocPrint()
        Clock.schedule_interval(self.enviar_pedido, .5)

    def onPress_seccion(self, boton):
        for btn in boton:
            tipo = btn.tag.get('tipo')
            if tipo == 'clase':
                self.remove_widget(self.inicio)
                self.add_widget(self.pedido)
                self.pedido.nuevo_pedido(btn.tag)
            elif tipo == "abrir_cajon":
                self.abrir_cajon()

    def imprimirTicket(self, pd):
        tk = pd['tk']['reg']
        self.docPrint.imprimirTicket("caja", tk.get('numTicket'),
                                     tk.get('lineas'), tk.get('fecha'),
                                     tk.get('total'))


    def abrir_cajon(self):
        self.docPrint.initDoc()
        self.docPrint.abrir_cajon('caja')

    def enviar_pedido(self, pd):
        list = glob('db/pd/*.00.json')
        for l in list:
            db = l.replace(".00.", ".11.")
            rename(l, db)
            st = JsonStore(db)
            if st.exists('tk'):
                tk = st['tk']['reg']
                self.docPrint.printPedido("cocina", tk.get('num_avisador'),
                                          tk.get('lineas'), tk.get('fecha'),
                                          tk.get('para_llevar'))

    def mostrar_inicio(self):
        self.remove_widget(self.pedido)
        self.add_widget(self.inicio)
