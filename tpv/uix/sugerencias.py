from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.lang import Builder

Builder.load_string('''
#:import Botonera shared.botonera.Botonera
#:import VTeclado shared.vteclado.VTeclado
<Sugerencias>:
    canvas:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            size: root.size
            pos: root.pos
    des: 'Descrpicion'
    GridLayout:
        cols: 1
        padding: 20
        Label:
            text: "Sugerencias"
            size_hint_y: None
            height: 40
            font_size: 30
            color: 0,0,0,1
        BoxLayout:
            spacing: 5
            orientation: 'horizontal'
            AnchorLayout:
                size_hint_x: .7
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
                        id: _contenido_sug
            GridLayout:
                cols: 1
                spacing: 5
                size_hint_x: .3
                Label:
                    text: "Descrpicion"
                    size_hint_y: None
                    height: 40
                    font_size: 30
                    color: 0,0,0,1
                Label:
                    canvas.before:
                        Color:
                            rgba: .5, .5, .5, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    padding: 10, 10
                    text: root.des
                    size_hint_y: None
                    height: 90
                    font_size: 24
                    color: 1, 1, 1, 1
                    text_size: self.size
                    halign: 'left'
                    valign: 'middle'
                Label:
                    canvas.before:
                        Color:
                            rgba: .5, .5, .5, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    padding: 10, 10
                    text: root.texto
                    size_hint_y: None
                    height: 90
                    font_size: 24
                    color: 1, 1, 1, 1
                    text_size: self.size
                    halign: 'left'
                    valign: 'middle'
        VTeclado:
            id: _dock
            tipo: 'letras'
                   ''')

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
        self.ids._dock.bind(texto=self.on_text)
        self.ids._dock.exit = self.content_exit
        self.bind(sug=self.on_sug)

    def on_sug(self, key, value):
        self.ids._contenido_sug.clear_widgets()
        for item in self.sug:
            btn = Button(text=item.get('text'))
            btn.tag = item
            btn.bind(on_press=self.onPress)
            self.ids._contenido_sug.add_widget(btn)

    def onPress(self, b):
        self.onExit(self.key, self.content, b.tag, self.tag)

    def on_text(self, key, value):
        self.texto = value

    def clear_text(self):
        self.texto = ""
        self.ids._dock.texto = self.texto

    def content_exit(self):
        if self.onExit:
            value = {'text': self.texto, 'precio': 0.0, "modificadores": []}
            if self.texto != "":
                self.sug.append(value)
            self.onExit(self.key, self.content, value, self.tag)
