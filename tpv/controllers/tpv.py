# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 18-Sep-2017
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
from valle_libs.tpv.impresora import DocPrint
from controllers import (Inicio, PedidoController, ListadoWidget,
                         ListadoPdWidget, ListadoParking,
                         ClientesController, Arqueo)
from kivy.clock import Clock
from glob import glob
from os import rename, path
from datetime import datetime
import threading

Builder.load_file('view/tpv.kv')

class Tpv(AnchorLayout):

    def __init__(self, **kargs):
        super(Tpv, self).__init__(**kargs)
        self.inicio = Inicio(tpv=self)
        self.pedido = PedidoController(tpv=self)
        self.pendientes = ListadoPdWidget(tpv=self)
        self.listado = ListadoWidget(tpv=self)
        self.clientes = ClientesController(tpv=self)
        self.parking = ListadoParking(tpv=self)
        self.arqueo = Arqueo(tpv=self)
        self.content.add_widget(self.inicio)
        self.docPrint = DocPrint()

    def onPress_seccion(self, btns):
        for btn in btns:
            tipo = btn.tag.get('tipo')
            if tipo == 'clase':
                self.content.remove_widget(self.inicio)
                self.content.add_widget(self.pedido)
                self.pedido.nuevo_pedido(btn.tag)

    def pedir_domicilio(self, dbCliente):
        dbCliente.save()
        self.content.clear_widgets()
        self.pedido.pedido_domicilio(dbCliente)
        self.content.add_widget(self.pedido)


    def imprimirTicket(self, pd):
        self.pd = pd
        threading.Thread(target=self.imprimir).start()

    def imprimir(self):
        llevar = self.pd.para_llevar
        cl = None
        if llevar == "Domicilio":
            cl = self.pd.clientes.get()

        self.docPrint.imprimirTicket("caja", self.pd.id,
                                     self.pd.lineaspedido.get(), self.pd.fecha,
                                     self.pd.total, float(self.pd.entrega),
                                     float(self.pd.cambio), cl)


    def abrir_cajon(self):
        threading.Thread(target=self.cash_asincrono).start()


    def cash_asincrono(self):
        self.docPrint.abrir_cajon('caja')



    def recuperar_pedido(self, db):
        self.pedido.recuperar_pedido(db)
        self.content.clear_widgets()
        self.content.add_widget(self.pedido)

    def mostrar_inicio(self):
        self.sync_db()
        self.content.clear_widgets()
        self.content.add_widget(self.inicio)

    def mostrar_pedidos(self):
        self.listado.mostrar_lista()
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

    def mostrar_parking(self):
        self.parking.mostrar_lista()
        self.content.remove_widget(self.inicio)
        self.content.add_widget(self.parking)

    def sync_db(self):
        threading.Thread(target=self.run_sync_db).start()

    def run_sync_db(self):
        import os
        os.system("python ./syncdb_send.py")



    def refresh(self):
        threading.Thread(target=self.run_refresh).start()

    def run_refresh(self):
        import os
        os.system("python ./syncdb.py")
