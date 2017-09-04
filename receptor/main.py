#!/usr/bin/env python
# coding=utf-8
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

Builder.load_string("""
#:import CustomListView valle.component.listview.CustomListView
#:import BotonImg valle.component.botonimg.BotonImg
#:import LabelClicable valle.component.labelclicable.LabelClicable

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
        CustomListView:
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
            BotonImg:
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
        s = tag.servido.get()
        s = "False" if s == "True" else "True"
        root.bgColor = (0, .01, 0, 1) if s == "True" else (.1, .1, .1, 1)
        tag.servido.set(s)
        tag.save()
        query = "IDPedido={0} AND servido='False'".format(tag.IDPedido.get())


    def rm(self, root, tag):
        tag.remove()
        self.view.remove_widget(root)


    def mostra_pedidos(self, dt):
        pedidos = Pedido().find("servido='False'")

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
        val = json.loads(val)
        for s in  val:
            fl = s.get('fl')
            db = s.get('db')
            p = Pedido()
            p.fecha.set(db.get("fecha"))
            p.modo_pago.set(db.get("modo_pago"))
            p.num_avisador.set(db.get("num_avisador"))
            p.para_llevar.set(db.get("para_llevar"))
            p.num_tlf.set(db.get("num_tlf"))
            p.total.set(db.get("total"))
            p.save()
            for l in db.get("lineas"):
                linea = LineasPedido()
                linea.cant.set(l.get("cant"))
                linea.des.set(l.get("des"))
                linea.precio.set(l.get("precio"))
                linea.text.set(l.get("text"))
                linea.total.set(l.get("total"))
                linea.tipo.set(l.get("tipo"))
                linea.imprimible.set(self.esImprimible(l))
                p.lineas.add(linea)

            data={"fl":fl}
            data = urllib.urlencode(data)
            headers = {'Content-type': 'application/x-www-form-urlencoded',
                       'Accept': 'text/json'}
            r = UrlRequest("http://192.168.0.102:8000/pedidos/servido/",
                            on_success=self.echo, req_body=data, req_headers=headers, method="POST")

        Clock.schedule_once(self.pedidos, 5)

    def echo(self, request, val):
        pass

    def esImprimible(self, val):
        if val.get("tipo") == "refresco" or val.get("tipo") == "postre":
            return "False"
        else:
            return "True"

    def pedidos(self, dt):
        r = UrlRequest("http://192.168.0.102:8000/pedidos/", self.got_json)


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
