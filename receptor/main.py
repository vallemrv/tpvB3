#!/usr/bin/env python
# coding=utf-8
# @Author: Manuel Rodriguez <valle>
# @Date:   02-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 22-Sep-2017
# @License: Apache license vesion 2.0

import sys
reload(sys)
sys.setdefaultencoding('utf8')


from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from models.pedidos import *
from kivy.network.urlrequest import UrlRequest
from datetime import datetime
import json
import urllib
import threading
import time

URL_SERVER = "http://btres.elbrasilia.com"

SEND_DATA = {
    'token': '4po-8eaed7f5d56569670b0a',
    'user': 2,
    'data': ""
    }

Builder.load_string("""
#:import ValleListView components.listview
#:import BotonIcon components.buttons
#:import LabelClicable components.labels
#:import res components.resources
<Pedidos>:
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
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        size_hint: 1, .1
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


class Pedidos(AnchorLayout):

    stop = threading.Event()

    def __init__(self, **kargs):
        super(Pedidos, self).__init__(**kargs)
        threading.Thread(target=self.pedidos).start()
        Clock.schedule_once(self.mostra_pedidos, 5)
        self.listapedidos = []


    def servido(self, root):
        tag = root.tag
        s = tag.servido
        s = "False" if s == "True" else "True"
        root.color = '#beec90' if s == "True" else '#b9b9b9'
        tag.servido = s
        tag.save()
        query = "IDpedido={0} AND servido='False'".format(tag.IDpedido)


    def rm(self, root, tag):
        self.listapedidos.remove(tag.ID)
        tag.delete()
        self.view.remove_widget(root)


    def mostra_pedidos(self, dt):
        pedidos = Pedido().getAll(query="servido='False'")
        for p in pedidos:
            if not p.ID in self.listapedidos:
                self.listapedidos.append(p.ID)
                ls = p.lineas.get(query="imprimible='True'")
                if len(ls) > 0:
                    pedidowidget = PedidoWidget(rm=self.rm, tag=p)
                    fecha = datetime.strptime(p.fecha, "%Y-%m-%d %H:%M:%S.%f")
                    fs = fecha.strftime("%d/%m/%Y %H:%M")
                    texto = "{0}\nnum: {1}\n{2}".format(fs,
                                                       p.num_avisador,
                                                       p.para_llevar)
                    pedidowidget.texto = texto
                    for l in ls:
                        linea = LineaWidget(borrar=self.servido)
                        if l.servido == "True":
                            linea.color = "#beec90"
                        linea.tag = l
                        linea.contenedor = pedidowidget
                        linea.des = "{0} {1} {2} {3}".format(l.cant, l.tipo, l.text, l.des)
                        pedidowidget.lineas.add_linea(linea)

                    self.view.add_widget(pedidowidget)

        Clock.schedule_once(self.mostra_pedidos, 6)

    def got_json(self, result, val):
        self.modify_pedidos = []
        for s in  val["get"]["pedidos"]:
            self.modify_pedidos.append({
                "id": s["id"],
                'estado': s["estado"].replace("NO", "SI")
            })
            p = Pedido(**s)
            p.save()
            for l in s["lineaspedido"]:
                linea = LineasPedido(**l)
                linea.imprimible = self.esImprimible(l)
                linea.save()
                p.lineas.add(linea)

        self.close_pedidos()


    def echo(self, request, val):
        print val

    def esImprimible(self, val):
        if val.get("tipo") == "bebidas" or val.get("tipo") == "postres":
            return "False"
        else:
            return "True"

    def pedidos(self):
        while True:

            if self.stop.is_set():
                # Stop running this thread so the main Python process can exit.
                return

            SEND_DATA["data"]= json.dumps(
                {'get':{
                    'db': 'ventas',
                    "pedidos":{
                        "query": "estado LIKE '%_NO%'",
                        'lineaspedido':{}
                    }
                }}
            )
            data = urllib.urlencode(SEND_DATA)
            headers = {'Content-type': 'application/x-www-form-urlencoded',
                       'Accept': 'text/json'}
            r = UrlRequest(URL_SERVER+"/themagicapi/qson_django/",
                           on_success=self.got_json, req_body=data,
                           req_headers=headers, method="POST")
            time.sleep(6)

    def close_pedidos(self):
        SEND_DATA["data"]= json.dumps(
            {'add':{
                'db': 'ventas',
                "pedidos":self.modify_pedidos
            }}
        )

        data = urllib.urlencode(SEND_DATA)
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/json'}
        r = UrlRequest(URL_SERVER+"/themagicapi/qson_django/",
                       on_success=self.echo, req_body=data,
                       req_headers=headers, method="POST")


class AppRun(App):

    def build(self):
        self.title = "Pedidos"
        return Pedidos()

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
