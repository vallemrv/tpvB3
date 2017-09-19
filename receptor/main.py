#!/usr/bin/env python
# coding=utf-8
# @Author: Manuel Rodriguez <valle>
# @Date:   02-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 19-Sep-2017
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
import json
import urllib

URL_SERVER = "http://btres.elbrasilia.com"

SEND_DATA = {
    'token': '4pl-1b7b438f2ce88941e147',
    'user': 1,
    'data': ""
    }

Builder.load_string("""
#:import ValleListView components.listview
#:import BotonImg components.buttons
#:import LabelClicable components.labels

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
            width: len(self.children) * (root.width/5)
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
            ButtonImg:
                src: './img/papelera.png'
                on_press: root.rm(root, root.tag)

<LineaWidget>:
    contenedor: None
    color: .1,.1,.1,1
    tag: None
    des: ''
    spacing: 5
    orientation: 'horizontal'
    LabelClicable:
        font_size: 15
        tag: root.tag
        event: root.borrar
        texto: root.des
        bgColor: root.color


""")
class LineaWidget(BoxLayout):
    borrar = ObjectProperty(None, allowNone=True)


class PedidoWidget(BoxLayout):
    rm = ObjectProperty(None, allowNone=True)
    tag = ObjectProperty(None, allowNone=True)


class Pedidos(AnchorLayout):


    def __init__(self, **kargs):
        super(Pedidos, self).__init__(**kargs)
        Clock.schedule_once(self.pedidos, 1)
        Clock.schedule_once(self.mostra_pedidos, 1)
        self.listapedidos = []


    def servido(self, root):
        tag = root.tag
        s = tag.servido
        s = "False" if s == "True" else "True"
        root.bgColor = (0, .01, 0, 1) if s == "True" else (.1, .1, .1, 1)
        tag.servido.set(s)
        tag.save()
        query = "IDPedido={0} AND servido='False'".format(tag.IDPedido.get())


    def rm(self, root, tag):
        tag.remove()
        self.view.remove_widget(root)


    def mostra_pedidos(self, dt):
        pedidos = Pedido().getAll(query="servido='False'")

        for p in pedidos:
            if not p.ID in self.listapedidos:
                self.listapedidos.append(p.ID)
                p.lineas.reg = p
                ls = p.lineas.get(query="imprimible='True'")
                if len(ls) > 0:
                    pedidowidget = PedidoWidget(rm=self.rm, tag=p)
                    texto = "{0}\nnum: {1}\n{2}".format(p.fecha.get(),
                                                       p.num_avisador.get(),
                                                       p.para_llevar.get())
                    pedidowidget.texto = texto
                    for l in ls:
                        linea = LineaWidget(borrar=self.servido)
                        if l.servido.get() == "True":
                            linea.color = (0, .5, 0, 1)
                        linea.tag = l
                        linea.contenedor = pedidowidget
                        linea.des = l.des.get()
                        pedidowidget.lineas.add_linea(linea)

                    self.view.add_widget(pedidowidget)

        Clock.schedule_once(self.mostra_pedidos, 6)

    def got_json(self, result, val):
        print val, 'holaaaaaaa', result
        val = json.loads(val)
        for s in  val:
            fl = s.get('fl')
            db = s.get('db')
            p = Pedido(**db)
            p.save()
            for l in db.get("lineas"):
                linea = LineasPedido(**l)
                linea.imprimible = self.esImprimible(l)
                liena.save()
                p.lineas.add(linea)



        Clock.schedule_once(self.pedidos, 5)

    def echo(self, request, val):
        pass

    def esImprimible(self, val):
        if val.get("tipo") == "refresco" or val.get("tipo") == "postre":
            return "False"
        else:
            return "True"

    def pedidos(self, dt):
        SEND_DATA["data"]= json.dumps(
            {'get':{
                'db': 'arqueos',
                "pedidos":{
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


class AppRun(App):
    def build(self):
        self.title = "Pedidos"
        return Pedidos()

    def on_pause(self):
        return True

if __name__ == '__main__':
    from kivy.core.window import Window
    Window.clearcolor = (1,1,1,1)
    AppRun().run()
