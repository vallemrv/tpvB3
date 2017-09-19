# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 15-Sep-2017
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

    def guardar(self):
        self.db.save(telefono=self.tlf.text,
                     nombre=self.nombre.text,
                     apellido="",
                     email=self.email.text,
                     nota=self.notas.text)

    def on_db(self, key, value):
        self.tlf.text = self.db.telefono if self.db.telefono is not None else ""
        self.nombre.text = self.db.nombre if self.db.nombre is not None else ""
        self.email.text = self.db.email if self.db.email is not None else ""
        self.notas.text = self.db.nota if self.db.nota is not None else ""
        id_direccion = self.db.direccion
        if id_direccion != None:
            self.dir.text = self.db.direcciones.get(query="id=%d" % id_direccion)[0].direccion
        self.rellena_list()


    def rellena_list(self):
        self.listDirecciones.rm_all_widgets()
        for l in self.db.direcciones.get():
            btn = LabelClicable(text=l.direccion)
            btn.tag = l
            btn.bind(on_press=self.sel_dir)
            self.listDirecciones.add_linea(btn)

    def sel_dir(self, btn):
        direccion = self.db.direcciones.get(query="id=%d" % btn.tag.id)
        if len(direccion) > 0:
            self.dir.text = direccion[0].direccion
            self.db.direccion = btn.tag.id
            self.db.save()

    def add_dir(self):
        list = self.db
        direccion = self.db.direcciones.get(query="direccion='%s'" % self.dir.text)
        if len(direccion) <= 0:
            direccion = Direcciones(direccion=self.dir.text)
            self.guardar()
            self.db.direcciones.add(direccion)
            self.db.direccion = direccion.id
            self.db.save()
        self.rellena_list()

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
        self.add_widget(self.find)

    def aceptar(self, numTlf):
        if len(numTlf) == 9:
            db = ClientesModel()
            db.load_first_by_query(query="telefono='%s'" % numTlf)
            if db.id == -1:
                db.telefono = numTlf
            self.clientes.db = db
            self.remove_widget(self.find)
            self.add_widget(self.clientes)

    
