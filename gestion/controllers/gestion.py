# @Author: Manuel Rodriguez <valle>
# @Date:   15-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: menu.py
# @Last modified by:   valle
# @Last modified time: 15-Jul-2017
# @License: Apache license vesion 2.0


from components.pagenavigations import PageManager
from components.buttons import ButtonIcon
import components.resources as res

from kivy.properties import ObjectProperty
from kivy.lang import  Builder

Builder.load_string('''
#:import ValleListView components.listview.ValleListView
<Gestion>:
    menu: _menu
    MainPage:
        title: 'Menu'
        ValleListView:
            id: _menu
            spacing: -1
                    ''')

class Gestion(PageManager):
    menu = ObjectProperty(None)
    items = ListProperty([])
    def __init__(self, **kargs):
        super(Gestion, self).__init__(**kargs)
        self.items = [
            {'icon': res.FA_CUBES,
             'text': "Alta familias",
             'bgColor': '#ffffff',
             'nav': 'add_familias'}
        ]

    def on_menu(self, w, val):
        for item in self.items:
            btn = ButtonsIcon(text=item.get('text'), bgColor=item.get('bgColor'),
                              icon=item.get('icon'), orientation='horizontal',
                              border_size='1', font_size='25dp')

            btn.bind(on_press=self.navigate(item.get('nav')))
            self.menu.add_linea(btn)
