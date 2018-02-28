# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 23-Feb-2018
# @License: Apache license vesion 2.0



from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from glob import glob
from os import rename
from time import strftime
from controllers.lineaarqueo import LineaArqueo
from valle_libs.tpv.impresora import DocPrint
from valle_libs.utils import parse_float

from modals import Aceptar
from models.db import Arqueos, Pedidos, Conteo, Gastos, PedidosExtra
import threading

Builder.load_file("view/arqueo.kv")

class Arqueo(AnchorLayout):
    tpv = ObjectProperty(None)
    text_cambio = StringProperty("300")

    def nuevo_arqueo(self):
        self.lista_conteo = []
        self.lista_gastos = []
        self.lista_ticket = []
        self.lista_ingresos = []
        self.fecha = ""
        self.cambio = 300.00
        self.caja_dia = 0.0
        self.efectivo = 0.0
        self.tarjeta = 0.0
        self.total_gastos = 0.0
        self.conteo.rm_all_widgets()
        self.gastos.rm_all_widgets()
        self.ingresos.rm_all_widgets()
        pd = Pedidos.filter(query="estado LIKE 'NPG_%'")
        if len(pd) > 0:
            self.aceptar = Aceptar(onExit=self.salir_arqueo)
            self.aceptar.open()
        else:
            threading.Thread(target=self.get_ticket).start()


    def salir_arqueo(self):
        if self.aceptar != None:
            self.aceptar.dismiss()
        self.tpv.mostrar_inicio()

    def get_ticket(self):
        for tk in Pedidos.filter(query="estado LIKE 'PG_%'"):
            self.lista_ticket.append(tk)
            self.caja_dia += tk.total
            if tk.modo_pago == "Tarjeta":
                self.tarjeta += tk.total

    def arquear(self):
        self.tpv.show_spin()
        self.tpv.mostrar_inicio()
        threading.Thread(target=self.run_arqueo).start()

    def run_arqueo(self):
        arqueo = Arqueos()
        if self.cambio == "":
            self.cambio = 300.00
        self.efectivo = self.efectivo - parse_float(self.cambio)
        descuadre =  (self.total_gastos +
                      self.efectivo + self.tarjeta) - self.caja_dia
        self.lista_conteo = sorted(self.lista_conteo, key=lambda k: k["tipo"],
                                   reverse=True)
        arqueo.save(caja_dia=self.caja_dia,
                    efectivo=self.efectivo,
                    cambio=self.cambio,
                    total_gastos=self.total_gastos,
                    tarjeta=self.tarjeta,
                    descuadre=descuadre)
        for tk in self.lista_ticket:
            tk.estado = "arqueado"
            arqueo.pedidos.add(tk)

        for conteo in self.lista_conteo:
            c = Conteo(**conteo)
            c.save()
            arqueo.conteo.add(c)

        for gastos in self.lista_gastos:
            g = Gastos(**gastos)
            g.save()
            arqueo.gastos.add(g)

        for ingreso in self.lista_ingresos:
            ing = PedidosExtra(**ingreso)
            ing.save()
            arqueo.pedidosextra.add(ing)

        self.fecha = arqueo.fecha
        self.imprime_desglose()

    def imprime_desglose(self):
        desglose = []
        retirar = 0
        for ls in self.lista_conteo:
            if self.efectivo - retirar > 0.1:
                total_linea = ls["total"]
                subtotal = retirar + total_linea
                if subtotal <= self.efectivo:
                    retirar += total_linea
                    desglose.append(ls)
                else:
                    subtotal = self.efectivo - retirar
                    tipo = parse_float(ls["tipo"])
                    num = int(subtotal/tipo)
                    if num > 0:
                        total_linea = num * tipo
                        retirar += total_linea
                        desglose.append({"can": num, "tipo": tipo,
                                         "total": total_linea,
                                         "texto_tipo": ls["texto_tipo"]})
            else:
                break

        self.tpv.hide_spin()
        printDoc = DocPrint()
        printDoc.printDesglose("caja", self.fecha, desglose)



    def add_conteo(self, _can, _tipo):
        can = _can.text
        tipo = parse_float(_tipo.text)
        _can.text = _tipo.text = ""
        linea = LineaArqueo(borrar=self.borrar_conteo)
        texto_tipo = "Monedas" if tipo < 5 else "Billetes"
        linea.text = u"{0: >5} {1} de {2}".format(can, texto_tipo, tipo)
        linea.total = parse_float(can) * tipo
        linea.tag = {"can": can, "tipo": tipo,
                     "texto_tipo": texto_tipo,
                     "total": linea.total}
        self.efectivo += linea.total
        self.lista_conteo.append(linea.tag)
        self.conteo.add_linea(linea)

    def borrar_conteo(self, linea):
        self.efectivo -= linea.total
        self.lista_conteo.remove(linea.tag)
        self.conteo.rm_linea(linea)

    def add_gasto(self, _des, _gasto):
        des = _des.text
        gasto = _gasto.text
        _des.text = _gasto.text = ""
        linea = LineaArqueo(borrar=self.borrar_gasto)
        linea.text = u"{0}  ".format(des)
        linea.total = parse_float(gasto)
        linea.tag = {"des": des, "gasto": gasto}
        self.total_gastos += linea.total
        self.lista_gastos.append(linea.tag)
        self.gastos.add_linea(linea)

    def borrar_gasto(self, linea):
        self.total_gastos -= linea.total
        self.lista_gastos.remove(linea.tag)
        self.gastos.rm_linea(linea)

    def add_ingreso(self, num_pd, importe, modo_pago):
        _num_pd = num_pd.text
        _importe = importe.text
        linea = LineaArqueo(borrar=self.borrar_ingreso)
        _modo_pago = "Efectivo" if not modo_pago.active else "Tarjeta"
        linea.text = u"Peddos {0} modo pago {1}  ".format(_num_pd, _modo_pago)
        linea.total = parse_float(_importe)
        linea.tag = {"numero_pedido": _num_pd, "importe": _importe,
                     "modo_pago": _modo_pago, "estado": "arqueado"}
        if _modo_pago == "Tarjeta":
            self.tarjeta += linea.total
        self.caja_dia += linea.total
        num_pd.text = importe.text = ""
        modo_pago.active = False
        self.lista_ingresos.append(linea.tag)
        self.ingresos.add_linea(linea)

    def borrar_ingreso(self, linea):
        modo_pago = linea.tag.get("modo_pago")
        if modo_pago == "Tarjeta":
            self.tarjeta -= linea.total
        self.caja_dia -= linea.total
        self.lista_ingresos.remove(linea.tag)
        self.ingresos.rm_linea(linea)
