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
        self.dock.bind(texto=self.on_text)
        self.dock.exit = self.content_exit
        self.bind(sug=self.on_sug)

    def on_sug(self, key, value):
        self.lista.rm_all_widgets()
        for item in self.sug:
            btn = Button(text=item.get('text'))
            btn.tag = item
            btn.bind(on_press=self.onPress)
            self.lista.add_linea(btn)

    def onPress(self, b):
        self.onExit(self.key, self.content, b.tag, self.tag)

    def on_text(self, key, value):
        self.texto = value

    def clear_text(self):
        self.texto = ""
        self.dock.texto = self.texto

    def content_exit(self):
        self.texto = self.txtSug.text
        if self.onExit:
            value = {'text': self.texto, 'precio': 0.0, "modificadores": []}
            if self.texto != "":
                self.sug.append(value)
            self.onExit(self.key, self.content, value, self.tag)
