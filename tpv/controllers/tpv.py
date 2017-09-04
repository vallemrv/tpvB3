# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 04-Sep-2017
# @License: Apache license vesion 2.0


# -*- coding: utf-8 -*-
from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
from valle_libs.tpv.impresora import DocPrint
from controllers.inicio import Inicio
from controllers.pedido import PedidoController
from controllers.listadowidget import ListadoWidget
from controllers.listadopdwidget import ListadoPdWidget
from controllers.clientes import ClientesController
from controllers.arqueo import Arqueo
from kivy.clock import Clock
from glob import glob
from os import rename

Builder.load_file('view/tpv.kv')

class Tpv(AnchorLayout):

    def __init__(self, **kargs):
        super(Tpv, self).__init__(**kargs)
        self.inicio = Inicio(tpv=self)
        self.pedido = PedidoController(tpv=self)
        self.pendientes = ListadoPdWidget(tpv=self)
        self.listado = ListadoWidget(tpv=self)
        self.clientes = ClientesController(tpv=self)
        self.arqueo = Arqueo(tpv=self)
        self.content.add_widget(self.inicio)
        self.docPrint = DocPrint()
        Clock.schedule_once(self.enviar_pedido, .5)

    def onPress_seccion(self, btns):
        for btn in btns:
            tipo = btn.tag.get('tipo')
            if tipo == 'clase':
                self.content.remove_widget(self.inicio)
                self.content.add_widget(self.pedido)
                self.pedido.nuevo_pedido(btn.tag)

    def pedir_domicilio(self, num_tlf):
        self.content.clear_widgets()
        self.pedido.pedido_domicilio(num_tlf)
        self.content.add_widget(self.pedido)


    def imprimirTicket(self, pd):
        tk = pd['reg']
        llevar = tk.get('para_llevar')
        cl = None
        if llevar == "Domicilio":
            num_tlf = tk.get("num_tlf")
            cl = JsonStore("db/clientes/{0}.json".format(num_tlf))
            cl = cl['reg']

        self.docPrint.imprimirTicket("caja", tk.get('numTicket'),
                                     tk.get('lineas'), tk.get('fecha'),
                                     tk.get('total'), cl)

    def abrir_cajon(self):
        self.docPrint.initDoc()
        self.docPrint.abrir_cajon('caja')

    def enviar_pedido(self, pd):
        list = glob('db/pd/*.00.json')
        for l in list:
            db = l.replace(".00.", ".11.")
            rename(l, db)
            st = JsonStore(db)
            if st.exists('reg'):
                tk = st['reg']
                self.docPrint.printPedido("cocina", tk.get('num_avisador'),
                                          tk.get('lineas'), tk.get('fecha'),
                                          tk.get('para_llevar'))
        Clock.schedule_once(self.enviar_pedido, .5)

    def mostrar_inicio(self):
        self.content.clear_widgets()
        self.content.add_widget(self.inicio)

    def mostrar_pedidos(self):
        self.listado.stop_refresh()
        self.content.remove_widget(self.inicio)
        self.content.add_widget(self.listado)

    def mostrar_domicilio(self):
        self.content.remove_widget(self.inicio)
        self.clientes.show_find()
        self.content.add_widget(self.clientes)

    def mostrar_arqueo(self):
        self.arqueo.nuevo_arqueo()
        self.content.remove_widget(self.inicio)
        self.content.add_widget(self.arqueo)


    def mostrar_pendientes(self):
        self.pendientes.mostrar_lista()
        self.content.remove_widget(self.inicio)
        self.content.add_widget(self.pendientes)
