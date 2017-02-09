from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_string('''
<LabelClicable>:
    font_size: 20
    color: .9, .9, .9, 1
    texto: ""
    tag: None
    Button:
        on_press: root.onPress(root)
        AnchorLayout:
            anchor_y: 'top'
            anchor_x: 'left'
            size: self.parent.size
            pos: self.parent.pos
            Label:
                color: root.color
                font_size: root.font_size
                text: root.texto
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                    ''')

class LabelClicable(BoxLayout):
    event = ObjectProperty(None)
    def onPress(self, obj):
        if self.event:
            self.event(obj)
