# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty, NumericProperty
from kivy.lang import Builder
from uix.lineawidget import LineaWidget
from uix.sugerencias import Sugerencias
from shared.utils import json_to_list
from models.pedido import Pedido

Builder.load_file('uix/pedidowidget.kv')

class Wrap():
    def __init__(self, obj):
        self.tag = obj

class PedidoWidget(BoxLayout):
    tpv = ObjectProperty(None, allownone=True)
    pedido = ObjectProperty(None, allownone=True)
    precio = NumericProperty(0.0)

    def __init__(self, **kargs):
        super(PedidoWidget, self).__init__(**kargs)
        self.clase = None
        self.puntero = 0
        self.pilaDeStados = []
        self.linea_editable = None
        self.tipo_cobro = "Efectivo"
        self.modal = Sugerencias(onExit=self.exit_sug)

    def on_pedido(self, key, value):
        self.pedido.bind(total=self.show_total)

    def show_total(self, key, value):
        self.precio = self.pedido.total

    def onPress(self, botones):

        for i in range(len(botones)):
            btn = botones[i]
            tipo = btn.tag.get('tipo')
            if tipo == 'cobros':
                self.pedido.modo_pago = btn.tag.get("text")
                self.tpv.abrir_cajon()
                self.show_botonera("db/privado/num_avisador.json")
            elif tipo == 'llevar':
                self.show_botonera('db/privado/cobrar.json')
                self.pedido.para_llevar = btn.tag.get('text')
            elif tipo == 'num':
                self.pedido.num_avisador = btn.tag.get("text")
                self.tpv.mostrar_inicio()
                self.tpv.imprimirTicket(self.pedido.guardar_pedido())
            elif tipo == 'clase':
                self.clase = btn.tag
                self.puntero = 0
                db = self.clase.get('productos')
                self.show_botonera(db)
                self.linea_editable = None
                self.pilaDeStados = []
                self.pilaDeStados.append({'db': db, 'punt': 0,
                                          'pass': 1})
                self.ids._btnAtras.disabled = False

            else:
                db = self.pedido.add_modificador(btn.tag)

                if not self.linea_editable:
                    self.add_linea()

                self.refresh_linea()
                num = len(self.clase.get('preguntas')) if self.clase else 0
                ps = len(botones) - 1
                if db:
                    self.show_botonera(db)
                elif not db and self.puntero < num and i == ps:
                    db = self.clase.get('preguntas')[self.puntero]
                    self.puntero = self.puntero + 1
                    self.show_botonera(db)
                elif self.puntero >= num and i == ps:
                    self.linea_nueva()
                if i == ps:
                    self.pilaDeStados.append({'db': db, 'punt': self.puntero,
                                              'pass': len(botones)})

    def exit_sug(self, key, w, v, ln):
        if v.get("text") != "":
            ln.obj["modificadores"].append(v)
            db = JsonStore("db/sugerencias.json")
            sug = self.modal.sug
            db.put(ln.obj.get("text").lower(), db=sug)
            self.rf_parcial(w, ln)
            self.modal.content = None
        self.modal.dismiss()

    def sugerencia(self, w, linea):
        try:
            name = linea.obj.get('text').lower()
            db = JsonStore("db/sugerencias.json")
            if not db.exists(name):
                db.put(name, db=[])
            self.modal.sug = db[name].get("db")
            self.modal.des = linea.getTexto()
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
                self.ids._contenido_pedido.remove_widget(self.linea_editable)
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
        db = "db/clases.json"
        self.show_botonera(db)
        self.clase = None
        self.linea_editable = None
        if len(self.pedido.lineas_pedido) > 0:
            self.ids._btnPedido.disabled = False
        self.ids._btnAtras.disabled = True
        self.pedido.finaliza_linea()
        self.pilaDeStados = []

    def add_linea(self):
        self.ids._btnPedido.disabled = True
        self.ids._btnAtras.disabled = False
        if self.pedido.linea:
            self.linea_editable = LineaWidget(tag=self.pedido.linea,
                                              borrar=self.borrar,
                                              sumar=self.sumar,
                                              sugerencia=self.sugerencia)
            self.ids._contenido_pedido.add_widget(self.linea_editable)
            self.ids._scroll.scroll_y = 0

    def refresh_linea(self):
        if self.pedido and self.pedido.linea:
            self.linea_editable.texto = self.pedido.linea.getTexto()
            self.linea_editable.total = self.pedido.linea.getTotal()
        if len(self.pedido.lineas_pedido) == 0:
            self.ids._btnPedido.disabled = True


    def rf_parcial(self, w, ln):
        w.texto = ln.getTexto()
        w.total = ln.getTotal()

    def sumar(self, w, tag):
        self.pedido.sumar(tag)
        self.rf_parcial(w, tag)

    def borrar(self, widget, tag):
        if self.pedido.borrar(tag):
            self.linea_nueva()
            self.pedido.borrar(tag)
            self.ids._contenido_pedido.remove_widget(widget)
            self.refresh_linea()
        else:
            self.rf_parcial(widget, tag)

    def show_botonera(self, db):
        self.storage = JsonStore(db)
        if self.storage.exists('titulo'):
            if self.storage.exists('selectable'):
                self.ids._botonera.selectable = True
            else:
                self.ids._botonera.selectable = False

            self.ids._botonera.titulo = str(self.storage['titulo'].get('text'))
            self.ids._botonera.botones = []
            self.ids._botonera.botones = json_to_list(
                                        self.storage['db'].get('lista'))


    def nuevo_pedido(self, clase):
        self.onPress([Wrap(clase)])
        self.ids._contenido_pedido.clear_widgets()
        self.pedido = Pedido()
        self.ids._btnPedido.disabled = True
        self.ids._btnAtras.disabled = False


    def cancelar_pedido(self):
        self.tpv.mostrar_inicio()

    def hacer_pedido(self):
        self.ids._btnPedido.disabled = True
        self.ids._btnAtras.disabled = True
        self.show_botonera('db/privado/llevar.json')
