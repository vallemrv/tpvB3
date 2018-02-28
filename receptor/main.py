#!/usr/bin/env python
# coding=utf-8
# @Author: Manuel Rodriguez <valle>
# @Date:   02-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 27-Feb-2018
# @License: Apache license vesion 2.0

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except Exception as e:
    from importlib import sys, reload
    reload(sys)

from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from models.pedidos import *
from kivy.network.urlrequest import UrlRequest
from datetime import datetime
from valleorm.qson import QSonSender, QSon
from kivy.logger import Logger

import json
import threading
import time


Builder.load_string("""
#:import ValleListView components.listview
#:import BotonIcon components.buttons
#:import * components.labels
#:import res components.resources
<PedidosWidget>:
    anchor_x: 'center'
    anchor_y: 'center'
    scroll: _scroll
    view: _listado
    ScrollView:
        id: _scroll
        size_hint: .99, .99
        BoxLayout:
            orientation: 'horizontal'
            spacing: 5
            size_hint: None, 1
            width: len(self.children) * (root.width/4)
            id: _listado



<PedidoWidget>:
    canvas:
        Color:
            rgba: 0.2, 0.2, 0.2, 1
        Rectangle:
            size: self.size
            pos: self.pos
    texto: ""
    lineas: _listview
    orientation: 'vertical'
    spacing: 5
    size_hint: 1, 1
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        size_hint: 1, .23
        Label:
            font_size: 12
            size_hint: 1, 1
            text: root.texto
            text_size: self.size
            halign: 'center'
            valign: 'middle'
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        ValleListView:
            size_hint: 1, 1
            id: _listview
            cheight: '60dp'
            
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        size_hint: 1, .2
        BoxLayout:
            orientation: 'vertical'
            size_hint: .95, .95
            LabelColor:
                text: root.direccion
                font_size: '12dp'
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        size_hint: 1, .2
        BoxLayout:
            orientation: 'horizontal'
            size_hint: .95, .95
            Label:
                text: "Borrar comada"
                text_size: self.size
                halign: 'center'
                valign: 'middle'
            ButtonIcon:
                size_hint: None, .95
                width: self.height
                icon: res.FA_TRASH
                font_size: "6dp"
                on_press: root.rm(root, root.tag)

<LineaWidget>:
    contenedor: None
    color: "#b9b9b9"
    tag: None
    des: ''
    spacing: 5
    orientation: 'horizontal'
    LabelClicable:
        font_size: "15dp"
        tag: root.tag
        event: root.borrar
        text: root.des
        bgColor: root.color
        on_release: root.borrar(root)

""")

class PedidosSenderQSon(QSonSender):
    db_name = "ventas"
    url = "http://btres.elbrasilia.com/simpleapi/"
    LineasPedido()

class LineaWidget(BoxLayout):
    borrar = ObjectProperty(None, allowNone=True)


class PedidoWidget(BoxLayout):
    rm = ObjectProperty(None, allowNone=True)
    tag = ObjectProperty(None, allowNone=True)
    direccion = StringProperty("No hay direccion")


class PedidosWidget(AnchorLayout):

    stop = threading.Event()

    def __init__(self, **kargs):
        super(PedidosWidget, self).__init__(**kargs)
        Logger.debug('Cagada')
        self.listapedidos = []
        self.modify_pedidos = []
        self.lock = threading.Lock()
        threading.Thread(target=self.get_pedidos).start()
        Clock.schedule_once(self.mostra_pedidos, 5)



    def servido(self, root):
        tag = root.tag
        s = tag.servido
        s = False if s == True else True
        tag.servido = s
        tag.save()
        self.servir_linea(tag.id)
        root.color = '#beec90' if s == True else '#b9b9b9'


    def rm(self, root, tag):
        self.listapedidos.remove(tag.id)
        tag.delete()
        tag.servido = True
        self.servir_pedido(tag)
        if tag.id in self.listapedidos:
            self.listapedidos.remove(tag.id)
        self.view.remove_widget(root)


    def mostra_pedidos(self, dt):
        pedidos = Pedidos.filter()
        for p in pedidos:
            if not p.id in self.listapedidos:
                self.listapedidos.append(p.id)
                ls = p.lineaspedido_set.get(query="imprimible=1")
                if len(ls) > 0:
                    pedidowidget = PedidoWidget(rm=self.rm, tag=p)
                    fecha = p.fecha
                    fs = fecha.strftime("%d/%m/%Y %H:%M")
                    texto = "{0}\nnum: {1}\n{2}".format(fs,
                                                       p.num_avisador,
                                                       p.para_llevar)
                    pedidowidget.texto = texto
                    pedidowidget.direccion = p.direccion
                    for l in ls:
                        linea = LineaWidget(borrar=self.servido)
                        if l.servido == True:
                            linea.color = "#beec90"
                        linea.tag = l
                        linea.contenedor = pedidowidget
                        linea.des = "{0} {1} {2} {3}".format(l.cant, l.tipo, l.text, l.des)
                        pedidowidget.lineas.add_linea(linea)

                    self.view.add_widget(pedidowidget)

        Clock.schedule_once(self.mostra_pedidos, 1)

    def got_json(self, result, val):
        print val
        if val["success"] == True:
            lista_pedidos = []
            for s in  val["get"]["pedidos"]:
                if  s["id"] in self.modify_pedidos:
                    continue
                p = Pedidos(**s)
                p.estado = p.estado.replace("NO", "SI")
                self.modify_pedidos.append(s["id"])
                lista_pedidos.append(s)
                for c in s["clientes"]:
                    for d in c["direcciones"]:
                        if d["id"] == c["direccion"]:
                            p.direccion = d["direccion"] + '  Tlf:' + c["telefono"]
                p.save()
                for l in s["lineaspedido"]:
                    linea = LineasPedido(**l)
                    linea.imprimible = self.esImprimible(l)
                    linea.save()
                    p.lineaspedido_set.add(linea)

            if len(lista_pedidos) > 0:
                self.close_pedidos(lista_pedidos)

    def echo(self, request, val):
        pass

    def echo_servido(self, request, val):
        pass

    def esImprimible(self, val):
        if val.get("tipo") == "bebidas" or val.get("tipo") == "postres":
            return False
        else:
            return True

    def get_pedidos(self):
        while True:

            if self.stop.is_set():
                # Stop running this thread so the main Python process can exit.
                print ("Adioooooos....")
                return

            qsonsender = PedidosSenderQSon()
            qson = QSon("Pedidos", estado__icontains="_NO")
            qson.append_child(QSon("LineasPedido"))
            cl = QSon("Clientes")
            cl.append_child(QSon("Direcciones"))
            qson.append_child(cl)
            qsonsender.filter(self.got_json, qson=(qson,), wait=False)
            time.sleep(2)

    def servir_linea(self, id):
        qsonsender = PedidosSenderQSon()
        qsons = []
        for s in LineasPedido.filter(id=id):
            qson = QSon("LineasPedido", reg=s.toDICT())
            qsons.append(qson)

        qsonsender.save(self.echo_servido, qson=qsons, wait=False)

    def servir_pedido(self, p):
        qsonsender = PedidosSenderQSon()
        qson = QSon("Pedidos", reg=p.toDICT())
        qsonsender.save(self.echo_servido, qson=(qson,), wait=False)


    def close_pedidos(self, lista_pedidos):
        qsonsender = PedidosSenderQSon()
        qsons = []
        for s in lista_pedidos:
            s["estado"] = s["estado"].replace("NO", "SI")
            qson = QSon("Pedidos", reg=s)
            qsons.append(qson)

        qsonsender.save(self.echo, qson=qsons, wait=False)



class AppRun(App):

    def build(self):
        self.title = "Pedidos"
        return PedidosWidget()

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        self.root.stop.set()

    def on_pause(self):
        return True

if __name__ == '__main__':
    from kivy.core.window import Window
    Window.clearcolor = (1,1,1,1)
    AppRun().run()
