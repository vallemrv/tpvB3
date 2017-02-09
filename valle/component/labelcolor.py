from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.properties import StringProperty

Builder.load_string('''
<LabelColor>:
    _color: 0, 0, 0, 1
    canvas.before:
        Color:
            rgba: root._color
        Rectangle:
            size: self.size
            pos: self.pos
    font_size: 30
                    ''')

class LabelColor(Label):
    bColor = StringProperty()

    def on_bColor(self, key, value):
        self._color = get_color_from_hex(value)
