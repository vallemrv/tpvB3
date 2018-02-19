# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   04-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 14-Feb-2018
# @License: Apache license vesion 2.0

from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, StringProperty
from models.lineapedido import Constructor
from models.lineapedido import Linea
from models.db.pedidos import *
from kivy.storage.jsonstore import JsonStore
from copy import deepcopy
from datetime import datetime
import os


class Pedido(EventDispatcher):
    total = NumericProperty(0.0)
    modo_pago = StringProperty('Efectivo')
    fecha = StringProperty('')
    num_avisador = StringProperty('')
    para_llevar = StringProperty('')

    def __init__(self, **kargs):
        super(Pedido, self).__init__(**kargs)
        self.lineas_pedido = []
        self.constructor = None
        self.linea = None
        self.dbCliente = None
        self.efectivo = 0.0
        self.cambio = 0.0


    def add_modificador(self, obj):
        db = None
        if not self.linea:
            self.linea = Linea(deepcopy(obj))
            self.linea.obj['cant'] = 1
            self.constructor = Constructor(producto=self.linea)
            self.lineas_pedido.append(self.linea)

            nom_ing = obj.get("ingredientes") if "ingredientes" in obj else None
            if nom_ing != None:
                mod = Linea(obj)
                db = "../db/ingredientes/%s.json" % nom_ing

            if self.linea.hay_preguntas():
                db = self.linea.get_pregunta()
        else:

            db = self.constructor.add_modificador(obj)
        return db

    def rm_estado(self):
        if self.linea:
            if self.linea.getNumMod() > 0:
                self.linea.remove_modificador()
            else:
                self.lineas_pedido.pop()
                self.linea = None

    def actualizar_total(self):
        self.total = 0.0
        for item in self.lineas_pedido:
            self.total = self.total + item.getTotal()

    def finaliza_linea(self):
        self.actualizar_total()
        self.linea = None
        self.constructor = None

    def borrar(self, linea):
        borrar = False
        obj = linea.obj
        if obj['cant'] > 1:
            obj['cant'] = obj['cant'] - 1
        else:
            self.linea = None
            self.constructor = None
            if linea in self.lineas_pedido:
                self.lineas_pedido.remove(linea)
            borrar = True

        self.total = 0.0
        for item in self.lineas_pedido:
            self.total = self.total + item.getTotal()

        return borrar

    def getNumArt(self):
        num = 0
        for item in self.lineas_pedido:
            num = num + item.getNumArt()
        return num

    def sumar(self, linea):
        linea.obj['cant'] = linea.obj['cant'] + 1
        self.total = 0.0
        for item in self.lineas_pedido:
            self.total = self.total + item.getTotal()


    def set_list_pedidos(self, db):
        for obj in self.lineas_pedido:
            linea = LineasPedido()
            linea = LineasPedido(**{'text': obj.obj.get('text'),
                                    'des': obj.getDescripcion(),
                                    'cant': obj.obj.get('cant'),
                                    'precio': obj.getPrecio(),
                                    'total': obj.getTotal(),
                                    'tipo': obj.obj.get("tipo")})
            linea.pedidos_id = db.id
            linea.save()

    def guardar_pedido(self):
        db = Pedidos()
        db.save(total=self.total,
                modo_pago=self.modo_pago,
                para_llevar=self.para_llevar,
                num_avisador=self.num_avisador,
                entrega=self.efectivo,
                cambio=self.cambio)
        self.set_list_pedidos(db)
        if self.num_avisador == "Para recoger":
            db.save(estado = "NPG_NO")
        if self.dbCliente:
            self.dbCliente.pedidos.add(db)
            db.save(estado = "NPG_NO")
        return db

    def aparcar_pedido(self):
        fecha = str(datetime.now())
        db = JsonStore("../db/parking/%s.json" % fecha)
        lineas = []
        for obj in self.lineas_pedido:
            sug = [] if not 'sug' in obj.obj else obj.obj["sug"]
            linea = {'text': obj.obj.get('text'),
                     'modificadores': obj.obj.get("modificadores"),
                     'cant': obj.obj.get('cant'),
                     'precio': obj.obj.get('precio'),
                     'sug': sug,
                     'tipo': obj.obj.get("tipo")}
            lineas.append(linea)
        db.put("db", total=self.total,
                modo_pago=self.modo_pago,
                para_llevar=self.para_llevar,
                num_avisador=self.num_avisador,
                efectivo=self.efectivo,
                cambio=self.cambio,
                lineas=lineas)

    def cargar_pedido(self, db):
         self.total=db.get("db")["total"]
         self.modo_pago=db.get("db")['modo_pago']
         self.para_llevar=db.get("db")['para_llevar']
         self.num_avisador=db.get("db")['num_avisador']
         self.efectivo=db.get("db")['efectivo']
         self.cambio=db.get("db")['cambio']

    def add_linea(self, obj):
        self.linea = Linea(deepcopy(obj))
        self.linea.obj['text'] = obj.get('text')
        self.linea.obj['modificadores'] = obj.get("modificadores")
        self.linea.obj['precio'] = obj.get('precio')
        self.linea.obj['sug'] = obj.get('sug')
        self.linea.obj['tipo'] = obj.get('tipo')
        self.linea.obj['cant'] = obj.get('cant')
        self.lineas_pedido.append(self.linea)
