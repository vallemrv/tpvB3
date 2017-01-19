from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from shared.utils import json_to_list
from uix.tools import ToolsClases

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
        anchor_x: 'center'
        anchor_y: 'center'
        id: _tools
''')

class Editor(BoxLayout):
    exit = ObjectProperty(None, allownone=True)
    def onPress(self, btn):
        self.tools.editar(btn.tag)

    def show_editor(self, code):
        self.storage = JsonStore('db/{0}.json'.format(code))
        if not self.storage.exists(code):
            self.storage.put(code, lista=[])
        self.ids._botonera.titulo = code.upper()
        self.refres_botones(code)
        self.show_tools(code)

    def refres_botones(self, code):
        self.ids._botonera.botones = [] 
        self.ids._botonera.botones = json_to_list(
                                    self.storage[code].get('lista'))


    def show_tools(self, code):
        self.ids._tools.clear_widgets()
        if code == 'clases':
            self.tools = ToolsClases(modificar=self.modificar,
                                     exit=self.exit,
                                     lista=self.storage[code].get('lista'))
            self.ids._tools.add_widget(self.tools)

    def modificar(self, code, lista):
        self.storage.put(code, lista=lista)
        self.refres_botones(code)
