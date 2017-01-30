from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from uix.toolsclases import ToolsClases

Builder.load_string('''
#:import Botonera shared.botonera.Botonera
<Editor>:
    size_hint: .9, .9
    orientation: 'horizontal'
    spacing: 10
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        Botonera:
            size_hint: .9, .9
            completo: False
            onPress: root.onPress
            font_size: 20
            id: _botonera

    AnchorLayout:
        size_hint_x: .3
        anchor_x: 'center'
        anchor_y: 'center'
        id: _tools
''')

class Editor(BoxLayout):
    exit = ObjectProperty(None, allownone=True)

    def onPress(self, btn):
        self.tools.editar(btn[0].tag)


    def show_editor(self, db):
        self.storage = JsonStore(db)
        if not self.storage.exists('titulo'):
            self.crear_db()
        self.ids._botonera.titulo = str(self.storage['titulo'].get('text'))
        self.refresh_botones()
        self.show_tools()

    def crear_db(self):
        self.storage.put('titulo', text='Nuevo')
        self.storage.put('db', lista=[])

    def refresh_botones(self):
        self.ids._botonera.botones = []
        self.ids._botonera.botones = self.storage['db'].get('lista')
        self.ids._botonera.titulo = str(self.storage['titulo'].get('text'))


    def show_tools(self):
        self.ids._tools.clear_widgets()
        self.tools = ToolsClases(refresh=self.refresh_botones,
                                 exit=self.exit,
                                 storage=self.storage,
                                 show=self.show_editor)
        self.ids._tools.add_widget(self.tools)
