from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from menu import Menu
from uix.editor import Editor
Builder.load_string('''
#!import Botonera valle.component.botonera.Botonera
<Selector>:
    anchor_x: 'center'
    anchor_y: 'center'
    Botonera:
        size_hint: .9, .9
        completo: True
        onPress: root.onPress
        font_size: 20
        id: _botonera

<Gestor>:
    anchor_x: 'center'
    anchor_y: 'center'
''')

class Selector(AnchorLayout):
    onPress = ObjectProperty(None, allownone=True)

    def setDB(self, db):
        self.storage = JsonStore(db)
        self.ids._botonera.titulo = "Elige una clase"
        self.ids._botonera.botones = self.storage['db'].get('lista')

    def setProductosDB(self):
        aux = self.ids._botonera.botones
        self.storage.put('db', lista=aux)

class Gestor(AnchorLayout):
    def __init__(self, **kargs):
        super(Gestor, self).__init__(**kargs)
        #self.menu = Menu(action=self.on_action_menu)
        #self.familias = EditorFamilias(action=self.on_action_familias)
        #self.productos = EditorProductos(action=self.on_action_productos)
        #self.add_widget(self.menu)


        self.editor = Editor(exit=self.show_menu)
        self.menu = Menu(acion=self.edit_clases,
                         edit_productos=self.show_selector_clase)
        self.productos = Selector(onPress=self.edit_productos)
        self.productos.setDB('db/clases.json')
        self.add_widget(self.menu)

    def on_action_familias(self, action):
        pass

    def on_action_productos(self, action):
        pass

    def on_action_menu(self, action):
        self.clear_widgets()
        if action == "menu":
            self.add_widget(self.menu)
        elif action == "familias":
            self.add_widget(self.familias)
        elif action == "productos":
            self.add_widget(self.productos)

    def edit_productos(self, btn):
        nombre = btn[0].tag.get('text').lower()
        db = 'db/productos/{0}.json'.format(nombre)
        btn[0].tag['productos'] = db
        self.productos.setProductosDB()
        self.remove_widget(self.menu)
        self.remove_widget(self.productos)
        self.editor.show_editor(db)
        self.add_widget(self.editor)

    def show_selector_clase(self):
        self.remove_widget(self.menu)
        self.remove_widget(self.editor)
        self.add_widget(self.productos)

    def edit_clases(self):
        self.remove_widget(self.menu)
        self.remove_widget(self.productos)
        self.editor.show_editor('db/clases.json')
        self.add_widget(self.editor)

    def show_menu(self):
        self.remove_widget(self.productos)
        self.remove_widget(self.editor)
        self.add_widget(self.menu)
