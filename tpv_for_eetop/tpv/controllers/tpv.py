# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 16-Mar-2018
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
from valle_libs.tpv.impresora import DocPrint
from controllers import (Inicio, PedidoController, ListadoWidget,
                         ListadoPdWidget, ListadoParking,
                         ClientesController, Arqueo)
from kivy.clock import Clock
from kivy.lib import osc
from kivy.properties import ObjectProperty, StringProperty
from config import config
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
        self.content.clear_widgets()
        self.pedido.pedido_domicilio(dbCliente)
        self.content.add_widget(self.pedido)


    def imprimirTicket(self, pd, result):
        if result["success"] == True:
            pd = result["add"]["pedidos"]
            for p in pd:
                cl = p["clientes"] if "clientes" in p else None
                self.docPrint.imprimirTicket("caja", p["id"],
                                             p["lineaspedido"], p["fecha"],
                                             float(p["total"]), float(p["entrega"]),
                                             float(p['cambio']), cl)

    def imprimir_directo(self, pd):
        cl = pd["clientes"] if "clientes" in pd else None
        self.docPrint.imprimirTicket("caja", pd["id"],
                                     pd["lineaspedido"], pd["fecha"],
                                     float(pd["total"]), float(pd["entrega"]),
                                     float(pd['cambio']), cl)

    def abrir_cajon(self):
        threading.Thread(target=self.cash_asynchrono).start()

    def cash_asynchrono(self):
        self.docPrint.abrir_cajon('caja')

    def recuperar_pedido(self, db):
        self.pedido.recuperar_pedido(db)
        self.content.clear_widgets()
        self.content.add_widget(self.pedido)

    def mostrar_inicio(self):
        self.content.clear_widgets()
        self.inicio.show_button_inicio()
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

    def run_sync_db(self, dt):
        self.inicio.show_button_inicio()

    def refresh(self):
        threading.Thread(target=self.run_refresh).start()

    def run_refresh(self):
        import os
        os.system("python ./syncdb.py")
        Clock.schedule_once(self.run_sync_db, .1)
