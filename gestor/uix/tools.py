from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.lang import Builder

Builder.load_string('''
<ToolsClases>:
    orientation: 'vertical'
    spacing: 10
    size_hint: .9, .9
    Label:
        size_hint_y: .1
        color: 0,0,0,1
        font_size: 25
        text: 'Editar clase'
    TextInput:
        size_hint_y: None
        height: 30
        id: _nombre
        hint_text: 'Nombre'
    ColorPicker:
        size_hint_y: .7
        id: _color
    BoxLayout:
        size_hint_y: .1
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
''')

class ToolsProductos(BoxLayout):
    pass

class ToolsClases(BoxLayout):
    exit = ObjectProperty(None, allownone=True)
    modificar = ObjectProperty(None, allownone=True)
    code = StringProperty("clases")
    lista = ListProperty()
    def __init__(self, **kargs):
        super(ToolsClases, self).__init__(**kargs)
        self.clase = None

    def borrar(self):
        if self.clase:
            self.lista.remove(self.clase)
            self.modificar(self.code, self.lista)

    def editar(self, obj):
        self.clase = obj
        self.ids._nombre.text = obj.get('text')
        self.ids._color.hex_color = obj.get('color')

    def on_press(self):
        if self.clase:
            self.clase['text'] = self.ids._nombre.text
            self.clase['color'] = self.ids._color.hex_color
            self.clase['tipo'] = 'clase'
            self.clase['productos'] = "db/{0}.json".format(
                                              self.ids._nombre.text.lower())
        else:
            self.clase = {'text': self.ids._nombre.text,
                          'color': self.ids._color.hex_color,
                          'tipo': 'clase',
                          'porductos': "db/{0}.json".format(
                                                self.ids._nombre.text.lower()),
                          'preguntas': []}
            self.lista.append(self.clase)

        self.clase = None
        self.modificar(self.code, self.lista)
