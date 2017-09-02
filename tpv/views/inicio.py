# @Author: Manuel Rodriguez <valle>
# @Date:   29-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Filename: inicio.py
# @Last modified by:   valle
# @Last modified time: 02-Sep-2017
# @License: Apache license vesion 2.0

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_string('''
<ToolsButtons@ButtonImg>:
    bgColor: "#eae5f0"
    border_size: 1

<Inicio>:
    orientation: 'horizontal'
    size_hint: .92, .95

    GridButtons:
        size_hint: .95, 1
        tpv: None
        orientation: 'horizontal'
        id: _content

    AnchorLayout:
        size_hint: None, 1
        width: dp(70)
        anchor_x: 'right'
        anchor_y: 'top'

        GridLayout:
            cols: 1
            spacing: 2
            size_hint: 1, None
            height: len(self.children) * 70
            ToolsButtons:
                src: 'tpv/img/llevar.png'
                on_press: root.tpv.mostrar_domicilio()
            ToolsButtons:
                src: 'tpv/img/listapd.png'
                on_press: root.tpv.mostrar_pendientes()
            ToolsButtons:
                src: 'tpv/img/lista.png'
                on_press: root.tpv.mostrar_pedidos()
            ToolsButtons:
                src: 'tpv/img/arqueo.jpeg'
                on_press: root.tpv.mostrar_arqueo()
            ToolsButtons:
                src: 'tpv/img/llave.png'

''')
class Inicio(BoxLayout):
    controller = ObjectProperty()
    def __init__(self, **kargs):
        super(Inicio, self).__init__(**kargs)


    def draw_botonera(self, botones):
        self.contente.titulo = 'Inicio'
        self.content.botones = self.botones
        self.content.onPress = self.on_press


    def on_press(self, btns):
        print btns
