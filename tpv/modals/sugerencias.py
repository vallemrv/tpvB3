# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 23-Feb-2018
# @License: Apache license vesion 2.0


from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.lang import Builder

Builder.load_file("view/sugerencias.kv")

class Sugerencias(ModalView):
    onExit = ObjectProperty(None, allownone=True)
    content = ObjectProperty(None, allownone=True)
    texto = StringProperty("")
    des = StringProperty("")
    sug = ListProperty([])
    key = StringProperty("")
    tag = ObjectProperty(None, allownone=True)

    def __init__(self, **kargs):
        super(Sugerencias, self).__init__(**kargs)
        self.auto_dismiss=False

    def on_sug(self, key, value):
        self.lista.rm_all_widgets()
        for item in self.sug:
            btn = Button(text=item)
            btn.tag = item
            btn.bind(on_press=self.onPress)
            self.lista.add_linea(btn)

    def onPress(self, b):
        self.onExit(self.key, self.content, b.tag, self.tag)

    def clear_text(self):
        self.texto = ""

    def exit(self):
        self.texto = self.txtSug.text
        if self.onExit:
            if self.texto != "":
                self.sug.append(self.texto)
            self.onExit(self.key, self.content, self.texto, self.tag)
