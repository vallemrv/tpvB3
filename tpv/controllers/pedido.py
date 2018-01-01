# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 26-Sep-2017
# @License: Apache license vesion 2.0

from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.lang import Builder
from controllers.lineawidget import LineaWidget
from modals import Sugerencias, Efectivo

from models.pedido import Pedido

Builder.load_file('view/pedido.kv')

class Wrap():
    def __init__(self, obj):
        self.tag = obj

class PedidoController(BoxLayout):
    tpv = ObjectProperty(None, allownone=True)
    pedido = ObjectProperty(None, allownone=True)
    total = NumericProperty(0.0)
    des = StringProperty("Pedido {0: >10} articulos".format(0))

    def __init__(self, **kargs):
        super(PedidoController, self).__init__(**kargs)
        self.clase = None
        self.puntero = 0
        self.pilaDeStados = []
        self.linea_editable = None
        self.tipo_cobro = "Efectivo"
        self.dbCliente = None
        self.promocion = None
        self.modal = Sugerencias(onExit=self.exit_sug)
        self.efectivo = Efectivo(onExit=self.salir_efectivo)

    def on_pedido(self, key, value):
        self.pedido.bind(total=self.show_total)

    def show_total(self, key, value):
        self.total = self.pedido.total
        self.des = "Pedido {0: >10} articulos".format(
                    self.pedido.getNumArt())

    def pedido_domicilio(self, db):
        self.dbCliente = db
        self.lista.rm_all_widgets()
        self.pedido = Pedido()
        self.btnPedido.disabled = True
        self.btnAtras.disabled = False
        self.total = 0
        self.des = "Pedido {0: >10} articulos".format(0)
        self.linea_nueva()

    def onPress(self, botones):
        for i in range(len(botones)):
            btn = botones[i]
            tipo = btn.tag.get('tipo')
            if tipo == 'cobros':
                self.pedido.modo_pago = btn.tag.get("text")
                if self.pedido.modo_pago == "Efectivo":
                    self.mostrar_efectivo()
                else:
                    self.pedido.cambio = 0.00
                    self.pedido.efectivo = 0.00
                    self.tpv.imprimirTicket(self.pedido.guardar_pedido())
                    self.tpv.mostrar_inicio()

            elif tipo == 'llevar':
                self.show_botonera('../db/privado/num_avisador.json')
                self.pedido.para_llevar = btn.tag.get('text')
                if self.pedido.para_llevar == "Para recoger":
                    self.pedido.para_llevar = "Para llevar"
                    self.pedido.num_avisador = "Para recoger"
                    self.pedido.modo_pago = "Efectivo"
                    self.pedido.cambio = 0.00
                    self.pedido.efectivo = 0.00
                    self.pedido.guardar_pedido()
                    self.tpv.mostrar_inicio()

            elif tipo == 'num':
                self.show_botonera('../db/privado/cobrar.json')
                self.pedido.num_avisador = btn.tag.get("text")
            elif tipo == 'clase':
                self.clase = btn.tag
                if "promocion" in self.clase:
                    self.promocion = self.clase["promocion"]
                self.puntero = 0
                name = self.clase.get('productos')
                db = "../db/productos/%s.json" % name
                self.show_botonera(db)
                self.linea_editable = None
                self.pilaDeStados = []
                self.pilaDeStados.append({'db': db, 'punt': 0,
                                          'pass': 1})
                self.btnAtras.disabled = False
            else:
                if "precio" in self.clase:
                    btn.tag["precio"] = btn.tag["precio"] * self.clase["precio"]
                db = self.pedido.add_modificador(btn.tag)
                if not self.linea_editable:
                    self.add_linea()
                self.refresh_linea()
                num = len(self.clase.get('preguntas')) if self.clase else 0
                ps = len(botones) - 1
                if db != None:
                    self.show_botonera(db)
                elif db == None and self.puntero < num and i == ps:
                    db = None
                    igDb = False
                    while self.puntero < num:
                        name = self.clase.get('preguntas')[self.puntero]
                        db = "../db/preguntas/%s.json" %  name
                        self.puntero += 1
                        if 'ignore' in btn.tag:
                            if db not in btn.tag.get('ignore'):
                                igDb = False
                                break
                            else:
                                igDb = True
                                db = None
                        else:
                            break

                    if not igDb:
                        self.show_botonera(db)
                    else:
                        self.puntero += 1

                if not db and self.puntero >= num and i == ps:
                    self.linea_nueva()

                if i == ps:
                    self.pilaDeStados.append({'db': db, 'punt': self.puntero,
                                              'pass': len(botones)})


    def mostrar_efectivo(self):
        self.efectivo.total = str(self.total)
        self.efectivo.open()

    def salir_efectivo(self, cancelar=True):
        self.efectivo.dismiss()
        if cancelar:
            self.show_botonera('../db/privado/cobrar.json')
        else:
            self.pedido.efectivo = self.efectivo.efectivo.replace("€", "")
            self.pedido.cambio = self.efectivo.cambio.replace("€", "")
            self.tpv.imprimirTicket(self.pedido.guardar_pedido())
            self.tpv.abrir_cajon()
            self.tpv.mostrar_inicio()
            self.tpv.mostrar_men_cobro("Cambio "+ self.efectivo.cambio)



    def exit_sug(self, key, w, txt, ln):
        if txt != "":
            if "sug" not in ln.obj:
                ln.obj["sug"] = []

            ln.obj["sug"].append(txt)
            db = JsonStore("../db/sugerencias.json")
            sug = self.modal.sug
            db.put(ln.obj.get("text").lower(), db=sug)
            self.rf_parcial(w, ln)
        self.modal.dismiss()


    def sugerencia(self, w, linea):
        try:
            name = linea.obj.get('text').lower()
            db = JsonStore("../db/sugerencias.json")
            if not db.exists(name):
                db.put(name, db=[])
            self.modal.sug = db[name].get("db")
            self.modal.des = "{0}  {1:.2f}".format(linea.getTexto(),
                                                   linea.getTotal())
            self.modal.clear_text()
            self.modal.tag = linea
            self.modal.content = w
            self.modal.open()
        except:
            self.modal.content = None


    def atras(self):
        num = len(self.pilaDeStados)
        if num == 1:
            self.linea_nueva()
        if num == 2:
            self.pilaDeStados.pop()
            pr = self.pilaDeStados[-1]
            self.show_botonera(pr['db'])
            self.puntero = pr['punt']
            self.pedido.rm_estado()
            if self.linea_editable:
                self.lista.rm_linea(self.linea_editable)
                self.linea_editable = None

        if num > 2:
            sc = self.pilaDeStados.pop()
            pr = self.pilaDeStados[-1]
            self.show_botonera(pr['db'])
            self.puntero = pr['punt']
            if sc['pass'] > 1:
                for i in range(int(sc['pass'])):
                    self.pedido.rm_estado()
            else:
                self.pedido.rm_estado()

        self.refresh_linea()


    def linea_nueva(self):
        db = "../db/clases.json"
        self.show_botonera(db)
        self.clase = None
        self.promocion = None
        self.linea_editable = None
        if len(self.pedido.lineas_pedido) > 0:
            self.btnPedido.disabled = False
        self.btnAtras.disabled = True
        self.pedido.finaliza_linea()
        self.pilaDeStados = []

    def add_linea(self):
        self.btnPedido.disabled = True
        self.btnAtras.disabled = False
        if self.pedido.linea:
            self.linea_editable = LineaWidget(tag=self.pedido.linea,
                                              borrar=self.borrar,
                                              sumar=self.sumar,
                                              sugerencia=self.sugerencia)
            if self.promocion is not None:
                self.linea_editable.mostar_btnpromo()
                self.linea_editable.aplicar = self.aplicar_promo
                self.linea_editable.promocion = self.promocion
            else:
                self.linea_editable.mostar_btnpromo(False)

            self.lista.add_linea(self.linea_editable)

    def aplicar_promo(self, btn):
        self.rf_parcial(btn, btn.tag)

    def refresh_linea(self):
        if self.pedido and self.pedido.linea:
            self.linea_editable.texto = self.pedido.linea.getTexto()
            self.linea_editable.total = self.pedido.linea.getTotal()
        if len(self.pedido.lineas_pedido) == 0:
            self.btnPedido.disabled = True


    def rf_parcial(self, w, ln):
        w.texto = ln.getTexto()
        w.total = ln.getTotal()
        if self.pedido:
            self.pedido.actualizar_total()

    def sumar(self, w, tag):
        self.pedido.sumar(tag)
        self.rf_parcial(w, tag)

    def borrar(self, widget, tag):
        if self.pedido.borrar(tag):
            self.linea_nueva()
            self.pedido.borrar(tag)
            self.lista.rm_linea(widget)
            self.refresh_linea()
        else:
            self.rf_parcial(widget, tag)

    def show_botonera(self, db):
        self.storage = JsonStore(db)
        if self.storage.exists('db'):
            if self.storage.exists('selectable'):
                self.botonera.selectable = True
            else:
                self.botonera.selectable = False
            lista = self.storage['db'].get('lista')
            num = len(lista)
            if num <= 4:
                self.botonera.cols = 1
            elif num > 4 and num <= 12:
                self.botonera.cols = 3
            else:
                self.botonera.cols = 4
            title = 'None'
            if self.clase != None:
                title = str(self.clase['text'])
            self.botonera.title = title
            self.botonera.botones = []
            self.botonera.botones = self.storage['db'].get('lista')


    def nuevo_pedido(self, clase):
        self.onPress([Wrap(clase)])
        self.clear_pedidos()

    def clear_pedidos(self):
        self.lista.rm_all_widgets()
        self.pedido = Pedido()
        self.btnPedido.disabled = True
        self.btnAtras.disabled = False
        self.total = 0
        self.des = "Pedido {0: >10} articulos".format(0)
        self.dbCliente = None

    def aparcar_pedido(self):
        if self.dbCliente == None:
            self.pedido.aparcar_pedido()
            self.tpv.mostrar_inicio()


    def recuperar_pedido(self, db):
        self.clear_pedidos()
        self.pedido.cargar_pedido(db)
        lineas = db.get("db")['lineas']
        for linea in lineas:
            self.pedido.add_linea(linea)
            self.add_linea()
            self.refresh_linea()
            self.linea_nueva()



    def hacer_pedido(self):
        if not self.dbCliente and self.total > 0:
            self.btnPedido.disabled = True
            self.btnAtras.disabled = True
            self.show_botonera('../db/privado/llevar.json')
        else:
            if self.dbCliente:
                self.pedido.para_llevar = "Domicilio"
                self.pedido.dbCliente = self.dbCliente
                self.pedido.num_avisador = "Domicilio"
                self.pedido.modo_pago = "Efectivo"
                self.tpv.imprimirTicket(self.pedido.guardar_pedido())
                self.tpv.mostrar_inicio()

            else:
                self.show_botonera("../db/privado/num_avisador.json")
                self.pedido.modo_pago = "Efectivo"
