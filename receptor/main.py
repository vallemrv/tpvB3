#!/usr/bin/env python
# coding=utf-8
# @Author: Manuel Rodriguez <valle>
# @Date:   02-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 10-Mar-2018
# @License: Apache license vesion 2.0

import sys
import os
reload(sys)
sys.setdefaultencoding('UTF8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
os.chdir(BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "valle_libs"))
sys.path.insert(0, os.path.join(BASE_DIR))


from kivy.app import App
from kivy.utils import platform
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivy.lib import osc
from datetime import datetime
from kivy.logger import Logger
from models.pedidos import *


import json
import threading
import time

activityport = 3011
serviceport = 3010

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
        if platform == 'android':
            from android import AndroidService
            service = AndroidService('TpvB3 receptor', 'running')
            service.start('service started')
            self.service = service
        else:
            import os, threading
            #threading.Thread(target=os.system, args=("python ./service/main.py",)).start()


        osc.init()
        oscid = osc.listen(ipAddr='127.0.0.1', port=activityport)
        osc.bind(oscid, self.mostrar_pedidos, '/sync_pedidos')
        Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0)
        self.mostrar_pedidos('ok')
        #self.lock = threading.Lock()
        #threading.Thread(target=self.get_pedidos).start()
        #Clock.schedule_once(self.mostra_pedidos, 5)



    def servido(self, root):
        tag = root.tag
        s = tag.servido
        s = False if s == True else True
        tag.servido = s
        tag.save()
        osc.sendMsg('/servidor_men', ['linea_servida',tag.id, tag.servido], port=serviceport)
        root.color = '#beec90' if s == True else '#b9b9b9'


    def rm(self, root, tag):
        self.listapedidos.remove(tag.id)
        osc.sendMsg('/servidor_men', ['pedido_servido',tag.id], port=serviceport)
        tag.delete()
        tag.servido = True
        if tag.id in self.listapedidos:
            self.listapedidos.remove(tag.id)
        self.view.remove_widget(root)


    def mostrar_pedidos(self, men, *args):
        print("[DEBUG ] %s" % men)
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



class AppRun(App):
    service = ObjectProperty()
    def build(self):
        self.title = "Pedidos"
        self.p = PedidosWidget()
        if platform == 'android':
            self.service = self.p.service
        return self.p

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        if platform == 'android':
            self.p.service.stop()
        osc.sendMsg('/servidor_men', ['finalizar',], port=serviceport)


    def on_pause(self):
        return True

if __name__ == '__main__':
    from kivy.core.window import Window
    Window.clearcolor = (1,1,1,1)
    AppRun().run()
