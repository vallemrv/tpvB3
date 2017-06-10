# coding=utf-8
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.listview import ListView
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty, StringProperty, OptionProperty
from kivy.lang import Builder
from kivy.uix.button import Button

Builder.load_string('''
<DialogColor>:
    color: _color
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
            hex_color: root.color_init
        Button:
            size_hint_y: None
            text: 'Elegir'
            on_press: root.dismiss()
            height: 40

#:import CustomListView valle.component.listview.CustomListView
<ToolsClases>:
    anchor_x: 'center'
    anchor_y: 'center'
    listPreguntas: _pregutas
    nombre: _nombre
    titulo: _titulo
    color: _color
    precio: _precio
    impresora: _impresora
    nuevo: None
    guardar: None
    exit: None
    setTitulo: None
    borrar: None
    GridLayout:
        cols: 1
        spacing: 10
        size_hint: 1, .85
        Label:
            size_hint_y: None
            height: 30
            color: 0,0,0,1
            font_size: 25
            text: 'Editar Titulo'
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
                on_press: root.setTitulo
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
                id: _color
                hint_text: 'Color'
            Button:
                size_hint: .15, None
                height: 30
                text: '...'
                on_press: root.show_modal()
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 5
            orientation: 'horizontal'
            Button:
                text: 'Nuevo'
                on_press: root.nuevo
            Button:
                text: 'Grabar'
                on_press: root.guardar
            Button:
                text: 'Borrar'
                on_press: root.borrar
            Button:
                text: 'Exit'
                on_press: root.exit
        Label:
            size_hint_y: None
            height: 30
            color: 0,0,0,1
            font_size: 25
            text: 'Editar Preguntas'
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
        CustomListView:
            id: _pregutas


''')

class DialogColor(ModalView):
    color_init = StringProperty('#000000')
    def getColor(self):
        return self.color.hex_color

    def set_color(self, color):
        self.color.hex_color = color


class Tools(AnchorLayout):
    tipo = OptionProperty("clase", options=["clase", "producto", "pregunta"])
    obj = ObjectProperty(None, allowNone=True)
    editar_pregunta = ObjectProperty(None, allowNone=True)
    modal = ObjectProperty(DialogColor())
    def __init__(self, **kargs):
        super(Tools, self).__init__(**kargs)
        self.modal.bind(on_dismiss=self.set_color)

    def on_tipo(self, obj, val):
        if val == "clase":
            self.remove_widget(self.impresora)
            self.remove_widget(self.precio)
        elif val == "pregunta":
            self.remove_widget(self.impresora)


    def get_valores(self):
        if self.obj:
            self.obj['text'] = self.nombre.text
            self.obj['color'] = self.color.text
            self.obj['tipo'] = self.tipo.text
            self.obj['impresora'] = self.impresora.text
            self.obj['precio'] = self.precio.text
        else:
            self.obj = {'text': self.nombre.text,
                        'color': self.color.text,
                        'tipo': self.tipo,
                        'precio': self.precio.text,
                        'productos': self.nombre.text,
                        'preguntas': [],
                        'modificadores': [],
                        'impresora': self.impresora.text}
        return self.obj

    def set_color(self, obj):
        self.ids._color.text = self.modal.getColor()

    def new(self):
        self.obj = None
        self.nombre.text = ""
        self.color.text = ""
        self.precio.text = ""
        self.impresora.text = ""
        self.tipo.text = ""
        self.listPreguntas.rm_all_widgets()

    def set_valores(self, obj):
        self.obj = obj
        self._nombre.text = obj.get('text')
        self.color.text = obj.get('color')
        self.precio.text = str(obj.get('precio'))
        self.impresora.text = obj.get('impresora')
        for l in self.obj.get("preguntas"):
            self.listPreguntas.add_linea(Button(text=l, on_press=self._editar_pregunta))

    def _editar_pregunta(self, boton):
        if editar_pregunta:
            editar_pregunta(boton.text)

    def show_modal(self):
        self.modal.set_color(self.color.text)
        self.modal.open()
