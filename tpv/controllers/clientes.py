# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 20-Feb-2018
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from components.labels import LabelClicable

from models.db.pedidos import Clientes as ClientesModel, Direcciones

Builder.load_file("view/clientescontroller.kv")

class Find(AnchorLayout):
    salir = ObjectProperty(None)
    aceptar = ObjectProperty(None)

class Clientes(AnchorLayout):
    db = ObjectProperty(None)
    salir = ObjectProperty(None)
    pedir = ObjectProperty(None)

    def guardar(self, add_dir=False):
        self.db.save(telefono=self.tlf.text,
                     nombre=self.nombre.text,
                     apellido="",
                     email=self.email.text,
                     nota=self.notas.text)
        if self.db.direccion == None and not add_dir:
            d = Direcciones(direccion=self.dir.text)
            self.db.direcciones_set.add(d)
            self.db.direccion = d.id
            self.db.save()

    def guardar_salir(self):
        self.guardar()
        self.salir()

    def on_db(self, key, value):
        self.tlf.text = self.db.telefono if self.db.telefono is not None else ""
        self.nombre.text = self.db.nombre if self.db.nombre is not None else ""
        self.email.text = self.db.email if self.db.email is not None else ""
        self.notas.text = self.db.nota if self.db.nota is not None else ""
        id_direccion = self.db.direccion
        self.dir.text = ''
        direcciones = []
        if id_direccion != None:
            direcciones = self.db.direcciones_set.get(query="id=%d" % id_direccion)
        if len(direcciones) > 0:
            self.dir.text = direcciones[0].direccion
        self.rellena_list()


    def rellena_list(self):
        self.listDirecciones.rm_all_widgets()
        for l in self.db.direcciones_set.get():
            btn = LabelClicable(text=l.direccion)
            btn.tag = l
            btn.bind(on_press=self.sel_dir)
            self.listDirecciones.add_linea(btn)

    def sel_dir(self, btn):
        direccion = self.db.direcciones_set.get(query="id=%d" % btn.tag.id)
        if len(direccion) > 0:
            self.dir.text = direccion[0].direccion
            self.db.direccion = btn.tag.id
            self.db.save()

    def add_dir(self):
        list = self.db
        direccion = self.db.direcciones_set.get(query="direccion='%s'" % self.dir.text)
        if len(direccion) <= 0:
            self.guardar(add_dir=True)
            direccion = Direcciones(direccion=self.dir.text)
            self.db.direcciones_set.add(direccion)
            self.db.direccion = direccion.id
            self.db.save()
        self.rellena_list()

    def hacer_pedido(self, db):
        self.guardar()
        self.pedir(db)


class ClientesController(AnchorLayout):
    tpv = ObjectProperty(None)
    def __init__(self, **kargs):
        super(ClientesController, self).__init__(**kargs)
        self.clientes = Clientes(salir=self.salir,
                                 pedir=self.tpv.pedir_domicilio)
        self.find = Find(salir=self.salir, aceptar=self.aceptar)
        self.add_widget(self.find)

    def salir(self):
        self.show_find()
        self.find.txt.text = ""
        self.tpv.mostrar_inicio()

    def show_find(self):
        self.clear_widgets()
        self.find.txt.text = ""
        self.add_widget(self.find)

    def aceptar(self, numTlf):
        if len(numTlf) == 9:
            db = ClientesModel()
            cs = db.filter(query="telefono='%s'" % numTlf)
            if len(cs) > 0:
                db = cs[0]
            if db.id == -1:
                db.telefono = numTlf
            self.clientes.db = db
            self.remove_widget(self.find)
            self.add_widget(self.clientes)
