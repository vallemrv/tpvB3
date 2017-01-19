# -*- coding: utf-8 -*
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
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
    text: root.texto
  Button:
    size_hint_x: .2
    onPress: root.borrar(root)
    Image:
      source: './img/papelera.png'
      allow_stretch: True
      pos: self.parent.pos
      size: self.parent.width, self.parent.height - 1
''')

class LineaWidget(BoxLayout):
    UID = StringProperty("")
    borrar = ObjectProperty(None, allownone=True)
    texto = StringProperty("")
