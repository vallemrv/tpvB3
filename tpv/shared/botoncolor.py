from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.properties import ObjectProperty, StringProperty

class BotonColor (Button):
    bColor = StringProperty('')
    tag = ObjectProperty(None, allownone=True)

    def __init__(self, **kargs):
        super(BotonColor, self).__init__(**kargs)
        self.background_normal = ''
        self.border = (3, 3, 3, 3)
        self.font_size = 30

    def on_bColor(self, key, value):
        self.background_color = get_color_from_hex(value)
