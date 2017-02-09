from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.utils import get_color_from_hex

Builder.load_string('''
<CustomListView>:
    list: _listado
    scroll: _scroll
    canvas.before:
        Color:
            rgba: root._color
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
            spacing: 5
            padding: 5
            size_hint: 1, None
            height: len(self.children) * 70
            id: _listado
                    ''')

class CustomListView(AnchorLayout):
    bColor = StringProperty()
    _color = ListProperty([0, 0, 0, 1])

    def on_bColor(self, key, value):
        self._color = get_color_from_hex(value)

    def add_linea(self, widget):
        self.list.add_widget(widget)
        self.scroll.scroll_y = 0

    def rm_linea(self, widget):
        self.list.remove_widget(widget)

    def rm_all_widgets(self):
        self.list.clear_widgets()

    def scroll_up(self):
        self.scroll.scroll_y = .9
