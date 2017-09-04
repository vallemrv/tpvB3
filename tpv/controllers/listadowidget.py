# -*- coding: utf-8 -*-
from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.clock import Clock
from kivy.lang import Builder
from valle.component.labelclicable import LabelClicable
from valle.utils import parse_float
from valle.tpv.impresora import DocPrint
from glob import glob

Builder.load_file('view/listadowidget.kv')

class ListadoWidget(AnchorLayout):
    tpv = ObjectProperty(None)
    precio = NumericProperty(0)
    des = StringProperty('Pedido')


    def __init__(self, **kargs):
        super(ListadoWidget, self).__init__(**kargs)
        self.start = True
        self.selected = None
        Clock.schedule_once(self.mostrar_lista, 2)

    def start_refresh(self):
        self.start = True
        Clock.schedule_once(self.mostrar_lista, 2)

    def salir(self):
        self.start_refresh()
        self.tpv.mostrar_inicio()

    def clear_self_widget(self):
        self.selected = None
        self.precio = 0
        self.pedido.rm_all_widgets()


    def stop_refresh(self):
        self.start = False
        self.clear_self_widget()

    def mostrar_lista(self, dt):
        files = sorted(glob("db/pd/*.11.json"))
        num = len(files)
        init = num - 15
        self.lista.rm_all_widgets()
        if num < 15:
            init = 0
        for i in range(init, num, 1):
            btn = LabelClicable(bColor="#444444")
            db = JsonStore(files[i]).get("reg")
            btn.tag = {"db": db, "file": files[i]}
            btn.font_size = 20
            texto = "{0: >25}   Avisador: {1: >6}   Total: {2:5.2f} €".format(
                         db["fecha"], db["num_avisador"],
                         parse_float(db["total"]))
            btn.texto = texto
            btn.event = self.onPress
            self.lista.add_linea(btn)

        if self.start:
            Clock.schedule_once(self.mostrar_lista, 2)

    def onPress(self, btn):
        self.pedido.rm_all_widgets()
        self.selected = btn.tag
        lineas = self.selected.get("db").get('lineas')
        total = 0
        for item in lineas:
            btn = LabelClicable(bColor="#444444")
            btn.font_size = 16
            tl = item["total"]
            total += tl
            btn.texto = "{0}   {1:.2f} €".format(
                item["des"], parse_float(tl))
            self.pedido.add_linea(btn)
        self.precio = total

    def imprimir(self):
        self.salir()
        Clock.schedule_once(self.hacer_pedido, .5)

    def imprimirTk(self):
        self.salir()
        Clock.schedule_once(self.imprimirTicket, .5)

    def imprimirTicket(self, dt):
        if self.selected:
            tk = self.selected.get("db")
            llevar = tk.get('para_llevar')
            cl = None
            if llevar == "Domicilio":
                num_tlf = tk.get("num_tlf")
                cl = JsonStore("db/clientes/{0}.json".format(num_tlf))
                cl = cl['reg']
            docPrint = DocPrint()
            docPrint.imprimirTicket("caja", tk.get('numTicket'),
                                         tk.get('lineas'), tk.get('fecha'),
                                         tk.get('total'), cl)


    def hacer_pedido(self, dt):
        if self.selected:
            nombre = self.selected.get("file")
            aux = self.selected.get("file")
	    if "4.11." in nombre:
	        nombre = nombre.replace("4.11.", "0.11.")
	    elif "3.11." in nombre:
	        nombre = nombre.replace("3.11.", "1.11.")
            from os import rename
            rename(aux, nombre)
            tk = self.selected.get("db")
            docPrint = DocPrint()
            docPrint.printPedido("cocina", tk.get('num_avisador'),
                                 tk.get('lineas'), tk.get('fecha'),
                                 tk.get('para_llevar'))
