# @Author: Manuel Rodriguez <valle>
# @Date:   15-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: menu.py
# @Last modified by:   valle
# @Last modified time: 16-Jul-2017
# @License: Apache license vesion 2.0


from components.pagenavigations import PageManager
from components.buttons import ButtonIcon
import components.resources as res

from kivy.properties import ObjectProperty, ListProperty
from kivy.lang import  Builder

Builder.load_string('''
#:import ValleListView components.listview.ValleListView
#:import Familias controllers.familias.Familias
#:import Productos controllers.productos.Productos
<Gestion>:
    menu: _menu
    MainPage:
        title: 'Menu'
        ValleListView:
            bgColor: "#ffffff"
            id: _menu
            spacing: -1
    Page:
        id_page: "familias"
        title: "Familias"
        Familias:

    Page:
        id_page: "productos"
        title: "Productos"
        Productos:
                    ''')

class Gestion(PageManager):
    menu = ObjectProperty(None)
    items = ListProperty([
        {'icon': res.FA_CUBES,
         'text': "Familias",
         'bgColor': '#FFFFFf',
         'nav': 'familias'},
        {'icon': res.FA_CUTLERY,
         'text': "Productos",
         'bgColor': '#FFFFFf',
         'nav': 'productos'},
        ])

    def __init__(self, **kargs):
        super(Gestion, self).__init__(**kargs)


    def on_menu(self, w, val):
        for item in self.items:
            btn = ButtonIcon(text=item.get('text'), bgColor=item.get('bgColor'),
                             icon=item.get('icon'), orientation='horizontal',
                             color=(0,0,0,1),
                             border_size='1', font_size='25dp',
                             tag=item, on_press=self.on_press)

            self.menu.add_linea(btn)

    def on_press(self, btn):
        self.navigate(btn.tag.get('nav'))
