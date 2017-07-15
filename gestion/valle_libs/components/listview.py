# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Filename: listview.py
# @Last modified by:   valle
# @Last modified time: 14-Jul-2017
# @License: Apache license vesion 2.0


from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.utils import get_color_from_hex

Builder.load_string('''
#:import get_color kivy.utils.get_color_from_hex
<ValleListView>:
    list: _listado
    scroll: _scroll
    spacing: 5
    ancho: 70
    canvas.before:
        Color:
            rgb: get_color(root.bgColor)
        Rectangle:
            size: self.size
            pos: self.pos
    anchor_x: 'center'
    anchor_y: 'center'
    ScrollView:
        id: _scroll
        size_hint: 1, 1
        GridLayout:
            cols: 1
            spacing: root.spacing
            size_hint: 1, None
            height: len(self.children) * dp(root.ancho)
            id: _listado
                    ''')

class ValleListView(AnchorLayout):
    bgColor = StringProperty("#b0a18a")

    def add_linea(self, widget):
        self.list.add_widget(widget)
        self.scroll.scroll_y = 0

    def rm_linea(self, widget):
        self.list.remove_widget(widget)

    def rm_all_widgets(self):
        self.list.clear_widgets()

    def scroll_up(self, up=1):
        self.scroll.scroll_y = up
