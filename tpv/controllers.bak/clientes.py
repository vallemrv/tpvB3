# -*- coding: utf-8 -*-
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file("view/clientescontroller.kv")

class Find(AnchorLayout):
    salir = ObjectProperty(None)
    aceptar = ObjectProperty(None)

class Clientes(AnchorLayout):
    db = ObjectProperty(None)
    salir = ObjectProperty(None)
    pedir = ObjectProperty(None)

    def guardar(self):
        list = self.db["reg"].get("list")
        pedidos = self.db["reg"].get("pedidos")
        self.db.put("reg", num_tlf=self.tlf.text, nombre=self.nombre.text,
                    direccion=self.dir.text,
                    pedidos=pedidos,
                    list=list,
                    notas=self.notas.text)

    def on_db(self, key, value):
        self.tlf.text = self.db['reg'].get('num_tlf')
        self.nombre.text = self.db['reg'].get('nombre')
        self.dir.text = self.db['reg'].get('direccion')
        self.rellena_list()
        self.notas.text = self.db['reg'].get('notas')

    def rellena_list(self):
        self.list.rm_all_widgets()
        for l in self.db["reg"].get('list'):
            btn = Button(text=l)
            self.list.add_linea(btn)
            btn.bind(on_press=self.sel_dir)

    def sel_dir(self, btn):
        self.dir.text = btn.text
        self.guardar()

    def add_dir(self):
        list = self.db["reg"].get("list")
        if self.dir.text not in list:
            list.append(self.dir.text)
            self.guardar()
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
            db = JsonStore("db/clientes/{0}.json".format(numTlf))
            if not db.exists("reg"):
                db.put("reg", num_tlf=numTlf, nombre="",
                       direccion="", list=[], pedidos=[], notas="")
            self.clientes.db = db
            self.remove_widget(self.find)
            self.add_widget(self.clientes)
