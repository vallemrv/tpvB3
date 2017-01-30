from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder

Builder.load_string('''
<DialogColor>:
    id: _dialogo
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
    GridLayout:
        size_hint: .85, .85
        cols: 1
        spacing: 10
        Label:
            size_hint_y: None
            font_size: 25
            text: 'Escoge un color'
            height: 40
        ColorPicker:
            size_hint_y: .7
            id: _color
            hex_color: root.color
        Button:
            size_hint_y: None
            text: 'Elegir'
            on_press: root.dismiss()
            height: 40

<ToolsClases>:
    anchor_x: 'center'
    anchor_y: 'center'
    GridLayout:
        cols: 1
        spacing: 10
        size_hint: 1, .85
        Label:
            size_hint_y: None
            height: 30
            color: 0,0,0,1
            font_size: 25
            text: 'Editar clase'
        TextInput:
            size_hint_y: None
            height: 30
            id: _nombre
            hint_text: 'Nombre'
        TextInput:
            size_hint_y: None
            height: 30
            id: _tipo
            hint_text: 'Tipo'
        TextInput:
            size_hint_y: None
            height: 30
            id: _precio
            hint_text: 'Precio'
        TextInput:
            size_hint_y: None
            height: 30
            id: _impresora
            hint_text: 'Impresora'
        BoxLayout:
            size_hint_y: None
            height: 40
            orientation: 'horizontal'
            spacing: 5
            TextInput:
                size_hint_y: None
                height: 30
                id: _titulo
                hint_text: 'Titulo teclado'
                text: root.titulo
            Button:
                size_hint: .15, None
                height: 30
                text: '...'
                on_press: root.setTitulo()

        BoxLayout:
            size_hint_y: None
            height: 40
            orientation: 'horizontal'
            spacing: 5
            TextInput:
                size_hint_y: None
                height: 30
                id: _color
                hint_text: 'Color'
            Button:
                size_hint: .15, None
                height: 30
                text: '...'
                on_press: root.show_modal()
        BoxLayout:
            size_hint_y: None
            height: 60
            spacing: 5
            orientation: 'horizontal'
            Button:
                text: 'Grabar'
                on_press: root.on_press()
            Button:
                text: 'Borrar'
                on_press: root.borrar()
            Button:
                text: 'Exit'
                on_press: root.exit()
        BoxLayout:
            size_hint_y: None
            height: 40
            orientation: 'horizontal'
            spacing: 5
            TextInput:
                size_hint_y: None
                height: 30
                id: _pregunta
                hint_text: 'Crear preguntas'
            Button:
                size_hint: .15, None
                height: 30
                text: '...'
                on_press: root.crear_preguntas()

''')

class DialogColor(ModalView):
    color = StringProperty('#000000')
    def getColor(self):
        return self.ids._color.hex_color

class ToolsClases(AnchorLayout):
    exit = ObjectProperty(None, allownone=True)
    refresh = ObjectProperty(None, allownone=True)
    storage = ObjectProperty(None, allownone=True)
    show = ObjectProperty(None, allownone=True)
    titulo = StringProperty("")

    def __init__(self, **kargs):
        super(ToolsClases, self).__init__(**kargs)
        self.clase = None
        self.modal = DialogColor()
        self.modal.bind(on_dismiss=self.set_color)
        self.ids._color.text = self.modal.getColor()

    def crear_preguntas(self):
        if self.clase:
            db = "db/preguntas/{0}.json".format(self.ids._pregunta.text)
            if db not in self.clase['preguntas']:
                self.clase['preguntas'].append(db)
                self.clase = None
                self.storage.put('db', lista=self.lista)
            self.show(db)

    def on_storage(self, key, value):
        self.titulo = self.storage['titulo'].get('text')
        self.lista = self.storage['db'].get('lista')

    def setTitulo(self):
        self.titulo = self.ids._titulo.text
        self.storage.put('titulo', text=self.titulo)
        self.refresh()

    def borrar(self):
        if self.clase:
            self.lista.remove(self.clase)
            self.storage.put('db', lista=self.lista)
            self.refresh()


    def set_color(self, obj):
        self.ids._color.text = self.modal.getColor()

    def editar(self, obj):
        self.clase = obj
        self.ids._nombre.text = obj.get('text')
        self.ids._color.text = obj.get('color')
        self.ids._precio.text = str(obj.get('precio'))
        self.ids._impresora.text = obj.get('impresora')
        self.ids._tipo.text = obj.get('tipo')

    def show_modal(self):
        self.modal.color = self.ids._color.text
        self.modal.open()

    def on_press(self):
        if self.clase:
            self.clase['text'] = self.ids._nombre.text
            self.clase['color'] = self.ids._color.text
            self.clase['tipo'] = self.ids._tipo.text
            self.clase['productos'] = ""
            self.clase['preguntas'] = []
            self.clase['modificadores'] = []
            self.clase['impresora'] = self.ids._impresora.text
            self.clase['precio'] = self.ids._precio.text
        else:
            self.clase = {'text': self.ids._nombre.text,
                          'color': self.ids._color.text,
                          'tipo': self.ids._tipo.text,
                          'productos': "",
                          'precio': self.ids._precio.text,
                          'preguntas': [],
                          'modificadores': [],
                          'impresora': self.ids._impresora.text}
            self.lista.append(self.clase)

        self.clase = None
        self.storage.put('db', lista=self.lista)
        self.refresh()
