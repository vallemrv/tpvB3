# -*- coding: utf-8 -*
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.lang import Builder

Builder.load_string('''
<LineaWidget>:
  canvas.before:
    Color:
      rgba: .3,.3,.3,1
    Rectangle:
      size: self.size
      pos: self.pos
  spacing: 5
  orientation: 'horizontal'
  Label:
    color: .9,.9,.9,1
    size_hint_x: .8
    text: "{0}  {1:.2f}".format(root.texto, root.total)
  Button:
    size_hint_x: .2
    on_press: root.borrar(root, root.tag)
    Image:
      source: './img/papelera.png'
      allow_stretch: True
      pos: self.parent.pos
      size: self.parent.width, self.parent.height - 1
''')

class LineaWidget(BoxLayout):
    tag = ObjectProperty(None, allownone=True)
    borrar = ObjectProperty(None, allownone=True)
    texto = StringProperty("")
    total = NumericProperty(0.0)
