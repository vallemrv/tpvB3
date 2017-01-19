from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
from uix.editor import Editor
from uix.menu import Menu

Builder.load_string('''
<Gestor>:
    anchor_x: 'center'
    anchor_y: 'center'
''')
class Gestor(AnchorLayout):
    def __init__(self, **kargs):
        super(Gestor, self).__init__(**kargs)
        self.editor = Editor(exit=self.show_menu)
        self.menu = Menu(show_editor=self.show_editor)
        self.add_widget(self.menu)

    def show_editor(self, code):
        self.remove_widget(self.menu)
        self.editor.show_editor(code)
        self.add_widget(self.editor)

    def show_menu(self):
        self.remove_widget(self.editor)
        self.add_widget(self.menu)
