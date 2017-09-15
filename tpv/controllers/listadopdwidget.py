# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 15-Sep-2017
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.lang import Builder
from kivy.clock import Clock
from glob import glob
from os import rename
from components.labels import LabelClicable
from models.db.pedidos import Pedidos
from modals import Efectivo
from datetime import datetime
from valle_libs.tpv.impresora import DocPrint


Builder.load_file('view/listadopdwidget.kv')


class ListadoPdWidget(AnchorLayout):
    tpv = ObjectProperty(None)
    precio = NumericProperty(0)
    des = StringProperty('Pedido')



    def __init__(self, **kargs):
        super(ListadoPdWidget, self).__init__(**kargs)
        self.selected = None
        self.file = None
        self.efectivo = Efectivo(onExit=self.salir_efectivo)

    def cobrar_targeta(self):
        if self.selected:
            pd = self.selected.get("db")
            pd.modo_pago = "Efectivo"
            pd.efectivo = 0.00
            pd.cambio = 0.00
            pd.estado = "PG_SI"
            pd.save()
            self.tpv.abrir_cajon()
            self.tpv.mostrar_inicio()

    def mostrar_efectivo(self):
        self.efectivo.total = str(self.precio)
        self.efectivo.open()

    def salir_efectivo(self, cancelar=True):
        if cancelar == False:
            pd = self.selected.get("db")
            pd.modo_pago = "Efectivo"
            pd.efectivo = self.efectivo.efectivo.replace("€", "")
            pd.cambio = self.efectivo.cambio.replace("€", "")
            pd.estado = "PG_SI"
            pd.save()
            self.tpv.abrir_cajon()
            self.tpv.mostrar_inicio()
        self.efectivo.dismiss()

    def salir(self):
        self.tpv.mostrar_inicio()

    def clear_self_widget(self):
        self.selected = None
        self.precio = 0
        self.pedido.rm_all_widgets()


    def mostrar_lista(self):
        self.lista.rm_all_widgets()
        self.pedido.rm_all_widgets()

        for db in Pedidos().getAll(query="estado LIKE 'NPG_%'"):
            clientes = db.clientes.get()
            direccion = ""
            if len(clientes) > 0:
                id = clientes[0].id
                if id != None:
                    direccion = clientes[0].direcciones.get(query="id=%d"%id)[0].direccion

            btn = LabelClicable(bgColor="#444444",
                                font_size="16dp",
                                color="#ffffff")
            btn.tag = {"db": db}
            if type(db.fecha) is datetime:
                fecha = db.fecha.strftime("%H:%M:%S")
            else:
                fecha = datetime.strptime(db.fecha, "%Y-%m-%d %H:%M:%S.%f")
                fecha = fecha.strftime("%H:%M:%S")

            texto = "{0: >25} {2}  Total: {1:5.2f} €".format(fecha, db.total, direccion)
            btn.text = texto
            btn.bind(on_press=self.onPress)
            self.lista.add_linea(btn)

    def onPress(self, btn):
        self.pedido.rm_all_widgets()
        self.selected = btn.tag
        lineas = self.selected.get("db").lineaspedido.get()
        total = 0
        for item in lineas:
            btn = LabelClicable(bgColor="#444444",
                                font_size = '16dp',
                                color = "#ffffff")
            tl = item.total
            total += tl
            tipo = "" if not item.tipo in ("pizzas", "burger") else item.tipo
            if tipo.endswith("s"):
                tipo = tipo[:-1]
            btn.text = "{0: >4}  {4} {1} {2: <30}  {3:.2f} €".format(item.cant, item.text,
                                                                    item.des.lower(), tl, tipo)
            self.pedido.add_linea(btn)
        self.precio = total

    def cobrar(self):
        if self.selected != None:
            self.mostrar_efectivo()


    def imprimirTk(self):
        self.salir()
        Clock.schedule_once(self.imprimirTicket, .5)

    def imprimirTicket(self, dt):
        if self.selected:
            pd = self.selected.get("db")
            llevar = pd.para_llevar
            cl = None
            if llevar == "Domicilio":
                cl = pd.clientes.get()

            docPrint = DocPrint()
            docPrint.imprimirTicket("caja", pd.id,
                                     pd.lineaspedido.get(), pd.fecha,
                                     pd.total, pd.entrega, pd.cambio, cl)
