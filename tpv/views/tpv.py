# @Author: Manuel Rodriguez <valle>
# @Date:   29-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Filename: tpv.py
# @Last modified by:   valle
# @Last modified time: 02-Sep-2017
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from views.inicio import Inicio

Builder.load_string('''
#:import GridButtons components.gridbuttons.GridButtons
#:import ButtonImg components.buttons.ButtonImg
<Tpv>:
    anchor_y: 'center'
    anchor_x: 'center'
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            size: self.size
            pos: self.pos

''')

class Tpv(AnchorLayout):
    def __init__(self, **kargs):
        super(Tpv, self).__init__(**kargs)
        self.inicio = Inicio()
        self.add_widget(self.inicio)
