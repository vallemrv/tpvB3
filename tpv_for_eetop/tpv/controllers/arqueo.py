# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 17-Mar-2018
# @License: Apache license vesion 2.0



from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.core import Logger
from kivy.network.urlrequest import UrlRequest
from controllers.lineaarqueo import LineaArqueo
from valle_libs.tpv.impresora import DocPrint
from valle_libs.utils import parse_float
from models.db import QSon, VentasSender
from config import config
from modals import Aceptar
from glob import glob
from os import rename
from datetime import datetime
from time import strftime
import urllib
import threading
import json


Builder.load_file("view/arqueo.kv")

class Arqueo(AnchorLayout):
    tpv = ObjectProperty(None)
    text_cambio = StringProperty("300")
    url = config.URL_SERVER+"/ventas/arquear/"


    def __on_success__(self, req, result):
        self.tpv.hide_spin()
        if result["success"] == True:
            desglose = result["desglose"]
            self.tpv.mostrar_inicio()
            printDoc = DocPrint()
            printDoc.printDesglose("caja", self.fecha, desglose)



    def __got_error__(self, req,  *args):
        req._resp_status = "Error"
        Logger.debug("got error {0}".format(req.url))
        self.tpv.hide_spin()

    def __got_fail__(self, req, *args):
        req._resp_status = "Fail"
        Logger.debug("got fail {0}".format(req.url))
        self.tpv.hide_spin()

    def __got_redirect__(self, req, *args):
        req._resp_status = "Redirect"
        Logger.debug("got redirect {0}".format(req.url))
        self.tpv.hide_spin()


    def send(self, data):
        SEND_DATA = {'data':json.dumps(data)}
        data = urllib.urlencode(SEND_DATA)
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/json'}
        r = UrlRequest(self.url, on_success=self.__on_success__, req_body=data,
                       req_headers=headers, method="POST",
                       on_failure=self.__got_fail__,
                       on_error=self.__got_error__,
                       on_redirect=self.__got_redirect__)


    def nuevo_arqueo(self):
        self.lista_conteo = []
        self.lista_gastos = []
        self.lista_ticket = []
        self.lista_ingresos = []
        self.fecha = ""
        self.caja_dia = 0.0
        self.efectivo = 0.0
        self.tarjeta = 0.0
        self.total_gastos = 0.0
        self.conteo.rm_all_widgets()
        self.gastos.rm_all_widgets()
        self.ingresos.rm_all_widgets()
        sender = VentasSender()
        sender.filter(QSon("Pedidos", estado__contains="NPG"))
        sender.send(self.comprobar_npg, wait=False)

    def comprobar_npg(self, req, r):
        if r["success"] == True:
            if len(r["get"]['pedidos']) > 0:
                self.aceptar = Aceptar(onExit=self.salir_arqueo)
                self.aceptar.open()


    def salir_arqueo(self):
        if self.aceptar != None:
            self.aceptar.dismiss()
        self.tpv.mostrar_inicio()


    def arquear(self):
        self.fecha = str(datetime.now())
        if self.cambio == "":
            self.cambio = 300.00

        self.lista_conteo = sorted(self.lista_conteo, key=lambda k: k["tipo"],
                                   reverse=True)
        self.run_arqueo()


    def run_arqueo(self):
        arqueo = {'caja_dia': self.caja_dia,
                  'efectivo':self.efectivo,
                  'cambio':self.cambio,
                  'total_gastos':self.total_gastos,
                  'tarjeta':self.tarjeta,
                  'descuadre':0,
                  'conteo':[],
                  'gastos':[],
                  'extras': []}

        for conteo in self.lista_conteo:
            arqueo['conteo'].append(conteo)

        for gasto in self.lista_gastos:
            arqueo['gastos'].append(gasto)

        for ing in self.lista_ingresos:
            arqueo['extras'].append(ing)

        self.send(arqueo)
        self.tpv.show_spin()


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
        else:
            self.caja_dia += linea.total
        num_pd.text = importe.text = ""
        modo_pago.active = False
        self.lista_ingresos.append(linea.tag)
        self.ingresos.add_linea(linea)

    def borrar_ingreso(self, linea):
        modo_pago = linea.tag.get("modo_pago")
        if modo_pago == "Tarjeta":
            self.tarjeta -= linea.total
        else:
            self.caja_dia -= linea.total
        self.lista_ingresos.remove(linea.tag)
        self.ingresos.rm_linea(linea)
