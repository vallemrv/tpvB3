# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 17-Mar-2018
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from components.labels import LabelClicable
from models.db import Clientes,  Direcciones, QSon, VentasSender
import threading

Builder.load_file("view/clientescontroller.kv")

class Find(AnchorLayout):
    salir = ObjectProperty(None)
    aceptar = ObjectProperty(None)

class ClientesWidget(AnchorLayout):
    db = ObjectProperty(None)
    salir = ObjectProperty(None)
    pedir = ObjectProperty(None)

    def guardar(self):
        self.guardar_dir()
        self.db.telefono = self.tlf.text
        self.db.nombre = self.nombre.text
        self.db.nota = self.notas.text
        qson = QSon("Clientes", reg=self.db.toDICT())
        for d in self.db.direcciones:
            qson.append_child(QSon("Direcciones", reg=d))
        sender = VentasSender()
        sender.save(qson)
        sender.send(self.set_cliente, wait=False)

    def set_cliente(self, req, result):
        if result["success"] == True:
            cliente = result["add"]["clientes"]
            if len(cliente) > 0:
                self.db.load_data(**cliente[0])
                if "direcciones" in cliente[0]:
                    self.db.direcciones = cliente[0]["direcciones"]
                    if len(self.db.direcciones) > 0:
                        if self.db.direccion in [0, None, "", -1]:
                            self.db.direccion = self.db.direcciones[0]["id"]


    def guardar_salir(self):
        self.guardar()
        self.salir()

    def on_db(self, key, value):
        self.tlf.text = self.db.telefono if self.db.telefono is not None else ""
        self.nombre.text = self.db.nombre if self.db.nombre is not None else ""
        self.notas.text = self.db.nota if self.db.nota is not None else ""
        id_direccion = self.db.direccion
        if len(self.db.direcciones) > 0:
            self.dir.text = self.db.direcciones[0]['direccion']
            if self.db.direccion in [0, None, "", -1]:
                self.db.direccion = self.db.direcciones[0]["id"]
        for l in self.db.direcciones:
            if id_direccion == l["id"]:
                self.dir.text = l["direccion"]

        self.rellena_list()

    def rellena_list(self):
        self.listDirecciones.rm_all_widgets()
        for l in self.db.direcciones:
            btn = LabelClicable(text=l['direccion'])
            btn.tag = l
            btn.bind(on_press=self.sel_dir)
            self.listDirecciones.add_linea(btn)

    def sel_dir(self, btn):
        self.dir.text = btn.tag['direccion']
        self.db.direccion = btn.tag['id']

    def guardar_dir(self):
        text_dir = self.dir.text
        dirs = filter(lambda dir: dir['direccion'] == text_dir, self.db.direcciones)
        if len(dirs) <= 0:
            self.db.direcciones.append({
                "direccion": text_dir,
            })

    def add_dir(self):
        self.guardar_dir()
        self.rellena_list()

    def hacer_pedido(self, db):
        self.guardar()
        self.pedir(db)


class ClientesController(AnchorLayout):
    tpv = ObjectProperty(None)
    def __init__(self, **kargs):
        super(ClientesController, self).__init__(**kargs)
        self.clientes = ClientesWidget(salir=self.salir,
                                 pedir=self.tpv.pedir_domicilio)
        self.find = Find(salir=self.salir, aceptar=self.aceptar)
        self.add_widget(self.find)

    def salir(self):
        self.show_find()
        self.find.txt.text = ""
        self.tpv.mostrar_inicio()

    def show_find(self):
        self.find.txt.text = ""
        self.clear_widgets()
        self.add_widget(self.find)

    def aceptar(self, numTlf):
        if len(numTlf) == 9:
            sender = VentasSender()
            qson = QSon("Clientes", telefono__icontains=numTlf)
            qson.append_child(QSon("Direcciones"))
            sender.filter(qson)
            threading.Thread(target=lambda: sender.send(self.show_clientes)).start()


    def show_clientes(self, req, result):
        if result["success"] == True:
            cliente = result["get"]["clientes"]
            if len(cliente) <= 0:
                db = Clientes()
                db.telefono = self.find.txt.text
                db.direcciones = []
            else:
                db = Clientes(**cliente[0])
                db.direcciones = cliente[0]["direcciones"]
                if len(db.direcciones) > 0:
                    if db.direccion in [0, None, "", -1]:
                        db.direccion = db.direcciones[0]["id"]

            self.clientes.db = db
            self.remove_widget(self.find)
            self.add_widget(self.clientes)
