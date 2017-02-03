# -*- coding: utf-8 -*-
from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
from valle.tpv.impresora import DocPrint
from controllers.inicio import Inicio
from controllers.pedido import PedidoController
from kivy.clock import Clock
from glob import glob
from os import rename

Builder.load_string('''
<tpv>:
    Carousel:
        direction: 'right'
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'center'
            id: _pageUno
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'center'
            id: _pageDos
            canvas:
                Color:
                    rgba: 1,1,1,1
                Rectangle:
                    size: self.size
                    pos: self.pos
            Label:
                text: 'Lista de pedidos'
                    ''')

class Tpv(AnchorLayout):

    def __init__(self, **kargs):
        super(Tpv, self).__init__(**kargs)
        self.inicio = Inicio(controller=self.onPress_seccion)
        self.pedido = PedidoController(tpv=self)
        self.ids._pageUno.add_widget(self.inicio)
        self.docPrint = DocPrint()
        Clock.schedule_interval(self.enviar_pedido, .5)

    def onPress_seccion(self, btns):
        for btn in btns:
            tipo = btn.tag.get('tipo')
            if tipo == 'clase':
                self.ids._pageUno.remove_widget(self.inicio)
                self.ids._pageUno.add_widget(self.pedido)
                self.pedido.nuevo_pedido(btn.tag)
            elif tipo == "abrir_cajon":
                self.abrir_cajon()

    def imprimirTicket(self, pd):
        tk = pd['tk']['reg']
        self.docPrint.imprimirTicket("caja", tk.get('numTicket'),
                                     tk.get('lineas'), tk.get('fecha'),
                                     tk.get('total'))


    def abrir_cajon(self):
        self.docPrint.initDoc()
        self.docPrint.abrir_cajon('caja')

    def enviar_pedido(self, pd):
        list = glob('db/pd/*.00.json')
        for l in list:
            db = l.replace(".00.", ".11.")
            rename(l, db)
            st = JsonStore(db)
            if st.exists('tk'):
                tk = st['tk']['reg']
                self.docPrint.printPedido("cocina", tk.get('num_avisador'),
                                          tk.get('lineas'), tk.get('fecha'),
                                          tk.get('para_llevar'))

    def mostrar_inicio(self):
        self.ids._pageUno.remove_widget(self.pedido)
        self.ids._pageUno.add_widget(self.inicio)
