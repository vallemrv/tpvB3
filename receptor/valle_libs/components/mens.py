# @Author: Manuel Rodriguez <valle>
# @Date:   20-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: mensaje.py
# @Last modified by:   valle
# @Last modified time: 13-Aug-2017
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_string('''
#:import get_color kivy.utils.get_color_from_hex
<FloatMen>:
    anchor_x: 'center'
    anchor_y: 'top'
    AnchorLayout:
        anchor_y: 'center'
        anchor_x: 'center'
        size_hint: 1, .5
        Label:
            size_hint: .9,.9
            text_size: self.size
            valign: 'center'
            halign: 'center'
            text: root.men
            font_size: root.font_size
            color: get_color(root.color)
                        ''')


class FloatMen(AnchorLayout):
    men = StringProperty('')
    font_size = StringProperty('30dp')
    color = StringProperty("#000000")
