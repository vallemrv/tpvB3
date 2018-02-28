# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 21-Feb-2018
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
from valle_libs.tpv.impresora import DocPrint
from controllers import (Inicio, PedidoController, ListadoWidget,
                         ListadoPdWidget, ListadoParking,
                         ClientesController, Arqueo)
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from glob import glob
from os import rename, path
from datetime import datetime
import threading

Builder.load_file('view/tpv.kv')

class MensajeCobro(AnchorLayout):
    tpv = ObjectProperty(None)
    text = StringProperty("Cambio 0.00 €")
    def __init__(self, tpv,  **kargs):
        super(MensajeCobro, self).__init__(**kargs)
        self.tpv = tpv

    def show(self, men):
        self.text = men
        self.tpv.mensajes.add_widget(self)
        Clock.schedule_once(self.run_hidde, 15)

    def hidden(self):
        self.tpv.mensajes.remove_widget(self)

    def run_hidde(self, dt):
        self.tpv.hidden_men_cobro()

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
        self.men_cobro = None

    def on_width(self, w, val):
        self.spin.width = self.width
        self.hide_spin()

    def mostrar_men_cobro(self, men):
        self.hidden_men_cobro()
        self.men_cobro = MensajeCobro(self)
        self.men_cobro.show(men)

    def hidden_men_cobro(self):
        if self.men_cobro != None:
            self.men_cobro.hidden()
            self.men_cobro = None

    def show_spin(self):
        self.spin.show()

    def hide_spin(self):
        self.spin.hide()

    def onPress_seccion(self, btns):
        self.hidden_men_cobro()
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
        if type(pd) == dict:
            self.pd = pd.get("db")
        else:
            self.pd = pd
        threading.Thread(target=self.imprimir).start()

    def imprimir(self):
        llevar = self.pd.para_llevar
        cl = None
        if llevar == "Domicilio":
            cl = self.pd.clientes_set.get()

        self.docPrint.imprimirTicket("caja", self.pd.id,
                                     self.pd.lineaspedido_set.get(), self.pd.fecha,
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
        self.hidden_men_cobro()
        self.listado.mostrar_lista()
        self.content.remove_widget(self.inicio)
        self.content.add_widget(self.listado)

    def mostrar_domicilio(self):
        self.hidden_men_cobro()
        self.content.remove_widget(self.inicio)
        self.clientes.show_find()
        self.content.add_widget(self.clientes)

    def mostrar_arqueo(self):
        self.hidden_men_cobro()
        self.arqueo.nuevo_arqueo()
        self.content.remove_widget(self.inicio)
        self.content.add_widget(self.arqueo)


    def mostrar_pendientes(self):
        self.hidden_men_cobro()
        self.pendientes.mostrar_lista()
        self.content.remove_widget(self.inicio)
        self.content.add_widget(self.pendientes)

    def mostrar_parking(self):
        self.hidden_men_cobro()
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
